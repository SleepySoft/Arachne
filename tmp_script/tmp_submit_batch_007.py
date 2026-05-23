"""
Batch 007 产业图与公司视图提交脚本
为 data/stock_batches/batch_007.json 中的10家中国公司构建产业实体图和公司视图。
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
    # ---- 工程机械（中联重科）----
    {
        "node_id": "construction_machinery",
        "canonical_name_zh": "工程机械",
        "canonical_name_en": "Construction Machinery",
        "aliases": ["工程机械设备", "土方机械", "起重机械"],
        "definition": "用于各类工程建设施工的土石方作业、起重装卸、路面修筑及市政环卫等作业的机械设备，包括挖掘机、起重机、混凝土泵车、压路机、推土机等。",
        "entity_type": "device",
        "evidence": [ev("中联重科2024年年度报告", "主要业务为混凝土机械、起重机械、环卫机械、路面机械、非开挖设备等基础设施重大装备及其配套部件的生产和销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 纺织品（常山北明）----
    {
        "node_id": "textile_product",
        "canonical_name_zh": "纺织品",
        "canonical_name_en": "Textile Product",
        "aliases": ["棉纺织品", "纺织面料", "机织布"],
        "definition": "以天然纤维或化学纤维为原料，通过纺纱、织造、印染等工艺加工成的纺织材料及制品，包括各类服装面料、家用纺织品及产业用纺织品。",
        "entity_type": "material",
        "evidence": [ev("常山北明2024年年度报告", "主要业务包括纺织业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 焦炭（国际实业）----
    {
        "node_id": "coke",
        "canonical_name_zh": "焦炭",
        "canonical_name_en": "Coke",
        "aliases": ["冶金焦", "炼焦碳"],
        "definition": "烟煤在隔绝空气的条件下高温干馏得到的固体产物，具有高强度、低灰分、低硫分等特点，是高炉炼铁的主要还原剂和热源。",
        "entity_type": "material",
        "evidence": [ev("国际实业2024年年度报告", "主要业务包括原煤、焦炭及煤焦化附产品的销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- PTA（东方盛虹）----
    {
        "node_id": "pta",
        "canonical_name_zh": "精对苯二甲酸",
        "canonical_name_en": "Purified Terephthalic Acid",
        "aliases": ["PTA", "对苯二甲酸"],
        "definition": "一种重要的大宗有机化工原料，由对二甲苯（PX）氧化制得，主要用于生产聚酯纤维（涤纶）、聚酯瓶片和聚酯薄膜。",
        "entity_type": "material",
        "evidence": [ev("东方盛虹2024年年度报告", "公司形成'PTA-聚酯-化纤'业务结构，拥有390万吨/年PTA产能。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 涤纶长丝（东方盛虹）----
    {
        "node_id": "polyester_filament",
        "canonical_name_zh": "涤纶长丝",
        "canonical_name_en": "Polyester Filament",
        "aliases": ["聚酯长丝", "涤纶丝", "PET长丝"],
        "definition": "以精对苯二甲酸（PTA）和乙二醇（MEG）为原料，经酯化、缩聚、熔体纺丝等工艺制成的合成纤维长丝，是纺织工业最主要的化学纤维原料。",
        "entity_type": "material",
        "evidence": [ev("东方盛虹2024年年度报告", "公司民用涤纶长丝的研发、生产和销售为核心业务，拥有涤纶长丝产能约360万吨/年。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- EVA树脂（东方盛虹）----
    {
        "node_id": "eva_resin",
        "canonical_name_zh": "EVA树脂",
        "canonical_name_en": "Ethylene-Vinyl Acetate Resin",
        "aliases": ["乙烯-醋酸乙烯共聚物", "EVA胶膜原料"],
        "definition": "由乙烯和醋酸乙烯共聚而成的高分子材料，具有良好的柔软性、透明性和粘结性，广泛用于光伏组件封装胶膜、发泡鞋材、热熔胶、电线电缆护套等领域。",
        "entity_type": "material",
        "evidence": [ev("东方盛虹2024年年度报告", "斯尔邦石化拥有EVA产能50万吨/年，光伏级EVA产品技术达到国际先进水平。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 配电设备（许继电气）----
    {
        "node_id": "power_distribution_equipment",
        "canonical_name_zh": "配电设备",
        "canonical_name_en": "Power Distribution Equipment",
        "aliases": ["电力配电设备", "配网设备", "开关设备"],
        "definition": "用于电力系统中电能分配、控制、保护和测量的成套设备，包括断路器、隔离开关、负荷开关、配电变压器、继电保护装置及配电自动化终端等。",
        "entity_type": "device",
        "evidence": [ev("许继电气2024年年度报告", "主要产品包括电力保护及自动化设备、干式变压器、电力开关、继电器及装置、电能仪表等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 血液制品（派林生物）----
    {
        "node_id": "blood_product",
        "canonical_name_zh": "血液制品",
        "canonical_name_en": "Blood Product",
        "aliases": ["血浆制品", "血液制剂"],
        "definition": "以健康人血浆为原料，采用生物学工艺或分离纯化技术制备的生物活性制剂，包括人血白蛋白、免疫球蛋白、凝血因子类等，用于临床治疗多种疾病。",
        "entity_type": "material",
        "evidence": [ev("派林生物2024年年度报告", "主营业务为血液制品的研究、开发、生产和销售。主要产品包括人血白蛋白、静注人免疫球蛋白(pH4)、乙型肝炎人免疫球蛋白等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 制冷压缩机（长虹华意）----
    {
        "node_id": "refrigeration_compressor",
        "canonical_name_zh": "制冷压缩机",
        "canonical_name_en": "Refrigeration Compressor",
        "aliases": ["冰箱压缩机", "制冷压塑机", "压缩机"],
        "definition": "制冷系统的核心动力部件，通过机械压缩使制冷剂在系统中循环，实现热量从低温区向高温区的转移，广泛应用于冰箱、冷柜、空调等制冷设备。",
        "entity_type": "component",
        "evidence": [ev("长虹华意2024年年度报告", "主要业务为无氟压缩机的生产和销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    # 煤炭→焦炭
    {
        "edge_id": "flow_coal_to_coke",
        "from_node": "coal",
        "to_node": "coke",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "烟煤在高温干馏炉中隔绝空气加热，经过干馏过程转化为焦炭，同时副产煤焦油和焦炉煤气。",
        "evidence": [ev("焦化产业常识", "焦炭由烟煤在高温（约1000°C）隔绝空气条件下干馏制得，是钢铁高炉冶炼的关键原料。")],
        "confidence": "HIGH",
    },
    # 炼油→PTA
    {
        "edge_id": "flow_refinery_to_pta",
        "from_node": "refining_service",
        "to_node": "pta",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "石油炼化一体化装置产出对二甲苯（PX），PX经氧化反应制得精对苯二甲酸（PTA）。",
        "evidence": [ev("东方盛虹2024年年度报告", "公司炼化一体化项目拥有280万吨/年芳烃联合装置，为PTA生产提供PX原料。")],
        "confidence": "HIGH",
    },
    # PTA→涤纶长丝
    {
        "edge_id": "flow_pta_to_polyester",
        "from_node": "pta",
        "to_node": "polyester_filament",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "PTA与乙二醇（MEG）经酯化、缩聚反应生成聚对苯二甲酸乙二醇酯（PET），再经熔体纺丝制成涤纶长丝。",
        "evidence": [ev("聚酯化纤产业常识", "涤纶长丝以PTA和MEG为主要原料，经聚合、纺丝、拉伸、假捻变形等工序制成。")],
        "confidence": "HIGH",
    },
    # 炼油→EVA树脂
    {
        "edge_id": "flow_refinery_to_eva",
        "from_node": "refining_service",
        "to_node": "eva_resin",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "石油炼化产出的乙烯与醋酸乙烯在高压下共聚反应，生成EVA树脂。",
        "evidence": [ev("东方盛虹2024年年度报告", "斯尔邦石化拥有240万吨/年MTO装置和50万吨/年EVA产能。")],
        "confidence": "HIGH",
    },
    # EVA→光伏组件（胶膜封装）
    {
        "edge_id": "flow_eva_to_pv_module",
        "from_node": "eva_resin",
        "to_node": "photovoltaic_module",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "EVA树脂加工成光伏封装胶膜，用于太阳能电池片的封装保护，是光伏组件的关键辅材。",
        "evidence": [ev("光伏组件制造常识", "光伏组件采用EVA胶膜将电池片与背板、玻璃封装在一起，起到绝缘、防潮和保护作用。")],
        "confidence": "HIGH",
    },
    # 压缩机→冰箱
    {
        "edge_id": "flow_compressor_to_refrigerator",
        "from_node": "refrigeration_compressor",
        "to_node": "refrigerator",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "制冷压缩机是电冰箱制冷系统的核心部件，与蒸发器、冷凝器、节流装置共同构成完整的蒸气压缩制冷循环。",
        "evidence": [ev("冰箱制造技术常识", "电冰箱由箱体、制冷系统、控制系统等组成，其中压缩机是制冷系统的心脏。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "zoomlion",
        "name_zh": "中联重科股份有限公司",
        "name_en": "Zoomlion Heavy Industry Science & Technology Co., Ltd.",
        "aliases": ["中联重科"],
        "stock_codes": ["000157.SZ", "1157.HK"],
        "description": "中国工程机械行业领军企业，产品涵盖混凝土机械、起重机械、土方机械、路面机械、环卫机械及农业机械等，是全球装备制造领域的重要参与者。",
        "country": "CN", "province": "湖南", "city": "长沙市",
        "founded_year": 1992, "employee_count": 35344,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "changshan_beiming",
        "name_zh": "石家庄常山北明科技股份有限公司",
        "name_en": "Shijiazhuang Changshan Beiming Technology Co., Ltd.",
        "aliases": ["常山北明"],
        "stock_codes": ["000158.SZ"],
        "description": "以软件信息技术服务和纺织制造为主业的双主业企业，软件业务聚焦智慧城市、政务云、大数据及行业数字化转型，纺织业务为传统棉纺织制造。",
        "country": "CN", "province": "河北", "city": "石家庄市",
        "founded_year": 1998, "employee_count": 2015,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "guoji_industry",
        "name_zh": "新疆国际实业股份有限公司",
        "name_en": "Xinjiang International Industry Co., Ltd.",
        "aliases": ["国际实业"],
        "stock_codes": ["000159.SZ"],
        "description": "综合性能源贸易与房地产企业，业务涵盖煤炭、焦炭及煤化工产品销售、进出口贸易及房地产开发。",
        "country": "CN", "province": "新疆", "city": "乌鲁木齐市",
        "founded_year": 1999, "employee_count": 648,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "eastern_shenghong",
        "name_zh": "江苏东方盛虹股份有限公司",
        "name_en": "Jiangsu Eastern Shenghong Co., Ltd.",
        "aliases": ["东方盛虹"],
        "stock_codes": ["000301.SZ"],
        "description": "大型民营石化-化纤一体化企业，拥有1,600万吨/年原油加工能力的盛虹炼化一体化项目，核心产业涵盖炼油、PTA、EVA、丙烯腈及差别化涤纶长丝，2024年石化及化工新材料业务营收超1,082亿元。",
        "country": "CN", "province": "江苏", "city": "苏州市",
        "founded_year": 1998, "employee_count": 29526,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "xj_electric",
        "name_zh": "许继电气股份有限公司",
        "name_en": "XJ Electric Co., Ltd.",
        "aliases": ["许继电气"],
        "stock_codes": ["000400.SZ"],
        "description": "中国电力装备行业领先企业，隶属于中国电气装备集团，主要产品包括电力保护及自动化设备、干式变压器、电力开关、继电器、电能仪表及智能电网解决方案。",
        "country": "CN", "province": "河南", "city": "许昌市",
        "founded_year": 1996, "employee_count": 5811,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "jinyu_jidong",
        "name_zh": "金隅冀东水泥集团股份有限公司",
        "name_en": "BBMG Jidong Cement Co., Ltd.",
        "aliases": ["金隅冀东"],
        "stock_codes": ["000401.SZ"],
        "description": "中国北方最大的水泥生产企业之一，由北京金隅集团与冀东水泥战略重组而成，主营硅酸盐水泥及熟料的制造和销售。",
        "country": "CN", "province": "河北", "city": "唐山市",
        "founded_year": 1994, "employee_count": 21148,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "financial_street",
        "name_zh": "金融街控股股份有限公司",
        "name_en": "Financial Street Holding Co., Ltd.",
        "aliases": ["金融街"],
        "stock_codes": ["000402.SZ"],
        "description": "以北京金融街区域开发运营为核心的城市综合运营商，业务涵盖区域规划、土地开发、房产开发、房屋租赁和物业管理。",
        "country": "CN", "province": "北京", "city": "北京市",
        "founded_year": 1996, "employee_count": 1933,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "pailin_biological",
        "name_zh": "派斯双林生物制药股份有限公司",
        "name_en": "Paisi Shuanglin Bio-Pharmaceutical Co., Ltd.",
        "aliases": ["派林生物"],
        "stock_codes": ["000403.SZ"],
        "description": "中国血液制品行业重点企业，专业从事血液制品的研究、开发和生产，产品包括人血白蛋白、各类免疫球蛋白及凝血因子等。",
        "country": "CN", "province": "山西", "city": "太原市",
        "founded_year": 1995, "employee_count": 2635,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "changhong_huayi",
        "name_zh": "长虹华意压缩机股份有限公司",
        "name_en": "Changhong Huayi Compressor Co., Ltd.",
        "aliases": ["长虹华意"],
        "stock_codes": ["000404.SZ"],
        "description": "全球领先的冰箱压缩机制造商，主营无氟压缩机的研发、生产和销售，产品广泛应用于家用冰箱、冷柜及轻型商用制冷设备。",
        "country": "CN", "province": "江西", "city": "景德镇市",
        "founded_year": 1996, "employee_count": 7281,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shengli",
        "name_zh": "山东胜利股份有限公司",
        "name_en": "Shandong Shengli Co., Ltd.",
        "aliases": ["胜利股份"],
        "stock_codes": ["000407.SZ"],
        "description": "综合性能源化工贸易企业，主营业务涵盖天然气销售、农化产品贸易及塑胶材料销售。",
        "country": "CN", "province": "山东", "city": "济南市",
        "founded_year": 1994, "employee_count": 1857,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 中联重科 ----
    {
        "exposure_id": "zoomlion_manufacture_machinery",
        "company_id": "zoomlion",
        "node_id": "construction_machinery",
        "activity_type": "manufacture",
        "role": "工程机械制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中联重科2024年年度报告", "主要业务为混凝土机械、起重机械、环卫机械、路面机械等基础设施重大装备的生产和销售。")],
        "status": "ACTIVE",
    },
    # ---- 常山北明 ----
    {
        "exposure_id": "beiming_manufacture_textile",
        "company_id": "changshan_beiming",
        "node_id": "textile_product",
        "activity_type": "manufacture",
        "role": "棉纺织品制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("常山北明2024年年度报告", "主要业务包括纺织业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "beiming_provide_it_service",
        "company_id": "changshan_beiming",
        "node_id": "information_system_integration",
        "activity_type": "provide_service",
        "role": "软件与信息技术服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("常山北明2024年年度报告", "主要业务包括软件信息技术服务业。")],
        "status": "ACTIVE",
    },
    # ---- 国际实业 ----
    {
        "exposure_id": "guoji_provide_coal",
        "company_id": "guoji_industry",
        "node_id": "coal",
        "activity_type": "provide_service",
        "role": "煤炭销售贸易商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("国际实业2024年年度报告", "主要业务包括原煤、焦炭及煤焦化附产品的销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "guoji_provide_coke",
        "company_id": "guoji_industry",
        "node_id": "coke",
        "activity_type": "provide_service",
        "role": "焦炭销售贸易商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("国际实业2024年年度报告", "主要业务包括原煤、焦炭及煤焦化附产品的销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "guoji_produce_property",
        "company_id": "guoji_industry",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("国际实业2024年年度报告", "主要业务包括房地产开发、销售、租赁。")],
        "status": "ACTIVE",
    },
    # ---- 东方盛虹 ----
    {
        "exposure_id": "shenghong_procure_crude",
        "company_id": "eastern_shenghong",
        "node_id": "crude_oil",
        "activity_type": "procure",
        "role": "原油采购商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "盛虹炼化一体化项目拥有1,600万吨/年原油加工能力。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenghong_operate_refinery",
        "company_id": "eastern_shenghong",
        "node_id": "refining_service",
        "activity_type": "operate",
        "role": "炼化一体化运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "盛虹炼化是国内三大民营炼化企业之一，拥有1,600万吨/年原油加工能力。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenghong_manufacture_pta",
        "company_id": "eastern_shenghong",
        "node_id": "pta",
        "activity_type": "manufacture",
        "role": "PTA生产商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "公司拥有390万吨/年PTA产能。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenghong_manufacture_polyester",
        "company_id": "eastern_shenghong",
        "node_id": "polyester_filament",
        "activity_type": "manufacture",
        "role": "涤纶长丝生产商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "公司拥有涤纶长丝产能约360万吨/年，差别化率超过90%。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenghong_manufacture_eva",
        "company_id": "eastern_shenghong",
        "node_id": "eva_resin",
        "activity_type": "manufacture",
        "role": "EVA树脂生产商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "斯尔邦石化拥有EVA产能50万吨/年，光伏级EVA市场份额全球领先。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shenghong_manufacture_petro",
        "company_id": "eastern_shenghong",
        "node_id": "petrochemical_product",
        "activity_type": "manufacture",
        "role": "石化及化工新材料生产商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("东方盛虹2024年年度报告", "石化及化工新材料业务2024年营收1,082.77亿元，占总营收78.65%。")],
        "status": "ACTIVE",
    },
    # ---- 许继电气 ----
    {
        "exposure_id": "xj_manufacture_distribution_equip",
        "company_id": "xj_electric",
        "node_id": "power_distribution_equipment",
        "activity_type": "manufacture",
        "role": "配电设备制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("许继电气2024年年度报告", "主要产品包括电力保护及自动化设备、干式变压器、电力开关、继电器及装置等。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xj_manufacture_smart_meter",
        "company_id": "xj_electric",
        "node_id": "smart_meter",
        "activity_type": "manufacture",
        "role": "智能电表制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("许继电气2024年年度报告", "主要产品包括电能仪表。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xj_provide_power_dist",
        "company_id": "xj_electric",
        "node_id": "electricity_distribution",
        "activity_type": "provide_service",
        "role": "配电自动化解决方案提供商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("许继电气2024年年度报告", "公司主要产品包括电力保护及自动化设备。")],
        "status": "ACTIVE",
    },
    # ---- 金隅冀东 ----
    {
        "exposure_id": "jinyu_manufacture_cement",
        "company_id": "jinyu_jidong",
        "node_id": "cement",
        "activity_type": "manufacture",
        "role": "水泥制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("金隅冀东2024年年度报告", "主要业务为硅酸盐水泥制造、销售。")],
        "status": "ACTIVE",
    },
    # ---- 金融街 ----
    {
        "exposure_id": "fs_produce_residential",
        "company_id": "financial_street",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("金融街2024年年度报告", "主要业务包括房产开发。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fs_produce_commercial",
        "company_id": "financial_street",
        "node_id": "commercial_property",
        "activity_type": "produce",
        "role": "商业地产开发商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("金融街2024年年度报告", "主要业务为北京金融街的区域规划、土地开发、房产开发。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fs_provide_property_mgmt",
        "company_id": "financial_street",
        "node_id": "property_management_service",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("金融街2024年年度报告", "主要业务包括房屋租赁和综合管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fs_provide_housing_rental",
        "company_id": "financial_street",
        "node_id": "housing_rental_service",
        "activity_type": "provide_service",
        "role": "房屋租赁运营商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("金融街2024年年度报告", "主要业务包括房屋租赁。")],
        "status": "ACTIVE",
    },
    # ---- 派林生物 ----
    {
        "exposure_id": "pailin_manufacture_blood",
        "company_id": "pailin_biological",
        "node_id": "blood_product",
        "activity_type": "manufacture",
        "role": "血液制品制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("派林生物2024年年度报告", "主营业务为血液制品的研究、开发、生产和销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "pailin_manufacture_biological",
        "company_id": "pailin_biological",
        "node_id": "biological_drug",
        "activity_type": "manufacture",
        "role": "生物制药商（血液制品）",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("派林生物2024年年度报告", "主要产品包括人血白蛋白、静注人免疫球蛋白等血液制品。")],
        "status": "ACTIVE",
    },
    # ---- 长虹华意 ----
    {
        "exposure_id": "huayi_manufacture_compressor",
        "company_id": "changhong_huayi",
        "node_id": "refrigeration_compressor",
        "activity_type": "manufacture",
        "role": "制冷压缩机制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("长虹华意2024年年度报告", "主要业务为无氟压缩机的生产和销售。")],
        "status": "ACTIVE",
    },
    # ---- 胜利股份 ----
    {
        "exposure_id": "shengli_provide_natural_gas",
        "company_id": "shengli",
        "node_id": "natural_gas",
        "activity_type": "provide_service",
        "role": "天然气销售贸易商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("胜利股份2024年年度报告", "主营业务包括天然气销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shengli_provide_fertilizer",
        "company_id": "shengli",
        "node_id": "chemical_fertilizer",
        "activity_type": "provide_service",
        "role": "农化产品贸易商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("胜利股份2024年年度报告", "主营业务包括农化产业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "shengli_provide_plastic",
        "company_id": "shengli",
        "node_id": "plastic_resin",
        "activity_type": "provide_service",
        "role": "塑胶材料贸易商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("胜利股份2024年年度报告", "主营业务包括塑胶产业。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_007_industrial_graph",
        "task_description": "Batch 007: 为10家中国公司构建产业实体图，涵盖工程机械、纺织、煤炭焦化、石化化纤、配电设备、水泥、房地产、血液制品、制冷压缩机及能源化工贸易等产业链。",
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
        "batch_id": "batch_007_company_views",
        "task_description": "Batch 007: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
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
    print("Batch 007 产业图与公司视图提交")
    print("=" * 70)
    print(f"新建节点: {len(NEW_NODES)}")
    print(f"新建边: {len(EDGES)}")
    print(f"新建公司: {len(COMPANIES)}")
    print(f"新建暴露关系: {len(EXPOSURES)}")
    print()

    print("=" * 70)
    print("Step 1: 提交产业图 (GraphRegistrationBatch)")
    print("=" * 70)
    graph_result = await submit_graph_batch()

    print("\n" + "=" * 70)
    print("Step 2: 提交公司视图 (BusinessRegistrationBatch)")
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
