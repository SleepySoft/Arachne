#!/usr/bin/env python3
"""
Arachne Database Import Script
==============================
Import Neo4j and PostgreSQL data from JSON files produced by export_db.py.

Usage:
    cd backend && python scripts/import_db.py --input-dir ../data/backup/20240115_120000
    cd backend && python scripts/import_db.py --input-dir ../data/backup/20240115_120000 --clear
    cd backend && python scripts/import_db.py --input-dir ../data/backup/20240115_120000 --no-company-view

Options:
    --clear             Drop existing data before import (DESTRUCTIVE)
    --no-company-view   Skip company view data
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent dir to path so we can import app.*
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.database import get_async_driver, close_async_driver
from app.database_postgres import get_postgres_pool, close_postgres_pool


# ---------------------------------------------------------------------------
# Neo4j import
# ---------------------------------------------------------------------------

async def import_neo4j_nodes(driver, filepath: Path, label: str, id_key: str) -> int:
    """Import nodes from a JSON file. Returns count of imported nodes."""
    if not filepath.exists():
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return 0

    BATCH_SIZE = 500
    total = 0

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i : i + BATCH_SIZE]
        # Remove internal metadata fields
        clean_batch = []
        for item in batch:
            clean = {k: v for k, v in item.items() if not k.startswith("__")}
            clean_batch.append(clean)

        async with driver.session() as session:
            result = await session.run(
                f"""
                UNWIND $batch AS item
                MERGE (n:{label} {{{id_key}: item.{id_key}}})
                SET n = item
                RETURN count(n) AS cnt
                """,
                batch=clean_batch,
            )
            record = await result.single()
            total += record["cnt"] if record else 0

    return total


async def import_neo4j_edges(
    driver,
    filepath: Path,
    rel_type: str,
    from_label: str,
    to_label: str,
    from_key: str,
    to_key: str,
) -> int:
    """Import edges from a JSON file. Returns count of imported edges."""
    if not filepath.exists():
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return 0

    BATCH_SIZE = 500
    total = 0

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i : i + BATCH_SIZE]
        # Build clean batch with from/to IDs and properties
        clean_batch = []
        for item in batch:
            clean = {
                "__from": item.get("__from"),
                "__to": item.get("__to"),
            }
            # Copy all properties except metadata
            for k, v in item.items():
                if not k.startswith("__"):
                    clean[k] = v
            clean_batch.append(clean)

        async with driver.session() as session:
            result = await session.run(
                f"""
                UNWIND $batch AS item
                MATCH (a:{from_label} {{{from_key}: item.__from}}), (b:{to_label} {{{to_key}: item.__to}})
                CREATE (a)-[r:{rel_type}]->(b)
                SET r = apoc.map.removeKeys(item, ['__from', '__to'])
                RETURN count(r) AS cnt
                """,
                batch=clean_batch,
            )
            record = await result.single()
            total += record["cnt"] if record else 0

    return total


async def import_neo4j_edges_no_apoc(
    driver,
    filepath: Path,
    rel_type: str,
    from_label: str,
    to_label: str,
    from_key: str,
    to_key: str,
) -> int:
    """Import edges without APOC (fallback). Build SET clause manually."""
    if not filepath.exists():
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return 0

    # Determine property keys from first item (excluding metadata)
    sample = data[0]
    prop_keys = [k for k in sample.keys() if not k.startswith("__")]
    set_clauses = ", ".join([f"r.{k} = item.{k}" for k in prop_keys])

    BATCH_SIZE = 500
    total = 0

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i : i + BATCH_SIZE]
        clean_batch = []
        for item in batch:
            clean = {"__from": item.get("__from"), "__to": item.get("__to")}
            for k in prop_keys:
                clean[k] = item.get(k)
            clean_batch.append(clean)

        async with driver.session() as session:
            result = await session.run(
                f"""
                UNWIND $batch AS item
                MATCH (a:{from_label} {{{from_key}: item.__from}}), (b:{to_label} {{{to_key}: item.__to}})
                CREATE (a)-[r:{rel_type}]->(b)
                SET {set_clauses}
                RETURN count(r) AS cnt
                """,
                batch=clean_batch,
            )
            record = await result.single()
            total += record["cnt"] if record else 0

    return total


async def clear_neo4j(driver, include_company_view: bool) -> None:
    """Clear all data from Neo4j."""
    print("  Clearing Neo4j ...")

    async with driver.session() as session:
        # Delete all edges first
        await session.run("MATCH ()-[r:INDUSTRIAL_FLOW]->() DELETE r")
        await session.run("MATCH ()-[r:ONTOLOGY]->() DELETE r")
        if include_company_view:
            await session.run("MATCH ()-[r:INFERRED_UPSTREAM]->() DELETE r")

        # Delete all nodes
        if include_company_view:
            await session.run("MATCH (n:Company) DELETE n")
        await session.run("MATCH (n:IndustrialNode) DELETE n")


async def import_neo4j(input_dir: Path, include_company_view: bool, clear: bool) -> None:
    driver = get_async_driver()
    neo4j_dir = input_dir / "neo4j"

    if clear:
        await clear_neo4j(driver, include_company_view)

    print("  Importing Neo4j industrial_nodes ...", end=" ")
    count = await import_neo4j_nodes(driver, neo4j_dir / "industrial_nodes.json", "IndustrialNode", "node_id")
    print(f"{count} nodes")

    # Try APOC first, fallback to manual SET
    has_apoc = False
    async with driver.session() as session:
        try:
            result = await session.run("RETURN apoc.version() AS v")
            record = await result.single()
            has_apoc = record is not None and record.get("v") is not None
        except Exception:
            has_apoc = False

    import_edges = import_neo4j_edges if has_apoc else import_neo4j_edges_no_apoc
    if not has_apoc:
        print("  (APOC not available, using fallback edge import)")

    print("  Importing Neo4j industrial_flow_edges ...", end=" ")
    count = await import_edges(
        driver, neo4j_dir / "industrial_flow_edges.json",
        "INDUSTRIAL_FLOW", "IndustrialNode", "IndustrialNode", "node_id", "node_id"
    )
    print(f"{count} edges")

    print("  Importing Neo4j ontology_edges ...", end=" ")
    count = await import_edges(
        driver, neo4j_dir / "ontology_edges.json",
        "ONTOLOGY", "IndustrialNode", "IndustrialNode", "node_id", "node_id"
    )
    print(f"{count} edges")

    if include_company_view:
        print("  Importing Neo4j company_nodes ...", end=" ")
        count = await import_neo4j_nodes(driver, neo4j_dir / "company_nodes.json", "Company", "company_id")
        print(f"{count} nodes")

        print("  Importing Neo4j company_relations ...", end=" ")
        count = await import_edges(
            driver, neo4j_dir / "company_relations.json",
            "INFERRED_UPSTREAM", "Company", "Company", "company_id", "company_id"
        )
        print(f"{count} edges")

    await close_async_driver()


# ---------------------------------------------------------------------------
# PostgreSQL import
# ---------------------------------------------------------------------------

# Tables in dependency order (foreign keys first)
POSTGRES_IMPORT_ORDER = [
    "industries",
    "companies",
    "industry_node_mappings",
    "company_node_exposures",
    "computation_jobs",
    "company_view_versions",
]

POSTGRES_TRUNCATE_ORDER = [
    "company_view_versions",
    "computation_jobs",
    "company_node_exposures",
    "industry_node_mappings",
    "companies",
    "industries",
]


async def clear_postgres(pool) -> None:
    """Truncate all PostgreSQL tables."""
    print("  Clearing PostgreSQL ...")
    async with pool.acquire() as conn:
        for table in POSTGRES_TRUNCATE_ORDER:
            await conn.execute(f"TRUNCATE TABLE {table} CASCADE")


async def import_postgres_table(conn, table: str, filepath: Path) -> int:
    """Import a single PostgreSQL table from JSON."""
    if not filepath.exists():
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return 0

    # Get column names from first row
    columns = list(data[0].keys())
    col_str = ",".join(columns)
    placeholders = ",".join(f"${i+1}" for i in range(len(columns)))

    # Build ON CONFLICT clause using primary key columns
    # We'll use DO NOTHING to skip duplicates
    query = f"""
        INSERT INTO {table} ({col_str})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    # Parse datetime strings back to objects
    values = []
    for row in data:
        row_values = []
        for col in columns:
            val = row.get(col)
            # Try to parse ISO datetime strings
            if isinstance(val, str) and len(val) >= 19 and "T" in val:
                try:
                    val = datetime.fromisoformat(val)
                except ValueError:
                    pass
            row_values.append(val)
        values.append(row_values)

    await conn.executemany(query, values)
    return len(data)


async def import_postgres(input_dir: Path, clear: bool, include_company_view: bool) -> None:
    pool = await get_postgres_pool()
    if pool is None:
        print("  WARNING: PostgreSQL not available, skipping PostgreSQL import")
        return

    pg_dir = input_dir / "postgres"

    if clear:
        await clear_postgres(pool)

    async with pool.acquire() as conn:
        for table in POSTGRES_IMPORT_ORDER:
            if not include_company_view and table == "company_view_versions":
                continue

            filepath = pg_dir / f"{table}.json"
            print(f"  Importing PostgreSQL {table} ...", end=" ")
            count = await import_postgres_table(conn, table, filepath)
            print(f"{count} rows")

    await close_postgres_pool()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Import Arachne database from JSON files")
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory (produced by export_db.py)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Drop existing data before import (DESTRUCTIVE!)",
    )
    parser.add_argument(
        "--no-company-view",
        action="store_true",
        help="Skip company view data",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"ERROR: Input directory does not exist: {input_dir}")
        sys.exit(1)

    include_company_view = not args.no_company_view

    if args.clear:
        print("WARNING: --clear is set. All existing data will be DESTROYED.")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.strip().lower() != "yes":
            print("Aborted.")
            sys.exit(0)

    print(f"Importing from: {input_dir}")
    print()

    print("Importing Neo4j ...")
    asyncio.run(import_neo4j(input_dir, include_company_view, args.clear))
    print()

    print("Importing PostgreSQL ...")
    asyncio.run(import_postgres(input_dir, args.clear, include_company_view))
    print()

    print("Import complete.")


if __name__ == "__main__":
    main()
