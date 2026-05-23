import json, asyncio, httpx

API_BASE = "http://localhost:8000/api/v1"

# Missing nodes
MISSING_NODES = [
    {
        "node_id": "magnetic_head",
        "canonical_name_zh": "磁头",
        "canonical_name_en": "Magnetic Head",
        "aliases": ["硬盘磁头", "读写磁头"],
        "definition": "硬盘驱动器中用于在旋转盘片上进行数据读写操作的精密电磁部件，是硬盘的核心组件之一。",
        "entity_type": "component",
        "evidence": [{"source_title": "深科技2024年年报", "source_url": None, "quote": "硬盘磁头业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE",
        "notes": "深科技核心产品之一"
    },
    {
        "node_id": "hard_disk_platter",
        "canonical_name_zh": "硬盘盘片",
        "canonical_name_en": "Hard Disk Platter",
        "aliases": ["盘基片", "磁盘片"],
        "definition": "硬盘驱动器中用于存储数据的圆形磁性盘片，通常由铝合金或玻璃基材制成，表面涂覆磁性材料。",
        "entity_type": "component",
        "evidence": [{"source_title": "深科技2024年年报", "source_url": None, "quote": "盘基片业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE",
        "notes": "深科技核心产品之一"
    }
]

# Failed edges
FAILED_EDGES = [
    {"edge_id": "cement_to_construction", "from_node": "cement", "to_node": "construction_service", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "水泥作为核心建筑材料输入到建筑施工服务中", "evidence": [{"source_title": "建筑行业常识", "quote": "水泥是混凝土的主要胶凝材料"}], "confidence": "HIGH"},
    {"edge_id": "construction_to_residential", "from_node": "construction_service", "to_node": "residential_property", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "建筑施工服务将原材料建造成商品住宅", "evidence": [{"source_title": "沙河股份年报", "quote": "从事房地产开发经营业务"}], "confidence": "HIGH"},
    {"edge_id": "construction_to_commercial", "from_node": "construction_service", "to_node": "commercial_property", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "建筑施工服务将原材料建造成商业地产", "evidence": [{"source_title": "沙河股份年报", "quote": "从事房地产开发经营业务"}], "confidence": "HIGH"},
    {"edge_id": "residential_to_property_mgmt", "from_node": "residential_property", "to_node": "property_management_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商品住宅交付后需要物业管理服务进行运营维护", "evidence": [{"source_title": "沙河股份年报", "quote": "物业管理业务"}], "confidence": "HIGH"},
    {"edge_id": "commercial_to_property_mgmt", "from_node": "commercial_property", "to_node": "property_management_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业地产交付后需要物业管理服务进行运营维护", "evidence": [{"source_title": "沙河股份年报", "quote": "物业管理业务"}], "confidence": "HIGH"},
    {"edge_id": "magnetic_head_to_hdd", "from_node": "magnetic_head", "to_node": "hard_disk_drive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "磁头是硬盘驱动器的核心读写部件", "evidence": [{"source_title": "深科技年报", "quote": "硬盘磁头业务"}], "confidence": "HIGH"},
    {"edge_id": "hard_disk_platter_to_hdd", "from_node": "hard_disk_platter", "to_node": "hard_disk_drive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "盘基片是硬盘驱动器中存储数据的磁性盘片", "evidence": [{"source_title": "深科技年报", "quote": "盘基片业务"}], "confidence": "HIGH"},
    {"edge_id": "watch_to_watch_retail", "from_node": "watch", "to_node": "watch_retail_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "手表产品通过钟表零售服务销售给终端消费者", "evidence": [{"source_title": "飞亚达年报", "quote": "钟表及其零配件的制造、销售和维修"}], "confidence": "HIGH"},
]

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_002_fix",
        "task_description": "Batch 002 fix: 补充缺失的磁头和盘基片节点，以及重新提交失败的8条产业流边。",
        "nodes_to_upsert": MISSING_NODES,
        "edges_to_upsert": FAILED_EDGES,
        "rejected_or_pending": []
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/batches", json=batch, timeout=120.0)
        print(f"Status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

asyncio.run(submit_graph_batch())
