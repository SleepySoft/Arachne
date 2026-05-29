#!/usr/bin/env python3
"""Submit batches 061-065 to Arachne API."""
import json, requests
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=60)
    return r.status_code, r.text

def make_evidence(quote, title="tushare"):
    return [{"source_title": title, "quote": quote}]

def load_existing():
    with open("tmp_existing_nodes.json", "r", encoding="utf-8") as f:
        nodes = set(json.load(f))
    with open("tmp_existing_edges.json", "r", encoding="utf-8") as f:
        edges = set(json.load(f))
    return nodes, edges

EXISTING_NODES, EXISTING_EDGES = load_existing()

BATCHES = {}

# =============================================================================
# BATCH 061 (600257-600269)
# =============================================================================
BATCHES["061"] = {
    "new_nodes": [
        {"node_id": "aquatic_product", "canonical_name_zh": "水产品", "definition": "淡水及海水养殖加工销售的水产食品", "entity_type": "material"},
        {"node_id": "hotel", "canonical_name_zh": "酒店服务", "definition": "经济连锁型及中高端酒店的投资与运营管理", "entity_type": "service"},
        {"node_id": "rare_earth_metal", "canonical_name_zh": "稀土金属", "definition": "稀土、钨等稀有金属的采选、冶炼及加工", "entity_type": "material"},
        {"node_id": "tungsten", "canonical_name_zh": "钨", "definition": "钨矿采选及钨制品加工", "entity_type": "material"},
        {"node_id": "lighting_equipment", "canonical_name_zh": "照明设备", "definition": "一体化电子节能灯、荧光灯及配套灯具、特种光源", "entity_type": "device"},
        {"node_id": "mining_truck", "canonical_name_zh": "矿用自卸车", "definition": "非公路自卸汽车及工程机械", "entity_type": "device"},
        {"node_id": "forest_chemical", "canonical_name_zh": "林化产品", "definition": "脂松香、脂松节油等林产化工系列产品", "entity_type": "material"},
        {"node_id": "power_grid_protection", "canonical_name_zh": "电网保护自动化", "definition": "电网保护及自动化系统、电厂保护及自动化系统", "entity_type": "service"},
        {"node_id": "expressway", "canonical_name_zh": "高速公路", "definition": "高速公路的投资、建设、管理、养护及收费运营", "entity_type": "infrastructure"},
    ],
    "new_edges": [
        {"edge_id": "aquatic_product_to_food", "from_node": "aquatic_product", "to_node": "food", "edge_type": "material_flow", "description": "水产品加工为食品"},
        {"edge_id": "forest_chemical_to_timber", "from_node": "forest_chemical", "to_node": "timber", "edge_type": "material_flow", "description": "林化产品与林木资源关联"},
        {"edge_id": "power_grid_protection_to_power_grid", "from_node": "power_grid_protection", "to_node": "power_grid", "edge_type": "capability_supply", "description": "电网保护自动化系统保障电网安全运行"},
    ],
    "companies": [
        {"company_id": "dahu", "name_zh": "大湖健康产业股份有限公司", "stock_codes": ["600257.SH"], "province": "湖南", "city": "常德", "description": "水产品养殖加工销售和中成药生产,医药贸易,白酒类产品营销"},
        {"company_id": "btg_hotels", "name_zh": "北京首旅酒店(集团)股份有限公司", "stock_codes": ["600258.SH"], "province": "北京", "city": "北京", "description": "经济连锁型及中高端酒店的投资与运营管理,景区经营"},
        {"company_id": "chinanonferrous", "name_zh": "中稀有色金属股份有限公司", "stock_codes": ["600259.SH"], "province": "海南", "city": "海口", "description": "稀土,钨的采选,冶炼,加工及销售"},
        {"company_id": "yankon", "name_zh": "浙江阳光照明电器集团股份有限公司", "stock_codes": ["600261.SH"], "province": "浙江", "city": "绍兴", "description": "一体化电子节能灯,T5大功率节能荧光灯及配套灯具,特种光源及灯具"},
        {"company_id": "northhaul", "name_zh": "内蒙古北方重型汽车股份有限公司", "stock_codes": ["600262.SH"], "province": "内蒙古", "city": "包头", "description": "特雷克斯牌非公路自卸汽车和备件,工程机械"},
        {"company_id": "st_jinggu", "name_zh": "云南景谷林业股份有限公司", "stock_codes": ["600265.SH"], "province": "云南", "city": "普洱", "description": "林化产品,林木产品,林板产品"},
        {"company_id": "ucd", "name_zh": "北京城建投资发展股份有限公司", "stock_codes": ["600266.SH"], "province": "北京", "city": "北京", "description": "房地产开发,销售商品房,投资及投资管理"},
        {"company_id": "hisun_pharma", "name_zh": "浙江海正药业股份有限公司", "stock_codes": ["600267.SH"], "province": "浙江", "city": "台州", "description": "抗寄生虫药,抗肿瘤药,心血管药,抗感染药"},
        {"company_id": "guodian_nanz", "name_zh": "国电南京自动化股份有限公司", "stock_codes": ["600268.SH"], "province": "江苏", "city": "南京", "description": "电网保护及自动化类产品,电厂保护及自动化类产品"},
        {"company_id": "ganyue", "name_zh": "江西赣粤高速公路股份有限公司", "stock_codes": ["600269.SH"], "province": "江西", "city": "南昌", "description": "高速公路的管理,养护,收费和投资"},
    ],
    "exposures": [
        ("dahu", "aquatic_product", "produce", "水产品生产商", 0.9),
        ("dahu", "chinese_patent_medicine", "produce", "中成药生产商", 0.8),
        ("dahu", "baijiu", "produce", "白酒生产商", 0.75),
        ("btg_hotels", "hotel", "operate", "酒店运营商", 0.95),
        ("btg_hotels", "tourism_service", "provide_service", "旅游服务商", 0.8),
        ("chinanonferrous", "rare_earth_metal", "produce", "稀土金属生产商", 0.95),
        ("chinanonferrous", "tungsten", "produce", "钨生产商", 0.9),
        ("yankon", "lighting_equipment", "manufacture", "照明设备制造商", 0.95),
        ("yankon", "led_display", "manufacture", "LED显示器件制造商", 0.85),
        ("northhaul", "mining_truck", "manufacture", "矿用自卸车制造商", 0.95),
        ("northhaul", "construction_machinery", "manufacture", "工程机械制造商", 0.85),
        ("st_jinggu", "forest_chemical", "produce", "林化产品生产商", 0.9),
        ("st_jinggu", "timber", "produce", "林木产品生产商", 0.85),
        ("ucd", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("hisun_pharma", "chemical_pharmaceutical", "produce", "化学制药生产商", 0.95),
        ("hisun_pharma", "pharmaceutical", "produce", "药品生产商", 0.9),
        ("guodian_nanz", "power_grid_protection", "provide_service", "电网保护自动化服务商", 0.95),
        ("guodian_nanz", "power_automation", "manufacture", "电力自动化设备制造商", 0.9),
        ("ganyue", "expressway", "operate", "高速公路运营商", 0.95),
        ("ganyue", "toll_road", "operate", "路桥收费运营商", 0.9),
    ],
}

# =============================================================================
# BATCH 062 (600271-600283)
# =============================================================================
BATCHES["062"] = {
    "new_nodes": [
        {"node_id": "private_network_comm", "canonical_name_zh": "专网通信", "definition": "专网通信产品、通信光纤光缆及量子保密通信", "entity_type": "service"},
        {"node_id": "quantum_crypto", "canonical_name_zh": "量子保密通信", "definition": "量子保密通信技术研发及产品", "entity_type": "service"},
        {"node_id": "steam_supply", "canonical_name_zh": "蒸汽供应", "definition": "向工业园区提供蒸汽供热服务", "entity_type": "service"},
        {"node_id": "fatty_alcohol", "canonical_name_zh": "脂肪醇", "definition": "脂肪醇(酸)等精细化工产品", "entity_type": "material"},
        {"node_id": "antitumor_drug", "canonical_name_zh": "抗肿瘤药", "definition": "抗肿瘤药物及制剂的研发、生产与销售", "entity_type": "material"},
        {"node_id": "department_store", "canonical_name_zh": "百货零售", "definition": "百货、食品、针织服装等商品的零售批发", "entity_type": "service"},
        {"node_id": "platinum_mesh", "canonical_name_zh": "铂网", "definition": "氯碱工业用铂网催化剂", "entity_type": "component"},
    ],
    "new_edges": [
        {"edge_id": "private_network_comm_to_optical_fiber", "from_node": "private_network_comm", "to_node": "optical_fiber", "edge_type": "composition", "description": "专网通信系统包含通信光纤光缆组件"},
        {"edge_id": "steam_supply_to_chemical_industry", "from_node": "steam_supply", "to_node": "chemical_industry", "edge_type": "energy_flow", "description": "蒸汽供应为化工生产提供热能"},
        {"edge_id": "antitumor_drug_to_pharmaceutical", "from_node": "antitumor_drug", "to_node": "pharmaceutical", "edge_type": "material_flow", "description": "抗肿瘤药是医药产业的重要细分领域"},
    ],
    "companies": [
        {"company_id": "aisino", "name_zh": "航天信息股份有限公司", "stock_codes": ["600271.SH"], "province": "北京", "city": "北京", "description": "专网通信产品,通信光纤,光缆,通信硅管,量子保密通信"},
        {"company_id": "kaikai", "name_zh": "上海开开实业股份有限公司", "stock_codes": ["600272.SH"], "province": "上海", "city": "上海", "description": "服装生产销售和中医药流通"},
        {"company_id": "jiahua_energy", "name_zh": "浙江嘉化能源化工股份有限公司", "stock_codes": ["600273.SH"], "province": "浙江", "city": "嘉兴", "description": "蒸汽供热,邻对位,氯碱,脂肪醇(酸)等系列产品"},
        {"company_id": "hengrui_pharma", "name_zh": "江苏恒瑞医药股份有限公司", "stock_codes": ["600276.SH"], "province": "江苏", "city": "连云港", "description": "抗肿瘤药,抗感染药"},
        {"company_id": "oricorient", "name_zh": "东方国际创业股份有限公司", "stock_codes": ["600278.SH"], "province": "上海", "city": "上海", "description": "自营业务出口,加工补偿贸易,内销,货运及代理"},
        {"company_id": "chongqing_port", "name_zh": "重庆港股份有限公司", "stock_codes": ["600279.SH"], "province": "重庆", "city": "重庆", "description": "货物装卸,货运代理服务,港口物流"},
        {"company_id": "central_mall", "name_zh": "南京中央商场(集团)股份有限公司", "stock_codes": ["600280.SH"], "province": "江苏", "city": "南京", "description": "百货,食品,针织服装,五金交电化工等商品的零售批发"},
        {"company_id": "huayang_material", "name_zh": "山西华阳新材料股份有限公司", "stock_codes": ["600281.SH"], "province": "山西", "city": "太原", "description": "氯碱系列,聚氯乙烯系列,焦炭及深加工,铂网"},
        {"company_id": "nangang_steel", "name_zh": "南京钢铁股份有限公司", "stock_codes": ["600282.SH"], "province": "江苏", "city": "南京", "description": "宽中厚板(卷),棒材,线材,带钢,型钢等精品中厚板,优特钢长材"},
        {"company_id": "qianjiang_water", "name_zh": "钱江水利开发股份有限公司", "stock_codes": ["600283.SH"], "province": "浙江", "city": "杭州", "description": "水的生产,供应及水力发电"},
    ],
    "exposures": [
        ("aisino", "private_network_comm", "provide_service", "专网通信服务商", 0.95),
        ("aisino", "quantum_crypto", "provide_service", "量子保密通信服务商", 0.85),
        ("aisino", "communication_equipment", "manufacture", "通信设备制造商", 0.8),
        ("kaikai", "garment", "produce", "服装生产商", 0.85),
        ("kaikai", "textile_product", "produce", "纺织品生产商", 0.8),
        ("jiahua_energy", "steam_supply", "provide_service", "蒸汽供热供应商", 0.95),
        ("jiahua_energy", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.9),
        ("jiahua_energy", "fatty_alcohol", "produce", "脂肪醇生产商", 0.85),
        ("hengrui_pharma", "antitumor_drug", "produce", "抗肿瘤药生产商", 0.95),
        ("hengrui_pharma", "pharmaceutical", "produce", "药品生产商", 0.9),
        ("oricorient", "import_export_trade", "provide_service", "进出口贸易服务商", 0.9),
        ("oricorient", "textile_product", "procure", "纺织品贸易商", 0.85),
        ("chongqing_port", "port_logistics", "operate", "港口物流运营商", 0.95),
        ("chongqing_port", "logistics_service", "provide_service", "综合物流服务商", 0.85),
        ("central_mall", "department_store", "operate", "百货零售运营商", 0.95),
        ("central_mall", "retail_channel", "operate", "零售渠道运营商", 0.85),
        ("huayang_material", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.9),
        ("huayang_material", "pvc", "produce", "聚氯乙烯生产商", 0.85),
        ("huayang_material", "platinum_mesh", "manufacture", "铂网制造商", 0.8),
        ("nangang_steel", "steel_plate", "produce", "钢铁板材生产商", 0.95),
        ("nangang_steel", "special_steel", "produce", "特种钢生产商", 0.9),
        ("qianjiang_water", "water_supply", "provide_service", "供水服务商", 0.95),
        ("qianjiang_water", "hydro_power", "operate", "水力发电运营商", 0.85),
    ],
}

# =============================================================================
# BATCH 063 (600284-600299)
# =============================================================================
BATCHES["063"] = {
    "new_nodes": [
        {"node_id": "municipal_engineering", "canonical_name_zh": "市政工程", "definition": "市政基础工程、道路公路桥梁及各类基础工程施工", "entity_type": "service"},
        {"node_id": "asphalt", "canonical_name_zh": "沥青", "definition": "沥青路面摊铺及沥青砼销售", "entity_type": "material"},
        {"node_id": "chinese_medicine_plaster", "canonical_name_zh": "中药膏剂", "definition": "中药橡胶膏剂、颗粒剂、酊剂、片剂、胶囊剂", "entity_type": "material"},
        {"node_id": "optomechatronics", "canonical_name_zh": "光机电一体化", "definition": "光学、激光、红外元器件及设备,信息技术及办公自动化产品", "entity_type": "service"},
        {"node_id": "information_security", "canonical_name_zh": "信息安全", "definition": "网络信息安全应用软件及信息安全整体解决方案", "entity_type": "service"},
        {"node_id": "float_glass", "canonical_name_zh": "浮法玻璃", "definition": "浮法玻璃及移动互联网终端业务", "entity_type": "material"},
        {"node_id": "cashmere_product", "canonical_name_zh": "羊绒制品", "definition": "无毛绒、羊绒纱、羊绒衫等羊绒制品", "entity_type": "material"},
        {"node_id": "yeast", "canonical_name_zh": "酵母", "definition": "酵母及深加工产品、烘焙原料、食品添加剂", "entity_type": "material"},
        {"node_id": "nutritional_additive", "canonical_name_zh": "营养添加剂", "definition": "饲料营养添加剂及有机硅等化工产品", "entity_type": "material"},
        {"node_id": "silicone", "canonical_name_zh": "有机硅", "definition": "有机硅、双酚A、环氧树脂等化工新材料", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "asphalt_to_road", "from_node": "asphalt", "to_node": "road", "edge_type": "composition", "description": "沥青是道路铺设的主要材料"},
        {"edge_id": "yeast_to_food", "from_node": "yeast", "to_node": "food", "edge_type": "material_flow", "description": "酵母是食品加工的重要原料"},
        {"edge_id": "silicone_to_electronic_material", "from_node": "silicone", "to_node": "electronic_material", "edge_type": "material_flow", "description": "有机硅是电子材料的重要组成部分"},
    ],
    "companies": [
        {"company_id": "pudong_construction", "name_zh": "上海浦东建设股份有限公司", "stock_codes": ["600284.SH"], "province": "上海", "city": "上海", "description": "市政基础工程,沥青路面摊铺,沥青砼销售,建筑材料销售"},
        {"company_id": "lingrui_pharma", "name_zh": "河南羚锐制药股份有限公司", "stock_codes": ["600285.SH"], "province": "河南", "city": "信阳", "description": "中药橡胶膏剂,颗粒剂,酊剂,片剂,胶囊剂的生产和销售"},
        {"company_id": "suhao_fashion", "name_zh": "江苏苏豪时尚集团股份有限公司", "stock_codes": ["600287.SH"], "province": "江苏", "city": "南京", "description": "商品流通,服装加工,化工仓储及现代金融服务业投资"},
        {"company_id": "daheng_tech", "name_zh": "大恒新纪元科技股份有限公司", "stock_codes": ["600288.SH"], "province": "北京", "city": "北京", "description": "光机电一体化产品,信息技术及办公自动化产品,半导体元器件"},
        {"company_id": "st_eastcom", "name_zh": "亿阳信通股份有限公司", "stock_codes": ["600289.SH"], "province": "黑龙江", "city": "哈尔滨", "description": "通信网络业务支撑系统,网络信息安全应用软件研发"},
        {"company_id": "spic_hydro", "name_zh": "国家电投集团水电股份有限公司", "stock_codes": ["600292.SH"], "province": "重庆", "city": "重庆", "description": "发电业务,环保业务,大气污染治理,水环境污染防治"},
        {"company_id": "sanxia_newmat", "name_zh": "湖北三峡新型建材股份有限公司", "stock_codes": ["600293.SH"], "province": "湖北", "city": "宜昌", "description": "浮法玻璃,移动互联网终端业务"},
        {"company_id": "erdos", "name_zh": "内蒙古鄂尔多斯资源股份有限公司", "stock_codes": ["600295.SH"], "province": "内蒙古", "city": "鄂尔多斯", "description": "四季服装,纱线,面料,电力冶金化工产品"},
        {"company_id": "angelyeast", "name_zh": "安琪酵母股份有限公司", "stock_codes": ["600298.SH"], "province": "湖北", "city": "宜昌", "description": "酵母及深加工产品,保健食品,烘焙原料,食品添加剂"},
        {"company_id": "adisseo", "name_zh": "蓝星安迪苏股份有限公司", "stock_codes": ["600299.SH"], "province": "北京", "city": "北京", "description": "有机硅,双酚A,环氧树脂类,PBT树脂系列,苯酚丙酮,营养添加剂"},
    ],
    "exposures": [
        ("pudong_construction", "municipal_engineering", "provide_service", "市政工程承包商", 0.95),
        ("pudong_construction", "asphalt", "produce", "沥青生产商", 0.85),
        ("pudong_construction", "construction_engineering", "provide_service", "建筑工程承包商", 0.9),
        ("lingrui_pharma", "chinese_medicine_plaster", "produce", "中药膏剂生产商", 0.95),
        ("lingrui_pharma", "chinese_patent_medicine", "produce", "中成药生产商", 0.9),
        ("suhao_fashion", "commodity_circulation", "provide_service", "商品流通服务商", 0.85),
        ("suhao_fashion", "garment", "produce", "服装生产商", 0.8),
        ("daheng_tech", "optomechatronics", "provide_service", "光机电一体化服务商", 0.85),
        ("daheng_tech", "optoelectronic_device", "manufacture", "光电子器件制造商", 0.8),
        ("st_eastcom", "information_security", "provide_service", "信息安全服务商", 0.9),
        ("st_eastcom", "communication_network_support", "provide_service", "通信网络支撑服务商", 0.85),
        ("spic_hydro", "power_generation", "operate", "发电业务运营商", 0.95),
        ("spic_hydro", "environmental_service", "provide_service", "环保服务提供商", 0.85),
        ("sanxia_newmat", "float_glass", "produce", "浮法玻璃生产商", 0.95),
        ("sanxia_newmat", "glass", "produce", "玻璃生产商", 0.85),
        ("erdos", "cashmere_product", "produce", "羊绒制品生产商", 0.95),
        ("erdos", "textile_product", "produce", "纺织品生产商", 0.85),
        ("erdos", "power_generation", "operate", "电力运营商", 0.8),
        ("angelyeast", "yeast", "produce", "酵母生产商", 0.95),
        ("angelyeast", "food_additive", "produce", "食品添加剂生产商", 0.9),
        ("adisseo", "nutritional_additive", "produce", "营养添加剂生产商", 0.9),
        ("adisseo", "silicone", "produce", "有机硅生产商", 0.85),
        ("adisseo", "chemical_product", "produce", "化工产品生产商", 0.8),
    ],
}

# =============================================================================
# BATCH 064 (600300-600312)
# =============================================================================
BATCHES["064"] = {
    "new_nodes": [
        {"node_id": "soy_milk_powder", "canonical_name_zh": "豆奶粉", "definition": "豆奶粉、炼乳等植物蛋白饮料及食品", "entity_type": "material"},
        {"node_id": "nonferrous_metal_mining", "canonical_name_zh": "有色金属采选", "definition": "有色金属矿采选与冶炼", "entity_type": "service"},
        {"node_id": "industrial_sewing_machine", "canonical_name_zh": "工业缝纫机", "definition": "全系列工业缝纫机和自动缝制单元", "entity_type": "device"},
        {"node_id": "vehicle_axle", "canonical_name_zh": "车桥", "definition": "汽车车桥及汽车零部件", "entity_type": "component"},
        {"node_id": "special_vehicle", "canonical_name_zh": "专用车", "definition": "客车、专用车及特种车辆", "entity_type": "system"},
        {"node_id": "vinegar", "canonical_name_zh": "食醋", "definition": "食醋、酱油、酱菜等调味品", "entity_type": "material"},
        {"node_id": "soy_sauce", "canonical_name_zh": "酱油", "definition": "酿造酱油及复合调味料", "entity_type": "material"},
        {"node_id": "carbon_steel", "canonical_name_zh": "碳钢", "definition": "碳钢线材、棒材、中厚板、热轧板、冷轧薄板", "entity_type": "material"},
        {"node_id": "stainless_steel", "canonical_name_zh": "不锈钢", "definition": "不锈钢热轧及冷轧板材", "entity_type": "material"},
        {"node_id": "newsprint", "canonical_name_zh": "新闻纸", "definition": "中高档新闻纸、文化纸及纸制品", "entity_type": "material"},
        {"node_id": "mdi", "canonical_name_zh": "MDI", "definition": "纯MDI、聚合MDI等聚氨酯原料", "entity_type": "material"},
        {"node_id": "high_voltage_switchgear", "canonical_name_zh": "高压开关设备", "definition": "高压、超高压、特高压开关设备及控制设备", "entity_type": "device"},
    ],
    "new_edges": [
        {"edge_id": "vinegar_to_food", "from_node": "vinegar", "to_node": "food", "edge_type": "material_flow", "description": "食醋是食品加工的重要调味品"},
        {"edge_id": "carbon_steel_to_construction", "from_node": "carbon_steel", "to_node": "construction_material", "edge_type": "material_flow", "description": "碳钢是建筑用钢材的重要品种"},
        {"edge_id": "mdi_to_polyurethane", "from_node": "mdi", "to_node": "polyurethane", "edge_type": "material_flow", "description": "MDI是生产聚氨酯的核心原料"},
    ],
    "companies": [
        {"company_id": "vivi", "name_zh": "维维食品饮料股份有限公司", "stock_codes": ["600300.SH"], "province": "江苏", "city": "徐州", "description": "豆奶粉,炼乳,植物蛋白饮料及食品"},
        {"company_id": "huaxi_nonferrous", "name_zh": "广西华锡有色金属股份有限公司", "stock_codes": ["600301.SH"], "province": "广西", "city": "南宁", "description": "有色金属矿采选与冶炼"},
        {"company_id": "st_standard", "name_zh": "西安标准工业股份有限公司", "stock_codes": ["600302.SH"], "province": "陕西", "city": "西安", "description": "全系列工业缝纫机和自动缝制单元"},
        {"company_id": "sg_auto", "name_zh": "辽宁曙光汽车集团股份有限公司", "stock_codes": ["600303.SH"], "province": "辽宁", "city": "丹东", "description": "车桥,黄海客车,曙光专用车,汽车零部件"},
        {"company_id": "hengshun", "name_zh": "江苏恒顺醋业股份有限公司", "stock_codes": ["600305.SH"], "province": "江苏", "city": "镇江", "description": "醋,酱油,酱菜,复合调味料等调味品"},
        {"company_id": "jiugang", "name_zh": "甘肃酒钢集团宏兴钢铁股份有限公司", "stock_codes": ["600307.SH"], "province": "甘肃", "city": "嘉峪关", "description": "碳钢及不锈钢线材,棒材,中厚板,热轧板,冷轧薄板"},
        {"company_id": "huatai_paper", "name_zh": "山东华泰纸业股份有限公司", "stock_codes": ["600308.SH"], "province": "山东", "city": "东营", "description": "中高档新闻纸,文化纸及相关化工产品"},
        {"company_id": "wanhua_chem", "name_zh": "万华化学集团股份有限公司", "stock_codes": ["600309.SH"], "province": "山东", "city": "烟台", "description": "纯MDI,聚合MDI,化工产品,新材料"},
        {"company_id": "guangxi_energy", "name_zh": "广西能源股份有限公司", "stock_codes": ["600310.SH"], "province": "广西", "city": "贺州", "description": "发电,供电,电力投资开发"},
        {"company_id": "pinggao_elec", "name_zh": "河南平高电气股份有限公司", "stock_codes": ["600312.SH"], "province": "河南", "city": "平顶山", "description": "高压,超高压,特高压开关设备,控制设备及其配件"},
    ],
    "exposures": [
        ("vivi", "soy_milk_powder", "produce", "豆奶粉生产商", 0.95),
        ("vivi", "beverage", "produce", "饮料生产商", 0.85),
        ("vivi", "food", "produce", "食品生产商", 0.8),
        ("huaxi_nonferrous", "nonferrous_metal_mining", "operate", "有色金属采选运营商", 0.95),
        ("huaxi_nonferrous", "rare_earth_metal", "produce", "稀有金属生产商", 0.85),
        ("st_standard", "industrial_sewing_machine", "manufacture", "工业缝纫机制造商", 0.95),
        ("st_standard", "textile_machinery", "manufacture", "纺织机械制造商", 0.9),
        ("sg_auto", "vehicle_axle", "manufacture", "车桥制造商", 0.9),
        ("sg_auto", "bus", "manufacture", "客车制造商", 0.85),
        ("sg_auto", "special_vehicle", "manufacture", "专用车制造商", 0.8),
        ("sg_auto", "automobile_part", "manufacture", "汽车零部件制造商", 0.85),
        ("hengshun", "vinegar", "produce", "食醋生产商", 0.95),
        ("hengshun", "soy_sauce", "produce", "酱油生产商", 0.9),
        ("hengshun", "food", "produce", "食品生产商", 0.8),
        ("jiugang", "carbon_steel", "produce", "碳钢生产商", 0.95),
        ("jiugang", "stainless_steel", "produce", "不锈钢生产商", 0.9),
        ("jiugang", "steel_plate", "produce", "钢铁板材生产商", 0.85),
        ("huatai_paper", "newsprint", "produce", "新闻纸生产商", 0.95),
        ("huatai_paper", "cultural_paper", "produce", "文化纸生产商", 0.9),
        ("huatai_paper", "paper", "produce", "纸制品生产商", 0.85),
        ("wanhua_chem", "mdi", "produce", "MDI生产商", 0.95),
        ("wanhua_chem", "chemical_product", "produce", "化工产品生产商", 0.9),
        ("wanhua_chem", "polyurethane", "produce", "聚氨酯生产商", 0.9),
        ("guangxi_energy", "power_generation", "operate", "发电业务运营商", 0.95),
        ("guangxi_energy", "hydro_power", "operate", "水力发电运营商", 0.85),
        ("pinggao_elec", "high_voltage_switchgear", "manufacture", "高压开关设备制造商", 0.95),
        ("pinggao_elec", "switchgear", "manufacture", "开关设备制造商", 0.9),
        ("pinggao_elec", "power_distribution_equipment", "manufacture", "配电设备制造商", 0.85),
    ],
}

# =============================================================================
# BATCH 065 (600313-600326)
# =============================================================================
BATCHES["065"] = {
    "new_nodes": [
        {"node_id": "seed", "canonical_name_zh": "种子", "definition": "高粱、玉米等农作物种子的生产、加工、销售", "entity_type": "material"},
        {"node_id": "agricultural_material", "canonical_name_zh": "农资", "definition": "化肥、农药等农业生产资料贸易", "entity_type": "service"},
        {"node_id": "daily_chemical_product", "canonical_name_zh": "日用化学品", "definition": "化妆品、洗漱用品、清洁用品等日化产品", "entity_type": "material"},
        {"node_id": "trainer_aircraft", "canonical_name_zh": "教练机", "definition": "教练机、通用飞机等航空飞行器的研发、制造", "entity_type": "system"},
        {"node_id": "general_aviation", "canonical_name_zh": "通用航空", "definition": "通用航空服务及航空产品销售维修", "entity_type": "service"},
        {"node_id": "financial_service", "canonical_name_zh": "金融服务", "definition": "小额贷款、融资租赁等金融服务", "entity_type": "service"},
        {"node_id": "cpe", "canonical_name_zh": "氯化聚乙烯", "definition": "氯化聚乙烯、聚氯乙烯、烧碱等氯碱化工产品", "entity_type": "material"},
        {"node_id": "caustic_soda", "canonical_name_zh": "烧碱", "definition": "氢氧化钠等烧碱产品", "entity_type": "material"},
        {"node_id": "port_crane", "canonical_name_zh": "港口起重机", "definition": "集装箱起重机、散货机械等大型港口装卸设备", "entity_type": "device"},
        {"node_id": "offshore_equipment", "canonical_name_zh": "海洋工程装备", "definition": "海上重型装备、海洋工程装备及钢结构", "entity_type": "system"},
        {"node_id": "solid_waste_treatment", "canonical_name_zh": "固废处理", "definition": "城市生活垃圾、餐厨垃圾、危险废物处理及发电", "entity_type": "service"},
        {"node_id": "road_engineering", "canonical_name_zh": "公路工程", "definition": "公路工程施工及基础设施建设", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "seed_to_agricultural_product", "from_node": "seed", "to_node": "agricultural_product", "edge_type": "material_flow", "description": "种子是农业生产的基础原料"},
        {"edge_id": "trainer_aircraft_to_aviation", "from_node": "trainer_aircraft", "to_node": "air_transport", "edge_type": "capability_supply", "description": "教练机为航空运输培养飞行员提供能力支撑"},
        {"edge_id": "port_crane_to_port_logistics", "from_node": "port_crane", "to_node": "port_logistics", "edge_type": "capability_supply", "description": "港口起重机为港口物流提供装卸能力"},
    ],
    "companies": [
        {"company_id": "cn_agriseed", "name_zh": "中农发种业集团股份有限公司", "stock_codes": ["600313.SH"], "province": "北京", "city": "北京", "description": "种业及农资贸易,高粱种子,玉米种子,化肥,农药"},
        {"company_id": "jahwa", "name_zh": "上海家化联合股份有限公司", "stock_codes": ["600315.SH"], "province": "上海", "city": "上海", "description": "化妆品,中药饮片,日用化学制品及原辅材料"},
        {"company_id": "hongdu_aviation", "name_zh": "江西洪都航空工业股份有限公司", "stock_codes": ["600316.SH"], "province": "江西", "city": "南昌", "description": "教练机,通用飞机,其他航空产品及零件部件的设计,研制,生产,销售"},
        {"company_id": "xinli_finance", "name_zh": "安徽新力金融股份有限公司", "stock_codes": ["600318.SH"], "province": "安徽", "city": "合肥", "description": "水泥产品,商品熟料,金融服务"},
        {"company_id": "yaxing_chem", "name_zh": "潍坊亚星化学股份有限公司", "stock_codes": ["600319.SH"], "province": "山东", "city": "潍坊", "description": "氯化聚乙烯,聚氯乙烯,烧碱,液氯"},
        {"company_id": "zpmc", "name_zh": "上海振华重工(集团)股份有限公司", "stock_codes": ["600320.SH"], "province": "上海", "city": "上海", "description": "集装箱起重机,散货机械,海上重型装备,海洋工程装备"},
        {"company_id": "tianjin_ucd", "name_zh": "天津津投城市开发股份有限公司", "stock_codes": ["600322.SH"], "province": "天津", "city": "天津", "description": "房地产开发经营,商品房销售,房屋租赁"},
        {"company_id": "hanlan", "name_zh": "瀚蓝环境股份有限公司", "stock_codes": ["600323.SH"], "province": "广东", "city": "佛山", "description": "自来水生产和供应,污水处理,固废处理,燃气经营"},
        {"company_id": "huafa", "name_zh": "珠海华发实业股份有限公司", "stock_codes": ["600325.SH"], "province": "广东", "city": "珠海", "description": "住宅,车库及商铺等房地产开发经营"},
        {"company_id": "tibet_road", "name_zh": "西藏天路股份有限公司", "stock_codes": ["600326.SH"], "province": "西藏", "city": "拉萨", "description": "公路工程施工,水泥生产,基础设施建设"},
    ],
    "exposures": [
        ("cn_agriseed", "seed", "produce", "种子生产商", 0.95),
        ("cn_agriseed", "agricultural_material", "provide_service", "农资供应商", 0.9),
        ("cn_agriseed", "agricultural_product", "produce", "农产品生产商", 0.85),
        ("jahwa", "daily_chemical_product", "produce", "日用化学品生产商", 0.95),
        ("jahwa", "cosmetics", "produce", "化妆品生产商", 0.9),
        ("jahwa", "toothpaste", "produce", "牙膏生产商", 0.85),
        ("hongdu_aviation", "trainer_aircraft", "manufacture", "教练机制造商", 0.95),
        ("hongdu_aviation", "general_aviation", "provide_service", "通用航空服务商", 0.85),
        ("hongdu_aviation", "defense_equipment", "manufacture", "防务装备制造商", 0.8),
        ("xinli_finance", "cement", "produce", "水泥生产商", 0.85),
        ("xinli_finance", "financial_service", "provide_service", "金融服务商", 0.8),
        ("yaxing_chem", "cpe", "produce", "氯化聚乙烯生产商", 0.95),
        ("yaxing_chem", "pvc", "produce", "聚氯乙烯生产商", 0.9),
        ("yaxing_chem", "caustic_soda", "produce", "烧碱生产商", 0.9),
        ("yaxing_chem", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.85),
        ("zpmc", "port_crane", "manufacture", "港口起重机制造商", 0.95),
        ("zpmc", "offshore_equipment", "manufacture", "海洋工程装备制造商", 0.9),
        ("zpmc", "construction_machinery", "manufacture", "工程机械制造商", 0.85),
        ("tianjin_ucd", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("hanlan", "water_supply", "provide_service", "供水服务商", 0.95),
        ("hanlan", "sewage_treatment", "provide_service", "污水处理服务商", 0.9),
        ("hanlan", "solid_waste_treatment", "provide_service", "固废处理服务商", 0.9),
        ("hanlan", "power_generation", "operate", "发电运营商", 0.85),
        ("huafa", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("tibet_road", "road_engineering", "provide_service", "公路工程承包商", 0.95),
        ("tibet_road", "cement", "produce", "水泥生产商", 0.85),
        ("tibet_road", "construction_engineering", "provide_service", "建筑工程承包商", 0.8),
    ],
}


# =============================================================================
# SUBMISSION LOGIC
# =============================================================================

def submit_batch(batch_num, data):
    print(f"\n{'='*60}")
    print(f"Batch {batch_num} Submission")
    print(f"{'='*60}")

    nodes_to_upsert = []
    for n in data["new_nodes"]:
        if n["node_id"] not in EXISTING_NODES:
            nodes_to_upsert.append({
                "node_id": n["node_id"],
                "canonical_name_zh": n["canonical_name_zh"],
                "definition": n["definition"],
                "entity_type": n["entity_type"],
                "confidence": "HIGH",
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch {batch_num}: {n['canonical_name_zh']}"),
            })

    edges_to_upsert = []
    for e in data["new_edges"]:
        if e["edge_id"] not in EXISTING_EDGES:
            edges_to_upsert.append({
                "edge_id": e["edge_id"],
                "from_node": e["from_node"],
                "to_node": e["to_node"],
                "edge_namespace": "industrial_flow",
                "edge_type": e["edge_type"],
                "description": e["description"],
                "confidence": "MEDIUM",
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch {batch_num}: {e['description']}"),
            })

    graph_batch = {
        "batch_id": f"batch_{batch_num}",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

    print(f"Graph batch: {len(nodes_to_upsert)} new nodes, {len(edges_to_upsert)} new edges")
    if nodes_to_upsert or edges_to_upsert:
        status, text = api_post("batches", graph_batch)
        print(f"  Response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {text[:500]}")
            return False
    else:
        print("  Nothing new to submit")

    companies_to_upsert = []
    for c in data["companies"]:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "stock_codes": c["stock_codes"],
            "country": "CN",
            "province": c["province"],
            "city": c["city"],
            "description": c["description"],
            "company_type": "public",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare: {c['description']}"),
        })

    exposures_to_upsert = []
    for company_id, node_id, activity, role, weight in data["exposures"]:
        exposure_id = f"{company_id}_{activity}_{node_id}"
        exposures_to_upsert.append({
            "exposure_id": exposure_id,
            "company_id": company_id,
            "node_id": node_id,
            "activity_type": activity,
            "role": role,
            "weight": weight,
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch {batch_num}: {company_id} -> {node_id}"),
        })

    biz_batch = {
        "batch_id": f"batch_{batch_num}",
        "task_description": f"Batch {batch_num} companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

    print(f"Business batch: {len(companies_to_upsert)} companies, {len(exposures_to_upsert)} exposures")
    status, text = api_post("business-batches", biz_batch)
    print(f"  Response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {text[:500]}")
        return False

    return True


if __name__ == "__main__":
    results = {}
    for num in ["061", "062", "063", "064", "065"]:
        ok = submit_batch(num, BATCHES[num])
        results[num] = ok

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for num, ok in results.items():
        print(f"  Batch {num}: {'OK' if ok else 'FAILED'}")
