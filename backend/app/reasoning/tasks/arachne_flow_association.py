"""Arachne-flow association reasoning: 主线深度遍历 + 支线广度扩展。

与旧的“机械 hop 计数”实现的区别：

- 主线（深度）：物料转化链。RESOURCE -> ACTION -> RESOURCE 计为 1 个工艺阶段，
  ACTION 本身不计深度。主线 ACTION 的其余投入作为该阶段的“协同投入”叶子挂上
  （回答“这一步还需要什么”），但不继续向外扩展。
- 支线（广度）：主线上每个 ACTION 经 ref 引用 METHOD（工艺）；从 METHOD 反向找到
  引用同一工艺的其他 ACTION（可跨流程文件），收集其投入/产出物料作为“关联物料”
  （回答“这个工艺还和什么相关”）。支线只扩 1 层，并按 method 限量防止爆炸。
- 启发性：node_scores 输出“关联强度”排序（资源连接的主线 ACTION 数 + 支线连接数），
  枢纽物料/工艺（多工艺共享）排在最前——共享工艺与共享物料正是瓶颈、替代与协同线索。
- 可选 include_company_exposures：主线+支线的 RESOURCE/METHOD 的 node_id 即 legacy
  产业节点 id，直接查 PG company_node_exposures 输出公司暴露。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from app.database_flow import get_flow_async_driver
from app.reasoning.arachne_flow_adapter import (
    INPUT_ROLES,
    OUTPUT_ROLES,
    validate_arachne_flow_sources,
)
from app.reasoning.schemas import (
    GraphType,
    NodeScore,
    OriginGraph,
    OutputType,
    ReasoningDiagnostics,
    ReasoningPath,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TempGraphEdge,
    TempGraphNode,
    TempGraphScope,
    TemporaryReasoningGraph,
)
from app.reasoning.tasks.utils import build_company_exposures
from app.services import node_storage

# 每个 METHOD 最多展开的兄弟 ACTION 数（支线广度上限）
DEFAULT_BRANCH_PER_METHOD = 5
# 支线关联物料总量上限
DEFAULT_BRANCH_LIMIT = 20
# 单个资源在每个阶段最多展开的主线 ACTION 数（广度收敛，防止枢纽资源爆图）
DEFAULT_MAX_ACTIONS_PER_RESOURCE = 4
# 每个主线 ACTION 最多挂出的协同投入叶子数
DEFAULT_MAX_SUPPORT_PER_ACTION = 8
# 每个资源节点最多携带的路径数（防止路径组合爆炸）
MAX_PATHS_PER_NODE = 3


# ---------------------------------------------------------------------------
# Cypher helpers (batched, one round-trip per stage)
# ---------------------------------------------------------------------------


async def _stage_expand(frontier: List[str], direction: str) -> List[Dict[str, Any]]:
    """按工艺阶段扩展 frontier 资源。

    forward（下游）: 资源 -[input]-> ACTION -[output]-> 产物；ACTION 的其余输入为协同投入。
    backward（上游）: 资源 <-[output]- ACTION <-[input]- 原料；ACTION 的其余产出为协同产出。
    每个 ACTION 占 0.5 跳语义——本函数一次返回“资源 -> ACTION -> 资源”的完整 1 阶段。
    """
    driver = get_flow_async_driver()
    if direction == "forward":
        cypher = """
        UNWIND $frontier AS rid
        MATCH (r:ArachneFlowNode {node_id: rid})-[e1:ARACHNE_FLOW]->(a:ArachneFlowNode)
        WHERE e1.edge_type IN $input_roles
        WITH rid, a, e1
        OPTIONAL MATCH (a)-[e2:ARACHNE_FLOW]->(r2:ArachneFlowNode)
        WHERE e2.edge_type IN $output_roles
        WITH rid, a, e1,
             collect(DISTINCT {node_id: r2.node_id, edge_id: e2.edge_id, role: e2.edge_type}) AS outputs
        OPTIONAL MATCH (s:ArachneFlowNode)-[e3:ARACHNE_FLOW]->(a)
        WHERE e3.edge_type IN $input_roles AND s.node_id <> rid
        RETURN rid, a.node_id AS action, e1.edge_id AS main_edge, e1.edge_type AS main_role,
               outputs,
               collect(DISTINCT {node_id: s.node_id, edge_id: e3.edge_id, role: e3.edge_type}) AS co_resources
        """
    else:
        cypher = """
        UNWIND $frontier AS rid
        MATCH (a:ArachneFlowNode)-[e1:ARACHNE_FLOW]->(r:ArachneFlowNode {node_id: rid})
        WHERE e1.edge_type IN $output_roles
        WITH rid, a, e1
        OPTIONAL MATCH (s:ArachneFlowNode)-[e2:ARACHNE_FLOW]->(a)
        WHERE e2.edge_type IN $input_roles AND s.node_id <> rid
        WITH rid, a, e1,
             collect(DISTINCT {node_id: s.node_id, edge_id: e2.edge_id, role: e2.edge_type}) AS inputs
        OPTIONAL MATCH (a)-[e3:ARACHNE_FLOW]->(o:ArachneFlowNode)
        WHERE e3.edge_type IN $output_roles AND o.node_id <> rid
        RETURN rid, a.node_id AS action, e1.edge_id AS main_edge, e1.edge_type AS main_role,
               inputs AS outputs,
               collect(DISTINCT {node_id: o.node_id, edge_id: e3.edge_id, role: e3.edge_type}) AS co_resources
        """
    async with driver.session() as session:
        result = await session.run(
            cypher,
            {
                "frontier": frontier,
                "input_roles": sorted(INPUT_ROLES),
                "output_roles": sorted(OUTPUT_ROLES),
            },
        )
        return [dict(record) async for record in result]


async def _action_io(action_ids: List[str]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """批量取 ACTION 的输入/输出资源边。"""
    if not action_ids:
        return {}
    driver = get_flow_async_driver()
    cypher = """
    UNWIND $actions AS aid
    OPTIONAL MATCH (s:ArachneFlowNode)-[e1:ARACHNE_FLOW]->(a:ArachneFlowNode {node_id: aid})
    WHERE e1.edge_type IN $input_roles
    WITH aid, collect(DISTINCT {node_id: s.node_id, edge_id: e1.edge_id, role: e1.edge_type}) AS inputs
    OPTIONAL MATCH (a:ArachneFlowNode {node_id: aid})-[e2:ARACHNE_FLOW]->(o:ArachneFlowNode)
    WHERE e2.edge_type IN $output_roles
    RETURN aid, inputs,
           collect(DISTINCT {node_id: o.node_id, edge_id: e2.edge_id, role: e2.edge_type}) AS outputs
    """
    out: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    async with driver.session() as session:
        result = await session.run(
            cypher,
            {
                "actions": action_ids,
                "input_roles": sorted(INPUT_ROLES),
                "output_roles": sorted(OUTPUT_ROLES),
            },
        )
        async for record in result:
            out[record["aid"]] = {"inputs": record["inputs"], "outputs": record["outputs"]}
    return out


async def _action_methods(action_ids: List[str]) -> Dict[str, str]:
    """ACTION -> 其 ref 引用的 METHOD。"""
    if not action_ids:
        return {}
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            UNWIND $actions AS aid
            MATCH (a:ArachneFlowNode {node_id: aid})-[e:ARACHNE_FLOW {edge_type: 'ref'}]->(m:ArachneFlowNode)
            RETURN aid, m.node_id AS method, e.edge_id AS edge_id
            """,
            {"actions": action_ids},
        )
        return {record["aid"]: record["method"] async for record in result}


async def _method_sibling_actions(
    method_ids: List[str], per_method: int
) -> Dict[str, List[str]]:
    """METHOD -> 引用它的所有 ACTION（每 method 限量）。"""
    if not method_ids:
        return {}
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            UNWIND $methods AS mid
            MATCH (a:ArachneFlowNode)-[:ARACHNE_FLOW {edge_type: 'ref'}]->(m:ArachneFlowNode {node_id: mid})
            RETURN mid, collect(DISTINCT a.node_id)[..$per] AS actions
            """,
            {"methods": method_ids, "per": per_method},
        )
        return {record["mid"]: record["actions"] async for record in result}


async def _node_kinds(node_ids: List[str]) -> Dict[str, str]:
    """node_id -> resource|action|method（按 ArachneFlow 标签判断）。"""
    if not node_ids:
        return {}
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:ArachneFlowNode) WHERE n.node_id IN $ids
            RETURN n.node_id AS id, labels(n) AS labels
            """,
            {"ids": node_ids},
        )
        kinds: Dict[str, str] = {}
        async for record in result:
            labels = set(record["labels"] or [])
            if "ArachneFlowResource" in labels:
                kinds[record["id"]] = "resource"
            elif "ArachneFlowAction" in labels:
                kinds[record["id"]] = "action"
            elif "ArachneFlowMethod" in labels:
                kinds[record["id"]] = "method"
            else:
                kinds[record["id"]] = "unknown"
        return kinds


async def _suggest_flow_nodes(query_ids: List[str], limit: int = 6) -> List[Dict[str, Any]]:
    """种子不在 flow 图中时，推荐图内真实存在的相似 RESOURCE/METHOD 节点。

    flow 引擎的种子必须来自已编译流程文件；用户从 PG 产业节点表里选来的种子
    很可能不在 flow 图中（如 foundry）。这里对图内节点做轻量相似匹配
    （id 子串 + PG 中文名子串 + SequenceMatcher），给出可直接点击的替代起点。
    """
    if not query_ids:
        return []
    from difflib import SequenceMatcher

    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:ArachneFlowNode)
            WHERE n:ArachneFlowResource OR n:ArachneFlowMethod
            RETURN n.node_id AS id
            """
        )
        flow_ids = [record["id"] async for record in result]
    if not flow_ids:
        return []

    name_map: Dict[str, str] = {}
    try:
        pg_nodes = await node_storage.get_nodes_by_ids(flow_ids)
        for nid, pn in pg_nodes.items():
            name_map[nid] = pn.canonical_name_zh or ""
    except Exception:
        pass

    def score(nid: str) -> float:
        name = name_map.get(nid, "")
        best = 0.0
        for q in query_ids:
            q = q.lower()
            if not q:
                continue
            if q in nid.lower() or (name and q in name.lower()):
                best = max(best, 1.0)
            else:
                best = max(
                    best,
                    SequenceMatcher(None, q, nid.lower()).ratio(),
                    SequenceMatcher(None, q, name.lower()).ratio() if name else 0.0,
                )
        return best

    scored = sorted(flow_ids, key=score, reverse=True)[:limit]
    return [
        {"node_id": nid, "label": name_map.get(nid) or nid, "score": round(score(nid), 3)}
        for nid in scored
    ]


# ---------------------------------------------------------------------------
# Main task
# ---------------------------------------------------------------------------


async def run_arachne_flow_association(
    task: ReasoningTask,
    reasoning_id: str,
) -> ReasoningResultEnvelope:
    """主线/支线双层关联推理（arachne_flow 引擎）。"""
    started_at = datetime.utcnow()
    diagnostics = ReasoningDiagnostics()
    warnings: List[str] = []

    max_depth = task.constraints.max_depth
    max_paths = task.constraints.max_paths
    max_nodes = task.constraints.max_nodes
    direction = task.constraints.traversal_direction.value
    params = task.parameters or {}

    branch_enabled = bool(params.get("expand_method_ref", True))
    branch_per_method = int(params.get("branch_per_method", DEFAULT_BRANCH_PER_METHOD))
    branch_limit = int(params.get("branch_limit", DEFAULT_BRANCH_LIMIT))
    max_actions_per_resource = int(
        params.get("max_actions_per_resource", DEFAULT_MAX_ACTIONS_PER_RESOURCE)
    )
    max_support_per_action = int(
        params.get("max_support_per_action", DEFAULT_MAX_SUPPORT_PER_ACTION)
    )

    # ---- 1. 种子校验与归类 ------------------------------------------------
    existing, missing = await validate_arachne_flow_sources(task.source_nodes)
    if missing:
        warnings.append(f"Missing source nodes in arachne_flow graph: {missing}")
        diagnostics.dangling_reference_count += len(missing)
    if not existing:
        suggestions = await _suggest_flow_nodes(missing)
        if suggestions:
            warnings.append("流程图内的相似可用起点见 missing_flow_suggestions")
        diagnostics.warnings = warnings
        diagnostics.execution_time_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)
        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.NO_RESULT,
            generated_at=datetime.utcnow(),
            input_fingerprint="",
            output_types=[o.value for o in task.requested_outputs],
            result_payload={"missing_flow_suggestions": suggestions},
            diagnostics=diagnostics,
        )

    kinds = await _node_kinds(existing)
    seed_resources: Set[str] = set()
    seed_actions: Set[str] = set()
    method_seeds: List[str] = []
    for nid in existing:
        kind = kinds.get(nid, "resource")
        if kind == "action":
            seed_actions.add(nid)
        elif kind == "method":
            method_seeds.append(nid)
        else:
            seed_resources.add(nid)
    if method_seeds:
        siblings = await _method_sibling_actions(method_seeds, branch_per_method)
        for mid, acts in siblings.items():
            seed_actions.update(acts)
        warnings.append(
            f"METHOD 种子经 ref 展开为 {len(seed_actions)} 个 ACTION: {method_seeds}"
        )

    # ---- 2. 主线 BFS（按工艺阶段；ACTION 不计深度） ------------------------
    # nodes: id -> {line, stage, direction, kind, via_action, via_method}
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Dict[str, Dict[str, Any]] = {}
    resource_actions: Dict[str, Set[str]] = {}  # 资源 -> 相邻主线 ACTION（评分用）
    branch_links: Dict[str, Set[str]] = {}  # 资源/method -> 支线连接（评分用）
    main_actions: Set[str] = set()
    capped_action_count = 0  # 因广度上限被丢弃的主线 ACTION 数
    # 资源的“流程血统”：产出它的 ACTION 所属 flow_id；同 flow 延续优先于跨 flow 跳转
    resource_lineage: Dict[str, Optional[str]] = {rid: None for rid in seed_resources}
    # 每个资源携带的路径（nodes/edges 交替 id 列表），条数受限
    path_carriers: Dict[str, List[Tuple[List[str], List[str]]]] = {}
    main_paths: List[Tuple[List[str], List[str]]] = []
    truncated = False

    def add_node(nid: str, **info: Any) -> None:
        if nid in nodes:
            # 已存在：主线优先、stage 取小；补充 direction 标记
            cur = nodes[nid]
            priority = {"seed": 0, "main": 1, "method": 2, "support": 3, "branch": 4}
            if priority.get(info.get("line", "branch"), 9) < priority.get(cur["line"], 9):
                cur["line"] = info.get("line", cur["line"])
            cur["stage"] = min(cur["stage"], info.get("stage", cur["stage"]))
            if info.get("direction") and info["direction"] not in cur["direction"]:
                cur["direction"] = f'{cur["direction"]}+{info["direction"]}'
            return
        nodes[nid] = {
            "line": info.get("line", "main"),
            "stage": info.get("stage", 0),
            "direction": info.get("direction", direction),
            "kind": info.get("kind", "resource"),
            "via_action": info.get("via_action"),
            "via_method": info.get("via_method"),
        }

    def add_edge(edge_id: Optional[str], src: str, dst: str, role: str, line: str) -> None:
        if not edge_id:
            return
        if edge_id in edges:
            return
        edges[edge_id] = {"from": src, "to": dst, "role": role, "line": line}

    def over_budget() -> bool:
        return len(nodes) > max_nodes

    # 种子落图
    for rid in seed_resources:
        add_node(rid, line="seed", stage=0, kind="resource")
        path_carriers[rid] = [([rid], [])]
    for aid in seed_actions:
        add_node(aid, line="seed", stage=0, kind="action")
        main_actions.add(aid)
    for mid in method_seeds:
        add_node(mid, line="seed", stage=0, kind="method")

    # ACTION 种子：预取 IO，作为双向 stage-1 的 frontier，并把对侧资源作为协同叶
    frontier_forward: Set[str] = set()
    frontier_backward: Set[str] = set()
    if seed_actions:
        io_map = await _action_io(sorted(seed_actions))
        for aid, io in io_map.items():
            for e in io["inputs"]:
                if not e["node_id"]:
                    continue
                add_node(e["node_id"], line="main", stage=1, direction="backward", kind="resource")
                add_edge(e["edge_id"], e["node_id"], aid, e["role"], "main")
                resource_actions.setdefault(e["node_id"], set()).add(aid)
                frontier_backward.add(e["node_id"])
                path_carriers.setdefault(e["node_id"], []).append(([e["node_id"], aid], [e["edge_id"]]))
            for e in io["outputs"]:
                if not e["node_id"]:
                    continue
                add_node(e["node_id"], line="main", stage=1, direction="forward", kind="resource")
                add_edge(e["edge_id"], aid, e["node_id"], e["role"], "main")
                resource_actions.setdefault(e["node_id"], set()).add(aid)
                frontier_forward.add(e["node_id"])
                path_carriers.setdefault(e["node_id"], []).append(([aid, e["node_id"]], [e["edge_id"]]))

    if direction in ("forward", "both"):
        frontier_forward |= seed_resources
    if direction in ("backward", "both"):
        frontier_backward |= seed_resources

    visited_main: Set[str] = set(seed_resources)

    def action_flow(action_id: str) -> str:
        return action_id.split(":", 1)[0] if ":" in action_id else ""

    async def bfs(direction_: str, frontier: Set[str], stage_offset: int) -> None:
        nonlocal truncated, capped_action_count
        current = sorted(frontier)
        for stage in range(stage_offset + 1, max_depth + 1 + stage_offset):
            if not current:
                break
            if over_budget():
                truncated = True
                warnings.append("Node collection truncated due to max_nodes")
                break
            rows = await _stage_expand(current, direction_)
            # 按资源分组：同 flow 延续优先，跨 flow 跳转靠后；超出单资源广度上限的丢弃
            by_resource: Dict[str, List[Dict[str, Any]]] = {}
            for row in rows:
                by_resource.setdefault(row["rid"], []).append(row)
            next_frontier: Set[str] = set()
            for rid, res_rows in by_resource.items():
                lineage = resource_lineage.get(rid)
                res_rows.sort(
                    key=lambda r: 0 if (lineage and action_flow(r["action"]) == lineage) else 1
                )
                kept = res_rows[:max_actions_per_resource]
                capped_action_count += len(res_rows) - len(kept)
                for row in kept:
                    action = row["action"]
                    main_actions.add(action)
                    add_node(action, line="main", stage=stage, direction=direction_, kind="action")
                    resource_actions.setdefault(rid, set()).add(action)
                    if direction_ == "forward":
                        add_edge(row["main_edge"], rid, action, row["main_role"], "main")
                    else:
                        add_edge(row["main_edge"], action, rid, row["main_role"], "main")

                    # 主线延续资源（下一阶段）
                    for e in row["outputs"]:
                        dst = e["node_id"]
                        if not dst:
                            continue
                        add_node(dst, line="main", stage=stage, direction=direction_, kind="resource")
                        if direction_ == "forward":
                            add_edge(e["edge_id"], action, dst, e["role"], "main")
                        else:
                            add_edge(e["edge_id"], dst, action, e["role"], "main")
                        resource_actions.setdefault(dst, set()).add(action)
                        resource_lineage.setdefault(dst, action_flow(action))
                        # 路径传递
                        carriers = path_carriers.get(rid, [])
                        for pn, pe in carriers[:MAX_PATHS_PER_NODE]:
                            if len(main_paths) >= max_paths:
                                break
                            if direction_ == "forward":
                                newp = (pn + [action, dst], pe + [row["main_edge"], e["edge_id"]])
                            else:
                                newp = ([dst, action] + pn, [e["edge_id"], row["main_edge"]] + pe)
                            main_paths.append(newp)
                            path_carriers.setdefault(dst, []).append(newp)
                        if dst not in visited_main:
                            visited_main.add(dst)
                            next_frontier.add(dst)

                    # 协同投入/产出（叶子，不再扩展，限量）
                    for e in row["co_resources"][:max_support_per_action]:
                        cid = e["node_id"]
                        if not cid:
                            continue
                        add_node(
                            cid, line="support", stage=stage, direction=direction_,
                            kind="resource", via_action=action,
                        )
                        if direction_ == "forward":
                            add_edge(e["edge_id"], cid, action, e["role"], "support")
                        else:
                            add_edge(e["edge_id"], action, cid, e["role"], "support")
                        resource_actions.setdefault(cid, set()).add(action)
            current = sorted(next_frontier)

    if capped_action_count:
        warnings.append(
            f"广度收敛：{capped_action_count} 个主线 ACTION 因单资源每阶段最多 "
            f"{max_actions_per_resource} 个的上限被省略"
        )

    if direction in ("forward", "both"):
        await bfs("forward", frontier_forward, 0)
    if direction in ("backward", "both"):
        await bfs("backward", frontier_backward, 0)

    # ---- 3. 支线：METHOD -> 兄弟 ACTION -> 关联物料 ------------------------
    action_method = await _action_methods(sorted(main_actions)) if main_actions else {}
    method_ids = sorted(set(action_method.values()))
    # METHOD 节点挂上主线（ref 边），展示“这一步用的是什么工艺”
    for aid, mid in action_method.items():
        add_node(mid, line="method", stage=nodes.get(aid, {}).get("stage", 0), kind="method")
        add_edge(f"ref:{aid}->{mid}", aid, mid, "ref", "method")
        resource_actions.setdefault(mid, set()).add(aid)

    branch_count = 0
    if branch_enabled and method_ids:
        siblings_map = await _method_sibling_actions(method_ids, branch_per_method)
        sibling_actions: Set[str] = set()
        action_via_method: Dict[str, str] = {}
        for mid, acts in siblings_map.items():
            for a in acts:
                if a in main_actions:
                    continue
                sibling_actions.add(a)
                action_via_method.setdefault(a, mid)
        io_map = await _action_io(sorted(sibling_actions))
        for aid, io in io_map.items():
            if branch_count >= branch_limit:
                truncated = True
                warnings.append("Branch expansion truncated due to branch_limit")
                break
            mid = action_via_method[aid]
            add_node(aid, line="branch", kind="action", via_method=mid)
            add_edge(f"ref:{aid}->{mid}", aid, mid, "ref", "branch")
            branch_links.setdefault(mid, set()).add(aid)
            for e in io["inputs"] + io["outputs"]:
                rid = e["node_id"]
                if not rid:
                    continue
                if branch_count >= branch_limit:
                    break
                is_new = rid not in nodes
                add_node(rid, line="branch", kind="resource", via_method=mid, via_action=aid)
                if e in io["inputs"]:
                    add_edge(e["edge_id"], rid, aid, e["role"], "branch")
                else:
                    add_edge(e["edge_id"], aid, rid, e["role"], "branch")
                branch_links.setdefault(rid, set()).add(aid)
                if is_new:
                    branch_count += 1

    if truncated:
        diagnostics.truncated = True
        diagnostics.truncation_reason = "max_nodes/branch_limit reached"

    # ---- 4. 节点元数据（PG 中文名；RESOURCE/METHOD 的 id 即 legacy id） -----
    legacy_ids = [nid for nid, n in nodes.items() if n["kind"] in ("resource", "method")]
    name_map: Dict[str, str] = {}
    entity_map: Dict[str, str] = {}
    try:
        pg_nodes = await node_storage.get_nodes_by_ids(legacy_ids)
        for nid, pn in pg_nodes.items():
            name_map[nid] = pn.canonical_name_zh or nid
            entity_map[nid] = pn.entity_type
    except Exception as exc:
        warnings.append(f"PG metadata lookup failed: {exc}")

    # Action nodes: lookup local_name from Neo4j (actions are not in PG).
    # Actions are per-flow occurrences with synthetic ids; they are not stored
    # in PostgreSQL, so we query the flow graph directly for their local_name.
    action_ids = [nid for nid, n in nodes.items() if n["kind"] == "action" and nid not in name_map]
    if action_ids:
        try:
            flow_driver = get_flow_async_driver()
            async with flow_driver.session() as flow_session:
                result = await flow_session.run(
                    """UNWIND $ids AS aid
                    MATCH (a:ArachneFlowAction {node_id: aid})
                    RETURN a.node_id AS node_id, a.local_name AS local_name, a.method_ref AS method_ref""",
                    {"ids": action_ids},
                )
                async for record in result:
                    local_name = record["local_name"]
                    if local_name:
                        name_map[record["node_id"]] = local_name
        except Exception:
            pass

    def node_label(nid: str, kind: str) -> str:
        if nid in name_map:
            return name_map[nid]
        if kind == "action":
            # 动作名 = 去掉 flow 前缀；若能定位 method 则用工艺名
            mid = action_method.get(nid)
            if mid and mid in name_map:
                return name_map[mid]
            return nid.split(":", 1)[-1]
        return nid

    # ---- 5. 关联强度评分（启发性排序） -------------------------------------
    scored: List[NodeScore] = []
    for nid, n in nodes.items():
        main_deg = len(resource_actions.get(nid, set()))
        branch_deg = len(branch_links.get(nid, set()))
        score = main_deg + 0.5 * branch_deg
        if score <= 0:
            continue
        scored.append(
            NodeScore(
                node_id=nid,
                graph="arachne_flow",
                score=score,
                rank=0,
                score_type="association_strength",
                score_components={
                    "main_actions": main_deg,
                    "branch_links": branch_deg,
                    "line": n["line"],
                },
                canonical_name_zh=name_map.get(nid),
                entity_type=entity_map.get(nid) or n["kind"],
            )
        )
    scored.sort(key=lambda s: s.score, reverse=True)
    for i, s in enumerate(scored, start=1):
        s.rank = i

    # ---- 6. 公司暴露（可选） -----------------------------------------------
    company_exposures = None
    if params.get("include_company_exposures"):
        max_exposures = int(params.get("max_company_exposures", 50))
        company_exposures = await build_company_exposures(legacy_ids, max_exposures=max_exposures)

    # ---- 7. 组装输出 --------------------------------------------------------
    node_name_map = {
        nid: {
            "canonical_name_zh": name_map.get(nid),
            "canonical_name_en": None,
            "entity_type": entity_map.get(nid) or nodes[nid]["kind"],
        }
        for nid in nodes
    }
    reasoning_paths: List[ReasoningPath] = []
    for idx, (pn, pe) in enumerate(main_paths[:max_paths]):
        reasoning_paths.append(
            ReasoningPath(
                path_id=f"path_{reasoning_id}_{idx}",
                start_node_id=pn[0],
                end_node_id=pn[-1],
                node_sequence=pn,
                edge_sequence=[e for e in pe if e],
                graph_sequence=["arachne_flow"] * len(pn),
                path_length=len([e for e in pe if e]),
                node_name_map={nid: node_name_map.get(nid, {}) for nid in pn},
                flags=["main_line"],
            )
        )

    temp_nodes: List[TempGraphNode] = []
    for nid in sorted(nodes):
        n = nodes[nid]
        kind = n["kind"]
        if kind == "action":
            display_type = "process"
        elif kind == "method":
            display_type = "technology_capability"
        else:
            display_type = entity_map.get(nid, "material")
        main_deg = len(resource_actions.get(nid, set()))
        branch_deg = len(branch_links.get(nid, set()))
        temp_nodes.append(
            TempGraphNode(
                temp_node_id=nid,
                origin_graph=OriginGraph.INDUSTRIAL,
                origin_node_id=nid,
                node_type=display_type,
                label=node_label(nid, kind),
                properties={
                    "line": n["line"],
                    "stage": n["stage"],
                    "direction": n["direction"],
                    "node_kind": kind,
                    "via_action": n["via_action"],
                    "via_method": n["via_method"],
                    "canonical_name_zh": name_map.get(nid),
                },
                score=(main_deg + 0.5 * branch_deg) or None,
                score_components={"main_actions": main_deg, "branch_links": branch_deg},
            )
        )

    temp_edges: List[TempGraphEdge] = []
    for eid, e in edges.items():
        temp_edges.append(
            TempGraphEdge(
                temp_edge_id=eid,
                origin_graph=OriginGraph.INDUSTRIAL,
                origin_edge_id=eid,
                from_temp_node_id=e["from"],
                to_temp_node_id=e["to"],
                edge_namespace="arachne_flow",
                edge_type=e["role"],
                properties={"line": e["line"]},
                weight=1.0 if e["line"] in ("main", "method") else 0.5,
            )
        )

    temp_graph = TemporaryReasoningGraph(
        temp_graph_id=f"temp_graph_{reasoning_id}",
        reasoning_id=reasoning_id,
        graph_scope=TempGraphScope.SINGLE_GRAPH,
        source_graphs=[GraphType.INDUSTRIAL],
        nodes=temp_nodes,
        edges=temp_edges,
        created_at=datetime.utcnow(),
    )

    result_payload: Dict[str, Any] = {
        "seed_nodes": list(existing),
        "seed_resources": sorted(seed_resources),
        "paths": [p.model_dump() for p in reasoning_paths],
        "node_scores": [s.model_dump() for s in scored[:50]],
        "main_line": {
            "stages": max_depth,
            "actions": len(main_actions),
            "methods": len(method_ids),
            "capped_actions": capped_action_count,
        },
        "branch": {
            "enabled": branch_enabled,
            "materials": sum(1 for n in nodes.values() if n["line"] == "branch" and n["kind"] == "resource"),
        },
        "node_counts": {
            line: sum(1 for n in nodes.values() if n["line"] == line)
            for line in ("seed", "main", "method", "support", "branch")
        },
    }
    if OutputType.TEMPORARY_GRAPH in task.requested_outputs or not task.requested_outputs:
        result_payload["temporary_graph"] = temp_graph.model_dump()
    if company_exposures:
        result_payload["company_exposures"] = company_exposures.model_dump()

    diagnostics.warnings = warnings
    diagnostics.execution_time_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
