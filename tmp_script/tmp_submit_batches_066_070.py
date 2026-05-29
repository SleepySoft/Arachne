#!/usr/bin/env python3
"""Submit batches 066-070 to Arachne API."""
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
# BATCH 066 (600327-600337)
# =============================================================================
BATCHES["066"] = {
    "new_nodes": [
        {"node_id": "salt", "canonical_name_zh": "食盐", "definition": "食用盐及盐化工产品", "entity_type": "material"},
        {"node_id": "sodium_metal", "canonical_name_zh": "金属钠", "definition": "金属钠及钠化工产品", "entity_type": "material"},
        {"node_id": "liquid_chlorine", "canonical_name_zh": "液氯", "definition": "液氯等氯碱化工产品", "entity_type": "material"},
        {"node_id": "magnetic_material", "canonical_name_zh": "磁性材料", "definition": "软磁、永磁等磁性材料及磁电子器件", "entity_type": "material"},
        {"node_id": "zinc_product", "canonical_name_zh": "锌产品", "definition": "锌锭、锌合金、锌精矿等锌冶炼加工产品", "entity_type": "material"},
        {"node_id": "herbal_tea", "canonical_name_zh": "凉茶", "definition": "王老吉等植物饮料及凉茶产品", "entity_type": "material"},
        {"node_id": "natural_gas_supply", "canonical_name_zh": "天然气供应", "definition": "天然气、混合燃气、焦炉煤气的生产与销售", "entity_type": "service"},
        {"node_id": "coke", "canonical_name_zh": "焦炭", "definition": "冶金焦炭及煤焦油产品", "entity_type": "material"},
        {"node_id": "refrigerator", "canonical_name_zh": "冰箱冷柜", "definition": "家用及商用冰箱、冰柜、展示柜等制冷设备", "entity_type": "device"},
        {"node_id": "furniture", "canonical_name_zh": "家具", "definition": "餐桌、餐椅、茶几、橱柜等家居家具", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "salt_to_food", "from_node": "salt", "to_node": "food", "edge_type": "material_flow", "description": "食盐是食品加工的基础调味品"},
        {"edge_id": "zinc_product_to_galvanized_steel", "from_node": "zinc_product", "to_node": "steel_plate", "edge_type": "material_flow", "description": "锌用于钢铁镀锌防腐"},
        {"edge_id": "natural_gas_supply_to_heating", "from_node": "natural_gas_supply", "to_node": "heating_supply", "edge_type": "energy_flow", "description": "天然气为供热系统提供燃料"},
    ],
    "companies": [
        {"company_id": "da_orient", "name_zh": "无锡商业大厦大东方股份有限公司", "stock_codes": ["600327.SH"], "province": "江苏", "city": "无锡", "description": "百货零售,汽车零售,超市,餐饮服务"},
        {"company_id": "cnsalt_chem", "name_zh": "中盐内蒙古化工股份有限公司", "stock_codes": ["600328.SH"], "province": "内蒙古", "city": "阿拉善盟", "description": "盐,金属钠,液氯,ADC发泡剂"},
        {"company_id": "dartong", "name_zh": "津药达仁堂集团股份有限公司", "stock_codes": ["600329.SH"], "province": "天津", "city": "天津", "description": "速效救心丸,牛黄降压丸,藿香正气软胶囊等中成药"},
        {"company_id": "tdg", "name_zh": "天通控股股份有限公司", "stock_codes": ["600330.SH"], "province": "浙江", "city": "嘉兴", "description": "磁性材料,电子表面贴装产品,通信设备终端"},
        {"company_id": "hongda", "name_zh": "四川宏达股份有限公司", "stock_codes": ["600331.SH"], "province": "四川", "city": "德阳", "description": "锌锭,锌合金,锌精矿,铅精矿以及磷酸盐系列产品,复合肥"},
        {"company_id": "baiyunshan", "name_zh": "广州白云山医药集团股份有限公司", "stock_codes": ["600332.SH"], "province": "广东", "city": "广州", "description": "消渴丸,夏桑菊,乌鸡白凤丸,华佗再造丸,头孢硫脒,王老吉凉茶"},
        {"company_id": "ccgas", "name_zh": "长春燃气股份有限公司", "stock_codes": ["600333.SH"], "province": "吉林", "city": "长春", "description": "天然气,混合燃气,焦炉煤气,冶金焦炭,煤焦油"},
        {"company_id": "sinomach_auto", "name_zh": "国机汽车股份有限公司", "stock_codes": ["600335.SH"], "province": "天津", "city": "天津", "description": "汽车贸易综合服务"},
        {"company_id": "aucma", "name_zh": "澳柯玛股份有限公司", "stock_codes": ["600336.SH"], "province": "山东", "city": "青岛", "description": "冰柜,冰箱,展示柜,空调器,自动售货机,锂离子电池"},
        {"company_id": "st_markor", "name_zh": "美克国际家居用品股份有限公司", "stock_codes": ["600337.SH"], "province": "江西", "city": "赣州", "description": "餐桌,餐椅,茶几,橱柜等家具"},
    ],
    "exposures": [
        ("da_orient", "department_store", "operate", "百货零售运营商", 0.9),
        ("da_orient", "auto_retail", "operate", "汽车零售运营商", 0.85),
        ("da_orient", "supermarket", "operate", "超市运营商", 0.8),
        ("cnsalt_chem", "salt", "produce", "食盐生产商", 0.95),
        ("cnsalt_chem", "sodium_metal", "produce", "金属钠生产商", 0.9),
        ("cnsalt_chem", "liquid_chlorine", "produce", "液氯生产商", 0.85),
        ("cnsalt_chem", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.8),
        ("dartong", "chinese_patent_medicine", "produce", "中成药生产商", 0.95),
        ("tdg", "magnetic_material", "produce", "磁性材料生产商", 0.95),
        ("tdg", "communication_equipment", "manufacture", "通信设备制造商", 0.85),
        ("hongda", "zinc_product", "produce", "锌产品生产商", 0.95),
        ("hongda", "phosphorus_chemical", "produce", "磷化工产品生产商", 0.9),
        ("baiyunshan", "pharmaceutical", "produce", "药品生产商", 0.95),
        ("baiyunshan", "herbal_tea", "produce", "凉茶生产商", 0.85),
        ("baiyunshan", "chinese_patent_medicine", "produce", "中成药生产商", 0.9),
        ("ccgas", "natural_gas_supply", "provide_service", "天然气供应商", 0.95),
        ("ccgas", "coke", "produce", "焦炭生产商", 0.85),
        ("ccgas", "heating_supply", "provide_service", "供热供应商", 0.8),
        ("sinomach_auto", "auto_trade", "provide_service", "汽车贸易服务商", 0.95),
        ("aucma", "refrigerator", "manufacture", "冰箱冷柜制造商", 0.95),
        ("aucma", "air_conditioner", "manufacture", "空调器制造商", 0.85),
        ("aucma", "lithium_battery", "manufacture", "锂电池制造商", 0.8),
        ("st_markor", "furniture", "produce", "家具生产商", 0.95),
        ("st_markor", "home_decoration", "provide_service", "家居装饰服务商", 0.8),
    ],
}

# =============================================================================
# BATCH 067 (600338-600352)
# =============================================================================
BATCHES["067"] = {
    "new_nodes": [
        {"node_id": "lead_zinc", "canonical_name_zh": "铅锌", "definition": "铅锌矿采选及铅锌冶炼加工", "entity_type": "material"},
        {"node_id": "petroleum_engineering", "canonical_name_zh": "石油工程", "definition": "石油工程设计、施工及工程总承包服务", "entity_type": "service"},
        {"node_id": "industrial_park", "canonical_name_zh": "产业园区", "definition": "产业新城、产业小镇等产业园区开发运营", "entity_type": "infrastructure"},
        {"node_id": "gas_meter", "canonical_name_zh": "燃气表", "definition": "智能燃气表及计量设备", "entity_type": "device"},
        {"node_id": "pump", "canonical_name_zh": "泵", "definition": "泵及泵系统、液力传动产品", "entity_type": "device"},
        {"node_id": "smart_terminal", "canonical_name_zh": "智能终端", "definition": "北斗定位终端、视频监控终端、移动通信终端", "entity_type": "device"},
        {"node_id": "pta", "canonical_name_zh": "PTA", "definition": "精对苯二甲酸等石化中间体", "entity_type": "material"},
        {"node_id": "polyester_filament", "canonical_name_zh": "涤纶长丝", "definition": "民用涤纶长丝、工业涤纶长丝及聚酯切片", "entity_type": "material"},
        {"node_id": "dye", "canonical_name_zh": "染料", "definition": "分散染料、活性染料、酸性染料及化工中间体", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "lead_zinc_to_battery", "from_node": "lead_zinc", "to_node": "battery", "edge_type": "material_flow", "description": "铅锌用于制造蓄电池"},
        {"edge_id": "pta_to_polyester_filament", "from_node": "pta", "to_node": "polyester_filament", "edge_type": "material_flow", "description": "PTA是生产涤纶长丝的主要原料"},
        {"edge_id": "pump_to_hydraulic_system", "from_node": "pump", "to_node": "hydraulic_system", "edge_type": "composition", "description": "泵是液压系统的核心组件"},
    ],
    "companies": [
        {"company_id": "tibet_summit", "name_zh": "西藏珠峰资源股份有限公司", "stock_codes": ["600338.SH"], "province": "西藏", "city": "拉萨", "description": "矿产资源的勘察,采矿,选矿,冶炼及其产品的销售"},
        {"company_id": "cnpc_eng", "name_zh": "中国石油集团工程股份有限公司", "stock_codes": ["600339.SH"], "province": "新疆", "city": "克拉玛依", "description": "工程总承包服务,工程项目管理,工程勘察设计"},
        {"company_id": "st_chinafortune", "name_zh": "华夏幸福基业股份有限公司", "stock_codes": ["600340.SH"], "province": "河北", "city": "廊坊", "description": "产业园区开发和房地产开发,产业新城和产业小镇"},
        {"company_id": "aeropower", "name_zh": "陕西航天动力高科技股份有限公司", "stock_codes": ["600343.SH"], "province": "陕西", "city": "西安", "description": "智能燃气表,泵及泵系统,液力传动产品,电机"},
        {"company_id": "yangtze_com", "name_zh": "武汉长江通信产业集团股份有限公司", "stock_codes": ["600345.SH"], "province": "湖北", "city": "武汉", "description": "智能化终端,管理平台和信息化应用软件,信息电子配件"},
        {"company_id": "hengli_petro", "name_zh": "恒力石化股份有限公司", "stock_codes": ["600346.SH"], "province": "辽宁", "city": "大连", "description": "PTA,聚酯切片,民用涤纶长丝,工业涤纶长丝,聚酯薄膜,工程塑料"},
        {"company_id": "huayang", "name_zh": "山西华阳集团新能股份有限公司", "stock_codes": ["600348.SH"], "province": "山西", "city": "阳泉", "description": "洗块煤,洗粉煤,洗末煤,煤泥,供热"},
        {"company_id": "sd_expressway", "name_zh": "山东高速股份有限公司", "stock_codes": ["600350.SH"], "province": "山东", "city": "济南", "description": "高速公路的投资,管理,养护,收费"},
        {"company_id": "yabao_pharma", "name_zh": "亚宝药业集团股份有限公司", "stock_codes": ["600351.SH"], "province": "山西", "city": "运城", "description": "丁桂儿脐贴,曲克芦丁片等中成药"},
        {"company_id": "longsheng", "name_zh": "浙江龙盛集团股份有限公司", "stock_codes": ["600352.SH"], "province": "浙江", "city": "绍兴", "description": "分散染料,活性染料,酸性染料,化工中间体及染料助剂"},
    ],
    "exposures": [
        ("tibet_summit", "lead_zinc", "produce", "铅锌生产商", 0.95),
        ("tibet_summit", "mineral_mining", "operate", "矿产开采运营商", 0.9),
        ("cnpc_eng", "petroleum_engineering", "provide_service", "石油工程承包商", 0.95),
        ("cnpc_eng", "construction_engineering", "provide_service", "建筑工程承包商", 0.85),
        ("st_chinafortune", "industrial_park", "operate", "产业园区运营商", 0.9),
        ("st_chinafortune", "real_estate_development", "operate", "房地产开发运营商", 0.85),
        ("aeropower", "gas_meter", "manufacture", "燃气表制造商", 0.9),
        ("aeropower", "pump", "manufacture", "泵制造商", 0.9),
        ("aeropower", "hydraulic_system", "manufacture", "液压系统制造商", 0.85),
        ("yangtze_com", "smart_terminal", "manufacture", "智能终端制造商", 0.9),
        ("yangtze_com", "communication_equipment", "manufacture", "通信设备制造商", 0.85),
        ("hengli_petro", "pta", "produce", "PTA生产商", 0.95),
        ("hengli_petro", "polyester_filament", "produce", "涤纶长丝生产商", 0.95),
        ("hengli_petro", "chemical_product", "produce", "化工产品生产商", 0.9),
        ("huayang", "coal", "produce", "煤炭生产商", 0.95),
        ("huayang", "power_generation", "operate", "发电运营商", 0.85),
        ("sd_expressway", "expressway", "operate", "高速公路运营商", 0.95),
        ("sd_expressway", "toll_road", "operate", "路桥收费运营商", 0.9),
        ("yabao_pharma", "chinese_patent_medicine", "produce", "中成药生产商", 0.95),
        ("longsheng", "dye", "produce", "染料生产商", 0.95),
        ("longsheng", "chemical_intermediate", "produce", "化工中间体生产商", 0.85),
    ],
}

# =============================================================================
# BATCH 068 (600353-600365)
# =============================================================================
BATCHES["068"] = {
    "new_nodes": [
        {"node_id": "vacuum_electronic_device", "canonical_name_zh": "真空电子器件", "definition": "电子管、开关管(真空灭弧室)及固封极柱", "entity_type": "component"},
        {"node_id": "cigarette_paper", "canonical_name_zh": "卷烟纸", "definition": "卷烟纸、滤嘴棒纸、铝箔衬纸等特种纸", "entity_type": "material"},
        {"node_id": "tourism_investment", "canonical_name_zh": "旅游投资", "definition": "旅游产业投资、景区管理及文化演艺", "entity_type": "service"},
        {"node_id": "power_semiconductor", "canonical_name_zh": "功率半导体", "definition": "功率半导体器件的设计研发、芯片制造、封装测试", "entity_type": "component"},
        {"node_id": "aluminum_alloy", "canonical_name_zh": "铝合金", "definition": "铝合金材料及有色金属压延加工", "entity_type": "material"},
        {"node_id": "copper_smelting", "canonical_name_zh": "铜冶炼", "definition": "阴极铜、铜杆、铜管、铜箔等铜冶炼加工", "entity_type": "service"},
        {"node_id": "precious_metal", "canonical_name_zh": "贵金属", "definition": "黄金、白银等贵金属的提取与加工", "entity_type": "material"},
        {"node_id": "wine", "canonical_name_zh": "葡萄酒", "definition": "葡萄酒、果露酒的酿造与销售", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "vacuum_electronic_device_to_switchgear", "from_node": "vacuum_electronic_device", "to_node": "switchgear", "edge_type": "composition", "description": "真空电子器件是高压开关设备的核心组件"},
        {"edge_id": "copper_smelting_to_electronic_component", "from_node": "copper_smelting", "to_node": "electronic_component", "edge_type": "material_flow", "description": "铜冶炼产品用于制造电子元器件"},
        {"edge_id": "aluminum_alloy_to_automobile", "from_node": "aluminum_alloy", "to_node": "automobile", "edge_type": "composition", "description": "铝合金用于汽车轻量化零部件制造"},
    ],
    "companies": [
        {"company_id": "xuguang_elec", "name_zh": "成都旭光电子股份有限公司", "stock_codes": ["600353.SH"], "province": "四川", "city": "成都", "description": "电子管,开关管(真空灭弧室),固封极柱,高低压配电成套装置"},
        {"company_id": "dunhuang_seed", "name_zh": "甘肃省敦煌种业集团股份有限公司", "stock_codes": ["600354.SH"], "province": "甘肃", "city": "酒泉", "description": "玉米,棉花,西瓜,甜瓜,蔬菜等农作物良种"},
        {"company_id": "hengfeng_paper", "name_zh": "牡丹江恒丰纸业股份有限公司", "stock_codes": ["600356.SH"], "province": "黑龙江", "city": "牡丹江", "description": "卷烟纸,滤嘴棒纸,铝箔衬纸"},
        {"company_id": "cits_union", "name_zh": "国旅文化投资集团股份有限公司", "stock_codes": ["600358.SH"], "province": "江西", "city": "南昌", "description": "运输业,旅游业,房地产业,彩票业"},
        {"company_id": "xinong", "name_zh": "新疆塔里木农业综合开发股份有限公司", "stock_codes": ["600359.SH"], "province": "新疆", "city": "阿拉尔", "description": "棉花种植及加工"},
        {"company_id": "huaweimicro", "name_zh": "吉林华微电子股份有限公司", "stock_codes": ["600360.SH"], "province": "吉林", "city": "吉林", "description": "功率半导体器件的设计研发,芯片制造,封装测试"},
        {"company_id": "innovation_material", "name_zh": "创新新材料科技股份有限公司", "stock_codes": ["600361.SH"], "province": "北京", "city": "北京", "description": "铝合金材料,有色金属压延加工"},
        {"company_id": "jiangxi_copper", "name_zh": "江西铜业股份有限公司", "stock_codes": ["600362.SH"], "province": "江西", "city": "鹰潭", "description": "阴极铜,黄金,白银,硫酸,铜杆,铜管,铜箔"},
        {"company_id": "lianchuang_opt", "name_zh": "江西联创光电科技股份有限公司", "stock_codes": ["600363.SH"], "province": "江西", "city": "南昌", "description": "LED芯片,显示及照明用LED器件,背光源,智能控制器"},
        {"company_id": "st_tongpu", "name_zh": "通化葡萄酒股份有限公司", "stock_codes": ["600365.SH"], "province": "吉林", "city": "通化", "description": "葡萄酒,果露酒"},
    ],
    "exposures": [
        ("xuguang_elec", "vacuum_electronic_device", "manufacture", "真空电子器件制造商", 0.95),
        ("xuguang_elec", "switchgear", "manufacture", "开关设备制造商", 0.9),
        ("xuguang_elec", "high_voltage_switchgear", "manufacture", "高压开关设备制造商", 0.85),
        ("dunhuang_seed", "seed", "produce", "种子生产商", 0.95),
        ("dunhuang_seed", "agricultural_product", "produce", "农产品生产商", 0.85),
        ("hengfeng_paper", "cigarette_paper", "produce", "卷烟纸生产商", 0.95),
        ("hengfeng_paper", "specialty_paper", "produce", "特种纸生产商", 0.9),
        ("cits_union", "tourism_investment", "provide_service", "旅游投资服务商", 0.85),
        ("cits_union", "tourism_service", "provide_service", "旅游服务商", 0.8),
        ("xinong", "cotton", "produce", "棉花生产商", 0.95),
        ("xinong", "cotton_product", "produce", "棉制品生产商", 0.85),
        ("huaweimicro", "power_semiconductor", "manufacture", "功率半导体制造商", 0.95),
        ("huaweimicro", "semiconductor_device", "manufacture", "半导体器件制造商", 0.9),
        ("innovation_material", "aluminum_alloy", "produce", "铝合金生产商", 0.95),
        ("innovation_material", "aluminum_product", "produce", "铝加工产品生产商", 0.9),
        ("jiangxi_copper", "copper_smelting", "operate", "铜冶炼运营商", 0.95),
        ("jiangxi_copper", "precious_metal", "produce", "贵金属生产商", 0.85),
        ("jiangxi_copper", "nonferrous_metal_mining", "operate", "有色金属采选运营商", 0.9),
        ("lianchuang_opt", "led_display", "manufacture", "LED显示器件制造商", 0.9),
        ("lianchuang_opt", "optoelectronic_device", "manufacture", "光电子器件制造商", 0.9),
        ("st_tongpu", "wine", "produce", "葡萄酒生产商", 0.95),
        ("st_tongpu", "liquor", "produce", "酒类生产商", 0.85),
    ],
}

# =============================================================================
# BATCH 069 (600366-600376)
# =============================================================================
BATCHES["069"] = {
    "new_nodes": [
        {"node_id": "rare_earth_permanent_magnet", "canonical_name_zh": "稀土永磁材料", "definition": "钕铁硼等稀土永磁材料的研发、制造和销售", "entity_type": "material"},
        {"node_id": "barium_carbonate", "canonical_name_zh": "碳酸钡", "definition": "碳酸钡、碳酸锶等无机化工产品", "entity_type": "material"},
        {"node_id": "electrolytic_manganese_dioxide", "canonical_name_zh": "电解二氧化锰", "definition": "电解二氧化锰、金属锰等锰系产品", "entity_type": "material"},
        {"node_id": "road_bridge", "canonical_name_zh": "公路桥梁", "definition": "公路、桥梁的建设和经营管理", "entity_type": "infrastructure"},
        {"node_id": "printed_fabric", "canonical_name_zh": "印染布", "definition": "印染布、纱线及PBT树脂等化工纺织产品", "entity_type": "material"},
        {"node_id": "pbt_resin", "canonical_name_zh": "PBT树脂", "definition": "聚对苯二甲酸丁二醇酯等工程塑料", "entity_type": "material"},
        {"node_id": "starch_sugar", "canonical_name_zh": "淀粉糖", "definition": "高麦芽糖浆、啤酒专用糖浆、麦芽糊精等淀粉糖产品", "entity_type": "material"},
        {"node_id": "avionics", "canonical_name_zh": "航空电子", "definition": "机载航空电子系统、飞行控制系统、机电系统", "entity_type": "system"},
        {"node_id": "new_media", "canonical_name_zh": "新媒体", "definition": "数字出版、互联网游戏、影视剧生产、在线教育", "entity_type": "service"},
        {"node_id": "heavy_truck", "canonical_name_zh": "重型卡车", "definition": "重卡、专用汽车及汽车零部件的生产研发", "entity_type": "system"},
    ],
    "new_edges": [
        {"edge_id": "rare_earth_permanent_magnet_to_motor", "from_node": "rare_earth_permanent_magnet", "to_node": "large_motor", "edge_type": "composition", "description": "稀土永磁材料用于制造高效电机"},
        {"edge_id": "starch_sugar_to_beverage", "from_node": "starch_sugar", "to_node": "beverage", "edge_type": "material_flow", "description": "淀粉糖是饮料生产的重要原料"},
        {"edge_id": "avionics_to_aircraft", "from_node": "avionics", "to_node": "trainer_aircraft", "edge_type": "composition", "description": "航空电子系统是飞行器的核心组成部分"},
    ],
    "companies": [
        {"company_id": "yunsheng", "name_zh": "宁波韵升股份有限公司", "stock_codes": ["600366.SH"], "province": "浙江", "city": "宁波", "description": "稀土永磁材料的研发,制造和销售"},
        {"company_id": "redstar_dev", "name_zh": "贵州红星发展股份有限公司", "stock_codes": ["600367.SH"], "province": "贵州", "city": "安顺", "description": "碳酸钡,碳酸锶,不溶性硫磺,硫脲,电解二氧化锰,金属锰"},
        {"company_id": "wuzhou_traffic", "name_zh": "广西五洲交通股份有限公司", "stock_codes": ["600368.SH"], "province": "广西", "city": "南宁", "description": "公路,桥梁的建设和经营管理"},
        {"company_id": "southwest_securities", "name_zh": "西南证券股份有限公司", "stock_codes": ["600369.SH"], "province": "重庆", "city": "重庆", "description": "证券经纪,证券承销与保荐,证券自营,证券资产管理"},
        {"company_id": "st_sanfang", "name_zh": "江苏三房巷聚材股份有限公司", "stock_codes": ["600370.SH"], "province": "江苏", "city": "无锡", "description": "印染布,纱,PBT树脂,电,蒸汽"},
        {"company_id": "wanxiang_denong", "name_zh": "万向德农股份有限公司", "stock_codes": ["600371.SH"], "province": "黑龙江", "city": "哈尔滨", "description": "玉米,牧草,油葵等农作物种子,高麦芽糖浆,啤酒专用糖浆"},
        {"company_id": "avic_systems", "name_zh": "中航机载系统股份有限公司", "stock_codes": ["600372.SH"], "province": "北京", "city": "北京", "description": "航空,防务及安全领域电子产品,智能装备"},
        {"company_id": "chinesemedia", "name_zh": "中文天地出版传媒集团股份有限公司", "stock_codes": ["600373.SH"], "province": "江西", "city": "上饶", "description": "书刊和音像电子出版物编辑出版,印刷发行,新媒体,数字出版"},
        {"company_id": "hanma_tech", "name_zh": "汉马科技集团股份有限公司", "stock_codes": ["600375.SH"], "province": "安徽", "city": "马鞍山", "description": "混凝土搅拌车,散装水泥车,混凝土泵车,重卡,专用汽车"},
        {"company_id": "shoukai", "name_zh": "北京首都开发股份有限公司", "stock_codes": ["600376.SH"], "province": "北京", "city": "北京", "description": "商品房,经济适用房,普通办公楼,商业设施以及土地的开发与销售"},
    ],
    "exposures": [
        ("yunsheng", "rare_earth_permanent_magnet", "produce", "稀土永磁材料生产商", 0.95),
        ("yunsheng", "rare_earth_functional", "produce", "稀土功能材料生产商", 0.9),
        ("redstar_dev", "barium_carbonate", "produce", "碳酸钡生产商", 0.95),
        ("redstar_dev", "electrolytic_manganese_dioxide", "produce", "电解二氧化锰生产商", 0.9),
        ("redstar_dev", "chemical_product", "produce", "化工产品生产商", 0.85),
        ("wuzhou_traffic", "road_bridge", "operate", "公路桥梁运营商", 0.95),
        ("wuzhou_traffic", "toll_road", "operate", "路桥收费运营商", 0.9),
        ("southwest_securities", "securities_service", "provide_service", "证券服务商", 0.95),
        ("southwest_securities", "financial_service", "provide_service", "金融服务商", 0.9),
        ("st_sanfang", "printed_fabric", "produce", "印染布生产商", 0.9),
        ("st_sanfang", "pbt_resin", "produce", "PBT树脂生产商", 0.85),
        ("st_sanfang", "textile_product", "produce", "纺织品生产商", 0.8),
        ("wanxiang_denong", "seed", "produce", "种子生产商", 0.95),
        ("wanxiang_denong", "starch_sugar", "produce", "淀粉糖生产商", 0.9),
        ("wanxiang_denong", "agricultural_product", "produce", "农产品生产商", 0.85),
        ("avic_systems", "avionics", "manufacture", "航空电子制造商", 0.95),
        ("avic_systems", "flight_control", "manufacture", "飞行控制系统制造商", 0.9),
        ("avic_systems", "aircraft_electromechanical", "manufacture", "航空机电系统制造商", 0.9),
        ("chinesemedia", "publishing_media", "provide_service", "出版传媒服务商", 0.95),
        ("chinesemedia", "new_media", "provide_service", "新媒体服务商", 0.85),
        ("hanma_tech", "heavy_truck", "manufacture", "重型卡车制造商", 0.95),
        ("hanma_tech", "special_vehicle", "manufacture", "专用车制造商", 0.9),
        ("hanma_tech", "automobile_part", "manufacture", "汽车零部件制造商", 0.85),
        ("shoukai", "real_estate_development", "operate", "房地产开发运营商", 0.95),
    ],
}

# =============================================================================
# BATCH 070 (600377-600389)
# =============================================================================
BATCHES["070"] = {
    "new_nodes": [
        {"node_id": "catalyst", "canonical_name_zh": "催化剂", "definition": "化工催化剂及特种化学品的研制、生产、销售", "entity_type": "material"},
        {"node_id": "specialty_gas", "canonical_name_zh": "特种气体", "definition": "工业特种气体的研制、开发、生产、销售", "entity_type": "material"},
        {"node_id": "specialty_valve", "canonical_name_zh": "特种阀门", "definition": "工业特种阀门生产及销售", "entity_type": "component"},
        {"node_id": "vacuum_switchgear", "canonical_name_zh": "真空开关设备", "definition": "真空开关设备及元器件", "entity_type": "device"},
        {"node_id": "health_product", "canonical_name_zh": "保健品", "definition": "太太口服液、静心口服液等保健食品及营养健康产品", "entity_type": "material"},
        {"node_id": "cordyceps", "canonical_name_zh": "冬虫夏草", "definition": "冬虫夏草产品的研发、生产与销售", "entity_type": "material"},
        {"node_id": "iron_ore", "canonical_name_zh": "铁矿石", "definition": "铁矿石开采及销售", "entity_type": "material"},
        {"node_id": "bus_advertising", "canonical_name_zh": "公交广告", "definition": "公交车身广告、候车亭广告等媒体代理发布", "entity_type": "service"},
        {"node_id": "auto_service", "canonical_name_zh": "汽车服务", "definition": "汽车租赁、修理、清洁燃料开发销售", "entity_type": "service"},
        {"node_id": "electrostatic_precipitator", "canonical_name_zh": "电除尘器", "definition": "电除尘器成套项目、脱硫项目及环保设备", "entity_type": "device"},
        {"node_id": "desulfurization", "canonical_name_zh": "脱硫设备", "definition": "烟气脱硫、脱硝等大气污染治理设备", "entity_type": "device"},
        {"node_id": "glyphosate", "canonical_name_zh": "草甘膦", "definition": "草甘膦、敌敌畏、敌百虫等农药产品及化工产品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "catalyst_to_chemical_industry", "from_node": "catalyst", "to_node": "chemical_industry", "edge_type": "capability_supply", "description": "催化剂为化工生产提供反应加速能力"},
        {"edge_id": "vacuum_switchgear_to_power_grid", "from_node": "vacuum_switchgear", "to_node": "power_grid", "edge_type": "composition", "description": "真空开关设备是电网配电系统的组成部分"},
        {"edge_id": "electrostatic_precipitator_to_power_plant", "from_node": "electrostatic_precipitator", "to_node": "power_generation", "edge_type": "capability_supply", "description": "电除尘器为火力发电厂提供烟气净化能力"},
    ],
    "companies": [
        {"company_id": "ninghu_expressway", "name_zh": "江苏宁沪高速公路股份有限公司", "stock_codes": ["600377.SH"], "province": "江苏", "city": "南京", "description": "沪宁高速公路江苏段,宁沪二级公路,广靖锡澄高速公路"},
        {"company_id": "haohua_tech", "name_zh": "昊华化工科技集团股份有限公司", "stock_codes": ["600378.SH"], "province": "四川", "city": "成都", "description": "催化剂,变压吸附气体分离技术及装置,特种气体,有机化工产品"},
        {"company_id": "baoguang", "name_zh": "陕西宝光真空电器股份有限公司", "stock_codes": ["600379.SH"], "province": "陕西", "city": "宝鸡", "description": "真空开关设备及元器件"},
        {"company_id": "joincare", "name_zh": "健康元药业集团股份有限公司", "stock_codes": ["600380.SH"], "province": "广东", "city": "深圳", "description": "太太口服液,静心口服液,药品及保健品"},
        {"company_id": "st_chuntian", "name_zh": "青海春天药用资源科技股份有限公司", "stock_codes": ["600381.SH"], "province": "青海", "city": "西宁", "description": "冬虫夏草产品的研发,生产与销售"},
        {"company_id": "guangdong_mingzhu", "name_zh": "广东明珠集团股份有限公司", "stock_codes": ["600382.SH"], "province": "广东", "city": "梅州", "description": "PPP模式项目合作,土地一级开发,实业投资"},
        {"company_id": "gemdale", "name_zh": "金地(集团)股份有限公司", "stock_codes": ["600383.SH"], "province": "广东", "city": "深圳", "description": "房地产开发与经营,物业租赁和物业管理"},
        {"company_id": "beibamedia", "name_zh": "北京巴士传媒股份有限公司", "stock_codes": ["600386.SH"], "province": "北京", "city": "北京", "description": "公交广告业务,汽车服务业务和投资业务"},
        {"company_id": "longking", "name_zh": "福建龙净环保股份有限公司", "stock_codes": ["600388.SH"], "province": "福建", "city": "龙岩", "description": "电除尘器成套项目,脱硫项目,固废治理"},
        {"company_id": "jiangshan", "name_zh": "南通江山农药化工股份有限公司", "stock_codes": ["600389.SH"], "province": "江苏", "city": "南通", "description": "草甘膦,敌敌畏,敌百虫,丁乙草胺等农药产品"},
    ],
    "exposures": [
        ("ninghu_expressway", "expressway", "operate", "高速公路运营商", 0.95),
        ("ninghu_expressway", "toll_road", "operate", "路桥收费运营商", 0.9),
        ("haohua_tech", "catalyst", "produce", "催化剂生产商", 0.95),
        ("haohua_tech", "specialty_gas", "produce", "特种气体生产商", 0.9),
        ("haohua_tech", "specialty_valve", "manufacture", "特种阀门制造商", 0.85),
        ("haohua_tech", "chemical_product", "produce", "化工产品生产商", 0.85),
        ("baoguang", "vacuum_switchgear", "manufacture", "真空开关设备制造商", 0.95),
        ("baoguang", "switchgear", "manufacture", "开关设备制造商", 0.9),
        ("baoguang", "power_distribution_equipment", "manufacture", "配电设备制造商", 0.85),
        ("joincare", "health_product", "produce", "保健品生产商", 0.9),
        ("joincare", "pharmaceutical", "produce", "药品生产商", 0.85),
        ("st_chuntian", "cordyceps", "produce", "冬虫夏草产品生产商", 0.95),
        ("st_chuntian", "chinese_patent_medicine", "produce", "中成药生产商", 0.85),
        ("guangdong_mingzhu", "iron_ore", "produce", "铁矿石生产商", 0.85),
        ("guangdong_mingzhu", "land_development", "operate", "土地开发运营商", 0.8),
        ("gemdale", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("gemdale", "property_management", "provide_service", "物业管理服务商", 0.85),
        ("beibamedia", "bus_advertising", "provide_service", "公交广告服务商", 0.9),
        ("beibamedia", "auto_service", "provide_service", "汽车服务商", 0.85),
        ("longking", "electrostatic_precipitator", "manufacture", "电除尘器制造商", 0.95),
        ("longking", "desulfurization", "manufacture", "脱硫设备制造商", 0.9),
        ("longking", "solid_waste_treatment", "provide_service", "固废处理服务商", 0.85),
        ("longking", "environmental_service", "provide_service", "环保服务提供商", 0.9),
        ("jiangshan", "glyphosate", "produce", "草甘膦生产商", 0.95),
        ("jiangshan", "pesticide", "produce", "农药生产商", 0.9),
        ("jiangshan", "caustic_soda", "produce", "烧碱生产商", 0.85),
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
    for num in ["066", "067", "068", "069", "070"]:
        ok = submit_batch(num, BATCHES[num])
        results[num] = ok

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for num, ok in results.items():
        print(f"  Batch {num}: {'OK' if ok else 'FAILED'}")
