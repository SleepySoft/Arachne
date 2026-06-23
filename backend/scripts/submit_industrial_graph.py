import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_node(node_data):
    resp = requests.post(f"{BASE_URL}/nodes", json=node_data)
    if resp.status_code == 200 or resp.status_code == 201:
        print(f"  OK node: {node_data['node_id']}")
        return resp.json()
    else:
        print(f"  FAIL node {node_data['node_id']}: {resp.status_code} {resp.text[:200]}")
        return None

def create_edge(edge_data):
    resp = requests.post(f"{BASE_URL}/edges", json=edge_data)
    if resp.status_code == 200 or resp.status_code == 201:
        print(f"  OK edge: {edge_data['edge_id']}")
        return resp.json()
    else:
        print(f"  FAIL edge {edge_data['edge_id']}: {resp.status_code} {resp.text[:200]}")
        return None

evidence_default = {
    "source_title": "tushare_stock_analysis_batch_001",
    "source_url": None,
    "quote": "Derived from company business scope and industry analysis",
    "retrieved_at": "2026-05-23T09:00:00Z"
}

def make_node(node_id, name_zh, name_en, entity_type, definition, notes=""):
    return {
        "node_id": node_id,
        "canonical_name_zh": name_zh,
        "canonical_name_en": name_en,
        "definition": definition,
        "entity_type": entity_type,
        "evidence": [evidence_default],
        "confidence": "HIGH",
        "status": "ACTIVE",
        "notes": notes
    }

def make_edge(edge_id, from_node, to_node, edge_type, description):
    return {
        "edge_namespace": "industrial_flow",
        "edge_id": edge_id,
        "from_node": from_node,
        "to_node": to_node,
        "edge_type": edge_type,
        "description": description,
        "evidence": [evidence_default],
        "confidence": "HIGH"
    }

# ====== NODES TO CREATE ======
nodes = [
    # Financial services
    make_node("public_deposit", "公众存款", "Public Deposit", "material", "个人及企业存入银行的资金，是银行开展信贷业务的基础资金来源。", "银行核心负债业务"),
    make_node("loan_service", "贷款服务", "Loan Service", "service", "银行向企业或个人提供资金支持并收取利息的金融服务。", "银行核心资产业务"),
    make_node("interbank_lending_service", "同业拆借服务", "Interbank Lending Service", "service", "金融机构之间进行短期资金融通的服务。", "银行流动性管理工具"),
    make_node("bond_investment_service", "债券投资服务", "Bond Investment Service", "service", "银行利用资金购买政府债券、金融债券等固定收益证券的投资服务。", "银行资金运用业务"),
    make_node("financial_bond", "金融债券", "Financial Bond", "service", "银行及其他金融机构为筹集资金而发行的债务凭证。", "银行主动负债工具"),

    # Real estate
    make_node("land", "土地", "Land", "material", "用于房地产开发建设的土地资源，是房地产产业链的最上游要素。", "房地产开发基础要素"),
    make_node("residential_property", "商品住宅", "Residential Property", "service", "面向个人消费者销售的住房产品，房地产企业的核心产出。", "房地产开发核心产出"),
    make_node("commercial_property", "商业地产", "Commercial Property", "service", "用于商业经营的地产项目，包括写字楼、商场、酒店等。", "房地产开发商业产出"),
    make_node("property_management_service", "物业服务", "Property Management Service", "service", "对已交付使用的物业进行维护、管理和运营的服务。", "房地产后服务"),
    make_node("housing_rental_service", "房屋租赁服务", "Housing Rental Service", "service", "将自有或受托管理的房屋出租给承租人使用并收取租金的服务。", "房地产运营服务"),
    make_node("construction_service", "建筑施工服务", "Construction Service", "service", "按照设计图纸和规范要求，将建筑材料转化为建筑物的工程服务。", "房地产开发核心环节"),
    make_node("cement", "水泥", "Cement", "material", "建筑工程中广泛使用的胶凝材料，是混凝土的主要组成部分。", "核心建筑材料"),

    # Rail transportation
    make_node("rail_vehicle", "轨道车辆", "Rail Vehicle", "device", "在轨道上运行的机车、动车组、地铁车辆等交通工具。", "轨道交通核心装备"),
    make_node("signaling_system", "信号系统", "Signaling System", "system", "用于控制列车运行、保证行车安全的通信与控制系统。", "轨道交通安全系统"),
    make_node("power_supply_system", "供电系统", "Power Supply System", "system", "为轨道交通提供牵引动力和运营用电的电力供应系统。", "轨道交通动力系统"),
    make_node("rail_maintenance_service", "轨道运维服务", "Rail Maintenance Service", "service", "对轨道交通线路、车辆、设备进行日常检修、维护和运营管理的综合服务。", "轨道交通后服务"),

    # Landscaping
    make_node("nursery_stock", "苗木", "Nursery Stock", "material", "用于园林绿化种植的树木、灌木、花卉等植物材料。", "园林绿化基础材料"),
    make_node("soil", "土壤", "Soil", "material", "用于植物栽培和地形塑造的自然或改良土壤材料。", "园林绿化基础材料"),
    make_node("gardening_material", "园艺材料", "Gardening Material", "material", "园林绿化工程中使用的肥料、基质、园艺工具等辅助材料。", "园林绿化辅助材料"),
    make_node("landscape_design_service", "景观设计服务", "Landscape Design Service", "service", "对室外空间进行艺术化规划和功能布局的专业设计服务。", "园林绿化前端服务"),
    make_node("greening_construction_service", "绿化施工服务", "Greening Construction Service", "service", "按照景观设计方案进行植物种植、地形整理和园林设施建设的工程服务。", "园林绿化核心施工"),
    make_node("ecological_restoration_service", "生态修复服务", "Ecological Restoration Service", "service", "对受损生态系统进行治理、恢复和重建的专业技术服务。", "园林绿化延伸服务"),

    # New energy materials
    make_node("silicon_material", "硅材料", "Silicon Material", "material", "用于光伏产业的高纯度硅原料，包括工业硅和多晶硅。", "光伏产业上游材料"),
    make_node("photovoltaic_module", "光伏组件", "Photovoltaic Module", "device", "将太阳能转换为电能的发电单元，由电池片、玻璃、背板等封装而成。", "光伏产业终端产品"),
]

# ====== EDGES TO CREATE ======
edges = [
    # Financial
    make_edge("public_deposit_to_loan", "public_deposit", "loan_service", "service_provision", "公众存款为银行贷款业务提供资金来源"),
    make_edge("public_deposit_to_interbank", "public_deposit", "interbank_lending_service", "service_provision", "公众存款为银行同业拆借业务提供资金基础"),
    make_edge("public_deposit_to_bond_inv", "public_deposit", "bond_investment_service", "service_provision", "公众存款为银行债券投资业务提供资金基础"),
    make_edge("financial_bond_to_bond_inv", "financial_bond", "bond_investment_service", "service_provision", "金融债券是债券投资服务的主要标的之一"),

    # Real estate
    make_edge("land_to_residential", "land", "residential_property", "material_input", "土地是商品住宅开发的基础要素投入"),
    make_edge("land_to_commercial", "land", "commercial_property", "material_input", "土地是商业地产开发的基础要素投入"),
    make_edge("cement_to_construction", "cement", "construction_service", "material_input", "水泥是建筑施工服务的主要原材料输入"),
    make_edge("construction_to_residential", "construction_service", "residential_property", "service_provision", "建筑施工服务将土地和材料转化为商品住宅"),
    make_edge("construction_to_commercial", "construction_service", "commercial_property", "service_provision", "建筑施工服务将土地和材料转化为商业地产"),
    make_edge("residential_to_property_mgmt", "residential_property", "property_management_service", "service_provision", "商品住宅交付后需要物业服务进行维护管理"),
    make_edge("commercial_to_property_mgmt", "commercial_property", "property_management_service", "service_provision", "商业地产交付后需要物业服务进行维护管理"),
    make_edge("residential_to_rental", "residential_property", "housing_rental_service", "service_provision", "商品住宅可通过租赁服务提供给承租人使用"),

    # Rail
    make_edge("rail_vehicle_to_maintenance", "rail_vehicle", "rail_maintenance_service", "service_provision", "轨道车辆需要运维服务进行检修和保养"),
    make_edge("signaling_to_maintenance", "signaling_system", "rail_maintenance_service", "service_provision", "信号系统需要运维服务进行维护和升级"),
    make_edge("power_to_maintenance", "power_supply_system", "rail_maintenance_service", "service_provision", "供电系统需要运维服务进行维护和保障"),

    # Landscaping
    make_edge("nursery_to_greening", "nursery_stock", "greening_construction_service", "material_input", "苗木是绿化施工服务的主要植物材料输入"),
    make_edge("soil_to_greening", "soil", "greening_construction_service", "material_input", "土壤是绿化施工服务的基础栽培介质"),
    make_edge("gardening_to_greening", "gardening_material", "greening_construction_service", "material_input", "园艺材料为绿化施工服务提供辅助支持"),
    make_edge("design_to_greening", "landscape_design_service", "greening_construction_service", "service_provision", "景观设计服务为绿化施工提供设计方案和指导"),
    make_edge("greening_to_eco_restore", "greening_construction_service", "ecological_restoration_service", "service_provision", "绿化施工服务是生态修复服务的实施手段之一"),

    # Solar
    make_edge("silicon_to_pv_module", "silicon_material", "photovoltaic_module", "material_input", "硅材料是光伏组件的核心原材料"),
    make_edge("pv_glass_to_module", "pv_glass", "photovoltaic_module", "structural_composition", "光伏玻璃是光伏组件的重要组成部分"),
]

print(f"Creating {len(nodes)} nodes...")
for node in nodes:
    create_node(node)

print(f"\nCreating {len(edges)} edges...")
for edge in edges:
    create_edge(edge)

print("\nDone!")
