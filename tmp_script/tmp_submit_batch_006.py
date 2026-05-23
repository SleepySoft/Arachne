"""
Batch 006 产业图与公司视图提交脚本
为 data/stock_batches/batch_006.json 中的10家中国公司构建产业实体图和公司视图。
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
    # ---- 商品混凝土（盐田港）----
    {
        "node_id": "ready_mixed_concrete",
        "canonical_name_zh": "商品混凝土",
        "canonical_name_en": "Ready-Mixed Concrete",
        "aliases": ["商砼", "预拌混凝土"],
        "definition": "在搅拌站集中生产，通过搅拌运输车送至施工现场浇筑的混凝土拌合物，是现代建筑工程的主要结构材料之一。",
        "entity_type": "material",
        "evidence": [ev("盐田港2024年年度报告", "主要业务包括商品混凝土生产业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 机场运营服务（深圳机场）----
    {
        "node_id": "airport_operation_service",
        "canonical_name_zh": "机场运营服务",
        "canonical_name_en": "Airport Operation Service",
        "aliases": ["航空港运营", "机场地面服务"],
        "definition": "为航空公司和旅客提供的机场基础设施管理与运营服务，包括航班起降保障、旅客服务、行李处理、地面交通协调、商业租赁及航空货运服务等。",
        "entity_type": "service",
        "evidence": [ev("深圳机场2024年年度报告", "主要业务为航空主业以及航空主业延伸出的非航空业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 液化石油气（广聚能源）----
    {
        "node_id": "lpg",
        "canonical_name_zh": "液化石油气",
        "canonical_name_en": "Liquefied Petroleum Gas",
        "aliases": ["LPG", "液化气"],
        "definition": "由丙烷、丁烷等低碳烃类组成的石油炼化副产品，在加压或低温条件下液化，广泛用于民用燃气、工业燃料及化工原料。",
        "entity_type": "material",
        "evidence": [ev("广聚能源2024年年度报告", "主要业务为石油制品、液化石油气销售及电力投资。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 通用航空服务（中信海直）----
    {
        "node_id": "general_aviation_service",
        "canonical_name_zh": "通用航空服务",
        "canonical_name_en": "General Aviation Service",
        "aliases": ["通航服务", "通用航空运营"],
        "definition": "使用民用航空器从事公共航空运输以外的民用航空活动，包括石油服务、医疗救护、空中游览、航空摄影、城市消防、航空护林、科学实验及私人飞行等。",
        "entity_type": "service",
        "evidence": [ev("中信海直2024年年度报告", "主要业务为通航飞行业务和维修业务，包括石油服务、直升机引航、医疗救护、空中游览等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- OLED面板（TCL科技）----
    {
        "node_id": "oled_panel",
        "canonical_name_zh": "OLED面板",
        "canonical_name_en": "OLED Panel",
        "aliases": ["有机发光二极管面板", "柔性OLED面板"],
        "definition": "采用有机发光二极管技术自发光的有源矩阵显示面板，无需背光源，具有对比度高、响应速度快、可柔性折叠等特点，广泛应用于智能手机、智能穿戴及车载显示。",
        "entity_type": "component",
        "evidence": [ev("TCL科技2024年年度报告", "公司半导体显示业务涵盖LCD和OLED面板，柔性OLED面板加速向智能手机中端市场渗透。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 危废处理（中成股份）----
    {
        "node_id": "hazardous_waste_treatment_service",
        "canonical_name_zh": "危险废物处理服务",
        "canonical_name_en": "Hazardous Waste Treatment Service",
        "aliases": ["危废处置服务", "危废处理"],
        "definition": "对具有毒性、腐蚀性、易燃性、反应性或感染性等危险特性的废物进行专业化收集、运输、贮存、处理和最终处置的环保服务。",
        "entity_type": "service",
        "evidence": [ev("中成股份2024年年度报告", "业务范围包括危险废物经营、固体废物治理、再生资源回收等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 再生资源回收（中成股份）----
    {
        "node_id": "recycling_service",
        "canonical_name_zh": "再生资源回收服务",
        "canonical_name_en": "Recycling Service",
        "aliases": ["资源再生服务", "废品回收利用"],
        "definition": "对废旧金属、塑料、纸张等可再生资源进行回收、分拣、加工和再利用的循环经济服务，旨在减少原生资源消耗和环境污染。",
        "entity_type": "service",
        "evidence": [ev("中成股份2024年年度报告", "业务范围包括再生资源回收、再生资源加工、再生资源销售等。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 化学药（丰原药业）----
    {
        "node_id": "chemical_drug",
        "canonical_name_zh": "化学药",
        "canonical_name_en": "Chemical Drug",
        "aliases": ["化学合成药", "化学药品"],
        "definition": "通过化学合成或从天然产物中提取分离制得的具有明确化学结构和药理活性的药物，包括原料药及其各种剂型制剂。",
        "entity_type": "material",
        "evidence": [ev("丰原药业2024年年度报告", "主要产品包括化学合成药及其制剂。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 有线电视网络服务（华数传媒）----
    {
        "node_id": "cable_tv_network_service",
        "canonical_name_zh": "有线电视网络服务",
        "canonical_name_en": "Cable TV Network Service",
        "aliases": ["有线电视服务", "广电网络服务"],
        "definition": "通过同轴电缆或光纤混合网向用户提供电视节目传输、视频点播、宽带接入等综合信息服务的网络运营业务。",
        "entity_type": "service",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务为杭州地区有线电视网络业务、宽带网络业务及全国范围内的新媒体业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 宽带网络服务（华数传媒）----
    {
        "node_id": "broadband_network_service",
        "canonical_name_zh": "宽带网络服务",
        "canonical_name_en": "Broadband Network Service",
        "aliases": ["宽带接入服务", "互联网接入服务"],
        "definition": "通过光纤、同轴电缆或无线等方式向终端用户提供高速互联网接入及数据通信服务的电信业务。",
        "entity_type": "service",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务包括宽带网络业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 新媒体服务（华数传媒）----
    {
        "node_id": "new_media_service",
        "canonical_name_zh": "新媒体服务",
        "canonical_name_en": "New Media Service",
        "aliases": ["数字媒体服务", "网络视听服务"],
        "definition": "基于互联网、移动互联网和数字技术提供的互动式内容传播服务，包括网络视频、OTT电视、手机电视、短视频及互动娱乐等。",
        "entity_type": "service",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务包括全国范围内的新媒体业务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    # 炼油产出LPG
    {
        "edge_id": "flow_refinery_to_lpg",
        "from_node": "refining_service",
        "to_node": "lpg",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "石油炼化过程将原油中的轻质烃类分离并加压液化，产出液化石油气（LPG）。",
        "evidence": [ev("石油化工产业常识", "LPG是石油炼制过程中的重要副产品，主要来自常减压蒸馏和催化裂化装置。")],
        "confidence": "HIGH",
    },
    # 原料药→化学药
    {
        "edge_id": "flow_pharma_raw_to_chemical",
        "from_node": "pharmaceutical_raw_material",
        "to_node": "chemical_drug",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "化学原料药经过合成、纯化、制剂等工艺加工成片剂、胶囊、注射剂等化学药品制剂。",
        "evidence": [ev("丰原药业2024年年度报告", "主要产品包括化学合成药及其制剂。")],
        "confidence": "HIGH",
    },
    # 有线电视设备→网络服务
    {
        "edge_id": "flow_cable_tv_equip_to_network",
        "from_node": "cable_tv_equipment",
        "to_node": "cable_tv_network_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "有线电视网络设备（光接收机、放大器、机顶盒等）是构建和运营有线电视网络服务的基础设施。",
        "evidence": [ev("广电网络技术常识", "有线电视网络服务依赖HFC网络设备、光节点、机顶盒等终端和传输设备。")],
        "confidence": "HIGH",
    },
    # 网络设备→宽带服务
    {
        "edge_id": "flow_network_equip_to_broadband",
        "from_node": "network_equipment",
        "to_node": "broadband_network_service",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "description": "宽带接入网设备（OLT、ONU、路由器等）是提供宽带网络服务的核心基础设施。",
        "evidence": [ev("宽带接入技术常识", "光纤宽带服务通过OLT、分光器、ONU等网络设备实现用户接入。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "yantian_port",
        "name_zh": "深圳市盐田港股份有限公司",
        "name_en": "Shenzhen Yantian Port Holdings Co., Ltd.",
        "aliases": ["盐田港"],
        "stock_codes": ["000088.SZ"],
        "description": "深圳港核心港区运营商，业务涵盖集装箱码头装卸、高速公路运输、隧道疏港运输、仓储物流及商品混凝土生产等港口综合物流业务。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1997, "employee_count": 895,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shenzhen_airport",
        "name_zh": "深圳市机场股份有限公司",
        "name_en": "Shenzhen Airport Co., Ltd.",
        "aliases": ["深圳机场"],
        "stock_codes": ["000089.SZ"],
        "description": "深圳宝安国际机场的运营主体，主营航空客运与货运地面保障服务，同时拓展航空商务服务、广告、商业租赁及非航空业务。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1998, "employee_count": 5446,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "tianjian_group",
        "name_zh": "深圳市天健(集团)股份有限公司",
        "name_en": "Shenzhen Tianjian Group Co., Ltd.",
        "aliases": ["天健集团"],
        "stock_codes": ["000090.SZ"],
        "description": "深圳市属国有城市建设与运营综合服务商，主营业务涵盖房地产开发与经营、市政工程建设和管理、城市基础设施投资运营。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1993, "employee_count": 10052,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "guangju_energy",
        "name_zh": "深圳市广聚能源股份有限公司",
        "name_en": "Shenzhen Guangju Energy Co., Ltd.",
        "aliases": ["广聚能源"],
        "stock_codes": ["000096.SZ"],
        "description": "深圳市能源贸易与投资企业，主营石油制品零售批发、液化石油气（LPG）销售及电力项目投资运营。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1999, "employee_count": 328,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "citic_offshore_helicopter",
        "name_zh": "中信海洋直升机股份有限公司",
        "name_en": "Citic Offshore Helicopter Co., Ltd.",
        "aliases": ["中信海直"],
        "stock_codes": ["000099.SZ"],
        "description": "中国规模最大的通用航空运营企业之一，主营海上石油飞行服务、直升机引航、医疗救护、空中游览、航空器代管及通航维修业务。",
        "country": "CN", "province": "广东", "city": "深圳市",
        "founded_year": 1999, "employee_count": 1094,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "tcl_technology",
        "name_zh": "TCL科技集团股份有限公司",
        "name_en": "TCL Technology Group Corporation",
        "aliases": ["TCL科技"],
        "stock_codes": ["000100.SZ"],
        "description": "全球领先的半导体显示及新能源光伏科技企业，核心主业为半导体显示器件（TCL华星）和新能源光伏及硅材料（TCL中环），2024年半导体显示业务营收超1,043亿元。",
        "country": "CN", "province": "广东", "city": "惠州市",
        "founded_year": 1982, "employee_count": 71419,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "zhongcheng",
        "name_zh": "中成进出口股份有限公司",
        "name_en": "China National Complete Plant Import & Export Corporation Ltd.",
        "aliases": ["中成股份"],
        "stock_codes": ["000151.SZ"],
        "description": "中国成套设备与技术进出口企业，业务涵盖国际工程承包、固废治理、危险废物经营、再生资源回收及环保技术服务。",
        "country": "CN", "province": "北京", "city": "北京市",
        "founded_year": 1999, "employee_count": 698,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "fengyuan_pharmaceutical",
        "name_zh": "安徽丰原药业股份有限公司",
        "name_en": "Anhui Fengyuan Pharmaceutical Co., Ltd.",
        "aliases": ["丰原药业"],
        "stock_codes": ["000153.SZ"],
        "description": "综合性医药制造企业，产品涵盖中药制剂、化学合成药制剂及生物药制剂，拥有从原料药到制剂的完整产业链。",
        "country": "CN", "province": "安徽", "city": "芜湖市",
        "founded_year": 1997, "employee_count": 4542,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "chuanneng_power",
        "name_zh": "四川省新能源动力股份有限公司",
        "name_en": "Sichuan Chuanneng Power Co., Ltd.",
        "aliases": ["川能动力"],
        "stock_codes": ["000155.SZ"],
        "description": "四川省新能源发电投资运营平台，主营风力发电和光伏发电项目的开发、建设和运营。",
        "country": "CN", "province": "四川", "city": "成都市",
        "founded_year": 1997, "employee_count": 2139,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huashu_media",
        "name_zh": "华数传媒控股股份有限公司",
        "name_en": "Huashu Media Holding Co., Ltd.",
        "aliases": ["华数传媒"],
        "stock_codes": ["000156.SZ"],
        "description": "浙江省广电网络运营及新媒体服务龙头企业，业务涵盖杭州地区有线电视网络、宽带网络接入及全国范围的新媒体业务运营。",
        "country": "CN", "province": "浙江", "city": "杭州市",
        "founded_year": 1994, "employee_count": 11086,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 盐田港 ----
    {
        "exposure_id": "yantian_provide_container_handling",
        "company_id": "yantian_port",
        "node_id": "container_handling_service",
        "activity_type": "provide_service",
        "role": "集装箱码头装卸服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("盐田港2024年年度报告", "主要业务包括集装箱码头装卸业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yantian_provide_logistics",
        "company_id": "yantian_port",
        "node_id": "logistics_service",
        "activity_type": "provide_service",
        "role": "港口综合物流服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("盐田港2024年年度报告", "主要业务包括仓储、运输业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yantian_manufacture_concrete",
        "company_id": "yantian_port",
        "node_id": "ready_mixed_concrete",
        "activity_type": "manufacture",
        "role": "商品混凝土生产商",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("盐田港2024年年度报告", "主要业务包括商品混凝土生产业务。")],
        "status": "ACTIVE",
    },
    # ---- 深圳机场 ----
    {
        "exposure_id": "airport_operate_airport",
        "company_id": "shenzhen_airport",
        "node_id": "airport_operation_service",
        "activity_type": "operate",
        "role": "民用机场运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("深圳机场2024年年度报告", "主要业务为航空主业以及航空主业延伸出的非航空业务。")],
        "status": "ACTIVE",
    },
    # ---- 天健集团 ----
    {
        "exposure_id": "tianjian_produce_residential",
        "company_id": "tianjian_group",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅地产开发商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("天健集团2024年年度报告", "主营业务为房地产开发与经营。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tianjian_provide_construction",
        "company_id": "tianjian_group",
        "node_id": "construction_service",
        "activity_type": "provide_service",
        "role": "市政工程建设服务商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("天健集团2024年年度报告", "主营业务包括市政工程建设和管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tianjian_produce_commercial",
        "company_id": "tianjian_group",
        "node_id": "commercial_property",
        "activity_type": "produce",
        "role": "商业地产开发商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("天健集团2024年年度报告", "主营业务为房地产开发与经营。")],
        "status": "ACTIVE",
    },
    # ---- 广聚能源 ----
    {
        "exposure_id": "guangju_provide_petrochemical",
        "company_id": "guangju_energy",
        "node_id": "petrochemical_product",
        "activity_type": "provide_service",
        "role": "石油制品销售商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("广聚能源2024年年度报告", "主要业务为石油制品销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "guangju_provide_lpg",
        "company_id": "guangju_energy",
        "node_id": "lpg",
        "activity_type": "provide_service",
        "role": "液化石油气销售商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("广聚能源2024年年度报告", "主要业务包括液化石油气销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "guangju_operate_electricity",
        "company_id": "guangju_energy",
        "node_id": "electricity_power",
        "activity_type": "operate",
        "role": "电力投资运营商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("广聚能源2024年年度报告", "主要业务包括电力投资。")],
        "status": "ACTIVE",
    },
    # ---- 中信海直 ----
    {
        "exposure_id": "citic_provide_general_aviation",
        "company_id": "citic_offshore_helicopter",
        "node_id": "general_aviation_service",
        "activity_type": "provide_service",
        "role": "通用航空运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("中信海直2024年年度报告", "主要业务为通航飞行业务和维修业务，包括石油服务、直升机引航、医疗救护、空中游览等。")],
        "status": "ACTIVE",
    },
    # ---- TCL科技 ----
    {
        "exposure_id": "tcl_manufacture_lcd_panel",
        "company_id": "tcl_technology",
        "node_id": "lcd_panel",
        "activity_type": "manufacture",
        "role": "半导体显示面板制造商（LCD）",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("TCL科技2024年年度报告", "公司半导体显示业务全年实现营业收入1,043亿元，液晶产品业务竞争力取得领先地位，TV产品市场份额稳居全球前二。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tcl_manufacture_oled_panel",
        "company_id": "tcl_technology",
        "node_id": "oled_panel",
        "activity_type": "manufacture",
        "role": "半导体显示面板制造商（OLED）",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("TCL科技2024年年度报告", "柔性OLED业务竞争力增强，公司实现印刷OLED正式量产。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tcl_manufacture_display_module",
        "company_id": "tcl_technology",
        "node_id": "display_module",
        "activity_type": "manufacture",
        "role": "显示模组制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("TCL科技2024年年度报告", "公司积极完善全球化布局，扩充自建模组产能。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tcl_manufacture_pv_module",
        "company_id": "tcl_technology",
        "node_id": "photovoltaic_module",
        "activity_type": "manufacture",
        "role": "光伏组件及硅材料制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("TCL科技2024年年度报告", "新能源光伏及其他硅材料业务全年实现营业收入284亿元，光伏硅片销售量约143亿片。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "tcl_manufacture_silicon",
        "company_id": "tcl_technology",
        "node_id": "silicon_material",
        "activity_type": "manufacture",
        "role": "半导体硅材料制造商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("TCL科技2024年年度报告", "中环领先半导体材料业务取得30%营收增长，市场份额提高。")],
        "status": "ACTIVE",
    },
    # ---- 中成股份 ----
    {
        "exposure_id": "zhongcheng_provide_waste_treatment",
        "company_id": "zhongcheng",
        "node_id": "municipal_waste_treatment",
        "activity_type": "provide_service",
        "role": "固废治理服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中成股份2024年年度报告", "业务范围包括固体废物治理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongcheng_provide_hazardous_waste",
        "company_id": "zhongcheng",
        "node_id": "hazardous_waste_treatment_service",
        "activity_type": "provide_service",
        "role": "危废处理服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("中成股份2024年年度报告", "业务范围包括危险废物经营。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhongcheng_provide_recycling",
        "company_id": "zhongcheng",
        "node_id": "recycling_service",
        "activity_type": "provide_service",
        "role": "再生资源回收服务商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("中成股份2024年年度报告", "业务范围包括再生资源回收、再生资源加工、再生资源销售。")],
        "status": "ACTIVE",
    },
    # ---- 丰原药业 ----
    {
        "exposure_id": "fengyuan_manufacture_tcm",
        "company_id": "fengyuan_pharmaceutical",
        "node_id": "traditional_chinese_medicine",
        "activity_type": "manufacture",
        "role": "中成药制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("丰原药业2024年年度报告", "主要产品包括中药及其制剂。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fengyuan_manufacture_chemical_drug",
        "company_id": "fengyuan_pharmaceutical",
        "node_id": "chemical_drug",
        "activity_type": "manufacture",
        "role": "化学药制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("丰原药业2024年年度报告", "主要产品包括化学合成药及其制剂。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "fengyuan_manufacture_biological",
        "company_id": "fengyuan_pharmaceutical",
        "node_id": "biological_drug",
        "activity_type": "manufacture",
        "role": "生物药制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("丰原药业2024年年度报告", "主要产品包括生物药及其制剂。")],
        "status": "ACTIVE",
    },
    # ---- 川能动力 ----
    {
        "exposure_id": "chuanneng_operate_wind",
        "company_id": "chuanneng_power",
        "node_id": "wind_power_generation",
        "activity_type": "operate",
        "role": "风力发电运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("川能动力2024年年度报告", "主要业务为风力发电、光伏发电。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "chuanneng_operate_solar",
        "company_id": "chuanneng_power",
        "node_id": "solar_power_generation",
        "activity_type": "operate",
        "role": "光伏发电运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("川能动力2024年年度报告", "主要业务为风力发电、光伏发电。")],
        "status": "ACTIVE",
    },
    # ---- 华数传媒 ----
    {
        "exposure_id": "huashu_operate_cable_tv",
        "company_id": "huashu_media",
        "node_id": "cable_tv_network_service",
        "activity_type": "operate",
        "role": "有线电视网络运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务为杭州地区有线电视网络业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huashu_operate_broadband",
        "company_id": "huashu_media",
        "node_id": "broadband_network_service",
        "activity_type": "operate",
        "role": "宽带网络接入运营商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务包括宽带网络业务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huashu_provide_new_media",
        "company_id": "huashu_media",
        "node_id": "new_media_service",
        "activity_type": "provide_service",
        "role": "新媒体内容服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("华数传媒2024年年度报告", "主要业务包括全国范围内的新媒体业务。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_006_industrial_graph",
        "task_description": "Batch 006: 为10家中国公司构建产业实体图，涵盖港口物流、机场运营、房地产、能源贸易、通用航空、半导体显示、环保治理、化学药、新能源发电及广电网络等产业链。",
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
        "batch_id": "batch_006_company_views",
        "task_description": "Batch 006: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
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
    print("Batch 006 产业图与公司视图提交")
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
