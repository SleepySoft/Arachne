#!/usr/bin/env python3
"""Submit batches 056-060 to Arachne API."""
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
# BATCH 056 (600189-600201)
# =============================================================================
BATCHES["056"] = {
    "new_nodes": [
        {"node_id": "mineral_water", "canonical_name_zh": "天然矿泉水", "definition": "长白山等水源地生产的天然饮用矿泉水", "entity_type": "material"},
        {"node_id": "timber", "canonical_name_zh": "木材", "definition": "原木、人造板及木材加工产品", "entity_type": "material"},
        {"node_id": "landscape_service", "canonical_name_zh": "园林景观服务", "definition": "园林规划设计、工程施工及苗木种植销售", "entity_type": "service"},
        {"node_id": "sugar", "canonical_name_zh": "食糖", "definition": "甘蔗或甜菜加工制成的白砂糖及糖制品", "entity_type": "material"},
        {"node_id": "switchgear", "canonical_name_zh": "开关设备", "definition": "中高压开关设备及配电电器元件", "entity_type": "device"},
        {"node_id": "large_motor", "canonical_name_zh": "大中型电机", "definition": "工业用大中型电动机及发电设备", "entity_type": "device"},
        {"node_id": "decoration_engineering", "canonical_name_zh": "装饰工程", "definition": "主题乐园、酒店及住宅的室内装修总承包", "entity_type": "service"},
        {"node_id": "veterinary_medicine", "canonical_name_zh": "兽药", "definition": "兽用生物制品及化学药品", "entity_type": "material"},
        {"node_id": "animal_feed", "canonical_name_zh": "饲料", "definition": "畜牧及水产养殖用配合饲料及饲料添加剂", "entity_type": "material"},
        {"node_id": "diagnostic_product", "canonical_name_zh": "诊断产品", "definition": "医学诊断试剂及设备", "entity_type": "device"},
        {"node_id": "baijiu", "canonical_name_zh": "白酒", "definition": "以高粱等粮食为原料蒸馏酿造的烈性酒", "entity_type": "material"},
        {"node_id": "communication_chip", "canonical_name_zh": "通信芯片", "definition": "可信识别芯片、汽车电子芯片及融合通信芯片", "entity_type": "component"},
        {"node_id": "veterinary_biological", "canonical_name_zh": "兽用生物制品", "definition": "动物用疫苗及生物药品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "sugar_to_food", "from_node": "sugar", "to_node": "food", "edge_type": "material_flow", "description": "食糖作为原料用于食品加工"},
        {"edge_id": "animal_feed_to_meat_product", "from_node": "animal_feed", "to_node": "meat_product", "edge_type": "material_flow", "description": "饲料用于畜禽养殖生产肉制品"},
        {"edge_id": "timber_to_furniture", "from_node": "timber", "to_node": "furniture", "edge_type": "material_flow", "description": "木材加工成家具产品"},
    ],
    "companies": [
        {"company_id": "quanyangquan", "name_zh": "吉林泉阳泉股份有限公司", "stock_codes": ["600189.SH"], "province": "吉林", "city": "长春", "description": "木材产品,进口木材贸易,定制家居,长白山天然饮用矿泉水,园林景观"},
        {"company_id": "huazi_industry", "name_zh": "包头华资实业股份有限公司", "stock_codes": ["600191.SH"], "province": "内蒙古", "city": "包头", "description": "糖及其副产品,电子信息产品"},
        {"company_id": "greatwall_elec", "name_zh": "兰州长城电工股份有限公司", "stock_codes": ["600192.SH"], "province": "甘肃", "city": "兰州", "description": "中高压开关设备,大中型电机及发电设备,工业控制及配电电器元件"},
        {"company_id": "st_chuangxing", "name_zh": "上海创兴资源开发股份有限公司", "stock_codes": ["600193.SH"], "province": "上海", "city": "上海", "description": "主题乐园场馆,高端酒店及住宅的工程施工总承包,室内装修总承包"},
        {"company_id": "cahic", "name_zh": "中牧实业股份有限公司", "stock_codes": ["600195.SH"], "province": "北京", "city": "北京", "description": "生物制品,饲料,兽药的生产与销售"},
        {"company_id": "fosun_pharma", "name_zh": "上海复星医药(集团)股份有限公司", "stock_codes": ["600196.SH"], "province": "上海", "city": "上海", "description": "诊断产品,药品零售,药品批发,齿科治疗设备"},
        {"company_id": "yilite", "name_zh": "新疆伊力特实业股份有限公司", "stock_codes": ["600197.SH"], "province": "新疆", "city": "可克达拉", "description": "白酒生产研发及销售,火力发电及供应"},
        {"company_id": "datang_telecom", "name_zh": "大唐电信科技股份有限公司", "stock_codes": ["600198.SH"], "province": "北京", "city": "北京", "description": "可信识别芯片,汽车电子芯片,融合通信芯片等集成电路设计"},
        {"company_id": "jinzhongzi", "name_zh": "安徽金种子酒业股份有限公司", "stock_codes": ["600199.SH"], "province": "安徽", "city": "阜阳", "description": "白酒生产与销售"},
        {"company_id": "jinyu_bio", "name_zh": "金宇生物技术股份有限公司", "stock_codes": ["600201.SH"], "province": "内蒙古", "city": "呼和浩特", "description": "兽用生物药品制造和销售,兽用化学药品制剂"},
    ],
    "exposures": [
        ("quanyangquan", "mineral_water", "produce", "天然矿泉水生产商", 0.9),
        ("quanyangquan", "timber", "produce", "木材生产商", 0.8),
        ("quanyangquan", "landscape_service", "provide_service", "园林景观服务商", 0.75),
        ("quanyangquan", "furniture", "produce", "定制家居生产商", 0.75),
        ("huazi_industry", "sugar", "produce", "食糖生产商", 0.9),
        ("huazi_industry", "food", "produce", "食品生产商", 0.8),
        ("greatwall_elec", "switchgear", "manufacture", "开关设备制造商", 0.95),
        ("greatwall_elec", "large_motor", "manufacture", "大中型电机制造商", 0.9),
        ("greatwall_elec", "power_distribution_equipment", "manufacture", "配电设备制造商", 0.85),
        ("st_chuangxing", "decoration_engineering", "provide_service", "装饰工程承包商", 0.9),
        ("cahic", "veterinary_medicine", "produce", "兽药生产商", 0.95),
        ("cahic", "animal_feed", "produce", "饲料生产商", 0.9),
        ("fosun_pharma", "pharmaceutical", "produce", "药品生产商", 0.95),
        ("fosun_pharma", "diagnostic_product", "manufacture", "诊断产品制造商", 0.85),
        ("yilite", "baijiu", "produce", "白酒生产商", 0.95),
        ("datang_telecom", "communication_chip", "manufacture", "通信芯片制造商", 0.9),
        ("datang_telecom", "integrated_circuit", "manufacture", "集成电路制造商", 0.85),
        ("jinzhongzi", "baijiu", "produce", "白酒生产商", 0.95),
        ("jinyu_bio", "veterinary_biological", "produce", "兽用生物制品生产商", 0.95),
        ("jinyu_bio", "veterinary_medicine", "produce", "兽药生产商", 0.9),
    ],
}

# =============================================================================
# BATCH 057 (600202-600216)
# =============================================================================
BATCHES["057"] = {
    "new_nodes": [
        {"node_id": "air_cooling_equipment", "canonical_name_zh": "空冷设备", "definition": "石化空冷器、电站空冷器及核电站空气处理机组", "entity_type": "device"},
        {"node_id": "led_display", "canonical_name_zh": "LED显示器件", "definition": "发光二极管、显示器件及照明灯具", "entity_type": "component"},
        {"node_id": "semiconductor_material", "canonical_name_zh": "半导体材料", "definition": "超高纯金属、稀贵金属及微电子光电子用薄膜材料", "entity_type": "material"},
        {"node_id": "rare_earth_functional", "canonical_name_zh": "稀土功能材料", "definition": "高端稀土功能材料及光电材料", "entity_type": "material"},
        {"node_id": "pv_glass", "canonical_name_zh": "光伏玻璃", "definition": "太阳能电池用光伏玻璃及浮法玻璃", "entity_type": "material"},
        {"node_id": "natural_gas_supply", "canonical_name_zh": "天然气供应", "definition": "天然气管道运输及销售", "entity_type": "service"},
        {"node_id": "packaging_material", "canonical_name_zh": "包装材料", "definition": "PET瓶及瓶坯、瓶盖、标签等容器包装", "entity_type": "material"},
        {"node_id": "tibetan_medicine", "canonical_name_zh": "藏药", "definition": "诺迪康胶囊等藏药产品的研发、生产与销售", "entity_type": "material"},
        {"node_id": "charging_pile", "canonical_name_zh": "充电桩", "definition": "电动汽车充电桩及充电基础设施", "entity_type": "device"},
        {"node_id": "industrial_automation", "canonical_name_zh": "工业自动化", "definition": "工业自动控制系统、智能控制系统及工业机器人", "entity_type": "service"},
        {"node_id": "vitamin_e", "canonical_name_zh": "维生素E", "definition": "合成VE油及胶丸剂等维生素系列产品", "entity_type": "material"},
        {"node_id": "chemical_pharmaceutical", "canonical_name_zh": "化学制药", "definition": "化学原料药及制剂的研发、生产与销售", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "semiconductor_material_to_chip", "from_node": "semiconductor_material", "to_node": "integrated_circuit", "edge_type": "material_flow", "description": "半导体材料用于制造集成电路芯片"},
        {"edge_id": "pv_glass_to_solar_panel", "from_node": "pv_glass", "to_node": "solar_panel", "edge_type": "composition", "description": "光伏玻璃是太阳能电池板的重要组成部分"},
        {"edge_id": "charging_pile_to_new_energy_vehicle", "from_node": "charging_pile", "to_node": "new_energy_vehicle", "edge_type": "capability_supply", "description": "充电桩为新能源汽车提供能源补给能力"},
    ],
    "companies": [
        {"company_id": "harbin_aircon", "name_zh": "哈尔滨空调股份有限公司", "stock_codes": ["600202.SH"], "province": "黑龙江", "city": "哈尔滨", "description": "石化空冷器,电站空冷器,核电站空气处理机组"},
        {"company_id": "furi_elec", "name_zh": "福建福日电子股份有限公司", "stock_codes": ["600203.SH"], "province": "福建", "city": "福州", "description": "LED及工业节能,节能家电及通讯产品"},
        {"company_id": "grimn_advanced", "name_zh": "有研新材料股份有限公司", "stock_codes": ["600206.SH"], "province": "北京", "city": "北京", "description": "半导体材料,稀土材料,光电材料和高纯金属材料"},
        {"company_id": "ancai_hitech", "name_zh": "河南安彩高科股份有限公司", "stock_codes": ["600207.SH"], "province": "河南", "city": "安阳", "description": "天然气,管道运输,光伏玻璃,浮法玻璃"},
        {"company_id": "quzhou_dev", "name_zh": "衢州信安发展股份有限公司", "stock_codes": ["600208.SH"], "province": "浙江", "city": "衢州", "description": "地产开发,煤炭销售,实业投资"},
        {"company_id": "zijiang", "name_zh": "上海紫江企业集团股份有限公司", "stock_codes": ["600210.SH"], "province": "上海", "city": "上海", "description": "PET瓶及瓶坯,皇冠盖,标签,塑料防盗盖,纸包装印刷"},
        {"company_id": "tibet_rhodiola", "name_zh": "西藏诺迪康药业股份有限公司", "stock_codes": ["600211.SH"], "province": "西藏", "city": "拉萨", "description": "诺迪康胶囊,诺迪康颗粒,藏药产品"},
        {"company_id": "lvenergy", "name_zh": "绿能慧充数字能源技术股份有限公司", "stock_codes": ["600212.SH"], "province": "山东", "city": "临沂", "description": "输配电及控制设备,充电桩,储能技术服务"},
        {"company_id": "paslin", "name_zh": "派斯林数字科技股份有限公司", "stock_codes": ["600215.SH"], "province": "吉林", "city": "长春", "description": "工业自动控制系统,智能控制系统,工业机器人"},
        {"company_id": "zhejiang_pharma", "name_zh": "浙江医药股份有限公司", "stock_codes": ["600216.SH"], "province": "浙江", "city": "绍兴", "description": "合成VE油及胶丸剂,来立信系列,天然VE原料及制剂"},
    ],
    "exposures": [
        ("harbin_aircon", "air_cooling_equipment", "manufacture", "空冷设备制造商", 0.95),
        ("harbin_aircon", "air_conditioner", "manufacture", "空调设备制造商", 0.85),
        ("furi_elec", "led_display", "manufacture", "LED显示器件制造商", 0.9),
        ("furi_elec", "display_device", "manufacture", "显示器件制造商", 0.85),
        ("grimn_advanced", "semiconductor_material", "produce", "半导体材料生产商", 0.95),
        ("grimn_advanced", "rare_earth_functional", "produce", "稀土功能材料生产商", 0.9),
        ("ancai_hitech", "pv_glass", "produce", "光伏玻璃生产商", 0.9),
        ("ancai_hitech", "natural_gas_supply", "provide_service", "天然气供应商", 0.85),
        ("quzhou_dev", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("zijiang", "packaging_material", "produce", "包装材料生产商", 0.95),
        ("zijiang", "pet_bottle", "produce", "PET瓶生产商", 0.9),
        ("tibet_rhodiola", "tibetan_medicine", "produce", "藏药生产商", 0.95),
        ("tibet_rhodiola", "chinese_patent_medicine", "produce", "中成药生产商", 0.85),
        ("lvenergy", "charging_pile", "manufacture", "充电桩制造商", 0.9),
        ("lvenergy", "energy_storage", "provide_service", "储能技术服务商", 0.85),
        ("paslin", "industrial_automation", "provide_service", "工业自动化服务商", 0.9),
        ("paslin", "industrial_robot", "manufacture", "工业机器人制造商", 0.85),
        ("zhejiang_pharma", "chemical_pharmaceutical", "produce", "化学制药生产商", 0.95),
        ("zhejiang_pharma", "vitamin_e", "produce", "维生素E生产商", 0.9),
    ],
}

# =============================================================================
# BATCH 058 (600217-600229)
# =============================================================================
BATCHES["058"] = {
    "new_nodes": [
        {"node_id": "e_waste_recycling", "canonical_name_zh": "电子废弃物回收", "definition": "废弃电器电子产品的回收与拆解处理", "entity_type": "service"},
        {"node_id": "diesel_engine", "canonical_name_zh": "柴油发动机", "definition": "内燃机、农业装备及工程机械用柴油机", "entity_type": "component"},
        {"node_id": "aluminum_product", "canonical_name_zh": "铝加工产品", "definition": "氧化铝、电解铝、铝板带箔及挤压型材", "entity_type": "material"},
        {"node_id": "air_transport", "canonical_name_zh": "航空运输", "definition": "国际及国内航空客货邮运输业务", "entity_type": "service"},
        {"node_id": "cosmetics", "canonical_name_zh": "化妆品", "definition": "护肤、彩妆等日化产品的研发、生产与销售", "entity_type": "material"},
        {"node_id": "pesticide", "canonical_name_zh": "农药", "definition": "农药原料药及其制品的生产与销售", "entity_type": "material"},
        {"node_id": "urea", "canonical_name_zh": "尿素", "definition": "氮肥、合成氨等化肥产品", "entity_type": "material"},
        {"node_id": "internet_advertising", "canonical_name_zh": "互联网广告", "definition": "数字营销、广告发布及技术服务", "entity_type": "service"},
        {"node_id": "publishing_media", "canonical_name_zh": "出版传媒", "definition": "图书、期刊、电子音像等出版物的出版发行", "entity_type": "service"},
        {"node_id": "zirconium_product", "canonical_name_zh": "锆系列产品", "definition": "锆化学品及锆制品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "aluminum_product_to_automobile", "from_node": "aluminum_product", "to_node": "automobile", "edge_type": "composition", "description": "铝加工产品用于汽车轻量化零部件"},
        {"edge_id": "diesel_engine_to_agricultural_machinery", "from_node": "diesel_engine", "to_node": "agricultural_machinery", "edge_type": "composition", "description": "柴油发动机是农业机械的核心动力部件"},
        {"edge_id": "urea_to_fertilizer", "from_node": "urea", "to_node": "chemical_fertilizer", "edge_type": "material_flow", "description": "尿素是重要的氮肥原料"},
    ],
    "companies": [
        {"company_id": "zhongzai_zihuan", "name_zh": "中再资源环境股份有限公司", "stock_codes": ["600217.SH"], "province": "陕西", "city": "铜川", "description": "废弃电器电子产品的回收与拆解处理"},
        {"company_id": "quanchai_power", "name_zh": "安徽全柴动力股份有限公司", "stock_codes": ["600218.SH"], "province": "安徽", "city": "滁州", "description": "柴油机,新型化学建材"},
        {"company_id": "nanshan_aluminum", "name_zh": "山东南山铝业股份有限公司", "stock_codes": ["600219.SH"], "province": "山东", "city": "烟台", "description": "铝土矿冶炼,电解铝生产,铝挤压材和铝压延材研发,加工与销售"},
        {"company_id": "hainan_airlines", "name_zh": "海南航空控股股份有限公司", "stock_codes": ["600221.SH"], "province": "海南", "city": "海口", "description": "国际,国内航空客货邮运输业务"},
        {"company_id": "tailong_pharma", "name_zh": "河南太龙药业股份有限公司", "stock_codes": ["600222.SH"], "province": "河南", "city": "郑州", "description": "口服液,输液等药品的生产与销售"},
        {"company_id": "freda", "name_zh": "鲁商福瑞达医药股份有限公司", "stock_codes": ["600223.SH"], "province": "山东", "city": "淄博", "description": "化妆品,生物基材料,医药制造,房地产开发"},
        {"company_id": "hengtong", "name_zh": "浙江亨通控股股份有限公司", "stock_codes": ["600226.SH"], "province": "浙江", "city": "湖州", "description": "农药原料药,兽药,饲料添加剂,锆系列产品"},
        {"company_id": "cht", "name_zh": "贵州赤天化股份有限公司", "stock_codes": ["600227.SH"], "province": "贵州", "city": "贵阳", "description": "尿素和甲醇的生产销售,药品,医疗器械"},
        {"company_id": "st_fanli", "name_zh": "返利网数字科技股份有限公司", "stock_codes": ["600228.SH"], "province": "江西", "city": "赣州", "description": "软件开发,广告发布,互联网销售,数字营销"},
        {"company_id": "city_media", "name_zh": "青岛城市传媒股份有限公司", "stock_codes": ["600229.SH"], "province": "山东", "city": "青岛", "description": "图书,期刊,电子音像等出版物的出版发行"},
    ],
    "exposures": [
        ("zhongzai_zihuan", "e_waste_recycling", "provide_service", "电子废弃物回收服务商", 0.95),
        ("zhongzai_zihuan", "environmental_service", "provide_service", "环保服务提供商", 0.85),
        ("quanchai_power", "diesel_engine", "manufacture", "柴油发动机制造商", 0.95),
        ("quanchai_power", "automobile_part", "manufacture", "汽车零部件制造商", 0.85),
        ("nanshan_aluminum", "aluminum_product", "produce", "铝加工产品生产商", 0.95),
        ("nanshan_aluminum", "aerospace_metal", "produce", "航空航天金属生产商", 0.85),
        ("hainan_airlines", "air_transport", "operate", "航空运输运营商", 0.95),
        ("tailong_pharma", "chinese_patent_medicine", "produce", "中成药生产商", 0.9),
        ("freda", "cosmetics", "produce", "化妆品生产商", 0.85),
        ("freda", "biomaterial", "produce", "生物基材料生产商", 0.8),
        ("freda", "real_estate_development", "operate", "房地产开发运营商", 0.75),
        ("hengtong", "pesticide", "produce", "农药生产商", 0.9),
        ("hengtong", "veterinary_medicine", "produce", "兽药生产商", 0.85),
        ("hengtong", "zirconium_product", "produce", "锆系列产品生产商", 0.8),
        ("cht", "urea", "produce", "尿素生产商", 0.95),
        ("cht", "methanol", "produce", "甲醇生产商", 0.9),
        ("cht", "pharmaceutical", "produce", "药品生产商", 0.75),
        ("st_fanli", "internet_advertising", "provide_service", "互联网广告服务商", 0.9),
        ("city_media", "publishing_media", "provide_service", "出版传媒服务商", 0.95),
    ],
}

# =============================================================================
# BATCH 059 (600230-600239)
# =============================================================================
BATCHES["059"] = {
    "new_nodes": [
        {"node_id": "tdi", "canonical_name_zh": "甲苯二异氰酸酯", "definition": "TDI等聚氨酯原料及化工产品", "entity_type": "material"},
        {"node_id": "textile_machinery", "canonical_name_zh": "纺织机械", "definition": "纺机及配件、塑机及配件", "entity_type": "device"},
        {"node_id": "flax_textile", "canonical_name_zh": "亚麻纺织", "definition": "亚麻纺织品及服装", "entity_type": "material"},
        {"node_id": "express_delivery", "canonical_name_zh": "快递服务", "definition": "国内及国际快递物流服务", "entity_type": "service"},
        {"node_id": "specialty_paper", "canonical_name_zh": "特种纸", "definition": "卷烟纸、电容器纸、描图纸等特种纸", "entity_type": "material"},
        {"node_id": "hydro_power", "canonical_name_zh": "水力发电", "definition": "水电站开发建设和经营", "entity_type": "service"},
        {"node_id": "film_capacitor", "canonical_name_zh": "薄膜电容器", "definition": "薄膜电容器及其薄膜材料的研发、生产和销售", "entity_type": "component"},
        {"node_id": "liquor", "canonical_name_zh": "酒类", "definition": "保健酒、椰汁等特色酒类及饮料", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "tdi_to_polyurethane", "from_node": "tdi", "to_node": "polyurethane", "edge_type": "material_flow", "description": "TDI是生产聚氨酯的重要原料"},
        {"edge_id": "textile_machinery_to_textile_product", "from_node": "textile_machinery", "to_node": "textile_product", "edge_type": "capability_supply", "description": "纺织机械为纺织品生产提供制造能力"},
        {"edge_id": "hydro_power_to_power_grid", "from_node": "hydro_power", "to_node": "power_grid", "edge_type": "energy_flow", "description": "水力发电向电网输送电力"},
    ],
    "companies": [
        {"company_id": "czdahua", "name_zh": "沧州大化股份有限公司", "stock_codes": ["600230.SH"], "province": "河北", "city": "沧州", "description": "尿素,TDI等化工产品的生产与销售"},
        {"company_id": "lingang", "name_zh": "凌源钢铁股份有限公司", "stock_codes": ["600231.SH"], "province": "辽宁", "city": "朝阳", "description": "热轧中宽带钢,螺纹钢,圆钢,焊接钢管"},
        {"company_id": "jinying", "name_zh": "浙江金鹰股份有限公司", "stock_codes": ["600232.SH"], "province": "浙江", "city": "舟山", "description": "纺机及配件,塑机及配件,绢纺织品,亚麻纺织品,服装"},
        {"company_id": "yto_express", "name_zh": "圆通速递股份有限公司", "stock_codes": ["600233.SH"], "province": "辽宁", "city": "大连", "description": "国内,国际快递,道路航空水路国际货物运输代理"},
        {"company_id": "kexin", "name_zh": "山西科新发展股份有限公司", "stock_codes": ["600234.SH"], "province": "山西", "city": "太原", "description": "自有房屋租赁,高端红酒贸易"},
        {"company_id": "minfeng_paper", "name_zh": "民丰特种纸股份有限公司", "stock_codes": ["600235.SH"], "province": "浙江", "city": "嘉兴", "description": "卷烟纸系列,工业配套用纸,描图纸,电容器纸"},
        {"company_id": "guiguan_power", "name_zh": "广西桂冠电力股份有限公司", "stock_codes": ["600236.SH"], "province": "广西", "city": "南宁", "description": "水力发电,输变电工程"},
        {"company_id": "tongfeng_elec", "name_zh": "安徽铜峰电子股份有限公司", "stock_codes": ["600237.SH"], "province": "安徽", "city": "铜陵", "description": "薄膜电容器及其薄膜材料的研发,生产和销售"},
        {"company_id": "st_yedao", "name_zh": "海南椰岛(集团)股份有限公司", "stock_codes": ["600238.SH"], "province": "海南", "city": "海口", "description": "酒类,贸易,特色食品饮料,房地产开发"},
        {"company_id": "st_yuncheng", "name_zh": "云南城投置业股份有限公司", "stock_codes": ["600239.SH"], "province": "云南", "city": "昆明", "description": "房地产开发经营"},
    ],
    "exposures": [
        ("czdahua", "tdi", "produce", "TDI生产商", 0.95),
        ("czdahua", "urea", "produce", "尿素生产商", 0.9),
        ("lingang", "steel_plate", "produce", "钢铁板材生产商", 0.95),
        ("lingang", "special_steel", "produce", "特种钢生产商", 0.85),
        ("jinying", "textile_machinery", "manufacture", "纺织机械制造商", 0.9),
        ("jinying", "flax_textile", "produce", "亚麻纺织品生产商", 0.85),
        ("jinying", "textile_product", "produce", "纺织品生产商", 0.8),
        ("yto_express", "express_delivery", "provide_service", "快递服务提供商", 0.95),
        ("yto_express", "logistics_service", "provide_service", "综合物流服务商", 0.9),
        ("kexin", "wine", "procure", "红酒贸易商", 0.8),
        ("minfeng_paper", "specialty_paper", "produce", "特种纸生产商", 0.95),
        ("guiguan_power", "hydro_power", "operate", "水力发电运营商", 0.95),
        ("guiguan_power", "power_generation", "operate", "电力运营商", 0.9),
        ("tongfeng_elec", "film_capacitor", "manufacture", "薄膜电容器制造商", 0.95),
        ("tongfeng_elec", "electronic_component", "manufacture", "电子元器件制造商", 0.85),
        ("st_yedao", "liquor", "produce", "酒类生产商", 0.9),
        ("st_yedao", "real_estate_development", "operate", "房地产开发运营商", 0.75),
        ("st_yuncheng", "real_estate_development", "operate", "房地产开发运营商", 0.95),
    ],
}

# =============================================================================
# BATCH 060 (600241-600256)
# =============================================================================
BATCHES["060"] = {
    "new_nodes": [
        {"node_id": "new_energy_battery", "canonical_name_zh": "新能源电池", "definition": "锂离子电池等新能源动力电池制造", "entity_type": "component"},
        {"node_id": "machine_tool", "canonical_name_zh": "机床设备", "definition": "重型机床、加工中心、数控铣床等金属切削设备", "entity_type": "device"},
        {"node_id": "elevator_parts", "canonical_name_zh": "电梯配件", "definition": "电梯齿轮箱等电梯零部件", "entity_type": "component"},
        {"node_id": "toothpaste", "canonical_name_zh": "牙膏", "definition": "牙膏、牙刷等口腔护理产品", "entity_type": "material"},
        {"node_id": "daily_chemical", "canonical_name_zh": "日用化工", "definition": "香皂、洗衣粉、洗发露等日化产品", "entity_type": "material"},
        {"node_id": "commerce_tourism", "canonical_name_zh": "商贸旅游", "definition": "纺织品进出口、商贸代理及旅游服务", "entity_type": "service"},
        {"node_id": "cotton_product", "canonical_name_zh": "棉花及棉制品", "definition": "皮棉、棉纱及棉制品加工销售", "entity_type": "material"},
        {"node_id": "fruit_vegetable_product", "canonical_name_zh": "果蔬制品", "definition": "果蔬制品、番茄浓缩酱等农产品加工", "entity_type": "material"},
        {"node_id": "copper_alloy", "canonical_name_zh": "铜合金材料", "definition": "高精度铜带材、铜合金线材及铜加工产品", "entity_type": "material"},
        {"node_id": "lng", "canonical_name_zh": "液化天然气", "definition": "液化天然气生产、储运及销售", "entity_type": "material"},
        {"node_id": "petroleum_exploration", "canonical_name_zh": "石油勘探开采", "definition": "石油、天然气的勘探开采及技术服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "new_energy_battery_to_electric_vehicle", "from_node": "new_energy_battery", "to_node": "new_energy_vehicle", "edge_type": "composition", "description": "新能源电池是电动汽车的核心部件"},
        {"edge_id": "copper_alloy_to_electronic_component", "from_node": "copper_alloy", "to_node": "electronic_component", "edge_type": "material_flow", "description": "铜合金材料用于制造电子元器件"},
        {"edge_id": "lng_to_natural_gas_supply", "from_node": "lng", "to_node": "natural_gas_supply", "edge_type": "material_flow", "description": "液化天然气经气化后进入天然气供应网络"},
    ],
    "companies": [
        {"company_id": "sdwh", "name_zh": "辽宁时代万恒股份有限公司", "stock_codes": ["600241.SH"], "province": "辽宁", "city": "大连", "description": "林业资源开发,新能源电池制造"},
        {"company_id": "st_haihua", "name_zh": "青海华鼎实业股份有限公司", "stock_codes": ["600243.SH"], "province": "青海", "city": "西宁", "description": "重型机床,加工中心,数控铣床,食品机械,电梯配件,齿轮箱"},
        {"company_id": "vantone", "name_zh": "北京万通新发展集团股份有限公司", "stock_codes": ["600246.SH"], "province": "北京", "city": "北京", "description": "房地产开发,销售商品房,停车场建设及经营管理"},
        {"company_id": "shaanxi_const", "name_zh": "陕西建工集团股份有限公司", "stock_codes": ["600248.SH"], "province": "陕西", "city": "西安", "description": "石油化工安装,房屋建筑,市政基础设施工程总承包"},
        {"company_id": "lmz", "name_zh": "柳州两面针股份有限公司", "stock_codes": ["600249.SH"], "province": "广西", "city": "柳州", "description": "牙膏,香皂,洗衣粉,洗发露,卫生巾等日化产品"},
        {"company_id": "nj_commerce", "name_zh": "南京商贸旅游股份有限公司", "stock_codes": ["600250.SH"], "province": "江苏", "city": "南京", "description": "纺织面料及辅料,服装,纺织原料进出口,旅游业务"},
        {"company_id": "guannong", "name_zh": "新疆冠农股份有限公司", "stock_codes": ["600251.SH"], "province": "新疆", "city": "铁门关", "description": "果蔬制品,皮棉,白砂糖,棉花,番茄浓缩酱加工销售"},
        {"company_id": "zhongheng", "name_zh": "广西梧州中恒集团股份有限公司", "stock_codes": ["600252.SH"], "province": "广西", "city": "梧州", "description": "医药制造,食品生产,房地产开发"},
        {"company_id": "xinke_material", "name_zh": "安徽鑫科新材料股份有限公司", "stock_codes": ["600255.SH"], "province": "安徽", "city": "芜湖", "description": "高精度铜带材,铜合金线材,辐照交联电缆,特种电缆"},
        {"company_id": "guanghui_energy", "name_zh": "广汇能源股份有限公司", "stock_codes": ["600256.SH"], "province": "新疆", "city": "乌鲁木齐", "description": "液化天然气,石油,天然气,煤炭,煤化工"},
    ],
    "exposures": [
        ("sdwh", "new_energy_battery", "manufacture", "新能源电池制造商", 0.95),
        ("sdwh", "timber", "produce", "木材生产商", 0.8),
        ("st_haihua", "machine_tool", "manufacture", "机床设备制造商", 0.9),
        ("st_haihua", "elevator_parts", "manufacture", "电梯配件制造商", 0.85),
        ("st_haihua", "gearbox", "manufacture", "齿轮箱制造商", 0.8),
        ("vantone", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("shaanxi_const", "construction_engineering", "provide_service", "建筑工程承包商", 0.95),
        ("shaanxi_const", "petrochemical_installation", "provide_service", "石油化工安装承包商", 0.9),
        ("lmz", "toothpaste", "produce", "牙膏生产商", 0.95),
        ("lmz", "daily_chemical", "produce", "日用化工产品生产商", 0.9),
        ("nj_commerce", "commerce_tourism", "provide_service", "商贸旅游服务商", 0.85),
        ("nj_commerce", "textile_product", "procure", "纺织品贸易商", 0.8),
        ("guannong", "fruit_vegetable_product", "produce", "果蔬制品生产商", 0.9),
        ("guannong", "cotton_product", "produce", "棉花及棉制品生产商", 0.9),
        ("guannong", "sugar", "produce", "食糖生产商", 0.85),
        ("guannong", "tomato_product", "produce", "番茄制品生产商", 0.85),
        ("zhongheng", "pharmaceutical", "produce", "药品生产商", 0.9),
        ("zhongheng", "chinese_patent_medicine", "produce", "中成药生产商", 0.85),
        ("zhongheng", "real_estate_development", "operate", "房地产开发运营商", 0.8),
        ("xinke_material", "copper_alloy", "produce", "铜合金材料生产商", 0.95),
        ("xinke_material", "special_cable", "produce", "特种电缆生产商", 0.85),
        ("guanghui_energy", "lng", "produce", "液化天然气生产商", 0.95),
        ("guanghui_energy", "coal", "produce", "煤炭生产商", 0.95),
        ("guanghui_energy", "petroleum_exploration", "operate", "石油勘探开采运营商", 0.9),
        ("guanghui_energy", "natural_gas_supply", "provide_service", "天然气供应商", 0.85),
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
    for num in ["056", "057", "058", "059", "060"]:
        ok = submit_batch(num, BATCHES[num])
        results[num] = ok

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for num, ok in results.items():
        print(f"  Batch {num}: {'OK' if ok else 'FAILED'}")
