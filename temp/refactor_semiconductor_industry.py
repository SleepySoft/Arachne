# -*- coding: utf-8 -*-
"""
为半导体行业补充并映射工艺节点，减少 chip 节点的直接下游连接数。
"""
import asyncio
import httpx
import uuid

BASE = "http://localhost:16060/api/v1"
INDUSTRY_ID = "semiconductor_industry"

EVIDENCE = {
    "process": {"source_title": "产业本体设计规则", "quote": "芯片需通过封测、系统集成等应用工艺环节进入下游电子系统。"},
    "packaging": {"source_title": "半导体封测工艺", "quote": "芯片完成前端制造后，需经过封装与测试才能成为可用的半导体器件。"},
    "integration": {"source_title": "电子系统集成", "quote": "芯片及器件通过板级/系统级集成进入汽车电子、消费电子、服务器等终端应用。"},
}

NEW_NODES = [
    {
        "node_id": "chip_packaging_and_testing",
        "canonical_name_zh": "芯片封测",
        "canonical_name_en": "Chip Packaging and Testing",
        "definition": "将已完成前道制造的晶圆或芯片进行切割、封装、测试，使其成为可交付半导体器件的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["packaging"]],
    },
    {
        "node_id": "electronics_system_integration",
        "canonical_name_zh": "电子系统集成",
        "canonical_name_en": "Electronics System Integration",
        "definition": "将芯片、器件、模块等通过板卡、整机设计集成到汽车电子、消费电子、服务器、智能手机等终端系统的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["integration"]],
    },
]

PROCESS_NODES_TO_MAP = [
    "wafer_manufacturing",
    "chip_design",
    "lithography_process",
    "etching_process",
    "thin_film_deposition_process",
    "ion_implantation_process",
    "cleaning_process",
    "cmp_process",
    "metrology_inspection",
    "chip_packaging_and_testing",
    "electronics_system_integration",
]

EDGES_TO_DELETE = [
    "chip_to_automotive_electronics",
    "chip_to_consumer_electronics",
    "chip_to_industrial_electronics",
    "chip_to_new_energy_vehicle",
    "chip_to_personal_computer",
    "chip_to_server",
    "chip_to_smartphone",
    "chip_material_flow_osat",
]

NEW_EDGES = [
    # chip -> packaging/testing -> system integration -> applications
    {"edge_id": "chip_to_packaging_and_testing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "chip", "to_node": "chip_packaging_and_testing",
     "description": "芯片进入封测环节进行封装和测试。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["packaging"]]},
    {"edge_id": "packaging_and_testing_to_system_integration", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "chip_packaging_and_testing", "to_node": "electronics_system_integration",
     "description": "封测后的芯片及器件进入电子系统集成环节。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_automotive_electronics", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "automotive_electronics",
     "description": "电子系统集成过程产出汽车电子系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_consumer_electronics", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "consumer_electronics",
     "description": "电子系统集成过程产出消费电子系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_industrial_electronics", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "industrial_electronics",
     "description": "电子系统集成过程产出工业电子系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_new_energy_vehicle", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "new_energy_vehicle",
     "description": "电子系统集成过程产出新能源汽车电子电气系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_personal_computer", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "personal_computer",
     "description": "电子系统集成过程产出个人计算机系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_server", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "server",
     "description": "电子系统集成过程产出服务器系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},
    {"edge_id": "system_integration_to_smartphone", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronics_system_integration", "to_node": "smartphone",
     "description": "电子系统集成过程产出智能手机系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["integration"]]},

    # OSAT provides capability to packaging/testing, not directly to chip
    {"edge_id": "osat_to_packaging_and_testing", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "osat", "to_node": "chip_packaging_and_testing",
     "description": "OSAT 为芯片封测提供封装与测试服务能力。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["packaging"]]},
]


async def create_node(client: httpx.AsyncClient, node: dict):
    try:
        r = await client.post(f"{BASE}/nodes", json=node)
        if r.status_code == 201:
            print(f"  created node {node['node_id']}")
        elif r.status_code == 409:
            print(f"  node {node['node_id']} already exists")
        else:
            print(f"  failed node {node['node_id']}: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"  error node {node['node_id']}: {e}")


async def create_mapping(client: httpx.AsyncClient, node_id: str):
    mapping_id = f"{INDUSTRY_ID}_contains_{node_id}"
    payload = {
        "mapping_id": mapping_id,
        "industry_id": INDUSTRY_ID,
        "node_id": node_id,
        "role": "制造工艺",
        "weight": 1.0,
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    }
    try:
        r = await client.post(f"{BASE}/industries/{INDUSTRY_ID}/mappings", json=payload)
        if r.status_code == 201:
            print(f"  mapped {node_id}")
        elif r.status_code == 409:
            print(f"  mapping for {node_id} already exists")
        else:
            print(f"  failed map {node_id}: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"  error map {node_id}: {e}")


async def create_edge(client: httpx.AsyncClient, edge: dict):
    try:
        r = await client.post(f"{BASE}/edges", json=edge)
        if r.status_code == 201:
            print(f"  created edge {edge['edge_id']}")
        elif r.status_code == 400 and "already exists" in r.text.lower():
            print(f"  edge {edge['edge_id']} already exists")
        else:
            print(f"  failed edge {edge['edge_id']}: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"  error edge {edge['edge_id']}: {e}")


async def delete_edge(client: httpx.AsyncClient, edge_id: str):
    try:
        r = await client.delete(f"{BASE}/edges/{edge_id}")
        if r.status_code == 204:
            print(f"  deleted edge {edge_id}")
        elif r.status_code == 404:
            print(f"  edge {edge_id} not found")
        else:
            print(f"  failed delete {edge_id}: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"  error delete {edge_id}: {e}")


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        print("=== creating process nodes ===")
        for node in NEW_NODES:
            await create_node(client, node)

        print("\n=== mapping process nodes to semiconductor industry ===")
        for node_id in PROCESS_NODES_TO_MAP:
            await create_mapping(client, node_id)

        print("\n=== creating new edges ===")
        for edge in NEW_EDGES:
            await create_edge(client, edge)

        print("\n=== deleting old direct edges ===")
        for edge_id in EDGES_TO_DELETE:
            await delete_edge(client, edge_id)


if __name__ == "__main__":
    asyncio.run(main())
