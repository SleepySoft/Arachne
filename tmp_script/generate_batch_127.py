#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batch 127 submission scripts."""
import json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

def write_batch(batch_num, nodes, edges, companies, exposures):
    graph = {
        "batch_id": f"batch_{batch_num}_nodes",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges
    }
    path_g = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_nodes.json")
    with open(path_g, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    business = {
        "batch_id": f"batch_{batch_num}_business",
        "task_description": f"Batch {batch_num} business registration",
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures,
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": []
    }
    path_b = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_business.json")
    with open(path_b, "w", encoding="utf-8") as f:
        json.dump(business, f, ensure_ascii=False, indent=2)
    print(f"Batch {batch_num}: {len(nodes)} nodes, {len(edges)} edges, {len(companies)} companies, {len(exposures)} exposures")

NODES_127 = [
    {"node_id": "express_delivery_service", "canonical_name_zh": "快递服务", "canonical_name_en": "express delivery service", "entity_type": "service", "aliases": [], "definition": "通过快递网络提供的门到门包裹递送服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("韵达股份主营业务")},
    {"node_id": "engineering_design", "canonical_name_zh": "工程设计", "canonical_name_en": "engineering design", "entity_type": "service", "aliases": [], "definition": "为工程项目提供的设计方案和技术图纸服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国海诚主营业务")},
    {"node_id": "engineering_consulting", "canonical_name_zh": "工程咨询", "canonical_name_en": "engineering consulting", "entity_type": "service", "aliases": [], "definition": "为工程项目提供的技术咨询和可行性研究服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国海诚主营业务")},
    {"node_id": "engineering_supervision", "canonical_name_zh": "工程监理", "canonical_name_en": "engineering supervision", "entity_type": "service", "aliases": [], "definition": "对工程建设过程进行监督和管理的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国海诚主营业务")},
    {"node_id": "engineering_general_contracting", "canonical_name_zh": "工程总承包", "canonical_name_en": "engineering general contracting", "entity_type": "service", "aliases": ["EPC"], "definition": "对工程项目进行设计、采购、施工一体化的总承包服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国海诚主营业务")},
    {"node_id": "commercial_bill_printing", "canonical_name_zh": "商业票据印刷", "canonical_name_en": "commercial bill printing", "entity_type": "service", "aliases": [], "definition": "为商业领域提供的票据、票证印刷服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东港股份主营业务")},
    {"node_id": "paper_product_processing", "canonical_name_zh": "纸制品加工", "canonical_name_en": "paper product processing", "entity_type": "service", "aliases": [], "definition": "对纸张进行印刷、裁切、装订等加工服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东港股份主营业务")},
    {"node_id": "integrated_circuit_chip", "canonical_name_zh": "集成电路芯片", "canonical_name_en": "integrated circuit chip", "entity_type": "component", "aliases": ["IC芯片"], "definition": "将电路集成在半导体晶片上的微型电子器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东港股份经营范围")},
    {"node_id": "commercial_banking_service", "canonical_name_zh": "商业银行业务", "canonical_name_en": "commercial banking service", "entity_type": "service", "aliases": [], "definition": "商业银行提供的存款、贷款、结算等金融服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("兴业银行主营业务")},
    {"node_id": "semiconductor_lead_frame", "canonical_name_zh": "半导体引线框架", "canonical_name_en": "semiconductor lead frame", "entity_type": "component", "aliases": [], "definition": "半导体封装中用于连接芯片和外部电路的金属框架", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("康强电子主营业务")},
    {"node_id": "bonding_wire", "canonical_name_zh": "键合金丝", "canonical_name_en": "bonding wire", "entity_type": "component", "aliases": [], "definition": "用于半导体芯片与引线框架之间电连接的金属细丝", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("康强电子主营业务")},
    {"node_id": "semiconductor_packaging_material", "canonical_name_zh": "半导体封装材料", "canonical_name_en": "semiconductor packaging material", "entity_type": "material", "aliases": [], "definition": "用于半导体器件封装的各类材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("康强电子主营业务")},
    {"node_id": "small_section_steel", "canonical_name_zh": "小型材", "canonical_name_en": "small section steel", "entity_type": "material", "aliases": [], "definition": "截面尺寸较小的钢材产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("柳钢股份主营业务")},
    {"node_id": "medium_section_steel", "canonical_name_zh": "中型材", "canonical_name_en": "medium section steel", "entity_type": "material", "aliases": [], "definition": "截面尺寸中等的钢材产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("柳钢股份主营业务")},
    {"node_id": "coking_service", "canonical_name_zh": "炼焦", "canonical_name_en": "coking service", "entity_type": "service", "aliases": [], "definition": "将煤高温干馏生产焦炭的工业过程", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("柳钢股份经营范围")},
    {"node_id": "iron_making_service", "canonical_name_zh": "炼铁", "canonical_name_en": "iron making service", "entity_type": "service", "aliases": [], "definition": "将铁矿石冶炼为生铁的工业过程", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("柳钢股份经营范围")},
    {"node_id": "steel_making_service", "canonical_name_zh": "炼钢", "canonical_name_en": "steel making service", "entity_type": "service", "aliases": [], "definition": "将生铁冶炼为钢的工业过程", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("柳钢股份经营范围")},
    {"node_id": "aquatic_feed", "canonical_name_zh": "水产饲料", "canonical_name_en": "aquatic feed", "entity_type": "material", "aliases": [], "definition": "用于水产养殖的专用饲料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("天邦食品主营业务")},
    {"node_id": "extruded_pellet_feed", "canonical_name_zh": "膨化颗粒饲料", "canonical_name_en": "extruded pellet feed", "entity_type": "material", "aliases": [], "definition": "通过膨化工艺制成的颗粒状饲料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("天邦食品主营业务")},
    {"node_id": "pig_breeding", "canonical_name_zh": "生猪养殖", "canonical_name_en": "pig breeding", "entity_type": "service", "aliases": [], "definition": "以繁殖和饲养生猪为主的农业活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("天邦食品经营范围")},
    {"node_id": "wire_rod", "canonical_name_zh": "线材", "canonical_name_en": "wire rod", "entity_type": "material", "aliases": [], "definition": "直径较小的盘条状钢材", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("重庆钢铁主营业务")},
    {"node_id": "steel_bar", "canonical_name_zh": "棒材", "canonical_name_en": "steel bar", "entity_type": "material", "aliases": [], "definition": "截面为圆形的条状钢材", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("重庆钢铁主营业务")},
    {"node_id": "cold_rolled_plate", "canonical_name_zh": "冷轧板", "canonical_name_en": "cold rolled plate", "entity_type": "material", "aliases": [], "definition": "在常温下轧制的钢板产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("重庆钢铁主营业务")},
    {"node_id": "coking_by_product", "canonical_name_zh": "焦化副产品", "canonical_name_en": "coking by product", "entity_type": "material", "aliases": [], "definition": "炼焦过程中产生的焦油、粗苯等副产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("重庆钢铁主营业务")},
    {"node_id": "securities_service", "canonical_name_zh": "证券业务", "canonical_name_en": "securities service", "entity_type": "service", "aliases": [], "definition": "证券公司提供的股票、债券等金融服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国平安主营业务")},
    {"node_id": "trust_service", "canonical_name_zh": "信托业务", "canonical_name_en": "trust service", "entity_type": "service", "aliases": [], "definition": "信托公司提供的财产管理和融通服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国平安主营业务")},
    {"node_id": "mobile_instant_messaging", "canonical_name_zh": "移动信息即时通讯", "canonical_name_en": "mobile instant messaging", "entity_type": "service", "aliases": [], "definition": "基于移动通信网络的即时消息传输服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("梦网科技主营业务")},
    {"node_id": "mobile_audio_video", "canonical_name_zh": "移动音视频", "canonical_name_en": "mobile audio video", "entity_type": "service", "aliases": [], "definition": "基于移动通信网络的音频视频服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("梦网科技主营业务")},
    {"node_id": "mobile_smart_traffic", "canonical_name_zh": "移动智能流量", "canonical_name_en": "mobile smart traffic", "entity_type": "service", "aliases": [], "definition": "基于移动网络的智能流量分发和管理服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("梦网科技主营业务")},
    {"node_id": "power_electronics_equipment", "canonical_name_zh": "电力电子设备", "canonical_name_en": "power electronics equipment", "entity_type": "device", "aliases": [], "definition": "用于电能变换和控制的电力电子装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("梦网科技主营业务")},
]

EDGES_127 = [
    {"edge_id": "express_delivery_service_logistics", "from_node": "express_delivery_service", "to_node": "logistics", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "快递服务是物流服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_design_technical_service", "from_node": "engineering_design", "to_node": "technical_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程设计是技术服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_consulting_technical_service", "from_node": "engineering_consulting", "to_node": "technical_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程咨询是技术服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_supervision_technical_service", "from_node": "engineering_supervision", "to_node": "technical_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程监理是技术服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_general_contracting_construction_engineering", "from_node": "engineering_general_contracting", "to_node": "construction_engineering", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程总承包是建筑工程的一种组织模式", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "commercial_bill_printing_paper_product", "from_node": "commercial_bill_printing", "to_node": "paper_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "商业票据印刷是纸制品加工的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "paper_product_processing_paper_product", "from_node": "paper_product_processing", "to_node": "paper_product", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "纸制品加工是纸制品产业链的环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "integrated_circuit_chip_integrated_circuit", "from_node": "integrated_circuit_chip", "to_node": "integrated_circuit", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "集成电路芯片是集成电路的载体", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "commercial_banking_service_banking_service", "from_node": "commercial_banking_service", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业银行业务是银行服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "semiconductor_lead_frame_semiconductor", "from_node": "semiconductor_lead_frame", "to_node": "semiconductor", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "半导体引线框架是半导体器件的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "bonding_wire_semiconductor", "from_node": "bonding_wire", "to_node": "semiconductor", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "键合金丝是半导体封装的连接材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "semiconductor_packaging_material_semiconductor", "from_node": "semiconductor_packaging_material", "to_node": "semiconductor", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "半导体封装材料是半导体产业的配套材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "small_section_steel_steel", "from_node": "small_section_steel", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "小型材是钢材的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "medium_section_steel_steel", "from_node": "medium_section_steel", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "中型材是钢材的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "coking_service_chemical_product", "from_node": "coking_service", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "炼焦是化工生产过程的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "iron_making_service_steel", "from_node": "iron_making_service", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "炼铁是钢铁生产的上游环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_making_service_steel", "from_node": "steel_making_service", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "炼钢是钢铁生产的核心环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aquatic_feed_feed", "from_node": "aquatic_feed", "to_node": "feed", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "水产饲料是饲料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "extruded_pellet_feed_feed", "from_node": "extruded_pellet_feed", "to_node": "feed", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "膨化颗粒饲料是饲料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "pig_breeding_livestock_breeding", "from_node": "pig_breeding", "to_node": "livestock_breeding", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "生猪养殖是畜禽养殖的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "wire_rod_steel", "from_node": "wire_rod", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "线材是钢材的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_bar_steel", "from_node": "steel_bar", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "棒材是钢材的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "cold_rolled_plate_steel", "from_node": "cold_rolled_plate", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "冷轧板是钢材的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "coking_by_product_chemical_product", "from_node": "coking_by_product", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "焦化副产品是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "securities_service_banking_service", "from_node": "securities_service", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "证券业务是金融服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "trust_service_banking_service", "from_node": "trust_service", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "信托业务是金融服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mobile_instant_messaging_telecommunication", "from_node": "mobile_instant_messaging", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "移动信息即时通讯是电信服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mobile_audio_video_telecommunication", "from_node": "mobile_audio_video", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "移动音视频是电信服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mobile_smart_traffic_telecommunication", "from_node": "mobile_smart_traffic", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "移动智能流量是电信服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "power_electronics_equipment_electronic_component", "from_node": "power_electronics_equipment", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电力电子设备是电子设备的范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "iron_making_service_steel_making_service", "from_node": "iron_making_service", "to_node": "steel_making_service", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "炼铁为炼钢提供生铁原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_making_service_steel_bar", "from_node": "steel_making_service", "to_node": "steel_bar", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "炼钢产出棒材", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "coking_service_coking_by_product", "from_node": "coking_service", "to_node": "coking_by_product", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "炼焦过程产生焦化副产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_design_engineering_general_contracting", "from_node": "engineering_design", "to_node": "engineering_general_contracting", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程设计是工程总承包的前期环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

COMPANIES_127 = [
    {"company_id": "sz_002120", "name_zh": "韵达股份", "name_en": "Yunda Holding Group Co., Ltd.", "country": "CN", "province": "浙江", "city": "宁波市", "stock_codes": ["002120.SZ"], "description": "快递服务、物流", "founded_year": 1996, "employee_count": 9765},
    {"company_id": "sz_002116", "name_zh": "中国海诚", "name_en": "China Haisum Engineering Co., Ltd.", "country": "CN", "province": "上海", "city": "上海市", "stock_codes": ["002116.SZ"], "description": "工程设计、工程咨询、工程监理、工程总承包", "founded_year": 1993, "employee_count": 4517},
    {"company_id": "sz_002117", "name_zh": "东港股份", "name_en": "Donggang Co., Ltd.", "country": "CN", "province": "山东", "city": "济南市", "stock_codes": ["002117.SZ"], "description": "商业票据印刷、纸制品加工、集成电路芯片", "founded_year": 1996, "employee_count": 1110},
    {"company_id": "sh_601166", "name_zh": "兴业银行", "name_en": "Industrial Bank Co., Ltd.", "country": "CN", "province": "福建", "city": "福州市", "stock_codes": ["601166.SH"], "description": "商业银行业务", "founded_year": 1988, "employee_count": 68963},
    {"company_id": "sz_002119", "name_zh": "康强电子", "name_en": "Ningbo Kangqiang Electronics Co., Ltd.", "country": "CN", "province": "浙江", "city": "宁波市", "stock_codes": ["002119.SZ"], "description": "半导体封装材料引线框架和键合金丝", "founded_year": 1992, "employee_count": 1218},
    {"company_id": "sh_601003", "name_zh": "柳钢股份", "name_en": "Liuzhou Iron & Steel Co., Ltd.", "country": "CN", "province": "广西", "city": "柳州市", "stock_codes": ["601003.SH"], "description": "中板材、小型材、中型材、钢坯、炼焦、炼铁、炼钢", "founded_year": 2000, "employee_count": 12637},
    {"company_id": "sz_002124", "name_zh": "天邦食品", "name_en": "Tianbang Food Co., Ltd.", "country": "CN", "province": "浙江", "city": "宁波市", "stock_codes": ["002124.SZ"], "description": "水产饲料、膨化颗粒饲料、生猪养殖、兽药", "founded_year": 1996, "employee_count": 6588},
    {"company_id": "sh_601005", "name_zh": "重庆钢铁", "name_en": "Chongqing Iron & Steel Co., Ltd.", "country": "CN", "province": "重庆", "city": "重庆市", "stock_codes": ["601005.SH"], "description": "中厚钢板、型材、线材、棒材、钢坯、冷轧板、焦化副产品", "founded_year": 1997, "employee_count": 5204},
    {"company_id": "sh_601318", "name_zh": "中国平安", "name_en": "Ping An Insurance (Group) Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["601318.SH"], "description": "保险、银行、证券、信托等多元化金融服务", "founded_year": 1988, "employee_count": 258806},
    {"company_id": "sz_002123", "name_zh": "梦网科技", "name_en": "Mengwang Cloud Technology Group Co., Ltd.", "country": "CN", "province": "辽宁", "city": "鞍山市", "stock_codes": ["002123.SZ"], "description": "移动信息即时通讯、移动音视频、移动智能流量、电力电子设备", "founded_year": 1998, "employee_count": 882},
]

EXPOSURES_127 = [
    {"exposure_id": "sz_002120_provide_service_express_delivery_service", "company_id": "sz_002120", "node_id": "express_delivery_service", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:快递服务")},
    {"exposure_id": "sz_002120_provide_service_logistics", "company_id": "sz_002120", "node_id": "logistics", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物流")},
    {"exposure_id": "sz_002120_provide_service_e_commerce", "company_id": "sz_002120", "node_id": "e_commerce", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电子商务")},
    {"exposure_id": "sz_002120_provide_service_technical_service", "company_id": "sz_002120", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002120_provide_service_internet_advertising", "company_id": "sz_002120", "node_id": "internet_advertising", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:广告发布")},
    {"exposure_id": "sz_002116_provide_service_engineering_design", "company_id": "sz_002116", "node_id": "engineering_design", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:工程设计")},
    {"exposure_id": "sz_002116_provide_service_engineering_consulting", "company_id": "sz_002116", "node_id": "engineering_consulting", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:工程咨询")},
    {"exposure_id": "sz_002116_provide_service_engineering_supervision", "company_id": "sz_002116", "node_id": "engineering_supervision", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:工程监理")},
    {"exposure_id": "sz_002116_provide_service_engineering_general_contracting", "company_id": "sz_002116", "node_id": "engineering_general_contracting", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:工程总承包")},
    {"exposure_id": "sz_002116_provide_service_technical_service", "company_id": "sz_002116", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002117_provide_service_commercial_bill_printing", "company_id": "sz_002117", "node_id": "commercial_bill_printing", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:商业票据印刷")},
    {"exposure_id": "sz_002117_provide_service_paper_product_processing", "company_id": "sz_002117", "node_id": "paper_product_processing", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纸制品加工")},
    {"exposure_id": "sz_002117_produce_integrated_circuit_chip", "company_id": "sz_002117", "node_id": "integrated_circuit_chip", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:集成电路芯片")},
    {"exposure_id": "sz_002117_produce_paper_product", "company_id": "sz_002117", "node_id": "paper_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纸制品制造")},
    {"exposure_id": "sz_002117_provide_service_technical_service", "company_id": "sz_002117", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sh_601166_provide_service_commercial_banking_service", "company_id": "sh_601166", "node_id": "commercial_banking_service", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:商业银行业务")},
    {"exposure_id": "sh_601166_provide_service_banking_service", "company_id": "sh_601166", "node_id": "banking_service", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:银行业务")},
    {"exposure_id": "sh_601166_provide_service_insurance", "company_id": "sh_601166", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:代理保险业务")},
    {"exposure_id": "sh_601166_provide_service_securities_service", "company_id": "sh_601166", "node_id": "securities_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:证券投资基金销售")},
    {"exposure_id": "sh_601166_provide_service_trust_service", "company_id": "sh_601166", "node_id": "trust_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:资产托管业务")},
    {"exposure_id": "sz_002119_produce_semiconductor_lead_frame", "company_id": "sz_002119", "node_id": "semiconductor_lead_frame", "activity_type": "produce", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:半导体引线框架")},
    {"exposure_id": "sz_002119_produce_bonding_wire", "company_id": "sz_002119", "node_id": "bonding_wire", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:键合金丝")},
    {"exposure_id": "sz_002119_produce_semiconductor_packaging_material", "company_id": "sz_002119", "node_id": "semiconductor_packaging_material", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:半导体封装材料")},
    {"exposure_id": "sz_002119_produce_semiconductor", "company_id": "sz_002119", "node_id": "semiconductor", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:半导体元器件")},
    {"exposure_id": "sh_601003_produce_medium_plate", "company_id": "sh_601003", "node_id": "medium_plate", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:中板材")},
    {"exposure_id": "sh_601003_produce_small_section_steel", "company_id": "sh_601003", "node_id": "small_section_steel", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:小型材")},
    {"exposure_id": "sh_601003_produce_medium_section_steel", "company_id": "sh_601003", "node_id": "medium_section_steel", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:中型材")},
    {"exposure_id": "sh_601003_produce_steel_billet", "company_id": "sh_601003", "node_id": "steel_billet", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:钢坯")},
    {"exposure_id": "sh_601003_operate_coking_service", "company_id": "sh_601003", "node_id": "coking_service", "activity_type": "operate", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:炼焦")},
    {"exposure_id": "sh_601003_produce_steel", "company_id": "sh_601003", "node_id": "steel", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢材")},
    {"exposure_id": "sh_601003_operate_iron_making_service", "company_id": "sh_601003", "node_id": "iron_making_service", "activity_type": "operate", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:炼铁")},
    {"exposure_id": "sz_002124_produce_aquatic_feed", "company_id": "sz_002124", "node_id": "aquatic_feed", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:水产饲料")},
    {"exposure_id": "sz_002124_produce_extruded_pellet_feed", "company_id": "sz_002124", "node_id": "extruded_pellet_feed", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:膨化颗粒饲料")},
    {"exposure_id": "sz_002124_operate_pig_breeding", "company_id": "sz_002124", "node_id": "pig_breeding", "activity_type": "operate", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:生猪养殖")},
    {"exposure_id": "sz_002124_produce_veterinary_medicine", "company_id": "sz_002124", "node_id": "veterinary_medicine", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:兽药")},
    {"exposure_id": "sz_002124_produce_feed", "company_id": "sz_002124", "node_id": "feed", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:饲料")},
    {"exposure_id": "sz_002124_operate_livestock_breeding", "company_id": "sz_002124", "node_id": "livestock_breeding", "activity_type": "operate", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:畜禽养殖")},
    {"exposure_id": "sh_601005_produce_medium_plate", "company_id": "sh_601005", "node_id": "medium_plate", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:中厚钢板")},
    {"exposure_id": "sh_601005_produce_wire_rod", "company_id": "sh_601005", "node_id": "wire_rod", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:线材")},
    {"exposure_id": "sh_601005_produce_steel_bar", "company_id": "sh_601005", "node_id": "steel_bar", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:棒材")},
    {"exposure_id": "sh_601005_produce_cold_rolled_plate", "company_id": "sh_601005", "node_id": "cold_rolled_plate", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:冷轧板")},
    {"exposure_id": "sh_601005_produce_steel_billet", "company_id": "sh_601005", "node_id": "steel_billet", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢坯")},
    {"exposure_id": "sh_601005_produce_coking_by_product", "company_id": "sh_601005", "node_id": "coking_by_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:焦化副产品")},
    {"exposure_id": "sh_601005_produce_steel", "company_id": "sh_601005", "node_id": "steel", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢材")},
    {"exposure_id": "sh_601318_provide_service_insurance", "company_id": "sh_601318", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:保险业务")},
    {"exposure_id": "sh_601318_provide_service_banking_service", "company_id": "sh_601318", "node_id": "banking_service", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:银行业务")},
    {"exposure_id": "sh_601318_provide_service_securities_service", "company_id": "sh_601318", "node_id": "securities_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:证券业务")},
    {"exposure_id": "sh_601318_provide_service_trust_service", "company_id": "sh_601318", "node_id": "trust_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:信托业务")},
    {"exposure_id": "sh_601318_provide_service_health_insurance", "company_id": "sh_601318", "node_id": "health_insurance", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:健康保险")},
    {"exposure_id": "sh_601318_provide_service_life_insurance", "company_id": "sh_601318", "node_id": "life_insurance", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:人寿保险")},
    {"exposure_id": "sh_601318_provide_service_accident_insurance", "company_id": "sh_601318", "node_id": "accident_insurance", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:意外伤害保险")},
    {"exposure_id": "sz_002123_provide_service_mobile_instant_messaging", "company_id": "sz_002123", "node_id": "mobile_instant_messaging", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:移动信息即时通讯")},
    {"exposure_id": "sz_002123_provide_service_mobile_audio_video", "company_id": "sz_002123", "node_id": "mobile_audio_video", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:移动音视频")},
    {"exposure_id": "sz_002123_provide_service_mobile_smart_traffic", "company_id": "sz_002123", "node_id": "mobile_smart_traffic", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:移动智能流量")},
    {"exposure_id": "sz_002123_produce_power_electronics_equipment", "company_id": "sz_002123", "node_id": "power_electronics_equipment", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电力电子设备")},
    {"exposure_id": "sz_002123_provide_service_telecommunication", "company_id": "sz_002123", "node_id": "telecommunication", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:增值电信业务")},
    {"exposure_id": "sz_002123_provide_service_technical_service", "company_id": "sz_002123", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
]

write_batch(127, NODES_127, EDGES_127, COMPANIES_127, EXPOSURES_127)
print("Batch 127 generated.")
