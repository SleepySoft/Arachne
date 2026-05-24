"""
Batch 018 Submission Script
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
    {"node_id": "cosmetic", "canonical_name_zh": "化妆品", "definition": "以涂擦、喷洒或其他类似方法施用于人体表面以达到清洁、保养、美容和修饰目的的日用化学工业产品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "medical_cosmetic_service", "canonical_name_zh": "医疗美容服务", "definition": "运用手术、药物和医疗器械等医学技术对人的容貌和身体部位进行修复和再塑的专业医疗服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "viscose_filament", "canonical_name_zh": "粘胶长丝", "definition": "以天然纤维素为原料经化学处理制成的连续长丝纤维，用于高档服装和装饰织物", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "gas_engine", "canonical_name_zh": "气体机", "definition": "以天然气、沼气或煤气等气体燃料工作的内燃机", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "diesel_generator_set", "canonical_name_zh": "柴油发电机组", "definition": "以柴油机为动力驱动发电机发电的成套设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "gas_generator_set", "canonical_name_zh": "燃气发电机组", "definition": "以气体燃料发动机为动力驱动发电机发电的成套设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "building_profile", "canonical_name_zh": "建筑型材", "definition": "具有特定截面形状的金属材料或塑料材料，用于建筑结构的框架和围护系统", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "door_window", "canonical_name_zh": "门窗", "definition": "建筑物中用于采光、通风和出入的围护构件总成", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "plastic_profile", "canonical_name_zh": "塑料型材", "definition": "以聚氯乙烯等塑料为原料挤出成型的具有特定截面形状的建材", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "passenger_car", "canonical_name_zh": "乘用车", "definition": "设计和技术特性上主要用于载运乘客及其随身行李的汽车，包括轿车、SUV和MPV等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "mini_bus", "canonical_name_zh": "微型客车", "definition": "车长小于等于3.5米、发动机排量小于等于1升的小型载客汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "mini_truck", "canonical_name_zh": "微型货车", "definition": "车长小于等于3.5米、总质量小于等于1.8吨的小型载货汽车", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "trade_service", "canonical_name_zh": "商贸服务", "definition": "从事商品批发、零售和进出口代理的贸易经营活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "futures_brokerage", "canonical_name_zh": "期货经纪", "definition": "接受客户委托代理进行期货合约买卖并收取佣金的中介服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "kitchen_cabinet", "canonical_name_zh": "厨柜", "definition": "厨房中用于储存物品和操作的平台及柜体组合家具", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vanadium_titanium", "canonical_name_zh": "钒钛制品", "definition": "以钒和钛为主要元素的有色金属合金及化合物产品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vanadium_oxide", "canonical_name_zh": "氧化钒", "definition": "钒的氧化物，是生产钒铁和钒氮合金的主要原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "ferrovanadium", "canonical_name_zh": "钒铁", "definition": "钒与铁组成的合金，是炼钢中重要的合金添加剂", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vanadium_nitrogen_alloy", "canonical_name_zh": "钒氮合金", "definition": "钒、氮和铁的合金，作为高强度低合金钢的微合金化元素", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "titanium_slag", "canonical_name_zh": "钛渣", "definition": "高钛高炉渣或电炉渣，是生产钛白粉的主要原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "copper", "canonical_name_zh": "阴极铜", "definition": "通过电解精炼得到的高纯度铜，是重要的工业基础原材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "copper_wire", "canonical_name_zh": "铜线", "definition": "以铜为导体材料拉制成的线材，用于电力传输和电气设备", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "copper_foil", "canonical_name_zh": "铜箔", "definition": "厚度很薄的铜带材，主要用于印制电路板、锂电池和电磁屏蔽", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "copper_sheet", "canonical_name_zh": "铜板带", "definition": "宽度大于厚度十倍的扁平铜材，广泛用于电气、建筑和热交换领域", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_viscose_filament_to_fiber", "from_node": "viscose_filament", "to_node": "viscose_fiber", "edge_type": "composition", "description": "粘胶长丝是粘胶纤维的一种产品形式"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_to_diesel_gen", "from_node": "diesel_engine", "to_node": "diesel_generator_set", "edge_type": "composition", "description": "柴油机是柴油发电机组的动力单元"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_gas_engine_to_gas_gen", "from_node": "gas_engine", "to_node": "gas_generator_set", "edge_type": "composition", "description": "气体机是燃气发电机组的动力单元"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_gen_to_gen_set", "from_node": "diesel_generator_set", "to_node": "generator_set", "edge_type": "composition", "description": "柴油发电机组是发电机组的一种类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_gas_gen_to_gen_set", "from_node": "gas_generator_set", "to_node": "generator_set", "edge_type": "composition", "description": "燃气发电机组是发电机组的一种类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_plastic_to_profile", "from_node": "plastic_resin", "to_node": "plastic_profile", "edge_type": "material_flow", "description": "塑料树脂是塑料型材的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_plastic_profile_to_building", "from_node": "plastic_profile", "to_node": "building_profile", "edge_type": "composition", "description": "塑料型材是建筑型材的重要品类"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_profile_to_door_window", "from_node": "building_profile", "to_node": "door_window", "edge_type": "composition", "description": "建筑型材是门窗产品的主要框架材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_engine_to_passenger_car", "from_node": "automotive_engine", "to_node": "passenger_car", "edge_type": "composition", "description": "发动机是乘用车的核心动力总成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_engine_to_mini_bus", "from_node": "automotive_engine", "to_node": "mini_bus", "edge_type": "composition", "description": "发动机是微型客车的核心动力总成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_engine_to_mini_truck", "from_node": "automotive_engine", "to_node": "mini_truck", "edge_type": "composition", "description": "发动机是微型货车的核心动力总成"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_passenger_to_road", "from_node": "passenger_car", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "乘用车是公路运输车辆的组成类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_mini_bus_to_road", "from_node": "mini_bus", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "微型客车是公路运输车辆的组成类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_mini_truck_to_road", "from_node": "mini_truck", "to_node": "road_transport_vehicle", "edge_type": "composition", "description": "微型货车是公路运输车辆的组成类型"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_trade_to_retail", "from_node": "trade_service", "to_node": "chain_retail_service", "edge_type": "service_flow", "description": "商贸服务是连锁零售的上游环节"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_vanadium_oxide_to_ferro", "from_node": "vanadium_oxide", "to_node": "ferrovanadium", "edge_type": "material_flow", "description": "氧化钒经还原冶炼成为钒铁"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ferro_to_vanadium_nitrogen", "from_node": "ferrovanadium", "to_node": "vanadium_nitrogen_alloy", "edge_type": "material_flow", "description": "钒铁是生产钒氮合金的原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_titanium_slag_to_dioxide", "from_node": "titanium_slag", "to_node": "titanium_dioxide", "edge_type": "material_flow", "description": "钛渣是生产钛白粉的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_vanadium_oxide_to_product", "from_node": "vanadium_oxide", "to_node": "vanadium_titanium", "edge_type": "composition", "description": "氧化钒是钒钛制品的组成产品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ferro_to_product", "from_node": "ferrovanadium", "to_node": "vanadium_titanium", "edge_type": "composition", "description": "钒铁是钒钛制品的组成产品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_copper_to_wire", "from_node": "copper", "to_node": "copper_wire", "edge_type": "material_flow", "description": "阴极铜加工成铜线"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_copper_to_foil", "from_node": "copper", "to_node": "copper_foil", "edge_type": "material_flow", "description": "阴极铜加工成铜箔"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_copper_to_sheet", "from_node": "copper", "to_node": "copper_sheet", "edge_type": "material_flow", "description": "阴极铜加工成铜板带"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_copper_to_wire_cable", "from_node": "copper", "to_node": "wire_cable", "edge_type": "material_flow", "description": "阴极铜是电线电缆的主要导体材料"},
]

graph_batch = {
    "batch_id": "batch_018_graph",
    "task_description": "Batch 018 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 018 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "st_meigu", "name_zh": "*ST美谷", "aliases": ["九州美谷科技股份有限公司"], "stock_codes": ["000615.SZ"], "country": "CN", "province": "湖北", "city": "襄阳市", "employee_count": 2206, "company_type": "public", "description": "综合企业，主营粘胶长丝、移动通信器材、房地产和医疗美容业务"},
    {"company_id": "zhongyou_capital", "name_zh": "中油资本", "aliases": ["中国石油集团资本股份有限公司"], "stock_codes": ["000617.SZ"], "country": "CN", "province": "新疆", "city": "克拉玛依市", "employee_count": 3979, "company_type": "public", "description": "能源装备企业，主营柴油机、柴油发电机组、气体机和燃气发电机组"},
    {"company_id": "hailuo_new_material", "name_zh": "海螺新材", "aliases": ["海螺(安徽)节能环保新材料股份有限公司"], "stock_codes": ["000619.SZ"], "country": "CN", "province": "安徽", "city": "芜湖市", "employee_count": 4133, "company_type": "public", "description": "建材企业，主营塑料型材和门窗产品"},
    {"company_id": "yingxin_development", "name_zh": "盈新发展", "aliases": ["北京铜官盈新文化旅游发展股份有限公司"], "stock_codes": ["000620.SZ"], "country": "CN", "province": "北京", "city": "北京市", "employee_count": 3097, "company_type": "public", "description": "房地产开发企业"},
    {"company_id": "jilin_aodong", "name_zh": "吉林敖东", "aliases": ["吉林敖东药业集团股份有限公司"], "stock_codes": ["000623.SZ"], "country": "CN", "province": "吉林", "city": "延边朝鲜族自治州", "employee_count": 5454, "company_type": "public", "description": "中成药制药企业"},
    {"company_id": "changan_automotive", "name_zh": "长安汽车", "aliases": ["重庆长安汽车股份有限公司"], "stock_codes": ["000625.SZ"], "country": "CN", "province": "重庆", "city": "重庆市", "employee_count": 55119, "company_type": "public", "description": "大型汽车整车制造企业，主营乘用车和发动机研发生产"},
    {"company_id": "yuanda_holdings", "name_zh": "远大控股", "aliases": ["远大产业控股股份有限公司"], "stock_codes": ["000626.SZ"], "country": "CN", "province": "江苏", "city": "连云港市", "employee_count": 1168, "company_type": "public", "description": "商贸企业，主营商品批发和零售贸易"},
    {"company_id": "gaoxin_development", "name_zh": "高新发展", "aliases": ["成都高新发展股份有限公司"], "stock_codes": ["000628.SZ"], "country": "CN", "province": "四川", "city": "成都市", "employee_count": 1100, "company_type": "public", "description": "综合企业，主营建筑业、期货经纪、房地产和厨柜制造"},
    {"company_id": "vantai", "name_zh": "钒钛股份", "aliases": ["攀钢集团钒钛资源股份有限公司"], "stock_codes": ["000629.SZ"], "country": "CN", "province": "四川", "city": "攀枝花市", "employee_count": 3182, "company_type": "public", "description": "钒钛资源企业，主营氧化钒、钒铁、钒氮合金、钛白粉和钛渣"},
    {"company_id": "tongling_nonferrous", "name_zh": "铜陵有色", "aliases": ["铜陵有色金属集团股份有限公司"], "stock_codes": ["000630.SZ"], "country": "CN", "province": "安徽", "city": "铜陵市", "employee_count": 11669, "company_type": "public", "description": "大型铜冶炼企业，主营阴极铜、黄金、白银及铜加工产品"},
]

exposures = [
    {"exposure_id": "st_meigu_manufacture_viscose_fiber", "company_id": "st_meigu", "node_id": "viscose_fiber", "activity_type": "manufacture", "role": "粘胶纤维制造商", "weight": 0.5},
    {"exposure_id": "st_meigu_manufacture_viscose_filament", "company_id": "st_meigu", "node_id": "viscose_filament", "activity_type": "manufacture", "role": "粘胶长丝制造商", "weight": 0.5},
    {"exposure_id": "st_meigu_manufacture_comm_equip", "company_id": "st_meigu", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "移动通信器材制造商", "weight": 0.3},
    {"exposure_id": "st_meigu_operate_real_estate", "company_id": "st_meigu", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.3},
    {"exposure_id": "st_meigu_manufacture_cosmetic", "company_id": "st_meigu", "node_id": "cosmetic", "activity_type": "manufacture", "role": "化妆品制造商", "weight": 0.3},
    {"exposure_id": "st_meigu_operate_medical_cosmetic", "company_id": "st_meigu", "node_id": "medical_cosmetic_service", "activity_type": "operate", "role": "医疗美容服务商", "weight": 0.4},
    {"exposure_id": "st_meigu_manufacture_medical_device", "company_id": "st_meigu", "node_id": "medical_device", "activity_type": "manufacture", "role": "医疗器械制造商", "weight": 0.2},
    {"exposure_id": "zhongyou_manufacture_diesel_engine", "company_id": "zhongyou_capital", "node_id": "diesel_engine", "activity_type": "manufacture", "role": "柴油机制造商", "weight": 0.8},
    {"exposure_id": "zhongyou_manufacture_gas_engine", "company_id": "zhongyou_capital", "node_id": "gas_engine", "activity_type": "manufacture", "role": "气体机制造商", "weight": 0.7},
    {"exposure_id": "zhongyou_manufacture_generator", "company_id": "zhongyou_capital", "node_id": "generator_set", "activity_type": "manufacture", "role": "发电机组制造商", "weight": 0.8},
    {"exposure_id": "zhongyou_manufacture_diesel_gen", "company_id": "zhongyou_capital", "node_id": "diesel_generator_set", "activity_type": "manufacture", "role": "柴油发电机组制造商", "weight": 0.7},
    {"exposure_id": "zhongyou_manufacture_gas_gen", "company_id": "zhongyou_capital", "node_id": "gas_generator_set", "activity_type": "manufacture", "role": "燃气发电机组制造商", "weight": 0.6},
    {"exposure_id": "hailuo_manufacture_profile", "company_id": "hailuo_new_material", "node_id": "building_profile", "activity_type": "manufacture", "role": "建筑型材制造商", "weight": 0.8},
    {"exposure_id": "hailuo_manufacture_door_window", "company_id": "hailuo_new_material", "node_id": "door_window", "activity_type": "manufacture", "role": "门窗制造商", "weight": 0.8},
    {"exposure_id": "hailuo_manufacture_plastic_profile", "company_id": "hailuo_new_material", "node_id": "plastic_profile", "activity_type": "manufacture", "role": "塑料型材制造商", "weight": 0.9},
    {"exposure_id": "yingxin_operate_real_estate", "company_id": "yingxin_development", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9},
    {"exposure_id": "jilin_manufacture_tcm", "company_id": "jilin_aodong", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中成药制造商", "weight": 0.9},
    {"exposure_id": "changan_manufacture_engine", "company_id": "changan_automotive", "node_id": "automotive_engine", "activity_type": "manufacture", "role": "汽车发动机制造商", "weight": 0.9},
    {"exposure_id": "changan_manufacture_passenger_car", "company_id": "changan_automotive", "node_id": "passenger_car", "activity_type": "manufacture", "role": "乘用车制造商", "weight": 0.9},
    {"exposure_id": "changan_manufacture_mini_bus", "company_id": "changan_automotive", "node_id": "mini_bus", "activity_type": "manufacture", "role": "微型客车制造商", "weight": 0.6},
    {"exposure_id": "changan_manufacture_mini_truck", "company_id": "changan_automotive", "node_id": "mini_truck", "activity_type": "manufacture", "role": "微型货车制造商", "weight": 0.6},
    {"exposure_id": "changan_manufacture_vehicle", "company_id": "changan_automotive", "node_id": "road_transport_vehicle", "activity_type": "manufacture", "role": "整车制造商", "weight": 0.9},
    {"exposure_id": "changan_operate_sales", "company_id": "changan_automotive", "node_id": "automotive_sales_service", "activity_type": "operate", "role": "汽车销售服务商", "weight": 0.7},
    {"exposure_id": "yuanda_operate_trade", "company_id": "yuanda_holdings", "node_id": "trade_service", "activity_type": "operate", "role": "商贸服务商", "weight": 0.9},
    {"exposure_id": "gaoxin_operate_construction", "company_id": "gaoxin_development", "node_id": "construction_service", "activity_type": "operate", "role": "建筑施工服务商", "weight": 0.6},
    {"exposure_id": "gaoxin_operate_futures", "company_id": "gaoxin_development", "node_id": "futures_brokerage", "activity_type": "operate", "role": "期货经纪商", "weight": 0.4},
    {"exposure_id": "gaoxin_operate_real_estate", "company_id": "gaoxin_development", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.4},
    {"exposure_id": "gaoxin_manufacture_kitchen", "company_id": "gaoxin_development", "node_id": "kitchen_cabinet", "activity_type": "manufacture", "role": "厨柜制造商", "weight": 0.3},
    {"exposure_id": "vantai_manufacture_vanadium_oxide", "company_id": "vantai", "node_id": "vanadium_oxide", "activity_type": "manufacture", "role": "氧化钒制造商", "weight": 0.8},
    {"exposure_id": "vantai_manufacture_ferrovanadium", "company_id": "vantai", "node_id": "ferrovanadium", "activity_type": "manufacture", "role": "钒铁制造商", "weight": 0.8},
    {"exposure_id": "vantai_manufacture_vanadium_nitrogen", "company_id": "vantai", "node_id": "vanadium_nitrogen_alloy", "activity_type": "manufacture", "role": "钒氮合金制造商", "weight": 0.7},
    {"exposure_id": "vantai_manufacture_titanium_dioxide", "company_id": "vantai", "node_id": "titanium_dioxide", "activity_type": "manufacture", "role": "钛白粉制造商", "weight": 0.7},
    {"exposure_id": "vantai_manufacture_titanium_slag", "company_id": "vantai", "node_id": "titanium_slag", "activity_type": "manufacture", "role": "钛渣制造商", "weight": 0.6},
    {"exposure_id": "vantai_manufacture_vanadium_titanium", "company_id": "vantai", "node_id": "vanadium_titanium", "activity_type": "manufacture", "role": "钒钛制品制造商", "weight": 0.9},
    {"exposure_id": "tongling_manufacture_copper", "company_id": "tongling_nonferrous", "node_id": "copper", "activity_type": "manufacture", "role": "阴极铜制造商", "weight": 0.9},
    {"exposure_id": "tongling_manufacture_copper_wire", "company_id": "tongling_nonferrous", "node_id": "copper_wire", "activity_type": "manufacture", "role": "铜线制造商", "weight": 0.7},
    {"exposure_id": "tongling_manufacture_copper_foil", "company_id": "tongling_nonferrous", "node_id": "copper_foil", "activity_type": "manufacture", "role": "铜箔制造商", "weight": 0.6},
    {"exposure_id": "tongling_manufacture_copper_sheet", "company_id": "tongling_nonferrous", "node_id": "copper_sheet", "activity_type": "manufacture", "role": "铜板带制造商", "weight": 0.6},
    {"exposure_id": "tongling_produce_precious", "company_id": "tongling_nonferrous", "node_id": "precious_metal", "activity_type": "produce", "role": "贵金属生产商", "weight": 0.5},
    {"exposure_id": "tongling_produce_silver", "company_id": "tongling_nonferrous", "node_id": "silver", "activity_type": "produce", "role": "白银生产商", "weight": 0.4},
]

business_batch = {
    "batch_id": "batch_018_business",
    "task_description": "Batch 018 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 018 ===")
post_business_batch(business_batch)
