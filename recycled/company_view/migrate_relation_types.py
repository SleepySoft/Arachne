"""
One-off migration: add relation_type and relation_subtype to existing
INFERRED_UPSTREAM edges in Neo4j.

Run: cd backend && python scripts/migrate_relation_types.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_async_driver


async def migrate():
    driver = get_async_driver()

    async with driver.session() as session:
        # Set properties on all INFERRED_UPSTREAM edges that don't have them yet
        result = await session.run(
            """
            MATCH ()-[r:INFERRED_UPSTREAM]->()
            WHERE r.relation_type IS NULL
            SET r.relation_type = 'inferred_industrial'
            SET r.relation_subtype = 'upstream_of'
            RETURN count(r) AS cnt
            """
        )
        record = await result.single()
        updated = record["cnt"] if record else 0
        print(f"Updated {updated} edges with relation_type='inferred_industrial', relation_subtype='upstream_of'")

        # Verify
        result2 = await session.run(
            """
            MATCH ()-[r:INFERRED_UPSTREAM]->()
            RETURN count(r) AS total,
                   count(CASE WHEN r.relation_type IS NOT NULL THEN 1 END) AS with_type
            """
        )
        record2 = await result2.single()
        print(f"Total edges: {record2['total']}, With type: {record2['with_type']}")


if __name__ == "__main__":
    asyncio.run(migrate())
