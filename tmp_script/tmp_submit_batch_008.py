"""
Batch 008 产业图与公司视图提交脚本
为 data/stock_batches/batch_008.json 中的10家中国公司构建产业实体图和公司视图。
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
    # ---- 氯化钾（藏格矿业）----
    {
        "node_id": "potassium_chloride",
        "canonical_name_zh": "氯化钾",
        "canonical_name_en": "Potassium Chloride",
        "aliases": ["钾肥", "KCl"],
        "definition": "一种重要的钾肥原料，由钾盐矿开采或盐湖卤水提取制得，是农业生产中钾元素的主要来源，也可用于工业生产和医药领域。",
        "entity_type": "material",
        "evidence": [ev("藏格矿业2024年年度报告", "主营业务为氯化钾的生产和销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 工业互联网平台（云鼎科技）----
    {
        "node_id": "industrial_internet_platform",
        "canonical_name_zh": "工业互联网平台",
        "canonical_name_en": "Industrial Internet Platform",
        "aliases": ["工业物联网平台", "智能制造平台"],
        "definition": "面向制造业数字化转型的综合性信息技术平台，通过物联网、大数据、人工智能等技术实现设备互联、生产监控、数据分析和智能决策，服务于矿山、能源、制造等行业。",
        "entity_type": "service",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务为工业互联网平台、智能矿山业务、智能洗选业务、智慧电力新能源业务、ERP实施及运维服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 智能矿山服务（云鼎科技）----
    {
        "node_id": "smart_mining_service",
        "canonical_name_zh": "智能矿山服务",
        "canonical_name_en": "Smart Mining Service",
        "aliases": ["智慧矿山服务", "矿山智能化服务"],
        "definition": "利用自动化、信息化和智能化技术对矿山开采、运输、安全监控和选矿等环节进行升级改造的专业技术服务，旨在提高矿山生产效率、保障安全生产和降低环境影响。",
        "entity_type": "service",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务包括智能矿山业务、智能洗选业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 机床（沈阳机床）----
    {
        "node_id": "machine_tool",
        "canonical_name_zh": "机床",
        "canonical_name_en": "Machine Tool",
        "aliases": ["数控机床", "金属切削机床", "加工中心"],
        "definition": "用于对金属或其他材料进行切削、成形、磨削等机械加工的基础制造装备，是装备制造业的核心工作母机，包括车床、铣床、加工中心、磨床等。",
        "entity_type": "device",
        "evidence": [ev("沈阳机床2024年年度报告", "主要产品包括卧式加工中心、立式加工中心、卧式数控车床、立式数控车床、行业专机等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 航空器（渤海租赁）----
    {
        "node_id": "aircraft",
        "canonical_name_zh": "航空器",
        "canonical_name_en": "Aircraft",
        "aliases": ["民用飞机", "商用客机", "货运飞机"],
        "definition": "用于民用航空运输的固定翼飞机，包括客运飞机和货运飞机，由机体、发动机、航电系统和起落架等子系统组成，是现代航空运输业的核心资产。",
        "entity_type": "device",
        "evidence": [ev("渤海租赁2024年年度报告", "主营业务为飞机租赁、集装箱租赁、基础设施租赁、大型设备租赁等租赁服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 粘胶纤维（吉林化纤）----
    {
        "node_id": "viscose_fiber",
        "canonical_name_zh": "粘胶纤维",
        "canonical_name_en": "Viscose Fiber",
        "aliases": ["人造纤维", "再生纤维素纤维", "粘胶丝"],
        "definition": "以天然纤维素（如木材、棉短绒）为原料，经化学处理后通过湿法纺丝制成的人造纤维，具有吸湿性好、穿着舒适等特点，广泛用于服装、家纺和产业用纺织品。",
        "entity_type": "material",
        "evidence": [ev("吉林化纤2024年年度报告", "主要业务为生产销售粘胶长丝和粘胶短纤维。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 烧碱（湖北宜化）----
    {
        "node_id": "caustic_soda",
        "canonical_name_zh": "烧碱",
        "canonical_name_en": "Caustic Soda",
        "aliases": ["氢氧化钠", "火碱", "苛性钠", "NaOH"],
        "definition": "一种重要的基础化工原料，由电解饱和食盐水制得，具有强碱性，广泛应用于造纸、纺织、肥皂、洗涤剂、石油精炼、水处理及化学合成等领域。",
        "entity_type": "material",
        "evidence": [ev("湖北宜化2024年年度报告", "主要产品包括烧碱、聚氯乙烯等化工产品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    # 氯化钾→化肥
    {
        "edge_id": "flow_potassium_to_fertilizer",
        "from_node": "potassium_chloride",
        "to_node": "chemical_fertilizer",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "氯化钾是生产复合肥和钾肥的核心原料，为农作物提供必需的钾营养元素。",
        "evidence": [ev("化肥产业常识", "氯化钾是重要的钾肥品种，可直接施用或作为复合肥的原料。")],
        "confidence": "HIGH",
    },
    # 钢材→机床
    {
        "edge_id": "flow_steel_to_machine_tool",
        "from_node": "steel_sheet",
        "to_node": "machine_tool",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "优质钢材和铸铁是制造机床床身、主轴、导轨及传动部件的主要结构材料。",
        "evidence": [ev("机床制造产业常识", "机床床身、立柱、横梁等大型结构件主要采用灰铸铁或树脂砂铸造，关键运动部件采用合金钢。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "zangge_mining",
        "name_zh": "藏格矿业股份有限公司",
        "name_en": "Zangge Mining Co., Ltd.",
        "aliases": ["藏格矿业"],
        "stock_codes": ["000408.SZ"],
        "description": "中国领先的钾肥生产企业之一，主营氯化钾的采选和销售，拥有青海察尔汗盐湖等优质钾盐资源。",
        "country": "CN", "province": "青海", "city": "海西蒙古族藏族自治州",
        "founded_year": 1996, "employee_count": 1733,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "yunding_tech",
        "name_zh": "云鼎科技股份有限公司",
        "name_en": "Yunding Technology Co., Ltd.",
        "aliases": ["云鼎科技"],
        "stock_codes": ["000409.SZ"],
        "description": "聚焦工业互联网和智能矿山领域的科技企业，为能源、矿山等行业提供工业互联网平台、智能化解决方案及ERP实施运维服务。",
        "country": "CN", "province": "山东", "city": "济南市",
        "founded_year": 1993, "employee_count": 1255,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shenyang_machine_tool",
        "name_zh": "沈阳机床股份有限公司",
        "name_en": "Shenyang Machine Tool Co., Ltd.",
        "aliases": ["沈阳机床"],
        "stock_codes": ["000410.SZ"],
        "description": "中国机床行业重点企业，主营数控机床及普通机床的研发、制造和销售，产品涵盖立式/卧式加工中心、数控车床及行业专用机床。",
        "country": "CN", "province": "辽宁", "city": "沈阳市",
        "founded_year": 1993, "employee_count": 2275,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "inte_group",
        "name_zh": "浙江英特集团股份有限公司",
        "name_en": "Zhejiang Inte Group Co., Ltd.",
        "aliases": ["英特集团"],
        "stock_codes": ["000411.SZ"],
        "description": "浙江省医药流通龙头企业，业务涵盖药品、医疗器械、保健品及中药材的批发与零售，同时涉及房地产开发和纺织品销售。",
        "country": "CN", "province": "浙江", "city": "杭州市",
        "founded_year": 1995, "employee_count": 3072,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "bohai_leasing",
        "name_zh": "渤海租赁股份有限公司",
        "name_en": "Bohai Leasing Co., Ltd.",
        "aliases": ["渤海租赁"],
        "stock_codes": ["000415.SZ"],
        "description": "中国领先的综合性租赁企业，主营飞机租赁、集装箱租赁、基础设施租赁及大型设备租赁，覆盖境内外市场，提供经营租赁和融资租赁服务。",
        "country": "CN", "province": "新疆", "city": "乌鲁木齐市",
        "founded_year": 1993, "employee_count": 580,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "hebai_group",
        "name_zh": "合肥百货大楼集团股份有限公司",
        "name_en": "Hefei Department Store Group Co., Ltd.",
        "aliases": ["合百集团"],
        "stock_codes": ["000417.SZ"],
        "description": "安徽省大型商业零售企业，主营业务涵盖百货商场和超市连锁经营，拥有多个区域性商业品牌。",
        "country": "CN", "province": "安徽", "city": "合肥市",
        "founded_year": 1996, "employee_count": 6676,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "tongcheng",
        "name_zh": "长沙通程控股股份有限公司",
        "name_en": "Changsha Tongcheng Holding Co., Ltd.",
        "aliases": ["通程控股"],
        "stock_codes": ["000419.SZ"],
        "description": "湖南省综合性商业企业，主营业务涵盖现代商贸零售和旅游酒店产业，拥有通程商业广场、通程温泉大酒店等品牌。",
        "country": "CN", "province": "湖南", "city": "长沙市",
        "founded_year": 1996, "employee_count": 1216,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "jilin_chemical_fiber",
        "name_zh": "吉林化纤股份有限公司",
        "name_en": "Jilin Chemical Fiber Co., Ltd.",
        "aliases": ["吉林化纤"],
        "stock_codes": ["000420.SZ"],
        "description": "中国粘胶纤维行业龙头企业，主营粘胶长丝和粘胶短纤维的生产与销售，产品广泛应用于纺织、服装和产业用纤维领域。",
        "country": "CN", "province": "吉林", "city": "吉林市",
        "founded_year": 1988, "employee_count": 5376,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "nanjing_public",
        "name_zh": "南京公用发展股份有限公司",
        "name_en": "Nanjing Public Utilities Development Co., Ltd.",
        "aliases": ["南京公用"],
        "stock_codes": ["000421.SZ"],
        "description": "南京市综合性公用事业企业，业务涵盖燃气供应、城市客运、房地产开发、旅游服务及商业零售。",
        "country": "CN", "province": "江苏", "city": "南京市",
        "founded_year": 1992, "employee_count": 2795,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "hubei_yihua",
        "name_zh": "湖北宜化化工股份有限公司",
        "name_en": "Hubei Yihua Chemical Industry Co., Ltd.",
        "aliases": ["湖北宜化"],
        "stock_codes": ["000422.SZ"],
        "description": "中国大型综合性化工企业，主营化肥（尿素、磷肥）、氯碱化工（聚氯乙烯、烧碱）及精细化工产品的生产和销售。",
        "country": "CN", "province": "湖北", "city": "宜昌市",
        "founded_year": 1993, "employee_count": 7460,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 藏格矿业 ----
    {
        "exposure_id": "zangge_produce_potassium",
        "company_id": "zangge_mining",
        "node_id": "potassium_chloride",
        "activity_type": "produce",
        "role": "氯化钾生产商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("藏格矿业2024年年度报告", "主营业务为氯化钾的生产和销售。")],
        "status": "ACTIVE",
    },
    # ---- 云鼎科技 ----
    {
        "exposure_id": "yunding_provide_industrial_internet",
        "company_id": "yunding_tech",
        "node_id": "industrial_internet_platform",
        "activity_type": "provide_service",
        "role": "工业互联网平台服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务为工业互联网平台。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yunding_provide_smart_mining",
        "company_id": "yunding_tech",
        "node_id": "smart_mining_service",
        "activity_type": "provide_service",
        "role": "智能矿山解决方案提供商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务包括智能矿山业务、智能洗选业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yunding_provide_cloud",
        "company_id": "yunding_tech",
        "node_id": "cloud_solution",
        "activity_type": "provide_service",
        "role": "云计算解决方案提供商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务包括智慧电力新能源业务、ERP实施及运维服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yunding_provide_it_integration",
        "company_id": "yunding_tech",
        "node_id": "information_system_integration",
        "activity_type": "provide_service",
        "role": "信息系统集成服务商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("云鼎科技2024年年度报告", "主要业务包括ERP实施及运维服务。")],
        "status": "ACTIVE",
    },
    # ---- 沈阳机床 ----
    {
        "exposure_id": "shenyang_manufacture_machine_tool",
        "company_id": "shenyang_machine_tool",
        "node_id": "machine_tool",
        "activity_type": "manufacture",
        "role": "数控机床制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("沈阳机床2024年年度报告", "主要产品包括卧式加工中心、立式加工中心、卧式数控车床、立式数控车床、行业专机等。")],
        "status": "ACTIVE",
    },
    # ---- 英特集团 ----
    {
        "exposure_id": "inte_provide_pharma_dist",
        "company_id": "inte_group",
        "node_id": "pharmaceutical_distribution",
        "activity_type": "provide_service",
        "role": "医药流通服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("英特集团2024年年度报告", "主要业务包括药品、保健品、医疗器械、中成药和药材的生产、销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "inte_provide_medical_device",
        "company_id": "inte_group",
        "node_id": "medical_device",
        "activity_type": "provide_service",
        "role": "医疗器械流通商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("英特集团2024年年度报告", "主要业务包括医疗器械的销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "inte_provide_tcm",
        "company_id": "inte_group",
        "node_id": "traditional_chinese_medicine",
        "activity_type": "provide_service",
        "role": "中成药流通商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("英特集团2024年年度报告", "主要业务包括中成药和药材的销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "inte_provide_textile",
        "company_id": "inte_group",
        "node_id": "textile_product",
        "activity_type": "provide_service",
        "role": "纺织品销售商",
        "weight": 0.3, "confidence": "HIGH",
        "evidence": [ev("英特集团2024年年度报告", "主要业务包括印染、服装的销售业务。")],
        "status": "ACTIVE",
    },
    # ---- 渤海租赁 ----
    {
        "exposure_id": "bohai_operate_aircraft",
        "company_id": "bohai_leasing",
        "node_id": "aircraft",
        "activity_type": "operate",
        "role": "飞机租赁资产运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("渤海租赁2024年年度报告", "主营业务为飞机租赁、集装箱租赁、基础设施租赁、大型设备租赁等租赁服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "bohai_operate_container",
        "company_id": "bohai_leasing",
        "node_id": "container",
        "activity_type": "operate",
        "role": "集装箱租赁资产运营商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("渤海租赁2024年年度报告", "主营业务包括集装箱租赁服务。")],
        "status": "ACTIVE",
    },
    # ---- 合百集团 ----
    {
        "exposure_id": "hebai_provide_retail",
        "company_id": "hebai_group",
        "node_id": "chain_retail_service",
        "activity_type": "provide_service",
        "role": "百货及超市零售商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("合百集团2024年年度报告", "主要业务为商业（百货业、超市）。")],
        "status": "ACTIVE",
    },
    # ---- 通程控股 ----
    {
        "exposure_id": "tongcheng_provide_retail",
        "company_id": "tongcheng",
        "node_id": "chain_retail_service",
        "activity_type": "provide_service",
        "role": "现代商贸零售商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("通程控股2024年年度报告", "主要业务为现代商贸。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tongcheng_operate_hotel",
        "company_id": "tongcheng",
        "node_id": "hotel_operation_service",
        "activity_type": "operate",
        "role": "酒店运营商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("通程控股2024年年度报告", "主要业务包括旅游酒店产业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tongcheng_operate_tourism",
        "company_id": "tongcheng",
        "node_id": "tourism_service",
        "activity_type": "operate",
        "role": "旅游服务运营商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("通程控股2024年年度报告", "主要业务包括旅游酒店产业。")],
        "status": "ACTIVE",
    },
    # ---- 吉林化纤 ----
    {
        "exposure_id": "jilin_manufacture_viscose",
        "company_id": "jilin_chemical_fiber",
        "node_id": "viscose_fiber",
        "activity_type": "manufacture",
        "role": "粘胶纤维制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("吉林化纤2024年年度报告", "主要业务为生产销售粘胶长丝和粘胶短纤维。")],
        "status": "ACTIVE",
    },
    # ---- 南京公用 ----
    {
        "exposure_id": "nanjing_produce_property",
        "company_id": "nanjing_public",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("南京公用2024年年度报告", "主要业务包括房产开发。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "nanjing_operate_tourism",
        "company_id": "nanjing_public",
        "node_id": "tourism_service",
        "activity_type": "operate",
        "role": "旅游服务运营商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("南京公用2024年年度报告", "主要业务包括旅游服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "nanjing_provide_retail",
        "company_id": "nanjing_public",
        "node_id": "chain_retail_service",
        "activity_type": "provide_service",
        "role": "商业零售运营商",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("南京公用2024年年度报告", "主要业务包括商业。")],
        "status": "ACTIVE",
    },
    # ---- 湖北宜化 ----
    {
        "exposure_id": "yihua_manufacture_fertilizer",
        "company_id": "hubei_yihua",
        "node_id": "chemical_fertilizer",
        "activity_type": "manufacture",
        "role": "化肥制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("湖北宜化2024年年度报告", "主要产品包括尿素、磷酸二铵等化肥产品。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yihua_manufacture_plastic",
        "company_id": "hubei_yihua",
        "node_id": "plastic_resin",
        "activity_type": "manufacture",
        "role": "聚氯乙烯制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("湖北宜化2024年年度报告", "主要产品包括聚氯乙烯。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yihua_manufacture_caustic",
        "company_id": "hubei_yihua",
        "node_id": "caustic_soda",
        "activity_type": "manufacture",
        "role": "烧碱制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("湖北宜化2024年年度报告", "主要产品包括烧碱。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_008_industrial_graph",
        "task_description": "Batch 008: 为10家中国公司构建产业实体图，涵盖钾肥、工业互联网、数控机床、医药流通、航空租赁、商业零售、粘胶纤维、氯碱化工等产业链。",
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
        "batch_id": "batch_008_company_views",
        "task_description": "Batch 008: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
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
    print("Batch 008 产业图与公司视图提交")
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
