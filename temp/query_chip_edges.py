# -*- coding: utf-8 -*-
import asyncio
from app.database import get_async_driver


async def main():
    driver = get_async_driver()
    async with driver.session() as s:
        print("=== from chip ===")
        result = await s.run(
            """
            MATCH (chip:IndustrialNode {node_id: 'chip'})-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(n:IndustrialNode)
            RETURN type(r) AS ns, r.edge_type AS et, r.edge_id AS eid, n.node_id AS nid, n.canonical_name_zh AS name, n.entity_type AS t
            ORDER BY ns, et, nid
            """
        )
        from_rows = []
        async for rec in result:
            from_rows.append(rec)
        print(f"total={len(from_rows)}")
        for rec in from_rows:
            print(f"  {rec['eid']}: chip -> {rec['name']}({rec['nid']}) [{rec['ns']}/{rec['et']}] [{rec['t']}]")

        print("\n=== to chip ===")
        result = await s.run(
            """
            MATCH (n:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(chip:IndustrialNode {node_id: 'chip'})
            RETURN type(r) AS ns, r.edge_type AS et, r.edge_id AS eid, n.node_id AS nid, n.canonical_name_zh AS name, n.entity_type AS t
            ORDER BY ns, et, nid
            """
        )
        to_rows = []
        async for rec in result:
            to_rows.append(rec)
        print(f"total={len(to_rows)}")
        for rec in to_rows:
            print(f"  {rec['eid']}: {rec['name']}({rec['nid']}) -> chip [{rec['ns']}/{rec['et']}] [{rec['t']}]")


if __name__ == "__main__":
    asyncio.run(main())
