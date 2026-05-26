#!/usr/bin/env python3
"""Batch 043: 600007-600020"""
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
    "batch_id": "batch_043_graph",
    "task_description": "Batch 043 graph: office building, rare earth steel, waste incineration.",
    "nodes_to_upsert": [
        {"node_id": "office_building", "canonical_name_zh": "写字楼", "canonical_name_en": "Office Building", "aliases": ["办公楼", "商务楼宇"], "definition": "用于企业办公经营活动的高层商业建筑物业。", "entity_type": "infrastructure", "evidence": [{"source_title": "中国国贸主营业务", "quote": "主要业务:高级写字楼、高级公寓、商场等物业出租及经营"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "rare_earth_steel", "canonical_name_zh": "稀土钢", "canonical_name_en": "Rare Earth Steel", "aliases": ["稀土处理钢"], "definition": "在炼钢过程中加入稀土元素以改善性能的特殊钢材，具有优异的韧性和耐磨性。", "entity_type": "material", "evidence": [{"source_title": "包钢股份主营业务", "quote": "主要产品:稀土钢产品和板材产品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "waste_incineration", "canonical_name_zh": "垃圾焚烧", "canonical_name_en": "Waste Incineration", "aliases": ["固废焚烧", "垃圾焚烧发电"], "definition": "通过高温焚烧处理城市固体废弃物并回收热能用于发电的环保技术。", "entity_type": "service", "evidence": [{"source_title": "首创环保主营业务", "quote": "供水、污水处理、固废处理、大气治理、餐厨及污泥处理"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "rare_earth_to_steel", "from_node": "rare_earth_steel", "to_node": "steel_plate", "edge_type": "material_flow", "description": "稀土钢是钢材的一种特殊品种，用于高端制造业。", "evidence": [{"source_title": "包钢股份主营业务", "quote": "主要产品:稀土钢产品和板材产品"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_043_business",
    "task_description": "Batch 043 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "china_world", "name_zh": "中国国际贸易中心股份有限公司", "aliases": ["中国国贸"], "stock_codes": ["600007.SH"], "description": "高级写字楼、公寓、商场及展览设施经营企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "capital_env", "name_zh": "北京首创生态环保集团股份有限公司", "aliases": ["首创环保"], "stock_codes": ["600008.SH"], "description": "自来水、污水处理、固废处理及大气治理企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "shanghai_airport", "name_zh": "上海国际机场股份有限公司", "aliases": ["上海机场"], "stock_codes": ["600009.SH"], "description": "机场航空业务及航空地面服务企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "baotou_steel", "name_zh": "内蒙古包钢钢联股份有限公司", "aliases": ["包钢股份"], "stock_codes": ["600010.SH"], "description": "稀土钢产品及板材产品生产企业", "country": "CN", "province": "内蒙古", "city": "包头", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "huaneng_power", "name_zh": "华能国际电力股份有限公司", "aliases": ["华能国际"], "stock_codes": ["600011.SH"], "description": "电力生产及销售企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "wantong_highway", "name_zh": "安徽皖通高速公路股份有限公司", "aliases": ["皖通高速"], "stock_codes": ["600012.SH"], "description": "高速公路运营及投资企业", "country": "CN", "province": "安徽", "city": "合肥", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "huaxia_bank", "name_zh": "华夏银行股份有限公司", "aliases": ["华夏银行"], "stock_codes": ["600015.SH"], "description": "商业银行", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "minsheng_bank", "name_zh": "中国民生银行股份有限公司", "aliases": ["民生银行"], "stock_codes": ["600016.SH"], "description": "商业银行", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "baosteel", "name_zh": "宝山钢铁股份有限公司", "aliases": ["宝钢股份"], "stock_codes": ["600019.SH"], "description": "碳钢、不锈钢、特钢等综合钢铁企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "zhongyuan_highway", "name_zh": "河南中原高速公路股份有限公司", "aliases": ["中原高速"], "stock_codes": ["600020.SH"], "description": "高速公路运营企业", "country": "CN", "province": "河南", "city": "郑州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "china_world_operate_office", "company_id": "china_world", "node_id": "office_building", "activity_type": "operate", "role": "写字楼物业运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中国国贸主营业务", "quote": "主要业务:高级写字楼、高级公寓、商场等物业出租及经营"}]},
        {"exposure_id": "capital_operate_water", "company_id": "capital_env", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "首创环保主营业务", "quote": "供水、污水处理、固废处理、大气治理"}]},
        {"exposure_id": "capital_operate_waste", "company_id": "capital_env", "node_id": "waste_incineration", "activity_type": "operate", "role": "固废处理运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "首创环保主营业务", "quote": "供水、污水处理、固废处理、大气治理、餐厨及污泥处理"}]},
        {"exposure_id": "shanghai_operate_airport", "company_id": "shanghai_airport", "node_id": "airport_operation_service", "activity_type": "operate", "role": "机场运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "上海机场主营业务", "quote": "经营业务:机场航空业务、航站楼商业业务、航空物流业务"}]},
        {"exposure_id": "baotou_produce_rare_earth_steel", "company_id": "baotou_steel", "node_id": "rare_earth_steel", "activity_type": "produce", "role": "稀土钢生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "包钢股份主营业务", "quote": "主要产品:稀土钢产品和板材产品"}]},
        {"exposure_id": "baotou_produce_steel_plate", "company_id": "baotou_steel", "node_id": "steel_plate", "activity_type": "produce", "role": "板材生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "包钢股份主营业务", "quote": "主要产品:稀土钢产品和板材产品"}]},
        {"exposure_id": "huaneng_operate_coal_power", "company_id": "huaneng_power", "node_id": "coal_power_generation", "activity_type": "operate", "role": "火电运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "华能国际主营业务", "quote": "主要产品:电力"}]},
        {"exposure_id": "wantong_operate_highway", "company_id": "wantong_highway", "node_id": "highway_operation_service", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "皖通高速主营业务", "quote": "收费公路之运营和广告业务"}]},
        {"exposure_id": "huaxia_provide_banking", "company_id": "huaxia_bank", "node_id": "banking_service", "activity_type": "provide_service", "role": "商业银行", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "华夏银行业务", "quote": "主要业务:存款、贷款、银票承兑与贴现、同业拆借"}]},
        {"exposure_id": "minsheng_provide_banking", "company_id": "minsheng_bank", "node_id": "banking_service", "activity_type": "provide_service", "role": "商业银行", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "民生银行业务", "quote": "主要业务:存款(不含财政)、贷款、票据贴现、同业拆借"}]},
        {"exposure_id": "baosteel_produce_steel", "company_id": "baosteel", "node_id": "steel_plate", "activity_type": "produce", "role": "综合钢铁生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "宝钢股份主营业务", "quote": "主要产品:碳钢产品、不锈钢、特钢、钢管材和高线"}]},
        {"exposure_id": "zhongyuan_operate_highway", "company_id": "zhongyuan_highway", "node_id": "highway_operation_service", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中原高速主营业务", "quote": "经营业务:郑州至漯河高速公路、郑州黄河公路大桥"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 043 done!")
