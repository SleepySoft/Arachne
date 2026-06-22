# -*- coding: utf-8 -*-
import asyncio
import json
from collections import defaultdict
from app.database import get_async_driver


async def main():
    driver = get_async_driver()
    async with driver.session() as s:
        result = await s.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE a.entity_type IN ['material','device','technology_capability']
              AND b.entity_type IN ['component','module','subsystem','system','platform','application_system']
              AND r.edge_type IN ['material_flow','capability_supply','information_flow']
            RETURN a.node_id AS from_id, a.canonical_name_zh AS from_name, a.entity_type AS from_type,
                   r.edge_type AS et, r.edge_id AS edge_id, r.description AS description,
                   b.node_id AS to_id, b.canonical_name_zh AS to_name, b.entity_type AS to_type
            ORDER BY from_id, to_id
            """
        )
        rows = []
        by_source = defaultdict(list)
        by_target = defaultdict(list)
        async for rec in result:
            item = {
                "edge_id": rec["edge_id"],
                "from_id": rec["from_id"],
                "from_name": rec["from_name"],
                "from_type": rec["from_type"],
                "to_id": rec["to_id"],
                "to_name": rec["to_name"],
                "to_type": rec["to_type"],
                "edge_type": rec["et"],
                "description": rec["description"],
            }
            rows.append(item)
            by_source[rec["from_id"]].append(item)
            by_target[rec["to_id"]].append(item)

    out_path = "C:/D/Code/git/Arachne/temp/r17_violations.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total": len(rows),
                "by_source": dict(by_source),
                "by_target": {k: v for k, v in sorted(by_target.items(), key=lambda x: -len(x[1]))[:30]},
                "items": rows,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"total={len(rows)}")
    print("top sources:")
    for sid, items in sorted(by_source.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {sid}({items[0]['from_name']}): {len(items)}")
    print("top targets:")
    for tid, items in sorted(by_target.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {tid}({items[0]['to_name']}): {len(items)}")


if __name__ == "__main__":
    asyncio.run(main())
