import asyncio, sys
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def debug():
    driver = get_async_driver()
    async with driver.session() as session:
        # Check nodes
        for nid in ['watch', 'watch_retail_service']:
            result = await session.run("MATCH (n:IndustrialNode {node_id: $id}) RETURN n", id=nid)
            rec = await result.single()
            print(f"Node {nid}: {'EXISTS' if rec else 'MISSING'}")
            if rec:
                print(f"  props: {dict(rec['n'])}")
        
        # Try CREATE with explicit node labels and ids
        result2 = await session.run("""
            MATCH (a:IndustrialNode {node_id: 'watch'})
            MATCH (b:IndustrialNode {node_id: 'watch_retail_service'})
            RETURN a.node_id AS a_id, b.node_id AS b_id
        """)
        rec2 = await result2.single()
        print(f"MATCH result: {dict(rec2) if rec2 else None}")

asyncio.run(debug())
