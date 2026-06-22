# -*- coding: utf-8 -*-
"""
处理剩余的 R17 违规：为每个高频来源或目标领域插入 process 节点，
将 material -> product 直接边迁移为 material -> process -> product。
"""
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

EVIDENCE = {
    "process": {"source_title": "产业本体设计规则", "quote": "原材料需通过工艺过程节点转化为产品。"},
    "aluminum": {"source_title": "铝加工工艺", "quote": "铝板可通过冲压、挤压、机加工、表面处理等工艺制成活塞、幕墙、电容器箔等制品。"},
    "cement": {"source_title": "水泥制品制造", "quote": "水泥与骨料、水混合后成型养护制成水泥制品。"},
    "automotive_fuel": {"source_title": "燃油喷射系统制造", "quote": "柴油作为工质，燃油喷射系统由精密零部件加工装配而成。"},
    "wood": {"source_title": "人造板制造", "quote": "木材产品通过胶合、热压、贴面等工序制成人造板。"},
    "real_estate": {"source_title": "房地产开发流程", "quote": "土地通过规划、设计、施工、销售等环节开发为商业地产或商品住宅。"},
    "paper": {"source_title": "纸包装制造", "quote": "纸浆、纸板等经模切、印刷、折叠、粘合等工序制成纸包装制品。"},
    "pcb": {"source_title": "印制电路板制造", "quote": "覆铜板经蚀刻、钻孔、电镀、层压等工序制成印制电路板。"},
    "pet": {"source_title": "PET瓶胚注塑", "quote": "PET树脂经注塑成型制成瓶胚。"},
    "plastic": {"source_title": "塑料制品加工", "quote": "塑胶原料经注塑、挤出等工序制成注塑件、型材等塑料制品。"},
    "rubber": {"source_title": "橡胶制品制造", "quote": "高分子橡胶材料经混炼、硫化、成型制成密封件、轮胎等橡胶制品。"},
    "steel": {"source_title": "金属钣金成形", "quote": "冷轧钢板经冲压、焊接、机加工、热处理制成结构件、壳体、轴承等金属制品。"},
}

NEW_NODES = [
    {
        "node_id": "aluminum_panel_processing",
        "canonical_name_zh": "铝板加工",
        "canonical_name_en": "Aluminum Panel Processing",
        "definition": "将铝板通过冲压、挤压、机加工、表面处理等工序制成建筑幕墙、活塞、电容器箔等铝制品的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["aluminum"]],
    },
    {
        "node_id": "cement_product_manufacturing",
        "canonical_name_zh": "水泥制品制造",
        "canonical_name_en": "Cement Product Manufacturing",
        "definition": "将水泥与骨料、水等混合后成型、养护，制成水泥制品和预制构件的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["cement"]],
    },
    {
        "node_id": "fuel_injection_system_manufacturing",
        "canonical_name_zh": "燃油喷射系统制造",
        "canonical_name_en": "Fuel Injection System Manufacturing",
        "definition": "将燃油喷射系统零部件进行精密加工、装配和标定，形成完整燃油喷射系统的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["automotive_fuel"]],
    },
    {
        "node_id": "wood_based_panel_manufacturing",
        "canonical_name_zh": "人造板制造",
        "canonical_name_en": "Wood-based Panel Manufacturing",
        "definition": "将木材产品、浸渍纸等原料通过胶合、热压、贴面等工序制成人造板的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["wood"]],
    },
    {
        "node_id": "real_estate_development",
        "canonical_name_zh": "房地产开发",
        "canonical_name_en": "Real Estate Development",
        "definition": "将土地通过规划、设计、施工、销售等环节开发为商业地产或商品住宅的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["real_estate"]],
    },
    {
        "node_id": "paper_packaging_manufacturing",
        "canonical_name_zh": "纸包装制造",
        "canonical_name_en": "Paper Packaging Manufacturing",
        "definition": "将纸浆、纸板、瓦楞纸等包装材料通过模切、印刷、折叠、粘合等工序制成纸箱、纸盒等纸包装制品的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["paper"]],
    },
    {
        "node_id": "printed_circuit_board_fabrication",
        "canonical_name_zh": "印制电路板制造",
        "canonical_name_en": "Printed Circuit Board Fabrication",
        "definition": "将覆铜板通过蚀刻、钻孔、电镀、层压等工序制成印制电路板的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["pcb"]],
    },
    {
        "node_id": "pet_preform_injection_molding",
        "canonical_name_zh": "PET瓶胚注塑",
        "canonical_name_en": "PET Preform Injection Molding",
        "definition": "将PET树脂加热熔融后注入模具，冷却成型为瓶胚的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["pet"]],
    },
    {
        "node_id": "plastic_processing",
        "canonical_name_zh": "塑料制品加工",
        "canonical_name_en": "Plastic Processing",
        "definition": "将塑胶原料通过注塑、挤出等工序制成注塑件、塑料型材等塑料制品的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["plastic"]],
    },
    {
        "node_id": "rubber_seal_molding",
        "canonical_name_zh": "橡胶密封件成型",
        "canonical_name_en": "Rubber Seal Molding",
        "definition": "将高分子橡胶材料通过混炼、硫化、成型等工序制成橡胶密封件的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["rubber"]],
    },
    {
        "node_id": "tire_manufacturing",
        "canonical_name_zh": "轮胎制造",
        "canonical_name_en": "Tire Manufacturing",
        "definition": "将橡胶、钢丝、帘布等原材料通过混炼、压延、成型、硫化等工序制成轮胎的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["rubber"]],
    },
    {
        "node_id": "steel_sheet_metal_forming",
        "canonical_name_zh": "钢板钣金成形",
        "canonical_name_en": "Steel Sheet Metal Forming",
        "definition": "将冷轧钢板通过冲压、焊接、机加工、热处理等工序制成炮弹壳体、气缸套、轴承、导弹/火箭弹结构件等金属制品的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["steel"]],
    },
]

EDGES_TO_DELETE = [
    "flow_alum_to_piston",
    "flow_alum_to_curtain",
    "flow_aluminum_to_capacitor",
    "flow_cement_to_cement_product",
    "flow_diesel_to_injection",
    "flow_impregnated_to_board",
    "flow_wood_to_board",
    "land_to_commercial",
    "land_to_residential",
    "flow_packaging_material_to_paper_pack",
    "flow_pulp_to_packaging",
    "pcb_substrate_to_pcb",
    "flow_pet_resin_to_preform",
    "flow_plastic_to_inject",
    "flow_plastic_to_profile",
    "flow_polymer_to_seal",
    "flow_rubber_to_tire",
    "flow_steel_to_shell",
    "flow_steel_to_cylinder",
    "flow_steel_to_missile",
    "flow_steel_to_psd",
    "flow_steel_to_rocket",
    "flow_steel_to_bearing",
]

NEW_EDGES = [
    # aluminum panel
    {"edge_id": "aluminum_panel_to_processing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "aluminum_panel", "to_node": "aluminum_panel_processing",
     "description": "铝板作为原材料输入铝板加工过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["aluminum"]]},
    {"edge_id": "aluminum_panel_processing_produces_piston", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "aluminum_panel_processing", "to_node": "aluminum_piston",
     "description": "铝板加工过程产出铝活塞。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["aluminum"]]},
    {"edge_id": "aluminum_panel_processing_produces_curtain_wall", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "aluminum_panel_processing", "to_node": "building_curtain_wall",
     "description": "铝板加工过程产出建筑幕墙。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["aluminum"]]},
    {"edge_id": "aluminum_panel_processing_produces_capacitor", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "aluminum_panel_processing", "to_node": "electronic_capacitor",
     "description": "铝板加工过程产出电子电容器用铝箔及壳体。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["aluminum"]]},

    # cement
    {"edge_id": "cement_to_cement_product_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "cement", "to_node": "cement_product_manufacturing",
     "description": "水泥作为胶凝材料输入水泥制品制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["cement"]]},
    {"edge_id": "cement_product_manufacturing_produces_product", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "cement_product_manufacturing", "to_node": "cement_product",
     "description": "水泥制品制造过程产出水泥制品。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["cement"]]},

    # diesel / fuel injection
    {"edge_id": "diesel_to_fuel_injection_system_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "diesel", "to_node": "fuel_injection_system_manufacturing",
     "description": "柴油作为工质和测试介质输入燃油喷射系统制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive_fuel"]]},
    {"edge_id": "fuel_injection_system_manufacturing_produces_system", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "fuel_injection_system_manufacturing", "to_node": "fuel_injection_system",
     "description": "燃油喷射系统制造过程产出燃油喷射系统。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["automotive_fuel"]]},

    # wood / artificial board
    {"edge_id": "impregnated_paper_to_wood_based_panel_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "impregnated_paper", "to_node": "wood_based_panel_manufacturing",
     "description": "浸渍纸作为表面贴面材料输入人造板制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["wood"]]},
    {"edge_id": "wood_product_to_wood_based_panel_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "wood_product", "to_node": "wood_based_panel_manufacturing",
     "description": "木材产品作为基材输入人造板制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["wood"]]},
    {"edge_id": "wood_based_panel_manufacturing_produces_board", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "wood_based_panel_manufacturing", "to_node": "artificial_board",
     "description": "人造板制造过程产出人造板。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["wood"]]},

    # real estate
    {"edge_id": "land_to_real_estate_development", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "land", "to_node": "real_estate_development",
     "description": "土地作为基础要素输入房地产开发过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["real_estate"]]},
    {"edge_id": "real_estate_development_produces_commercial_property", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "real_estate_development", "to_node": "commercial_property",
     "description": "房地产开发过程产出商业地产。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["real_estate"]]},
    {"edge_id": "real_estate_development_produces_residential_property", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "real_estate_development", "to_node": "residential_property",
     "description": "房地产开发过程产出商品住宅。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["real_estate"]]},

    # paper packaging
    {"edge_id": "packaging_material_to_paper_packaging_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "packaging_material", "to_node": "paper_packaging_manufacturing",
     "description": "包装材料输入纸包装制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["paper"]]},
    {"edge_id": "paper_pulp_to_paper_packaging_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "paper_pulp", "to_node": "paper_packaging_manufacturing",
     "description": "纸浆作为原料输入纸包装制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["paper"]]},
    {"edge_id": "paper_packaging_manufacturing_produces_product", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "paper_packaging_manufacturing", "to_node": "paper_packaging_product",
     "description": "纸包装制造过程产出纸包装制品。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["paper"]]},

    # pcb
    {"edge_id": "pcb_substrate_to_pcb_fabrication", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "pcb_substrate", "to_node": "printed_circuit_board_fabrication",
     "description": "覆铜板作为核心基材输入印制电路板制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["pcb"]]},
    {"edge_id": "pcb_fabrication_produces_pcb_board", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "printed_circuit_board_fabrication", "to_node": "pcb_board",
     "description": "印制电路板制造过程产出印制电路板。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["pcb"]]},

    # pet preform
    {"edge_id": "pet_resin_to_preform_molding", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "pet_resin", "to_node": "pet_preform_injection_molding",
     "description": "PET树脂作为原料输入瓶胚注塑过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["pet"]]},
    {"edge_id": "preform_molding_produces_bottle_preform", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "pet_preform_injection_molding", "to_node": "bottle_preform",
     "description": "PET瓶胚注塑过程产出瓶胚。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["pet"]]},

    # plastic
    {"edge_id": "plastic_resin_to_plastic_processing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "plastic_resin", "to_node": "plastic_processing",
     "description": "塑胶原料输入塑料制品加工过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["plastic"]]},
    {"edge_id": "plastic_processing_produces_injection_part", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "plastic_processing", "to_node": "injection_molding_part",
     "description": "塑料制品加工过程产出注塑件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["plastic"]]},
    {"edge_id": "plastic_processing_produces_profile", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "plastic_processing", "to_node": "plastic_profile",
     "description": "塑料制品加工过程产出塑料型材。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["plastic"]]},

    # rubber seal
    {"edge_id": "polymer_material_to_rubber_seal_molding", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "polymer_material", "to_node": "rubber_seal_molding",
     "description": "高分子橡胶材料输入橡胶密封件成型过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["rubber"]]},
    {"edge_id": "rubber_seal_molding_produces_seal", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "rubber_seal_molding", "to_node": "rubber_seal",
     "description": "橡胶密封件成型过程产出橡胶密封件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["rubber"]]},

    # tire
    {"edge_id": "rubber_to_tire_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "rubber", "to_node": "tire_manufacturing",
     "description": "橡胶作为原材料输入轮胎制造过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["rubber"]]},
    {"edge_id": "tire_manufacturing_produces_tire", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "tire_manufacturing", "to_node": "tire",
     "description": "轮胎制造过程产出轮胎。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["rubber"]]},

    # steel sheet
    {"edge_id": "steel_sheet_to_metal_forming", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "steel_sheet", "to_node": "steel_sheet_metal_forming",
     "description": "冷轧钢板作为原材料输入钢板钣金成形过程。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_shell", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "artillery_shell",
     "description": "钢板钣金成形过程产出炮弹壳体。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_cylinder_liner", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "cylinder_liner",
     "description": "钢板钣金成形过程产出气缸套。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_missile", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "missile",
     "description": "钢板钣金成形过程产出导弹结构件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_psd", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "platform_screen_door",
     "description": "钢板钣金成形过程产出站台屏蔽门结构件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_rocket", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "rocket",
     "description": "钢板钣金成形过程产出火箭弹结构件。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
    {"edge_id": "steel_sheet_metal_forming_produces_bearing", "edge_namespace": "industrial_flow", "edge_type": "produces",
     "from_node": "steel_sheet_metal_forming", "to_node": "rolling_bearing",
     "description": "钢板钣金成形过程产出滚动轴承。", "confidence": "MEDIUM",
     "evidence": [EVIDENCE["steel"]]},
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
