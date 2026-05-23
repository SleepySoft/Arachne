import asyncio, sys, json
sys.path.insert(0, 'backend')
from app.database import get_async_driver
from datetime import datetime

async def create():
    driver = get_async_driver()
    now = datetime.utcnow()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:IndustrialNode {node_id: $from_node})
            MATCH (b:IndustrialNode {node_id: $to_node})
            CREATE (a)-[r:INDUSTRIAL_FLOW {
                edge_uuid: $edge_uuid,
                edge_id: $edge_id,
                edge_namespace: $edge_namespace,
                edge_type: $edge_type,
                description: $description,
                evidence: $evidence,
                confidence: $confidence,
                notes: $notes,
                created_at: $now,
                updated_at: $now
            }]->(b)
            RETURN r, a AS start_node, b AS end_node
            """,
            edge_uuid="test-uuid",
            edge_id="watch_to_watch_retail",
            edge_namespace="industrial_flow",
            edge_type="service_flow",
            from_node="watch",
            to_node="watch_retail_service",
            description="手表产品通过钟表零售服务销售给终端消费者",
            evidence=json.dumps([{"source_title": "飞亚达年报", "quote": "钟表及其零配件的制造、销售和维修"}], ensure_ascii=False),
            confidence="HIGH",
            notes=None,
            now=now,
        )
        record = await result.single()
        print(f"Record: {record}")

asyncio.run(create())
