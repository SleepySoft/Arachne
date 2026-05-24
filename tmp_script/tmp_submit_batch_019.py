"""
Batch 019 Submission Script
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
    {"node_id": "energy_storage_service", "canonical_name_zh": "储能服务", "definition": "通过储能设备实现电能存储和释放的能源调节服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "daily_necessities", "canonical_name_zh": "日用百货", "definition": "日常生活中使用的各类轻工业消费品，包括纺织品、塑料制品和五金用品等", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "electromechanical_product", "canonical_name_zh": "机电产品", "definition": "机械和电气设备及其零部件的统称，广泛应用于工业和民用领域", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "nickel_based_alloy", "canonical_name_zh": "镍基合金", "definition": "以镍为基体元素并含有铬、钼等合金元素的高温耐腐蚀合金材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pvc", "canonical_name_zh": "聚氯乙烯", "definition": "由氯乙烯单体聚合而成的通用塑料，广泛用于管材、型材和薄膜", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "calcium_carbide", "canonical_name_zh": "电石", "definition": "碳化钙的俗称，是重要的基本化工原料，用于生产乙炔和PVC", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "dicyandiamide", "canonical_name_zh": "双氰胺", "definition": "由电石制得的氰胺二聚物，用于生产化肥、医药中间体和环氧树脂固化剂", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "ceramic_capacitor", "canonical_name_zh": "陶瓷电容器", "definition": "以陶瓷为介质的电容器，具有高频特性好、温度稳定性高的特点", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "chip_resistor", "canonical_name_zh": "片式电阻器", "definition": "表面贴装型的微型电阻元件，用于限制电流和分压", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "lithium_battery_cell", "canonical_name_zh": "锂离子电池电芯", "definition": "由正极、负极、隔膜和电解液组成的可充电电化学储能单元", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "polypropylene", "canonical_name_zh": "聚丙烯", "definition": "由丙烯聚合而成的热塑性树脂，广泛用于注塑、纤维和薄膜", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "salt_product", "canonical_name_zh": "盐产品", "definition": "以氯化钠为主要成分的矿物产品，包括工业盐和食用盐", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_storage_to_elec", "from_node": "energy_storage_service", "to_node": "electricity_power", "edge_type": "capability_supply", "description": "储能服务支撑电力系统的稳定供应"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_nickel_to_ht_alloy", "from_node": "nickel_based_alloy", "to_node": "high_temperature_alloy", "edge_type": "composition", "description": "镍基合金是高温合金的重要品类"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_carbide_to_pvc", "from_node": "calcium_carbide", "to_node": "pvc", "edge_type": "material_flow", "description": "电石是生产PVC的基础原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_carbide_to_dicyandiamide", "from_node": "calcium_carbide", "to_node": "dicyandiamide", "edge_type": "material_flow", "description": "电石是生产双氰胺的原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ceramic_cap_to_pcb", "from_node": "ceramic_capacitor", "to_node": "pcb_board", "edge_type": "composition", "description": "陶瓷电容器是印制电路板的表面贴装元件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_chip_resistor_to_pcb", "from_node": "chip_resistor", "to_node": "pcb_board", "edge_type": "composition", "description": "片式电阻器是印制电路板的表面贴装元件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_battery_cell_to_ion", "from_node": "lithium_battery_cell", "to_node": "lithium_ion_cell", "edge_type": "composition", "description": "锂离子电池电芯是锂离子电池的组成单元"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_petro_to_pp", "from_node": "petrochemical_product", "to_node": "polypropylene", "edge_type": "material_flow", "description": "石化产品经聚合反应制成聚丙烯"},
]

graph_batch = {
    "batch_id": "batch_019_graph",
    "task_description": "Batch 019 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 019 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "shunfa_hengneng", "name_zh": "顺发恒能", "aliases": ["顺发恒能股份公司"], "stock_codes": ["000631.SZ"], "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 653, "company_type": "public", "description": "综合企业，主营房地产开发与新能源业务"},
    {"company_id": "st_sanmu", "name_zh": "ST三木", "aliases": ["福建三木集团股份有限公司"], "stock_codes": ["000632.SZ"], "country": "CN", "province": "福建", "city": "福州市", "employee_count": 496, "company_type": "public", "description": "综合企业，主营房地产开发、施工工程、日用百货和食品加工"},
    {"company_id": "hejin_investment", "name_zh": "合金投资", "aliases": ["新疆合金投资股份有限公司"], "stock_codes": ["000633.SZ"], "country": "CN", "province": "新疆", "city": "昌吉回族自治州", "employee_count": 194, "company_type": "public", "description": "新材料企业，主营镍基合金材料的生产销售"},
    {"company_id": "yinglite", "name_zh": "英力特", "aliases": ["宁夏英力特化工股份有限公司"], "stock_codes": ["000635.SZ"], "country": "CN", "province": "宁夏", "city": "石嘴山市", "employee_count": 1815, "company_type": "public", "description": "化工企业，主营PVC、电石和双氰胺"},
    {"company_id": "fenghua_high_tech", "name_zh": "风华高科", "aliases": ["广东风华高新科技股份有限公司"], "stock_codes": ["000636.SZ"], "country": "CN", "province": "广东", "city": "肇庆市", "employee_count": 8716, "company_type": "public", "description": "电子元器件企业，主营陶瓷电容器、片式电阻器和锂离子电池电芯"},
    {"company_id": "maohua_shihua", "name_zh": "茂化实华", "aliases": ["茂名石化实华股份有限公司"], "stock_codes": ["000637.SZ"], "country": "CN", "province": "广东", "city": "茂名市", "employee_count": 903, "company_type": "public", "description": "石化企业，主营聚丙烯、液化气和盐产品"},
    {"company_id": "st_wanfang", "name_zh": "*ST万方", "aliases": ["万方城镇投资发展股份有限公司"], "stock_codes": ["000638.SZ"], "country": "CN", "province": "吉林", "city": "白山市", "employee_count": 157, "company_type": "public", "description": "房地产开发企业"},
    {"company_id": "st_xiwang", "name_zh": "ST西王", "aliases": ["西王食品股份有限公司"], "stock_codes": ["000639.SZ"], "country": "CN", "province": "山东", "city": "滨州市", "employee_count": 1602, "company_type": "public", "description": "食品企业，主营健康食用油及运动营养产品"},
    {"company_id": "renhe_pharmaceutical", "name_zh": "仁和药业", "aliases": ["仁和药业股份有限公司"], "stock_codes": ["000650.SZ"], "country": "CN", "province": "江西", "city": "宜春市", "employee_count": 5394, "company_type": "public", "description": "医药企业，主营仁和可立克、优卡丹、妇炎洁等知名药品"},
    {"company_id": "gree_electric", "name_zh": "格力电器", "aliases": ["珠海格力电器股份有限公司"], "stock_codes": ["000651.SZ"], "country": "CN", "province": "广东", "city": "珠海市", "employee_count": 72808, "company_type": "public", "description": "家电龙头企业，主营空调等家用电器产品"},
]

exposures = [
    {"exposure_id": "shunfa_operate_real_estate", "company_id": "shunfa_hengneng", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.7},
    {"exposure_id": "shunfa_operate_solar", "company_id": "shunfa_hengneng", "node_id": "solar_power_generation", "activity_type": "operate", "role": "太阳能发电运营商", "weight": 0.5},
    {"exposure_id": "shunfa_operate_wind", "company_id": "shunfa_hengneng", "node_id": "wind_power_generation", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.3},
    {"exposure_id": "shunfa_produce_elec", "company_id": "shunfa_hengneng", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.5},
    {"exposure_id": "shunfa_operate_storage", "company_id": "shunfa_hengneng", "node_id": "energy_storage_service", "activity_type": "operate", "role": "储能服务商", "weight": 0.4},
    {"exposure_id": "st_sanmu_operate_real_estate", "company_id": "st_sanmu", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.7},
    {"exposure_id": "st_sanmu_operate_construction", "company_id": "st_sanmu", "node_id": "construction_service", "activity_type": "operate", "role": "工程施工服务商", "weight": 0.5},
    {"exposure_id": "st_sanmu_operate_dept_store", "company_id": "st_sanmu", "node_id": "department_store", "activity_type": "operate", "role": "百货零售商", "weight": 0.3},
    {"exposure_id": "st_sanmu_operate_daily", "company_id": "st_sanmu", "node_id": "daily_necessities", "activity_type": "operate", "role": "日用百货销售商", "weight": 0.3},
    {"exposure_id": "st_sanmu_operate_food", "company_id": "st_sanmu", "node_id": "food_ingredient", "activity_type": "operate", "role": "食品销售商", "weight": 0.3},
    {"exposure_id": "st_sanmu_operate_electromechanical", "company_id": "st_sanmu", "node_id": "electromechanical_product", "activity_type": "operate", "role": "机电产品销售商", "weight": 0.3},
    {"exposure_id": "hejin_manufacture_nickel_alloy", "company_id": "hejin_investment", "node_id": "nickel_based_alloy", "activity_type": "manufacture", "role": "镍基合金制造商", "weight": 0.9},
    {"exposure_id": "yinglite_manufacture_pvc", "company_id": "yinglite", "node_id": "pvc", "activity_type": "manufacture", "role": "PVC制造商", "weight": 0.8},
    {"exposure_id": "yinglite_manufacture_carbide", "company_id": "yinglite", "node_id": "calcium_carbide", "activity_type": "manufacture", "role": "电石制造商", "weight": 0.8},
    {"exposure_id": "yinglite_manufacture_dicyandiamide", "company_id": "yinglite", "node_id": "dicyandiamide", "activity_type": "manufacture", "role": "双氰胺制造商", "weight": 0.6},
    {"exposure_id": "fenghua_manufacture_ceramic_cap", "company_id": "fenghua_high_tech", "node_id": "ceramic_capacitor", "activity_type": "manufacture", "role": "陶瓷电容器制造商", "weight": 0.8},
    {"exposure_id": "fenghua_manufacture_chip_resistor", "company_id": "fenghua_high_tech", "node_id": "chip_resistor", "activity_type": "manufacture", "role": "片式电阻器制造商", "weight": 0.8},
    {"exposure_id": "fenghua_manufacture_battery_cell", "company_id": "fenghua_high_tech", "node_id": "lithium_battery_cell", "activity_type": "manufacture", "role": "锂离子电池电芯制造商", "weight": 0.6},
    {"exposure_id": "maohua_manufacture_pp", "company_id": "maohua_shihua", "node_id": "polypropylene", "activity_type": "manufacture", "role": "聚丙烯制造商", "weight": 0.8},
    {"exposure_id": "maohua_operate_lpg", "company_id": "maohua_shihua", "node_id": "lpg", "activity_type": "operate", "role": "液化气运营商", "weight": 0.6},
    {"exposure_id": "maohua_manufacture_salt", "company_id": "maohua_shihua", "node_id": "salt_product", "activity_type": "manufacture", "role": "盐产品制造商", "weight": 0.4},
    {"exposure_id": "st_wanfang_operate_real_estate", "company_id": "st_wanfang", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9},
    {"exposure_id": "st_xiwang_manufacture_edible_oil", "company_id": "st_xiwang", "node_id": "edible_oil", "activity_type": "manufacture", "role": "食用油制造商", "weight": 0.8},
    {"exposure_id": "st_xiwang_manufacture_supplement", "company_id": "st_xiwang", "node_id": "dietary_supplement", "activity_type": "manufacture", "role": "运动营养品制造商", "weight": 0.6},
    {"exposure_id": "renhe_manufacture_pharma", "company_id": "renhe_pharmaceutical", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "药品制造商", "weight": 0.8},
    {"exposure_id": "renhe_manufacture_chemical", "company_id": "renhe_pharmaceutical", "node_id": "chemical_drug", "activity_type": "manufacture", "role": "化学药制造商", "weight": 0.6},
    {"exposure_id": "renhe_manufacture_tcm", "company_id": "renhe_pharmaceutical", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中成药制造商", "weight": 0.5},
    {"exposure_id": "renhe_operate_retail", "company_id": "renhe_pharmaceutical", "node_id": "pharmaceutical_retail", "activity_type": "operate", "role": "医药零售商", "weight": 0.5},
    {"exposure_id": "gree_manufacture_air_conditioner", "company_id": "gree_electric", "node_id": "air_conditioner", "activity_type": "manufacture", "role": "空调制造商", "weight": 0.9},
    {"exposure_id": "gree_manufacture_refrigerator", "company_id": "gree_electric", "node_id": "refrigerator", "activity_type": "manufacture", "role": "冰箱制造商", "weight": 0.4},
    {"exposure_id": "gree_manufacture_small_home", "company_id": "gree_electric", "node_id": "small_home_appliance", "activity_type": "manufacture", "role": "小家电制造商", "weight": 0.4},
    {"exposure_id": "gree_manufacture_kitchen", "company_id": "gree_electric", "node_id": "kitchen_appliance", "activity_type": "manufacture", "role": "厨卫电器制造商", "weight": 0.3},
]

business_batch = {
    "batch_id": "batch_019_business",
    "task_description": "Batch 019 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 019 ===")
post_business_batch(business_batch)
