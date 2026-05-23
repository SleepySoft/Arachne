import asyncio, sys
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def check():
    driver = get_async_driver()
    nodes = ['hard_disk_drive', 'watch', 'watch_retail_service', 'magnetic_head', 'hard_disk_platter', 'cement', 'construction_service', 'residential_property', 'commercial_property', 'property_management_service']
    async with driver.session() as session:
        for n in nodes:
            result = await session.run('MATCH (n:IndustrialNode {node_id: $id}) RETURN n.node_id AS id', id=n)
            rec = await result.single()
            status = "EXISTS" if rec else "MISSING"
            print(f"{n}: {status}")

asyncio.run(check())
