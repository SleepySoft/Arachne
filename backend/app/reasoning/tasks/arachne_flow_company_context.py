"""Arachne-flow company context reasoning: 公司在产业链中的位置与相关公司。

从公司（事实节点）出发：
  1. PG company_node_exposures -> 公司暴露的 legacy 产业节点（公司在产业中的位置）；
  2. 过滤出 flow 图中存在的节点，复用主线/支线关联推理（双向）展开产业链；
  3. 按节点相对于种子节点的位置把相关公司分为：
     - peers（同业）：暴露于种子公司相同环节、相同工艺 METHOD 或支线关联物料的公司；
     - upstream_companies（上游公司）：暴露于种子上游链（backward）节点的公司；
     - downstream_companies（下游公司）：暴露于种子下游链（forward）节点的公司。
"""

from __future__ import annotations

from typing import Any, Dict, List, Set

from app.reasoning.arachne_flow_adapter import validate_arachne_flow_sources
from app.reasoning.schemas import (
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TraversalDirection,
)
from app.reasoning.tasks.arachne_flow_association import (
    _suggest_flow_nodes,
    run_arachne_flow_association,
)
from app.services import company_storage


def _company_brief(company, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "company_id": company.company_id if company else None,
        "name_zh": company.name_zh if company else None,
        "name_en": company.name_en if company else None,
        "stock_codes": company.stock_codes if company else [],
        "listing_market": company.listing_market if company else None,
        "country": company.country if company else None,
        "nodes": nodes,
    }


async def run_arachne_flow_company_context(
    task: ReasoningTask,
    reasoning_id: str,
) -> ReasoningResultEnvelope:
    warnings: List[str] = []
    seed_company_ids = list(task.source_nodes)
    params = task.parameters or {}
    max_exposures = int(params.get("max_company_exposures", 100))

    # ---- 1. 公司 -> 暴露节点（产业位置） -----------------------------------
    seed_companies: List[Dict[str, Any]] = []
    exposed_ids: Set[str] = set()
    for cid in seed_company_ids:
        company = await company_storage.get_company(cid)
        if company is None:
            warnings.append(f"公司不存在: {cid}")
            continue
        exposures, _ = await company_storage.list_exposures_by_company(cid, limit=200)
        for e in exposures:
            exposed_ids.add(e.node_id)
        seed_companies.append(
            {
                "company_id": company.company_id,
                "name_zh": company.name_zh,
                "stock_codes": company.stock_codes,
                "listing_market": company.listing_market,
                "country": company.country,
                "exposures": exposures,
            }
        )
    if not exposed_ids:
        from app.reasoning.schemas import ReasoningDiagnostics
        from datetime import datetime

        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.NO_RESULT,
            generated_at=datetime.utcnow(),
            input_fingerprint="",
            output_types=[o.value for o in task.requested_outputs],
            result_payload={},
            diagnostics=ReasoningDiagnostics(
                warnings=warnings + ["种子公司没有任何节点暴露记录（company_node_exposures）"]
            ),
        )

    # ---- 2. 过滤到 flow 图存在的节点 ---------------------------------------
    existing, missing = await validate_arachne_flow_sources(sorted(exposed_ids))
    if missing:
        warnings.append(f"暴露节点中不在 flow 图（已忽略）: {missing}")
    if not existing:
        suggestions = await _suggest_flow_nodes(sorted(exposed_ids))
        from app.reasoning.schemas import ReasoningDiagnostics
        from datetime import datetime

        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.NO_RESULT,
            generated_at=datetime.utcnow(),
            input_fingerprint="",
            output_types=[o.value for o in task.requested_outputs],
            result_payload={"missing_flow_suggestions": suggestions},
            diagnostics=ReasoningDiagnostics(
                warnings=warnings + ["种子公司的暴露节点都不在 flow 图中"]
            ),
        )

    # ---- 3. 复用主线/支线推理（强制双向） ----------------------------------
    derived = task.model_copy(
        update={
            "source_nodes": existing,
            "constraints": task.constraints.model_copy(
                update={"traversal_direction": TraversalDirection.BOTH}
            ),
        }
    )
    result = await run_arachne_flow_association(derived, reasoning_id)
    if result.status != ResultStatus.SUCCESS:
        return result

    payload = result.result_payload
    tg = payload.get("temporary_graph") or {}
    tg_nodes = tg.get("nodes", [])
    props = {n["temp_node_id"]: n.get("properties", {}) for n in tg_nodes}
    labels = {n["temp_node_id"]: n.get("label") for n in tg_nodes}

    seed_set = set(existing)
    upstream_nodes = {
        nid for nid, p in props.items()
        if nid not in seed_set and "backward" in (p.get("direction") or "")
        and p.get("node_kind") in ("resource", "method")
    }
    downstream_nodes = {
        nid for nid, p in props.items()
        if nid not in seed_set and "forward" in (p.get("direction") or "")
        and p.get("node_kind") in ("resource", "method")
    }
    method_nodes = {nid for nid, p in props.items() if p.get("line") == "method"}
    branch_nodes = {
        nid for nid, p in props.items()
        if p.get("line") == "branch" and p.get("node_kind") == "resource"
    }

    # ---- 4. 相关公司分类 ----------------------------------------------------
    target_ids = sorted(seed_set | upstream_nodes | downstream_nodes | method_nodes | branch_nodes)
    exposures = await company_storage.list_exposures_by_nodes(target_ids, limit=max_exposures)
    company_ids = sorted({e.company_id for e in exposures})
    companies = await company_storage.get_companies_by_ids(company_ids)
    company_map = {c.company_id: c for c in companies}

    # 种子公司在每个节点上的活动类型（同业判定：同节点 + 同活动）
    seed_activity: Dict[str, str] = {}
    for sc in seed_companies:
        for e in sc["exposures"]:
            seed_activity.setdefault(e.node_id, e.activity_type or "")

    def node_brief(nid: str, activity: str | None = None) -> Dict[str, Any]:
        return {"node_id": nid, "label": labels.get(nid) or nid, "activity_type": activity}

    peers: Dict[str, List[Dict[str, Any]]] = {}
    related: Dict[str, List[Dict[str, Any]]] = {}
    upstream_cos: Dict[str, List[Dict[str, Any]]] = {}
    downstream_cos: Dict[str, List[Dict[str, Any]]] = {}
    seed_id_set = set(seed_company_ids)
    for e in exposures:
        if e.company_id in seed_id_set:
            continue
        entry = node_brief(e.node_id, e.activity_type)
        # 同业：暴露于种子公司相同节点且活动类型相同（如同为硅片生产商）
        if e.node_id in seed_set and e.activity_type == seed_activity.get(e.node_id):
            peers.setdefault(e.company_id, []).append(entry)
        # 相关：暴露于种子环节所用工艺 METHOD 或支线关联物料（产业配套/潜在竞合）
        elif e.node_id in method_nodes or e.node_id in branch_nodes:
            related.setdefault(e.company_id, []).append(entry)
        if e.node_id in upstream_nodes:
            upstream_cos.setdefault(e.company_id, []).append(entry)
        if e.node_id in downstream_nodes:
            downstream_cos.setdefault(e.company_id, []).append(entry)

    def to_list(grouped: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        out = [
            _company_brief(company_map.get(cid), nodes)
            for cid, nodes in grouped.items()
            if cid in company_map
        ]
        out.sort(key=lambda c: len(c["nodes"]), reverse=True)
        return out

    # 种子公司的产业位置：暴露节点 + 在 flow 图中的覆盖情况
    seed_out: List[Dict[str, Any]] = []
    for sc in seed_companies:
        pos = [
            node_brief(e.node_id, e.activity_type)
            for e in sc["exposures"]
            if e.node_id in props or e.node_id in seed_set
        ]
        seed_out.append(
            {
                "company_id": sc["company_id"],
                "name_zh": sc["name_zh"],
                "stock_codes": sc["stock_codes"],
                "listing_market": sc.get("listing_market"),
                "country": sc.get("country"),
                "position": pos,
                "exposed_node_count": len(sc["exposures"]),
                "in_flow_node_count": len([e for e in sc["exposures"] if e.node_id in existing]),
            }
        )

    payload["company_context"] = {
        "seed_companies": seed_out,
        "peers": to_list(peers),
        "related_companies": to_list(related),
        "upstream_companies": to_list(upstream_cos),
        "downstream_companies": to_list(downstream_cos),
        "categories": {
            "seed_nodes": sorted(seed_set),
            "upstream_nodes": sorted(upstream_nodes),
            "downstream_nodes": sorted(downstream_nodes),
            "method_nodes": sorted(method_nodes),
            "branch_nodes": sorted(branch_nodes),
        },
    }
    result.diagnostics.warnings = (result.diagnostics.warnings or []) + warnings
    return result
