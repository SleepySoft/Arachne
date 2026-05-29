#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batch 123 submission scripts."""
import json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

def write_batch(batch_num, nodes, edges, companies, exposures):
    graph = {
        "batch_id": f"batch_{batch_num}_nodes",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges
    }
    path_g = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_nodes.json")
    with open(path_g, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    business = {
        "batch_id": f"batch_{batch_num}_business",
        "task_description": f"Batch {batch_num} business registration",
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures,
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": []
    }
    path_b = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_business.json")
    with open(path_b, "w", encoding="utf-8") as f:
        json.dump(business, f, ensure_ascii=False, indent=2)
    print(f"Batch {batch_num}: {len(nodes)} nodes, {len(edges)} edges, {len(companies)} companies, {len(exposures)} exposures")

NODES_123 = [
    {"node_id": "wind_turbine_blade", "canonical_name_zh": "风力发电机叶片", "canonical_name_en": "wind turbine blade", "entity_type": "component", "aliases": [], "definition": "风力发电机组中将风能转化为机械能的旋转叶片", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材科技主营业务")},
    {"node_id": "high_pressure_composite_vessel", "canonical_name_zh": "高压复合气瓶", "canonical_name_en": "high pressure composite vessel", "entity_type": "component", "aliases": ["CNG瓶"], "definition": "采用复合材料制造的可承受高压的气体储存容器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材科技经营范围")},
    {"node_id": "membrane_material_product", "canonical_name_zh": "膜材料制品", "canonical_name_en": "membrane material product", "entity_type": "material", "aliases": [], "definition": "用于过滤、分离、渗透等功能的薄膜材料制品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材科技经营范围")},
    {"node_id": "lithium_battery_separator", "canonical_name_zh": "锂电池隔膜", "canonical_name_en": "lithium battery separator", "entity_type": "component", "aliases": [], "definition": "锂离子电池中隔离正负极的多孔薄膜", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材科技经营范围")},
    {"node_id": "public_decoration", "canonical_name_zh": "公共建筑装饰", "canonical_name_en": "public decoration", "entity_type": "service", "aliases": [], "definition": "对公共建筑内部空间进行装饰装修的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金螳螂主营业务")},
    {"node_id": "wood_product", "canonical_name_zh": "木制品", "canonical_name_en": "wood product", "entity_type": "material", "aliases": [], "definition": "以木材为原料加工制造的各类产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金螳螂经营范围")},
    {"node_id": "landscape_engineering", "canonical_name_zh": "园林景观", "canonical_name_en": "landscape engineering", "entity_type": "service", "aliases": [], "definition": "园林绿化的设计、施工和养护服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金螳螂经营范围")},
    {"node_id": "ancient_building_engineering", "canonical_name_zh": "古建筑工程", "canonical_name_en": "ancient building engineering", "entity_type": "service", "aliases": [], "definition": "对古建筑进行保护、修缮和复原的工程服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金螳螂经营范围")},
    {"node_id": "aluminum_profile", "canonical_name_zh": "铝合金型材", "canonical_name_en": "aluminum profile", "entity_type": "material", "aliases": [], "definition": "通过挤压工艺生产的铝合金截面材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万邦德主营业务")},
    {"node_id": "aluminum_plate", "canonical_name_zh": "铝板", "canonical_name_en": "aluminum plate", "entity_type": "material", "aliases": [], "definition": "厚度较大的平板状铝材", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万邦德经营范围")},
    {"node_id": "coal_sales", "canonical_name_zh": "煤炭销售", "canonical_name_en": "coal sales", "entity_type": "service", "aliases": [], "definition": "煤炭产品的销售和贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("平煤股份主营业务")},
    {"node_id": "electricity_sales", "canonical_name_zh": "电力销售", "canonical_name_en": "electricity sales", "entity_type": "service", "aliases": [], "definition": "电力产品的销售和供应活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("平煤股份经营范围")},
    {"node_id": "towel", "canonical_name_zh": "毛巾", "canonical_name_en": "towel", "entity_type": "material", "aliases": [], "definition": "用于擦拭的棉质纺织品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("孚日股份主营业务")},
    {"node_id": "decorative_fabric", "canonical_name_zh": "装饰布", "canonical_name_en": "decorative fabric", "entity_type": "material", "aliases": [], "definition": "用于装饰用途的各类纺织面料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("孚日股份主营业务")},
    {"node_id": "bathroom_hardware", "canonical_name_zh": "卫浴五金", "canonical_name_en": "bathroom hardware", "entity_type": "component", "aliases": [], "definition": "用于卫生间的各类金属配件和五金件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("海鸥住工主营业务")},
    {"node_id": "faucet", "canonical_name_zh": "水龙头", "canonical_name_en": "faucet", "entity_type": "component", "aliases": [], "definition": "控制水流的管道终端阀门装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("海鸥住工主营业务")},
    {"node_id": "sanitary_ware", "canonical_name_zh": "卫生陶瓷", "canonical_name_en": "sanitary ware", "entity_type": "material", "aliases": [], "definition": "用于卫生间和厨房的陶瓷洁具", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("海鸥住工主营业务")},
    {"node_id": "building_ceramics", "canonical_name_zh": "建筑陶瓷", "canonical_name_en": "building ceramics", "entity_type": "material", "aliases": [], "definition": "用于建筑装饰的陶瓷材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("海鸥住工经营范围")},
    {"node_id": "aluminum_wheel", "canonical_name_zh": "铝合金车轮", "canonical_name_en": "aluminum wheel", "entity_type": "component", "aliases": [], "definition": "采用铝合金材料制造的车辆轮毂", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万丰奥威主营业务")},
    {"node_id": "dacro_coating", "canonical_name_zh": "涂复加工", "canonical_name_en": "dacro coating", "entity_type": "service", "aliases": [], "definition": "在金属表面进行防腐涂层的加工服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万丰奥威经营范围")},
    {"node_id": "magnesium_alloy", "canonical_name_zh": "镁合金", "canonical_name_en": "magnesium alloy", "entity_type": "material", "aliases": [], "definition": "以镁为基础的合金材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万丰奥威经营范围")},
    {"node_id": "stamping_part", "canonical_name_zh": "冲压件", "canonical_name_en": "stamping part", "entity_type": "component", "aliases": [], "definition": "通过冲压工艺成型的金属零件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("万丰奥威经营范围")},
    {"node_id": "marine_product", "canonical_name_zh": "海洋产品", "canonical_name_en": "marine product", "entity_type": "material", "aliases": [], "definition": "来自海洋的各类产品，包括海产品和海洋药物", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东方海洋经营范围")},
    {"node_id": "ceramic_fiber", "canonical_name_zh": "陶瓷纤维", "canonical_name_en": "ceramic fiber", "entity_type": "material", "aliases": [], "definition": "以陶瓷为原料制成的高性能纤维材料，用于高温绝热", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("鲁阳节能主营业务")},
    {"node_id": "thermal_insulation_material", "canonical_name_zh": "保温材料", "canonical_name_en": "thermal insulation material", "entity_type": "material", "aliases": [], "definition": "用于减少热传导的材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("鲁阳节能经营范围")},
    {"node_id": "refractory_product", "canonical_name_zh": "耐火材料", "canonical_name_en": "refractory product", "entity_type": "material", "aliases": [], "definition": "在高温环境下能保持结构稳定的材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("鲁阳节能经营范围")},
    {"node_id": "crude_oil_transportation", "canonical_name_zh": "原油运输", "canonical_name_en": "crude oil transportation", "entity_type": "service", "aliases": [], "definition": "利用船舶运输原油的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("招商轮船主营业务")},
    {"node_id": "dry_bulk_shipping", "canonical_name_zh": "干散货运输", "canonical_name_en": "dry bulk shipping", "entity_type": "service", "aliases": [], "definition": "利用船舶运输干散货物的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("招商轮船主营业务")},
    {"node_id": "lng_transportation", "canonical_name_zh": "LNG运输", "canonical_name_en": "LNG transportation", "entity_type": "service", "aliases": [], "definition": "利用专用船舶运输液化天然气的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("招商轮船经营范围")},
    {"node_id": "ship_leasing", "canonical_name_zh": "船舶租赁", "canonical_name_en": "ship leasing", "entity_type": "service", "aliases": [], "definition": "船舶经营租赁和融资租赁服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("招商轮船经营范围")},
]

EDGES_123 = [
    {"edge_id": "wind_turbine_blade_wind_power_generation", "from_node": "wind_turbine_blade", "to_node": "wind_power_generation", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "风力发电机叶片是风力发电设备的关键部件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "high_pressure_composite_vessel_cng_equipment", "from_node": "high_pressure_composite_vessel", "to_node": "cng_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "高压复合气瓶是CNG设备的关键组件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lithium_battery_separator_power_battery", "from_node": "lithium_battery_separator", "to_node": "power_battery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锂电池隔膜是动力电池的关键组件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "membrane_material_product_filtration_equipment", "from_node": "membrane_material_product", "to_node": "filtration_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "膜材料制品是过滤设备的核心组件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "public_decoration_building_decoration", "from_node": "public_decoration", "to_node": "building_decoration", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "公共建筑装饰是建筑装饰的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "wood_product_building_decoration", "from_node": "wood_product", "to_node": "building_decoration", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "木制品用于建筑装饰", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "landscape_engineering_building_decoration", "from_node": "landscape_engineering", "to_node": "building_decoration", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "园林景观是建筑装饰的延伸服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ancient_building_engineering_building_decoration", "from_node": "ancient_building_engineering", "to_node": "building_decoration", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "古建筑工程是建筑装饰的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aluminum_profile_aluminum", "from_node": "aluminum_profile", "to_node": "aluminum", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "铝合金型材以铝为原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aluminum_plate_aluminum", "from_node": "aluminum_plate", "to_node": "aluminum", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "铝板以铝为原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "coal_sales_coal_mining", "from_node": "coal_sales", "to_node": "coal_mining", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "煤炭销售是煤炭开采的下游环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "electricity_sales_power_generation", "from_node": "electricity_sales", "to_node": "power_generation", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "电力销售是发电的下游环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "towel_home_textile", "from_node": "towel", "to_node": "home_textile", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "毛巾是家用纺织品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "decorative_fabric_home_textile", "from_node": "decorative_fabric", "to_node": "home_textile", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "装饰布是家用纺织品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "bathroom_hardware_sanitary_ware", "from_node": "bathroom_hardware", "to_node": "sanitary_ware", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "卫浴五金是卫生洁具的配套组件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "faucet_sanitary_ware", "from_node": "faucet", "to_node": "sanitary_ware", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "水龙头是卫生洁具的组件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "building_ceramics_building_material", "from_node": "building_ceramics", "to_node": "building_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "建筑陶瓷是建筑材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aluminum_wheel_automotive_part", "from_node": "aluminum_wheel", "to_node": "automotive_part", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "铝合金车轮是汽车零部件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "magnesium_alloy_aluminum", "from_node": "magnesium_alloy", "to_node": "aluminum", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "镁合金与铝合金同属轻合金材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "stamping_part_metal_fabrication", "from_node": "stamping_part", "to_node": "metal_fabrication", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "冲压件是金属加工的产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "marine_product_marine_aquaculture", "from_node": "marine_product", "to_node": "marine_aquaculture", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "海洋产品来自海水养殖", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ceramic_fiber_refractory_product", "from_node": "ceramic_fiber", "to_node": "refractory_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "陶瓷纤维是耐火材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "thermal_insulation_material_refractory_product", "from_node": "thermal_insulation_material", "to_node": "refractory_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "保温材料是耐火材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "crude_oil_transportation_shipping", "from_node": "crude_oil_transportation", "to_node": "shipping", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "原油运输是航运的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "dry_bulk_shipping_shipping", "from_node": "dry_bulk_shipping", "to_node": "shipping", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "干散货运输是航运的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lng_transportation_shipping", "from_node": "lng_transportation", "to_node": "shipping", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "LNG运输是航运的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ship_leasing_shipping", "from_node": "ship_leasing", "to_node": "shipping", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "船舶租赁服务于航运业", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

COMPANIES_123 = [
    {"company_id": "sz_002080", "name_zh": "中材科技", "name_en": "Sinoma Science & Technology Co., Ltd.", "country": "CN", "province": "江苏", "city": "南京市", "stock_codes": ["002080.SZ"], "description": "风电叶片、高压复合气瓶、膜材料制品及锂电池隔膜", "founded_year": 2001, "employee_count": 20964},
    {"company_id": "sz_002081", "name_zh": "金螳螂", "name_en": "Suzhou Gold Mantis Construction Decoration Co., Ltd.", "country": "CN", "province": "江苏", "city": "苏州市", "stock_codes": ["002081.SZ"], "description": "公共建筑装饰工程、幕墙、景观工程", "founded_year": 1993, "employee_count": 10500},
    {"company_id": "sz_002082", "name_zh": "万邦德", "name_en": "Zhejiang Wondel & Century Co., Ltd.", "country": "CN", "province": "浙江", "city": "湖州市", "stock_codes": ["002082.SZ"], "description": "铝型材、铝板材、医药", "founded_year": 1999, "employee_count": 4623},
    {"company_id": "sh_601666", "name_zh": "平煤股份", "name_en": "Pingdingshan Tianan Coal Mining Co., Ltd.", "country": "CN", "province": "河南", "city": "平顶山市", "stock_codes": ["601666.SH"], "description": "煤炭开采、洗选加工、销售", "founded_year": 1998, "employee_count": 43250},
    {"company_id": "sz_002083", "name_zh": "孚日股份", "name_en": "Shandong Vosges Textile Co., Ltd.", "country": "CN", "province": "山东", "city": "潍坊市", "stock_codes": ["002083.SZ"], "description": "毛巾、装饰布等家用纺织品", "founded_year": 1999, "employee_count": 10894},
    {"company_id": "sz_002084", "name_zh": "海鸥住工", "name_en": "Guangzhou Seagull Kitchen and Bath Products Co., Ltd.", "country": "CN", "province": "广东", "city": "广州市", "stock_codes": ["002084.SZ"], "description": "高档水龙头、卫浴五金", "founded_year": 1998, "employee_count": 2650},
    {"company_id": "sz_002085", "name_zh": "万丰奥威", "name_en": "Zhejiang Wanfeng Auto Wheel Co., Ltd.", "country": "CN", "province": "浙江", "city": "新昌县", "stock_codes": ["002085.SZ"], "description": "铝合金车轮、金属表面涂复加工、环保设备", "founded_year": 2001, "employee_count": 11846},
    {"company_id": "sz_002086", "name_zh": "东方海洋", "name_en": "Shandong Oriental Ocean Group Co., Ltd.", "country": "CN", "province": "山东", "city": "烟台市", "stock_codes": ["002086.SZ"], "description": "海水养殖、水产品加工", "founded_year": 2001, "employee_count": 2407},
    {"company_id": "sz_002088", "name_zh": "鲁阳节能", "name_en": "Shandong Luyang Share Co., Ltd.", "country": "CN", "province": "山东", "city": "淄博市", "stock_codes": ["002088.SZ"], "description": "陶瓷纤维、岩棉、节能材料", "founded_year": 1984, "employee_count": 3844},
    {"company_id": "sh_601872", "name_zh": "招商轮船", "name_en": "China Merchants Energy Shipping Co., Ltd.", "country": "CN", "province": "上海", "city": "上海市", "stock_codes": ["601872.SH"], "description": "油轮运输、散货船运输、滚装船运输", "founded_year": 2004, "employee_count": 269},
]

EXPOSURES_123 = [
    {"exposure_id": "sz_002080_produce_wind_turbine_blade", "company_id": "sz_002080", "node_id": "wind_turbine_blade", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:风电叶片")},
    {"exposure_id": "sz_002080_produce_high_pressure_composite_vessel", "company_id": "sz_002080", "node_id": "high_pressure_composite_vessel", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:高压复合气瓶")},
    {"exposure_id": "sz_002080_produce_lithium_battery_separator", "company_id": "sz_002080", "node_id": "lithium_battery_separator", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:锂电池隔膜")},
    {"exposure_id": "sz_002080_produce_membrane_material_product", "company_id": "sz_002080", "node_id": "membrane_material_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:膜材料制品")},
    {"exposure_id": "sz_002080_produce_glass_fiber", "company_id": "sz_002080", "node_id": "glass_fiber", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:玻璃纤维")},
    {"exposure_id": "sz_002080_provide_service_technical_service", "company_id": "sz_002080", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002081_provide_service_public_decoration", "company_id": "sz_002081", "node_id": "public_decoration", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:公共建筑装饰")},
    {"exposure_id": "sz_002081_provide_service_building_curtain_wall", "company_id": "sz_002081", "node_id": "building_curtain_wall", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:建筑幕墙")},
    {"exposure_id": "sz_002081_provide_service_landscape_engineering", "company_id": "sz_002081", "node_id": "landscape_engineering", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:景观工程")},
    {"exposure_id": "sz_002081_provide_service_ancient_building_engineering", "company_id": "sz_002081", "node_id": "ancient_building_engineering", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:古建筑工程")},
    {"exposure_id": "sz_002081_provide_service_fire_protection", "company_id": "sz_002081", "node_id": "fire_protection", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:消防设施安装")},
    {"exposure_id": "sz_002081_provide_service_building_decoration", "company_id": "sz_002081", "node_id": "building_decoration", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建筑装饰")},
    {"exposure_id": "sz_002081_provide_service_technical_service", "company_id": "sz_002081", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002082_produce_aluminum_profile", "company_id": "sz_002082", "node_id": "aluminum_profile", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:铝型材")},
    {"exposure_id": "sz_002082_produce_aluminum_plate", "company_id": "sz_002082", "node_id": "aluminum_plate", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:铝板材")},
    {"exposure_id": "sz_002082_produce_aluminum", "company_id": "sz_002082", "node_id": "aluminum", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:铝合金")},
    {"exposure_id": "sz_002082_produce_pharmaceutical", "company_id": "sz_002082", "node_id": "pharmaceutical", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:化学药")},
    {"exposure_id": "sz_002082_produce_medical_device", "company_id": "sz_002082", "node_id": "medical_device", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:医疗器械")},
    {"exposure_id": "sz_002082_provide_service_technical_service", "company_id": "sz_002082", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sh_601666_operate_coal_mining", "company_id": "sh_601666", "node_id": "coal_mining", "activity_type": "operate", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:煤炭开采")},
    {"exposure_id": "sh_601666_operate_coal_washing", "company_id": "sh_601666", "node_id": "coal_washing", "activity_type": "operate", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:洗选加工")},
    {"exposure_id": "sh_601666_provide_service_coal_sales", "company_id": "sh_601666", "node_id": "coal_sales", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:煤炭销售")},
    {"exposure_id": "sh_601666_operate_power_generation", "company_id": "sh_601666", "node_id": "power_generation", "activity_type": "operate", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发电")},
    {"exposure_id": "sh_601666_provide_service_electricity_sales", "company_id": "sh_601666", "node_id": "electricity_sales", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电力销售")},
    {"exposure_id": "sh_601666_provide_service_technical_service", "company_id": "sh_601666", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002083_produce_towel", "company_id": "sz_002083", "node_id": "towel", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:毛巾")},
    {"exposure_id": "sz_002083_produce_decorative_fabric", "company_id": "sz_002083", "node_id": "decorative_fabric", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:装饰布")},
    {"exposure_id": "sz_002083_produce_home_textile", "company_id": "sz_002083", "node_id": "home_textile", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:家用纺织品")},
    {"exposure_id": "sz_002083_produce_textile", "company_id": "sz_002083", "node_id": "textile", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纺织品生产销售")},
    {"exposure_id": "sz_002083_provide_service_technical_service", "company_id": "sz_002083", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002084_produce_bathroom_hardware", "company_id": "sz_002084", "node_id": "bathroom_hardware", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:高档水龙头")},
    {"exposure_id": "sz_002084_produce_faucet", "company_id": "sz_002084", "node_id": "faucet", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:高档水龙头")},
    {"exposure_id": "sz_002084_produce_sanitary_ware", "company_id": "sz_002084", "node_id": "sanitary_ware", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:卫生陶瓷")},
    {"exposure_id": "sz_002084_produce_building_ceramics", "company_id": "sz_002084", "node_id": "building_ceramics", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建筑陶瓷")},
    {"exposure_id": "sz_002084_provide_service_technical_service", "company_id": "sz_002084", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002085_produce_aluminum_wheel", "company_id": "sz_002085", "node_id": "aluminum_wheel", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:铝合金车轮")},
    {"exposure_id": "sz_002085_provide_service_dacro_coating", "company_id": "sz_002085", "node_id": "dacro_coating", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金属表面涂复加工")},
    {"exposure_id": "sz_002085_produce_magnesium_alloy", "company_id": "sz_002085", "node_id": "magnesium_alloy", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:镁合金")},
    {"exposure_id": "sz_002085_produce_stamping_part", "company_id": "sz_002085", "node_id": "stamping_part", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:冲压件")},
    {"exposure_id": "sz_002085_provide_service_technical_service", "company_id": "sz_002085", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002085_produce_automotive_part", "company_id": "sz_002085", "node_id": "automotive_part", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:汽车零部件")},
    {"exposure_id": "sz_002086_produce_marine_product", "company_id": "sz_002086", "node_id": "marine_product", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:海洋产品")},
    {"exposure_id": "sz_002086_operate_marine_aquaculture", "company_id": "sz_002086", "node_id": "marine_aquaculture", "activity_type": "operate", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:海水养殖")},
    {"exposure_id": "sz_002086_provide_service_food_processing", "company_id": "sz_002086", "node_id": "food_processing", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:食品加工")},
    {"exposure_id": "sz_002086_provide_service_technical_service", "company_id": "sz_002086", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002088_produce_ceramic_fiber", "company_id": "sz_002088", "node_id": "ceramic_fiber", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:陶瓷纤维")},
    {"exposure_id": "sz_002088_produce_refractory_product", "company_id": "sz_002088", "node_id": "refractory_product", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:耐火材料")},
    {"exposure_id": "sz_002088_produce_thermal_insulation_material", "company_id": "sz_002088", "node_id": "thermal_insulation_material", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:保温材料")},
    {"exposure_id": "sz_002088_provide_service_technical_service", "company_id": "sz_002088", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sh_601872_provide_service_crude_oil_transportation", "company_id": "sh_601872", "node_id": "crude_oil_transportation", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:油轮运输")},
    {"exposure_id": "sh_601872_provide_service_dry_bulk_shipping", "company_id": "sh_601872", "node_id": "dry_bulk_shipping", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:散货船运输")},
    {"exposure_id": "sh_601872_provide_service_lng_transportation", "company_id": "sh_601872", "node_id": "lng_transportation", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:LNG运输")},
    {"exposure_id": "sh_601872_provide_service_ship_leasing", "company_id": "sh_601872", "node_id": "ship_leasing", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:船舶租赁")},
    {"exposure_id": "sh_601872_provide_service_shipping", "company_id": "sh_601872", "node_id": "shipping", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:国际船舶运输")},
    {"exposure_id": "sh_601872_provide_service_technical_service", "company_id": "sh_601872", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
]

write_batch(123, NODES_123, EDGES_123, COMPANIES_123, EXPOSURES_123)
print("Batch 123 generated.")
