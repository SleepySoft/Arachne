"""
Batch 013 Submission Script
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
    {"node_id": "grinding_wheel", "canonical_name_zh": "固结磨具", "definition": "以磨料和结合剂制成的具有一定形状和强度的磨削工具，包括砂轮、油石等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "coated_abrasive", "canonical_name_zh": "涂附磨具", "definition": "将磨料涂附在柔性或刚性基材上制成的磨削材料，包括砂纸、砂带等", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "titanium_dioxide", "canonical_name_zh": "钛白粉", "definition": "二氧化钛白色颜料，广泛用于涂料、塑料、造纸和化妆品工业", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "titanium_ore", "canonical_name_zh": "钛矿", "definition": "含有钛元素的天然矿石，是生产钛白粉等钛制品的主要原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "real_estate_development", "canonical_name_zh": "房地产开发", "definition": "从事土地开发、房屋建设和销售的经营活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "generator_set", "canonical_name_zh": "发电机组", "definition": "将机械能转换为电能的成套设备，包括发动机、发电机和控制系统", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "communication_equipment", "canonical_name_zh": "通信设备", "definition": "用于信息传输和通信网络的电子设备及系统", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "highway", "canonical_name_zh": "高速公路", "definition": "专供汽车高速行驶的现代化公路基础设施", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "urban_complex", "canonical_name_zh": "城市综合体", "definition": "集商业、办公、居住、酒店和会展等功能于一体的综合性城市建筑集群", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "automotive_engine", "canonical_name_zh": "汽车发动机", "definition": "为汽车提供动力的内燃机或电动机系统，汽车的核心动力总成", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "light_truck", "canonical_name_zh": "轻型卡车", "definition": "总质量小于等于4.5吨的载货汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pickup_truck", "canonical_name_zh": "皮卡", "definition": "兼具载货和乘坐功能的轻型客货两用汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "suv", "canonical_name_zh": "SUV", "definition": "运动型多用途汽车，兼具越野能力和城市道路行驶性能", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "heavy_truck", "canonical_name_zh": "重型卡车", "definition": "总质量大于14吨的大型载货汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "commercial_vehicle", "canonical_name_zh": "商用车", "definition": "用于商业运输和营运活动的各类汽车，包括客车和货车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cast_part", "canonical_name_zh": "铸件", "definition": "通过铸造工艺获得的金属零件毛坯或成品", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cleanroom_equipment", "canonical_name_zh": "洁净设备", "definition": "用于控制空气洁净度、温湿度和压差的环境控制设备，广泛应用于电子和医药工业", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "insulator", "canonical_name_zh": "绝缘子", "definition": "输变电系统中用于电气绝缘和机械固定的器件，包括陶瓷和复合绝缘子", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "bearing", "canonical_name_zh": "轴承", "definition": "支撑机械旋转体并降低摩擦系数的精密机械元件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "surveying_instrument", "canonical_name_zh": "测绘仪器", "definition": "用于地形测量、工程测量的光机电算一体化精密仪器", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "abrasive_tool", "canonical_name_zh": "磨具", "definition": "利用磨料进行切削、研磨和抛光的工具总称", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "abrasive_material", "canonical_name_zh": "磨料", "definition": "具有锐利棱角和足够硬度的颗粒材料，用于磨削加工", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_titanium_ore_to_dioxide", "from_node": "titanium_ore", "to_node": "titanium_dioxide", "edge_type": "material_flow", "description": "钛矿是生产钛白粉的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cement_to_construction", "from_node": "cement", "to_node": "construction_service", "edge_type": "material_flow", "description": "水泥是建筑施工的重要材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cement_to_real_estate", "from_node": "cement", "to_node": "real_estate_development", "edge_type": "material_flow", "description": "水泥用于房地产开发建设"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_highway_to_operation", "from_node": "highway", "to_node": "highway_operation_service", "edge_type": "service_flow", "description": "高速公路提供道路运营服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_complex_to_mgmt", "from_node": "urban_complex", "to_node": "property_management_service", "edge_type": "service_flow", "description": "城市综合体需要物业管理服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_engine_to_light_truck", "from_node": "automotive_engine", "to_node": "light_truck", "edge_type": "composition", "description": "发动机是轻型卡车的核心动力总成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_engine_to_heavy_truck", "from_node": "automotive_engine", "to_node": "heavy_truck", "edge_type": "composition", "description": "发动机是重型卡车的核心动力总成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cast_to_engine", "from_node": "cast_part", "to_node": "automotive_engine", "edge_type": "composition", "description": "铸件是发动机缸体等关键部件的毛坯"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_light_truck_to_road", "from_node": "light_truck", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "轻型卡车是公路运输车辆的一种"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_heavy_truck_to_road", "from_node": "heavy_truck", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "重型卡车是公路运输车辆的一种"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_commercial_to_road", "from_node": "commercial_vehicle", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "商用车是公路运输车辆的重要组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_insulator_to_dist", "from_node": "insulator", "to_node": "power_distribution_equipment", "edge_type": "composition", "description": "绝缘子是输变电配电设备的组成元件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_abrasive_mat_to_tool", "from_node": "abrasive_material", "to_node": "abrasive_tool", "edge_type": "composition", "description": "磨料是磨具的核心工作材料"},
]

graph_batch = {
    "batch_id": "batch_013_graph",
    "task_description": "Batch 013 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 013 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "waneng_power", "name_zh": "皖能电力", "aliases": ["安徽省皖能股份有限公司"], "stock_codes": ["000543.SZ"], "country": "CN", "province": "安徽", "city": "合肥市", "employee_count": 4983, "company_type": "public", "description": "电力及节能项目投资经营企业，涵盖燃煤、燃气、太阳能、风力及水力发电"},
    {"company_id": "zhongyuan_environmental", "name_zh": "中原环保", "aliases": ["中原环保股份有限公司"], "stock_codes": ["000544.SZ"], "country": "CN", "province": "河南", "city": "郑州市", "employee_count": 2390, "company_type": "public", "description": "环境保护企业，主营城镇污水处理、集中供热及磨具制造"},
    {"company_id": "jinpu_titanium", "name_zh": "金浦钛业", "aliases": ["金浦钛业股份有限公司"], "stock_codes": ["000545.SZ"], "country": "CN", "province": "吉林", "city": "吉林市", "employee_count": 1149, "company_type": "public", "description": "钛白粉生产企业"},
    {"company_id": "jinyuan", "name_zh": "金圆股份", "aliases": ["金圆环保股份有限公司"], "stock_codes": ["000546.SZ"], "country": "CN", "province": "吉林", "city": "长春市", "employee_count": 503, "company_type": "public", "description": "水泥制造及房地产开发企业"},
    {"company_id": "aerospace_development", "name_zh": "航天发展", "aliases": ["航天工业发展股份有限公司"], "stock_codes": ["000547.SZ"], "country": "CN", "province": "福建", "city": "福州市", "employee_count": 2594, "company_type": "public", "description": "航天军工企业，主营通信设备、发电机组和机电新材料"},
    {"company_id": "hunan_investment", "name_zh": "湖南投资", "aliases": ["湖南投资集团股份有限公司"], "stock_codes": ["000548.SZ"], "country": "CN", "province": "湖南", "city": "长沙市", "employee_count": 620, "company_type": "public", "description": "基础设施投资企业，主营高速公路运营、酒店经营和城市综合体开发"},
    {"company_id": "jmc", "name_zh": "江铃汽车", "aliases": ["江铃汽车股份有限公司"], "stock_codes": ["000550.SZ"], "country": "CN", "province": "江西", "city": "南昌市", "employee_count": 11203, "company_type": "public", "description": "汽车整车制造企业，主要产品包括JMC轻型卡车、皮卡、SUV、重型卡车、福特全顺商用车及发动机"},
    {"company_id": "chuangyuan_tech", "name_zh": "创元科技", "aliases": ["创元科技股份有限公司"], "stock_codes": ["000551.SZ"], "country": "CN", "province": "江苏", "city": "苏州市", "employee_count": 2512, "company_type": "public", "description": "精密制造企业，主营洁净环保设备、输变电绝缘子、轴承、测绘仪器和磨具磨料"},
    {"company_id": "gansu_energy_chemical", "name_zh": "甘肃能化", "aliases": ["甘肃能化股份有限公司"], "stock_codes": ["000552.SZ"], "country": "CN", "province": "甘肃", "city": "白银市", "employee_count": 24300, "company_type": "public", "description": "煤炭开采洗选销售企业"},
    {"company_id": "adama", "name_zh": "安道麦A", "aliases": ["安道麦股份有限公司"], "stock_codes": ["000553.SZ"], "country": "CN", "province": "湖北", "city": "荆州市", "employee_count": 7255, "company_type": "public", "description": "农药和化工产品生产销售企业"},
]

exposures = [
    {"exposure_id": "waneng_power_produce_elec", "company_id": "waneng_power", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9},
    {"exposure_id": "waneng_power_produce_heat", "company_id": "waneng_power", "node_id": "heating_supply", "activity_type": "produce", "role": "热力生产商", "weight": 0.6},
    {"exposure_id": "waneng_power_operate_plant", "company_id": "waneng_power", "node_id": "power_plant_operation", "activity_type": "operate", "role": "电厂运营商", "weight": 0.9},
    {"exposure_id": "waneng_power_operate_coal", "company_id": "waneng_power", "node_id": "coal_power_generation", "activity_type": "operate", "role": "燃煤发电运营商", "weight": 0.6},
    {"exposure_id": "waneng_power_operate_solar", "company_id": "waneng_power", "node_id": "solar_power_generation", "activity_type": "operate", "role": "太阳能发电运营商", "weight": 0.3},
    {"exposure_id": "waneng_power_operate_wind", "company_id": "waneng_power", "node_id": "wind_power_generation", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.3},
    {"exposure_id": "zhongyuan_env_manufacture_grinding", "company_id": "zhongyuan_environmental", "node_id": "grinding_wheel", "activity_type": "manufacture", "role": "固结磨具制造商", "weight": 0.5},
    {"exposure_id": "zhongyuan_env_manufacture_coated", "company_id": "zhongyuan_environmental", "node_id": "coated_abrasive", "activity_type": "manufacture", "role": "涂附磨具制造商", "weight": 0.4},
    {"exposure_id": "zhongyuan_env_produce_heat", "company_id": "zhongyuan_environmental", "node_id": "heating_supply", "activity_type": "produce", "role": "热力生产商", "weight": 0.6},
    {"exposure_id": "zhongyuan_env_operate_wastewater", "company_id": "zhongyuan_environmental", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.7},
    {"exposure_id": "jinpu_titanium_manufacture_tio2", "company_id": "jinpu_titanium", "node_id": "titanium_dioxide", "activity_type": "manufacture", "role": "钛白粉制造商", "weight": 0.9},
    {"exposure_id": "jinpu_titanium_procure_ore", "company_id": "jinpu_titanium", "node_id": "titanium_ore", "activity_type": "procure", "role": "钛矿采购商", "weight": 0.8},
    {"exposure_id": "jinyuan_manufacture_cement", "company_id": "jinyuan", "node_id": "cement", "activity_type": "manufacture", "role": "水泥制造商", "weight": 0.7},
    {"exposure_id": "jinyuan_operate_real_estate", "company_id": "jinyuan", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.6},
    {"exposure_id": "aerospace_dev_manufacture_generator", "company_id": "aerospace_development", "node_id": "generator_set", "activity_type": "manufacture", "role": "发电机组制造商", "weight": 0.6},
    {"exposure_id": "aerospace_dev_manufacture_comm", "company_id": "aerospace_development", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.7},
    {"exposure_id": "hunan_inv_operate_highway", "company_id": "hunan_investment", "node_id": "highway", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.7},
    {"exposure_id": "hunan_inv_operate_highway_svc", "company_id": "hunan_investment", "node_id": "highway_operation_service", "activity_type": "operate", "role": "高速公路运营服务商", "weight": 0.7},
    {"exposure_id": "hunan_inv_operate_hotel", "company_id": "hunan_investment", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.4},
    {"exposure_id": "hunan_inv_operate_property", "company_id": "hunan_investment", "node_id": "property_management_service", "activity_type": "operate", "role": "物业管理服务商", "weight": 0.3},
    {"exposure_id": "jmc_manufacture_light_truck", "company_id": "jmc", "node_id": "light_truck", "activity_type": "manufacture", "role": "轻型卡车制造商", "weight": 0.8},
    {"exposure_id": "jmc_manufacture_pickup", "company_id": "jmc", "node_id": "pickup_truck", "activity_type": "manufacture", "role": "皮卡制造商", "weight": 0.6},
    {"exposure_id": "jmc_manufacture_suv", "company_id": "jmc", "node_id": "suv", "activity_type": "manufacture", "role": "SUV制造商", "weight": 0.5},
    {"exposure_id": "jmc_manufacture_heavy_truck", "company_id": "jmc", "node_id": "heavy_truck", "activity_type": "manufacture", "role": "重型卡车制造商", "weight": 0.4},
    {"exposure_id": "jmc_manufacture_commercial", "company_id": "jmc", "node_id": "commercial_vehicle", "activity_type": "manufacture", "role": "商用车制造商", "weight": 0.7},
    {"exposure_id": "jmc_manufacture_engine", "company_id": "jmc", "node_id": "automotive_engine", "activity_type": "manufacture", "role": "汽车发动机制造商", "weight": 0.7},
    {"exposure_id": "jmc_manufacture_cast", "company_id": "jmc", "node_id": "cast_part", "activity_type": "manufacture", "role": "铸件制造商", "weight": 0.5},
    {"exposure_id": "chuangyuan_manufacture_cleanroom", "company_id": "chuangyuan_tech", "node_id": "cleanroom_equipment", "activity_type": "manufacture", "role": "洁净环保设备制造商", "weight": 0.6},
    {"exposure_id": "chuangyuan_manufacture_insulator", "company_id": "chuangyuan_tech", "node_id": "insulator", "activity_type": "manufacture", "role": "输变电绝缘子制造商", "weight": 0.6},
    {"exposure_id": "chuangyuan_manufacture_bearing", "company_id": "chuangyuan_tech", "node_id": "bearing", "activity_type": "manufacture", "role": "轴承制造商", "weight": 0.5},
    {"exposure_id": "chuangyuan_manufacture_survey", "company_id": "chuangyuan_tech", "node_id": "surveying_instrument", "activity_type": "manufacture", "role": "测绘仪器制造商", "weight": 0.5},
    {"exposure_id": "chuangyuan_manufacture_abrasive_tool", "company_id": "chuangyuan_tech", "node_id": "abrasive_tool", "activity_type": "manufacture", "role": "磨具制造商", "weight": 0.4},
    {"exposure_id": "chuangyuan_manufacture_abrasive_mat", "company_id": "chuangyuan_tech", "node_id": "abrasive_material", "activity_type": "manufacture", "role": "磨料制造商", "weight": 0.4},
    {"exposure_id": "gansu_energy_produce_coal", "company_id": "gansu_energy_chemical", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.9},
    {"exposure_id": "adama_manufacture_pesticide", "company_id": "adama", "node_id": "pesticide", "activity_type": "manufacture", "role": "农药制造商", "weight": 0.9},
    {"exposure_id": "adama_manufacture_fertilizer", "company_id": "adama", "node_id": "chemical_fertilizer", "activity_type": "manufacture", "role": "化肥制造商", "weight": 0.5},
    {"exposure_id": "adama_manufacture_petro", "company_id": "adama", "node_id": "petrochemical_product", "activity_type": "manufacture", "role": "化工产品制造商", "weight": 0.6},
]

business_batch = {
    "batch_id": "batch_013_business",
    "task_description": "Batch 013 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 013 ===")
post_business_batch(business_batch)
