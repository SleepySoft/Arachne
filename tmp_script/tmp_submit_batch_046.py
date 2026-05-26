#!/usr/bin/env python3
"""Batch 046: 600058-600071"""
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
    "batch_id": "batch_046_graph",
    "task_description": "Batch 046 graph: shaoxing wine, injection, PVA fiber, enamelled wire, optical lens.",
    "nodes_to_upsert": [
        {"node_id": "shaoxing_wine", "canonical_name_zh": "绍兴黄酒", "canonical_name_en": "Shaoxing Rice Wine", "aliases": ["花雕酒", "加饭酒", "元红酒"], "definition": "以糯米、小麦和水为原料，经发酵酿造而成的中国传统低度酿造酒。", "entity_type": "material", "evidence": [{"source_title": "古越龙山主营业务", "quote": "主要产品:绍兴加饭酒、绍兴元红酒、绍兴香雪酒、绍兴善酿酒和绍兴花雕酒等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "injection", "canonical_name_zh": "注射剂", "canonical_name_en": "Injection", "aliases": ["针剂", "注射液"], "definition": "将药物配制成供注入体内的无菌溶液、乳状液或混悬液制剂。", "entity_type": "material", "evidence": [{"source_title": "华润双鹤主营业务", "quote": "主要产品:大容量注射剂、小容量注射剂、冻干粉针剂、冲洗剂、口服溶液剂等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "pva_fiber", "canonical_name_zh": "PVA纤维", "canonical_name_en": "PVA Fiber", "aliases": ["聚乙烯醇纤维", "维纶"], "definition": "以聚乙烯醇为原料制成的高强度合成纤维，广泛用于水泥增强、橡胶制品等领域。", "entity_type": "material", "evidence": [{"source_title": "皖维高业主营业务", "quote": "主要产品:聚乙烯醇、高强高模PVA纤维、水泥、聚脂切片、陶瓷膜"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "enamelled_wire", "canonical_name_zh": "漆包线", "canonical_name_en": "Enamelled Wire", "aliases": ["电磁线", "绕组线"], "definition": "以铜或铝为导体，表面涂覆绝缘漆层的电线，用于电机、变压器等绕组。", "entity_type": "material", "evidence": [{"source_title": "冠城新材主营业务", "quote": "主要产品:漆包线、钢芯铝绞线、其他线、房地产"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "optical_lens", "canonical_name_zh": "光学镜片", "canonical_name_en": "Optical Lens", "aliases": ["光学镜头", "透镜"], "definition": "利用光学原理对光线进行折射、反射或聚焦的精密光学元件。", "entity_type": "component", "evidence": [{"source_title": "凤凰光学主营业务", "quote": "主要产品:光学镜片、光学镜头、照相器材、望远镜、钢片快门、水晶饰品、电子产品及通信设备、光学原材料、仪器零配件等"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "pva_fiber_to_cement", "from_node": "pva_fiber", "to_node": "cement", "edge_type": "composition", "description": "PVA纤维作为增强材料掺入水泥中，提高水泥制品的抗裂性和韧性。", "evidence": [{"source_title": "皖维高业主营业务", "quote": "主要产品:聚乙烯醇、高强高模PVA纤维、水泥"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_046_business",
    "task_description": "Batch 046 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "minmetals_dev", "name_zh": "五矿发展股份有限公司", "aliases": ["五矿发展"], "stock_codes": ["600058.SH"], "description": "钢材、不锈钢及冶金原材料贸易企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "guyuelongshan", "name_zh": "浙江古越龙山绍兴酒股份有限公司", "aliases": ["古越龙山"], "stock_codes": ["600059.SH"], "description": "绍兴黄酒生产销售企业", "country": "CN", "province": "浙江", "city": "绍兴", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "hisense_visual", "name_zh": "海信视像科技股份有限公司", "aliases": ["海信视像"], "stock_codes": ["600060.SH"], "description": "电视产品研发、生产和销售企业", "country": "CN", "province": "山东", "city": "青岛", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sdic_capital", "name_zh": "国投资本股份有限公司", "aliases": ["国投资本"], "stock_codes": ["600061.SH"], "description": "证券期货、信托及公募基金业务企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "cr_double_crane", "name_zh": "华润双鹤药业股份有限公司", "aliases": ["华润双鹤"], "stock_codes": ["600062.SH"], "description": "大容量注射剂、冻干粉针剂及口服制剂等药品生产企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "wanwei", "name_zh": "安徽皖维高新材料股份有限公司", "aliases": ["皖维高新"], "stock_codes": ["600063.SH"], "description": "聚乙烯醇、PVA纤维、水泥及新材料生产企业", "country": "CN", "province": "安徽", "city": "巢湖", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "nanjing_gaoke", "name_zh": "南京高科股份有限公司", "aliases": ["南京高科"], "stock_codes": ["600064.SH"], "description": "市政基础设施、土地开发、电力及药品销售企业", "country": "CN", "province": "江苏", "city": "南京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "yutong_bus", "name_zh": "宇通客车股份有限公司", "aliases": ["宇通客车"], "stock_codes": ["600066.SH"], "description": "客车产品研发、制造和销售企业", "country": "CN", "province": "河南", "city": "郑州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "guancheng", "name_zh": "冠城新材料股份有限公司", "aliases": ["冠城新材"], "stock_codes": ["600067.SH"], "description": "漆包线、钢芯铝绞线等电气材料及房地产企业", "country": "CN", "province": "福建", "city": "福州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "phoenix_optical", "name_zh": "凤凰光学股份有限公司", "aliases": ["凤凰光学"], "stock_codes": ["600071.SH"], "description": "光学镜片、光学镜头、望远镜及显微镜等光学产品企业", "country": "CN", "province": "江西", "city": "上饶", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "minmetals_trade_steel", "company_id": "minmetals_dev", "node_id": "steel_plate", "activity_type": "procure", "role": "钢材贸易商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "五矿发展主营业务", "quote": "主要业务:国内外贸易;主要产品:不锈钢、冷轧卷板、热轧卷板、钢坯"}]},
        {"exposure_id": "guyuelongshan_produce_wine", "company_id": "guyuelongshan", "node_id": "shaoxing_wine", "activity_type": "produce", "role": "绍兴黄酒生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "古越龙山主营业务", "quote": "主要产品:绍兴加饭酒、绍兴元红酒、绍兴香雪酒、绍兴善酿酒和绍兴花雕酒等"}]},
        {"exposure_id": "hisense_manufacture_tv", "company_id": "hisense_visual", "node_id": "color_tv", "activity_type": "manufacture", "role": "电视机制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "海信视像主营业务", "quote": "主要产品:电视产品"}]},
        {"exposure_id": "sdic_provide_securities", "company_id": "sdic_capital", "node_id": "securities_service", "activity_type": "provide_service", "role": "综合金融服务商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "国投资本主营业务", "quote": "主营业务:证券期货业务、信托业务、公募基金业务"}]},
        {"exposure_id": "cr_crane_produce_injection", "company_id": "cr_double_crane", "node_id": "injection", "activity_type": "produce", "role": "注射剂生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华润双鹤主营业务", "quote": "主要产品:大容量注射剂、小容量注射剂、冻干粉针剂等"}]},
        {"exposure_id": "wanwei_produce_pva_fiber", "company_id": "wanwei", "node_id": "pva_fiber", "activity_type": "produce", "role": "PVA纤维生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "皖维高业主营业务", "quote": "主要产品:聚乙烯醇、高强高模PVA纤维、水泥"}]},
        {"exposure_id": "wanwei_produce_cement", "company_id": "wanwei", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "皖维高业主营业务", "quote": "主要产品:聚乙烯醇、高强高模PVA纤维、水泥"}]},
        {"exposure_id": "nanjing_operate_real_estate", "company_id": "nanjing_gaoke", "node_id": "real_estate_development", "activity_type": "operate", "role": "园区开发及房地产运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "南京高科主营业务", "quote": "主要业务:市政基础设施承建、土地成片开发转让、电力销售、药品销售"}]},
        {"exposure_id": "yutong_manufacture_bus", "company_id": "yutong_bus", "node_id": "bus", "activity_type": "manufacture", "role": "客车制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "宇通客车主营业务", "quote": "主营业务:客车产品研发、制造与销售"}]},
        {"exposure_id": "guancheng_produce_enamelled_wire", "company_id": "guancheng", "node_id": "enamelled_wire", "activity_type": "produce", "role": "漆包线生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "冠城新材主营业务", "quote": "主要产品:漆包线、钢芯铝绞线、其他线"}]},
        {"exposure_id": "phoenix_manufacture_optical_lens", "company_id": "phoenix_optical", "node_id": "optical_lens", "activity_type": "manufacture", "role": "光学镜片及镜头制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "凤凰光学主营业务", "quote": "主要产品:光学镜片、光学镜头、照相器材、望远镜、显微镜等"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 046 done!")
