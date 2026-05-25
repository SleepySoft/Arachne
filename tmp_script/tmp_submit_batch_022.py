#!/usr/bin/env python3
"""Batch 022 Submission Script"""
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
        "node_id": "port_passenger_service",
        "canonical_name_zh": "港口客运服务",
        "canonical_name_en": "Port Passenger Service",
        "aliases": ["港口客运", "码头客运"],
        "definition": "依托港口码头设施，为旅客提供水路客运、渡运、邮轮停靠及配套服务的水上交通服务业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "中山公用 主营业务", "quote": "港口客运"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "securities_brokerage",
        "canonical_name_zh": "证券经纪服务",
        "canonical_name_en": "Securities Brokerage Service",
        "aliases": ["证券经纪", "股票经纪"],
        "definition": "证券公司接受客户委托，代理买卖证券并收取佣金的金融服务，是证券市场的基础中介业务。",
        "entity_type": "service",
        "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券经纪业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "securities_underwriting",
        "canonical_name_zh": "证券承销与保荐服务",
        "canonical_name_en": "Securities Underwriting and Sponsorship",
        "aliases": ["投行承销", "IPO保荐"],
        "definition": "证券公司为企业股票、债券等证券的公开发行提供承销、配售及上市保荐服务的投行业务。",
        "entity_type": "service",
        "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券承销与保荐业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "securities_proprietary_trading",
        "canonical_name_zh": "证券自营业务",
        "canonical_name_en": "Securities Proprietary Trading",
        "aliases": ["自营投资", "券商自营"],
        "definition": "证券公司以自有资金买卖证券、获取投资收益的自营性投资业务，是券商重要的收入来源之一。",
        "entity_type": "service",
        "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券自营业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "asset_management_service",
        "canonical_name_zh": "资产管理服务",
        "canonical_name_en": "Asset Management Service",
        "aliases": ["资管业务", "受托资产管理"],
        "definition": "金融机构受客户委托，对受托资产进行投资管理、运作和处分，以实现资产保值增值的金融服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券资产管理业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "margin_trading_service",
        "canonical_name_zh": "融资融券服务",
        "canonical_name_en": "Margin Trading and Securities Lending",
        "aliases": ["两融业务", "信用交易"],
        "definition": "证券公司向客户出借资金供其买入证券（融资）或出借证券供其卖出（融券）的信用交易服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "东北证券 主营业务", "quote": "信用交易业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "clean_coal_power_generation",
        "canonical_name_zh": "洁净煤燃烧发电",
        "canonical_name_en": "Clean Coal Power Generation",
        "aliases": ["洁净煤发电", "清洁煤电"],
        "definition": "采用循环流化床、超临界/超超临界、煤气化联合循环（IGCC）等先进清洁燃烧技术，实现煤炭高效低污染燃烧发电的能源服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "宝新能源 主营业务", "quote": "洁净煤燃烧技术发电和可再生能源发电"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "pharmaceutical_intermediate",
        "canonical_name_zh": "医药中间体",
        "canonical_name_en": "Pharmaceutical Intermediate",
        "aliases": ["药物中间体", "合成中间体"],
        "definition": "用于化学合成原料药过程中的中间产物，是原料药生产的重要前体物料，通常需进一步反应纯化才能得到活性药物成分。",
        "entity_type": "material",
        "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "精细化工产品中的医药中间体...的研发,生产和销售"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "pesticide_intermediate",
        "canonical_name_zh": "农药中间体",
        "canonical_name_en": "Pesticide Intermediate",
        "aliases": ["农化中间体"],
        "definition": "用于合成农药原药过程中的关键中间产物，是农药产业链中连接基础化工原料与终端农药制剂的重要环节。",
        "entity_type": "material",
        "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "农药中间体的研发,生产和销售"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "heating_engineering_service",
        "canonical_name_zh": "供暖工程服务",
        "canonical_name_en": "Heating Engineering Service",
        "aliases": ["供热工程", "暖通工程"],
        "definition": "为居民及工商业用户提供供热管网、换热站、锅炉房等供暖设施的设计、施工、安装与维护服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "惠天热电 主营业务", "quote": "为居民及非居民提供供热及供暖工程服务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "industrial_steam",
        "canonical_name_zh": "工业蒸汽",
        "canonical_name_en": "Industrial Steam",
        "aliases": ["饱和蒸汽", "过热蒸汽"],
        "definition": "由工业锅炉或热电联产机组生产的、用于工业生产过程中的热能载体，广泛应用于化工、纺织、造纸、食品加工等行业的加热、烘干、蒸馏等工艺。",
        "entity_type": "material",
        "evidence": [{"source_title": "滨海能源 主营业务", "quote": "蒸汽,电力的生产,供应"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "printing_service",
        "canonical_name_zh": "印刷业务",
        "canonical_name_en": "Printing Service",
        "aliases": ["商业印刷", "包装印刷"],
        "definition": "利用印刷设备将文字、图像转印到纸张、塑料、金属等承印物上的加工服务，包括出版物印刷、包装装潢印刷、文件资料印刷等。",
        "entity_type": "service",
        "evidence": [{"source_title": "滨海能源 主营业务", "quote": "印刷业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "motorcycle_engine",
        "canonical_name_zh": "摩托车发动机",
        "canonical_name_en": "Motorcycle Engine",
        "aliases": ["摩托车动力", "摩托引擎"],
        "definition": "驱动摩托车行驶的内燃机或电动机总成，是摩托车的核心动力部件，按燃料类型可分为汽油机、柴油机和电动机。",
        "entity_type": "subsystem",
        "evidence": [{"source_title": "宗申动力 主营业务", "quote": "主要产品:摩托车发动机及零配件"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "aerospace_precision_part",
        "canonical_name_zh": "航空精密零部件",
        "canonical_name_en": "Aerospace Precision Part",
        "aliases": ["航发零部件", "航空精密件"],
        "definition": "用于航空器发动机、起落架、飞控系统等关键部位的精密加工金属零部件，需满足严格的尺寸精度、材料性能与可靠性要求。",
        "entity_type": "component",
        "evidence": [{"source_title": "炼石航空 主营业务", "quote": "主营产品:各种航空器相关精密零部件,结构件等,包括飞机的机翼前缘表层,发动机相关部件,起降设备,油泵罩等核心部件"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "aircraft_structural_part",
        "canonical_name_zh": "飞机结构件",
        "canonical_name_en": "Aircraft Structural Part",
        "aliases": ["航空结构件", "机体结构件"],
        "definition": "构成飞机机体骨架和气动外形的承力构件，包括机翼前缘、机身框梁、起落架舱门、发动机短舱等，需具备高强度重量比和耐疲劳特性。",
        "entity_type": "component",
        "evidence": [{"source_title": "炼石航空 主营业务", "quote": "主营产品:各种航空器相关精密零部件,结构件等"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "paste_pvc_resin",
        "canonical_name_zh": "糊树脂",
        "canonical_name_en": "Paste PVC Resin",
        "aliases": ["PVC糊树脂", "乳化法PVC"],
        "definition": "聚氯乙烯树脂的一种特殊形态，颗粒粒径极细（1-2μm），可在增塑剂中形成稳定糊状物，适用于涂覆、浸渍、搪塑等成型工艺，广泛用于人造革、地板革、手套、壁纸等产品。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:烧碱,糊树脂,93#汽油,轻柴油,丙烯"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "propylene",
        "canonical_name_zh": "丙烯",
        "canonical_name_en": "Propylene",
        "aliases": [" propene", "甲基乙烯"],
        "definition": "化学式为C₃H₆的无色气体，是重要的基础化工原料，通过石油炼化或蒸汽裂解制得，主要用于生产聚丙烯、丙烯腈、环氧丙烷、异丙醇等下游化工产品。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:烧碱,糊树脂,93#汽油,轻柴油,丙烯"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 2. INDUSTRIAL EDGES
# ---------------------------------------------------------------------------

edges = [
    {
        "edge_id": "flow_pharma_intermediate_to_api",
        "from_node": "pharmaceutical_intermediate",
        "to_node": "active_pharmaceutical_ingredient",
        "description": "医药中间体经进一步化学反应、纯化与结晶，转化为原料药（API）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "医药中间体...的研发,生产和销售"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pesticide_intermediate_to_pesticide",
        "from_node": "pesticide_intermediate",
        "to_node": "pesticide",
        "description": "农药中间体经合成反应转化为农药原药，再经复配制成农药制剂。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "农药中间体的研发,生产和销售"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_heating_engineering_to_supply",
        "from_node": "heating_engineering_service",
        "to_node": "heating_supply",
        "description": "供暖工程服务通过建设供热管网、换热站和热源设施，向社会提供供热服务。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "惠天热电 主营业务", "quote": "为居民及非居民提供供热及供暖工程服务"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_aerospace_part_to_aircraft",
        "from_node": "aerospace_precision_part",
        "to_node": "aircraft",
        "description": "航空精密零部件作为关键组成件装配到航空器发动机、飞控及起落架系统中。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "炼石航空 主营业务", "quote": "各种航空器相关精密零部件...发动机相关部件,起降设备"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_structural_part_to_aircraft",
        "from_node": "aircraft_structural_part",
        "to_node": "aircraft",
        "description": "飞机结构件构成航空器机体骨架和气动外形，是航空器的基础承载结构。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "炼石航空 主营业务", "quote": "各种航空器相关精密零部件,结构件等,包括飞机的机翼前缘表层"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_refinery_to_propylene",
        "from_node": "refining_service",
        "to_node": "propylene",
        "description": "石油炼化过程中的催化裂化与蒸汽裂解装置产出丙烯。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:...丙烯"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "variant_paste_pvc",
        "from_node": "paste_pvc_resin",
        "to_node": "pvc",
        "description": "糊树脂是聚氯乙烯（PVC）树脂的一种特殊形态，具有极细颗粒，可在增塑剂中形成糊状物。",
        "edge_namespace": "ontology",
        "edge_type": "variant_of",
        "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:糊树脂"}],
        "confidence": "HIGH"
    }
]

# ---------------------------------------------------------------------------
# 3. COMPANIES
# ---------------------------------------------------------------------------

companies = [
    {
        "company_id": "zhongshan_public",
        "name_zh": "中山公用事业集团股份有限公司",
        "aliases": ["中山公用"],
        "stock_codes": ["000685.SZ"],
        "description": "主营业务涵盖环保水务、固废处理、工程建设、市场运营、港口客运、金融服务与股权投资等领域。",
        "country": "CN", "province": "广东", "city": "中山市",
        "founded_year": 1992, "employee_count": 5794,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "northeast_securities",
        "name_zh": "东北证券股份有限公司",
        "aliases": ["东北证券"],
        "stock_codes": ["000686.SZ"],
        "description": "主营业务包括证券经纪、证券承销与保荐、证券自营、证券资产管理和信用交易业务等。",
        "country": "CN", "province": "吉林", "city": "长春市",
        "founded_year": 1992, "employee_count": 3656,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "guocheng_mining",
        "name_zh": "国城矿业股份有限公司",
        "aliases": ["国城矿业"],
        "stock_codes": ["000688.SZ"],
        "description": "主营业务为铅锌等有色金属的采选销售及下游硫酸的生产销售等业务。",
        "country": "CN", "province": "四川", "city": "阿坝藏族羌族自治州",
        "founded_year": 1978, "employee_count": 3190,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "baoxin_energy",
        "name_zh": "广东宝丽华新能源股份有限公司",
        "aliases": ["宝新能源"],
        "stock_codes": ["000690.SZ"],
        "description": "主营业务为洁净煤燃烧技术发电和可再生能源发电，新能源电力生产、销售、开发。",
        "country": "CN", "province": "广东", "city": "梅州市",
        "founded_year": 1997, "employee_count": 1258,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "st_yatai",
        "name_zh": "甘肃亚太实业发展股份有限公司",
        "aliases": ["*ST亚太", "亚太实业"],
        "stock_codes": ["000691.SZ"],
        "description": "主营业务由房地产开发变更为精细化工产品中的医药中间体、农药中间体的研发、生产和销售。",
        "country": "CN", "province": "甘肃", "city": "兰州市",
        "founded_year": 1988, "employee_count": 412,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "huitian_thermal",
        "name_zh": "沈阳惠天热电股份有限公司",
        "aliases": ["惠天热电"],
        "stock_codes": ["000692.SZ"],
        "description": "主要业务为居民及非居民提供供热及供暖工程服务。",
        "country": "CN", "province": "辽宁", "city": "沈阳市",
        "founded_year": 1993, "employee_count": 1254,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "binhai_energy",
        "name_zh": "天津滨海能源发展股份有限公司",
        "aliases": ["滨海能源"],
        "stock_codes": ["000695.SZ"],
        "description": "主营业务为蒸汽、电力的生产、供应和印刷业务。",
        "country": "CN", "province": "天津", "city": "天津市",
        "founded_year": 1997, "employee_count": 196,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zongshen_power",
        "name_zh": "重庆宗申动力机械股份有限公司",
        "aliases": ["宗申动力"],
        "stock_codes": ["001696.SZ"],
        "description": "主要产品为摩托车发动机及零配件，同时研发制造通用机械零部件和汽车零部件。",
        "country": "CN", "province": "重庆", "city": "重庆市",
        "founded_year": 1989, "employee_count": 9459,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "lianshi_aviation",
        "name_zh": "炼石航空科技股份有限公司",
        "aliases": ["炼石航空"],
        "stock_codes": ["000697.SZ"],
        "description": "主营产品包括各种航空器相关精密零部件、结构件等，涵盖飞机机翼前缘表层、发动机相关部件、起降设备、油泵罩等核心部件。",
        "country": "CN", "province": "陕西", "city": "咸阳市",
        "founded_year": 1993, "employee_count": 2458,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "st_shenhua",
        "name_zh": "沈阳化工股份有限公司",
        "aliases": ["ST沈化", "沈阳化工"],
        "stock_codes": ["000698.SZ"],
        "description": "主要产品包括烧碱、糊树脂、93#汽油、轻柴油、丙烯等化工及石油炼化产品。",
        "country": "CN", "province": "辽宁", "city": "沈阳市",
        "founded_year": 1996, "employee_count": 1484,
        "company_type": "public", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 4. COMPANY NODE EXPOSURES
# ---------------------------------------------------------------------------

exposures = [
    # 中山公用
    {"exposure_id": "exp_zs_water", "company_id": "zhongshan_public", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中山公用 主营业务", "quote": "环保水务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zs_solid_waste", "company_id": "zhongshan_public", "node_id": "solid_waste_treatment", "activity_type": "operate", "role": "固废处理运营商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "中山公用 主营业务", "quote": "固废处理"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zs_tap_water", "company_id": "zhongshan_public", "node_id": "tap_water_supply", "activity_type": "operate", "role": "自来水供应运营商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "中山公用 主营业务", "quote": "环保水务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zs_port", "company_id": "zhongshan_public", "node_id": "port_passenger_service", "activity_type": "operate", "role": "港口客运服务商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "中山公用 主营业务", "quote": "港口客运"}], "status": "ACTIVE"},

    # 东北证券
    {"exposure_id": "exp_db_brokerage", "company_id": "northeast_securities", "node_id": "securities_brokerage", "activity_type": "operate", "role": "证券经纪服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券经纪业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_db_underwriting", "company_id": "northeast_securities", "node_id": "securities_underwriting", "activity_type": "operate", "role": "证券承销与保荐服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券承销与保荐业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_db_proprietary", "company_id": "northeast_securities", "node_id": "securities_proprietary_trading", "activity_type": "operate", "role": "证券自营投资商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券自营业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_db_asset_mgmt", "company_id": "northeast_securities", "node_id": "asset_management_service", "activity_type": "operate", "role": "资产管理服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "东北证券 主营业务", "quote": "证券资产管理业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_db_margin", "company_id": "northeast_securities", "node_id": "margin_trading_service", "activity_type": "operate", "role": "融资融券服务商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "东北证券 主营业务", "quote": "信用交易业务"}], "status": "ACTIVE"},

    # 国城矿业
    {"exposure_id": "exp_gc_lead_zinc_ore", "company_id": "guocheng_mining", "node_id": "lead_zinc_ore", "activity_type": "produce", "role": "铅锌矿石生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国城矿业 主营业务", "quote": "铅锌等有色金属的采选销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gc_lead_zinc_metal", "company_id": "guocheng_mining", "node_id": "lead_zinc_metal", "activity_type": "produce", "role": "铅锌金属生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国城矿业 主营业务", "quote": "铅锌等有色金属的采选销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gc_sulfuric", "company_id": "guocheng_mining", "node_id": "sulfuric_acid", "activity_type": "produce", "role": "硫酸生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "国城矿业 主营业务", "quote": "下游硫酸的生产销售"}], "status": "ACTIVE"},

    # 宝新能源
    {"exposure_id": "exp_bx_clean_coal", "company_id": "baoxin_energy", "node_id": "clean_coal_power_generation", "activity_type": "operate", "role": "洁净煤发电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "宝新能源 主营业务", "quote": "洁净煤燃烧技术发电"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bx_renewable", "company_id": "baoxin_energy", "node_id": "renewable_energy_power_generation", "activity_type": "operate", "role": "可再生能源发电运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "宝新能源 主营业务", "quote": "可再生能源发电"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bx_coal_power", "company_id": "baoxin_energy", "node_id": "coal_power_generation", "activity_type": "operate", "role": "燃煤发电运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "宝新能源 主营业务", "quote": "洁净煤燃烧技术发电和可再生能源发电"}], "status": "ACTIVE"},

    # *ST亚太
    {"exposure_id": "exp_yt_pharma_int", "company_id": "st_yatai", "node_id": "pharmaceutical_intermediate", "activity_type": "produce", "role": "医药中间体生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "医药中间体...的研发,生产和销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_yt_pesticide_int", "company_id": "st_yatai", "node_id": "pesticide_intermediate", "activity_type": "produce", "role": "农药中间体生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "*ST亚太 主营业务", "quote": "农药中间体的研发,生产和销售"}], "status": "ACTIVE"},

    # 惠天热电
    {"exposure_id": "exp_ht_heating", "company_id": "huitian_thermal", "node_id": "heating_supply", "activity_type": "operate", "role": "供热服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "惠天热电 主营业务", "quote": "为居民及非居民提供供热"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ht_heating_eng", "company_id": "huitian_thermal", "node_id": "heating_engineering_service", "activity_type": "operate", "role": "供暖工程服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "惠天热电 主营业务", "quote": "供暖工程服务"}], "status": "ACTIVE"},

    # 滨海能源
    {"exposure_id": "exp_bh_steam", "company_id": "binhai_energy", "node_id": "industrial_steam", "activity_type": "produce", "role": "工业蒸汽生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "滨海能源 主营业务", "quote": "蒸汽...的生产,供应"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bh_electricity", "company_id": "binhai_energy", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "滨海能源 主营业务", "quote": "电力...的生产,供应"}], "status": "ACTIVE"},
    {"exposure_id": "exp_bh_printing", "company_id": "binhai_energy", "node_id": "printing_service", "activity_type": "operate", "role": "印刷业务运营商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "滨海能源 主营业务", "quote": "印刷业务"}], "status": "ACTIVE"},

    # 宗申动力
    {"exposure_id": "exp_zs_engine", "company_id": "zongshen_power", "node_id": "motorcycle_engine", "activity_type": "manufacture", "role": "摩托车发动机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "宗申动力 主营业务", "quote": "主要产品:摩托车发动机及零配件"}], "status": "ACTIVE"},

    # 炼石航空
    {"exposure_id": "exp_ls_aerospace_part", "company_id": "lianshi_aviation", "node_id": "aerospace_precision_part", "activity_type": "manufacture", "role": "航空精密零部件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "炼石航空 主营业务", "quote": "主营产品:各种航空器相关精密零部件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ls_structural_part", "company_id": "lianshi_aviation", "node_id": "aircraft_structural_part", "activity_type": "manufacture", "role": "飞机结构件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "炼石航空 主营业务", "quote": "主营产品:...结构件等,包括飞机的机翼前缘表层"}], "status": "ACTIVE"},

    # ST沈化
    {"exposure_id": "exp_sh_caustic", "company_id": "st_shenhua", "node_id": "caustic_soda", "activity_type": "produce", "role": "烧碱生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:烧碱"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sh_paste_pvc", "company_id": "st_shenhua", "node_id": "paste_pvc_resin", "activity_type": "produce", "role": "糊树脂生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:糊树脂"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sh_gasoline", "company_id": "st_shenhua", "node_id": "gasoline", "activity_type": "produce", "role": "汽油生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:93#汽油"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sh_diesel", "company_id": "st_shenhua", "node_id": "diesel", "activity_type": "produce", "role": "柴油生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:轻柴油"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sh_propylene", "company_id": "st_shenhua", "node_id": "propylene", "activity_type": "produce", "role": "丙烯生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST沈化 主营业务", "quote": "主要产品:丙烯"}], "status": "ACTIVE"}
]

# ---------------------------------------------------------------------------
# 5. SUBMIT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph_batch = {
        "batch_id": "batch_022_graph",
        "task_description": "Batch 022: Industrial nodes and edges for 10 companies (000685-000698). Focus on port passenger, securities, clean coal, pharma/pesticide intermediates, heating, industrial steam, motorcycle engines, aerospace parts, and petrochemicals.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }

    business_batch = {
        "batch_id": "batch_022_business",
        "task_description": "Batch 022: Company registrations and node exposures for 10 companies (000685-000698).",
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
