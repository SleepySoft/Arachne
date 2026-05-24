"""
Batch 011 Submission Script
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
    {"node_id": "cylinder_liner", "canonical_name_zh": "气缸套", "definition": "内燃机气缸套，用于活塞往复运动的圆柱形耐磨部件，是内燃机的关键基础件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aluminum_piston", "canonical_name_zh": "铝活塞", "definition": "内燃机铝合金活塞，用于将燃烧产生的热能转化为机械能的关键运动部件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "artillery_shell", "canonical_name_zh": "炮弹", "definition": "大口径火炮发射的弹药，包含弹体、装药和引信等部分", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rocket", "canonical_name_zh": "火箭弹", "definition": "依靠火箭发动机自推进的弹药系统，用于面杀伤或破甲作战", "entity_type": "system", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "missile", "canonical_name_zh": "导弹", "definition": "带有制导系统的自推进飞行武器，可精确打击目标", "entity_type": "system", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "modified_vehicle", "canonical_name_zh": "改装车", "definition": "基于现有汽车底盘进行结构或功能改装的特种车辆", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "special_purpose_vehicle", "canonical_name_zh": "专用车", "definition": "针对特定用途设计的专用汽车，如工程车、消防车等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vessel", "canonical_name_zh": "船舶", "definition": "用于水路运输的各类机动或非机动船只", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vessel_repair_service", "canonical_name_zh": "船舶维修服务", "definition": "对船舶进行维护、修理、技术改造和检验的服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pilotage_service", "canonical_name_zh": "引航服务", "definition": "为船舶进出港口或复杂水域提供操纵和导航的专业服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "freight_forwarding_service", "canonical_name_zh": "货运代理服务", "definition": "为货主组织运输、办理单证和协调物流节点的中介服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "sulfonic_acid", "canonical_name_zh": "磺酸", "definition": "洗涤用品的主要有机原料，用于合成各类表面活性剂", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "glycerin", "canonical_name_zh": "甘油", "definition": "精甘油，广泛用于化妆品、洗涤剂和食品工业的原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aes_surfactant", "canonical_name_zh": "AES表面活性剂", "definition": "脂肪醇聚氧乙烯醚硫酸钠，洗涤用品核心表面活性剂原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "business_travel_service", "canonical_name_zh": "商旅服务", "definition": "为企业客户提供的商务旅行策划、预订和管理服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "scenic_area_service", "canonical_name_zh": "景区服务", "definition": "旅游景区的运营、管理、接待和配套服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "car_rental_service", "canonical_name_zh": "汽车租赁服务", "definition": "提供汽车短期或长期租赁的服务业务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cold_storage_equipment", "canonical_name_zh": "冷藏设备", "definition": "用于食品冷藏保鲜的制冷设备及配套系统", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cold_storage_facility", "canonical_name_zh": "冷藏设施", "definition": "冷库等食品低温存储基础设施", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_steel_to_cylinder", "from_node": "steel_sheet", "to_node": "cylinder_liner", "edge_type": "material_flow", "description": "钢材用于制造内燃机气缸套"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_alum_to_piston", "from_node": "aluminum_panel", "to_node": "aluminum_piston", "edge_type": "material_flow", "description": "铝合金用于制造内燃机活塞"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cylinder_to_engine", "from_node": "cylinder_liner", "to_node": "automotive_engine_accessory", "edge_type": "composition", "description": "气缸套是内燃机配件的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_piston_to_engine", "from_node": "aluminum_piston", "to_node": "automotive_engine_accessory", "edge_type": "composition", "description": "铝活塞是内燃机配件的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_steel_to_shell", "from_node": "steel_sheet", "to_node": "artillery_shell", "edge_type": "material_flow", "description": "钢材用于制造炮弹壳体"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_steel_to_rocket", "from_node": "steel_sheet", "to_node": "rocket", "edge_type": "material_flow", "description": "钢材用于制造火箭弹结构"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_steel_to_missile", "from_node": "steel_sheet", "to_node": "missile", "edge_type": "material_flow", "description": "钢材用于制造导弹结构"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_vessel_to_shipping", "from_node": "vessel", "to_node": "shipping_service", "edge_type": "service_flow", "description": "船舶提供航运运输服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_vessel_to_repair", "from_node": "vessel", "to_node": "vessel_repair_service", "edge_type": "service_flow", "description": "船舶运营产生维修服务需求"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_petro_to_sulfonic", "from_node": "petrochemical_product", "to_node": "sulfonic_acid", "edge_type": "material_flow", "description": "石化产品用于制备磺酸"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_petro_to_aes", "from_node": "petrochemical_product", "to_node": "aes_surfactant", "edge_type": "material_flow", "description": "石化产品用于制备AES表面活性剂"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_sulfonic_to_detergent", "from_node": "sulfonic_acid", "to_node": "detergent", "edge_type": "material_flow", "description": "磺酸是洗涤剂的重要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_glycerin_to_detergent", "from_node": "glycerin", "to_node": "detergent", "edge_type": "material_flow", "description": "甘油用于洗涤剂配方"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_aes_to_detergent", "from_node": "aes_surfactant", "to_node": "detergent", "edge_type": "material_flow", "description": "AES是洗涤剂的核心表面活性剂"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tourism_to_business", "from_node": "tourism_service", "to_node": "business_travel_service", "edge_type": "service_flow", "description": "旅游服务体系包含商旅服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tourism_to_scenic", "from_node": "tourism_service", "to_node": "scenic_area_service", "edge_type": "service_flow", "description": "旅游服务体系包含景区服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tourism_to_rental", "from_node": "tourism_service", "to_node": "car_rental_service", "edge_type": "service_flow", "description": "旅游服务体系包含汽车租赁服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_compressor_to_cold_equip", "from_node": "refrigeration_compressor", "to_node": "cold_storage_equipment", "edge_type": "composition", "description": "制冷压缩机是冷藏设备的核心组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cold_equip_to_chain", "from_node": "cold_storage_equipment", "to_node": "food_cold_chain_service", "edge_type": "capability_supply", "description": "冷藏设备支撑食品冷链服务能力"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_cold_facility_to_chain", "from_node": "cold_storage_facility", "to_node": "food_cold_chain_service", "edge_type": "capability_supply", "description": "冷藏设施支撑食品冷链服务能力"},
]

graph_batch = {
    "batch_id": "batch_011_graph",
    "task_description": "Batch 011 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 011 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "sihuan_bioscience", "name_zh": "四环生物", "aliases": ["江苏四环生物股份有限公司"], "stock_codes": ["000518.SZ"], "country": "CN", "province": "江苏", "city": "无锡市", "employee_count": 277, "company_type": "public", "description": "生物制药及园林绿化工程企业，主要产品包括德路生、欣粒生等生物药品"},
    {"company_id": "norinco_red_arrow", "name_zh": "中兵红箭", "aliases": ["中兵红箭股份有限公司"], "stock_codes": ["000519.SZ"], "country": "CN", "province": "河南", "city": "南阳市", "employee_count": 8320, "company_type": "public", "description": "内燃机配件、超硬材料和军品研发生产企业，主要产品包括气缸套、铝活塞、人造金刚石、炮弹、火箭弹等"},
    {"company_id": "fenghuang_shipping", "name_zh": "凤凰航运", "aliases": ["凤凰航运(武汉)股份有限公司"], "stock_codes": ["000520.SZ"], "country": "CN", "province": "湖北", "city": "武汉市", "employee_count": 92, "company_type": "public", "description": "水路运输服务企业，主营船舶租赁、销售、维修、引航、货运代理及综合物流"},
    {"company_id": "changhong_meiling", "name_zh": "长虹美菱", "aliases": ["长虹美菱股份有限公司"], "stock_codes": ["000521.SZ"], "country": "CN", "province": "安徽", "city": "合肥市", "employee_count": 14028, "company_type": "public", "description": "家用电器制造企业，主要产品包括冰箱柜、空调、洗衣机、厨卫、小家电和生物医疗低温存储设备"},
    {"company_id": "hongmian", "name_zh": "红棉股份", "aliases": ["广州市红棉智汇科创股份有限公司"], "stock_codes": ["000523.SZ"], "country": "CN", "province": "广东", "city": "广州市", "employee_count": 881, "company_type": "public", "description": "洗涤用品及化工原料生产企业，主要品牌包括浪奇、高富力，同时生产磺酸、精甘油、AES等原料"},
    {"company_id": "lingnan_holdings", "name_zh": "岭南控股", "aliases": ["广州岭南集团控股股份有限公司"], "stock_codes": ["000524.SZ"], "country": "CN", "province": "广东", "city": "广州市", "employee_count": 5823, "company_type": "public", "description": "旅游服务综合企业，主营商旅出行、酒店住宿、餐饮、会展、景区和汽车服务"},
    {"company_id": "redsun", "name_zh": "红太阳", "aliases": ["南京红太阳股份有限公司"], "stock_codes": ["000525.SZ"], "country": "CN", "province": "江苏", "city": "南京市", "employee_count": 2920, "company_type": "public", "description": "农药化肥生产企业，主营农药和化肥产品"},
    {"company_id": "xueda_education", "name_zh": "学大教育", "aliases": ["学大(厦门)教育科技集团股份有限公司"], "stock_codes": ["000526.SZ"], "country": "CN", "province": "福建", "city": "厦门市", "employee_count": 8627, "company_type": "public", "description": "教育服务企业，主营教育培训、教育咨询及相关技术服务"},
    {"company_id": "liugong", "name_zh": "柳工", "aliases": ["广西柳工机械股份有限公司"], "stock_codes": ["000528.SZ"], "country": "CN", "province": "广西", "city": "柳州市", "employee_count": 17009, "company_type": "public", "description": "工程机械制造企业，主营装载机、挖掘机、起重机、压路机、叉车等工程机械及配件"},
    {"company_id": "guanghong_holdings", "name_zh": "广弘控股", "aliases": ["广东广弘控股股份有限公司"], "stock_codes": ["000529.SZ"], "country": "CN", "province": "广东", "city": "广州市", "employee_count": 936, "company_type": "public", "description": "食品冷链及冷藏设备企业，主营食品冷藏物流和冷藏设备制造"},
]

exposures = [
    {"exposure_id": "sihuan_bioscience_manufacture_biological_drug", "company_id": "sihuan_bioscience", "node_id": "biological_drug", "activity_type": "manufacture", "role": "生物药品制造商", "weight": 0.8},
    {"exposure_id": "sihuan_bioscience_manufacture_tcm", "company_id": "sihuan_bioscience", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中药提取物及制剂生产商", "weight": 0.3},
    {"exposure_id": "sihuan_bioscience_provide_greening", "company_id": "sihuan_bioscience", "node_id": "greening_construction_service", "activity_type": "provide_service", "role": "园林绿化工程服务商", "weight": 0.2},
    {"exposure_id": "norinco_red_arrow_manufacture_cylinder_liner", "company_id": "norinco_red_arrow", "node_id": "cylinder_liner", "activity_type": "manufacture", "role": "气缸套制造商", "weight": 0.5},
    {"exposure_id": "norinco_red_arrow_manufacture_aluminum_piston", "company_id": "norinco_red_arrow", "node_id": "aluminum_piston", "activity_type": "manufacture", "role": "铝活塞制造商", "weight": 0.5},
    {"exposure_id": "norinco_red_arrow_manufacture_superhard", "company_id": "norinco_red_arrow", "node_id": "superhard_material", "activity_type": "manufacture", "role": "人造金刚石和立方氮化硼超硬材料制造商", "weight": 0.7},
    {"exposure_id": "norinco_red_arrow_manufacture_artillery", "company_id": "norinco_red_arrow", "node_id": "artillery_shell", "activity_type": "manufacture", "role": "炮弹制造商", "weight": 0.6},
    {"exposure_id": "norinco_red_arrow_manufacture_rocket", "company_id": "norinco_red_arrow", "node_id": "rocket", "activity_type": "manufacture", "role": "火箭弹制造商", "weight": 0.6},
    {"exposure_id": "norinco_red_arrow_manufacture_missile", "company_id": "norinco_red_arrow", "node_id": "missile", "activity_type": "manufacture", "role": "导弹制造商", "weight": 0.6},
    {"exposure_id": "norinco_red_arrow_manufacture_modified_vehicle", "company_id": "norinco_red_arrow", "node_id": "modified_vehicle", "activity_type": "manufacture", "role": "改装车制造商", "weight": 0.3},
    {"exposure_id": "norinco_red_arrow_manufacture_special_vehicle", "company_id": "norinco_red_arrow", "node_id": "special_purpose_vehicle", "activity_type": "manufacture", "role": "专用车制造商", "weight": 0.3},
    {"exposure_id": "fenghuang_shipping_operate_shipping", "company_id": "fenghuang_shipping", "node_id": "shipping_service", "activity_type": "operate", "role": "水路运输运营商", "weight": 0.9},
    {"exposure_id": "fenghuang_shipping_provide_repair", "company_id": "fenghuang_shipping", "node_id": "vessel_repair_service", "activity_type": "provide_service", "role": "船舶维修服务商", "weight": 0.4},
    {"exposure_id": "fenghuang_shipping_provide_pilotage", "company_id": "fenghuang_shipping", "node_id": "pilotage_service", "activity_type": "provide_service", "role": "引航服务商", "weight": 0.3},
    {"exposure_id": "fenghuang_shipping_provide_forwarding", "company_id": "fenghuang_shipping", "node_id": "freight_forwarding_service", "activity_type": "provide_service", "role": "货运代理服务商", "weight": 0.4},
    {"exposure_id": "fenghuang_shipping_provide_logistics", "company_id": "fenghuang_shipping", "node_id": "logistics_service", "activity_type": "provide_service", "role": "综合物流服务商", "weight": 0.5},
    {"exposure_id": "changhong_meiling_manufacture_refrigerator", "company_id": "changhong_meiling", "node_id": "refrigerator", "activity_type": "manufacture", "role": "冰箱柜制造商", "weight": 0.8},
    {"exposure_id": "changhong_meiling_manufacture_air_conditioner", "company_id": "changhong_meiling", "node_id": "air_conditioner", "activity_type": "manufacture", "role": "空调制造商", "weight": 0.7},
    {"exposure_id": "changhong_meiling_manufacture_washing_machine", "company_id": "changhong_meiling", "node_id": "washing_machine", "activity_type": "manufacture", "role": "洗衣机制造商", "weight": 0.6},
    {"exposure_id": "changhong_meiling_manufacture_kitchen", "company_id": "changhong_meiling", "node_id": "kitchen_appliance", "activity_type": "manufacture", "role": "厨卫电器制造商", "weight": 0.5},
    {"exposure_id": "changhong_meiling_manufacture_small_home", "company_id": "changhong_meiling", "node_id": "small_home_appliance", "activity_type": "manufacture", "role": "小家电制造商", "weight": 0.4},
    {"exposure_id": "changhong_meiling_manufacture_medical_cold", "company_id": "changhong_meiling", "node_id": "medical_cold_storage", "activity_type": "manufacture", "role": "生物医疗低温存储设备制造商", "weight": 0.3},
    {"exposure_id": "hongmian_manufacture_detergent", "company_id": "hongmian", "node_id": "detergent", "activity_type": "manufacture", "role": "浪奇高富力等品牌洗涤剂制造商", "weight": 0.8},
    {"exposure_id": "hongmian_manufacture_sulfonic_acid", "company_id": "hongmian", "node_id": "sulfonic_acid", "activity_type": "manufacture", "role": "磺酸原料制造商", "weight": 0.6},
    {"exposure_id": "hongmian_manufacture_glycerin", "company_id": "hongmian", "node_id": "glycerin", "activity_type": "manufacture", "role": "精甘油制造商", "weight": 0.5},
    {"exposure_id": "hongmian_manufacture_aes", "company_id": "hongmian", "node_id": "aes_surfactant", "activity_type": "manufacture", "role": "AES表面活性剂制造商", "weight": 0.6},
    {"exposure_id": "lingnan_holdings_provide_business_travel", "company_id": "lingnan_holdings", "node_id": "business_travel_service", "activity_type": "provide_service", "role": "商旅出行服务商", "weight": 0.7},
    {"exposure_id": "lingnan_holdings_operate_hotel", "company_id": "lingnan_holdings", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店住宿运营商", "weight": 0.8},
    {"exposure_id": "lingnan_holdings_operate_catering", "company_id": "lingnan_holdings", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.6},
    {"exposure_id": "lingnan_holdings_operate_exhibition", "company_id": "lingnan_holdings", "node_id": "exhibition_service", "activity_type": "operate", "role": "会展服务商", "weight": 0.4},
    {"exposure_id": "lingnan_holdings_provide_scenic", "company_id": "lingnan_holdings", "node_id": "scenic_area_service", "activity_type": "provide_service", "role": "景区服务商", "weight": 0.3},
    {"exposure_id": "lingnan_holdings_provide_car_rental", "company_id": "lingnan_holdings", "node_id": "car_rental_service", "activity_type": "provide_service", "role": "汽车租赁服务商", "weight": 0.3},
    {"exposure_id": "redsun_manufacture_pesticide", "company_id": "redsun", "node_id": "pesticide", "activity_type": "manufacture", "role": "农药制造商", "weight": 0.9},
    {"exposure_id": "redsun_manufacture_fertilizer", "company_id": "redsun", "node_id": "chemical_fertilizer", "activity_type": "manufacture", "role": "化肥制造商", "weight": 0.7},
    {"exposure_id": "xueda_education_provide_education", "company_id": "xueda_education", "node_id": "education_service", "activity_type": "provide_service", "role": "教育培训服务商", "weight": 1.0},
    {"exposure_id": "liugong_manufacture_construction_machinery", "company_id": "liugong", "node_id": "construction_machinery", "activity_type": "manufacture", "role": "工程机械整机制造商", "weight": 1.0},
    {"exposure_id": "guanghong_holdings_operate_cold_chain", "company_id": "guanghong_holdings", "node_id": "food_cold_chain_service", "activity_type": "operate", "role": "食品冷链物流运营商", "weight": 0.8},
    {"exposure_id": "guanghong_holdings_manufacture_cold_equip", "company_id": "guanghong_holdings", "node_id": "cold_storage_equipment", "activity_type": "manufacture", "role": "冷藏设备制造商", "weight": 0.6},
    {"exposure_id": "guanghong_holdings_operate_cold_facility", "company_id": "guanghong_holdings", "node_id": "cold_storage_facility", "activity_type": "operate", "role": "冷藏设施运营商", "weight": 0.5},
]

business_batch = {
    "batch_id": "batch_011_business",
    "task_description": "Batch 011 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 011 ===")
post_business_batch(business_batch)
