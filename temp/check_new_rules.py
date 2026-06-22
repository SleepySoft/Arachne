# -*- coding: utf-8 -*-
import asyncio
from app.database import get_async_driver


async def main():
    driver = get_async_driver()
    async with driver.session() as s:
        print("=== device -> product edges ===")
        result = await s.run(
            """
            MATCH (d:IndustrialNode {entity_type:'device'})-[r:INDUSTRIAL_FLOW]->(p:IndustrialNode)
            WHERE p.entity_type IN ['component','module','subsystem','system','platform','application_system']
            RETURN d.node_id AS from_id, d.canonical_name_zh AS from_name,
                   p.node_id AS to_id, p.canonical_name_zh AS to_name, p.entity_type AS to_type,
                   r.edge_id AS edge_id, r.edge_type AS et
            ORDER BY from_id, to_id
            """
        )
        rows = 0
        async for rec in result:
            rows += 1
            print(
                f"  {rec['edge_id']}: {rec['from_name']}({rec['from_id']}) -> "
                f"{rec['to_name']}({rec['to_id']}) [{rec['to_type']}/{rec['et']}]"
            )
        print(f"total {rows}")

        print("\n=== company <-> industrial edges ===")
        result = await s.run(
            """
            MATCH (a)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b)
            WHERE (a:Company AND b:IndustrialNode) OR (a:IndustrialNode AND b:Company)
            RETURN labels(a) AS la, a.node_id AS a_id, labels(b) AS lb, b.node_id AS b_id,
                   type(r) AS rt, r.edge_id AS eid
            ORDER BY eid
            """
        )
        rows = 0
        async for rec in result:
            rows += 1
            print(
                f"  {rec['eid']}: {rec['la']} {rec['a_id']} -> {rec['lb']} {rec['b_id']} [{rec['rt']}]"
            )
        print(f"total {rows}")


if __name__ == "__main__":
    asyncio.run(main())
