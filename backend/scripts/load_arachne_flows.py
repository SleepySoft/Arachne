r"""Load arachne-flow YAML files into Neo4j and track their compile status in PostgreSQL.

This script first builds a unified in-memory graph from all flow files (deduplicating
shared resources/methods, namespacing actions by flow, and detecting conflicts), then
writes the whole graph to Neo4j in one pass and prints statistics.

Usage (from repo root):
    backend\venv\Scripts\python.exe backend/scripts/load_arachne_flows.py
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database_flow import close_flow_async_driver, init_flow_db
from app.database_postgres import close_postgres_pool, get_postgres_pool, init_postgres_tables
from app.engines.arachne_flow.builder import FlowGraphBuilder
from app.engines.arachne_flow.parser import FlowParseError, parse_flow_file
from app.engines.arachne_flow import storage


ROOT = Path(__file__).resolve().parents[2]
FLOW_DIR = ROOT / "data" / "flows"


async def _upsert_status(
    pool,
    flow_id: str,
    file_path: str,
    md5: str,
    status: str,
    error_message: str | None = None,
):
    await pool.execute(
        """
        INSERT INTO arachne_flow_files (flow_id, file_path, md5, status, error_message, compiled_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        ON CONFLICT (flow_id) DO UPDATE
        SET file_path = EXCLUDED.file_path,
            md5 = EXCLUDED.md5,
            status = EXCLUDED.status,
            error_message = EXCLUDED.error_message,
            compiled_at = EXCLUDED.compiled_at,
            updated_at = NOW()
        """,
        flow_id,
        file_path,
        md5,
        status,
        error_message,
    )


def _print_stats(stats) -> None:
    print("\n=== Arachne-flow build statistics ===")
    print(f"flows:            {stats.flow_count}")
    print(f"resources (dedup): {stats.resource_count}")
    print(f"methods (dedup):   {stats.method_count}")
    print(f"actions:          {stats.action_count}")
    print(f"triples:          {stats.triple_count}")
    print(f"edge types:       {json.dumps(stats.edge_type_counts, ensure_ascii=False)}")

    print(f"\nshared resources (>1 flow): {len(stats.shared_resources)}")
    for s in stats.shared_resources[:10]:
        print(f"  - {s.node_id}: {s.flow_count} flows ({', '.join(s.flow_ids)})")
    if len(stats.shared_resources) > 10:
        print(f"  ... and {len(stats.shared_resources) - 10} more")

    print(f"\nshared methods (>1 flow): {len(stats.shared_methods)}")
    for s in stats.shared_methods[:10]:
        print(f"  - {s.node_id}: {s.flow_count} flows ({', '.join(s.flow_ids)})")
    if len(stats.shared_methods) > 10:
        print(f"  ... and {len(stats.shared_methods) - 10} more")

    print(f"\nmethods referenced by multiple actions: {len(stats.methods_referenced_by_multiple_actions)}")
    for m in stats.methods_referenced_by_multiple_actions[:10]:
        print(f"  - {m.method_id}: {m.action_count} actions across {len(m.flow_ids)} flows")
    if len(stats.methods_referenced_by_multiple_actions) > 10:
        print(f"  ... and {len(stats.methods_referenced_by_multiple_actions) - 10} more")

    pg = stats.missing_in_pg
    print(f"\nmissing in PostgreSQL industrial_nodes:")
    print(f"  resources: {len(pg.resources)}")
    if pg.resources:
        for rid in pg.resources[:10]:
            print(f"    - {rid}")
        if len(pg.resources) > 10:
            print(f"    ... and {len(pg.resources) - 10} more")
    print(f"  methods: {len(pg.methods)}")
    if pg.methods:
        for mid in pg.methods[:10]:
            print(f"    - {mid}")
        if len(pg.methods) > 10:
            print(f"    ... and {len(pg.methods) - 10} more")
    print(f"  actions with missing method_ref in PG: {len(pg.actions_with_missing_method_ref)}")

    print(f"\ncommon action paths (by method_ref) across flows: {len(stats.common_paths)}")
    for p in stats.common_paths:
        print(f"  - {' -> '.join(p.path)}  in {p.flow_count} flows ({', '.join(p.flow_ids)})")
    print("=====================================\n")


async def load_all():
    await init_flow_db()
    await init_postgres_tables()
    pool = await get_postgres_pool()

    if not FLOW_DIR.exists():
        print(f"[error] flow directory not found: {FLOW_DIR}")
        return

    files = sorted(
        p
        for p in FLOW_DIR.rglob("*.yaml")
        if p.name != "manifest.yaml" and "legacy" not in p.parts
    )
    print(f"[info] found {len(files)} flow files in {FLOW_DIR}\n")

    builder = FlowGraphBuilder()
    parsed_ok: list[tuple[str, str, str]] = []  # flow_id, relative_path, md5

    for path in files:
        content = path.read_bytes()
        md5 = hashlib.md5(content).hexdigest()
        try:
            parsed = parse_flow_file(path)
            builder.add_parsed_flow(parsed)
            parsed_ok.append((parsed.flow_id, str(path.relative_to(ROOT)), md5))
        except FlowParseError as exc:
            await _upsert_status(pool, path.stem, str(path.relative_to(ROOT)), md5, "PARSE_ERROR", str(exc))
            print(f"[parse error] {path.name}: {exc}")
        except Exception as exc:
            await _upsert_status(pool, path.stem, str(path.relative_to(ROOT)), md5, "COMPILE_ERROR", str(exc))
            print(f"[compile error] {path.name}: {exc}")

    if not builder.graph.flow_ids:
        print("[warn] no flow files were successfully parsed; nothing to compile")
        await close_flow_async_driver()
        await close_postgres_pool()
        return

    builder.validate_global()
    if builder.graph.errors:
        for err in builder.graph.errors:
            print(f"[global error] {err}")
        for flow_id, _, _ in parsed_ok:
            await _upsert_status(pool, flow_id, "", "", "VALIDATION_ERROR", "; ".join(builder.graph.errors))
        await close_flow_async_driver()
        await close_postgres_pool()
        return

    if builder.graph.warnings:
        for warn in builder.graph.warnings:
            print(f"[warning] {warn}")

    stats = await builder.compute_statistics()
    _print_stats(stats)

    counts = await storage.compile_flow_graph(builder.graph, clear_existing=True)
    print(
        f"[ok] compiled {counts['resources']} resources, {counts['methods']} methods, "
        f"{counts['actions']} actions ({counts['dual']} dual), {counts['edges']} edges"
    )

    # Verify persistence: count nodes/edges actually present in Neo4j.
    driver = storage.get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run("MATCH (n:ArachneFlowNode) RETURN count(n) AS c")
        db_nodes = (await result.single())["c"]
        result = await session.run("MATCH ()-[r:ARACHNE_FLOW]->() RETURN count(r) AS c")
        db_edges = (await result.single())["c"]
    expected_nodes = counts["resources"] + counts["methods"] + counts["actions"] - counts["dual"]
    if db_nodes != expected_nodes or db_edges != counts["edges"]:
        print(
            f"[warn] persistence mismatch: expected {expected_nodes} nodes / {counts['edges']} edges, "
            f"but Neo4j has {db_nodes} nodes / {db_edges} edges"
        )
    else:
        print(f"[verify] Neo4j persisted {db_nodes} nodes / {db_edges} edges")

    for flow_id, file_path, md5 in parsed_ok:
        await _upsert_status(pool, flow_id, file_path, md5, "COMPILED")
        print(f"[status] {flow_id}: COMPILED")

    await close_flow_async_driver()
    await close_postgres_pool()


if __name__ == "__main__":
    asyncio.run(load_all())
