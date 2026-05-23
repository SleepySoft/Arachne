import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"

evidence_default = {
    "source_title": "tushare_stock_analysis_batch_001",
    "source_url": None,
    "quote": "Derived from company business scope and industry analysis",
    "retrieved_at": "2026-05-23T09:00:00Z"
}

# ====== INDUSTRIES ======
industries = [
    {"industry_id": "banking", "name_zh": "银行业", "industry_type": "curated_view", "description": "涵盖存款、贷款、同业拆借、债券投资等银行核心业务的产业节点集合"},
    {"industry_id": "real_estate", "name_zh": "房地产业", "industry_type": "curated_view", "description": "涵盖土地开发、建筑施工、商品住宅、商业地产、物业服务及房屋租赁的完整产业链"},
    {"industry_id": "software_security", "name_zh": "软件与信息安全", "industry_type": "curated_view", "description": "涵盖操作系统、安全数据库、移动应用安全及安全审计服务的产业节点集合"},
    {"industry_id": "rail_transportation", "name_zh": "轨道交通", "industry_type": "curated_view", "description": "涵盖轨道车辆、信号系统、供电系统及运维服务的轨道交通产业链"},
    {"industry_id": "landscaping", "name_zh": "园林绿化", "industry_type": "curated_view", "description": "涵盖苗木、土壤、园艺材料、景观设计、绿化施工及生态修复的园林绿化产业链"},
    {"industry_id": "new_energy_materials", "name_zh": "新能源新材料", "industry_type": "curated_view", "description": "涵盖硅材料、光伏组件、锂电池正负极材料等新能源新材料产业节点"},
    {"industry_id": "biopharma", "name_zh": "生物医药", "industry_type": "curated_view", "description": "涵盖药品、医疗器械、医药研发及分销服务的生物医药产业链"},
    {"industry_id": "glass_manufacturing", "name_zh": "玻璃制造", "industry_type": "curated_view", "description": "涵盖石英砂、纯碱、浮法玻璃、工程玻璃、电子玻璃及光伏玻璃的玻璃制造产业链"},
]

# ====== INDUSTRY-NODE MAPPINGS ======
mappings = [
    # banking
    {"mapping_id": "banking_contains_public_deposit", "industry_id": "banking", "node_id": "public_deposit", "role": "核心负债来源", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "banking_contains_loan_service", "industry_id": "banking", "node_id": "loan_service", "role": "核心资产业务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "banking_contains_interbank_lending", "industry_id": "banking", "node_id": "interbank_lending_service", "role": "流动性管理", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "banking_contains_bond_investment", "industry_id": "banking", "node_id": "bond_investment_service", "role": "资金运用", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "banking_contains_financial_bond", "industry_id": "banking", "node_id": "financial_bond", "role": "主动负债工具", "weight": 0.6, "confidence": "MEDIUM", "evidence": [evidence_default]},
    
    # real_estate
    {"mapping_id": "re_contains_land", "industry_id": "real_estate", "node_id": "land", "role": "基础要素", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_residential", "industry_id": "real_estate", "node_id": "residential_property", "role": "核心产出", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_commercial", "industry_id": "real_estate", "node_id": "commercial_property", "role": "商业产出", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_construction", "industry_id": "real_estate", "node_id": "construction_service", "role": "核心施工", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_cement", "industry_id": "real_estate", "node_id": "cement", "role": "建筑材料", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_property_mgmt", "industry_id": "real_estate", "node_id": "property_management_service", "role": "后服务", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "re_contains_rental", "industry_id": "real_estate", "node_id": "housing_rental_service", "role": "运营服务", "weight": 0.7, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # software_security
    {"mapping_id": "ss_contains_os", "industry_id": "software_security", "node_id": "operating_system", "role": "基础平台", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "ss_contains_server", "industry_id": "software_security", "node_id": "server_hardware", "role": "基础设施", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "ss_contains_security_db", "industry_id": "software_security", "node_id": "security_database", "role": "数据支撑", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "ss_contains_mobile_security", "industry_id": "software_security", "node_id": "mobile_app_security_service", "role": "核心服务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "ss_contains_emergency_security", "industry_id": "software_security", "node_id": "emergency_security_service", "role": "应急服务", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    
    # rail_transportation
    {"mapping_id": "rail_contains_vehicle", "industry_id": "rail_transportation", "node_id": "rail_vehicle", "role": "核心装备", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "rail_contains_signaling", "industry_id": "rail_transportation", "node_id": "signaling_system", "role": "安全系统", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "rail_contains_power", "industry_id": "rail_transportation", "node_id": "power_supply_system", "role": "动力系统", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "rail_contains_maintenance", "industry_id": "rail_transportation", "node_id": "rail_maintenance_service", "role": "运维服务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # landscaping
    {"mapping_id": "landscaping_contains_nursery", "industry_id": "landscaping", "node_id": "nursery_stock", "role": "植物材料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "landscaping_contains_soil", "industry_id": "landscaping", "node_id": "soil", "role": "栽培介质", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "landscaping_contains_gardening", "industry_id": "landscaping", "node_id": "gardening_material", "role": "辅助材料", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    {"mapping_id": "landscaping_contains_design", "industry_id": "landscaping", "node_id": "landscape_design_service", "role": "前端设计", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "landscaping_contains_greening", "industry_id": "landscaping", "node_id": "greening_construction_service", "role": "核心施工", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "landscaping_contains_eco_restore", "industry_id": "landscaping", "node_id": "ecological_restoration_service", "role": "延伸服务", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # new_energy_materials
    {"mapping_id": "nem_contains_silicon", "industry_id": "new_energy_materials", "node_id": "silicon_material", "role": "上游材料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_pv_module", "industry_id": "new_energy_materials", "node_id": "photovoltaic_module", "role": "终端产品", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_pv_glass", "industry_id": "new_energy_materials", "node_id": "pv_glass", "role": "组件材料", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_natural_graphite", "industry_id": "new_energy_materials", "node_id": "natural_graphite", "role": "负极原料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_needle_coke", "industry_id": "new_energy_materials", "node_id": "needle_coke", "role": "负极原料", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_lithium_salt", "industry_id": "new_energy_materials", "node_id": "lithium_salt", "role": "正极原料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_anode", "industry_id": "new_energy_materials", "node_id": "lithium_battery_anode", "role": "电池材料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "nem_contains_cathode", "industry_id": "new_energy_materials", "node_id": "lithium_battery_cathode", "role": "电池材料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # biopharma
    {"mapping_id": "bp_contains_drug", "industry_id": "biopharma", "node_id": "pharmaceutical_product", "role": "核心产品", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "bp_contains_device", "industry_id": "biopharma", "node_id": "medical_device", "role": "医疗器械", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "bp_contains_distribution", "industry_id": "biopharma", "node_id": "pharmaceutical_distribution", "role": "分销服务", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "bp_contains_retail", "industry_id": "biopharma", "node_id": "pharmaceutical_retail", "role": "零售服务", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    
    # glass_manufacturing
    {"mapping_id": "glass_contains_quartz", "industry_id": "glass_manufacturing", "node_id": "quartz_sand", "role": "主要原料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_soda", "industry_id": "glass_manufacturing", "node_id": "soda_ash", "role": "主要原料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_gas", "industry_id": "glass_manufacturing", "node_id": "natural_gas", "role": "能源输入", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_float", "industry_id": "glass_manufacturing", "node_id": "float_glass", "role": "基础产品", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_eng", "industry_id": "glass_manufacturing", "node_id": "engineering_glass", "role": "深加工产品", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_elec", "industry_id": "glass_manufacturing", "node_id": "electronic_glass", "role": "电子级产品", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"mapping_id": "glass_contains_pv", "industry_id": "glass_manufacturing", "node_id": "pv_glass", "role": "光伏级产品", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
]

# ====== COMPANIES ======
companies = [
    {"company_id": "pingan_bank", "name_zh": "平安银行", "name_en": "Ping An Bank", "stock_codes": ["000001.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1987, "employee_count": 41698, "revenue_cny": 164699000000.0, "market_cap_cny": 207255206355.0, "company_type": "public", "description": "全国性股份制商业银行，主营业务包括存贷款、同业业务、债券投资等。"},
    {"company_id": "vanke", "name_zh": "万科A", "name_en": "China Vanke", "stock_codes": ["000002.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1984, "employee_count": 131429, "revenue_cny": 465739076702.23, "market_cap_cny": 41280254770.0, "company_type": "public", "description": "全国性房地产开发企业，主营业务包括房地产开发和物业服务。"},
    {"company_id": "guohua_security", "name_zh": "国华网安", "name_en": "Guohua Cyber Security", "stock_codes": ["000004.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1986, "employee_count": 302, "revenue_cny": 110048548.32, "market_cap_cny": 365369578.0, "company_type": "public", "description": "移动应用安全服务提供商，主营业务包括移动互联网游戏和移动应用安全服务。"},
    {"company_id": "zhenye_real_estate", "name_zh": "深振业A", "name_en": "Shenzhen Zhenye Group", "stock_codes": ["000006.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1989, "employee_count": 417, "revenue_cny": 2810603447.85, "market_cap_cny": 14687946100.0, "company_type": "public", "description": "区域性房地产开发企业，主营业务为商品住宅开发和物业租赁。"},
    {"company_id": "quanxinhao", "name_zh": "全新好", "name_en": "Shenzhen Quanxinhao", "stock_codes": ["000007.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1983, "employee_count": 146, "revenue_cny": 216387969.48, "market_cap_cny": 4316742628.0, "company_type": "public", "description": "物业管理和房屋租赁企业。"},
    {"company_id": "shenzhou_highspeed", "name_zh": "神州高铁", "name_en": "Shenzhou High-Speed Railway", "stock_codes": ["000008.SZ"], "country": "CN", "province": "北京", "city": "北京市", "founded_year": 1989, "employee_count": 1914, "revenue_cny": 2511647824.07, "market_cap_cny": 7116909529.0, "company_type": "public", "description": "轨道交通运维服务提供商，主营业务包括轨道交通专用设备和运维服务。"},
    {"company_id": "china_baoan", "name_zh": "中国宝安", "name_en": "China Baoan Group", "stock_codes": ["000009.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1990, "employee_count": 16658, "revenue_cny": 30706431930.72, "market_cap_cny": 20014700368.0, "company_type": "public", "description": "多元化产业集团，主营业务包括新材料（锂电池材料）、新能源（光伏）、生物医药和房地产。"},
    {"company_id": "meili_ecology", "name_zh": "美丽生态", "name_en": "Meili Ecology", "stock_codes": ["000010.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1989, "employee_count": 152, "revenue_cny": 302915567.26, "market_cap_cny": 2563724611.0, "company_type": "public", "description": "园林绿化和生态修复企业，主营业务包括园林绿化工程和生态修复服务。"},
    {"company_id": "shenwu_property", "name_zh": "深物业A", "name_en": "Shenzhen Property Development", "stock_codes": ["000011.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1983, "employee_count": 8769, "revenue_cny": 2965117025.04, "market_cap_cny": 4505601936.0, "company_type": "public", "description": "房地产开发企业，主营业务包括房地产开发、物业管理和出租车运营。"},
    {"company_id": "csgholding", "name_zh": "南玻A", "name_en": "CSG Holding", "stock_codes": ["000012.SZ"], "country": "CN", "province": "广东", "city": "深圳市", "founded_year": 1984, "employee_count": 15217, "revenue_cny": 18194864366.0, "market_cap_cny": 13386862768.0, "company_type": "public", "description": "玻璃制造和新能源企业，主要产品包括平板玻璃、工程玻璃、电子玻璃、光伏玻璃及光伏组件。"},
]

# ====== COMPANY-NODE EXPOSURES ======
exposures = [
    # Ping An Bank
    {"exposure_id": "pingan_provides_loan", "company_id": "pingan_bank", "node_id": "loan_service", "activity_type": "provide_service", "role": "核心贷款服务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "pingan_provides_interbank", "company_id": "pingan_bank", "node_id": "interbank_lending_service", "activity_type": "provide_service", "role": "同业拆借服务", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "pingan_provides_bond_inv", "company_id": "pingan_bank", "node_id": "bond_investment_service", "activity_type": "provide_service", "role": "债券投资服务", "weight": 0.7, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "pingan_uses_deposit", "company_id": "pingan_bank", "node_id": "public_deposit", "activity_type": "use", "role": "资金来源", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # Vanke
    {"exposure_id": "vanke_produces_residential", "company_id": "vanke", "node_id": "residential_property", "activity_type": "produce", "role": "核心产品", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "vanke_produces_commercial", "company_id": "vanke", "node_id": "commercial_property", "activity_type": "produce", "role": "商业产品", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "vanke_provides_property_mgmt", "company_id": "vanke", "node_id": "property_management_service", "activity_type": "provide_service", "role": "物业服务", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # Guohua Security
    {"exposure_id": "guohua_provides_mobile_security", "company_id": "guohua_security", "node_id": "mobile_app_security_service", "activity_type": "provide_service", "role": "核心安全服务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # Zhenye
    {"exposure_id": "zhenye_produces_residential", "company_id": "zhenye_real_estate", "node_id": "residential_property", "activity_type": "produce", "role": "核心产品", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "zhenye_provides_rental", "company_id": "zhenye_real_estate", "node_id": "housing_rental_service", "activity_type": "provide_service", "role": "租赁服务", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # Quanxinhao
    {"exposure_id": "quanxinhao_provides_property_mgmt", "company_id": "quanxinhao", "node_id": "property_management_service", "activity_type": "provide_service", "role": "物业管理", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "quanxinhao_provides_rental", "company_id": "quanxinhao", "node_id": "housing_rental_service", "activity_type": "provide_service", "role": "房屋租赁", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # Shenzhou Highspeed
    {"exposure_id": "shenzhou_provides_rail_maint", "company_id": "shenzhou_highspeed", "node_id": "rail_maintenance_service", "activity_type": "provide_service", "role": "核心运维服务", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # China Baoan
    {"exposure_id": "baoan_manufactures_anode", "company_id": "china_baoan", "node_id": "lithium_battery_anode", "activity_type": "manufacture", "role": "锂电池负极材料", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "baoan_manufactures_cathode", "company_id": "china_baoan", "node_id": "lithium_battery_cathode", "activity_type": "manufacture", "role": "锂电池正极材料", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "baoan_manufactures_pv_module", "company_id": "china_baoan", "node_id": "photovoltaic_module", "activity_type": "manufacture", "role": "光伏组件", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "baoan_produces_drug", "company_id": "china_baoan", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "药品", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    {"exposure_id": "baoan_produces_residential", "company_id": "china_baoan", "node_id": "residential_property", "activity_type": "produce", "role": "房地产开发", "weight": 0.6, "confidence": "MEDIUM", "evidence": [evidence_default]},
    
    # Meili Ecology
    {"exposure_id": "meili_provides_greening", "company_id": "meili_ecology", "node_id": "greening_construction_service", "activity_type": "provide_service", "role": "核心绿化施工", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "meili_provides_eco_restore", "company_id": "meili_ecology", "node_id": "ecological_restoration_service", "activity_type": "provide_service", "role": "生态修复", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "meili_provides_landscape_design", "company_id": "meili_ecology", "node_id": "landscape_design_service", "activity_type": "provide_service", "role": "景观设计", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    
    # Shenwu Property
    {"exposure_id": "shenwu_produces_residential", "company_id": "shenwu_property", "node_id": "residential_property", "activity_type": "produce", "role": "房地产开发", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "shenwu_provides_property_mgmt", "company_id": "shenwu_property", "node_id": "property_management_service", "activity_type": "provide_service", "role": "物业管理", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    
    # CSG Holding
    {"exposure_id": "csg_manufactures_float_glass", "company_id": "csgholding", "node_id": "float_glass", "activity_type": "manufacture", "role": "浮法玻璃", "weight": 1.0, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "csg_manufactures_eng_glass", "company_id": "csgholding", "node_id": "engineering_glass", "activity_type": "manufacture", "role": "工程玻璃", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "csg_manufactures_elec_glass", "company_id": "csgholding", "node_id": "electronic_glass", "activity_type": "manufacture", "role": "电子玻璃", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "csg_manufactures_pv_glass", "company_id": "csgholding", "node_id": "pv_glass", "activity_type": "manufacture", "role": "光伏玻璃", "weight": 0.9, "confidence": "HIGH", "evidence": [evidence_default]},
    {"exposure_id": "csg_manufactures_silicon", "company_id": "csgholding", "node_id": "silicon_material", "activity_type": "manufacture", "role": "硅材料", "weight": 0.7, "confidence": "MEDIUM", "evidence": [evidence_default]},
    {"exposure_id": "csg_manufactures_pv_module", "company_id": "csgholding", "node_id": "photovoltaic_module", "activity_type": "manufacture", "role": "光伏组件", "weight": 0.8, "confidence": "HIGH", "evidence": [evidence_default]},
]

batch = {
    "batch_id": "batch_001_business_registration",
    "task_description": "Batch 001: 10家上市公司产业分析与公司视图构建",
    "industries_to_upsert": industries,
    "industry_node_mappings_to_upsert": mappings,
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print(f"Submitting business batch with {len(industries)} industries, {len(mappings)} mappings, {len(companies)} companies, {len(exposures)} exposures...")
resp = requests.post(f"{BASE_URL}/business-batches", json=batch)
print(f"Status: {resp.status_code}")
if resp.status_code == 200 or resp.status_code == 201:
    result = resp.json()
    print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)[:1000]}")
else:
    print(f"Error: {resp.text[:500]}")
