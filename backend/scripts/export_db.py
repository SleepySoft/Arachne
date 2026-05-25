#!/usr/bin/env python3
"""
Arachne Database Export Script
==============================
Export all Neo4j and PostgreSQL data to JSON files.

Usage:
    cd backend && python scripts/export_db.py
    cd backend && python scripts/export_db.py --output-dir ../data/backup/myexport
    cd backend && python scripts/export_db.py --no-company-view

Output structure:
    <output_dir>/
        neo4j/
            industrial_nodes.json
            industrial_flow_edges.json
            ontology_edges.json
            company_nodes.json          (skipped if --no-company-view)
            company_relations.json      (skipped if --no-company-view)
        postgres/
            industries.json
            industry_node_mappings.json
            companies.json
            company_node_exposures.json
            computation_jobs.json
            company_view_versions.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, date
from uuid import UUID
from pathlib import Path

# Add parent dir to path so we can import app.*
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.database import get_async_driver, close_async_driver
from app.database_postgres import get_postgres_pool, close_postgres_pool


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def serialize_value(val):
    """Convert asyncpg/Neo4j values to JSON-serializable types."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.isoformat()
    if isinstance(val, date):
        return val.isoformat()
    if isinstance(val, UUID):
        return str(val)
    if isinstance(val, (list, dict, str, int, float, bool)):
        return val
    # Fallback: try to convert to string
    return str(val)


def record_to_dict(record) -> dict:
    """Convert an asyncpg Record or Neo4j Record to a plain dict."""
    result = {}
    for key in record.keys():
        result[key] = serialize_value(record[key])
    return result


# ---------------------------------------------------------------------------
# Neo4j export
# ---------------------------------------------------------------------------

NEO4J_EXPORT_SPECS = [
    {
        "file": "industrial_nodes.json",
        "query": """
            MATCH (n:IndustrialNode)
            RETURN n {
                .*,
                __labels: labels(n)
            } AS node
        """,
        "extract": lambda r: r["node"],
    },
    {
        "file": "industrial_flow_edges.json",
        "query": """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            RETURN r { .*, __type: type(r), __from: a.node_id, __to: b.node_id } AS edge
        """,
        "extract": lambda r: r["edge"],
    },
    {
        "file": "ontology_edges.json",
        "query": """
            MATCH (a:IndustrialNode)-[r:ONTOLOGY]->(b:IndustrialNode)
            RETURN r { .*, __type: type(r), __from: a.node_id, __to: b.node_id } AS edge
        """,
        "extract": lambda r: r["edge"],
    },
]

NEO4J_COMPANY_VIEW_SPECS = [
    {
        "file": "company_nodes.json",
        "query": """
            MATCH (n:Company)
            RETURN n { .*, __labels: labels(n) } AS node
        """,
        "extract": lambda r: r["node"],
    },
    {
        "file": "company_relations.json",
        "query": """
            MATCH (a:Company)-[r:INFERRED_UPSTREAM]->(b:Company)
            RETURN r { .*, __type: type(r), __from: a.company_id, __to: b.company_id } AS edge
        """,
        "extract": lambda r: r["edge"],
    },
]


async def export_neo4j(output_dir: Path, include_company_view: bool) -> None:
    driver = get_async_driver()
    neo4j_dir = output_dir / "neo4j"
    neo4j_dir.mkdir(parents=True, exist_ok=True)

    specs = NEO4J_EXPORT_SPECS.copy()
    if include_company_view:
        specs.extend(NEO4J_COMPANY_VIEW_SPECS)

    for spec in specs:
        filepath = neo4j_dir / spec["file"]
        print(f"  Exporting Neo4j {spec['file']} ...", end=" ")

        data = []
        async with driver.session() as session:
            result = await session.run(spec["query"])
            async for record in result:
                item = spec["extract"](record)
                # Serialize all values
                serialized = {k: serialize_value(v) for k, v in item.items()}
                data.append(serialized)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"{len(data)} records")

    await close_async_driver()


# ---------------------------------------------------------------------------
# PostgreSQL export
# ---------------------------------------------------------------------------

POSTGRES_CORE_TABLES = [
    "industries",
    "industry_node_mappings",
    "companies",
    "company_node_exposures",
    "computation_jobs",
]

POSTGRES_COMPANY_VIEW_TABLES = [
    "company_view_versions",
]


async def export_postgres(output_dir: Path, include_company_view: bool) -> None:
    pool = await get_postgres_pool()
    if pool is None:
        print("  WARNING: PostgreSQL not available, skipping PostgreSQL export")
        return

    pg_dir = output_dir / "postgres"
    pg_dir.mkdir(parents=True, exist_ok=True)

    tables = POSTGRES_CORE_TABLES.copy()
    if include_company_view:
        tables.extend(POSTGRES_COMPANY_VIEW_TABLES)

    async with pool.acquire() as conn:
        for table in tables:
            filepath = pg_dir / f"{table}.json"
            print(f"  Exporting PostgreSQL {table} ...", end=" ")

            rows = await conn.fetch(f"SELECT * FROM {table}")
            data = [record_to_dict(row) for row in rows]

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"{len(data)} records")

    await close_postgres_pool()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Export Arachne database to JSON files")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: data/backup/YYYYMMDD_HHMMSS)",
    )
    parser.add_argument(
        "--no-company-view",
        action="store_true",
        help="Skip company view data (Company nodes, INFERRED_UPSTREAM edges, company_view_versions table)",
    )
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "backup" / timestamp

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Exporting to: {output_dir}")
    print()

    include_company_view = not args.no_company_view

    print("Exporting Neo4j ...")
    asyncio.run(export_neo4j(output_dir, include_company_view))
    print()

    print("Exporting PostgreSQL ...")
    asyncio.run(export_postgres(output_dir, include_company_view))
    print()

    print(f"Export complete: {output_dir}")

    # Print summary
    print("\nExported files:")
    for f in sorted(output_dir.rglob("*.json")):
        rel = f.relative_to(output_dir)
        size = f.stat().st_size
        print(f"  {rel} ({size:,} bytes)")


if __name__ == "__main__":
    main()
