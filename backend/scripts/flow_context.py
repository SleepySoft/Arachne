"""Flow authoring context tool: 在改流程图之前，快速拿到一个词的完整上下文。

解决的问题：图越来越大，新增节点/边时很难知道——
  1. 这个词是否已存在（flow 图 / legacy 产业图 / PG metadata），避免重复造节点；
  2. 它在哪些 YAML 文件里出现过、以什么角色出现（找“正确位置”和惯例）；
  3. 它在编译后图里的上下游是什么（判断断链/接链点）；
  4. 全图还有哪些断链缺口（--dangling），哪里最值得补。

Usage (from repo root):
    backend\\venv\\Scripts\\python.exe backend/scripts/flow_context.py foundry
    backend\\venv\\Scripts\\python.exe backend/scripts/flow_context.py 晶圆 --limit 10
    backend\\venv\\Scripts\\python.exe backend/scripts/flow_context.py --dangling
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import get_async_driver
from app.database_flow import get_flow_async_driver
from app.database_postgres import close_postgres_pool, get_postgres_pool
from app.reasoning.arachne_flow_adapter import INPUT_ROLES, OUTPUT_ROLES
from app.services import node_storage

ROOT = Path(__file__).resolve().parents[2]
FLOW_DIR = ROOT / "data" / "flows"


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


async def _pg_matches(term: str, limit: int) -> list[dict]:
    """PG industrial_nodes（legacy metadata）模糊匹配。"""
    nodes, _ = await node_storage.list_nodes(search=term, limit=limit)
    out = [
        {
            "node_id": n.node_id,
            "name": n.canonical_name_zh,
            "entity_type": n.entity_type,
            "score": 1.0,
        }
        for n in nodes
    ]
    if len(out) < limit:
        # 子串没命中时，全表按相似度兜底
        all_nodes, _ = await node_storage.list_nodes(limit=2000)
        scored = []
        for n in all_nodes:
            s = max(
                _sim(term, n.node_id),
                _sim(term, n.canonical_name_zh or ""),
                max((_sim(term, a) for a in (n.aliases or [])), default=0.0),
            )
            if s >= 0.5 and n.node_id not in {x["node_id"] for x in out}:
                scored.append(
                    {"node_id": n.node_id, "name": n.canonical_name_zh, "entity_type": n.entity_type, "score": s}
                )
        scored.sort(key=lambda x: x["score"], reverse=True)
        out.extend(scored[: limit - len(out)])
    return out[:limit]


async def _flow_graph_context(node_id: str) -> dict | None:
    """编译后 flow 图中的节点种类与上下游。"""
    driver = get_flow_async_driver()
    async with driver.session() as s:
        r = await s.run(
            """
            MATCH (n:ArachneFlowNode {node_id: $id})
            OPTIONAL MATCH (n)-[eo:ARACHNE_FLOW]->(t:ArachneFlowNode)
            OPTIONAL MATCH (f:ArachneFlowNode)-[ei:ARACHNE_FLOW]->(n)
            RETURN labels(n) AS labels,
                   collect(DISTINCT {et: eo.edge_type, other: t.node_id}) AS outs,
                   collect(DISTINCT {et: ei.edge_type, other: f.node_id}) AS ins
            """,
            {"id": node_id},
        )
        rec = await r.single()
        if not rec:
            return None
        labels = set(rec["labels"] or [])
        kind = (
            "RESOURCE" if "ArachneFlowResource" in labels
            else "ACTION" if "ArachneFlowAction" in labels
            else "METHOD" if "ArachneFlowMethod" in labels
            else "?"
        )
        return {
            "kind": kind,
            "outs": [e for e in rec["outs"] if e["et"]],
            "ins": [e for e in rec["ins"] if e["et"]],
        }


async def _flow_id_candidates(term: str, limit: int) -> list[str]:
    """flow 图内按 id 子串 + PG 中文名找候选节点。"""
    driver = get_flow_async_driver()
    async with driver.session() as s:
        r = await s.run(
            "MATCH (n:ArachneFlowNode) WHERE toLower(n.node_id) CONTAINS toLower($t) RETURN n.node_id AS id LIMIT $l",
            {"t": term, "l": limit},
        )
        ids = [rec["id"] async for rec in r]
    if len(ids) >= limit:
        return ids
    # 中文名匹配：先取全部 RESOURCE/METHOD id，再查 PG 名
    async with driver.session() as s:
        r = await s.run(
            "MATCH (n:ArachneFlowNode) WHERE n:ArachneFlowResource OR n:ArachneFlowMethod RETURN n.node_id AS id"
        )
        all_ids = [rec["id"] async for rec in r]
    pg = await node_storage.get_nodes_by_ids(all_ids)
    for nid, pn in pg.items():
        name = pn.canonical_name_zh or ""
        if term and (term in name or _sim(term, name) >= 0.6 or _sim(term, nid) >= 0.6):
            if nid not in ids:
                ids.append(nid)
        if len(ids) >= limit:
            break
    return ids[:limit]


async def _legacy_relations(node_id: str) -> list[str]:
    """legacy 产业图中的关系（判断 flow 是否漏建模）。"""
    driver = get_async_driver()
    async with driver.session() as s:
        r = await s.run(
            """
            MATCH (n:IndustrialNode {node_id: $id})
            OPTIONAL MATCH (n)-[o:INDUSTRIAL_FLOW]->(t:IndustrialNode)
            OPTIONAL MATCH (f:IndustrialNode)-[i:INDUSTRIAL_FLOW]->(n)
            OPTIONAL MATCH (n)-[ont:ONTOLOGY]->(ot:IndustrialNode)
            OPTIONAL MATCH (of:IndustrialNode)-[ont2:ONTOLOGY]->(n)
            RETURN collect(DISTINCT {d: '->', et: o.edge_type, other: t.node_id}) +
                   collect(DISTINCT {d: '<-', et: i.edge_type, other: f.node_id}) +
                   collect(DISTINCT {d: '~>', et: ont.edge_type, other: ot.node_id}) +
                   collect(DISTINCT {d: '<~', et: ont2.edge_type, other: of.node_id}) AS rels
            """,
            {"id": node_id},
        )
        rec = await r.single()
        if not rec:
            return []
        return [
            f"{e['d']} {e['et']} {e['d'] if e['d'].startswith('<') else ''} {e['other']}".replace("  ", " ")
            for e in rec["rels"]
            if e["et"]
        ]


def _yaml_mentions(term: str, limit: int = 40) -> list[str]:
    """在 data/flows/**/*.yaml 中做文本检索，返回 文件:行号: 内容。"""
    hits = []
    for path in sorted(FLOW_DIR.rglob("*.yaml")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        rel = path.relative_to(FLOW_DIR)
        for i, line in enumerate(lines, 1):
            if term.lower() in line.lower():
                hits.append(f"  {rel}:{i}: {line.strip()}")
                if len(hits) >= limit:
                    return hits
    return hits


async def show_context(term: str, limit: int) -> None:
    print(f"=== 1. PG / legacy metadata 匹配（{term}）===")
    pg = await _pg_matches(term, limit)
    if not pg:
        print("  (无) —— 这个词在产业图 metadata 里也不存在，是全新概念")
    for m in pg:
        print(f"  {m['node_id']}  {m['name']}  [{m['entity_type']}]  sim={m['score']:.2f}")

    print(f"\n=== 2. flow 图候选节点 ===")
    flow_ids = await _flow_id_candidates(term, limit)
    if not flow_ids:
        print("  (无) —— flow 图中尚无此节点")
    for nid in flow_ids:
        ctx = await _flow_graph_context(nid)
        if not ctx:
            continue
        print(f"  {nid} [{ctx['kind']}]")
        for e in ctx["ins"][:5]:
            print(f"      <- {e['et']} <- {e['other']}")
        for e in ctx["outs"][:5]:
            print(f"      -> {e['et']} -> {e['other']}")

    print(f"\n=== 3. legacy 产业图关系（flow 是否漏建模的对照）===")
    seen = set()
    for m in pg[:3]:
        nid = m["node_id"]
        if nid in seen:
            continue
        seen.add(nid)
        rels = await _legacy_relations(nid)
        if rels:
            print(f"  {nid}:")
            for r in rels[:10]:
                print(f"      {r}")

    print(f"\n=== 4. YAML 文件提及（找“正确位置”和角色惯例）===")
    hits = _yaml_mentions(term)
    if not hits:
        print("  (无)")
    for h in hits:
        print(h)


async def show_dangling() -> None:
    driver = get_flow_async_driver()
    async with driver.session() as s:
        r = await s.run(
            """
            MATCH (n:ArachneFlowResource)
            OPTIONAL MATCH (n)-[eo:ARACHNE_FLOW]->(a)
            OPTIONAL MATCH (f)-[ei:ARACHNE_FLOW]->(n)
            RETURN n.node_id AS id,
                   collect(DISTINCT ei.edge_type) AS ins,
                   collect(DISTINCT eo.edge_type) AS outs
            """
        )
        rows = []
        async for rec in r:
            has_up = any(et in OUTPUT_ROLES for et in rec["ins"])
            has_down = any(et in INPUT_ROLES for et in rec["outs"])
            rows.append((rec["id"], has_up, has_down))
    pg = await node_storage.get_nodes_by_ids([r[0] for r in rows])
    name = lambda nid: (pg.get(nid).canonical_name_zh if pg.get(nid) else None) or ""
    no_up = [(nid, name(nid)) for nid, up, down in rows if not up]
    no_down = [(nid, name(nid)) for nid, up, down in rows if not down]
    print(f"=== 无上游资源（{len(no_up)}；原料/设备/商业主体属正常，中间品属断链）===")
    for nid, nm in sorted(no_up):
        print(f"  {nid}  {nm}")
    print(f"\n=== 无下游资源（{len(no_down)}；终端产品属正常，中间品属断链）===")
    for nid, nm in sorted(no_down):
        print(f"  {nid}  {nm}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("term", nargs="?", help="要查的词（node_id / 中文名 / 片段）")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--dangling", action="store_true", help="输出全图断链报告")
    args = parser.parse_args()

    if args.dangling:
        asyncio.run(show_dangling())
        return
    if not args.term:
        parser.error("需要提供 term，或使用 --dangling")

    asyncio.run(show_context(args.term, args.limit))
    asyncio.run(close_postgres_pool())


if __name__ == "__main__":
    main()
