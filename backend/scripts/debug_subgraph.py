import asyncio
from app.database import get_async_driver
from app.services import industry_storage
from app.models.schemas import IndustrialNode
from app.services.neo4j_storage import _to_datetime

async def test():
    # Test banking subgraph
    industry = await industry_storage.get_industry("banking")
    print(f"Industry found: {industry.industry_id if industry else 'None'}")
    
    mappings, _ = await industry_storage.list_mappings_by_industry("banking", limit=1000)
    node_ids = [m.node_id for m in mappings]
    print(f"Node IDs: {node_ids}")
    
    driver = get_async_driver()
    async with driver.session() as session:
        node_result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n
            """,
            node_ids=node_ids,
        )
        node_records = await node_result.data()
        print(f"Node records count: {len(node_records)}")
        
        for record in node_records:
            props = dict(record["n"])
            print(f"Props keys: {props.keys()}")
            print(f"created_at type: {type(props.get('created_at'))}")
            props["created_at"] = _to_datetime(props.get("created_at"))
            props["updated_at"] = _to_datetime(props.get("updated_at"))
            try:
                node = IndustrialNode(**props)
                print(f"Node OK: {node.node_id}")
            except Exception as e:
                print(f"Node ERROR: {e}")
                print(f"Props: {props}")

asyncio.run(test())
