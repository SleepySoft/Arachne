"""
Batch 004 产业图与公司视图构建脚本
"""

import asyncio
import httpx
import json

API_BASE = "http://localhost:8000/api/v1"

def ev(source_title: str, quote: str, source_url: str = ""):
    return {"source_title": source_title, "source_url": source_url or None, "quote": quote}

# ============================================================
# 新建产业节点
# ============================================================

NEW_NODES = [
    # ---- 农业（京基智农）----
    {
        "node_id": "animal_feed",
        "canonical_name_zh": "饲料",
        "canonical_name_en": "Animal Feed",
        "aliases": ["畜禽饲料", "养殖饲料"],
        "definition": "用于喂养畜禽等经济动物的配合饲料，是连接种植业和养殖业的关键中间产品。",
        "entity_type": "material",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务为生猪养殖与销售、饲料生产与销售、种鸡和肉鸡养殖与销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "live_pig",
        "canonical_name_zh": "生猪",
        "canonical_name_en": "Live Pig",
        "aliases": ["活猪", "商品猪"],
        "definition": "人工饲养、用于屠宰取肉的猪只，是猪肉食品产业链的上游活体产品。",
        "entity_type": "material",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务为生猪养殖与销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "poultry",
        "canonical_name_zh": "家禽",
        "canonical_name_en": "Poultry",
        "aliases": ["肉鸡", "种鸡", "禽类"],
        "definition": "人工饲养的鸡、鸭、鹅等禽类，用于产蛋或肉用，是禽肉产业链的上游活体产品。",
        "entity_type": "material",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务包括种鸡、肉鸡养殖与销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 建材/显示（方大集团）----
    {
        "node_id": "building_curtain_wall",
        "canonical_name_zh": "建筑幕墙",
        "canonical_name_en": "Building Curtain Wall",
        "aliases": ["幕墙", "玻璃幕墙", "铝板幕墙"],
        "definition": "悬挂在建筑物主体结构外围、不承担主体结构荷载的板式围护结构，通常由面板和支承结构组成。",
        "entity_type": "component",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括节能幕墙、光电幕墙、LED彩显幕墙等各类建筑幕墙及铝板材料。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "platform_screen_door",
        "canonical_name_zh": "站台屏蔽门",
        "canonical_name_en": "Platform Screen Door",
        "aliases": ["屏蔽门", "安全门", "站台门"],
        "definition": "安装在地铁站台边缘、将站台与轨道区域隔离的机电设备系统，用于保障乘客安全和改善站台环境。",
        "entity_type": "subsystem",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括轨道交通屏蔽门系统。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "led_display_screen",
        "canonical_name_zh": "LED显示屏",
        "canonical_name_en": "LED Display Screen",
        "aliases": ["LED彩显幕墙", "LED大屏"],
        "definition": "由发光二极管阵列组成的电子显示设备，可用于室内外信息显示、广告播放和建筑幕墙装饰。",
        "entity_type": "device",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括LED彩显幕墙等各类建筑幕墙。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "aluminum_panel",
        "canonical_name_zh": "铝板",
        "canonical_name_en": "Aluminum Panel",
        "aliases": ["铝合金板", "铝板材料"],
        "definition": "以铝或铝合金为主要材料轧制而成的板材，具有轻质、耐腐蚀、易加工等特性，广泛用于建筑幕墙和工业制造。",
        "entity_type": "material",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括各类建筑幕墙及铝板材料。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 商业（*ST皇庭）----
    {
        "node_id": "chain_retail_service",
        "canonical_name_zh": "连锁零售服务",
        "canonical_name_en": "Chain Retail Service",
        "aliases": ["连锁商业", "零售连锁"],
        "definition": "通过统一品牌、统一管理和标准化运营模式，在多个地点开设门店向消费者销售商品的零售服务。",
        "entity_type": "service",
        "evidence": [ev("*ST皇庭2025年年度报告", "公司主要业务为连锁商业经营、房地产开发和物业管理。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 电子市场（深赛格）----
    {
        "node_id": "electronics_market_service",
        "canonical_name_zh": "电子专业市场服务",
        "canonical_name_en": "Electronics Market Service",
        "aliases": ["电子市场运营", "电子卖场服务"],
        "definition": "为电子元器件、IT产品等商户提供集中交易场所、物业管理和配套服务的专业市场运营服务。",
        "entity_type": "service",
        "evidence": [ev("深赛格2025年年度报告", "公司主营业务是电子专业市场及配套项目的开发及经营、物业租赁服务业务、IT产品渠道零售终端业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 石化（华锦股份）----
    {
        "node_id": "crude_oil",
        "canonical_name_zh": "原油",
        "canonical_name_en": "Crude Oil",
        "aliases": ["石油", "原石油"],
        "definition": "从地下开采出来的未经炼制的天然石油，是石油化工产业的最上游原料。",
        "entity_type": "material",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品、化学肥料的生产与销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "petrochemical_product",
        "canonical_name_zh": "石油化工产品",
        "canonical_name_en": "Petrochemical Product",
        "aliases": ["石化产品", "化工产品"],
        "definition": "以石油和天然气为原料，通过化学加工生产的各类有机化学品和合成材料，包括烯烃、芳烃、合成树脂等。",
        "entity_type": "material",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品的生产与销售，2025年营收417.56亿元。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "chemical_fertilizer",
        "canonical_name_zh": "化学肥料",
        "canonical_name_en": "Chemical Fertilizer",
        "aliases": ["化肥", "合成肥料"],
        "definition": "以化学方法合成或矿物加工制成的、为农作物提供氮磷钾等营养元素的肥料产品。",
        "entity_type": "material",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为化学肥料的生产与销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "refining_service",
        "canonical_name_zh": "石油炼化服务",
        "canonical_name_en": "Oil Refining Service",
        "aliases": ["炼油服务", "石油加工"],
        "definition": "将原油通过蒸馏、裂化、重整等工艺加工成汽油、柴油、石化原料等产品的工业生产过程。",
        "entity_type": "service",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品的生产与销售，涉及石油炼化加工。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    # 农业链
    {
        "edge_id": "flow_agri_to_feed",
        "from_node": "agricultural_product",
        "to_node": "animal_feed",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "农产品（玉米、大豆等）经过加工成为畜禽饲料，是种植业向养殖业转化的关键环节。",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务包括饲料生产与销售，饲料以农产品为原料加工而成。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_feed_to_pig",
        "from_node": "animal_feed",
        "to_node": "live_pig",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "饲料作为生猪养殖的主要投入品，为生猪生长提供营养，转化为活体商品猪。",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务为生猪养殖与销售、饲料生产与销售。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_feed_to_poultry",
        "from_node": "animal_feed",
        "to_node": "poultry",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "饲料作为家禽养殖的主要投入品，为鸡只生长提供营养，转化为商品肉鸡和种鸡。",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务包括种鸡、肉鸡养殖与销售、饲料生产与销售。")],
        "confidence": "HIGH",
    },
    # 显示链
    {
        "edge_id": "flow_panel_to_module",
        "from_node": "lcd_panel",
        "to_node": "display_module",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "液晶显示面板与驱动电路、背光源等组件组装构成完整的液晶显示模组。",
        "evidence": [ev("行业常识", "液晶显示模组由液晶面板、驱动IC、背光源、柔性电路板等组件组装而成。")],
        "confidence": "HIGH",
    },
    # 建材链
    {
        "edge_id": "flow_alum_to_curtain",
        "from_node": "aluminum_panel",
        "to_node": "building_curtain_wall",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "铝板作为建筑幕墙的主要面板材料之一，通过框架结构组装构成幕墙系统。",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括各类建筑幕墙及铝板材料。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_glass_to_curtain",
        "from_node": "float_glass",
        "to_node": "building_curtain_wall",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "浮法玻璃经过钢化、镀膜等深加工后，作为透明面板用于玻璃幕墙系统。",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括节能幕墙等各类建筑幕墙。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_steel_to_psd",
        "from_node": "steel_sheet",
        "to_node": "platform_screen_door",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "钢材作为站台屏蔽门主体结构的主要材料，提供门体框架和机械支撑。",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括轨道交通屏蔽门系统。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_semi_to_led",
        "from_node": "semiconductor_device",
        "to_node": "led_display_screen",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "LED芯片等半导体器件是LED显示屏的核心发光元件，通过驱动电路控制实现图像显示。",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括LED彩显幕墙等各类建筑幕墙。")],
        "confidence": "HIGH",
    },
    # 商业链
    {
        "edge_id": "flow_commercial_to_retail",
        "from_node": "commercial_property",
        "to_node": "chain_retail_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "商业地产为连锁零售服务提供经营场所和客流空间，是零售业态的载体。",
        "evidence": [ev("*ST皇庭2025年年度报告", "公司主要业务为连锁商业经营、房地产开发和物业管理。")],
        "confidence": "HIGH",
    },
    # 电子市场链
    {
        "edge_id": "flow_hw_to_market",
        "from_node": "it_hardware",
        "to_node": "electronics_market_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "IT硬件产品通过电子专业市场进行展示、交易和分销，市场运营方提供交易平台和配套服务。",
        "evidence": [ev("深赛格2025年年度报告", "公司主营业务是电子专业市场及配套项目的开发及经营、IT产品渠道零售终端业务。")],
        "confidence": "HIGH",
    },
    # 石化链
    {
        "edge_id": "flow_oil_to_refinery",
        "from_node": "crude_oil",
        "to_node": "refining_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "原油通过石油炼化加工转化为各类石化产品和燃料，是石化产业链的起点。",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品、化学肥料的生产与销售，涉及石油炼化加工。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_refinery_to_petro",
        "from_node": "refining_service",
        "to_node": "petrochemical_product",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "石油炼化过程产出乙烯、丙烯、芳烃等基础石化产品，是下游化工产业的基础原料。",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品的生产与销售。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_gas_to_petro",
        "from_node": "natural_gas",
        "to_node": "petrochemical_product",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "天然气（甲烷等）作为原料通过化工合成生产甲醇、合成氨等石化产品。",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品、化学肥料的生产与销售。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_petro_to_plastic",
        "from_node": "petrochemical_product",
        "to_node": "plastic_resin",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "石油化工产品（如乙烯、丙烯）通过聚合反应合成聚乙烯、聚丙烯等塑料树脂。",
        "evidence": [ev("行业常识", "塑料树脂是以石油化工产品为原料合成的高分子材料。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_petro_to_fertilizer",
        "from_node": "petrochemical_product",
        "to_node": "chemical_fertilizer",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "合成氨等石化中间产品进一步加工成为尿素等化学肥料。",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品、化学肥料的生产与销售。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司档案
# ============================================================

COMPANIES = [
    {
        "company_id": "zhongzhou_holding",
        "name_zh": "深圳市中洲投资控股股份有限公司",
        "name_en": "Shenzhen Zhongzhou Investment Holding Co., Ltd.",
        "aliases": ["中洲控股"],
        "stock_codes": ["000042.SZ"],
        "description": "深圳房地产开发企业，主要从事房地产开发及商品房销售，2025年营收25.94亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1984, "employee_count": 2285,
        "revenue_cny": 2594482776.47, "market_cap_cny": 6668256324.0, "net_profit_cny": -902407022.03,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "cms_jiyu",
        "name_zh": "招商局积余产业运营服务股份有限公司",
        "name_en": "China Merchants Jiyu Industrial Operation Service Co., Ltd.",
        "aliases": ["招商积余"],
        "stock_codes": ["001914.SZ"],
        "description": "招商局集团旗下物业管理和产业运营平台，主营物业管理、资产运营及相关增值服务，2025年营收192.73亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1985, "employee_count": 41450,
        "revenue_cny": 19273211990.16, "market_cap_cny": 10252694218.0, "net_profit_cny": 654579171.43,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shenzhen_textile",
        "name_zh": "深圳市纺织(集团)股份有限公司",
        "name_en": "Shenzhen Textile (Holdings) Co., Ltd.",
        "aliases": ["深纺织A"],
        "stock_codes": ["000045.SZ"],
        "description": "深圳国有控股企业，核心业务为偏光片等光学膜产品的研发、生产和销售，兼营物业租赁，2025年营收32.41亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1982, "employee_count": 1404,
        "revenue_cny": 3241380430.62, "market_cap_cny": 6179656558.0, "net_profit_cny": 68418663.02,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "jingji_smartfarm",
        "name_zh": "深圳市京基智农时代股份有限公司",
        "name_en": "Shenzhen Jingji Smart Agriculture Times Co., Ltd.",
        "aliases": ["京基智农"],
        "stock_codes": ["000048.SZ"],
        "description": "现代农业企业，主营生猪养殖与销售、饲料生产、种鸡肉鸡养殖及房地产开发，2025年营收48.72亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1979, "employee_count": 3281,
        "revenue_cny": 4871819142.45, "market_cap_cny": 7217141423.0, "net_profit_cny": 152808661.82,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "desay_battery",
        "name_zh": "深圳市德赛电池科技股份有限公司",
        "name_en": "Shenzhen Desay Battery Technology Co., Ltd.",
        "aliases": ["德赛电池"],
        "stock_codes": ["000049.SZ"],
        "description": "国内领先的小型锂电池及电源管理系统制造商，主营消费电子电池、动力电池及储能电池，2025年营收224.0亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1985, "employee_count": 16272,
        "revenue_cny": 22399427302.94, "market_cap_cny": 10546788602.0, "net_profit_cny": 292270104.15,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "tianma_micro",
        "name_zh": "天马微电子股份有限公司",
        "name_en": "Tianma Microelectronics Co., Ltd.",
        "aliases": ["深天马A", "天马微电子"],
        "stock_codes": ["000050.SZ"],
        "description": "国内领先的中小尺寸液晶显示面板制造商，产品涵盖智能手机、车载、工控等领域显示屏，2025年营收362.27亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1983, "employee_count": 23538,
        "revenue_cny": 36226540318.59, "market_cap_cny": 19364416012.0, "net_profit_cny": 167375926.83,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "fangda_group",
        "name_zh": "方大集团股份有限公司",
        "name_en": "Fangda Group Co., Ltd.",
        "aliases": ["方大集团"],
        "stock_codes": ["000055.SZ"],
        "description": "多元化产业集团，主营高端幕墙系统、轨道交通屏蔽门、太阳能光伏发电和房地产，2025年营收33.77亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1994, "employee_count": 2949,
        "revenue_cny": 3377303066.44, "market_cap_cny": 3855208475.0, "net_profit_cny": -515466884.24,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huangting_international",
        "name_zh": "深圳市皇庭国际企业股份有限公司",
        "name_en": "Shenzhen Wongtee International Enterprise Co., Ltd.",
        "aliases": ["*ST皇庭", "皇庭国际"],
        "stock_codes": ["000056.SZ"],
        "description": "深圳商业和房地产企业，主营连锁商业经营、房地产开发和物业管理，2025年营收33.60亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1985, "employee_count": 730,
        "revenue_cny": 3360179115.05, "market_cap_cny": 1489985557.0, "net_profit_cny": -2729683196.27,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "seg_electronics",
        "name_zh": "深圳赛格股份有限公司",
        "name_en": "Shenzhen Seg Co., Ltd.",
        "aliases": ["深赛格"],
        "stock_codes": ["000058.SZ"],
        "description": "深圳华强北电子市场运营商，主营电子专业市场开发经营、物业租赁、IT零售及光伏业务，2025年营收16.88亿元。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1996, "employee_count": 7186,
        "revenue_cny": 1687654147.69, "market_cap_cny": 9332501094.0, "net_profit_cny": 69394739.7,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huajin_chemical",
        "name_zh": "北方华锦化学工业股份有限公司",
        "name_en": "North Huajin Chemical Industries Co., Ltd.",
        "aliases": ["华锦股份"],
        "stock_codes": ["000059.SZ"],
        "description": "中国兵器工业集团旗下石化企业，主营石油化工产品和化学肥料的生产与销售，2025年营收417.56亿元。",
        "country": "CN", "province": "辽宁", "city": "盘锦市",
        "founded_year": 1997, "employee_count": 7683,
        "revenue_cny": 41756479557.71, "market_cap_cny": 7533374349.0, "net_profit_cny": -1763294889.03,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 中洲控股 ----
    {
        "exposure_id": "zhongzhou_produce_residential",
        "company_id": "zhongzhou_holding",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "商品住宅开发商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中洲控股2025年年度报告", "公司主营业务为房地产开发及商品房的销售、管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongzhou_produce_commercial",
        "company_id": "zhongzhou_holding",
        "node_id": "commercial_property",
        "activity_type": "produce",
        "role": "商业地产开发商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("中洲控股2025年年度报告", "公司主营业务为房地产开发及商品房的销售、管理；承接建筑安装工程；自有物业租赁。")],
        "status": "ACTIVE",
    },
    # ---- 招商积余 ----
    {
        "exposure_id": "cms_jiyu_produce_residential",
        "company_id": "cms_jiyu",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("招商积余2025年年度报告", "公司主营业务为地产开发业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "cms_jiyu_provide_property",
        "company_id": "cms_jiyu",
        "node_id": "property_management_service",
        "activity_type": "provide_service",
        "role": "物业管理及产业运营服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("招商积余2025年年度报告", "公司主营业务包括自有物业管理、经营，房产租赁服务，鉴证咨询服务，商务辅助服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "cms_jiyu_provide_housing_rental",
        "company_id": "cms_jiyu",
        "node_id": "housing_rental_service",
        "activity_type": "provide_service",
        "role": "房产租赁服务商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("招商积余2025年年度报告", "公司主营业务包括房产租赁服务。")],
        "status": "ACTIVE",
    },
    # ---- 深纺织A ----
    {
        "exposure_id": "shenzhen_textile_manufacture_lcd_pol",
        "company_id": "shenzhen_textile",
        "node_id": "lcd_polarizer",
        "activity_type": "manufacture",
        "role": "LCD偏光片制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深纺织A2025年年度报告", "公司生产、经营偏光片等光学膜产品，偏光片是公司的核心业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenzhen_textile_manufacture_oled_pol",
        "company_id": "shenzhen_textile",
        "node_id": "oled_polarizer",
        "activity_type": "manufacture",
        "role": "OLED偏光片制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("深纺织A2025年年度报告", "公司生产、经营偏光片等光学膜产品。")],
        "status": "ACTIVE",
    },
    # ---- 京基智农 ----
    {
        "exposure_id": "jingji_manufacture_feed",
        "company_id": "jingji_smartfarm",
        "node_id": "animal_feed",
        "activity_type": "manufacture",
        "role": "畜禽饲料生产商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务为生猪养殖与销售、饲料生产与销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "jingji_produce_live_pig",
        "company_id": "jingji_smartfarm",
        "node_id": "live_pig",
        "activity_type": "produce",
        "role": "生猪养殖企业",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务为生猪养殖与销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "jingji_produce_poultry",
        "company_id": "jingji_smartfarm",
        "node_id": "poultry",
        "activity_type": "produce",
        "role": "种鸡和肉鸡养殖企业",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务包括种鸡、肉鸡养殖与销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "jingji_produce_residential",
        "company_id": "jingji_smartfarm",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商（兼营）",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("京基智农2025年年度报告", "公司主要业务包括房地产开发。")],
        "status": "ACTIVE",
    },
    # ---- 德赛电池 ----
    {
        "exposure_id": "desay_manufacture_bms",
        "company_id": "desay_battery",
        "node_id": "bms_component",
        "activity_type": "manufacture",
        "role": "电源管理系统（BMS）制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("德赛电池2025年年度报告", "公司主营业务以生产制造电源管理系统及各类锂电池为主。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "desay_manufacture_consumer_battery",
        "company_id": "desay_battery",
        "node_id": "consumer_battery_pack",
        "activity_type": "manufacture",
        "role": "消费类锂电池Pack制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("德赛电池2025年年度报告", "公司主营业务以生产制造电源管理系统及各类锂电池为主。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "desay_manufacture_storage_battery",
        "company_id": "desay_battery",
        "node_id": "energy_storage_battery",
        "activity_type": "manufacture",
        "role": "储能电池制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("德赛电池2025年年度报告", "公司主营业务包括无汞碱锰电池、一次锂电池、镍氢电池、锂聚合物电池、燃料电池及其他种类电池。")],
        "status": "ACTIVE",
    },
    # ---- 深天马A ----
    {
        "exposure_id": "tianma_manufacture_lcd_panel",
        "company_id": "tianma_micro",
        "node_id": "lcd_panel",
        "activity_type": "manufacture",
        "role": "中小尺寸液晶显示面板制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深天马A2025年年度报告", "公司主要产品为液晶显示器、液晶显示模块。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tianma_manufacture_display_module",
        "company_id": "tianma_micro",
        "node_id": "display_module",
        "activity_type": "manufacture",
        "role": "液晶显示模组制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深天马A2025年年度报告", "公司主要产品为液晶显示器、液晶显示模块。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tianma_manufacture_lcd_monitor",
        "company_id": "tianma_micro",
        "node_id": "lcd_monitor",
        "activity_type": "manufacture",
        "role": "液晶显示器制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("深天马A2025年年度报告", "公司主要产品为液晶显示器、液晶显示模块。")],
        "status": "ACTIVE",
    },
    # ---- 方大集团 ----
    {
        "exposure_id": "fangda_manufacture_curtain_wall",
        "company_id": "fangda_group",
        "node_id": "building_curtain_wall",
        "activity_type": "manufacture",
        "role": "高端建筑幕墙系统制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括节能幕墙、光电幕墙、LED彩显幕墙等各类建筑幕墙及铝板材料。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fangda_manufacture_psd",
        "company_id": "fangda_group",
        "node_id": "platform_screen_door",
        "activity_type": "manufacture",
        "role": "轨道交通屏蔽门系统制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括轨道交通屏蔽门系统。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fangda_manufacture_led_screen",
        "company_id": "fangda_group",
        "node_id": "led_display_screen",
        "activity_type": "manufacture",
        "role": "LED显示屏制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("方大集团2025年年度报告", "公司主要产品包括LED彩显幕墙等各类建筑幕墙。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fangda_manufacture_pv_module",
        "company_id": "fangda_group",
        "node_id": "photovoltaic_module",
        "activity_type": "manufacture",
        "role": "太阳能光伏组件制造商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("方大集团2025年年度报告", "公司主营业务包括太阳能光伏发电。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fangda_produce_residential",
        "company_id": "fangda_group",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商（兼营）",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("方大集团2025年年度报告", "公司主营业务包括房地产和金融等板块。")],
        "status": "ACTIVE",
    },
    # ---- *ST皇庭 ----
    {
        "exposure_id": "huangting_produce_residential",
        "company_id": "huangting_international",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("*ST皇庭2025年年度报告", "公司主要业务为连锁商业经营、房地产开发和物业管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huangting_provide_property",
        "company_id": "huangting_international",
        "node_id": "property_management_service",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("*ST皇庭2025年年度报告", "公司主要业务为连锁商业经营、房地产开发和物业管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huangting_provide_retail",
        "company_id": "huangting_international",
        "node_id": "chain_retail_service",
        "activity_type": "provide_service",
        "role": "连锁商业运营商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("*ST皇庭2025年年度报告", "公司主要业务为连锁商业经营、房地产开发和物业管理。")],
        "status": "ACTIVE",
    },
    # ---- 深赛格 ----
    {
        "exposure_id": "seg_provide_electronics_market",
        "company_id": "seg_electronics",
        "node_id": "electronics_market_service",
        "activity_type": "provide_service",
        "role": "电子专业市场运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深赛格2025年年度报告", "公司主营业务是电子专业市场及配套项目的开发及经营。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "seg_provide_property",
        "company_id": "seg_electronics",
        "node_id": "property_management_service",
        "activity_type": "provide_service",
        "role": "物业租赁服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("深赛格2025年年度报告", "公司主营业务包括物业租赁服务业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "seg_provide_housing_rental",
        "company_id": "seg_electronics",
        "node_id": "housing_rental_service",
        "activity_type": "provide_service",
        "role": "房屋租赁服务商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("深赛格2025年年度报告", "公司主营业务包括物业租赁服务业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "seg_manufacture_pv",
        "company_id": "seg_electronics",
        "node_id": "photovoltaic_module",
        "activity_type": "manufacture",
        "role": "碲化镉薄膜太阳能电池组件制造商",
        "weight": 0.4, "confidence": "MEDIUM",
        "evidence": [ev("深赛格2025年年度报告", "公司经营范围包括碲化镉薄膜太阳能电池组件的技术开发、技术服务；制造、销售碲化镉太阳能电池组件产品。")],
        "status": "ACTIVE",
    },
    # ---- 华锦股份 ----
    {
        "exposure_id": "huajin_manufacture_petro",
        "company_id": "huajin_chemical",
        "node_id": "petrochemical_product",
        "activity_type": "manufacture",
        "role": "石油化工产品制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为石油化工产品的生产与销售，2025年营收417.56亿元。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huajin_manufacture_fertilizer",
        "company_id": "huajin_chemical",
        "node_id": "chemical_fertilizer",
        "activity_type": "manufacture",
        "role": "化学肥料制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华锦股份2025年年度报告", "公司主要业务为化学肥料的生产与销售。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_004_industrial_graph",
        "task_description": "Batch 004: 为10家上市公司构建产业实体图，涵盖房地产、物业、显示面板、农业养殖、电池、石化、建材幕墙、电子市场等产业链。",
        "nodes_to_upsert": NEW_NODES,
        "edges_to_upsert": EDGES,
        "rejected_or_pending": []
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/batches", json=batch, timeout=120.0)
        print(f"Graph batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


async def submit_business_batch():
    batch = {
        "batch_id": "batch_004_company_views",
        "task_description": "Batch 004: 为10家上市公司构建公司视图，包括公司信息和产业节点暴露关系。",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": COMPANIES,
        "company_node_exposures_to_upsert": EXPOSURES
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/business-batches", json=batch, timeout=120.0)
        print(f"Business batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


async def main():
    print("=" * 70)
    print("Batch 004 产业图与公司视图构建")
    print("=" * 70)
    print(f"新建节点: {len(NEW_NODES)}")
    print(f"新建边: {len(EDGES)}")
    print(f"新建公司: {len(COMPANIES)}")
    print(f"新建暴露关系: {len(EXPOSURES)}")
    print()

    print("=" * 70)
    print("Step 1: Submitting GraphRegistrationBatch (nodes + edges)")
    print("=" * 70)
    graph_result = await submit_graph_batch()

    print("\n" + "=" * 70)
    print("Step 2: Submitting BusinessRegistrationBatch (companies + exposures)")
    print("=" * 70)
    biz_result = await submit_business_batch()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Graph batch: nodes_created={graph_result.get('nodes_created')}, nodes_updated={graph_result.get('nodes_updated')}, edges_created={graph_result.get('edges_created')}, edges_updated={graph_result.get('edges_updated')}, errors={len(graph_result.get('errors', []))}")
    if graph_result.get('errors'):
        for e in graph_result['errors']:
            print(f"  ERROR: {e}")
    print(f"Business batch: companies_created={biz_result.get('companies_created')}, companies_updated={biz_result.get('companies_updated')}, exposures_created={biz_result.get('exposures_created')}, exposures_updated={biz_result.get('exposures_updated')}, errors={len(biz_result.get('errors', []))}")
    if biz_result.get('errors'):
        for e in biz_result['errors']:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(main())
