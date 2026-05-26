#!/usr/bin/env python3
"""Batch 048: 600085-600100"""
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
    "batch_id": "batch_048_graph",
    "task_description": "Batch 048 graph: film production, power cable, aquatic product, general engine.",
    "nodes_to_upsert": [
        {"node_id": "film_production", "canonical_name_zh": "影视制作", "canonical_name_en": "Film Production", "aliases": ["影视拍摄", "电视剧制作"], "definition": "以电影、电视剧、纪录片为载体的创意内容策划、拍摄、后期制作及发行业务。", "entity_type": "service", "evidence": [{"source_title": "中视传媒主营业务", "quote": "主要业务:影视拍摄、电视剧节目制作、销售经营、影视设备租赁"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "power_cable", "canonical_name_zh": "电力电缆", "canonical_name_en": "Power Cable", "aliases": ["电线电缆", "输电线缆"], "definition": "用于输送和分配电能的绝缘导线，包括高压、中压和低压电缆。", "entity_type": "component", "evidence": [{"source_title": "特变电工主营业务", "quote": "主要业务:变压器、电线电缆及其辅助设备的制造与销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "aquatic_product", "canonical_name_zh": "水产品", "canonical_name_en": "Aquatic Product", "aliases": ["海鲜", "水产加工品"], "definition": "通过海淡水养殖或捕捞获得并经加工处理的鱼、虾、贝类等食用产品。", "entity_type": "material", "evidence": [{"source_title": "开创国际主营业务", "quote": "主营业务:海淡水养殖、水产品加工和贸易"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "general_engine", "canonical_name_zh": "通用发动机", "canonical_name_en": "General Purpose Engine", "aliases": ["通用汽油机", "小型发动机"], "definition": "可为多种机械设备提供动力的小型内燃机，广泛应用于农林机械、工程机械及发电机组。", "entity_type": "device", "evidence": [{"source_title": "林海股份主营业务", "quote": "主要产品:通用发动机及其配套的特种车辆、汽油机、摩托车及全地形车、林机"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "transformer_to_power_cable", "from_node": "transformer", "to_node": "power_cable", "edge_type": "composition", "description": "变压器与电力电缆共同构成输配电系统的关键设备组合。", "evidence": [{"source_title": "特变电工主营业务", "quote": "主要业务:变压器、电线电缆及其辅助设备的制造与销售"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_048_business",
    "task_description": "Batch 048 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "tongrentang", "name_zh": "北京同仁堂股份有限公司", "aliases": ["同仁堂"], "stock_codes": ["600085.SH"], "description": "乌鸡白凤丸、六味地黄丸等中成药生产企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "cctv_media", "name_zh": "中视传媒股份有限公司", "aliases": ["中视传媒"], "stock_codes": ["600088.SH"], "description": "影视拍摄、电视剧制作及广告企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "tebian_electric", "name_zh": "特变电工股份有限公司", "aliases": ["特变电工"], "stock_codes": ["600089.SH"], "description": "变压器、电线电缆及其辅助设备制造企业", "country": "CN", "province": "新疆", "city": "昌吉", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "damingcheng", "name_zh": "上海大名城企业股份有限公司", "aliases": ["大名城"], "stock_codes": ["600094.SH"], "description": "房地产综合开发及物业管理企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "xiangcai", "name_zh": "湘财股份有限公司", "aliases": ["湘财股份"], "stock_codes": ["600095.SH"], "description": "证券经纪、投资银行及资产管理企业", "country": "CN", "province": "湖南", "city": "长沙", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "ytc_fertilizer", "name_zh": "云南云天化股份有限公司", "aliases": ["云天化"], "stock_codes": ["600096.SH"], "description": "化肥、有机化工、新材料及磷矿采选企业", "country": "CN", "province": "云南", "city": "昆明", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "kaichuang", "name_zh": "上海开创国际海洋资源股份有限公司", "aliases": ["开创国际"], "stock_codes": ["600097.SH"], "description": "海淡水养殖及水产品加工贸易企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "guangzhou_dev", "name_zh": "广州发展集团股份有限公司", "aliases": ["广州发展"], "stock_codes": ["600098.SH"], "description": "电力、能源物流及基础设施企业", "country": "CN", "province": "广东", "city": "广州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "linhai", "name_zh": "林海股份有限公司", "aliases": ["林海股份"], "stock_codes": ["600099.SH"], "description": "通用发动机、特种车辆、摩托车及全地形车企业", "country": "CN", "province": "江苏", "city": "泰州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "tongfang", "name_zh": "同方股份有限公司", "aliases": ["同方股份"], "stock_codes": ["600100.SH"], "description": "计算机、电视机、安防安检及节能照明等IT设备企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "tongrentang_produce_chinese_patent", "company_id": "tongrentang", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "同仁堂主营业务", "quote": "主要产品:乌鸡白凤丸系列、六味地黄丸系列"}]},
        {"exposure_id": "cctv_produce_film", "company_id": "cctv_media", "node_id": "film_production", "activity_type": "produce", "role": "影视制作服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中视传媒主营业务", "quote": "主要业务:影视拍摄、电视剧节目制作、销售经营"}]},
        {"exposure_id": "tebian_manufacture_transformer", "company_id": "tebian_electric", "node_id": "transformer", "activity_type": "manufacture", "role": "变压器制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "特变电工主营业务", "quote": "主要业务:变压器、电线电缆及其辅助设备的制造与销售"}]},
        {"exposure_id": "tebian_manufacture_power_cable", "company_id": "tebian_electric", "node_id": "power_cable", "activity_type": "manufacture", "role": "电力电缆制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "特变电工主营业务", "quote": "主要业务:变压器、电线电缆及其辅助设备的制造与销售"}]},
        {"exposure_id": "damingcheng_operate_real_estate", "company_id": "damingcheng", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "大名城主营业务", "quote": "主营业务主要为:房地产综合开发、建造、销售商品房"}]},
        {"exposure_id": "xiangcai_provide_securities", "company_id": "xiangcai", "node_id": "securities_service", "activity_type": "provide_service", "role": "综合证券服务商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "湘财股份主营业务", "quote": "主要产品:证券经纪、投资银行、证券投资、资产管理"}]},
        {"exposure_id": "ytc_produce_chemical_fertilizer", "company_id": "ytc_fertilizer", "node_id": "chemical_fertilizer", "activity_type": "produce", "role": "化肥生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "云天化主营业务", "quote": "主要产品:化肥、有机化工、新材料、磷矿采选等"}]},
        {"exposure_id": "kaichuang_produce_aquatic", "company_id": "kaichuang", "node_id": "aquatic_product", "activity_type": "produce", "role": "水产品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "开创国际主营业务", "quote": "主营业务:海淡水养殖、水产品加工和贸易"}]},
        {"exposure_id": "guangzhou_operate_power", "company_id": "guangzhou_dev", "node_id": "coal_power_generation", "activity_type": "operate", "role": "火电及能源物流运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "广州发展主营业务", "quote": "主要业务:电力产业、能源物流产业、基础设施产业"}]},
        {"exposure_id": "linhai_manufacture_engine", "company_id": "linhai", "node_id": "general_engine", "activity_type": "manufacture", "role": "通用发动机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "林海股份主营业务", "quote": "主要产品:通用发动机及其配套的特种车辆、汽油机、摩托车及全地形车、林机"}]},
        {"exposure_id": "tongfang_manufacture_computer", "company_id": "tongfang", "node_id": "desktop_computer", "activity_type": "manufacture", "role": "计算机及电子设备制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "同方股份主营业务", "quote": "主要产品:计算机、电视机、E人E本等商用和消费类电子设备"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 048 done!")
