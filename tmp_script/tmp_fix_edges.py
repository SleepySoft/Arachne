import json, asyncio, httpx

API_BASE = "http://localhost:8000/api/v1"

FAILED_EDGES = [
    {"edge_id": "cement_to_construction", "from_node": "cement", "to_node": "construction_service", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "水泥作为核心建筑材料输入到建筑施工服务中", "evidence": [{"source_title": "建筑行业常识", "quote": "水泥是混凝土的主要胶凝材料"}], "confidence": "HIGH"},
    {"edge_id": "construction_to_residential", "from_node": "construction_service", "to_node": "residential_property", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "建筑施工服务将原材料建造成商品住宅", "evidence": [{"source_title": "沙河股份年报", "quote": "从事房地产开发经营业务"}], "confidence": "HIGH"},
    {"edge_id": "construction_to_commercial", "from_node": "construction_service", "to_node": "commercial_property", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "建筑施工服务将原材料建造成商业地产", "evidence": [{"source_title": "沙河股份年报", "quote": "从事房地产开发经营业务"}], "confidence": "HIGH"},
    {"edge_id": "residential_to_property_mgmt", "from_node": "residential_property", "to_node": "property_management_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商品住宅交付后需要物业管理服务进行运营维护", "evidence": [{"source_title": "沙河股份年报", "quote": "物业管理业务"}], "confidence": "HIGH"},
    {"edge_id": "commercial_to_property_mgmt", "from_node": "commercial_property", "to_node": "property_management_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业地产交付后需要物业管理服务进行运营维护", "evidence": [{"source_title": "沙河股份年报", "quote": "物业管理业务"}], "confidence": "HIGH"},
    {"edge_id": "watch_to_watch_retail", "from_node": "watch", "to_node": "watch_retail_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "手表产品通过钟表零售服务销售给终端消费者", "evidence": [{"source_title": "飞亚达年报", "quote": "钟表及其零配件的制造、销售和维修"}], "confidence": "HIGH"},
]

async def submit():
    batch = {
        "batch_id": "batch_002_edge_fix",
        "task_description": "Batch 002 edge fix: 重新提交之前失败的6条产业流边。",
        "nodes_to_upsert": [],
        "edges_to_upsert": FAILED_EDGES,
        "rejected_or_pending": []
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/batches", json=batch, timeout=120.0)
        print(f"Status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

asyncio.run(submit())
