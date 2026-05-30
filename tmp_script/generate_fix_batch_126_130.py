#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ev(source_title, quote="基础设施节点"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

INFRA_NODES = [
    {"node_id": "metal_product", "canonical_name_zh": "金属制品", "canonical_name_en": "metal product", "entity_type": "material", "aliases": [], "definition": "以金属为主要材料加工制造的产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "engineering_construction", "canonical_name_zh": "工程建设", "canonical_name_en": "engineering construction", "entity_type": "service", "aliases": [], "definition": "各类工程项目的施工和建设活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "packaging", "canonical_name_zh": "包装", "canonical_name_en": "packaging", "entity_type": "service", "aliases": [], "definition": "为产品提供包装和容器的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "agriculture", "canonical_name_zh": "农业", "canonical_name_en": "agriculture", "entity_type": "service", "aliases": [], "definition": "种植、养殖等农业生产活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "food_processing", "canonical_name_zh": "食品加工", "canonical_name_en": "food processing", "entity_type": "service", "aliases": [], "definition": "将原材料加工成食品产品的工业活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "cloud_computing", "canonical_name_zh": "云计算", "canonical_name_en": "cloud computing", "entity_type": "service", "aliases": [], "definition": "通过网络提供可扩展的计算资源和服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "hospitality", "canonical_name_zh": "酒店业", "canonical_name_en": "hospitality", "entity_type": "service", "aliases": [], "definition": "提供住宿、餐饮等接待服务的行业", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "battery_material", "canonical_name_zh": "电池材料", "canonical_name_en": "battery material", "entity_type": "material", "aliases": [], "definition": "用于制造电池的各类原材料和组件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "mechanical_equipment", "canonical_name_zh": "机械设备", "canonical_name_en": "mechanical equipment", "entity_type": "device", "aliases": [], "definition": "利用机械原理工作的各类工业设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "automotive_component", "canonical_name_zh": "汽车零部件", "canonical_name_en": "automotive component", "entity_type": "component", "aliases": [], "definition": "汽车的各种组成部件和零配件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "material", "canonical_name_zh": "材料", "canonical_name_en": "material", "entity_type": "material", "aliases": [], "definition": "用于制造产品的各类原材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "silicon_wafer", "canonical_name_zh": "硅片", "canonical_name_en": "silicon wafer", "entity_type": "component", "aliases": [], "definition": "用于半导体和光伏制造的硅基圆片", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "solar_energy", "canonical_name_zh": "太阳能", "canonical_name_en": "solar energy", "entity_type": "service", "aliases": [], "definition": "利用太阳光发电的清洁能源", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "led", "canonical_name_zh": "LED", "canonical_name_en": "LED", "entity_type": "component", "aliases": ["发光二极管"], "definition": "半导体发光器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "construction_material", "canonical_name_zh": "建筑材料", "canonical_name_en": "construction material", "entity_type": "material", "aliases": [], "definition": "用于建筑工程的各类材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "engine", "canonical_name_zh": "发动机", "canonical_name_en": "engine", "entity_type": "device", "aliases": [], "definition": "将能量转换为机械动力的装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "energy", "canonical_name_zh": "能源", "canonical_name_en": "energy", "entity_type": "service", "aliases": [], "definition": "能够产生动力的各种资源", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "battery", "canonical_name_zh": "电池", "canonical_name_en": "battery", "entity_type": "component", "aliases": [], "definition": "将化学能转换为电能的储能装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "textile", "canonical_name_zh": "纺织品", "canonical_name_en": "textile", "entity_type": "material", "aliases": [], "definition": "以纤维为原料织造或编织的产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
]

FIX_EDGES = [
    # Batch 126 failures
    {"edge_id": "fastener_metal_product", "from_node": "fastener", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "紧固件是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_wire_metal_product", "from_node": "steel_wire", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钢丝是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "zinc_ingot_metal_product", "from_node": "zinc_ingot", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锌锭是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    # Batch 127 failures
    {"edge_id": "engineering_design_engineering_construction", "from_node": "engineering_design", "to_node": "engineering_construction", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程设计是工程建设的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "supervision_consulting_engineering_construction", "from_node": "supervision_consulting", "to_node": "engineering_construction", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "监理咨询是工程建设的配套服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "general_contracting_engineering_construction", "from_node": "general_contracting", "to_node": "engineering_construction", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程总承包是工程建设的模式", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "printing_packaging", "from_node": "printing", "to_node": "packaging", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "印刷业务与包装密切相关", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "animal_feed_agriculture", "from_node": "animal_feed", "to_node": "agriculture", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "饲料服务于农业", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aquaculture_agriculture", "from_node": "aquaculture", "to_node": "agriculture", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "水产养殖是农业的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "pork_product_food_processing", "from_node": "pork_product", "to_node": "food_processing", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "猪肉制品是食品加工的产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "pig_breeding_agriculture", "from_node": "pig_breeding", "to_node": "agriculture", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "种猪繁育是农业活动", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mobile_cloud_computing_cloud_computing", "from_node": "mobile_cloud_computing", "to_node": "cloud_computing", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "移动云计算是云计算的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "video_cloud_cloud_computing", "from_node": "video_cloud", "to_node": "cloud_computing", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "视频云是云计算的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    # Batch 128 failures
    {"edge_id": "hotel_management_hospitality", "from_node": "hotel_management", "to_node": "hospitality", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "酒店管理服务是酒店业的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "food_beverage_hospitality", "from_node": "food_beverage", "to_node": "hospitality", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "餐饮业务是酒店业的一部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "manganese_dioxide_battery_material", "from_node": "manganese_dioxide", "to_node": "battery_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "二氧化锰是电池材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "electrolytic_metal_manganese_metal_product", "from_node": "electrolytic_metal_manganese", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电解金属锰是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "battery_manganese_material_battery_material", "from_node": "battery_manganese_material", "to_node": "battery_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电池锰材料是电池材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "heat_exchanger_mechanical_equipment", "from_node": "heat_exchanger", "to_node": "mechanical_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "换热器是机械设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "egr_system_automotive_component", "from_node": "egr_system", "to_node": "automotive_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "EGR系统是汽车零部件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "thermal_management_system_mechanical_equipment", "from_node": "thermal_management_system", "to_node": "mechanical_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "热管理系统是机械设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "nuclear_material_material", "from_node": "nuclear_material", "to_node": "material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "核材料是材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "solar_silicon_wafer_silicon_wafer", "from_node": "solar_silicon_wafer", "to_node": "silicon_wafer", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "太阳能硅片是硅片的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "solar_cell_solar_energy", "from_node": "solar_cell", "to_node": "solar_energy", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "太阳能电池是太阳能产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "solar_module_solar_energy", "from_node": "solar_module", "to_node": "solar_energy", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "太阳能组件是太阳能产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    # Batch 129 failures
    {"edge_id": "sapphire_substrate_led", "from_node": "sapphire_substrate", "to_node": "led", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "蓝宝石衬底用于LED制造", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_structure_construction_material", "from_node": "steel_structure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钢结构是建筑材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "membrane_structure_construction_material", "from_node": "membrane_structure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "膜结构是建筑材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "diesel_engine_engine", "from_node": "diesel_engine", "to_node": "engine", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "柴油发动机是发动机的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engine_component_engine", "from_node": "engine_component", "to_node": "engine", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "发动机零部件是发动机的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "hydraulic_power_mechanical_equipment", "from_node": "hydraulic_power", "to_node": "mechanical_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "液压动力是机械设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "coal_energy", "from_node": "coal", "to_node": "energy", "edge_namespace": "industrial_flow", "edge_type": "energy_flow", "description": "煤炭是能源的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "new_energy_energy", "from_node": "new_energy", "to_node": "energy", "edge_namespace": "industrial_flow", "edge_type": "energy_flow", "description": "新能源是能源的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lithium_battery_battery", "from_node": "lithium_battery", "to_node": "battery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锂电池是电池的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "motor_mechanical_equipment", "from_node": "motor", "to_node": "mechanical_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电机是机械设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    # Batch 130 failures
    {"edge_id": "rare_earth_metal_product", "from_node": "rare_earth", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "稀土是金属产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "environmental_engineering_engineering_construction", "from_node": "environmental_engineering", "to_node": "engineering_construction", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "环保工程是工程建设的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lead_zinc_metal_metal_product", "from_node": "lead_zinc_metal", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "铅锌金属是金属产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "car_interior_automotive_component", "from_node": "car_interior", "to_node": "automotive_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "汽车内饰是汽车零部件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "automotive_fabric_textile", "from_node": "automotive_fabric", "to_node": "textile", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "汽车面料是纺织品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "medical_textile_textile", "from_node": "medical_textile", "to_node": "textile", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "医用纺织品是纺织品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lithium_ion_battery_material_battery_material", "from_node": "lithium_ion_battery_material", "to_node": "battery_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锂离子电池材料是电池材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "electrolyte_battery_material", "from_node": "electrolyte", "to_node": "battery_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电解液是电池材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

graph = {
    "batch_id": "fix_batch_126_130",
    "task_description": "Fix missing infrastructure nodes and edges for batches 126-130",
    "nodes_to_upsert": INFRA_NODES,
    "edges_to_upsert": FIX_EDGES
}

with open(os.path.join(BASE_DIR, "tmp_script", "fix_batch_126_130_nodes.json"), "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

print(f"Fix batch: {len(INFRA_NODES)} nodes, {len(FIX_EDGES)} edges")
