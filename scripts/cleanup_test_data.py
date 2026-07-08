#!/usr/bin/env python3
"""Standalone script to delete all test data.

Loads the backend app context and calls the cleanup service directly. This is
useful as a post-test hook when you do not want to go through the HTTP API.

Usage:
    python scripts/cleanup_test_data.py
    python scripts/cleanup_test_data.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Make backend imports available
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.test_data_cleanup import cleanup_test_data


def _print_summary(result: dict):
    print("Test data cleanup result:")
    print(f"  dry_run: {result.get('dry_run', False)}")
    print("  Neo4j:")
    for key, count in result.get("neo4j", {}).items():
        print(f"    {key}: {count}")
    print("  PostgreSQL:")
    pg = result.get("postgres", {})
    if not pg.get("available", True):
        print("    (PostgreSQL not available)")
    else:
        for table, info in pg.items():
            if table in ("available",):
                continue
            count = info["count"] if isinstance(info, dict) else info
            print(f"    {table}: {count}")


async def main():
    parser = argparse.ArgumentParser(description="Delete all test data")
    parser.add_argument("--dry-run", action="store_true", help="Count without deleting")
    args = parser.parse_args()

    result = await cleanup_test_data(dry_run=args.dry_run)
    _print_summary(result)

    if args.dry_run:
        print("\n[DRY-RUN] No data was deleted.")
    else:
        print("\n[OK] Test data deleted.")


if __name__ == "__main__":
    asyncio.run(main())
