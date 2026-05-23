import asyncio, sys
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def check():
    driver = get_async_driver()
    edges = ['cement_to_construction', 'construction_to_residential', 'construction_to_commercial', 
             'residential_to_property_mgmt', 'commercial_to_property_mgmt', 'watch_to_watch_retail']
    async with driver.session() as session:
        for eid in edges:
            result = await session.run("MATCH ()-[r {edge_id: $id}]->() RETURN r.edge_id AS id", id=eid)
            rec = await result.single()
            status = "EXISTS" if rec else "MISSING"
            print(f"{eid}: {status}")

asyncio.run(check())
