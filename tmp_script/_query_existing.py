import sys, os
os.chdir('C:/D/code/Arachne')
sys.path.insert(0, 'backend')
import asyncio
from app.database import get_async_driver

async def main():
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run('MATCH (n:IndustrialNode) RETURN n.node_id AS node_id, n.canonical_name_zh AS name, n.entity_type AS type ORDER BY n.node_id')
        records = await result.data()
        print(f'Total nodes: {len(records)}')
        for r in records:
            print(f"{r['node_id']} | {r['name']} | {r['type']}")
    await driver.close()

asyncio.run(main())
