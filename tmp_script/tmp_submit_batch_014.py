"""
Batch 014 Submission Script
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
    {"node_id": "gasoline", "canonical_name_zh": "汽油", "definition": "石油炼制得到的轻质石油产品，主要用于点燃式内燃机燃料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "diesel", "canonical_name_zh": "柴油", "definition": "石油炼制得到的中质石油产品，主要用于压燃式内燃机燃料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "fuel_retail_service", "canonical_name_zh": "成品油零售服务", "definition": "通过加油站等终端网络向消费者销售汽油、柴油等成品油的服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cng_station", "canonical_name_zh": "加气站", "definition": "为车辆提供压缩天然气或液化天然气加注服务的基础设施", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "atm_machine", "canonical_name_zh": "ATM机", "definition": "自动柜员机，为客户提供自助取款、转账和查询等金融服务的终端设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "software_development_service", "canonical_name_zh": "软件开发服务", "definition": "根据客户需求进行软件系统设计、编码、测试和交付的专业技术服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "fintech_service", "canonical_name_zh": "金融科技服务", "definition": "利用信息技术为金融行业提供产品创新、风险管理和运营效率提升的服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rail_transport_service", "canonical_name_zh": "铁路运输服务", "definition": "利用铁路网络提供货物和旅客运输的服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "warehouse_service", "canonical_name_zh": "仓储服务", "definition": "提供货物存储、保管、分拣和配送中转的物流服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "wine", "canonical_name_zh": "葡萄酒", "definition": "以葡萄为原料经发酵酿制而成的酒精饮料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "universal_joint", "canonical_name_zh": "万向节", "definition": "实现变角度动力传递的机械部件，广泛应用于汽车传动系统", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "wheel_hub_unit", "canonical_name_zh": "轮毂单元", "definition": "集成轮毂、轴承和密封件的汽车底盘旋转部件总成", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "automotive_exhaust_system", "canonical_name_zh": "汽车排气系统", "definition": "收集并净化发动机废气、降低噪声并安全排出的汽车子系统", "entity_type": "subsystem", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "fuel_tank", "canonical_name_zh": "燃油箱", "definition": "用于储存汽车燃油的容器总成", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "machinery_part", "canonical_name_zh": "机械零部件", "definition": "工程机械和通用机械设备中使用的各类金属零部件", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "real_estate_agency_service", "canonical_name_zh": "房地产经纪服务", "definition": "为房地产交易提供居间、代理和咨询的专业服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "residential_asset_management", "canonical_name_zh": "住宅资产管理", "definition": "对住宅类不动产进行运营、维护和增值管理的综合服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "commercial_property_operation", "canonical_name_zh": "商业地产运营", "definition": "对商业用途不动产进行招商、运营和管理的综合服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "electroacoustic_device", "canonical_name_zh": "电声器材", "definition": "将电信号与声音信号相互转换的电子设备及器件", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "wire_cable", "canonical_name_zh": "电线电缆", "definition": "用于传输电能和信号的导线及其绝缘护套组合产品", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "textile_machinery", "canonical_name_zh": "纺织机械", "definition": "用于纤维加工、纺纱、织造和染整的机械设备", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "trust_service", "canonical_name_zh": "信托服务", "definition": "受托人按照委托人意愿管理财产并提供财产保值增值和传承安排的金融服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "department_store", "canonical_name_zh": "百货零售", "definition": "经营多种商品门类、面向消费者的大型零售业态", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "paint", "canonical_name_zh": "油漆", "definition": "涂覆于物体表面形成保护或装饰膜的液态或粉末状涂料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "coating", "canonical_name_zh": "涂料", "definition": "具有流动性的材料，施涂于底材表面能形成具有保护、装饰或其他特殊功能的连续膜层", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "synthetic_resin", "canonical_name_zh": "合成树脂", "definition": "通过化学合成方法制得的高分子化合物，是涂料、塑料和胶粘剂的主要基料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "metal_packaging", "canonical_name_zh": "金属包装", "definition": "以金属薄板为主要材料制成的包装容器，如印铁包装桶、易拉罐等", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_refinery_to_gasoline", "from_node": "refining_service", "to_node": "gasoline", "edge_type": "service_flow", "description": "石油炼制服务产出汽油"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_refinery_to_diesel", "from_node": "refining_service", "to_node": "diesel", "edge_type": "service_flow", "description": "石油炼制服务产出柴油"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_gasoline_to_retail", "from_node": "gasoline", "to_node": "fuel_retail_service", "edge_type": "service_flow", "description": "汽油通过零售服务到达终端消费者"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_diesel_to_retail", "from_node": "diesel", "to_node": "fuel_retail_service", "edge_type": "service_flow", "description": "柴油通过零售服务到达终端消费者"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_natgas_to_cng", "from_node": "natural_gas", "to_node": "cng_station", "edge_type": "material_flow", "description": "天然气供应至加气站"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_software_to_fintech", "from_node": "software_development_service", "to_node": "fintech_service", "edge_type": "capability_supply", "description": "软件开发能力支撑金融科技服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_hw_to_atm", "from_node": "it_hardware", "to_node": "atm_machine", "edge_type": "composition", "description": "IT硬件是ATM机的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_software_to_atm", "from_node": "software_license", "to_node": "atm_machine", "edge_type": "composition", "description": "软件是ATM机的核心功能组件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_rail_vehicle_to_transport", "from_node": "rail_vehicle", "to_node": "rail_transport_service", "edge_type": "service_flow", "description": "铁路车辆提供铁路运输服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_warehouse_to_logistics", "from_node": "warehouse_service", "to_node": "logistics_service", "edge_type": "service_flow", "description": "仓储服务是物流服务的重要组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_universal_to_transmission", "from_node": "universal_joint", "to_node": "automotive_transmission_system", "edge_type": "composition", "description": "万向节是汽车传动系统的关键部件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_hub_to_chassis", "from_node": "wheel_hub_unit", "to_node": "chassis_system", "edge_type": "composition", "description": "轮毂单元是汽车底盘系统的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_bearing_to_chassis", "from_node": "bearing", "to_node": "chassis_system", "edge_type": "composition", "description": "轴承是汽车底盘系统的运动支撑部件"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_exhaust_to_env", "from_node": "automotive_exhaust_system", "to_node": "automotive_environment_system", "edge_type": "composition", "description": "排气系统是汽车环境控制系统的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_fuel_tank_to_chassis", "from_node": "fuel_tank", "to_node": "chassis_system", "edge_type": "composition", "description": "燃油箱是汽车底盘系统的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_machinery_part_to_construction", "from_node": "machinery_part", "to_node": "construction_machinery", "edge_type": "composition", "description": "机械零部件是工程机械的组成部分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_dept_store_to_retail", "from_node": "department_store", "to_node": "chain_retail_service", "edge_type": "service_flow", "description": "百货零售是连锁零售服务的重要业态"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_resin_to_paint", "from_node": "synthetic_resin", "to_node": "paint", "edge_type": "material_flow", "description": "合成树脂是油漆的主要成膜物质"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_resin_to_coating", "from_node": "synthetic_resin", "to_node": "coating", "edge_type": "material_flow", "description": "合成树脂是涂料的主要基料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_paint_to_construction", "from_node": "paint", "to_node": "construction_service", "edge_type": "material_flow", "description": "油漆用于建筑施工和装饰"},
]

graph_batch = {
    "batch_id": "batch_014_graph",
    "task_description": "Batch 014 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 014 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "taishan_petroleum", "name_zh": "泰山石油", "aliases": ["中国石化山东泰山石油股份有限公司"], "stock_codes": ["000554.SZ"], "country": "CN", "province": "山东", "city": "泰安市", "employee_count": 1080, "company_type": "public", "description": "成品油批发零售企业，主营汽油、柴油零售及车用天然气加气业务"},
    {"company_id": "shenzhou_information", "name_zh": "神州信息", "aliases": ["神州数码信息服务集团股份有限公司"], "stock_codes": ["000555.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "employee_count": 20726, "company_type": "public", "description": "金融科技企业，主营软件与信息技术服务及ATM产品研发制造"},
    {"company_id": "western_entrepreneurship", "name_zh": "西部创业", "aliases": ["宁夏西部创业实业股份有限公司"], "stock_codes": ["000557.SZ"], "country": "CN", "province": "宁夏", "city": "银川市", "employee_count": 1169, "company_type": "public", "description": "综合运输服务企业，主营铁路运输、仓储物流、葡萄酒酿造及酒店餐饮"},
    {"company_id": "tianfu_culture_tourism", "name_zh": "天府文旅", "aliases": ["成都新天府文化旅游发展股份有限公司"], "stock_codes": ["000558.SZ"], "country": "CN", "province": "四川", "city": "成都市", "employee_count": 372, "company_type": "public", "description": "文旅地产企业，主营房地产开发销售及旅游业务"},
    {"company_id": "wanxiang_qianchao", "name_zh": "万向钱潮", "aliases": ["万向钱潮股份公司"], "stock_codes": ["000559.SZ"], "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 8777, "company_type": "public", "description": "汽车零部件制造企业，主营万向节、轮毂单元、轴承、底盘悬架、制动系统、传动系统和工程机械零部件"},
    {"company_id": "woaiwojia", "name_zh": "我爱我家", "aliases": ["我爱我家控股集团股份有限公司"], "stock_codes": ["000560.SZ"], "country": "CN", "province": "云南", "city": "昆明市", "employee_count": 32659, "company_type": "public", "description": "房产服务企业，主营房地产经纪、住宅资产管理和商业地产运营"},
    {"company_id": "fenghuo_electronics", "name_zh": "烽火电子", "aliases": ["陕西烽火电子股份有限公司"], "stock_codes": ["000561.SZ"], "country": "CN", "province": "陕西", "city": "宝鸡市", "employee_count": 2451, "company_type": "public", "description": "军工通信企业，主营通信设备、电声器材、电线电缆和纺织机械"},
    {"company_id": "shanguotou", "name_zh": "陕国投A", "aliases": ["陕西省国际信托股份有限公司"], "stock_codes": ["000563.SZ"], "country": "CN", "province": "陕西", "city": "西安市", "employee_count": 733, "company_type": "public", "description": "信托公司，主营资金信托、不动产信托及实业投资"},
    {"company_id": "gongxiao_daji", "name_zh": "供销大集", "aliases": ["供销大集集团股份有限公司"], "stock_codes": ["000564.SZ"], "country": "CN", "province": "陕西", "city": "西安市", "employee_count": 1964, "company_type": "public", "description": "商业零售企业，主营百货零售和国内商业"},
    {"company_id": "yusanxia", "name_zh": "渝三峡A", "aliases": ["重庆三峡油漆股份有限公司"], "stock_codes": ["000565.SZ"], "country": "CN", "province": "重庆", "city": "重庆市", "employee_count": 759, "company_type": "public", "description": "涂料制造企业，主营油漆、合成树脂和印铁包装桶"},
]

exposures = [
    {"exposure_id": "taishan_petroleum_operate_gasoline", "company_id": "taishan_petroleum", "node_id": "gasoline", "activity_type": "operate", "role": "汽油零售商", "weight": 0.8},
    {"exposure_id": "taishan_petroleum_operate_diesel", "company_id": "taishan_petroleum", "node_id": "diesel", "activity_type": "operate", "role": "柴油零售商", "weight": 0.7},
    {"exposure_id": "taishan_petroleum_operate_fuel_retail", "company_id": "taishan_petroleum", "node_id": "fuel_retail_service", "activity_type": "operate", "role": "成品油零售服务商", "weight": 0.9},
    {"exposure_id": "taishan_petroleum_operate_natgas", "company_id": "taishan_petroleum", "node_id": "natural_gas", "activity_type": "operate", "role": "车用天然气运营商", "weight": 0.5},
    {"exposure_id": "shenzhou_info_provide_software_dev", "company_id": "shenzhou_information", "node_id": "software_development_service", "activity_type": "provide_service", "role": "软件开发服务商", "weight": 0.8},
    {"exposure_id": "shenzhou_info_provide_fintech", "company_id": "shenzhou_information", "node_id": "fintech_service", "activity_type": "provide_service", "role": "金融科技服务商", "weight": 0.7},
    {"exposure_id": "shenzhou_info_manufacture_atm", "company_id": "shenzhou_information", "node_id": "atm_machine", "activity_type": "manufacture", "role": "ATM机制造商", "weight": 0.6},
    {"exposure_id": "shenzhou_info_provide_sys_integration", "company_id": "shenzhou_information", "node_id": "information_system_integration", "activity_type": "provide_service", "role": "信息系统集成服务商", "weight": 0.7},
    {"exposure_id": "western_entre_operate_rail_transport", "company_id": "western_entrepreneurship", "node_id": "rail_transport_service", "activity_type": "operate", "role": "铁路运输运营商", "weight": 0.7},
    {"exposure_id": "western_entre_operate_warehouse", "company_id": "western_entrepreneurship", "node_id": "warehouse_service", "activity_type": "operate", "role": "仓储服务商", "weight": 0.5},
    {"exposure_id": "western_entre_operate_logistics", "company_id": "western_entrepreneurship", "node_id": "logistics_service", "activity_type": "operate", "role": "物流服务商", "weight": 0.5},
    {"exposure_id": "western_entre_manufacture_wine", "company_id": "western_entrepreneurship", "node_id": "wine", "activity_type": "manufacture", "role": "葡萄酒酿造商", "weight": 0.3},
    {"exposure_id": "western_entre_operate_hotel", "company_id": "western_entrepreneurship", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.3},
    {"exposure_id": "western_entre_operate_catering", "company_id": "western_entrepreneurship", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.2},
    {"exposure_id": "tianfu_operate_real_estate", "company_id": "tianfu_culture_tourism", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.7},
    {"exposure_id": "tianfu_operate_tourism", "company_id": "tianfu_culture_tourism", "node_id": "tourism_service", "activity_type": "operate", "role": "旅游服务商", "weight": 0.5},
    {"exposure_id": "wanxiang_manufacture_universal_joint", "company_id": "wanxiang_qianchao", "node_id": "universal_joint", "activity_type": "manufacture", "role": "万向节制造商", "weight": 0.8},
    {"exposure_id": "wanxiang_manufacture_wheel_hub", "company_id": "wanxiang_qianchao", "node_id": "wheel_hub_unit", "activity_type": "manufacture", "role": "轮毂单元制造商", "weight": 0.7},
    {"exposure_id": "wanxiang_manufacture_bearing", "company_id": "wanxiang_qianchao", "node_id": "bearing", "activity_type": "manufacture", "role": "轴承制造商", "weight": 0.7},
    {"exposure_id": "wanxiang_manufacture_chassis", "company_id": "wanxiang_qianchao", "node_id": "chassis_system", "activity_type": "manufacture", "role": "汽车底盘系统制造商", "weight": 0.6},
    {"exposure_id": "wanxiang_manufacture_suspension", "company_id": "wanxiang_qianchao", "node_id": "suspension_system", "activity_type": "manufacture", "role": "悬架系统制造商", "weight": 0.6},
    {"exposure_id": "wanxiang_manufacture_transmission", "company_id": "wanxiang_qianchao", "node_id": "automotive_transmission_system", "activity_type": "manufacture", "role": "传动系统制造商", "weight": 0.6},
    {"exposure_id": "wanxiang_manufacture_brake", "company_id": "wanxiang_qianchao", "node_id": "automotive_brake_system", "activity_type": "manufacture", "role": "制动系统制造商", "weight": 0.6},
    {"exposure_id": "wanxiang_manufacture_exhaust", "company_id": "wanxiang_qianchao", "node_id": "automotive_exhaust_system", "activity_type": "manufacture", "role": "排气系统制造商", "weight": 0.5},
    {"exposure_id": "wanxiang_manufacture_fuel_tank", "company_id": "wanxiang_qianchao", "node_id": "fuel_tank", "activity_type": "manufacture", "role": "燃油箱制造商", "weight": 0.5},
    {"exposure_id": "wanxiang_manufacture_machinery_part", "company_id": "wanxiang_qianchao", "node_id": "machinery_part", "activity_type": "manufacture", "role": "工程机械零部件制造商", "weight": 0.5},
    {"exposure_id": "woaiwojia_operate_agency", "company_id": "woaiwojia", "node_id": "real_estate_agency_service", "activity_type": "operate", "role": "房地产经纪服务商", "weight": 0.9},
    {"exposure_id": "woaiwojia_operate_residential_mgmt", "company_id": "woaiwojia", "node_id": "residential_asset_management", "activity_type": "operate", "role": "住宅资产管理服务商", "weight": 0.7},
    {"exposure_id": "woaiwojia_operate_commercial_prop", "company_id": "woaiwojia", "node_id": "commercial_property_operation", "activity_type": "operate", "role": "商业地产运营商", "weight": 0.5},
    {"exposure_id": "woaiwojia_operate_property_mgmt", "company_id": "woaiwojia", "node_id": "property_management_service", "activity_type": "operate", "role": "物业管理服务商", "weight": 0.5},
    {"exposure_id": "fenghuo_manufacture_comm_equip", "company_id": "fenghuo_electronics", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.8},
    {"exposure_id": "fenghuo_manufacture_electroacoustic", "company_id": "fenghuo_electronics", "node_id": "electroacoustic_device", "activity_type": "manufacture", "role": "电声器材制造商", "weight": 0.6},
    {"exposure_id": "fenghuo_manufacture_wire_cable", "company_id": "fenghuo_electronics", "node_id": "wire_cable", "activity_type": "manufacture", "role": "电线电缆制造商", "weight": 0.6},
    {"exposure_id": "fenghuo_manufacture_textile_mach", "company_id": "fenghuo_electronics", "node_id": "textile_machinery", "activity_type": "manufacture", "role": "纺织机械制造商", "weight": 0.4},
    {"exposure_id": "shanguotou_operate_trust", "company_id": "shanguotou", "node_id": "trust_service", "activity_type": "operate", "role": "信托服务商", "weight": 0.9},
    {"exposure_id": "shanguotou_operate_real_estate", "company_id": "shanguotou", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产及实业投资商", "weight": 0.4},
    {"exposure_id": "gongxiao_operate_dept_store", "company_id": "gongxiao_daji", "node_id": "department_store", "activity_type": "operate", "role": "百货零售商", "weight": 0.8},
    {"exposure_id": "gongxiao_operate_retail", "company_id": "gongxiao_daji", "node_id": "chain_retail_service", "activity_type": "operate", "role": "连锁零售服务商", "weight": 0.7},
    {"exposure_id": "yusanxia_manufacture_paint", "company_id": "yusanxia", "node_id": "paint", "activity_type": "manufacture", "role": "油漆制造商", "weight": 0.8},
    {"exposure_id": "yusanxia_manufacture_coating", "company_id": "yusanxia", "node_id": "coating", "activity_type": "manufacture", "role": "涂料制造商", "weight": 0.7},
    {"exposure_id": "yusanxia_manufacture_resin", "company_id": "yusanxia", "node_id": "synthetic_resin", "activity_type": "manufacture", "role": "合成树脂制造商", "weight": 0.6},
    {"exposure_id": "yusanxia_manufacture_metal_pack", "company_id": "yusanxia", "node_id": "metal_packaging", "activity_type": "manufacture", "role": "印铁包装桶制造商", "weight": 0.4},
]

business_batch = {
    "batch_id": "batch_014_business",
    "task_description": "Batch 014 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 014 ===")
post_business_batch(business_batch)
