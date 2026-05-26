#!/usr/bin/env python3
"""Batch 044: 600021-600037"""
import json, urllib.request, urllib.error
API_BASE = "http://localhost:8005/api/v1"

def api_post(path, data):
    url = f"{API_BASE}{path}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code} on {path}: {e.read().decode()[:500]}")
        raise

graph_batch = {
    "batch_id": "batch_044_graph",
    "task_description": "Batch 044 graph: oil tanker, lubricant, concrete machinery, road paver, securities service.",
    "nodes_to_upsert": [
        {"node_id": "oil_tanker", "canonical_name_zh": "油轮", "canonical_name_en": "Oil Tanker", "aliases": ["油船", "原油运输船"], "definition": "专门用于运输石油及石油制品的大型船舶。", "entity_type": "device", "evidence": [{"source_title": "中远海能主营业务", "quote": "主要业务:石油运输、煤炭运输"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "lubricant", "canonical_name_zh": "润滑油", "canonical_name_en": "Lubricant", "aliases": ["机油", "润滑脂"], "definition": "用于减少机械摩擦、冷却和防锈的石油基或合成基液体。", "entity_type": "material", "evidence": [{"source_title": "中国石化主营业务", "quote": "主要产品:原油、天然气、汽油、柴油、煤油、润滑油、合成树脂、合成纤维"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "concrete_machinery", "canonical_name_zh": "混凝土机械", "canonical_name_en": "Concrete Machinery", "aliases": ["混凝土泵车", "搅拌站"], "definition": "用于混凝土搅拌、输送、浇筑及泵送的工程机械。", "entity_type": "device", "evidence": [{"source_title": "三一重工主营业务", "quote": "主要业务:混凝土机械、挖掘机械、液压压路机、摊铺机等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "road_paver", "canonical_name_zh": "摊铺机", "canonical_name_en": "Road Paver", "aliases": ["沥青摊铺机"], "definition": "用于沥青或混凝土路面摊铺作业的工程机械。", "entity_type": "device", "evidence": [{"source_title": "三一重工主营业务", "quote": "主要业务:混凝土机械、挖掘机械、液压压路机、摊铺机等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "securities_service", "canonical_name_zh": "证券服务", "canonical_name_en": "Securities Service", "aliases": ["投行服务", "券商业务"], "definition": "证券公司提供的投资银行、经纪、资产管理及研究咨询等金融服务。", "entity_type": "service", "evidence": [{"source_title": "中信证券主营业务", "quote": "投资银行业务、债券承销结构融资业务、经纪业务、资管业务"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "crude_oil_to_gasoline", "from_node": "crude_oil", "to_node": "gasoline", "edge_type": "material_flow", "description": "原油经过炼制加工生产出汽油产品。", "evidence": [{"source_title": "中国石化主营业务", "quote": "主要产品:原油、天然气、汽油、柴油、煤油、润滑油、合成树脂、合成纤维"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_044_business",
    "task_description": "Batch 044 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "shanghai_electric_power", "name_zh": "上海电力股份有限公司", "aliases": ["上海电力"], "stock_codes": ["600021.SH"], "description": "电力、热力及燃气分布式能源企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "cosco_shipping_energy", "name_zh": "中远海运能源运输股份有限公司", "aliases": ["中远海能"], "stock_codes": ["600026.SH"], "description": "石油运输及煤炭运输企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sinopec", "name_zh": "中国石油化工股份有限公司", "aliases": ["中国石化"], "stock_codes": ["600028.SH"], "description": "原油、成品油、天然气及化工产品生产销售企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "china_southern_airlines", "name_zh": "中国南方航空股份有限公司", "aliases": ["南方航空"], "stock_codes": ["600029.SH"], "description": "航空客货运输及通用航空服务企业", "country": "CN", "province": "广东", "city": "广州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "citic_securities", "name_zh": "中信证券股份有限公司", "aliases": ["中信证券"], "stock_codes": ["600030.SH"], "description": "投资银行、证券经纪、资产管理及研究咨询企业", "country": "CN", "province": "广东", "city": "深圳", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sany_heavy", "name_zh": "三一重工股份有限公司", "aliases": ["三一重工"], "stock_codes": ["600031.SH"], "description": "混凝土机械、挖掘机械、液压压路机及摊铺机等工程机械企业", "country": "CN", "province": "湖南", "city": "长沙", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "fujian_highway", "name_zh": "福建发展高速公路股份有限公司", "aliases": ["福建高速"], "stock_codes": ["600033.SH"], "description": "高速公路收费及道路投资经营企业", "country": "CN", "province": "福建", "city": "福州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "chutian_highway", "name_zh": "湖北楚天智能交通股份有限公司", "aliases": ["楚天高速"], "stock_codes": ["600035.SH"], "description": "高速公路运营及交通服务企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "cmb", "name_zh": "招商银行股份有限公司", "aliases": ["招商银行"], "stock_codes": ["600036.SH"], "description": "商业银行", "country": "CN", "province": "广东", "city": "深圳", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "gehua", "name_zh": "北京歌华有线电视网络股份有限公司", "aliases": ["歌华有线"], "stock_codes": ["600037.SH"], "description": "有线电视网络运营企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "shanghai_power_operate_coal", "company_id": "shanghai_electric_power", "node_id": "coal_power_generation", "activity_type": "operate", "role": "火电及分布式能源运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "上海电力主营业务", "quote": "主要业务:电力、热力、燃气分布式"}]},
        {"exposure_id": "cosco_operate_tanker", "company_id": "cosco_shipping_energy", "node_id": "oil_tanker", "activity_type": "operate", "role": "油轮运输运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中远海能主营业务", "quote": "主要业务:石油运输、煤炭运输"}]},
        {"exposure_id": "sinopec_produce_gasoline", "company_id": "sinopec", "node_id": "gasoline", "activity_type": "produce", "role": "汽油生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中国石化主营业务", "quote": "主要产品:原油、天然气、汽油、柴油、煤油、润滑油、合成树脂、合成纤维"}]},
        {"exposure_id": "sinopec_produce_lubricant", "company_id": "sinopec", "node_id": "lubricant", "activity_type": "produce", "role": "润滑油生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中国石化主营业务", "quote": "主要产品:原油、天然气、汽油、柴油、煤油、润滑油、合成树脂、合成纤维"}]},
        {"exposure_id": "sinopec_produce_synthetic_resin", "company_id": "sinopec", "node_id": "synthetic_resin", "activity_type": "produce", "role": "合成树脂生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "中国石化主营业务", "quote": "主要产品:原油、天然气、汽油、柴油、煤油、润滑油、合成树脂、合成纤维"}]},
        {"exposure_id": "southern_operate_airline", "company_id": "china_southern_airlines", "node_id": "air_transport_service", "activity_type": "operate", "role": "航空运输运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "南方航空主营业务", "quote": "主要业务:提供国内、国际和地区的客货及邮件运输服务"}]},
        {"exposure_id": "citic_provide_securities", "company_id": "citic_securities", "node_id": "securities_service", "activity_type": "provide_service", "role": "综合证券服务商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中信证券主营业务", "quote": "投资银行业务、债券承销结构融资业务、经纪业务、资管业务"}]},
        {"exposure_id": "sany_manufacture_concrete", "company_id": "sany_heavy", "node_id": "concrete_machinery", "activity_type": "manufacture", "role": "混凝土机械制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "三一重工主营业务", "quote": "主要业务:混凝土机械、挖掘机械、液压压路机、摊铺机等"}]},
        {"exposure_id": "sany_manufacture_excavator", "company_id": "sany_heavy", "node_id": "excavator", "activity_type": "manufacture", "role": "挖掘机械制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "三一重工主营业务", "quote": "主要业务:混凝土机械、挖掘机械、液压压路机、摊铺机等"}]},
        {"exposure_id": "sany_manufacture_paver", "company_id": "sany_heavy", "node_id": "road_paver", "activity_type": "manufacture", "role": "摊铺机制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "三一重工主营业务", "quote": "主要业务:混凝土机械、挖掘机械、液压压路机、摊铺机等"}]},
        {"exposure_id": "fujian_operate_highway", "company_id": "fujian_highway", "node_id": "highway_operation_service", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "福建高速主营业务", "quote": "主要业务:经营所辖路段的高速公路通行费收入"}]},
        {"exposure_id": "chutian_operate_highway", "company_id": "chutian_highway", "node_id": "highway_operation_service", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "楚天高速主营业务", "quote": "主要业务:武汉至宜昌段高速公路车辆通行费"}]},
        {"exposure_id": "cmb_provide_banking", "company_id": "cmb", "node_id": "banking_service", "activity_type": "provide_service", "role": "商业银行", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "招商银行业务", "quote": "主要业务:存款、贷款、票据贴现、同业拆借"}]},
        {"exposure_id": "gehua_operate_cable_tv", "company_id": "gehua", "node_id": "cable_tv_network_service", "activity_type": "operate", "role": "有线电视网络运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "歌华有线主营业务", "quote": "主要业务:有线电视网络"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 044 done!")
