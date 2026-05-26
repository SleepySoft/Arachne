#!/usr/bin/env python3
"""Batch 045: 600038-600057"""
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
    "batch_id": "batch_045_graph",
    "task_description": "Batch 045 graph: helicopter, bridge construction, telecom service, x-ray, MRI.",
    "nodes_to_upsert": [
        {"node_id": "helicopter", "canonical_name_zh": "直升机", "canonical_name_en": "Helicopter", "aliases": ["直升飞机", "旋翼机"], "definition": "以旋翼为主要升力面和操纵面的航空器，可垂直起降、悬停及向任意方向飞行。", "entity_type": "device", "evidence": [{"source_title": "中直股份主营业务", "quote": "主要业务:直升机、Y12系列多用途飞机、EC120直升机等航空产品研制生产"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "bridge_construction", "canonical_name_zh": "桥梁施工", "canonical_name_en": "Bridge Construction", "aliases": ["桥梁工程", "路桥施工"], "definition": "各类桥梁的结构设计、基础施工、上部结构架设及桥面铺装等工程建设服务。", "entity_type": "service", "evidence": [{"source_title": "四川路桥主营业务", "quote": "主要业务:桥梁施工、道路施工、交通设施、房屋建筑"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "telecom_service", "canonical_name_zh": "电信服务", "canonical_name_en": "Telecommunications Service", "aliases": ["通信服务", "移动网络服务"], "definition": "通过有线或无线网络提供语音、数据及互联网接入等通信服务。", "entity_type": "service", "evidence": [{"source_title": "中国联通主营业务", "quote": "主要业务:电信业务投资"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "x_ray_equipment", "canonical_name_zh": "X射线诊断设备", "canonical_name_en": "X-ray Diagnostic Equipment", "aliases": ["X光机", "医用X射线机"], "definition": "利用X射线穿透人体成像原理进行医学诊断的放射影像设备。", "entity_type": "device", "evidence": [{"source_title": "万东医疗主营业务", "quote": "主要产品为医用X射线诊断设备、磁共振成像设备"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "mri_equipment", "canonical_name_zh": "磁共振成像设备", "canonical_name_en": "MRI Equipment", "aliases": ["MRI", "核磁共振设备"], "definition": "利用强磁场和射频脉冲使人体组织产生共振信号并重建图像的医学影像设备。", "entity_type": "device", "evidence": [{"source_title": "万东医疗主营业务", "quote": "主要产品为医用X射线诊断设备、磁共振成像设备"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_045_business",
    "task_description": "Batch 045 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "avic_helicopter", "name_zh": "中航直升机股份有限公司", "aliases": ["中直股份"], "stock_codes": ["600038.SH"], "description": "直升机及航空产品研制生产企业", "country": "CN", "province": "黑龙江", "city": "哈尔滨", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sichuan_road_bridge", "name_zh": "四川路桥建设集团股份有限公司", "aliases": ["四川路桥"], "stock_codes": ["600039.SH"], "description": "桥梁施工、道路施工及交通设施建设企业", "country": "CN", "province": "四川", "city": "成都", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "china_unicom", "name_zh": "中国联合网络通信股份有限公司", "aliases": ["中国联通"], "stock_codes": ["600050.SH"], "description": "综合电信运营企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "ningbo_union", "name_zh": "宁波联合集团股份有限公司", "aliases": ["宁波联合"], "stock_codes": ["600051.SH"], "description": "贸易、电力热力供应、房地产及旅游综合企业", "country": "CN", "province": "浙江", "city": "宁波", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "dongwang_era", "name_zh": "浙江东望时代科技股份有限公司", "aliases": ["东望时代"], "stock_codes": ["600052.SH"], "description": "房地产开发、影视投资及广告企业", "country": "CN", "province": "浙江", "city": "杭州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_jiuyou", "name_zh": "深圳九有股份有限公司", "aliases": ["*ST九有"], "stock_codes": ["600053.SH"], "description": "房地产开发与经营企业", "country": "CN", "province": "广东", "city": "深圳", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "huangshan_tourism", "name_zh": "黄山旅游发展股份有限公司", "aliases": ["黄山旅游"], "stock_codes": ["600054.SH"], "description": "旅游接待、园林门票、酒店餐饮及旅游服务企业", "country": "CN", "province": "安徽", "city": "黄山", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "wandong_medical", "name_zh": "万东医疗科技股份有限公司", "aliases": ["万东医疗"], "stock_codes": ["600055.SH"], "description": "医用X射线诊断设备及磁共振成像设备企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sinopharm", "name_zh": "中国医药健康产业股份有限公司", "aliases": ["中国医药"], "stock_codes": ["600056.SH"], "description": "国际贸易、招标代理、医疗器材及药品企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "xmxy", "name_zh": "厦门象屿股份有限公司", "aliases": ["厦门象屿"], "stock_codes": ["600057.SH"], "description": "物流商品贸易及采购供应管理综合企业", "country": "CN", "province": "福建", "city": "厦门", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "avic_manufacture_helicopter", "company_id": "avic_helicopter", "node_id": "helicopter", "activity_type": "manufacture", "role": "直升机制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中直股份主营业务", "quote": "主要业务:直升机、Y12系列多用途飞机、EC120直升机等航空产品研制生产"}]},
        {"exposure_id": "sichuan_provide_bridge", "company_id": "sichuan_road_bridge", "node_id": "bridge_construction", "activity_type": "provide_service", "role": "桥梁施工服务商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "四川路桥主营业务", "quote": "主要业务:桥梁施工、道路施工、交通设施、房屋建筑"}]},
        {"exposure_id": "unicom_provide_telecom", "company_id": "china_unicom", "node_id": "telecom_service", "activity_type": "provide_service", "role": "电信运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中国联通主营业务", "quote": "主要业务:电信业务投资"}]},
        {"exposure_id": "ningbo_operate_real_estate", "company_id": "ningbo_union", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "宁波联合主营业务", "quote": "经营业务:贸易、电力热力供应和供应业、房地产业、旅游业"}]},
        {"exposure_id": "dongwang_operate_film", "company_id": "dongwang_era", "node_id": "film_television", "activity_type": "operate", "role": "影视投资运营商", "weight": 0.7, "confidence": "MEDIUM", "evidence": [{"source_title": "东望时代主营业务", "quote": "主要业务:房地产开发、影视投资、广告"}]},
        {"exposure_id": "jiuyou_operate_real_estate", "company_id": "st_jiuyou", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "ST九有主营业务", "quote": "经营业务为房地产开发与经营"}]},
        {"exposure_id": "huangshan_operate_tourism", "company_id": "huangshan_tourism", "node_id": "tourism_service", "activity_type": "operate", "role": "旅游服务运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "黄山旅游主营业务", "quote": "经营业务:旅游接待、园林门票、酒店餐饮及旅游服务"}]},
        {"exposure_id": "wandong_manufacture_xray", "company_id": "wandong_medical", "node_id": "x_ray_equipment", "activity_type": "manufacture", "role": "X射线诊断设备制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "万东医疗主营业务", "quote": "主要产品为医用X射线诊断设备、磁共振成像设备"}]},
        {"exposure_id": "wandong_manufacture_mri", "company_id": "wandong_medical", "node_id": "mri_equipment", "activity_type": "manufacture", "role": "磁共振成像设备制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "万东医疗主营业务", "quote": "主要产品为医用X射线诊断设备、磁共振成像设备"}]},
        {"exposure_id": "sinopharm_provide_pharma_distribution", "company_id": "sinopharm", "node_id": "pharmaceutical_distribution", "activity_type": "provide_service", "role": "医药及医疗器械流通商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中国医药主营业务", "quote": "主要业务:国际贸易、招标代理、医疗器材、药品"}]},
        {"exposure_id": "xmxy_provide_logistics", "company_id": "xmxy", "node_id": "logistics_service", "activity_type": "provide_service", "role": "供应链及物流服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "厦门象屿主营业务", "quote": "经营业务:物流商品贸易、采购供应管理等综合管理服务"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 045 done!")
