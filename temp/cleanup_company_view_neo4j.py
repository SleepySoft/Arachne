#!/usr/bin/env python3
"""
Cleanup script: Remove deprecated Company View data from Neo4j.

This script deletes:
  - All :INFERRED_UPSTREAM relationships
  - All :Company nodes (will be re-synced by Factual Graph layer)

Run after company_view code has been removed from the backend.
"""

from __future__ import annotations

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_async_driver, close_async_driver


async def cleanup() -> None:
    driver = get_async_driver()

    print("Deleting :INFERRED_UPSTREAM relationships ...", end=" ")
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH ()-[r:INFERRED_UPSTREAM]->()
            WITH r LIMIT 10000
            DELETE r
            RETURN count(r) AS cnt
            """
        )
        record = await result.single()
        deleted_rels = record["cnt"] if record else 0
    print(f"{deleted_rels} deleted")

    # Repeat until all are gone
    while deleted_rels > 0:
        print("  (more to delete) ...", end=" ")
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH ()-[r:INFERRED_UPSTREAM]->()
                WITH r LIMIT 10000
                DELETE r
                RETURN count(r) AS cnt
                """
            )
            record = await result.single()
            deleted_rels = record["cnt"] if record else 0
        print(f"{deleted_rels} deleted")

    print("Deleting :Company nodes ...", end=" ")
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:Company)
            WITH n LIMIT 10000
            DELETE n
            RETURN count(n) AS cnt
            """
        )
        record = await result.single()
        deleted_nodes = record["cnt"] if record else 0
    print(f"{deleted_nodes} deleted")

    while deleted_nodes > 0:
        print("  (more to delete) ...", end=" ")
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (n:Company)
                WITH n LIMIT 10000
                DELETE n
                RETURN count(n) AS cnt
                """
            )
            record = await result.single()
            deleted_nodes = record["cnt"] if record else 0
        print(f"{deleted_nodes} deleted")

    await close_async_driver()
    print("Cleanup complete.")


if __name__ == "__main__":
    asyncio.run(cleanup())
