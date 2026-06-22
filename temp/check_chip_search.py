# -*- coding: utf-8 -*-
import asyncio
from app.database import get_async_driver


async def main():
    driver = get_async_driver()
    async with driver.session() as s:
        result = await s.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.canonical_name_zh CONTAINS '芯片' OR n.node_id CONTAINS 'chip' OR ANY(a IN n.aliases WHERE a CONTAINS '芯片')
            RETURN n.node_id AS id, n.canonical_name_zh AS name
            ORDER BY n.canonical_name_zh
            """
        )
        rows = []
        async for rec in result:
            rows.append((rec["id"], rec["name"]))
        print("total", len(rows))
        for i, (node_id, name) in enumerate(rows[:20]):
            print(i + 1, node_id, name)


if __name__ == "__main__":
    asyncio.run(main())
