"""
One-time migration: copy IndustrialNode metadata from Neo4j to PostgreSQL.

After this migration:
  - Neo4j keeps only the skeleton node (node_id + :IndustrialNode label)
    for relationship storage.
  - PostgreSQL industrial_nodes table becomes the source of truth for
    node metadata.

Usage:
    python scripts/migrate_nodes_to_postgres.py [--dry-run]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from uuid import UUID

sys.path.insert(0, ".")

from app.database import get_async_driver, close_async_driver
from app.database_postgres import (
    close_postgres_pool,
    get_postgres_pool,
    init_postgres_tables,
)


async def _fetch_all_nodes(driver):
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)
            RETURN n {
                .node_id,
                .node_uuid,
                .canonical_name_zh,
                .canonical_name_en,
                .aliases,
                .definition,
                .entity_type,
                .evidence,
                .confidence,
                .status,
                .notes,
                .is_test,
                .created_at,
                .updated_at
            } AS props
            ORDER BY n.node_id
            """
        )
        return [rec["props"] async for rec in result]


def _to_uuid(value):
    if value is None:
        return None
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        return UUID(value)
    return None


def _to_dt(value):
    if value is None:
        return None
    if hasattr(value, "to_native"):
        return value.to_native()
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def _evidence_to_jsonb(value):
    if value is None:
        return "[]"
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return value
        except Exception:
            pass
        return value
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return "[]"


async def migrate(dry_run: bool = False):
    print("Initializing PostgreSQL tables...")
    await init_postgres_tables()

    pool = await get_postgres_pool()
    if pool is None:
        print("ERROR: PostgreSQL not available", file=sys.stderr)
        return 1

    driver = get_async_driver()
    print("Fetching nodes from Neo4j...")
    nodes = await _fetch_all_nodes(driver)
    print(f"Found {len(nodes)} nodes in Neo4j")

    if dry_run:
        print("DRY RUN: would migrate the following nodes:")
        for n in nodes[:10]:
            print(f"  - {n['node_id']}: {n.get('canonical_name_zh')}")
        if len(nodes) > 10:
            print(f"  ... and {len(nodes) - 10} more")
        return 0

    inserted = 0
    skipped = 0
    errors = 0

    async with pool.acquire() as conn:
        for n in nodes:
            node_id = n.get("node_id")
            if not node_id:
                errors += 1
                continue

            # Skip if already migrated
            existing = await conn.fetchrow(
                "SELECT 1 FROM industrial_nodes WHERE node_id = $1",
                node_id,
            )
            if existing:
                skipped += 1
                continue

            node_uuid = _to_uuid(n.get("node_uuid")) or UUID(int=0)
            aliases = n.get("aliases") or []
            if isinstance(aliases, str):
                try:
                    aliases = json.loads(aliases)
                except Exception:
                    aliases = []

            evidence = _evidence_to_jsonb(n.get("evidence"))

            try:
                await conn.execute(
                    """
                    INSERT INTO industrial_nodes (
                        node_id, node_uuid, canonical_name_zh, canonical_name_en,
                        aliases, definition, entity_type, evidence, confidence,
                        status, notes, is_test, created_at, updated_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    """,
                    node_id,
                    node_uuid,
                    n.get("canonical_name_zh") or node_id,
                    n.get("canonical_name_en"),
                    aliases,
                    n.get("definition") or "",
                    n.get("entity_type") or "unknown",
                    evidence,
                    n.get("confidence") or "LOW",
                    n.get("status") or "PENDING",
                    n.get("notes"),
                    n.get("is_test") or False,
                    _to_dt(n.get("created_at")),
                    _to_dt(n.get("updated_at")),
                )
                inserted += 1
            except Exception as exc:
                print(f"ERROR migrating {node_id}: {exc}", file=sys.stderr)
                errors += 1

    print(f"Migration complete: inserted={inserted}, skipped={skipped}, errors={errors}")

    await close_postgres_pool()
    await close_async_driver()
    return 0 if errors == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Migrate IndustrialNode metadata to PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated")
    args = parser.parse_args()

    rc = asyncio.run(migrate(dry_run=args.dry_run))
    sys.exit(rc)


if __name__ == "__main__":
    main()
