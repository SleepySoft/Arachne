"""
Batch 016 Submission Script
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
    {"node_id": "optical_fiber", "canonical_name_zh": "光纤", "definition": "由高纯度石英玻璃或塑料制成的可传导光信号的细长纤维，是光通信的传输介质", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "fiber_optic_device", "canonical_name_zh": "光电子器件", "definition": "利用光电效应实现光信号与电信号转换的器件，包括光收发器、光放大器等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "tire", "canonical_name_zh": "轮胎", "definition": "安装于车辆或机械上与地面接触的环形弹性橡胶制品，承担承载、缓冲和传动功能", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rubber", "canonical_name_zh": "橡胶", "definition": "具有高弹性的天然或合成高分子材料，是轮胎和密封件等产品的主要原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "radial_tire", "canonical_name_zh": "子午线轮胎", "definition": "胎体帘线呈子午线方向排列的轮胎，具有滚动阻力小、耐磨性好的特点", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "bias_tire", "canonical_name_zh": "斜交轮胎", "definition": "胎体帘线呈斜向交叉排列的传统结构轮胎", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "solar_photovoltaic_power_station", "canonical_name_zh": "太阳能光伏电站", "definition": "利用光伏组件将太阳能转换为电能的大型发电设施，包括组件、逆变器和并网系统", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "forestry", "canonical_name_zh": "林业", "definition": "从事森林培育、保护和利用的生产经营活动，包括造林、营林和林产品采集", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "wood_product", "canonical_name_zh": "木材产品", "definition": "以原木为原料经初加工得到的板材、方材和木制品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "timber", "canonical_name_zh": "原木", "definition": "经采伐后未经加工或仅经初步加工的树木主干，是木材工业的基础原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "artificial_board", "canonical_name_zh": "人造板", "definition": "以木材或其他植物纤维为原料，经机械加工分离成各种单元材料后施加胶粘剂压制而成的板材", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "lng", "canonical_name_zh": "液化天然气", "definition": "天然气经净化和低温液化处理后的液态产物，便于储存和远洋运输", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "distributed_energy", "canonical_name_zh": "分布式能源", "definition": "布置在用户端的能源综合利用系统，通常以天然气为燃料实现热电冷联供", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rolling_bearing", "canonical_name_zh": "滚动轴承", "definition": "利用滚动体在内外圈之间滚动来减小摩擦的精密机械元件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "active_pharmaceutical_ingredient", "canonical_name_zh": "原料药", "definition": "用于药品制造中的任何一种物质或物质的混合物，是制剂中的有效成分", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "antibiotic", "canonical_name_zh": "抗生素", "definition": "由微生物或人工合成的具有抑制或杀灭其他微生物作用的化学物质", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "sewage_treatment_service", "canonical_name_zh": "污水处理服务", "definition": "通过物理、化学和生物方法去除污水中污染物的专业环保服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "tap_water_supply", "canonical_name_zh": "自来水供应", "definition": "对原水进行净化处理后通过管网向用户提供饮用水的公用事业服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_optical_fiber_to_cable", "from_node": "optical_fiber", "to_node": "optical_fiber_cable", "edge_type": "composition", "description": "光纤是光缆的核心传输组件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_rubber_to_tire", "from_node": "rubber", "to_node": "tire", "edge_type": "material_flow", "description": "橡胶是轮胎的主要原材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tire_to_vehicle", "from_node": "tire", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "轮胎是公路运输车辆的行走部件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_radial_to_tire", "from_node": "radial_tire", "to_node": "tire", "edge_type": "composition", "description": "子午线轮胎是轮胎的一种结构类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_bias_to_tire", "from_node": "bias_tire", "to_node": "tire", "edge_type": "composition", "description": "斜交轮胎是轮胎的一种结构类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pv_module_to_station", "from_node": "photovoltaic_module", "to_node": "solar_photovoltaic_power_station", "edge_type": "composition", "description": "光伏组件是太阳能光伏电站的发电单元"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_station_to_solar_power", "from_node": "solar_photovoltaic_power_station", "to_node": "solar_power_generation", "edge_type": "service_flow", "description": "光伏电站提供太阳能发电服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_forestry_to_timber", "from_node": "forestry", "to_node": "timber", "edge_type": "service_flow", "description": "林业经营活动产出原木"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_timber_to_wood", "from_node": "timber", "to_node": "wood_product", "edge_type": "material_flow", "description": "原木经加工成为木材产品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_wood_to_board", "from_node": "wood_product", "to_node": "artificial_board", "edge_type": "material_flow", "description": "木材产品用于制造人造板"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_natgas_to_lng", "from_node": "natural_gas", "to_node": "lng", "edge_type": "material_flow", "description": "天然气液化后成为液化天然气"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_lng_to_city_gas", "from_node": "lng", "to_node": "city_gas_supply", "edge_type": "material_flow", "description": "液化天然气气化后进入城市燃气供应系统"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_distributed_to_elec", "from_node": "distributed_energy", "to_node": "electricity_power", "edge_type": "energy_flow", "description": "分布式能源系统产生电力"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_steel_to_bearing", "from_node": "steel_sheet", "to_node": "rolling_bearing", "edge_type": "material_flow", "description": "钢材用于制造滚动轴承的内外圈和滚动体"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_rolling_to_bearing", "from_node": "rolling_bearing", "to_node": "bearing", "edge_type": "composition", "description": "滚动轴承是轴承的主要类型之一"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_api_to_pharma", "from_node": "active_pharmaceutical_ingredient", "to_node": "pharmaceutical_product", "edge_type": "material_flow", "description": "原料药是药品制剂的核心有效成分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_api_to_antibiotic", "from_node": "active_pharmaceutical_ingredient", "to_node": "antibiotic", "edge_type": "material_flow", "description": "原料药经制剂加工成为抗生素药品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tap_to_sewage", "from_node": "tap_water_supply", "to_node": "waste_water_treatment", "edge_type": "service_flow", "description": "自来水使用后产生污水需要处理"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_sewage_to_treatment", "from_node": "sewage_treatment_service", "to_node": "waste_water_treatment", "edge_type": "service_flow", "description": "污水处理服务是废水处理的具体实施形式"},
]

graph_batch = {
    "batch_id": "batch_016_graph",
    "task_description": "Batch 016 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 016 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "huiyuan_communication", "name_zh": "汇源通信", "aliases": ["四川汇源光通信股份有限公司"], "stock_codes": ["000586.SZ"], "country": "CN", "province": "四川", "city": "成都市", "employee_count": 471, "company_type": "public", "description": "光通信企业，主营光缆、光纤、光电子器件及通讯设备制造"},
    {"company_id": "guizhou_tire", "name_zh": "贵州轮胎", "aliases": ["贵州轮胎股份有限公司"], "stock_codes": ["000589.SZ"], "country": "CN", "province": "贵州", "city": "贵阳市", "employee_count": 6627, "company_type": "public", "description": "轮胎制造企业，主要生产前进牌斜交轮胎和子午线轮胎"},
    {"company_id": "guhan_pharmaceutical", "name_zh": "古汉医药", "aliases": ["古汉医药集团股份公司"], "stock_codes": ["000590.SZ"], "country": "CN", "province": "湖南", "city": "衡阳市", "employee_count": 1064, "company_type": "public", "description": "医药企业，主营古汉养生精等中成药、克林霉素磷酸酯等化学药及人血白蛋白"},
    {"company_id": "solar_energy", "name_zh": "太阳能", "aliases": ["中节能太阳能股份有限公司"], "stock_codes": ["000591.SZ"], "country": "CN", "province": "重庆", "city": "重庆市", "employee_count": 1781, "company_type": "public", "description": "新能源企业，主营太阳能光伏电站的投资运营"},
    {"company_id": "pingtan_development", "name_zh": "平潭发展", "aliases": ["中福海峡(平潭)发展股份有限公司"], "stock_codes": ["000592.SZ"], "country": "CN", "province": "福建", "city": "福州市", "employee_count": 1067, "company_type": "public", "description": "林业企业，主营造林营林、林木产品加工销售及农资贸易"},
    {"company_id": "delong_huineng", "name_zh": "德龙汇能", "aliases": ["德龙汇能集团股份有限公司"], "stock_codes": ["000593.SZ"], "country": "CN", "province": "四川", "city": "成都市", "employee_count": 951, "company_type": "public", "description": "城市燃气企业，主营城市燃气、LNG业务和分布式能源"},
    {"company_id": "st_baoshi", "name_zh": "*ST宝实", "aliases": ["宁夏国运新能源股份有限公司"], "stock_codes": ["000595.SZ"], "country": "CN", "province": "宁夏", "city": "银川市", "employee_count": 729, "company_type": "public", "description": "轴承制造企业，主营各类滚动轴承的生产销售"},
    {"company_id": "gujing_gongjiu", "name_zh": "古井贡酒", "aliases": ["安徽古井贡酒股份有限公司"], "stock_codes": ["000596.SZ"], "country": "CN", "province": "安徽", "city": "亳州市", "employee_count": 13453, "company_type": "public", "description": "白酒酿造企业，主营古井贡酒系列白酒"},
    {"company_id": "northeast_pharmaceutical", "name_zh": "东北制药", "aliases": ["东北制药集团股份有限公司"], "stock_codes": ["000597.SZ"], "country": "CN", "province": "辽宁", "city": "沈阳市", "employee_count": 5727, "company_type": "public", "description": "化学制药企业，主营化学原料药和制剂药品的生产销售"},
    {"company_id": "xingrong_environment", "name_zh": "兴蓉环境", "aliases": ["成都市兴蓉环境股份有限公司"], "stock_codes": ["000598.SZ"], "country": "CN", "province": "四川", "city": "成都市", "employee_count": 5325, "company_type": "public", "description": "水务环保企业，主营污水处理和自来水供应"},
]

exposures = [
    {"exposure_id": "huiyuan_manufacture_optical_cable", "company_id": "huiyuan_communication", "node_id": "optical_fiber_cable", "activity_type": "manufacture", "role": "光缆制造商", "weight": 0.8},
    {"exposure_id": "huiyuan_manufacture_optical_fiber", "company_id": "huiyuan_communication", "node_id": "optical_fiber", "activity_type": "manufacture", "role": "光纤制造商", "weight": 0.7},
    {"exposure_id": "huiyuan_manufacture_comm_equip", "company_id": "huiyuan_communication", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.6},
    {"exposure_id": "huiyuan_manufacture_fiber_device", "company_id": "huiyuan_communication", "node_id": "fiber_optic_device", "activity_type": "manufacture", "role": "光电子器件制造商", "weight": 0.5},
    {"exposure_id": "guizhou_manufacture_tire", "company_id": "guizhou_tire", "node_id": "tire", "activity_type": "manufacture", "role": "轮胎制造商", "weight": 0.9},
    {"exposure_id": "guizhou_procure_rubber", "company_id": "guizhou_tire", "node_id": "rubber", "activity_type": "procure", "role": "橡胶采购商", "weight": 0.8},
    {"exposure_id": "guizhou_manufacture_radial", "company_id": "guizhou_tire", "node_id": "radial_tire", "activity_type": "manufacture", "role": "子午线轮胎制造商", "weight": 0.8},
    {"exposure_id": "guizhou_manufacture_bias", "company_id": "guizhou_tire", "node_id": "bias_tire", "activity_type": "manufacture", "role": "斜交轮胎制造商", "weight": 0.5},
    {"exposure_id": "guhan_manufacture_tcm", "company_id": "guhan_pharmaceutical", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中成药制造商", "weight": 0.7},
    {"exposure_id": "guhan_manufacture_chemical", "company_id": "guhan_pharmaceutical", "node_id": "chemical_drug", "activity_type": "manufacture", "role": "化学药制造商", "weight": 0.5},
    {"exposure_id": "guhan_manufacture_blood", "company_id": "guhan_pharmaceutical", "node_id": "blood_product", "activity_type": "manufacture", "role": "血液制品制造商", "weight": 0.4},
    {"exposure_id": "solar_energy_operate_solar", "company_id": "solar_energy", "node_id": "solar_power_generation", "activity_type": "operate", "role": "太阳能发电运营商", "weight": 0.9},
    {"exposure_id": "solar_energy_operate_pv_station", "company_id": "solar_energy", "node_id": "solar_photovoltaic_power_station", "activity_type": "operate", "role": "光伏电站运营商", "weight": 0.9},
    {"exposure_id": "solar_energy_manufacture_pv_module", "company_id": "solar_energy", "node_id": "photovoltaic_module", "activity_type": "manufacture", "role": "光伏组件制造商", "weight": 0.5},
    {"exposure_id": "pingtan_operate_forestry", "company_id": "pingtan_development", "node_id": "forestry", "activity_type": "operate", "role": "林业经营商", "weight": 0.7},
    {"exposure_id": "pingtan_manufacture_wood", "company_id": "pingtan_development", "node_id": "wood_product", "activity_type": "manufacture", "role": "木材产品制造商", "weight": 0.6},
    {"exposure_id": "pingtan_produce_timber", "company_id": "pingtan_development", "node_id": "timber", "activity_type": "produce", "role": "原木生产商", "weight": 0.5},
    {"exposure_id": "pingtan_manufacture_board", "company_id": "pingtan_development", "node_id": "artificial_board", "activity_type": "manufacture", "role": "人造板制造商", "weight": 0.4},
    {"exposure_id": "pingtan_operate_fertilizer", "company_id": "pingtan_development", "node_id": "chemical_fertilizer", "activity_type": "operate", "role": "化肥销售商", "weight": 0.3},
    {"exposure_id": "delong_operate_natgas", "company_id": "delong_huineng", "node_id": "natural_gas", "activity_type": "operate", "role": "天然气运营商", "weight": 0.8},
    {"exposure_id": "delong_operate_city_gas", "company_id": "delong_huineng", "node_id": "city_gas_supply", "activity_type": "operate", "role": "城市燃气供应商", "weight": 0.9},
    {"exposure_id": "delong_operate_lng", "company_id": "delong_huineng", "node_id": "lng", "activity_type": "operate", "role": "LNG业务运营商", "weight": 0.6},
    {"exposure_id": "delong_operate_distributed", "company_id": "delong_huineng", "node_id": "distributed_energy", "activity_type": "operate", "role": "分布式能源运营商", "weight": 0.5},
    {"exposure_id": "st_baoshi_manufacture_rolling", "company_id": "st_baoshi", "node_id": "rolling_bearing", "activity_type": "manufacture", "role": "滚动轴承制造商", "weight": 0.9},
    {"exposure_id": "st_baoshi_manufacture_bearing", "company_id": "st_baoshi", "node_id": "bearing", "activity_type": "manufacture", "role": "轴承制造商", "weight": 0.8},
    {"exposure_id": "gujing_manufacture_liquor", "company_id": "gujing_gongjiu", "node_id": "liquor", "activity_type": "manufacture", "role": "白酒酿造商", "weight": 1.0},
    {"exposure_id": "northeast_manufacture_chemical", "company_id": "northeast_pharmaceutical", "node_id": "chemical_drug", "activity_type": "manufacture", "role": "化学药品制造商", "weight": 0.8},
    {"exposure_id": "northeast_manufacture_pharma", "company_id": "northeast_pharmaceutical", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "制剂药品制造商", "weight": 0.7},
    {"exposure_id": "northeast_manufacture_api", "company_id": "northeast_pharmaceutical", "node_id": "active_pharmaceutical_ingredient", "activity_type": "manufacture", "role": "原料药制造商", "weight": 0.8},
    {"exposure_id": "northeast_manufacture_antibiotic", "company_id": "northeast_pharmaceutical", "node_id": "antibiotic", "activity_type": "manufacture", "role": "抗生素制造商", "weight": 0.6},
    {"exposure_id": "xingrong_operate_wastewater", "company_id": "xingrong_environment", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.9},
    {"exposure_id": "xingrong_operate_sewage", "company_id": "xingrong_environment", "node_id": "sewage_treatment_service", "activity_type": "operate", "role": "污水处理服务商", "weight": 0.8},
    {"exposure_id": "xingrong_operate_tap_water", "company_id": "xingrong_environment", "node_id": "tap_water_supply", "activity_type": "operate", "role": "自来水供应商", "weight": 0.7},
]

business_batch = {
    "batch_id": "batch_016_business",
    "task_description": "Batch 016 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 016 ===")
post_business_batch(business_batch)
