#!/usr/bin/env python3
"""提取产业图两项遗漏（只读检查，不写库）。

检查 1：arachne-flow YAML（data/flows/**/*.yaml）中引用的 RESOURCE / METHOD，
        在 PG industrial_nodes 中是否有对应节点（ACTION 实例 act_* 自动排除）。
检查 2：PG industrial_nodes 中哪些节点数据不完整
        （缺中文名/英文名/定义/类型/证据，PENDING 状态），
        以及 Neo4j 与 PG 的双向一致性（哪边有而另一边没有）。

用途：新增/修改 flow 文件、或批量补数据后，定期跑一遍找遗漏。

用法（在仓库根目录）：
    backend\\venv\\Scripts\\python.exe scripts/extract_flow_pg_gaps.py

输出：
    - 控制台摘要
    - temp/flow_pg_gap_report.json（完整遗漏清单，供补全脚本消费）

依赖：PG(:5433) 与 Neo4j(:7687) 在线；不需要后端 API。
补全惯例（见 AGENTS.md）：真实体走 GraphRegistrationBatch 进 Neo4j+PG；
集成类合成 METHOD（integration_of_*）按先例只补 PG 行。
"""
import asyncio
import json
from pathlib import Path

import asyncpg
import yaml
from neo4j import AsyncGraphDatabase

ROOT = Path(__file__).resolve().parent.parent
FLOW_DIR = ROOT / "data" / "flows"
REPORT = ROOT / "temp" / "flow_pg_gap_report.json"

PG_URL = "postgresql://postgres:postgres@localhost:5433/arachne"
NEO4J_URL = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")

REF = "ref"
NEXT = "next"


def classify_flow_nodes():
    """按 parser 规则推断角色：ref 目标=METHOD，ref/next 源=ACTION，其余=RESOURCE。"""
    resources, methods = set(), set()
    local_names = {}  # id -> (flow_file, local_name)
    for f in sorted(FLOW_DIR.rglob("*.yaml")):
        if f.name == "manifest.yaml":
            continue
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for k, v in (doc.get("local") or {}).items():
            local_names.setdefault(k, (str(f.relative_to(FLOW_DIR)), v))
        for triple in doc.get("edges") or []:
            if not isinstance(triple, list) or len(triple) != 3:
                continue
            src, pred, dst = triple
            if pred == REF:
                methods.add(dst)
            elif pred == NEXT:
                pass  # 两端都是 ACTION
            else:
                resources.add(src)
                resources.add(dst)
    # METHOD 以 ref 判定为准剔除；ACTION 实例（act_* 前缀）不属于 PG，剔除
    resources -= methods
    actions = {r for r in resources if r.startswith("act_")}
    resources -= actions
    return resources, methods, actions, local_names


async def main():
    resources, methods, actions, local_names = classify_flow_nodes()
    all_refs = resources | methods

    conn = await asyncpg.connect(PG_URL)
    pg_rows = await conn.fetch(
        "SELECT node_id, canonical_name_zh, canonical_name_en, aliases, definition, "
        "entity_type, evidence, confidence, status FROM industrial_nodes"
    )
    pg = {r["node_id"]: dict(r) for r in pg_rows}

    # ---- 检查 1：flow 引用 vs PG ----
    missing_resources = sorted(r for r in resources if r not in pg)
    missing_methods = sorted(m for m in methods if m not in pg)
    no_zh_resources = sorted(r for r in resources if r in pg and not (pg[r]["canonical_name_zh"] or "").strip())
    no_zh_methods = sorted(m for m in methods if m in pg and not (pg[m]["canonical_name_zh"] or "").strip())

    # ---- 检查 2：PG 节点完整性 ----
    incomplete = {}
    for nid, r in pg.items():
        missing_fields = []
        if not (r["canonical_name_zh"] or "").strip():
            missing_fields.append("canonical_name_zh")
        if not (r["canonical_name_en"] or "").strip():
            missing_fields.append("canonical_name_en")
        if not (r["definition"] or "").strip() or len((r["definition"] or "").strip()) < 15:
            missing_fields.append("definition")
        if not (r["entity_type"] or "").strip() or r["entity_type"] == "unknown":
            missing_fields.append("entity_type")
        ev = r["evidence"]
        if not ev or ev == "[]" or ev == []:
            missing_fields.append("evidence")
        if r["status"] == "PENDING":
            missing_fields.append("status(PENDING)")
        if missing_fields:
            incomplete[nid] = {
                "missing": missing_fields,
                "canonical_name_zh": r["canonical_name_zh"],
                "entity_type": r["entity_type"],
                "status": r["status"],
                "confidence": r["confidence"],
                "referenced_by_flow": nid in all_refs,
            }

    # ---- Neo4j ↔ PG 一致性 ----
    driver = AsyncGraphDatabase.driver(NEO4J_URL, auth=NEO4J_AUTH)
    async with driver.session() as s:
        res = await s.run("MATCH (n:IndustrialNode) RETURN n.node_id AS nid")
        neo4j_ids = {rec["nid"] async for rec in res}
    await driver.close()
    neo4j_without_pg = sorted(neo4j_ids - set(pg.keys()))
    pg_without_neo4j = sorted(set(pg.keys()) - neo4j_ids)

    await conn.close()

    report = {
        "check1_flow_refs_vs_pg": {
            "flow_resource_count": len(resources),
            "flow_method_count": len(methods),
            "missing_resources": [
                {"node_id": r, "local_name": local_names.get(r, (None, None))[1],
                 "local_file": local_names.get(r, (None, None))[0]}
                for r in missing_resources
            ],
            "missing_methods": [
                {"node_id": m, "local_name": local_names.get(m, (None, None))[1],
                 "local_file": local_names.get(m, (None, None))[0]}
                for m in missing_methods
            ],
            "existing_but_no_zh_name": {"resources": no_zh_resources, "methods": no_zh_methods},
        },
        "check2_pg_incomplete": {
            "total_pg_nodes": len(pg),
            "incomplete_count": len(incomplete),
            "incomplete": incomplete,
        },
        "check2b_neo4j_pg_mismatch": {
            "neo4j_node_count": len(neo4j_ids),
            "neo4j_without_pg_metadata": neo4j_without_pg,
            "pg_without_neo4j_node": pg_without_neo4j,
        },
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 检查 1：flow 引用 vs PG ===")
    print(f"flow RESOURCE {len(resources)} 个 / METHOD {len(methods)} 个（ACTION 实例 {len(actions)} 个已排除）")
    print(f"PG 缺失 RESOURCE: {len(missing_resources)}")
    for item in report["check1_flow_refs_vs_pg"]["missing_resources"]:
        print(f"  {item['node_id']:42s} local={item['local_name']} file={item['local_file']}")
    print(f"PG 缺失 METHOD: {len(missing_methods)}")
    for item in report["check1_flow_refs_vs_pg"]["missing_methods"]:
        print(f"  {item['node_id']:42s} local={item['local_name']} file={item['local_file']}")
    print(f"已存在但缺中文名: resource {len(no_zh_resources)} / method {len(no_zh_methods)}")
    print()
    print("=== 检查 2：PG 节点完整性 ===")
    print(f"PG 节点总数 {len(pg)}，不完整 {len(incomplete)}")
    from collections import Counter
    field_counter = Counter(f for v in incomplete.values() for f in v["missing"])
    print("缺失字段分布:", dict(field_counter))
    flow_related = [k for k, v in incomplete.items() if v["referenced_by_flow"]]
    print(f"其中被 flow 引用的不完整节点: {len(flow_related)}")
    print()
    print("=== 检查 2b：Neo4j ↔ PG 一致性 ===")
    print(f"Neo4j 节点 {len(neo4j_ids)}；Neo4j 有而 PG 无: {len(neo4j_without_pg)}；PG 有而 Neo4j 无: {len(pg_without_neo4j)}")
    for nid in neo4j_without_pg[:30]:
        print(f"  neo4j_only: {nid}")
    for nid in pg_without_neo4j[:30]:
        print(f"  pg_only: {nid}")
    print(f"\n报告已写入 {REPORT}")


asyncio.run(main())
