"""
Batch 012 Submission Script
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
    {"node_id": "refrigeration_equipment", "canonical_name_zh": "制冷设备", "definition": "用于制冷制热的机械设备及配套系统，包括压缩机、换热器、阀门等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "valve", "canonical_name_zh": "阀门", "definition": "控制流体通断、流量和方向的管道附件，广泛应用于制冷、化工、能源系统", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "refrigeration_engineering_service", "canonical_name_zh": "制冷工程服务", "definition": "提供制冷空调系统工程的设计、施工、安装、调试及维护保养服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "power_plant_operation", "canonical_name_zh": "电厂运营", "definition": "电力生产设施的投资建设、运行管理和电力销售业务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "remote_education_service", "canonical_name_zh": "远程教育服务", "definition": "基于网络和信息技术的异地教育培训服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "network_engineering_service", "canonical_name_zh": "网络工程服务", "definition": "计算机网络系统的规划、设计、施工和运维服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "transformer", "canonical_name_zh": "变压器", "definition": "利用电磁感应原理改变交流电压的电气设备，电力系统的核心设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "reactor", "canonical_name_zh": "电抗器", "definition": "电力系统中用于限制短路电流、滤波和无功补偿的感性元件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "switchgear", "canonical_name_zh": "开关柜", "definition": "电力系统中用于电能分配、控制和保护的成套开关设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "packaged_substation", "canonical_name_zh": "预装式变电站", "definition": "将高压开关设备、变压器和低压配电设备预先组装在封闭箱体内的成套配电装置", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "microecological_preparation", "canonical_name_zh": "微生态制剂", "definition": "含有益生菌或其代谢产物的制剂，用于调节人体或动物微生态平衡", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "high_temperature_alloy", "canonical_name_zh": "高温合金", "definition": "以铁、镍、钴为基，能在600℃以上高温及一定应力条件下长期工作的金属材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "renewable_energy_power_generation", "canonical_name_zh": "可再生能源发电", "definition": "利用风能、太阳能等可再生能源进行电力生产的运营服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "lighting_fixture", "canonical_name_zh": "照明灯具", "definition": "用于人工照明的电光源及配套灯具产品", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "led_lighting", "canonical_name_zh": "LED照明", "definition": "采用发光二极管作为光源的节能照明产品", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_compressor_to_ref_equip", "from_node": "refrigeration_compressor", "to_node": "refrigeration_equipment", "edge_type": "composition", "description": "制冷压缩机是制冷设备的核心组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_valve_to_ref_equip", "from_node": "valve", "to_node": "refrigeration_equipment", "edge_type": "composition", "description": "阀门是制冷设备的管路控制组件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ref_equip_to_ref_eng", "from_node": "refrigeration_equipment", "to_node": "refrigeration_engineering_service", "edge_type": "capability_supply", "description": "制冷设备支撑制冷工程服务的实施"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_coal_to_plant_op", "from_node": "coal_power_generation", "to_node": "power_plant_operation", "edge_type": "service_flow", "description": "燃煤发电是电厂运营的核心业务形式"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_gas_to_plant_op", "from_node": "gas_power_generation", "to_node": "power_plant_operation", "edge_type": "service_flow", "description": "燃气发电是电厂运营的业务形式之一"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_plant_op_to_elec", "from_node": "power_plant_operation", "to_node": "electricity_power", "edge_type": "service_flow", "description": "电厂运营产生电力供应"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_remote_edu_to_edu", "from_node": "remote_education_service", "to_node": "education_service", "edge_type": "service_flow", "description": "远程教育是教育服务的一种形式"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_transformer_to_dist", "from_node": "transformer", "to_node": "power_distribution_equipment", "edge_type": "composition", "description": "变压器是配电设备的核心组成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_reactor_to_dist", "from_node": "reactor", "to_node": "power_distribution_equipment", "edge_type": "composition", "description": "电抗器是配电设备的组成元件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_switchgear_to_dist", "from_node": "switchgear", "to_node": "power_distribution_equipment", "edge_type": "composition", "description": "开关柜是配电设备的成套组件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pkg_sub_to_dist", "from_node": "packaged_substation", "to_node": "power_distribution_equipment", "edge_type": "composition", "description": "预装式变电站是一种集成化配电设备"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_renew_to_solar", "from_node": "renewable_energy_power_generation", "to_node": "solar_power_generation", "edge_type": "service_flow", "description": "可再生能源发电运营包含太阳能发电"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_renew_to_wind", "from_node": "renewable_energy_power_generation", "to_node": "wind_power_generation", "edge_type": "service_flow", "description": "可再生能源发电运营包含风力发电"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_solar_to_elec", "from_node": "solar_power_generation", "to_node": "electricity_power", "edge_type": "energy_flow", "description": "太阳能发电产生电力"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_wind_to_elec", "from_node": "wind_power_generation", "to_node": "electricity_power", "edge_type": "energy_flow", "description": "风力发电产生电力"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_led_to_fixture", "from_node": "led_lighting", "to_node": "lighting_fixture", "edge_type": "composition", "description": "LED光源是照明灯具的核心发光组件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_semi_to_led", "from_node": "semiconductor_device", "to_node": "led_lighting", "edge_type": "composition", "description": "半导体器件是LED照明产品的核心组成"},
]

graph_batch = {
    "batch_id": "batch_012_graph",
    "task_description": "Batch 012 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 012 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "bingshan_refrigeration", "name_zh": "冰山冷热", "aliases": ["冰山冷热科技股份有限公司"], "stock_codes": ["000530.SZ"], "country": "CN", "province": "辽宁", "city": "大连市", "employee_count": 4229, "company_type": "public", "description": "制冷设备及配套辅机、阀门、配件制造商，提供制冷工程服务"},
    {"company_id": "suihengyun", "name_zh": "穗恒运A", "aliases": ["广州恒运企业集团股份有限公司"], "stock_codes": ["000531.SZ"], "country": "CN", "province": "广东", "city": "广州市", "employee_count": 1067, "company_type": "public", "description": "电力及热力生产销售企业"},
    {"company_id": "huajin_capital", "name_zh": "华金资本", "aliases": ["珠海华金资本股份有限公司"], "stock_codes": ["000532.SZ"], "country": "CN", "province": "广东", "city": "珠海市", "employee_count": 417, "company_type": "public", "description": "多元金融投资企业，业务涵盖电子器件销售、远程教育、网络工程、IT代理及污水处理"},
    {"company_id": "shunna", "name_zh": "顺钠股份", "aliases": ["广东顺钠电气股份有限公司"], "stock_codes": ["000533.SZ"], "country": "CN", "province": "广东", "city": "佛山市", "employee_count": 1472, "company_type": "public", "description": "电气设备制造企业，主要产品包括变压器、电抗器、开关柜和预装式变电站"},
    {"company_id": "wanze", "name_zh": "万泽股份", "aliases": ["万泽实业股份有限公司"], "stock_codes": ["000534.SZ"], "country": "CN", "province": "广东", "city": "汕头市", "employee_count": 1397, "company_type": "public", "description": "微生态制剂和高温合金研发制造企业"},
    {"company_id": "huaying_tech", "name_zh": "华映科技", "aliases": ["华映科技(集团)股份有限公司"], "stock_codes": ["000536.SZ"], "country": "CN", "province": "福建", "city": "福州市", "employee_count": 1694, "company_type": "public", "description": "液晶模组及OLED显示屏制造企业"},
    {"company_id": "lufa_power", "name_zh": "绿发电力", "aliases": ["天津绿发电力集团股份有限公司", "广宇发展"], "stock_codes": ["000537.SZ"], "country": "CN", "province": "天津", "city": "天津市", "employee_count": 1224, "company_type": "public", "description": "风能和太阳能发电投资开发运营企业"},
    {"company_id": "yunnan_baiyao", "name_zh": "云南白药", "aliases": ["云南白药集团股份有限公司"], "stock_codes": ["000538.SZ"], "country": "CN", "province": "云南", "city": "昆明市", "employee_count": 9286, "company_type": "public", "description": "中成药及药品生产经营企业，知名中药品牌"},
    {"company_id": "yuedianli", "name_zh": "粤电力A", "aliases": ["广东电力发展股份有限公司"], "stock_codes": ["000539.SZ"], "country": "CN", "province": "广东", "city": "广州市", "employee_count": 10497, "company_type": "public", "description": "电力项目投资建设和经营管理企业，主营电力生产销售"},
    {"company_id": "foshan_lighting", "name_zh": "佛山照明", "aliases": ["佛山电器照明股份有限公司"], "stock_codes": ["000541.SZ"], "country": "CN", "province": "广东", "city": "佛山市", "employee_count": 12201, "company_type": "public", "description": "电光源及绿色节能照明产品研发制造企业"},
]

exposures = [
    {"exposure_id": "bingshan_refrigeration_manufacture_refrigeration_equipment", "company_id": "bingshan_refrigeration", "node_id": "refrigeration_equipment", "activity_type": "manufacture", "role": "制冷设备制造商", "weight": 0.9},
    {"exposure_id": "bingshan_refrigeration_manufacture_compressor", "company_id": "bingshan_refrigeration", "node_id": "refrigeration_compressor", "activity_type": "manufacture", "role": "制冷压缩机制造商", "weight": 0.7},
    {"exposure_id": "bingshan_refrigeration_manufacture_valve", "company_id": "bingshan_refrigeration", "node_id": "valve", "activity_type": "manufacture", "role": "阀门制造商", "weight": 0.4},
    {"exposure_id": "bingshan_refrigeration_provide_ref_eng", "company_id": "bingshan_refrigeration", "node_id": "refrigeration_engineering_service", "activity_type": "provide_service", "role": "制冷工程服务商", "weight": 0.5},
    {"exposure_id": "suihengyun_produce_electricity", "company_id": "suihengyun", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9},
    {"exposure_id": "suihengyun_produce_heat", "company_id": "suihengyun", "node_id": "heating_supply", "activity_type": "produce", "role": "热力生产商", "weight": 0.7},
    {"exposure_id": "suihengyun_operate_power_plant", "company_id": "suihengyun", "node_id": "power_plant_operation", "activity_type": "operate", "role": "电厂运营商", "weight": 0.9},
    {"exposure_id": "huajin_capital_operate_elec_dist", "company_id": "huajin_capital", "node_id": "electronic_component_distribution_service", "activity_type": "operate", "role": "电子器件分销商", "weight": 0.4},
    {"exposure_id": "huajin_capital_provide_education", "company_id": "huajin_capital", "node_id": "education_service", "activity_type": "provide_service", "role": "远程教育服务商", "weight": 0.3},
    {"exposure_id": "huajin_capital_provide_network_eng", "company_id": "huajin_capital", "node_id": "network_engineering_service", "activity_type": "provide_service", "role": "网络工程服务商", "weight": 0.3},
    {"exposure_id": "huajin_capital_operate_it_dist", "company_id": "huajin_capital", "node_id": "it_distribution_service", "activity_type": "operate", "role": "IT产品代理商", "weight": 0.3},
    {"exposure_id": "huajin_capital_operate_wastewater", "company_id": "huajin_capital", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.3},
    {"exposure_id": "shunna_manufacture_transformer", "company_id": "shunna", "node_id": "transformer", "activity_type": "manufacture", "role": "变压器制造商", "weight": 0.9},
    {"exposure_id": "shunna_manufacture_reactor", "company_id": "shunna", "node_id": "reactor", "activity_type": "manufacture", "role": "电抗器制造商", "weight": 0.6},
    {"exposure_id": "shunna_manufacture_switchgear", "company_id": "shunna", "node_id": "switchgear", "activity_type": "manufacture", "role": "开关柜制造商", "weight": 0.7},
    {"exposure_id": "shunna_manufacture_pkg_sub", "company_id": "shunna", "node_id": "packaged_substation", "activity_type": "manufacture", "role": "预装式变电站制造商", "weight": 0.6},
    {"exposure_id": "wanze_manufacture_microeco", "company_id": "wanze", "node_id": "microecological_preparation", "activity_type": "manufacture", "role": "微生态制剂制造商", "weight": 0.7},
    {"exposure_id": "wanze_manufacture_ht_alloy", "company_id": "wanze", "node_id": "high_temperature_alloy", "activity_type": "manufacture", "role": "高温合金制造商", "weight": 0.7},
    {"exposure_id": "huaying_tech_manufacture_display_module", "company_id": "huaying_tech", "node_id": "display_module", "activity_type": "manufacture", "role": "液晶模组制造商", "weight": 0.9},
    {"exposure_id": "huaying_tech_manufacture_lcd_panel", "company_id": "huaying_tech", "node_id": "lcd_panel", "activity_type": "manufacture", "role": "液晶面板制造商", "weight": 0.7},
    {"exposure_id": "huaying_tech_manufacture_oled_panel", "company_id": "huaying_tech", "node_id": "oled_panel", "activity_type": "manufacture", "role": "OLED面板制造商", "weight": 0.5},
    {"exposure_id": "lufa_power_operate_solar", "company_id": "lufa_power", "node_id": "solar_power_generation", "activity_type": "operate", "role": "太阳能发电运营商", "weight": 0.8},
    {"exposure_id": "lufa_power_operate_wind", "company_id": "lufa_power", "node_id": "wind_power_generation", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.8},
    {"exposure_id": "lufa_power_produce_electricity", "company_id": "lufa_power", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9},
    {"exposure_id": "lufa_power_operate_renewable", "company_id": "lufa_power", "node_id": "renewable_energy_power_generation", "activity_type": "operate", "role": "可再生能源发电运营商", "weight": 0.9},
    {"exposure_id": "yunnan_baiyao_manufacture_tcm", "company_id": "yunnan_baiyao", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中成药制造商", "weight": 0.9},
    {"exposure_id": "yunnan_baiyao_manufacture_pharma", "company_id": "yunnan_baiyao", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "药品制造商", "weight": 0.8},
    {"exposure_id": "yunnan_baiyao_operate_pharma_dist", "company_id": "yunnan_baiyao", "node_id": "pharmaceutical_distribution", "activity_type": "operate", "role": "医药分销商", "weight": 0.5},
    {"exposure_id": "yunnan_baiyao_operate_pharma_retail", "company_id": "yunnan_baiyao", "node_id": "pharmaceutical_retail", "activity_type": "operate", "role": "医药零售商", "weight": 0.4},
    {"exposure_id": "yuedianli_produce_electricity", "company_id": "yuedianli", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9},
    {"exposure_id": "yuedianli_operate_coal_power", "company_id": "yuedianli", "node_id": "coal_power_generation", "activity_type": "operate", "role": "燃煤发电运营商", "weight": 0.7},
    {"exposure_id": "yuedianli_operate_gas_power", "company_id": "yuedianli", "node_id": "gas_power_generation", "activity_type": "operate", "role": "燃气发电运营商", "weight": 0.5},
    {"exposure_id": "foshan_lighting_manufacture_fixture", "company_id": "foshan_lighting", "node_id": "lighting_fixture", "activity_type": "manufacture", "role": "照明灯具制造商", "weight": 0.9},
    {"exposure_id": "foshan_lighting_manufacture_led", "company_id": "foshan_lighting", "node_id": "led_lighting", "activity_type": "manufacture", "role": "LED照明产品制造商", "weight": 0.8},
    {"exposure_id": "foshan_lighting_manufacture_led_display", "company_id": "foshan_lighting", "node_id": "led_display_screen", "activity_type": "manufacture", "role": "LED显示屏制造商", "weight": 0.3},
]

business_batch = {
    "batch_id": "batch_012_business",
    "task_description": "Batch 012 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 012 ===")
post_business_batch(business_batch)
