# -*- coding: utf-8 -*-
"""
在多个高频领域插入 process 节点，将 material/device/capability -> product 的直接边
迁移为 material/device/capability -> process -> product 的规范结构。
"""
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

EVIDENCE = {
    "process": {"source_title": "产业本体设计规则", "quote": "原材料、设备与能力需通过工艺过程节点转化为产品。"},
    "eda": {"source_title": "半导体设计流程", "quote": "EDA 软件为芯片设计过程提供设计、仿真与实现工具支撑。"},
    "copper": {"source_title": "铜加工产业链", "quote": "阴极铜经熔铸、轧制、拉拔等加工制成铜箔、铜板带、铜线及电线电缆。"},
    "automotive": {"source_title": "汽车轻量化材料应用", "quote": "汽车钢材和铝材经冲压、压铸、焊接等成形工艺制成底盘、制动、传动等系统零部件。"},
    "glass": {"source_title": "玻璃与光纤制造工艺", "quote": "石英砂、纯碱等原料经高温熔融、成型制成浮法玻璃、电子玻璃、光伏玻璃；高纯石英砂经熔融拉制成光纤。"},
}

NEW_NODES = [
    {
        "node_id": "automotive_steel_forming_process",
        "canonical_name_zh": "汽车钢材成形工艺",
        "canonical_name_en": "Automotive Steel Forming Process",
        "definition": "将汽车钢材通过冲压、焊接、机加工、热处理等工序制成车身、底盘、传动、制动、悬架等系统零部件的制造过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["automotive"]],
    },
    {
        "node_id": "automotive_aluminum_forming_process",
        "canonical_name_zh": "汽车铝材成形工艺",
        "canonical_name_en": "Automotive Aluminum Forming Process",
        "definition": "将汽车铝材通过压铸、挤压、机加工等工序制成轻量化底盘、制动系统等零部件的制造过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["automotive"]],
    },
    {
        "node_id": "copper_processing",
        "canonical_name_zh": "铜加工",
        "canonical_name_en": "Copper Processing",
        "definition": "将阴极铜通过熔铸、轧制、拉拔等工序制成铜箔、铜板带、铜线等铜加工材的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["copper"]],
    },
    {
        "node_id": "wire_cable_manufacturing",
        "canonical_name_zh": "电线电缆制造",
        "canonical_name_en": "Wire and Cable Manufacturing",
        "definition": "将铜线或铝线通过绞合、绝缘挤出、护套等工序制成电线电缆产品的制造过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["copper"]],
    },
    {
        "node_id": "glass_manufacturing",
        "canonical_name_zh": "玻璃制造",
        "canonical_name_en": "Glass Manufacturing",
        "definition": "将石英砂、纯碱等原料经高温熔融、成型、退火等工序制成浮法玻璃、电子玻璃、光伏玻璃等玻璃制品的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["glass"]],
    },
    {
        "node_id": "optical_fiber_manufacturing",
        "canonical_name_zh": "光纤制造",
        "canonical_name_en": "Optical Fiber Manufacturing",
        "definition": "将高纯度石英砂经熔融、拉制成光纤预制棒并进一步拉丝、涂覆制成光纤及光缆的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["glass"]],
    },
]

EDGES_TO_DELETE = [
    # EDA / chip
    "eda_software_supports_chip",
    "molybdenum_film_to_chip",
    "tungsten_film_to_chip",
    "silicon_wafer_to_wafer",
    "silicon_wafer_to_semiconductor_device",
    # copper
    "flow_copper_to_foil",
    "flow_copper_to_sheet",
    "flow_copper_to_wire",
    "flow_copper_to_wire_cable",
    # automotive steel
    "flow_steel_to_brake",
    "flow_steel_to_engine_acc",
    "flow_steel_to_env",
    "flow_steel_to_steering",
    "flow_steel_to_transmission",
    "flow_steel_to_chassis",
    "flow_steel_to_susp",
    # automotive aluminum
    "flow_alum_to_brake",
    "flow_alum_to_chassis",
    # glass / quartz / soda
    "flow_quartz_to_elec",
    "flow_quartz_to_float",
    "flow_quartz_to_fiber_cable",
    "flow_quartz_to_pv",
    "flow_soda_to_float",
]

NEW_EDGES = [
    # EDA -> chip design -> chip
    {"edge_id": "eda_software_to_chip_design", "edge_namespace": "industrial_flow", "edge_type": "information_flow",
     "from_node": "eda_software", "to_node": "chip_design",
     "description": "EDA 软件为芯片设计过程提供设计、仿真、物理实现等工具能力支撑。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["eda"]]},
    {"edge_id": "chip_design_produces_chip", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "chip_design", "to_node": "chip",
     "description": "芯片设计过程输出芯片设计数据并指导后续制造，最终得到芯片产品。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["eda"]]},

    # semiconductor materials -> wafer_manufacturing -> products
    {"edge_id": "silicon_wafer_to_wafer_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "silicon_wafer", "to_node": "wafer_manufacturing",
     "description": "硅片作为晶圆制造的基础原材料输入。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},
    {"edge_id": "molybdenum_film_to_wafer_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "molybdenum_film", "to_node": "wafer_manufacturing",
     "description": "钼薄膜作为金属化材料输入晶圆制造过程的薄膜沉积环节。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},
    {"edge_id": "tungsten_film_to_wafer_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "tungsten_film", "to_node": "wafer_manufacturing",
     "description": "钨薄膜作为金属化材料输入晶圆制造过程的薄膜沉积环节。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},
    {"edge_id": "wafer_manufacturing_produces_wafer", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "wafer_manufacturing", "to_node": "wafer",
     "description": "晶圆制造过程将硅片等材料加工为晶圆。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},
    {"edge_id": "wafer_manufacturing_produces_chip", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "wafer_manufacturing", "to_node": "chip",
     "description": "晶圆制造过程在晶圆上完成电路加工，最终产出芯片。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},
    {"edge_id": "wafer_manufacturing_produces_semiconductor_device", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "wafer_manufacturing", "to_node": "semiconductor_device",
     "description": "晶圆制造过程将硅片加工为半导体器件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["process"]]},

    # copper
    {"edge_id": "copper_to_copper_processing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "copper", "to_node": "copper_processing",
     "description": "阴极铜作为原料输入铜加工过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},
    {"edge_id": "copper_processing_produces_foil", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "copper_processing", "to_node": "copper_foil",
     "description": "铜加工过程通过轧制等工序产出铜箔。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},
    {"edge_id": "copper_processing_produces_sheet", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "copper_processing", "to_node": "copper_sheet",
     "description": "铜加工过程通过轧制等工序产出铜板带。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},
    {"edge_id": "copper_processing_produces_wire", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "copper_processing", "to_node": "copper_wire",
     "description": "铜加工过程通过拉拔等工序产出铜线。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},
    {"edge_id": "copper_to_wire_cable_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "copper", "to_node": "wire_cable_manufacturing",
     "description": "阴极铜作为导体材料输入电线电缆制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},
    {"edge_id": "wire_cable_manufacturing_produces_wire_cable", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "wire_cable_manufacturing", "to_node": "wire_cable",
     "description": "电线电缆制造过程产出电线电缆产品。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["copper"]]},

    # automotive steel
    {"edge_id": "automotive_steel_to_forming_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "automotive_steel", "to_node": "automotive_steel_forming_process",
     "description": "汽车钢材作为原材料输入汽车钢材成形工艺。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_brake", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "automotive_brake_system",
     "description": "汽车钢材成形工艺产出汽车制动系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_engine_accessory", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "automotive_engine_accessory",
     "description": "汽车钢材成形工艺产出汽车发动机附件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_env", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "automotive_environment_system",
     "description": "汽车钢材成形工艺产出汽车环境系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_steering", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "automotive_steering_system",
     "description": "汽车钢材成形工艺产出汽车转向系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_transmission", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "automotive_transmission_system",
     "description": "汽车钢材成形工艺产出汽车传动系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_chassis", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "chassis_system",
     "description": "汽车钢材成形工艺产出底盘系统结构件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "steel_forming_produces_suspension", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_steel_forming_process", "to_node": "suspension_system",
     "description": "汽车钢材成形工艺产出悬架系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},

    # automotive aluminum
    {"edge_id": "automotive_aluminum_to_forming_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "automotive_aluminum", "to_node": "automotive_aluminum_forming_process",
     "description": "汽车铝材作为原材料输入汽车铝材成形工艺。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "aluminum_forming_produces_brake", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_aluminum_forming_process", "to_node": "automotive_brake_system",
     "description": "汽车铝材成形工艺产出轻量化汽车制动系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},
    {"edge_id": "aluminum_forming_produces_chassis", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "automotive_aluminum_forming_process", "to_node": "chassis_system",
     "description": "汽车铝材成形工艺产出轻量化底盘系统零部件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive"]]},

    # glass / quartz / soda
    {"edge_id": "quartz_sand_to_glass_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "quartz_sand", "to_node": "glass_manufacturing",
     "description": "石英砂作为玻璃制造的主要硅质原料输入。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "soda_ash_to_glass_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "soda_ash", "to_node": "glass_manufacturing",
     "description": "纯碱作为助熔剂输入玻璃制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "glass_manufacturing_produces_float", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "glass_manufacturing", "to_node": "float_glass",
     "description": "玻璃制造过程产出浮法玻璃。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "glass_manufacturing_produces_electronic_glass", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "glass_manufacturing", "to_node": "electronic_glass",
     "description": "玻璃制造过程产出电子玻璃。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "glass_manufacturing_produces_pv_glass", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "glass_manufacturing", "to_node": "pv_glass",
     "description": "玻璃制造过程产出光伏玻璃。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "quartz_sand_to_optical_fiber_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "quartz_sand", "to_node": "optical_fiber_manufacturing",
     "description": "高纯石英砂作为光纤制造的核心原料输入。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
    {"edge_id": "optical_fiber_manufacturing_produces_cable", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "optical_fiber_manufacturing", "to_node": "optical_fiber_cable",
     "description": "光纤制造过程产出光缆产品。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["glass"]]},
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

        print("\n=== creating new edges ===")
        for edge in NEW_EDGES:
            await create_edge(client, edge)

        print("\n=== deleting old direct edges ===")
        for edge_id in EDGES_TO_DELETE:
            await delete_edge(client, edge_id)


if __name__ == "__main__":
    asyncio.run(main())
