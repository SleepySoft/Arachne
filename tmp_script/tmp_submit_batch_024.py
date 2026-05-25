#!/usr/bin/env python3
"""Batch 024 Submission Script"""
import json
import requests

BASE_URL = "http://localhost:8000/api/v1"

def submit_graph_batch(batch):
    r = requests.post(f"{BASE_URL}/batches", json=batch)
    return r.status_code, r.json()

def submit_business_batch(batch):
    r = requests.post(f"{BASE_URL}/business-batches", json=batch)
    return r.status_code, r.json()

# ---------------------------------------------------------------------------
# 1. INDUSTRIAL NODES
# ---------------------------------------------------------------------------

nodes = [
    {
        "node_id": "rice_seed",
        "canonical_name_zh": "水稻种子",
        "canonical_name_en": "Rice Seed",
        "aliases": ["稻种", "杂交水稻种子"],
        "definition": "经过选育、繁育和加工处理，具备优良农艺性状（高产、抗病、优质）的水稻繁殖材料，是水稻种植业的核心上游投入品。",
        "entity_type": "material",
        "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:水稻类种子"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "corn_seed",
        "canonical_name_zh": "玉米种子",
        "canonical_name_en": "Corn Seed",
        "aliases": ["玉米杂交种", "苞米种子"],
        "definition": "经过杂交育种和精选加工，具备高产、抗倒伏、耐密植等优良性状的玉米繁殖材料，是玉米种植产业链的起点。",
        "entity_type": "material",
        "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:...玉米类种子"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "seed_production",
        "canonical_name_zh": "种子生产",
        "canonical_name_en": "Seed Production",
        "aliases": ["种子繁育", "制种"],
        "definition": "通过育种、原种繁殖、大田制种、精选加工、包衣包装等工序，规模化生产符合质量标准的农作物种子的产业活动。",
        "entity_type": "service",
        "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:水稻类种子,玉米类种子,农化产品"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "black_sesame_product",
        "canonical_name_zh": "黑芝麻食品",
        "canonical_name_en": "Black Sesame Product",
        "aliases": ["芝麻糊", "黑芝麻糊"],
        "definition": "以黑芝麻为主要原料，经烘焙、研磨、调配等工艺加工而成的营养食品，包括黑芝麻糊、黑芝麻丸、黑芝麻饼等传统健康食品。",
        "entity_type": "material",
        "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:黑芝麻系列食品,饮料"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "sesame_beverage",
        "canonical_name_zh": "芝麻饮料",
        "canonical_name_en": "Sesame Beverage",
        "aliases": ["黑芝麻乳", "芝麻饮品"],
        "definition": "以黑芝麻或芝麻提取物为主要原料，经调配、均质、杀菌等工艺制成的植物蛋白饮料或谷物饮料。",
        "entity_type": "material",
        "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:黑芝麻系列食品,饮料"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "news_media_service",
        "canonical_name_zh": "新闻媒体服务",
        "canonical_name_en": "News Media Service",
        "aliases": ["新闻传媒", "媒体运营"],
        "definition": "以报纸、期刊、网站、客户端为载体，进行新闻采编、发布与传播的媒体服务业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "publishing_service",
        "canonical_name_zh": "出版服务",
        "canonical_name_en": "Publishing Service",
        "aliases": ["图书出版", "期刊出版"],
        "definition": "对文字、图片作品进行编辑、排版、印刷、发行，以图书、期刊、电子出版物等形式向社会传播的出版服务业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "cultural_industry_service",
        "canonical_name_zh": "文化产业服务",
        "canonical_name_en": "Cultural Industry Service",
        "aliases": ["文化创意服务", "文化运营"],
        "definition": "围绕文化内容的生产、传播与消费提供的一揽子服务，包括出版、传媒、教育、文创、数字内容等领域。",
        "entity_type": "service",
        "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "industrial_park_operation",
        "canonical_name_zh": "产业园运营",
        "canonical_name_en": "Industrial Park Operation",
        "aliases": ["园区运营", "产业园管理"],
        "definition": "对产业园区进行规划、建设、招商、物业管理和产业服务配套，为入驻企业提供空间载体与增值服务的运营活动。",
        "entity_type": "service",
        "evidence": [{"source_title": "新能泰山 主营业务", "quote": "主要业务:产业园开发运营,电线电缆为主业"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "catering_service",
        "canonical_name_zh": "餐饮服务",
        "canonical_name_en": "Catering Service",
        "aliases": ["餐饮经营", "团餐服务"],
        "definition": "为消费者提供现场烹饪、加工及就餐服务的经营活动，包括正餐、快餐、团餐、外卖等业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "西安饮食 主营业务", "quote": "主要业务:餐饮服务和工业化食品生产及销售"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "industrial_food",
        "canonical_name_zh": "工业化食品",
        "canonical_name_en": "Industrial Food",
        "aliases": ["预制食品", "工业化餐饮产品"],
        "definition": "采用工业化标准流程生产的预包装或半成品食品，具有标准化配方、规模化生产和较长保质期的特点，包括速冻食品、中央厨房产品、即食食品等。",
        "entity_type": "material",
        "evidence": [{"source_title": "西安饮食 主营业务", "quote": "工业化食品生产及销售"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "medical_elderly_care_service",
        "canonical_name_zh": "医疗养老服务",
        "canonical_name_en": "Medical and Elderly Care Service",
        "aliases": ["医养结合服务", "康养服务"],
        "definition": "整合医疗服务与养老护理资源，为老年人提供健康管理、疾病诊疗、康复护理、生活照料及精神慰藉的一体化综合服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "湖南发展 主营业务", "quote": "水力发电综合开发经营以及医疗,机构养老,社区居家养老业务的投资,建设及运营管理"}],
        "confidence": "HIGH", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 2. INDUSTRIAL EDGES
# ---------------------------------------------------------------------------

edges = [
    {
        "edge_id": "flow_seed_production_to_rice",
        "from_node": "seed_production",
        "to_node": "rice_seed",
        "description": "种子生产服务产出水稻种子。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:水稻类种子"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_seed_production_to_corn",
        "from_node": "seed_production",
        "to_node": "corn_seed",
        "description": "种子生产服务产出玉米种子。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:...玉米类种子"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_sesame_to_black_sesame",
        "from_node": "grain_oil",
        "to_node": "black_sesame_product",
        "description": "黑芝麻作为粮油作物原料，经加工制成黑芝麻系列食品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:黑芝麻系列食品"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_sesame_to_beverage",
        "from_node": "grain_oil",
        "to_node": "sesame_beverage",
        "description": "芝麻作为原料经调配加工制成芝麻饮料。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:...饮料"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_publishing_to_culture",
        "from_node": "publishing_service",
        "to_node": "cultural_industry_service",
        "description": "出版服务是文化产业服务的重要组成部分，为文化产业链提供内容产品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_news_to_culture",
        "from_node": "news_media_service",
        "to_node": "cultural_industry_service",
        "description": "新闻媒体服务是文化产业服务的信息传播渠道与内容来源。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_industrial_park_to_zone_dev",
        "from_node": "industrial_park_operation",
        "to_node": "industrial_zone_development",
        "description": "产业园运营是工业区开发的后端环节，负责园区的持续经营与企业服务。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "新能泰山 主营业务", "quote": "产业园开发运营"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_catering_to_industrial_food",
        "from_node": "catering_service",
        "to_node": "industrial_food",
        "description": "餐饮服务企业通过中央厨房和标准化生产，将菜品转化为工业化食品产品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "西安饮食 主营业务", "quote": "餐饮服务和工业化食品生产及销售"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_medical_to_elderly_care",
        "from_node": "medical_service",
        "to_node": "medical_elderly_care_service",
        "description": "医疗服务与养老护理整合，形成医养结合的综合养老服务。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "湖南发展 主营业务", "quote": "医疗,机构养老,社区居家养老业务"}],
        "confidence": "HIGH"
    }
]

# ---------------------------------------------------------------------------
# 3. COMPANIES
# ---------------------------------------------------------------------------

companies = [
    {
        "company_id": "jinlong_share",
        "name_zh": "广东锦龙发展股份有限公司",
        "aliases": ["锦龙股份"],
        "stock_codes": ["000712.SZ"],
        "description": "主营业务为证券业务。",
        "country": "CN", "province": "广东", "city": "东莞市",
        "founded_year": 1997, "employee_count": 1237,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "guotou_fengle",
        "name_zh": "国投丰乐种业股份有限公司",
        "aliases": ["国投丰乐", "丰乐种业"],
        "stock_codes": ["000713.SZ"],
        "description": "主要产品包括水稻类种子、玉米类种子、农化产品、餐饮类服务。",
        "country": "CN", "province": "安徽", "city": "合肥市",
        "founded_year": 1997, "employee_count": 1461,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhongxing_commercial",
        "name_zh": "中兴-沈阳商业大厦(集团)股份有限公司",
        "aliases": ["中兴商业"],
        "stock_codes": ["000715.SZ"],
        "description": "主要业务为百货零售。",
        "country": "CN", "province": "辽宁", "city": "沈阳市",
        "founded_year": 1997, "employee_count": 1031,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "black_sesame_group",
        "name_zh": "南方黑芝麻集团股份有限公司",
        "aliases": ["黑芝麻"],
        "stock_codes": ["000716.SZ"],
        "description": "主要产品包括黑芝麻系列食品和饮料，主营业务为黑芝麻产业的经营。",
        "country": "CN", "province": "广西", "city": "玉林市",
        "founded_year": 1993, "employee_count": 1623,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhongnan_steel",
        "name_zh": "广东中南钢铁股份有限公司",
        "aliases": ["中南股份"],
        "stock_codes": ["000717.SZ"],
        "description": "主要产品包括板材、线材、棒材三大系列，主要业务为黑色金属冶炼加工、金属制品、焦炭及煤化工产品的生产、销售等。",
        "country": "CN", "province": "广东", "city": "韶关市",
        "founded_year": 1997, "employee_count": 5155,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "suning_global",
        "name_zh": "苏宁环球股份有限公司",
        "aliases": ["苏宁环球"],
        "stock_codes": ["000718.SZ"],
        "description": "主营业务为房地产开发及混凝土生产、销售。",
        "country": "CN", "province": "吉林", "city": "吉林市",
        "founded_year": 1993, "employee_count": 935,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhongyuan_media",
        "name_zh": "中原大地传媒股份有限公司",
        "aliases": ["中原传媒"],
        "stock_codes": ["000719.SZ"],
        "description": "主营业务为新闻、出版、文化教育产业。",
        "country": "CN", "province": "河南", "city": "焦作市",
        "founded_year": 1996, "employee_count": 12774,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "xinneng_taishan",
        "name_zh": "山东新能泰山发电股份有限公司",
        "aliases": ["新能泰山"],
        "stock_codes": ["000720.SZ"],
        "description": "主要业务为产业园开发运营、电线电缆为主业。",
        "country": "CN", "province": "山东", "city": "泰安市",
        "founded_year": 1994, "employee_count": 637,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "xian_catering",
        "name_zh": "西安饮食股份有限公司",
        "aliases": ["西安饮食"],
        "stock_codes": ["000721.SZ"],
        "description": "主要业务为餐饮服务和工业化食品生产及销售。",
        "country": "CN", "province": "陕西", "city": "西安市",
        "founded_year": 1996, "employee_count": 3106,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "hunan_development",
        "name_zh": "湖南能源集团发展股份有限公司",
        "aliases": ["湖南发展"],
        "stock_codes": ["000722.SZ"],
        "description": "主要业务为水力发电综合开发经营以及医疗、机构养老、社区居家养老业务的投资、建设及运营管理。",
        "country": "CN", "province": "湖南", "city": "长沙市",
        "founded_year": 1993, "employee_count": 196,
        "company_type": "public", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 4. COMPANY NODE EXPOSURES
# ---------------------------------------------------------------------------

exposures = [
    # 锦龙股份
    {"exposure_id": "exp_jl_brokerage", "company_id": "jinlong_share", "node_id": "securities_brokerage", "activity_type": "operate", "role": "证券经纪服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "锦龙股份 主营业务", "quote": "主营业务:证券业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_jl_underwriting", "company_id": "jinlong_share", "node_id": "securities_underwriting", "activity_type": "operate", "role": "证券承销与保荐服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "锦龙股份 主营业务", "quote": "主营业务:证券业务"}], "status": "ACTIVE"},

    # 国投丰乐
    {"exposure_id": "exp_fl_rice_seed", "company_id": "guotou_fengle", "node_id": "rice_seed", "activity_type": "produce", "role": "水稻种子生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:水稻类种子"}], "status": "ACTIVE"},
    {"exposure_id": "exp_fl_corn_seed", "company_id": "guotou_fengle", "node_id": "corn_seed", "activity_type": "produce", "role": "玉米种子生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:...玉米类种子"}], "status": "ACTIVE"},
    {"exposure_id": "exp_fl_seed_prod", "company_id": "guotou_fengle", "node_id": "seed_production", "activity_type": "operate", "role": "种子生产服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:水稻类种子,玉米类种子"}], "status": "ACTIVE"},
    {"exposure_id": "exp_fl_pesticide", "company_id": "guotou_fengle", "node_id": "pesticide", "activity_type": "produce", "role": "农化产品生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "国投丰乐 主营业务", "quote": "主要产品:...农化产品"}], "status": "ACTIVE"},

    # 中兴商业
    {"exposure_id": "exp_zx_dept", "company_id": "zhongxing_commercial", "node_id": "department_store", "activity_type": "operate", "role": "百货零售商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中兴商业 主营业务", "quote": "主要业务:百货零售"}], "status": "ACTIVE"},

    # 黑芝麻
    {"exposure_id": "exp_bz_black_sesame", "company_id": "black_sesame_group", "node_id": "black_sesame_product", "activity_type": "produce", "role": "黑芝麻食品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:黑芝麻系列食品"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bz_sesame_bev", "company_id": "black_sesame_group", "node_id": "sesame_beverage", "activity_type": "produce", "role": "芝麻饮料生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "主要产品:...饮料"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bz_grain_oil", "company_id": "black_sesame_group", "node_id": "grain_oil", "activity_type": "produce", "role": "粮油食品生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "黑芝麻 主营业务", "quote": "致力于黑芝麻产业的经营"}], "status": "ACTIVE"},

    # 中南股份
    {"exposure_id": "exp_zn_plate", "company_id": "zhongnan_steel", "node_id": "steel_plate", "activity_type": "produce", "role": "板材生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中南股份 主营业务", "quote": "主要产品:板材"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zn_wire_rod", "company_id": "zhongnan_steel", "node_id": "steel_wire_rod", "activity_type": "produce", "role": "线材生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中南股份 主营业务", "quote": "主要产品:...线材..."}], "status": "ACTIVE"},
    {"exposure_id": "exp_zn_bar", "company_id": "zhongnan_steel", "node_id": "steel_bar", "activity_type": "produce", "role": "棒材生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中南股份 主营业务", "quote": "主要产品:...棒材..."}], "status": "ACTIVE"},

    # 苏宁环球
    {"exposure_id": "exp_sn_realestate", "company_id": "suning_global", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "苏宁环球 主营业务", "quote": "主营业务:房地产开发"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sn_concrete", "company_id": "suning_global", "node_id": "ready_mixed_concrete", "activity_type": "produce", "role": "商品混凝土生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "苏宁环球 主营业务", "quote": "房地产开发及混凝土生产,销售"}], "status": "ACTIVE"},

    # 中原传媒
    {"exposure_id": "exp_zy_news", "company_id": "zhongyuan_media", "node_id": "news_media_service", "activity_type": "operate", "role": "新闻媒体运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zy_publishing", "company_id": "zhongyuan_media", "node_id": "publishing_service", "activity_type": "operate", "role": "出版服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zy_culture", "company_id": "zhongyuan_media", "node_id": "cultural_industry_service", "activity_type": "operate", "role": "文化产业运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中原传媒 主营业务", "quote": "主营业务:新闻,出版,文化教育产业"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zy_education", "company_id": "zhongyuan_media", "node_id": "education_service", "activity_type": "operate", "role": "教育产业运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "中原传媒 主营业务", "quote": "文化教育产业"}], "status": "ACTIVE"},

    # 新能泰山
    {"exposure_id": "exp_xt_park", "company_id": "xinneng_taishan", "node_id": "industrial_park_operation", "activity_type": "operate", "role": "产业园运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "新能泰山 主营业务", "quote": "主要业务:产业园开发运营"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xt_wire", "company_id": "xinneng_taishan", "node_id": "wire_cable", "activity_type": "manufacture", "role": "电线电缆制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "新能泰山 主营业务", "quote": "电线电缆,电子产品,电器机械及器材...的生产,销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xt_zone", "company_id": "xinneng_taishan", "node_id": "industrial_zone_development", "activity_type": "operate", "role": "工业区开发商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "新能泰山 主营业务", "quote": "产业园开发运营"}], "status": "ACTIVE"},

    # 西安饮食
    {"exposure_id": "exp_xa_catering", "company_id": "xian_catering", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "西安饮食 主营业务", "quote": "主要业务:餐饮服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xa_industrial_food", "company_id": "xian_catering", "node_id": "industrial_food", "activity_type": "produce", "role": "工业化食品生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "西安饮食 主营业务", "quote": "工业化食品生产及销售"}], "status": "ACTIVE"},

    # 湖南发展
    {"exposure_id": "exp_hn_hydro", "company_id": "hunan_development", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水力发电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "湖南发展 主营业务", "quote": "主要业务:水力发电综合开发经营"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hn_medical", "company_id": "hunan_development", "node_id": "medical_service", "activity_type": "operate", "role": "医疗服务运营商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "湖南发展 主营业务", "quote": "医疗...业务的投资,建设及运营管理"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hn_elderly_care", "company_id": "hunan_development", "node_id": "medical_elderly_care_service", "activity_type": "operate", "role": "医养结合服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "湖南发展 主营业务", "quote": "医疗,机构养老,社区居家养老业务"}], "status": "ACTIVE"}
]

# ---------------------------------------------------------------------------
# 5. SUBMIT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph_batch = {
        "batch_id": "batch_024_graph",
        "task_description": "Batch 024: Industrial nodes and edges for 10 companies (000712-000722). Focus on seeds, sesame foods, steel products, real estate, media publishing, industrial parks, catering, and hydro power.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }

    business_batch = {
        "batch_id": "batch_024_business",
        "task_description": "Batch 024: Company registrations and node exposures for 10 companies (000712-000722).",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures
    }

    print("Submitting graph batch...")
    status, resp = submit_graph_batch(graph_batch)
    print(f"Graph batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    print("\nSubmitting business batch...")
    status, resp = submit_business_batch(business_batch)
    print(f"Business batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))
