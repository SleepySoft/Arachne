import asyncio, sys, json
from datetime import datetime
sys.path.insert(0, 'backend')
from app.database import get_async_driver

async def create():
    driver = get_async_driver()
    now = datetime.utcnow()
    async with driver.session() as session:
        result = await session.run(
            """
            CREATE (n:IndustrialNode {
                node_uuid: $node_uuid,
                node_id: $node_id,
                canonical_name_zh: $canonical_name_zh,
                canonical_name_en: $canonical_name_en,
                aliases: $aliases,
                definition: $definition,
                entity_type: $entity_type,
                evidence: $evidence,
                confidence: $confidence,
                status: $status,
                notes: $notes,
                created_at: $now,
                updated_at: $now
            })
            RETURN n
            """,
            node_uuid="6a3e8f12-9c4d-4b8a-a1e2-5f7d3c6b9a0e",
            node_id="watch_retail_service",
            canonical_name_zh="钟表零售服务",
            canonical_name_en="Watch Retail Service",
            aliases=["钟表销售", "手表零售"],
            definition="通过门店、电商等渠道向终端消费者销售手表及钟表产品的零售服务。",
            entity_type="service",
            evidence=json.dumps([{"source_title": "飞亚达2024年年报", "source_url": None, "quote": "世界名表的商业连锁销售"}], ensure_ascii=False),
            confidence="HIGH",
            status="ACTIVE",
            notes="飞亚达业务之一",
            now=now,
        )
        record = await result.single()
        print(f"Created: {record is not None}")

asyncio.run(create())
