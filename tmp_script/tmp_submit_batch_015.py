"""
Batch 015 Submission Script
Manually designed industrial graph and company views for 10 companies.
"""
import requests
import json

BASE = "http://localhost:8000/api/v1"

def post_batch(batch):
    r = requests.post(f"{BASE}/batches", json=batch)
    print("batch nodes/edges status:", r.status_code)
    print(r.json())
    return r.status_code == 201

def post_business_batch(batch):
    r = requests.post(f"{BASE}/business-batches", json=batch)
    print("business batch status:", r.status_code)
    print(r.json())
    return r.status_code == 201

# ============================================================
# Step 1: Register new industrial nodes and edges
# ============================================================

nodes = [
    {"node_id": "non_performing_asset_management", "canonical_name_zh": "不良资产管理", "definition": "对银行或企业的不良贷款、不良债权等 distressed assets 进行收购、重组和处置的专业金融服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "diesel_engine", "canonical_name_zh": "柴油机", "definition": "以柴油为燃料的压燃式内燃机，广泛应用于农业机械、工程机械和商用车", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "combine_harvester", "canonical_name_zh": "联合收割机", "definition": "一次性完成收割、脱粒、清选等多个工序的农业收获机械", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "agricultural_transport_vehicle", "canonical_name_zh": "农用运输车", "definition": "用于农业生产资料运输和农产品转运的低速载货汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "agricultural_machinery", "canonical_name_zh": "农业机械", "definition": "用于种植业、畜牧业、渔业和农产品初加工的各种机械设备的总称", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "beef_product", "canonical_name_zh": "牛肉食品", "definition": "以牛肉为主要原料加工制成的各类食品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "automotive_manufacturing", "canonical_name_zh": "汽车制造", "definition": "将汽车零部件组装成整车的生产制造活动及相关服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "industrial_zone_development", "canonical_name_zh": "工业区开发", "definition": "对工业用地进行基础设施建设、厂房建设和招商引资的综合性开发经营活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "recycled_lead", "canonical_name_zh": "再生铅", "definition": "从废旧铅酸蓄电池等含铅废料中回收冶炼得到的铅金属", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "military_power_supply", "canonical_name_zh": "军用电源", "definition": "满足军用标准和环境适应性要求的特种电源变换设备及系统", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "special_alloy_product", "canonical_name_zh": "特种合金制品", "definition": "具有特殊物理化学性能的高端合金材料及其加工制品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "fuel_injection_system", "canonical_name_zh": "燃油喷射系统", "definition": "按精确计量将燃油喷入发动机燃烧室的系统总成，包括高压油泵、喷油器和电控单元", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "exhaust_aftertreatment_system", "canonical_name_zh": "尾气后处理系统", "definition": "安装在发动机排气系统中用于降低尾气污染物排放的装置总成，包括催化转化器和颗粒捕集器", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "intake_system", "canonical_name_zh": "进气系统", "definition": "为发动机提供过滤后空气的子系统，包括空气滤清器、进气管路和涡轮增压器", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "shipping_agency_service", "canonical_name_zh": "船舶代理服务", "definition": "为船舶进出港提供报关、补给、船员服务和单证代理的中介服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "stevedoring_service", "canonical_name_zh": "装卸堆存服务", "definition": "在港口码头为船舶和车辆提供货物装卸、搬运和堆场存储的服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_engine_to_harvester", "from_node": "diesel_engine", "to_node": "combine_harvester", "edge_type": "composition", "description": "柴油机是联合收割机的动力核心"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_engine_to_agri_transport", "from_node": "diesel_engine", "to_node": "agricultural_transport_vehicle", "edge_type": "composition", "description": "柴油机是农用运输车的动力核心"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_harvester_to_agri_mach", "from_node": "combine_harvester", "to_node": "agricultural_machinery", "edge_type": "composition", "description": "联合收割机是农业机械的重要组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_agri_transport_to_agri_mach", "from_node": "agricultural_transport_vehicle", "to_node": "agricultural_machinery", "edge_type": "composition", "description": "农用运输车是农业机械的重要组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_beef_to_food_ingredient", "from_node": "beef_product", "to_node": "food_ingredient", "edge_type": "material_flow", "description": "牛肉食品可作为餐饮业和食品工业的原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_auto_manufacturing_to_vehicle", "from_node": "automotive_manufacturing", "to_node": "road_transport_vehicle", "edge_type": "service_flow", "description": "汽车制造活动产出公路运输车辆"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_recycled_lead_to_lead_metal", "from_node": "recycled_lead", "to_node": "lead_zinc_metal", "edge_type": "material_flow", "description": "再生铅经冶炼后成为铅金属产品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ht_alloy_to_special_alloy", "from_node": "high_temperature_alloy", "to_node": "special_alloy_product", "edge_type": "material_flow", "description": "高温合金是特种合金制品的基础材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_fuel_injection_to_engine", "from_node": "fuel_injection_system", "to_node": "automotive_engine", "edge_type": "composition", "description": "燃油喷射系统是汽车发动机的核心子系统"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_exhaust_to_engine", "from_node": "exhaust_aftertreatment_system", "to_node": "automotive_engine", "edge_type": "composition", "description": "尾气后处理系统是汽车发动机的排放控制子系统"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_intake_to_engine", "from_node": "intake_system", "to_node": "automotive_engine", "edge_type": "composition", "description": "进气系统是汽车发动机的供气子系统"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_to_injection", "from_node": "diesel", "to_node": "fuel_injection_system", "edge_type": "material_flow", "description": "柴油是燃油喷射系统的工质"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_stevedoring_to_port", "from_node": "stevedoring_service", "to_node": "port_operation_service", "edge_type": "service_flow", "description": "装卸堆存服务是港口运营的核心业务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_shipping_agency_to_port", "from_node": "shipping_agency_service", "to_node": "port_operation_service", "edge_type": "service_flow", "description": "船舶代理服务是港口运营的配套业务"},
]

graph_batch = {
    "batch_id": "batch_015_graph",
    "task_description": "Batch 015 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 015 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "hainan_ha_pharmaceutical", "name_zh": "海南海药", "aliases": ["海南海药股份有限公司"], "stock_codes": ["000566.SZ"], "country": "CN", "province": "海南", "city": "海口市", "employee_count": 2003, "company_type": "public", "description": "化学制药企业，主营新特药、抗生素类普药及中药产品"},
    {"company_id": "haide_capital", "name_zh": "海德股份", "aliases": ["海南海德资本管理股份有限公司"], "stock_codes": ["000567.SZ"], "country": "CN", "province": "海南", "city": "海口市", "employee_count": 146, "company_type": "public", "description": "不良资产管理企业，主营不良资产收购、重组和处置"},
    {"company_id": "luzhou_laojiao", "name_zh": "泸州老窖", "aliases": ["泸州老窖股份有限公司"], "stock_codes": ["000568.SZ"], "country": "CN", "province": "四川", "city": "泸州市", "employee_count": 3832, "company_type": "public", "description": "白酒酿造企业，主营泸州老窖系列酒"},
    {"company_id": "suchangchai", "name_zh": "苏常柴A", "aliases": ["常柴股份有限公司"], "stock_codes": ["000570.SZ"], "country": "CN", "province": "江苏", "city": "常州市", "employee_count": 2421, "company_type": "public", "description": "农用机械制造企业，主营柴油机、联合收割机和农用运输车"},
    {"company_id": "new_continent", "name_zh": "新大洲A", "aliases": ["新大洲控股股份有限公司"], "stock_codes": ["000571.SZ"], "country": "CN", "province": "海南", "city": "海口市", "employee_count": 2237, "company_type": "public", "description": "综合企业，主营牛肉食品加工、煤炭开采及物流产业"},
    {"company_id": "haima_automotive", "name_zh": "海马汽车", "aliases": ["海马汽车股份有限公司"], "stock_codes": ["000572.SZ"], "country": "CN", "province": "海南", "city": "海口市", "employee_count": 2230, "company_type": "public", "description": "汽车整车制造企业，主营乘用车制造及销售服务"},
    {"company_id": "yuehongyuan", "name_zh": "粤宏远A", "aliases": ["东莞宏远工业区股份有限公司"], "stock_codes": ["000573.SZ"], "country": "CN", "province": "广东", "city": "东莞市", "employee_count": 145, "company_type": "public", "description": "综合企业，主营房地产和工业区开发、原煤开采及再生铅业务"},
    {"company_id": "ganhua_tech", "name_zh": "甘化科工", "aliases": ["广东甘化科工股份有限公司"], "stock_codes": ["000576.SZ"], "country": "CN", "province": "广东", "city": "江门市", "employee_count": 436, "company_type": "public", "description": "军工企业，主营电源及相关产品、高性能特种合金材料制品"},
    {"company_id": "weifu_high_tech", "name_zh": "威孚高科", "aliases": ["无锡威孚高科技集团股份有限公司"], "stock_codes": ["000581.SZ"], "country": "CN", "province": "江苏", "city": "无锡市", "employee_count": 5861, "company_type": "public", "description": "汽车零部件制造企业，主营柴油燃油喷射系统、汽车尾气后处理系统和进气系统产品"},
    {"company_id": "beibuwan_port", "name_zh": "北部湾港", "aliases": ["北部湾港股份有限公司"], "stock_codes": ["000582.SZ"], "country": "CN", "province": "广西", "city": "北海市", "employee_count": 8640, "company_type": "public", "description": "港口运营企业，主营装卸堆存、外轮代理和海运服务"},
]

exposures = [
    {"exposure_id": "hainan_ha_manufacture_pharma", "company_id": "hainan_ha_pharmaceutical", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "药品制造商", "weight": 0.8},
    {"exposure_id": "hainan_ha_manufacture_biological", "company_id": "hainan_ha_pharmaceutical", "node_id": "biological_drug", "activity_type": "manufacture", "role": "新特药制造商", "weight": 0.6},
    {"exposure_id": "hainan_ha_manufacture_chemical", "company_id": "hainan_ha_pharmaceutical", "node_id": "chemical_drug", "activity_type": "manufacture", "role": "抗生素类产品制造商", "weight": 0.5},
    {"exposure_id": "hainan_ha_manufacture_tcm", "company_id": "hainan_ha_pharmaceutical", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中药产品制造商", "weight": 0.4},
    {"exposure_id": "haide_operate_npa_mgmt", "company_id": "haide_capital", "node_id": "non_performing_asset_management", "activity_type": "operate", "role": "不良资产管理服务商", "weight": 1.0},
    {"exposure_id": "luzhou_manufacture_liquor", "company_id": "luzhou_laojiao", "node_id": "liquor", "activity_type": "manufacture", "role": "白酒酿造商", "weight": 1.0},
    {"exposure_id": "suchangchai_manufacture_diesel_engine", "company_id": "suchangchai", "node_id": "diesel_engine", "activity_type": "manufacture", "role": "柴油机制造商", "weight": 0.9},
    {"exposure_id": "suchangchai_manufacture_harvester", "company_id": "suchangchai", "node_id": "combine_harvester", "activity_type": "manufacture", "role": "联合收割机制造商", "weight": 0.5},
    {"exposure_id": "suchangchai_manufacture_agri_transport", "company_id": "suchangchai", "node_id": "agricultural_transport_vehicle", "activity_type": "manufacture", "role": "农用运输车制造商", "weight": 0.4},
    {"exposure_id": "suchangchai_manufacture_agri_mach", "company_id": "suchangchai", "node_id": "agricultural_machinery", "activity_type": "manufacture", "role": "农业机械制造商", "weight": 0.8},
    {"exposure_id": "new_continent_manufacture_beef", "company_id": "new_continent", "node_id": "beef_product", "activity_type": "manufacture", "role": "牛肉食品生产商", "weight": 0.5},
    {"exposure_id": "new_continent_produce_coal", "company_id": "new_continent", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.6},
    {"exposure_id": "new_continent_operate_logistics", "company_id": "new_continent", "node_id": "logistics_service", "activity_type": "operate", "role": "物流服务商", "weight": 0.5},
    {"exposure_id": "haima_manufacture_auto", "company_id": "haima_automotive", "node_id": "automotive_manufacturing", "activity_type": "manufacture", "role": "汽车整车制造商", "weight": 0.9},
    {"exposure_id": "haima_manufacture_vehicle", "company_id": "haima_automotive", "node_id": "road_transport_vehicle", "activity_type": "manufacture", "role": "乘用车制造商", "weight": 0.8},
    {"exposure_id": "haima_operate_sales", "company_id": "haima_automotive", "node_id": "automotive_sales_service", "activity_type": "operate", "role": "汽车销售服务商", "weight": 0.6},
    {"exposure_id": "yuehongyuan_operate_real_estate", "company_id": "yuehongyuan", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.6},
    {"exposure_id": "yuehongyuan_operate_industrial_zone", "company_id": "yuehongyuan", "node_id": "industrial_zone_development", "activity_type": "operate", "role": "工业区开发商", "weight": 0.4},
    {"exposure_id": "yuehongyuan_produce_coal", "company_id": "yuehongyuan", "node_id": "coal", "activity_type": "produce", "role": "原煤生产商", "weight": 0.5},
    {"exposure_id": "yuehongyuan_manufacture_recycled_lead", "company_id": "yuehongyuan", "node_id": "recycled_lead", "activity_type": "manufacture", "role": "再生铅制造商", "weight": 0.4},
    {"exposure_id": "ganhua_manufacture_power_supply", "company_id": "ganhua_tech", "node_id": "power_supply_system", "activity_type": "manufacture", "role": "电源系统制造商", "weight": 0.7},
    {"exposure_id": "ganhua_manufacture_military_power", "company_id": "ganhua_tech", "node_id": "military_power_supply", "activity_type": "manufacture", "role": "军用电源制造商", "weight": 0.6},
    {"exposure_id": "ganhua_manufacture_special_alloy", "company_id": "ganhua_tech", "node_id": "special_alloy_product", "activity_type": "manufacture", "role": "特种合金制品制造商", "weight": 0.6},
    {"exposure_id": "weifu_manufacture_fuel_injection", "company_id": "weifu_high_tech", "node_id": "fuel_injection_system", "activity_type": "manufacture", "role": "燃油喷射系统制造商", "weight": 0.9},
    {"exposure_id": "weifu_manufacture_exhaust_aftertreatment", "company_id": "weifu_high_tech", "node_id": "exhaust_aftertreatment_system", "activity_type": "manufacture", "role": "尾气后处理系统制造商", "weight": 0.8},
    {"exposure_id": "weifu_manufacture_intake", "company_id": "weifu_high_tech", "node_id": "intake_system", "activity_type": "manufacture", "role": "进气系统制造商", "weight": 0.7},
    {"exposure_id": "beibuwan_operate_port", "company_id": "beibuwan_port", "node_id": "port_operation_service", "activity_type": "operate", "role": "港口运营商", "weight": 0.9},
    {"exposure_id": "beibuwan_operate_shipping", "company_id": "beibuwan_port", "node_id": "shipping_service", "activity_type": "operate", "role": "海运服务商", "weight": 0.6},
    {"exposure_id": "beibuwan_operate_stevedoring", "company_id": "beibuwan_port", "node_id": "stevedoring_service", "activity_type": "operate", "role": "装卸堆存服务商", "weight": 0.8},
    {"exposure_id": "beibuwan_operate_shipping_agency", "company_id": "beibuwan_port", "node_id": "shipping_agency_service", "activity_type": "operate", "role": "外轮代理服务商", "weight": 0.5},
    {"exposure_id": "beibuwan_operate_container_handling", "company_id": "beibuwan_port", "node_id": "container_handling_service", "activity_type": "operate", "role": "集装箱装卸服务商", "weight": 0.6},
]

business_batch = {
    "batch_id": "batch_015_business",
    "task_description": "Batch 015 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 015 ===")
post_business_batch(business_batch)
