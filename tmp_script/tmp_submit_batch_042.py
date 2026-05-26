#!/usr/bin/env python3
"""Batch 042: 000993-600006"""
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
    "batch_id": "batch_042_graph",
    "task_description": "Batch 042 graph: payment terminal, vitamin, newspaper publishing, banking service.",
    "nodes_to_upsert": [
        {"node_id": "payment_terminal", "canonical_name_zh": "支付终端", "canonical_name_en": "Payment Terminal", "aliases": ["POS机", "支付设备"], "definition": "用于商户收单、银行卡刷卡、扫码支付的电子终端设备。", "entity_type": "device", "evidence": [{"source_title": "新大陆主营业务", "quote": "经营业务主要为商户支付服务行业和信息识别行业提供终端产品、系统解决方案"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "vitamin", "canonical_name_zh": "维生素", "canonical_name_en": "Vitamin", "aliases": ["维他命", "VIT"], "definition": "一类维持人体正常生理功能所必需的微量有机化合物，广泛用于医药、食品和饲料添加剂。", "entity_type": "material", "evidence": [{"source_title": "新和成主营业务", "quote": "主要经营维生素、香精香料、医药中间体系列产品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "newspaper_publishing", "canonical_name_zh": "报纸出版", "canonical_name_en": "Newspaper Publishing", "aliases": ["报刊出版"], "definition": "以报纸、期刊为载体的信息采集、编辑、印刷及发行业务。", "entity_type": "service", "evidence": [{"source_title": "粤传媒主营业务", "quote": "经营业务:报纸出版经营、印刷、报刊发行等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "banking_service", "canonical_name_zh": "银行服务", "canonical_name_en": "Banking Service", "aliases": ["金融服务", "存贷业务"], "definition": "银行机构提供的存款、贷款、结算、票据承兑与贴现等金融服务。", "entity_type": "service", "evidence": [{"source_title": "浦发银行主营业务", "quote": "经营业务:吸收公众存款;发放短期、中期和长期贷款;办理结算;办理票据贴现"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_042_business",
    "task_description": "Batch 042 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "mindong_power", "name_zh": "福建闽东电力股份有限公司", "aliases": ["闽东电力"], "stock_codes": ["000993.SZ"], "description": "水电开发与运营企业", "country": "CN", "province": "福建", "city": "宁德", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "huangtai", "name_zh": "甘肃皇台酒业股份有限公司", "aliases": ["皇台酒业"], "stock_codes": ["000995.SZ"], "description": "白酒及葡萄酒生产企业", "country": "CN", "province": "甘肃", "city": "武威", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "newland", "name_zh": "新大陆数字技术股份有限公司", "aliases": ["新大陆"], "stock_codes": ["000997.SZ"], "description": "支付终端、信息识别及移动通信设备企业", "country": "CN", "province": "福建", "city": "福州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "longping", "name_zh": "袁隆平农业高科技股份有限公司", "aliases": ["隆平高科"], "stock_codes": ["000998.SZ"], "description": "杂交水稻、蔬菜种子及农产品企业", "country": "CN", "province": "湖南", "city": "长沙", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "china_resources_sanjiu", "name_zh": "华润三九医药股份有限公司", "aliases": ["华润三九"], "stock_codes": ["000999.SZ"], "description": "药品、保健品及医疗器械企业", "country": "CN", "province": "广东", "city": "深圳", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "xinhecheng", "name_zh": "浙江新和成股份有限公司", "aliases": ["新和成"], "stock_codes": ["002001.SZ"], "description": "维生素、香精香料及医药中间体生产企业", "country": "CN", "province": "浙江", "city": "绍兴", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "yue_media", "name_zh": "广东广州日报传媒股份有限公司", "aliases": ["粤传媒"], "stock_codes": ["002181.SZ"], "description": "报纸出版、印刷及报刊发行企业", "country": "CN", "province": "广东", "city": "广州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "spdb", "name_zh": "上海浦东发展银行股份有限公司", "aliases": ["浦发银行"], "stock_codes": ["600000.SH"], "description": "商业银行", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "baiyun_airport", "name_zh": "广州白云国际机场股份有限公司", "aliases": ["白云机场"], "stock_codes": ["600004.SH"], "description": "机场运营及航空地面服务企业", "country": "CN", "province": "广东", "city": "广州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "dongfeng_auto", "name_zh": "东风汽车股份有限公司", "aliases": ["东风股份"], "stock_codes": ["600006.SH"], "description": "东风系列轻型商用车及东风康明斯发动机企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "mindong_operate_hydro", "company_id": "mindong_power", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "闽东电力主营业务", "quote": "主要业务:水电开发与运营"}]},
        {"exposure_id": "huangtai_produce_liquor", "company_id": "huangtai", "node_id": "liquor", "activity_type": "produce", "role": "白酒生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "皇台酒业主营业务", "quote": "主要产品:白酒、葡萄酒"}]},
        {"exposure_id": "newland_manufacture_payment", "company_id": "newland", "node_id": "payment_terminal", "activity_type": "manufacture", "role": "支付终端制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "新大陆主营业务", "quote": "经营业务主要为商户支付服务行业和信息识别行业提供终端产品"}]},
        {"exposure_id": "longping_produce_rice_seed", "company_id": "longping", "node_id": "rice_seed", "activity_type": "produce", "role": "杂交水稻种子生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "隆平高业主营业务", "quote": "主要产品:杂交水稻、蔬菜种子、农产品、棉花、鲜花"}]},
        {"exposure_id": "sanjiu_produce_chinese_patent", "company_id": "china_resources_sanjiu", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药及保健品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华润三九主营业务", "quote": "主要业务:药品、保健品、医疗器械的批发和零售"}]},
        {"exposure_id": "xinhecheng_produce_vitamin", "company_id": "xinhecheng", "node_id": "vitamin", "activity_type": "produce", "role": "维生素生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "新和成主营业务", "quote": "主要经营维生素、香精香料、医药中间体系列产品"}]},
        {"exposure_id": "yue_media_operate_publishing", "company_id": "yue_media", "node_id": "newspaper_publishing", "activity_type": "operate", "role": "报纸出版运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "粤传媒主营业务", "quote": "经营业务:报纸出版经营、印刷、报刊发行等"}]},
        {"exposure_id": "spdb_provide_banking", "company_id": "spdb", "node_id": "banking_service", "activity_type": "provide_service", "role": "商业银行", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "浦发银行业务", "quote": "经营业务:吸收公众存款;发放短期、中期和长期贷款;办理结算"}]},
        {"exposure_id": "baiyun_operate_airport", "company_id": "baiyun_airport", "node_id": "airport_operation_service", "activity_type": "operate", "role": "机场运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "白云机场主营业务", "quote": "主要业务:以航空器、旅客和货物、邮件为服务对象"}]},
        {"exposure_id": "dongfeng_manufacture_vehicle", "company_id": "dongfeng_auto", "node_id": "automotive_part", "activity_type": "manufacture", "role": "轻型商用车及发动机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东风股份主营业务", "quote": "主要产品:东风系列轻型商用车、东风康明斯发动机"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 042 done!")
