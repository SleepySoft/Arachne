#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batch 124 submission scripts."""
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

NODES_124 = [
    {"node_id": "power_automation", "canonical_name_zh": "电力自动化", "canonical_name_en": "power automation", "entity_type": "service", "aliases": [], "definition": "对电力系统进行自动监控、保护和控制的综合技术和服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金智科技主营业务")},
    {"node_id": "university_informatization", "canonical_name_zh": "高校信息化", "canonical_name_en": "university informatization", "entity_type": "service", "aliases": [], "definition": "为高等院校提供的信息化建设和管理服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金智科技主营业务")},
    {"node_id": "smart_grid", "canonical_name_zh": "智能电网", "canonical_name_en": "smart grid", "entity_type": "system", "aliases": [], "definition": "集成了通信和信息技术，具有智能化特性的电力网络", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("金智科技经营范围")},
    {"node_id": "textile_export", "canonical_name_zh": "纺织品出口", "canonical_name_en": "textile export", "entity_type": "service", "aliases": [], "definition": "纺织品的出口贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("江苏国泰主营业务")},
    {"node_id": "light_industry_export", "canonical_name_zh": "轻工产品出口", "canonical_name_en": "light industry export", "entity_type": "service", "aliases": [], "definition": "轻工类产品的出口贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("江苏国泰主营业务")},
    {"node_id": "mechanical_electrical_export", "canonical_name_zh": "机电产品出口", "canonical_name_en": "mechanical electrical export", "entity_type": "service", "aliases": [], "definition": "机械电子类产品的出口贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("江苏国泰主营业务")},
    {"node_id": "chemical_export", "canonical_name_zh": "化工产品出口", "canonical_name_en": "chemical export", "entity_type": "service", "aliases": [], "definition": "化工类产品的出口贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("江苏国泰经营范围")},
    {"node_id": "labor_export", "canonical_name_zh": "劳务输出", "canonical_name_en": "labor export", "entity_type": "service", "aliases": [], "definition": "向境外派遣劳务人员的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("江苏国泰经营范围")},
    {"node_id": "pvc_resin", "canonical_name_zh": "PVC树脂", "canonical_name_en": "PVC resin", "entity_type": "material", "aliases": ["聚氯乙烯"], "definition": "聚氯乙烯树脂，用于制造塑料管材、薄膜等产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中泰化学主营业务")},
    {"node_id": "caustic_soda", "canonical_name_zh": "烧碱", "canonical_name_en": "caustic soda", "entity_type": "material", "aliases": ["氢氧化钠"], "definition": "氢氧化钠，重要的基础化工原料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中泰化学主营业务")},
    {"node_id": "chlor_alkali", "canonical_name_zh": "氯碱化工", "canonical_name_en": "chlor alkali", "entity_type": "service", "aliases": [], "definition": "利用电解食盐水生产氯气、氢氧化钠等产品的化工过程", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中泰化学经营范围")},
    {"node_id": "calcium_carbide", "canonical_name_zh": "电石", "canonical_name_en": "calcium carbide", "entity_type": "material", "aliases": [], "definition": "碳化钙，用于生产乙炔和PVC", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中泰化学经营范围")},
    {"node_id": "b2b_e_commerce", "canonical_name_zh": "B2B电子商务", "canonical_name_en": "B2B e-commerce", "entity_type": "service", "aliases": [], "definition": "企业与企业之间通过电子方式进行的商务活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("生意宝主营业务")},
    {"node_id": "chemical_industry_information", "canonical_name_zh": "化工行业信息服务", "canonical_name_en": "chemical industry information", "entity_type": "service", "aliases": [], "definition": "为化工行业提供的信息咨询和数据服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("生意宝主营业务")},
    {"node_id": "textile_information", "canonical_name_zh": "纺织行业信息服务", "canonical_name_en": "textile information", "entity_type": "service", "aliases": [], "definition": "为纺织行业提供的信息咨询和数据服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("生意宝经营范围")},
    {"node_id": "candle", "canonical_name_zh": "蜡烛", "canonical_name_en": "candle", "entity_type": "material", "aliases": [], "definition": "以蜡为主要材料制成的照明用品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("青岛金王主营业务")},
    {"node_id": "polymer_candle_material", "canonical_name_zh": "聚合物蜡烛", "canonical_name_en": "polymer candle material", "entity_type": "material", "aliases": [], "definition": "采用高分子材料制作的蜡烛产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("青岛金王经营范围")},
    {"node_id": "glass_craft", "canonical_name_zh": "玻璃制品", "canonical_name_en": "glass craft", "entity_type": "material", "aliases": [], "definition": "以玻璃为材料制作的工艺品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("青岛金王经营范围")},
    {"node_id": "epoxy_resin_product", "canonical_name_zh": "环氧树脂产品", "canonical_name_en": "epoxy resin product", "entity_type": "material", "aliases": [], "definition": "以环氧树脂为主要成分的产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("青岛金王经营范围")},
    {"node_id": "telecom_network_service", "canonical_name_zh": "电信网络服务", "canonical_name_en": "telecom network service", "entity_type": "service", "aliases": [], "definition": "为电信运营商提供的网络优化和运维服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("国脉科技主营业务")},
    {"node_id": "communication_system_integration", "canonical_name_zh": "通信系统集成", "canonical_name_en": "communication system integration", "entity_type": "service", "aliases": [], "definition": "将通信设备和系统集成为完整解决方案的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("国脉科技经营范围")},
    {"node_id": "iot_service", "canonical_name_zh": "物联网服务", "canonical_name_en": "internet of things service", "entity_type": "service", "aliases": [], "definition": "基于物联网技术的信息服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("国脉科技经营范围")},
    {"node_id": "pharmaceutical_intermediate", "canonical_name_zh": "医药中间体", "canonical_name_en": "pharmaceutical intermediate", "entity_type": "material", "aliases": [], "definition": "用于合成药物的化学中间体", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("能特科技经营范围")},
    {"node_id": "gold_mining", "canonical_name_zh": "金矿采选", "canonical_name_en": "gold mining", "entity_type": "service", "aliases": [], "definition": "黄金矿石的开采和选矿活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("能特科技经营范围")},
    {"node_id": "plastic_trade", "canonical_name_zh": "塑料制品贸易", "canonical_name_en": "plastic trade", "entity_type": "service", "aliases": [], "definition": "塑料制品的批发零售贸易", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("能特科技经营范围")},
    {"node_id": "real_estate_leasing", "canonical_name_zh": "房地产租赁", "canonical_name_en": "real estate leasing", "entity_type": "service", "aliases": [], "definition": "房地产的经营租赁和融资租赁", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("能特科技经营范围")},
    {"node_id": "aluminum_die_casting", "canonical_name_zh": "铝合金压铸件", "canonical_name_en": "aluminum die casting", "entity_type": "component", "aliases": [], "definition": "通过压铸工艺成型的铝合金零件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("广东鸿图主营业务")},
    {"node_id": "special_purpose_vehicle", "canonical_name_zh": "专用车", "canonical_name_en": "special purpose vehicle", "entity_type": "system", "aliases": [], "definition": "具有特定用途的专用汽车", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("广东鸿图经营范围")},
    {"node_id": "investment_platform", "canonical_name_zh": "投资平台", "canonical_name_en": "investment platform", "entity_type": "service", "aliases": [], "definition": "用于资产管理和投资的金融平台", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("广东鸿图经营范围")},
    {"node_id": "dye_intermediate", "canonical_name_zh": "染料中间体", "canonical_name_en": "dye intermediate", "entity_type": "material", "aliases": [], "definition": "用于合成染料的化学中间体", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("海翔药业经营范围")},
]

EDGES_124 = [
    {"edge_id": "power_automation_smart_grid", "from_node": "power_automation", "to_node": "smart_grid", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "电力自动化是智能电网的核心技术", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "university_informatization_e_government_software", "from_node": "university_informatization", "to_node": "e_government_software", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "高校信息化是电子政务软件的延伸应用", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "smart_grid_power_generation_equipment", "from_node": "smart_grid", "to_node": "power_generation_equipment", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "智能电网是发电设备的智能化升级", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "textile_export_import_export", "from_node": "textile_export", "to_node": "import_export", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "纺织品出口是进出口贸易的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "light_industry_export_import_export", "from_node": "light_industry_export", "to_node": "import_export", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "轻工产品出口是进出口贸易的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mechanical_electrical_export_import_export", "from_node": "mechanical_electrical_export", "to_node": "import_export", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "机电产品出口是进出口贸易的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "chemical_export_import_export", "from_node": "chemical_export", "to_node": "import_export", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "化工产品出口是进出口贸易的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "labor_export_human_resource", "from_node": "labor_export", "to_node": "human_resource", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "劳务输出是人力资源服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "pvc_resin_chemical_product", "from_node": "pvc_resin", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "PVC树脂是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "caustic_soda_chemical_product", "from_node": "caustic_soda", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "烧碱是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "chlor_alkali_chemical_process", "from_node": "chlor_alkali", "to_node": "chemical_process", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "氯碱化工是重要的化工过程", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "calcium_carbide_pvc_resin", "from_node": "calcium_carbide", "to_node": "pvc_resin", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "电石是PVC树脂的原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "b2b_e_commerce_e_commerce", "from_node": "b2b_e_commerce", "to_node": "e_commerce", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "B2B电子商务是电子商务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "chemical_industry_information_b2b_e_commerce", "from_node": "chemical_industry_information", "to_node": "b2b_e_commerce", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "化工行业信息服务是B2B电子商务的延伸", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "textile_information_b2b_e_commerce", "from_node": "textile_information", "to_node": "b2b_e_commerce", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "纺织行业信息服务是B2B电子商务的延伸", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "polymer_candle_material_candle", "from_node": "polymer_candle_material", "to_node": "candle", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "聚合物材料用于蜡烛生产", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "glass_craft_candle", "from_node": "glass_craft", "to_node": "candle", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "玻璃制品与蜡烛同属工艺消费品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "epoxy_resin_product_epoxy_resin", "from_node": "epoxy_resin_product", "to_node": "epoxy_resin", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "环氧树脂产品以环氧树脂为原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "telecom_network_service_telecommunication", "from_node": "telecom_network_service", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "电信网络服务是电信业的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "communication_system_integration_telecommunication", "from_node": "communication_system_integration", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "通信系统集成是电信业的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "iot_service_telecommunication", "from_node": "iot_service", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "物联网服务是电信业的延伸", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "pharmaceutical_intermediate_pharmaceutical_api", "from_node": "pharmaceutical_intermediate", "to_node": "pharmaceutical_api", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "医药中间体是原料药的上游原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "gold_mining_mining", "from_node": "gold_mining", "to_node": "mining", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "金矿采选是采矿业的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "plastic_trade_plastic_product", "from_node": "plastic_trade", "to_node": "plastic_product", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "塑料制品贸易是塑料制品的流通环节", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "real_estate_leasing_real_estate", "from_node": "real_estate_leasing", "to_node": "real_estate", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "房地产租赁是房地产业务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aluminum_die_casting_aluminum", "from_node": "aluminum_die_casting", "to_node": "aluminum", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "铝合金压铸件以铝合金为原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "special_purpose_vehicle_automotive", "from_node": "special_purpose_vehicle", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "专用车是汽车产业的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "dye_intermediate_dye", "from_node": "dye_intermediate", "to_node": "dye", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "染料中间体是染料的上游原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

COMPANIES_124 = [
    {"company_id": "sz_002090", "name_zh": "金智科技", "name_en": "Wiscom System Co., Ltd.", "country": "CN", "province": "江苏", "city": "南京市", "stock_codes": ["002090.SZ"], "description": "电力自动化业务、高校信息化业务", "founded_year": 1995, "employee_count": 833},
    {"company_id": "sz_002091", "name_zh": "江苏国泰", "name_en": "Jiangsu Guotai International Group Co., Ltd.", "country": "CN", "province": "江苏", "city": "张家港市", "stock_codes": ["002091.SZ"], "description": "纺织品、轻工、机电、化工等产品的进出口贸易", "founded_year": 1998, "employee_count": 33150},
    {"company_id": "sz_002092", "name_zh": "中泰化学", "name_en": "Xinjiang Zhongtai Chemical Co., Ltd.", "country": "CN", "province": "新疆", "city": "乌鲁木齐市", "stock_codes": ["002092.SZ"], "description": "聚氯乙烯树脂、离子膜烧碱等化工产品", "founded_year": 2001, "employee_count": 23576},
    {"company_id": "sh_601991", "name_zh": "大唐发电", "name_en": "Datang International Power Generation Co., Ltd.", "country": "CN", "province": "北京", "city": "北京市", "stock_codes": ["601991.SH"], "description": "建设、经营电厂，销售电力、热力", "founded_year": 1994, "employee_count": 25801},
    {"company_id": "sz_002095", "name_zh": "生意宝", "name_en": "Toocle Inc.", "country": "CN", "province": "浙江", "city": "杭州市", "stock_codes": ["002095.SZ"], "description": "B2B电子商务", "founded_year": 2000, "employee_count": 403},
    {"company_id": "sz_002094", "name_zh": "青岛金王", "name_en": "Qingdao Kingking Applied Chemistry Co., Ltd.", "country": "CN", "province": "山东", "city": "青岛市", "stock_codes": ["002094.SZ"], "description": "蜡烛、蜡烛制品、日用化学品", "founded_year": 1993, "employee_count": 3295},
    {"company_id": "sz_002093", "name_zh": "国脉科技", "name_en": "Guomai Technologies Inc.", "country": "CN", "province": "福建", "city": "福州市", "stock_codes": ["002093.SZ"], "description": "电信网络服务、系统集成", "founded_year": 1996, "employee_count": 442},
    {"company_id": "sz_002102", "name_zh": "能特科技", "name_en": "Nente Bio-engineering Co., Ltd.", "country": "CN", "province": "湖北", "city": "荆州市", "stock_codes": ["002102.SZ"], "description": "医药中间体、黄金探矿及采矿", "founded_year": 2002, "employee_count": 498},
    {"company_id": "sz_002101", "name_zh": "广东鸿图", "name_en": "Guangdong Hongtu Technology (Holdings) Co., Ltd.", "country": "CN", "province": "广东", "city": "肇庆市", "stock_codes": ["002101.SZ"], "description": "铝合金压铸件、汽车内外饰件", "founded_year": 2000, "employee_count": 5426},
    {"company_id": "sz_002099", "name_zh": "海翔药业", "name_en": "Zhejiang Hisun Pharmaceutical Co., Ltd.", "country": "CN", "province": "浙江", "city": "台州市", "stock_codes": ["002099.SZ"], "description": "化学合成医药产品", "founded_year": 1966, "employee_count": 3585},
]

EXPOSURES_124 = [
    {"exposure_id": "sz_002090_provide_service_power_automation", "company_id": "sz_002090", "node_id": "power_automation", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电力自动化")},
    {"exposure_id": "sz_002090_provide_service_university_informatization", "company_id": "sz_002090", "node_id": "university_informatization", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:高校信息化")},
    {"exposure_id": "sz_002090_provide_service_smart_grid", "company_id": "sz_002090", "node_id": "smart_grid", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:智能电网")},
    {"exposure_id": "sz_002090_produce_energy_storage_system", "company_id": "sz_002090", "node_id": "energy_storage_system", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:储能系统")},
    {"exposure_id": "sz_002090_produce_charging_pile", "company_id": "sz_002090", "node_id": "charging_pile", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:充电桩")},
    {"exposure_id": "sz_002090_provide_service_technical_service", "company_id": "sz_002090", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002091_provide_service_textile_export", "company_id": "sz_002091", "node_id": "textile_export", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:纺织品进出口")},
    {"exposure_id": "sz_002091_provide_service_light_industry_export", "company_id": "sz_002091", "node_id": "light_industry_export", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:轻工产品进出口")},
    {"exposure_id": "sz_002091_provide_service_mechanical_electrical_export", "company_id": "sz_002091", "node_id": "mechanical_electrical_export", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:机电产品进出口")},
    {"exposure_id": "sz_002091_provide_service_chemical_export", "company_id": "sz_002091", "node_id": "chemical_export", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:化工产品进出口")},
    {"exposure_id": "sz_002091_provide_service_labor_export", "company_id": "sz_002091", "node_id": "labor_export", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:对外派遣劳务")},
    {"exposure_id": "sz_002091_provide_service_technical_service", "company_id": "sz_002091", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002091_provide_service_logistics", "company_id": "sz_002091", "node_id": "logistics", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物流配送")},
    {"exposure_id": "sz_002092_produce_pvc_resin", "company_id": "sz_002092", "node_id": "pvc_resin", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:聚氯乙烯树脂")},
    {"exposure_id": "sz_002092_produce_caustic_soda", "company_id": "sz_002092", "node_id": "caustic_soda", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:离子膜烧碱")},
    {"exposure_id": "sz_002092_operate_chlor_alkali", "company_id": "sz_002092", "node_id": "chlor_alkali", "activity_type": "operate", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:氯碱化工")},
    {"exposure_id": "sz_002092_produce_calcium_carbide", "company_id": "sz_002092", "node_id": "calcium_carbide", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电石")},
    {"exposure_id": "sz_002092_produce_cement", "company_id": "sz_002092", "node_id": "cement", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:水泥")},
    {"exposure_id": "sz_002092_provide_service_technical_service", "company_id": "sz_002092", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sh_601991_operate_thermal_power", "company_id": "sh_601991", "node_id": "thermal_power", "activity_type": "operate", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:火力发电")},
    {"exposure_id": "sh_601991_provide_service_electricity_sales", "company_id": "sh_601991", "node_id": "electricity_sales", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电力销售")},
    {"exposure_id": "sh_601991_provide_service_heat_supply", "company_id": "sh_601991", "node_id": "heat_supply", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:供热")},
    {"exposure_id": "sh_601991_operate_power_generation", "company_id": "sh_601991", "node_id": "power_generation", "activity_type": "operate", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建设经营电厂")},
    {"exposure_id": "sh_601991_provide_service_technical_service", "company_id": "sh_601991", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002095_provide_service_b2b_e_commerce", "company_id": "sz_002095", "node_id": "b2b_e_commerce", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:B2B电子商务")},
    {"exposure_id": "sz_002095_provide_service_chemical_industry_information", "company_id": "sz_002095", "node_id": "chemical_industry_information", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:化工行业信息服务")},
    {"exposure_id": "sz_002095_provide_service_textile_information", "company_id": "sz_002095", "node_id": "textile_information", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纺织信息服务")},
    {"exposure_id": "sz_002095_provide_service_internet_advertising", "company_id": "sz_002095", "node_id": "internet_advertising", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:互联网广告")},
    {"exposure_id": "sz_002095_provide_service_technical_service", "company_id": "sz_002095", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002094_produce_candle", "company_id": "sz_002094", "node_id": "candle", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:蜡烛")},
    {"exposure_id": "sz_002094_produce_polymer_candle_material", "company_id": "sz_002094", "node_id": "polymer_candle_material", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:聚合物蜡烛")},
    {"exposure_id": "sz_002094_produce_glass_craft", "company_id": "sz_002094", "node_id": "glass_craft", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:玻璃制品")},
    {"exposure_id": "sz_002094_produce_epoxy_resin_product", "company_id": "sz_002094", "node_id": "epoxy_resin_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:环氧树脂产品")},
    {"exposure_id": "sz_002094_produce_cosmetic", "company_id": "sz_002094", "node_id": "cosmetic", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:日用化学品")},
    {"exposure_id": "sz_002094_provide_service_technical_service", "company_id": "sz_002094", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002094_produce_paper_product", "company_id": "sz_002094", "node_id": "paper_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纸制品")},
    {"exposure_id": "sz_002093_provide_service_telecom_network_service", "company_id": "sz_002093", "node_id": "telecom_network_service", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电信网络服务")},
    {"exposure_id": "sz_002093_provide_service_communication_system_integration", "company_id": "sz_002093", "node_id": "communication_system_integration", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:通信系统集成")},
    {"exposure_id": "sz_002093_provide_service_iot_service", "company_id": "sz_002093", "node_id": "iot_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物联网")},
    {"exposure_id": "sz_002093_provide_service_telecommunication", "company_id": "sz_002093", "node_id": "telecommunication", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:通讯设备")},
    {"exposure_id": "sz_002093_provide_service_technical_service", "company_id": "sz_002093", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002093_provide_service_information_security_service", "company_id": "sz_002093", "node_id": "information_security_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:信息安全")},
    {"exposure_id": "sz_002102_produce_pharmaceutical_intermediate", "company_id": "sz_002102", "node_id": "pharmaceutical_intermediate", "activity_type": "produce", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:医药中间体")},
    {"exposure_id": "sz_002102_operate_gold_mining", "company_id": "sz_002102", "node_id": "gold_mining", "activity_type": "operate", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:黄金探矿及采矿")},
    {"exposure_id": "sz_002102_provide_service_plastic_trade", "company_id": "sz_002102", "node_id": "plastic_trade", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:塑料贸易")},
    {"exposure_id": "sz_002102_provide_service_real_estate_leasing", "company_id": "sz_002102", "node_id": "real_estate_leasing", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:房地产租赁")},
    {"exposure_id": "sz_002102_provide_service_technical_service", "company_id": "sz_002102", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002101_produce_aluminum_die_casting", "company_id": "sz_002101", "node_id": "aluminum_die_casting", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:铝合金压铸件")},
    {"exposure_id": "sz_002101_produce_auto_interior_exterior_trim", "company_id": "sz_002101", "node_id": "auto_interior_exterior_trim", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:汽车内外饰件")},
    {"exposure_id": "sz_002101_produce_automotive_part", "company_id": "sz_002101", "node_id": "automotive_part", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:汽车零部件")},
    {"exposure_id": "sz_002101_produce_special_purpose_vehicle", "company_id": "sz_002101", "node_id": "special_purpose_vehicle", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:专用车")},
    {"exposure_id": "sz_002101_provide_service_investment_platform", "company_id": "sz_002101", "node_id": "investment_platform", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:投资平台")},
    {"exposure_id": "sz_002101_provide_service_technical_service", "company_id": "sz_002101", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002099_produce_pharmaceutical", "company_id": "sz_002099", "node_id": "pharmaceutical", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:化学合成医药产品")},
    {"exposure_id": "sz_002099_produce_dye", "company_id": "sz_002099", "node_id": "dye", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:染料")},
    {"exposure_id": "sz_002099_produce_active_pharmaceutical_ingredient", "company_id": "sz_002099", "node_id": "active_pharmaceutical_ingredient", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:医药中间体")},
    {"exposure_id": "sz_002099_produce_chemical_drug", "company_id": "sz_002099", "node_id": "chemical_drug", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:原料药")},
    {"exposure_id": "sz_002099_provide_service_technical_service", "company_id": "sz_002099", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002099_produce_cosmetic", "company_id": "sz_002099", "node_id": "cosmetic", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:化妆品")},
]

write_batch(124, NODES_124, EDGES_124, COMPANIES_124, EXPOSURES_124)
print("Batch 124 generated.")
