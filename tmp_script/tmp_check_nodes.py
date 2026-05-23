import asyncio
import sys
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def list_nodes():
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run("MATCH (n:IndustrialNode) RETURN n.node_id AS node_id, n.canonical_name_zh AS name, n.entity_type AS type ORDER BY n.node_id")
        nodes = []
        async for rec in result:
            nid = rec["node_id"]
            name = rec["name"]
            etype = rec["type"]
            nodes.append(f"{nid} | {name} | {etype}")
        print("--- Existing Industrial Nodes ---")
        for n in nodes:
            print(n)
        print(f"Total: {len(nodes)}")

asyncio.run(list_nodes())
