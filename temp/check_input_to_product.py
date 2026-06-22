# -*- coding: utf-8 -*-
import asyncio
from app.database import get_async_driver


async def main():
    driver = get_async_driver()
    async with driver.session() as s:
        print("=== material/device/tech_capability -> product ===")
        result = await s.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE a.entity_type IN ['material','device','technology_capability']
              AND b.entity_type IN ['component','module','subsystem','system','platform','application_system']
              AND r.edge_type IN ['material_flow','capability_supply','information_flow']
            RETURN a.node_id AS a_id, a.canonical_name_zh AS a_name, a.entity_type AS a_type,
                   r.edge_type AS et, r.edge_id AS eid,
                   b.node_id AS b_id, b.canonical_name_zh AS b_name, b.entity_type AS b_type
            ORDER BY a_id, b_id
            """
        )
        rows = 0
        async for rec in result:
            rows += 1
            print(
                f"  {rec['eid']}: {rec['a_name']}({rec['a_type']}) --{rec['et']}--> "
                f"{rec['b_name']}({rec['b_type']})"
            )
        print(f"total {rows}")

        print("\n=== process -> product ===")
        result = await s.run(
            """
            MATCH (p:IndustrialNode {entity_type:'process'})-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE b.entity_type IN ['component','module','subsystem','system','platform','application_system']
            RETURN p.node_id AS p_id, p.canonical_name_zh AS p_name, r.edge_type AS et, r.edge_id AS eid,
                   b.node_id AS b_id, b.canonical_name_zh AS b_name
            ORDER BY p_id, b_id
            """
        )
        rows = 0
        async for rec in result:
            rows += 1
            print(f"  {rec['eid']}: {rec['p_name']} --{rec['et']}--> {rec['b_name']}")
        print(f"total {rows}")


if __name__ == "__main__":
    asyncio.run(main())
