# -*- coding: utf-8 -*-
"""
Refactor the silicon subgraph to avoid broad nodes and misuse of composition.
- Create semiconductor_material
- silicon is_a semiconductor_material (instead of semiconductor)
- silicon material_flow silicon_wafer (composition removed)
- silicon_wafer material_flow semiconductor_device
- chip is_a semiconductor_device (fix reversed is_a)
"""
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

async def main():
    async with httpx.AsyncClient() as c:
        # 1. Create semiconductor_material node
        node = {
            "node_id": "semiconductor_material",
            "canonical_name_zh": "半导体材料",
            "canonical_name_en": "Semiconductor Material",
            "definition": "用于制造半导体器件、集成电路、芯片等电子产品的原材料，包括硅、锗、砷化镓等单质或化合物材料。",
            "entity_type": "material",
            "confidence": "MEDIUM",
            "status": "ACTIVE",
            "evidence": [{"source_title": "半导体材料通用分类", "quote": "半导体材料包括硅、锗、砷化镓等，用于制造集成电路和半导体器件。"}],
        }
        r = await c.post(f"{BASE}/nodes", json=node)
        print("create semiconductor_material:", r.status_code, r.text[:200])

        # 2. Delete old/wrong edges
        to_delete = [
            "silicon_is_a_semiconductor",
            "silicon_to_silicon_wafer",
            "semiconductor_device_is_a_chip",
        ]
        for eid in to_delete:
            r = await c.delete(f"{BASE}/edges/{eid}")
            print(f"delete {eid}:", r.status_code)

        # 3. Create new edges
        edges = [
            {
                "edge_id": "silicon_is_a_semiconductor_material",
                "edge_namespace": "ontology",
                "edge_type": "is_a",
                "from_node": "silicon",
                "to_node": "semiconductor_material",
                "description": "硅是一种重要的半导体材料。",
                "confidence": "HIGH",
                "evidence": [{"source_title": "半导体材料通用分类", "quote": "硅（Si）是最常用的元素半导体材料之一。"}],
            },
            {
                "edge_id": "silicon_wafer_to_semiconductor_device",
                "edge_namespace": "industrial_flow",
                "edge_type": "material_flow",
                "from_node": "silicon_wafer",
                "to_node": "semiconductor_device",
                "description": "硅片经过光刻、刻蚀、离子注入、薄膜沉积等制造工序，加工成为半导体器件。",
                "confidence": "MEDIUM",
                "evidence": [],
            },
            {
                "edge_id": "chip_is_a_semiconductor_device",
                "edge_namespace": "ontology",
                "edge_type": "is_a",
                "from_node": "chip",
                "to_node": "semiconductor_device",
                "description": "芯片是一种实现具体功能的半导体器件。",
                "confidence": "HIGH",
                "evidence": [{"source_title": "半导体器件通用定义", "quote": "芯片（Chip/IC）是在半导体衬底上制造出的具有特定功能的微型电子器件。"}],
            },
        ]
        for e in edges:
            r = await c.post(f"{BASE}/edges", json=e)
            print(f"create {e['edge_id']}:", r.status_code, r.text[:200])

asyncio.run(main())
