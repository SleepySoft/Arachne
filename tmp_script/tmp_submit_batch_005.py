"""
Batch 005 产业图与公司视图提交脚本
为 data/stock_batches/batch_005.json 中的10家中国公司构建产业实体图和公司视图。
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
    # ---- 铅锌产业链（中金岭南）----
    {
        "node_id": "lead_zinc_ore",
        "canonical_name_zh": "铅锌矿石",
        "canonical_name_en": "Lead-Zinc Ore",
        "aliases": ["铅锌矿", "铅锌精矿"],
        "definition": "含有铅、锌等有价金属的矿石，经过采选后成为冶炼铅锌金属的主要原料，常伴生银、金等贵金属及硫元素。",
        "entity_type": "material",
        "evidence": [ev("中金岭南2024年年度报告", "公司主要业务为铅锌矿的采矿、选矿以及铅锌金属的冶炼。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "lead_zinc_metal",
        "canonical_name_zh": "铅锌金属",
        "canonical_name_en": "Lead-Zinc Metal",
        "aliases": ["铅锭", "锌锭", "锌合金", "铅锌锭"],
        "definition": "由铅锌矿石经冶炼工艺提取的金属产品，包括铅锭、锌锭及锌合金等，是蓄电池、镀锌、压铸等行业的基础原材料。",
        "entity_type": "material",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括铅锭、锌锭及锌合金、白银、黄金、镉锭、锗锭、铟锭、工业硫酸、硫磺等产品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "sulfuric_acid",
        "canonical_name_zh": "工业硫酸",
        "canonical_name_en": "Sulfuric Acid",
        "aliases": ["硫酸", "浓硫酸"],
        "definition": "一种重要的基础化工原料，由含硫矿石或冶炼烟气制酸工艺生产，广泛应用于化肥、冶金、石油化工、纺织等行业。",
        "entity_type": "material",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括工业硫酸、硫磺等产品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 农产品批发服务（农产品）----
    {
        "node_id": "agricultural_wholesale_service",
        "canonical_name_zh": "农产品批发服务",
        "canonical_name_en": "Agricultural Wholesale Service",
        "aliases": ["农批市场服务", "农产品流通服务"],
        "definition": "为农产品生产者与采购商提供集中交易场所、冷链仓储、物流配送、质量检测等配套服务的批发流通业态。",
        "entity_type": "service",
        "evidence": [ev("农产品2024年年度报告", "公司主要业务为农产品批发市场、商场销售、农产品加工生产养殖、农产品配套服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 电子元器件分销服务（深圳华强）----
    {
        "node_id": "electronic_component_distribution_service",
        "canonical_name_zh": "电子元器件分销服务",
        "canonical_name_en": "Electronic Component Distribution Service",
        "aliases": ["元器件分销", "电子分销服务"],
        "definition": "为电子元器件制造商与下游电子产品生产商之间提供采购、仓储、物流、技术支持及供应链管理的分销中介服务。",
        "entity_type": "service",
        "evidence": [ev("深圳华强2024年年度报告", "主营业务为电子元器件线下分销、电子元器件线上交易平台、电子元器件及电子终端产品线下交易平台等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 电信软件（中兴通讯）----
    {
        "node_id": "telecom_software",
        "canonical_name_zh": "电信软件",
        "canonical_name_en": "Telecommunication Software",
        "aliases": ["通信软件", "电信业务软件"],
        "definition": "支撑电信网络运营、管理和业务交付的软件系统，包括核心网软件、网管系统、运营支撑系统（OSS/BSS）及电信应用软件等。",
        "entity_type": "application_system",
        "evidence": [ev("中兴通讯2024年年度报告", "主要业务为电信软件服务开发生产。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 电脑及外设（中国长城）----
    {
        "node_id": "desktop_computer",
        "canonical_name_zh": "台式电脑",
        "canonical_name_en": "Desktop Computer",
        "aliases": ["台式机", "PC主机", "桌面计算机"],
        "definition": "放置在固定工作场所使用的个人计算机，通常由主机、显示器、键盘和鼠标组成，广泛应用于办公、教育、设计等场景。",
        "entity_type": "device",
        "evidence": [ev("中国长城2024年年度报告", "主要产品为电脑及外设、技术服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "computer_peripheral",
        "canonical_name_zh": "电脑外设",
        "canonical_name_en": "Computer Peripheral",
        "aliases": ["计算机外设", "电脑配件"],
        "definition": "与计算机主机配合使用的外部设备，包括显示器、打印机、扫描仪、键盘、鼠标及各类扩展接口设备等。",
        "entity_type": "device",
        "evidence": [ev("中国长城2024年年度报告", "主要产品为电脑及外设、技术服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 环保设备及材料（华控赛格）----
    {
        "node_id": "environmental_protection_equipment",
        "canonical_name_zh": "环保设备",
        "canonical_name_en": "Environmental Protection Equipment",
        "aliases": ["环境保护设备", "污染治理设备"],
        "definition": "用于防治环境污染、改善生态环境质量的专用设备和装置，包括污水处理设备、废气处理设备、固废处理设备及环境监测仪器等。",
        "entity_type": "device",
        "evidence": [ev("华控赛格2024年年度报告", "主要业务为节能环保、新材料行业，主要产品为环保设备及材料、技术咨询规划服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "environmental_protection_material",
        "canonical_name_zh": "环保材料",
        "canonical_name_en": "Environmental Protection Material",
        "aliases": ["环境功能材料", "绿色材料"],
        "definition": "具有特定环境功能或可降低环境负荷的新型材料，包括水处理滤料、吸附材料、可降解材料及节能保温材料等。",
        "entity_type": "material",
        "evidence": [ev("华控赛格2024年年度报告", "主要业务为节能环保、新材料行业，主要产品为环保设备及材料。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 旅游服务（华侨城A）----
    {
        "node_id": "tourism_service",
        "canonical_name_zh": "旅游服务",
        "canonical_name_en": "Tourism Service",
        "aliases": ["旅游综合服务", "文旅服务"],
        "definition": "围绕旅游活动提供的综合性服务，包括景区运营、酒店住宿、餐饮娱乐、旅游交通、旅行社服务及文旅项目开发等。",
        "entity_type": "service",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 纸包装产品（华侨城A）----
    {
        "node_id": "paper_packaging_product",
        "canonical_name_zh": "纸包装制品",
        "canonical_name_en": "Paper Packaging Product",
        "aliases": ["纸质包装", "纸箱", "纸盒"],
        "definition": "以纸板、纸张为主要原料，通过印刷、模切、折叠、粘合等工艺制成的包装容器和制品，广泛用于食品、电子、快消品等领域的产品包装。",
        "entity_type": "component",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 光纤光缆及设备（特发信息）----
    {
        "node_id": "optical_fiber_cable",
        "canonical_name_zh": "光缆",
        "canonical_name_en": "Optical Fiber Cable",
        "aliases": ["光纤光缆", "通信光缆"],
        "definition": "由光纤（光导纤维）和护套结构组成的通信线缆，利用光的全反射原理传输光信号，是现代通信网络的核心传输介质。",
        "entity_type": "component",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为光缆、光传输设备、铝电解电容器、有线电视产品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "optical_transmission_equipment",
        "canonical_name_zh": "光传输设备",
        "canonical_name_en": "Optical Transmission Equipment",
        "aliases": ["光通信传输设备", "光传输系统"],
        "definition": "用于光信号传输、复用、放大和交换的通信设备，包括光端机、波分复用设备（WDM）、光放大器及光交叉连接设备等。",
        "entity_type": "device",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为光缆、光传输设备。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "electronic_capacitor",
        "canonical_name_zh": "电子电容器",
        "canonical_name_en": "Electronic Capacitor",
        "aliases": ["电容器", "铝电解电容", "电容"],
        "definition": "一种能够储存电荷的无源电子元器件，由两个导体电极和中间的绝缘介质组成，广泛应用于电源滤波、信号耦合、能量存储等电路中。",
        "entity_type": "component",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为铝电解电容器。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "cable_tv_equipment",
        "canonical_name_zh": "有线电视设备",
        "canonical_name_en": "Cable TV Equipment",
        "aliases": ["有线电视网络设备", "CATV设备"],
        "definition": "用于有线电视信号接收、传输、分配和用户接入的专用设备，包括光接收机、放大器、分支分配器、机顶盒及同轴电缆网络设备等。",
        "entity_type": "device",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为有线电视产品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 医药细分（ST海王）----
    {
        "node_id": "traditional_chinese_medicine",
        "canonical_name_zh": "中成药",
        "canonical_name_en": "Traditional Chinese Medicine",
        "aliases": ["中药制剂", "中成药产品"],
        "definition": "以中药材为原料，在中医药理论指导下，按规定的处方和工艺加工制成的一定剂型的中药制品，如丸、散、膏、丹、片、胶囊等。",
        "entity_type": "material",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括银杏叶片等中成药。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "biological_drug",
        "canonical_name_zh": "生物药",
        "canonical_name_en": "Biological Drug",
        "aliases": ["生物制品", "生物制药"],
        "definition": "利用生物技术（基因工程、细胞工程、发酵工程等）制备的医药产品，包括疫苗、血液制品、重组蛋白、单克隆抗体及细胞治疗产品等。",
        "entity_type": "material",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括α-2b干扰素、白介素等生物药。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    {
        "node_id": "dietary_supplement",
        "canonical_name_zh": "膳食补充剂",
        "canonical_name_en": "Dietary Supplement",
        "aliases": ["保健食品", "营养补充剂", "保健品"],
        "definition": "以补充维生素、矿物质、动植物提取物等成分为目的，具有特定保健功能的食品类产品，不以治疗疾病为目的。",
        "entity_type": "material",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括海王金樽、海王牛初乳等保健食品。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    # 铅锌产业链
    {
        "edge_id": "flow_lead_zinc_ore_to_metal",
        "from_node": "lead_zinc_ore",
        "to_node": "lead_zinc_metal",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "铅锌矿石经过采矿、选矿和冶炼工艺，提取出铅锭、锌锭等金属产品。",
        "evidence": [ev("中金岭南2024年年度报告", "公司主要业务为铅锌矿的采矿、选矿以及铅锌金属的冶炼。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_lead_zinc_ore_to_acid",
        "from_node": "lead_zinc_ore",
        "to_node": "sulfuric_acid",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "铅锌矿石中的硫元素在冶炼过程中转化为二氧化硫，经制酸工艺生产工业硫酸。",
        "evidence": [ev("有色金属冶炼工艺常识", "铅锌冶炼过程中，硫化矿焙烧产生的SO2烟气是制酸的主要原料。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_lead_zinc_ore_to_precious",
        "from_node": "lead_zinc_ore",
        "to_node": "precious_metal",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "铅锌矿石中常伴生银、金等贵金属，在冶炼过程中通过电解精炼等工艺回收提取。",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括白银、黄金等贵金属。")],
        "confidence": "HIGH",
    },
    # 农产品批发
    {
        "edge_id": "flow_agri_to_wholesale",
        "from_node": "agricultural_product",
        "to_node": "agricultural_wholesale_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "农产品通过批发市场服务进行集散、交易和流通，连接生产端与零售端。",
        "evidence": [ev("农产品2024年年度报告", "公司主要业务为农产品批发市场、农产品配套服务。")],
        "confidence": "HIGH",
    },
    # 电子元器件分销
    {
        "edge_id": "flow_semiconductor_to_distribution",
        "from_node": "semiconductor_device",
        "to_node": "electronic_component_distribution_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "半导体器件等电子元器件通过分销服务触达下游电子产品制造商，提供供应链支持。",
        "evidence": [ev("深圳华强2024年年度报告", "主营业务为电子元器件线下分销、电子元器件线上交易平台等。")],
        "confidence": "HIGH",
    },
    # 电脑及外设
    {
        "edge_id": "flow_semiconductor_to_desktop",
        "from_node": "semiconductor_device",
        "to_node": "desktop_computer",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "半导体器件（CPU、GPU、内存芯片等）是构成台式电脑的核心电子部件。",
        "evidence": [ev("计算机硬件产业常识", "台式计算机由CPU、内存、主板、硬盘、显卡等半导体及电子部件组装而成。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_semiconductor_to_peripheral",
        "from_node": "semiconductor_device",
        "to_node": "computer_peripheral",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "半导体芯片及控制电路是电脑外设（显示器、打印机等）实现功能的核心组件。",
        "evidence": [ev("计算机硬件产业常识", "现代电脑外设内部均集成控制芯片和信号处理电路。")],
        "confidence": "HIGH",
    },
    # 环保设备
    {
        "edge_id": "flow_steel_to_env_equipment",
        "from_node": "steel_sheet",
        "to_node": "environmental_protection_equipment",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "钢材是制造环保设备外壳、支架及结构件的主要原材料。",
        "evidence": [ev("环保设备制造业常识", "污水处理设备、废气处理设备等环保装置大量使用碳钢和不锈钢材料制造。")],
        "confidence": "HIGH",
    },
    # 纸包装
    {
        "edge_id": "flow_packaging_material_to_paper_pack",
        "from_node": "packaging_material",
        "to_node": "paper_packaging_product",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "纸板、瓦楞纸等包装材料经过模切、印刷、折叠等工艺加工成纸箱、纸盒等纸包装制品。",
        "evidence": [ev("包装产业常识", "纸包装制品以纸板为主要原料，通过印刷、模切、粘合等工序制成。")],
        "confidence": "HIGH",
    },
    # 光纤光缆及设备
    {
        "edge_id": "flow_quartz_to_fiber_cable",
        "from_node": "quartz_sand",
        "to_node": "optical_fiber_cable",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "高纯度石英砂是制造光纤预制棒及光纤的核心原料，经高温熔融拉制成光导纤维。",
        "evidence": [ev("光纤通信产业常识", "光纤的主要原材料是高纯度二氧化硅（石英砂），经气相沉积等工艺制成预制棒后拉丝成纤。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_fiber_cable_to_transmission",
        "from_node": "optical_fiber_cable",
        "to_node": "optical_transmission_equipment",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "光缆作为光信号的传输介质，与光端机、波分复用器等设备组合构成完整的光传输系统。",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为光缆、光传输设备。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_aluminum_to_capacitor",
        "from_node": "aluminum_panel",
        "to_node": "electronic_capacitor",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "铝箔是铝电解电容器的关键原材料，经腐蚀、化成等工艺制成电容器的阳极和阴极箔。",
        "evidence": [ev("铝电解电容器制造工艺", "铝电解电容器的核心材料是高纯度铝箔（阳极箔和阴极箔）。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_capacitor_to_cable_tv",
        "from_node": "electronic_capacitor",
        "to_node": "cable_tv_equipment",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "电容器是有线电视设备电源电路和信号处理电路中不可或缺的基础电子元件。",
        "evidence": [ev("电子电路设计常识", "电容器广泛应用于电源滤波、信号耦合等电路模块中。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_semiconductor_to_cable_tv",
        "from_node": "semiconductor_device",
        "to_node": "cable_tv_equipment",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "description": "半导体芯片是有线电视设备（如机顶盒、光接收机）实现信号接收、解码和处理功能的核心部件。",
        "evidence": [ev("有线电视设备技术资料", "现代CATV设备大量使用ASIC、DSP等半导体芯片实现数字信号处理。")],
        "confidence": "HIGH",
    },
    # 医药细分
    {
        "edge_id": "flow_pharma_raw_to_tcm",
        "from_node": "pharmaceutical_raw_material",
        "to_node": "traditional_chinese_medicine",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "中药材及中药提取物等原料药经过制剂工艺加工成丸、散、膏、丹、片、胶囊等中成药产品。",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括银杏叶片等中成药。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_pharma_raw_to_biological",
        "from_node": "pharmaceutical_raw_material",
        "to_node": "biological_drug",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "生物原材料（如工程菌株、细胞系、血浆等）通过发酵、纯化等生物技术工艺制备成生物药品。",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括α-2b干扰素、白介素等生物药。")],
        "confidence": "HIGH",
    },
    {
        "edge_id": "flow_food_ingredient_to_supplement",
        "from_node": "food_ingredient",
        "to_node": "dietary_supplement",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "食品原料及营养素提取物经配方设计和加工制成具有特定保健功能的膳食补充剂。",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括海王金樽、海王牛初乳等保健食品。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "zhongjin_lingnan",
        "name_zh": "深圳市中金岭南有色金属股份有限公司",
        "name_en": "Shenzhen Zhongjin Lingnan Nonfemet Co., Ltd.",
        "aliases": ["中金岭南"],
        "stock_codes": ["000060.SZ"],
        "description": "中国领先的铅锌金属生产企业，业务涵盖铅锌矿的采矿、选矿、冶炼及综合回收，主要产品包括铅锭、锌锭、白银、黄金及工业硫酸等。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1984, "employee_count": 11432,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "nongchanpin",
        "name_zh": "深圳市农产品集团股份有限公司",
        "name_en": "Shenzhen Agricultural Products Group Co., Ltd.",
        "aliases": ["农产品"],
        "stock_codes": ["000061.SZ"],
        "description": "中国最大的农产品批发市场运营企业之一，业务涵盖农产品批发市场开发运营、农产品加工生产养殖及配套物流服务。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1989, "employee_count": 4838,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shenzhen_huaqiang",
        "name_zh": "深圳华强实业股份有限公司",
        "name_en": "Shenzhen Huaqiang Industry Co., Ltd.",
        "aliases": ["深圳华强"],
        "stock_codes": ["000062.SZ"],
        "description": "中国领先的电子元器件分销企业，构建了线上线下融合的电子元器件交易服务平台，同时开展品牌终端产品线上分销及创新创业服务。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1994, "employee_count": 1951,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "zte",
        "name_zh": "中兴通讯股份有限公司",
        "name_en": "ZTE Corporation",
        "aliases": ["中兴通讯", "ZTE"],
        "stock_codes": ["000063.SZ", "0763.HK"],
        "description": "全球领先的综合通信与信息技术解决方案提供商，业务涵盖无线通信、有线交换与接入、光通信、数据通信、智能终端及电信软件等领域。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1985, "employee_count": 65095,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "norinco_international",
        "name_zh": "北方国际合作股份有限公司",
        "name_en": "Norinco International Cooperation Ltd.",
        "aliases": ["北方国际"],
        "stock_codes": ["000065.SZ"],
        "description": "中国兵器工业集团旗下国际工程承包平台，主要从事国际工程承包、国内建筑安装及重型装备出口业务。",
        "country": "CN", "province": "北京", "city": "北京市",
        "founded_year": 1986, "employee_count": 3812,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "china_greatwall",
        "name_zh": "中国长城科技集团股份有限公司",
        "name_en": "China Greatwall Technology Group Co., Ltd.",
        "aliases": ["中国长城"],
        "stock_codes": ["000066.SZ"],
        "description": "中国电子信息产业集团旗下网信产业核心企业，主要从事自主安全电脑及外设、服务器、网络设备等产品的研发、生产和销售，是国产信创领域的重要力量。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1997, "employee_count": 13370,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huakong_saige",
        "name_zh": "深圳华控赛格股份有限公司",
        "name_en": "Shenzhen Huakong Seg Co., Ltd.",
        "aliases": ["华控赛格"],
        "stock_codes": ["000068.SZ"],
        "description": "专注于节能环保设备及新材料研发制造的企业，同时提供环保技术咨询规划服务，产品涵盖污水处理设备、废气治理设备及环境功能材料等。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1997, "employee_count": 377,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "overseas_chinese_town",
        "name_zh": "深圳华侨城股份有限公司",
        "name_en": "Overseas Chinese Town Enterprise Co., Ltd.",
        "aliases": ["华侨城A"],
        "stock_codes": ["000069.SZ"],
        "description": "中国文化旅游产业领军企业，业务涵盖旅游综合开发运营、房地产及纸包装制造，拥有欢乐谷、世界之窗等知名文旅品牌。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1997, "employee_count": 16478,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "teli_information",
        "name_zh": "深圳市特发信息股份有限公司",
        "name_en": "Shenzhen Teleinformation Industry Co., Ltd.",
        "aliases": ["特发信息"],
        "stock_codes": ["000070.SZ"],
        "description": "光通信产业核心企业，主要产品包括光纤光缆、光传输设备、铝电解电容器及有线电视网络设备，服务于通信运营商和广电网络。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1999, "employee_count": 3113,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "st_neptunus",
        "name_zh": "深圳市海王生物工程股份有限公司",
        "name_en": "Shenzhen Neptunus Bioengineering Co., Ltd.",
        "aliases": ["ST海王", "海王生物"],
        "stock_codes": ["000078.SZ"],
        "description": "集医药制造、医药商业流通于一体的大型医药企业，产品涵盖中成药、生物药、化学药、保健食品及大输液等，拥有海王星辰连锁药房体系。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1992, "employee_count": 8264,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 中金岭南 ----
    {
        "exposure_id": "zhongjin_produce_lead_zinc_ore",
        "company_id": "zhongjin_lingnan",
        "node_id": "lead_zinc_ore",
        "activity_type": "produce",
        "role": "铅锌矿石开采商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中金岭南2024年年度报告", "公司主要业务为铅锌矿的采矿、选矿以及铅锌金属的冶炼。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongjin_manufacture_lead_zinc_metal",
        "company_id": "zhongjin_lingnan",
        "node_id": "lead_zinc_metal",
        "activity_type": "manufacture",
        "role": "铅锌金属冶炼商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括铅锭、锌锭及锌合金。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongjin_manufacture_sulfuric_acid",
        "company_id": "zhongjin_lingnan",
        "node_id": "sulfuric_acid",
        "activity_type": "manufacture",
        "role": "冶炼副产品硫酸生产商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括工业硫酸、硫磺等产品。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongjin_manufacture_precious_metal",
        "company_id": "zhongjin_lingnan",
        "node_id": "precious_metal",
        "activity_type": "manufacture",
        "role": "伴生贵金属回收商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("中金岭南2024年年度报告", "主要产品包括白银、黄金等贵金属。")],
        "status": "ACTIVE",
    },
    # ---- 农产品 ----
    {
        "exposure_id": "nongchanpin_provide_wholesale",
        "company_id": "nongchanpin",
        "node_id": "agricultural_wholesale_service",
        "activity_type": "provide_service",
        "role": "农产品批发市场运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("农产品2024年年度报告", "公司主要业务为农产品批发市场、商场销售、农产品配套服务。")],
        "status": "ACTIVE",
    },
    # ---- 深圳华强 ----
    {
        "exposure_id": "huaqiang_provide_distribution",
        "company_id": "shenzhen_huaqiang",
        "node_id": "electronic_component_distribution_service",
        "activity_type": "provide_service",
        "role": "电子元器件分销平台运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深圳华强2024年年度报告", "主营业务为电子元器件线下分销、电子元器件线上交易平台。")],
        "status": "ACTIVE",
    },
    # ---- 中兴通讯 ----
    {
        "exposure_id": "zte_manufacture_comm_device",
        "company_id": "zte",
        "node_id": "communication_device",
        "activity_type": "manufacture",
        "role": "通信设备制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中兴通讯2024年年度报告", "主要业务为无线通信系统、有线交换和接入系统、数据通讯系统、多媒体通讯系统、光通信系统、卫星及微波通讯系统。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zte_manufacture_network_equip",
        "company_id": "zte",
        "node_id": "network_equipment",
        "activity_type": "manufacture",
        "role": "网络设备制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中兴通讯2024年年度报告", "主要业务包括数据通讯系统、光通信系统等网络设备。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zte_manufacture_mobile_phone",
        "company_id": "zte",
        "node_id": "mobile_phone",
        "activity_type": "manufacture",
        "role": "移动通信终端制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中兴通讯2024年年度报告", "主要业务包括移动通信终端。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zte_provide_telecom_software",
        "company_id": "zte",
        "node_id": "telecom_software",
        "activity_type": "provide_service",
        "role": "电信软件与解决方案提供商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中兴通讯2024年年度报告", "主要业务包括电信软件服务开发生产。")],
        "status": "ACTIVE",
    },
    # ---- 北方国际 ----
    {
        "exposure_id": "norinco_provide_construction",
        "company_id": "norinco_international",
        "node_id": "construction_service",
        "activity_type": "provide_service",
        "role": "国际工程承包商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("北方国际2024年年度报告", "主要业务为国际工程承包、国内建筑安装、产品生产销售。")],
        "status": "ACTIVE",
    },
    # ---- 中国长城 ----
    {
        "exposure_id": "greatwall_manufacture_desktop",
        "company_id": "china_greatwall",
        "node_id": "desktop_computer",
        "activity_type": "manufacture",
        "role": "国产台式电脑制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中国长城2024年年度报告", "主要产品为电脑及外设、技术服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "greatwall_manufacture_laptop",
        "company_id": "china_greatwall",
        "node_id": "laptop_computer",
        "activity_type": "manufacture",
        "role": "国产笔记本电脑制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中国长城2024年年度报告", "主要产品为电脑及外设、技术服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "greatwall_manufacture_peripheral",
        "company_id": "china_greatwall",
        "node_id": "computer_peripheral",
        "activity_type": "manufacture",
        "role": "电脑外设制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中国长城2024年年度报告", "主要产品为电脑及外设、技术服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "greatwall_manufacture_server",
        "company_id": "china_greatwall",
        "node_id": "server_hardware",
        "activity_type": "manufacture",
        "role": "国产服务器制造商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("中国长城官网及产业常识", "中国长城作为信创核心企业，产品线涵盖自主安全服务器。")],
        "status": "ACTIVE",
    },
    # ---- 华控赛格 ----
    {
        "exposure_id": "huakong_manufacture_env_equip",
        "company_id": "huakong_saige",
        "node_id": "environmental_protection_equipment",
        "activity_type": "manufacture",
        "role": "环保设备制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华控赛格2024年年度报告", "主要业务为节能环保、新材料行业，主要产品为环保设备及材料。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huakong_manufacture_env_material",
        "company_id": "huakong_saige",
        "node_id": "environmental_protection_material",
        "activity_type": "manufacture",
        "role": "环保新材料制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("华控赛格2024年年度报告", "主要业务为节能环保、新材料行业，主要产品为环保设备及材料。")],
        "status": "ACTIVE",
    },
    # ---- 华侨城A ----
    {
        "exposure_id": "oct_operate_tourism",
        "company_id": "overseas_chinese_town",
        "node_id": "tourism_service",
        "activity_type": "operate",
        "role": "文旅综合运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "oct_produce_residential",
        "company_id": "overseas_chinese_town",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "oct_produce_commercial",
        "company_id": "overseas_chinese_town",
        "node_id": "commercial_property",
        "activity_type": "produce",
        "role": "商业地产开发商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "oct_manufacture_paper_pack",
        "company_id": "overseas_chinese_town",
        "node_id": "paper_packaging_product",
        "activity_type": "manufacture",
        "role": "纸包装制品制造商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("华侨城A2024年年度报告", "主营业务为旅游综合、房地产和纸包装业。")],
        "status": "ACTIVE",
    },
    # ---- 特发信息 ----
    {
        "exposure_id": "teli_manufacture_fiber_cable",
        "company_id": "teli_information",
        "node_id": "optical_fiber_cable",
        "activity_type": "manufacture",
        "role": "光缆制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为光缆、光传输设备。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "teli_manufacture_optical_trans",
        "company_id": "teli_information",
        "node_id": "optical_transmission_equipment",
        "activity_type": "manufacture",
        "role": "光传输设备制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为光缆、光传输设备。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "teli_manufacture_capacitor",
        "company_id": "teli_information",
        "node_id": "electronic_capacitor",
        "activity_type": "manufacture",
        "role": "铝电解电容器制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为铝电解电容器。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "teli_manufacture_cable_tv",
        "company_id": "teli_information",
        "node_id": "cable_tv_equipment",
        "activity_type": "manufacture",
        "role": "有线电视设备制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("特发信息2024年年度报告", "主要产品为有线电视产品。")],
        "status": "ACTIVE",
    },
    # ---- ST海王 ----
    {
        "exposure_id": "neptunus_provide_pharma_dist",
        "company_id": "st_neptunus",
        "node_id": "pharmaceutical_distribution",
        "activity_type": "provide_service",
        "role": "医药商业流通商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("ST海王2024年年度报告", "主要业务为医药制造、医药商业流通。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "neptunus_manufacture_pharma",
        "company_id": "st_neptunus",
        "node_id": "pharmaceutical_product",
        "activity_type": "manufacture",
        "role": "医药产品制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("ST海王2024年年度报告", "主要业务为医药制造、医药商业流通。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "neptunus_manufacture_tcm",
        "company_id": "st_neptunus",
        "node_id": "traditional_chinese_medicine",
        "activity_type": "manufacture",
        "role": "中成药制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括银杏叶片等中成药。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "neptunus_manufacture_biological",
        "company_id": "st_neptunus",
        "node_id": "biological_drug",
        "activity_type": "manufacture",
        "role": "生物药制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括α-2b干扰素、白介素等生物药。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "neptunus_manufacture_supplement",
        "company_id": "st_neptunus",
        "node_id": "dietary_supplement",
        "activity_type": "manufacture",
        "role": "保健食品制造商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("ST海王2024年年度报告", "主要产品包括海王金樽、海王牛初乳等保健食品。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_005_industrial_graph",
        "task_description": "Batch 005: 为10家中国公司构建产业实体图，涵盖铅锌冶炼、农产品批发、电子元器件分销、通信设备、电脑外设、环保设备、旅游服务、光通信、医药等产业链。",
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
        "batch_id": "batch_005_company_views",
        "task_description": "Batch 005: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
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
    print("Batch 005 产业图与公司视图提交")
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
