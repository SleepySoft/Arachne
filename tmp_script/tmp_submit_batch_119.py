#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, subprocess, os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(BASE_DIR, "cli", "arachne_cli.py")
PY = os.path.join(BASE_DIR, "backend", "venv", "Scripts", "python.exe")

def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

NODES = [
    {"node_id": "international_engineering_contracting", "canonical_name_zh": "国际工程总承包", "canonical_name_en": "international engineering contracting", "entity_type": "service", "aliases": [], "definition": "受国外业主委托，按照合同约定对工程建设项目实行全过程或若干阶段的承包", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中工国际主营业务")},
    {"node_id": "complete_equipment_export", "canonical_name_zh": "成套设备出口", "canonical_name_en": "complete equipment export", "entity_type": "service", "aliases": [], "definition": "将工程项目所需的设备、材料和技术整体出口到国外", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中工国际主营业务")},
    {"node_id": "overseas_project", "canonical_name_zh": "境外工程", "canonical_name_en": "overseas project", "entity_type": "service", "aliases": [], "definition": "在中国境外实施的各类工程建设项目", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中工国际经营范围")},
    {"node_id": "digital_tv_receiver", "canonical_name_zh": "数字电视接收设备", "canonical_name_en": "digital TV receiver", "entity_type": "device", "aliases": [], "definition": "用于接收和解码数字电视信号的设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("同洲电子主营业务")},
    {"node_id": "led_display", "canonical_name_zh": "LED电子显示屏", "canonical_name_en": "LED display", "entity_type": "device", "aliases": [], "definition": "利用发光二极管作为显示元件的电子显示设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("同洲电子主营业务")},
    {"node_id": "industrial_salt", "canonical_name_zh": "工业盐", "canonical_name_en": "industrial salt", "entity_type": "material", "aliases": [], "definition": "用于工业生产的氯化钠，包括两碱工业用盐、印染工业用盐等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("云南能投主营业务")},
    {"node_id": "mirabilite", "canonical_name_zh": "芒硝", "canonical_name_en": "mirabilite", "entity_type": "material", "aliases": ["sodium sulfate"], "definition": "十水合硫酸钠矿物，用于制革、造纸、玻璃、洗涤剂等行业", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("云南能投主营业务")},
    {"node_id": "wind_power", "canonical_name_zh": "风力发电", "canonical_name_en": "wind power", "entity_type": "service", "aliases": [], "definition": "利用风力驱动风力发电机组产生电能的可再生能源发电方式", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("云南能投经营范围")},
    {"node_id": "commercial_bank", "canonical_name_zh": "商业银行", "canonical_name_en": "commercial bank", "entity_type": "service", "aliases": [], "definition": "以营利为目的，经营存贷款、结算等业务的金融机构", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国银行主营业务")},
    {"node_id": "investment_bank", "canonical_name_zh": "投资银行", "canonical_name_en": "investment bank", "entity_type": "service", "aliases": [], "definition": "从事证券发行、承销、交易、企业重组、兼并与收购等业务的金融机构", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国银行主营业务")},
    {"node_id": "insurance", "canonical_name_zh": "保险", "canonical_name_en": "insurance", "entity_type": "service", "aliases": [], "definition": "通过合同约定，对可能发生的事故所造成的财产损失或人身伤害承担赔偿责任的金融服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国银行主营业务")},
    {"node_id": "foreign_exchange", "canonical_name_zh": "外汇", "canonical_name_en": "foreign exchange", "entity_type": "material", "aliases": [], "definition": "以外币表示的用于国际结算的支付手段和资产", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国银行经营范围")},
    {"node_id": "fine_chemical", "canonical_name_zh": "精细化学品", "canonical_name_en": "fine chemical", "entity_type": "material", "aliases": [], "definition": "具有特定应用功能、技术密集度高、附加值高的化工产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("德美化工主营业务")},
    {"node_id": "petrochemical_product", "canonical_name_zh": "石油化工品", "canonical_name_en": "petrochemical product", "entity_type": "material", "aliases": [], "definition": "以石油和天然气为原料生产的各类化学产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("德美化工主营业务")},
    {"node_id": "printing_ink", "canonical_name_zh": "油墨", "canonical_name_en": "printing ink", "entity_type": "material", "aliases": [], "definition": "用于印刷的着色材料，由颜料、连结料、助剂等组成", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("德美化工经营范围")},
    {"node_id": "automotive_connector", "canonical_name_zh": "汽车连接器", "canonical_name_en": "automotive connector", "entity_type": "component", "aliases": [], "definition": "用于汽车电路系统中电气连接的专用连接器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("得润电子主营业务")},
    {"node_id": "wire_harness", "canonical_name_zh": "线束", "canonical_name_en": "wire harness", "entity_type": "component", "aliases": [], "definition": "由导线、端子、护套等组成的电路连接组件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("得润电子主营业务")},
    {"node_id": "flexible_printed_circuit", "canonical_name_zh": "柔性线路板", "canonical_name_en": "flexible printed circuit", "entity_type": "component", "aliases": ["FPC"], "definition": "以聚酰亚胺或聚酯薄膜为基材制成的可挠性印刷电路板", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("得润电子经营范围")},
    {"node_id": "crystalline_silicon_solar_cell", "canonical_name_zh": "晶体硅太阳能电池片", "canonical_name_en": "crystalline silicon solar cell", "entity_type": "component", "aliases": [], "definition": "以晶体硅为材料制成的将光能转换为电能的半导体器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("横店东磁主营业务")},
    {"node_id": "permanent_magnet_ferrite", "canonical_name_zh": "永磁铁氧体", "canonical_name_en": "permanent magnet ferrite", "entity_type": "material", "aliases": [], "definition": "具有永久磁性的铁氧体材料，用于制造永磁电机、扬声器等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("横店东磁主营业务")},
    {"node_id": "soft_magnet_ferrite", "canonical_name_zh": "软磁铁氧体", "canonical_name_en": "soft magnet ferrite", "entity_type": "material", "aliases": [], "definition": "易于磁化和退磁的铁氧体材料，用于制造变压器、电感器等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("横店东磁主营业务")},
    {"node_id": "solar_pv_equipment", "canonical_name_zh": "太阳能光伏设备", "canonical_name_en": "solar photovoltaic equipment", "entity_type": "device", "aliases": [], "definition": "用于太阳能光伏发电系统的各类设备和装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("横店东磁经营范围")},
    {"node_id": "property_management", "canonical_name_zh": "物业管理", "canonical_name_en": "property management", "entity_type": "service", "aliases": [], "definition": "对物业进行维护、保养、管理，为业主和使用人提供服务的活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("保利发展经营范围")},
    {"node_id": "house_leasing", "canonical_name_zh": "房屋租赁", "canonical_name_en": "house leasing", "entity_type": "service", "aliases": [], "definition": "将房屋出租给承租人使用并收取租金的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("保利发展经营范围")},
    {"node_id": "manganese_tetroxide", "canonical_name_zh": "四氧化三锰", "canonical_name_en": "manganese tetroxide", "entity_type": "material", "aliases": [], "definition": "化学式为Mn3O4的锰氧化物，用于制造软磁铁氧体和锂电池正极材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中钢天源主营业务")},
    {"node_id": "permanent_magnet_device", "canonical_name_zh": "永磁器件", "canonical_name_en": "permanent magnet device", "entity_type": "component", "aliases": [], "definition": "利用永磁材料制成的具有永久磁性的功能器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中钢天源主营业务")},
    {"node_id": "electronic_special_material", "canonical_name_zh": "电子专用材料", "canonical_name_en": "electronic special material", "entity_type": "material", "aliases": [], "definition": "用于电子元器件和集成电路制造的专用功能材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中钢天源经营范围")},
    {"node_id": "graphite_carbon_product", "canonical_name_zh": "石墨及碳素制品", "canonical_name_en": "graphite and carbon product", "entity_type": "material", "aliases": [], "definition": "以石墨和碳素为原料制成的各类产品，如电极、坩埚等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中钢天源经营范围")},
    {"node_id": "graphene", "canonical_name_zh": "石墨烯", "canonical_name_en": "graphene", "entity_type": "material", "aliases": [], "definition": "由碳原子以sp2杂化方式形成的单层二维蜂窝状晶格结构新材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中钢天源经营范围")},
]

EDGES = [
    {"edge_id": "complete_equipment_export_international_engineering_contracting", "from_node": "complete_equipment_export", "to_node": "international_engineering_contracting", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "成套设备出口是国际工程承包的重要组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "overseas_project_international_engineering_contracting", "from_node": "overseas_project", "to_node": "international_engineering_contracting", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "境外工程是国际工程承包的实施载体", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "digital_tv_receiver_communication_equipment", "from_node": "digital_tv_receiver", "to_node": "communication_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "数字电视接收设备属于通信设备范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "led_display_electronic_component", "from_node": "led_display", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "LED显示屏由电子元器件组成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "industrial_salt_mirabilite", "from_node": "industrial_salt", "to_node": "mirabilite", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "工业盐和芒硝均为盐化工产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "wind_power_solar_power_generation", "from_node": "wind_power", "to_node": "solar_power_generation", "edge_namespace": "industrial_flow", "edge_type": "energy_flow", "description": "风电和光伏发电同属可再生能源发电", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "commercial_bank_banking_service", "from_node": "commercial_bank", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业银行提供银行服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "investment_bank_banking_service", "from_node": "investment_bank", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "投资银行提供银行服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "insurance_financial_service", "from_node": "insurance", "to_node": "financial_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "保险是金融服务的重要组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "foreign_exchange_banking_service", "from_node": "foreign_exchange", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "外汇业务是银行服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "fine_chemical_chemical_product", "from_node": "fine_chemical", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "精细化学品是化工产品的一类", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "petrochemical_product_chemical_product", "from_node": "petrochemical_product", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "石油化工品是化工产品的一类", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "printing_ink_coating", "from_node": "printing_ink", "to_node": "coating", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "油墨和涂料同属涂装材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "automotive_connector_automotive_part", "from_node": "automotive_connector", "to_node": "automotive_part", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "汽车连接器是汽车零部件的一类", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "wire_harness_automotive_part", "from_node": "wire_harness", "to_node": "automotive_part", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "线束是汽车零部件的一类", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "flexible_printed_circuit_electronic_component", "from_node": "flexible_printed_circuit", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "柔性线路板是电子元器件的一类", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "crystalline_silicon_solar_cell_solar_cell", "from_node": "crystalline_silicon_solar_cell", "to_node": "solar_cell", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "晶体硅太阳能电池片是太阳能电池的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "permanent_magnet_ferrite_magnetic_material", "from_node": "permanent_magnet_ferrite", "to_node": "magnetic_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "永磁铁氧体是磁性材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "soft_magnet_ferrite_magnetic_material", "from_node": "soft_magnet_ferrite", "to_node": "magnetic_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "软磁铁氧体是磁性材料的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "solar_pv_equipment_solar_cell", "from_node": "solar_pv_equipment", "to_node": "solar_cell", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "太阳能光伏设备包含太阳能电池", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "property_management_real_estate_development", "from_node": "property_management", "to_node": "real_estate_development", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "物业管理服务于房地产开发", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "house_leasing_real_estate_development", "from_node": "house_leasing", "to_node": "real_estate_development", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "房屋租赁是房地产开发的后续服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "manganese_tetroxide_soft_magnet_ferrite", "from_node": "manganese_tetroxide", "to_node": "soft_magnet_ferrite", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "四氧化三锰是生产软磁铁氧体的原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "permanent_magnet_device_permanent_magnet_ferrite", "from_node": "permanent_magnet_device", "to_node": "permanent_magnet_ferrite", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "永磁器件以永磁铁氧体等材料制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "graphite_carbon_product_new_material", "from_node": "graphite_carbon_product", "to_node": "new_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "石墨及碳素制品属于新材料范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "graphene_new_material", "from_node": "graphene", "to_node": "new_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "石墨烯是新型材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

BUSINESS = {
    "batch_id": "batch_119_business",
    "task_description": "Batch 119 business registration for 10 A-share companies",
    "companies_to_upsert": [
        {"company_id": "sz_002051", "name_zh": "中工国际", "name_en": "China CAMC Engineering Co., Ltd.", "country": "CN", "province": "北京", "city": "北京市", "stock_codes": ["002051.SZ"], "description": "国际工程总承包及成套设备与技术出口", "founded_year": 2001, "employee_count": 4055},
        {"company_id": "sz_002052", "name_zh": "同洲电子", "name_en": "Shenzhen Coship Electronics Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["002052.SZ"], "description": "数字电视接收设备、机顶盒、LED显示屏等", "founded_year": 1994, "employee_count": 215},
        {"company_id": "sz_002053", "name_zh": "云南能投", "name_en": "Yunnan Energy Investment Co., Ltd.", "country": "CN", "province": "云南", "city": "昆明市", "stock_codes": ["002053.SZ"], "description": "食盐、工业盐、日化盐、芒硝及天然气、风电、太阳能发电", "founded_year": 2002, "employee_count": 1560},
        {"company_id": "sh_601001", "name_zh": "晋控煤业", "name_en": "Jinneng Holding Shanxi Coal Co., Ltd.", "country": "CN", "province": "山西", "city": "大同市", "stock_codes": ["601001.SH"], "description": "煤炭开采、洗选及煤炭产品销售", "founded_year": 2001, "employee_count": 9595},
        {"company_id": "sh_601988", "name_zh": "中国银行", "name_en": "Bank of China Limited", "country": "CN", "province": "北京", "city": "北京市", "stock_codes": ["601988.SH"], "description": "商业银行业务、投资银行业务及保险业务", "founded_year": 1983, "employee_count": 313746},
        {"company_id": "sz_002054", "name_zh": "德美化工", "name_en": "Guangdong Dynatic Chemicals Co., Ltd.", "country": "CN", "province": "广东", "city": "佛山市", "stock_codes": ["002054.SZ"], "description": "精细化学品、石油化工品和农牧食品", "founded_year": 2002, "employee_count": 1852},
        {"company_id": "sz_002055", "name_zh": "得润电子", "name_en": "Shenzhen Deren Electronic Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["002055.SZ"], "description": "电子连接器、汽车连接器及线束、汽车零部件", "founded_year": 1992, "employee_count": 5259},
        {"company_id": "sz_002056", "name_zh": "横店东磁", "name_en": "Hengdian Group DMEGC Magnetics Co., Ltd.", "country": "CN", "province": "浙江", "city": "金华市", "stock_codes": ["002056.SZ"], "description": "晶体硅太阳能电池片、永磁铁氧体、软磁铁氧体", "founded_year": 1999, "employee_count": 19159},
        {"company_id": "sh_600048", "name_zh": "保利发展", "name_en": "Poly Developments and Holdings Group Co., Ltd.", "country": "CN", "province": "广东", "city": "广州市", "stock_codes": ["600048.SH"], "description": "房地产开发、销售、租赁及其物业管理", "founded_year": 1992, "employee_count": 49790},
        {"company_id": "sz_002057", "name_zh": "中钢天源", "name_en": "Sinosteel Anhui Tianyuan Technology Co., Ltd.", "country": "CN", "province": "安徽", "city": "马鞍山市", "stock_codes": ["002057.SZ"], "description": "四氧化三锰、钢丝、永磁器件及磁性材料", "founded_year": 2002, "employee_count": 1133},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sz_002051_provide_service_international_engineering_contracting", "company_id": "sz_002051", "node_id": "international_engineering_contracting", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:国际工程总承包")},
        {"exposure_id": "sz_002051_provide_service_complete_equipment_export", "company_id": "sz_002051", "node_id": "complete_equipment_export", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:成套设备与技术出口")},
        {"exposure_id": "sz_002051_provide_service_overseas_project", "company_id": "sz_002051", "node_id": "overseas_project", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:承包境外工程")},
        {"exposure_id": "sz_002051_provide_service_construction_engineering", "company_id": "sz_002051", "node_id": "construction_engineering", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建设工程")},
        {"exposure_id": "sz_002052_produce_digital_tv_receiver", "company_id": "sz_002052", "node_id": "digital_tv_receiver", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:数字电视接收设备")},
        {"exposure_id": "sz_002052_produce_set_top_box", "company_id": "sz_002052", "node_id": "set_top_box", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:数字有线机顶盒")},
        {"exposure_id": "sz_002052_produce_led_display", "company_id": "sz_002052", "node_id": "led_display", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:LED电子显示屏")},
        {"exposure_id": "sz_002052_produce_communication_equipment", "company_id": "sz_002052", "node_id": "communication_equipment", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:通信设备")},
        {"exposure_id": "sz_002052_produce_integrated_circuit", "company_id": "sz_002052", "node_id": "integrated_circuit", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:集成电路")},
        {"exposure_id": "sz_002052_provide_service_iot", "company_id": "sz_002052", "node_id": "iot_device", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物联网设备")},
        {"exposure_id": "sz_002053_produce_salt", "company_id": "sz_002053", "node_id": "salt", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:食盐")},
        {"exposure_id": "sz_002053_produce_industrial_salt", "company_id": "sz_002053", "node_id": "industrial_salt", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:工业盐")},
        {"exposure_id": "sz_002053_produce_mirabilite", "company_id": "sz_002053", "node_id": "mirabilite", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:芒硝")},
        {"exposure_id": "sz_002053_provide_service_natural_gas_supply", "company_id": "sz_002053", "node_id": "natural_gas_supply", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:天然气销售")},
        {"exposure_id": "sz_002053_operate_wind_power", "company_id": "sz_002053", "node_id": "wind_power", "activity_type": "operate", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:风力发电技术服务")},
        {"exposure_id": "sz_002053_operate_solar_power_generation", "company_id": "sz_002053", "node_id": "solar_power_generation", "activity_type": "operate", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:太阳能发电技术服务")},
        {"exposure_id": "sh_601001_operate_coal_mining", "company_id": "sh_601001", "node_id": "coal_mining", "activity_type": "operate", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:煤炭开采")},
        {"exposure_id": "sh_601001_produce_coal", "company_id": "sh_601001", "node_id": "coal", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:煤炭及制品销售")},
        {"exposure_id": "sh_601001_operate_coal_washing", "company_id": "sh_601001", "node_id": "coal_washing", "activity_type": "operate", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:煤炭洗选")},
        {"exposure_id": "sh_601001_produce_coal_and_products", "company_id": "sh_601001", "node_id": "coal_and_products", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:煤炭及制品销售")},
        {"exposure_id": "sh_601988_provide_service_commercial_bank", "company_id": "sh_601988", "node_id": "commercial_bank", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:商业银行业务")},
        {"exposure_id": "sh_601988_provide_service_investment_bank", "company_id": "sh_601988", "node_id": "investment_bank", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:投资银行业务")},
        {"exposure_id": "sh_601988_provide_service_insurance", "company_id": "sh_601988", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:保险业务")},
        {"exposure_id": "sh_601988_provide_service_banking_service", "company_id": "sh_601988", "node_id": "banking_service", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:吸收存款发放贷款")},
        {"exposure_id": "sh_601988_provide_service_foreign_exchange", "company_id": "sh_601988", "node_id": "foreign_exchange", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:外汇业务")},
        {"exposure_id": "sh_601988_produce_financial_bond", "company_id": "sh_601988", "node_id": "financial_bond", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发行金融债券")},
        {"exposure_id": "sz_002054_produce_fine_chemical", "company_id": "sz_002054", "node_id": "fine_chemical", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:精细化学品")},
        {"exposure_id": "sz_002054_produce_petrochemical_product", "company_id": "sz_002054", "node_id": "petrochemical_product", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:石油化工品")},
        {"exposure_id": "sz_002054_produce_coating", "company_id": "sz_002054", "node_id": "coating", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:涂料制造")},
        {"exposure_id": "sz_002054_produce_printing_ink", "company_id": "sz_002054", "node_id": "printing_ink", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:油墨制造")},
        {"exposure_id": "sz_002054_produce_dye", "company_id": "sz_002054", "node_id": "dye", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:染料制造")},
        {"exposure_id": "sz_002054_produce_daily_chemical_product", "company_id": "sz_002054", "node_id": "daily_chemical_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:日用化学产品制造")},
        {"exposure_id": "sz_002054_provide_service_technical_service", "company_id": "sz_002054", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
        {"exposure_id": "sz_002055_produce_automotive_connector", "company_id": "sz_002055", "node_id": "automotive_connector", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:汽车连接器")},
        {"exposure_id": "sz_002055_produce_wire_harness", "company_id": "sz_002055", "node_id": "wire_harness", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:线束")},
        {"exposure_id": "sz_002055_produce_electronic_connector", "company_id": "sz_002055", "node_id": "electronic_connector", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:电子连接器")},
        {"exposure_id": "sz_002055_produce_flexible_printed_circuit", "company_id": "sz_002055", "node_id": "flexible_printed_circuit", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:柔性线路板")},
        {"exposure_id": "sz_002055_produce_automotive_part", "company_id": "sz_002055", "node_id": "automotive_part", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:汽车零部件")},
        {"exposure_id": "sz_002055_produce_led_display", "company_id": "sz_002055", "node_id": "led_display", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发光二极管")},
        {"exposure_id": "sz_002056_produce_crystalline_silicon_solar_cell", "company_id": "sz_002056", "node_id": "crystalline_silicon_solar_cell", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:晶体硅太阳能电池片")},
        {"exposure_id": "sz_002056_produce_permanent_magnet_ferrite", "company_id": "sz_002056", "node_id": "permanent_magnet_ferrite", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:永磁铁氧体")},
        {"exposure_id": "sz_002056_produce_soft_magnet_ferrite", "company_id": "sz_002056", "node_id": "soft_magnet_ferrite", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:软磁铁氧体")},
        {"exposure_id": "sz_002056_produce_magnetic_material", "company_id": "sz_002056", "node_id": "magnetic_material", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:磁性材料")},
        {"exposure_id": "sz_002056_produce_solar_pv_equipment", "company_id": "sz_002056", "node_id": "solar_pv_equipment", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:光伏设备")},
        {"exposure_id": "sz_002056_produce_battery", "company_id": "sz_002056", "node_id": "battery", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电池制造销售")},
        {"exposure_id": "sh_600048_provide_service_real_estate_development", "company_id": "sh_600048", "node_id": "real_estate_development", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:房地产开发")},
        {"exposure_id": "sh_600048_provide_service_property_management", "company_id": "sh_600048", "node_id": "property_management", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物业管理")},
        {"exposure_id": "sh_600048_provide_service_house_leasing", "company_id": "sh_600048", "node_id": "house_leasing", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:房屋租赁")},
        {"exposure_id": "sh_600048_provide_service_construction_engineering", "company_id": "sh_600048", "node_id": "construction_engineering", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建筑工程")},
        {"exposure_id": "sh_600048_provide_service_construction_service", "company_id": "sh_600048", "node_id": "construction_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建筑施工")},
        {"exposure_id": "sz_002057_produce_manganese_tetroxide", "company_id": "sz_002057", "node_id": "manganese_tetroxide", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:四氧化三锰")},
        {"exposure_id": "sz_002057_produce_steel_wire", "company_id": "sz_002057", "node_id": "steel_wire", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:钢丝")},
        {"exposure_id": "sz_002057_produce_permanent_magnet_device", "company_id": "sz_002057", "node_id": "permanent_magnet_device", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:永磁器件")},
        {"exposure_id": "sz_002057_produce_magnetic_material", "company_id": "sz_002057", "node_id": "magnetic_material", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:磁性材料")},
        {"exposure_id": "sz_002057_produce_rare_earth_functional_material", "company_id": "sz_002057", "node_id": "rare_earth_functional_material", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:稀土功能材料")},
        {"exposure_id": "sz_002057_produce_electronic_special_material", "company_id": "sz_002057", "node_id": "electronic_special_material", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电子专用材料")},
        {"exposure_id": "sz_002057_produce_graphite_carbon_product", "company_id": "sz_002057", "node_id": "graphite_carbon_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:石墨及碳素制品")},
        {"exposure_id": "sz_002057_produce_graphene", "company_id": "sz_002057", "node_id": "graphene", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:石墨烯材料销售")},
    ],
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
}

def submit():
    batch = {"batch_id": "batch_119_nodes", "task_description": "Batch 119 industrial nodes and edges", "nodes_to_upsert": NODES, "edges_to_upsert": EDGES}
    path = os.path.join(BASE_DIR, "tmp_script", "batch_119_nodes.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    r1 = subprocess.run([PY, CLI_PATH, "submit", path], capture_output=True, text=True)
    print("[GRAPH]", r1.stdout[:500], r1.stderr[:500])

    path2 = os.path.join(BASE_DIR, "tmp_script", "batch_119_business.json")
    with open(path2, "w", encoding="utf-8") as f:
        json.dump(BUSINESS, f, ensure_ascii=False, indent=2)
    r2 = subprocess.run([PY, CLI_PATH, "business-batch", path2], capture_output=True, text=True)
    print("[BUSINESS]", r2.stdout[:500], r2.stderr[:500])

if __name__ == "__main__":
    submit()
