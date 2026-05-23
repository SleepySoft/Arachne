import asyncio, sys
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def check():
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run("MATCH (n:IndustrialNode) RETURN n.node_id AS id ORDER BY n.node_id")
        async for rec in result:
            print(rec["id"])

asyncio.run(check())
