#!/usr/bin/env python3
"""Batch 047: 600072-600084"""
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
    "batch_id": "batch_047_graph",
    "task_description": "Batch 047 graph: canned food, chlor alkali, container floor, phosphorus chemical, anesthetic.",
    "nodes_to_upsert": [
        {"node_id": "canned_food", "canonical_name_zh": "罐头食品", "canonical_name_en": "Canned Food", "aliases": ["肉罐头", "水果罐头"], "definition": "将食品原料经预处理、装罐、密封、杀菌等工艺制成的可长期保存的即食食品。", "entity_type": "material", "evidence": [{"source_title": "光明肉业主营业务", "quote": "主要产品为猪肉、牛肉、羊肉、罐头、蜂蜜、大白兔奶糖、保健酒、味精、烘焙食品、饮用水等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "chlor_alkali_product", "canonical_name_zh": "氯碱化工产品", "canonical_name_en": "Chlor-alkali Product", "aliases": ["聚氯乙烯", "烧碱", "液氯"], "definition": "以电解食盐水为基础生产的烧碱、氯气和氢气及其下游化工产品。", "entity_type": "material", "evidence": [{"source_title": "新疆天业主营业务", "quote": "主营业务:氯碱化工和塑料节水器材"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "container_floor", "canonical_name_zh": "集装箱底板", "canonical_name_en": "Container Floor", "aliases": ["集装箱木地板", "COSB底板"], "definition": "用于集装箱内部的承重底板材料，需具备高强度、耐磨和防腐性能。", "entity_type": "component", "evidence": [{"source_title": "康欣新材主营业务", "quote": "主要从事集装箱底板等优质、新型木质复合材料的研发、生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "phosphorus_chemical", "canonical_name_zh": "磷化工产品", "canonical_name_en": "Phosphorus Chemical", "aliases": ["黄磷", "磷酸", "磷酸盐"], "definition": "以磷矿石为原料生产的黄磷、磷酸及其盐类化工产品。", "entity_type": "material", "evidence": [{"source_title": "澄星股份主营业务", "quote": "主要业务:黄磷、磷酸及磷酸盐类系列产品的生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "anesthetic_product", "canonical_name_zh": "麻醉药品", "canonical_name_en": "Anesthetic Product", "aliases": ["麻醉剂", "镇痛药"], "definition": "能使机体或机体局部暂时失去知觉及痛觉的药物，主要用于手术麻醉和疼痛管理。", "entity_type": "material", "evidence": [{"source_title": "人福医药主营业务", "quote": "宜昌人福枸橼酸芬太尼注射液、枸橼酸舒芬太尼注射液、注射用盐酸瑞芬太尼等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "ship_accessory", "canonical_name_zh": "船舶配件", "canonical_name_en": "Ship Accessory", "aliases": ["船用配件", "船舶零部件"], "definition": "用于船舶制造、维修和运营的各类机械、电气及舾装零部件。", "entity_type": "component", "evidence": [{"source_title": "中船科技主营业务", "quote": "主要产品:工程设计、勘察、咨询和监理、工程总承包、土地整理服务、船舶配件等"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "phosphorus_chemical_to_fertilizer", "from_node": "phosphorus_chemical", "to_node": "chemical_fertilizer", "edge_type": "material_flow", "description": "磷化工产品是磷肥生产的重要原料。", "evidence": [{"source_title": "化肥生产工艺", "quote": "磷酸是生产磷肥和复合肥的关键原料"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_047_business",
    "task_description": "Batch 047 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "cssc_tech", "name_zh": "中船科技股份有限公司", "aliases": ["中船科技"], "stock_codes": ["600072.SH"], "description": "工程设计、勘察、咨询、监理及船舶配件企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "bright_meat", "name_zh": "上海光明肉业集团股份有限公司", "aliases": ["光明肉业"], "stock_codes": ["600073.SH"], "description": "猪肉、牛肉、羊肉、罐头及乳制品等食品企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "xinjiang_tianye", "name_zh": "新疆天业股份有限公司", "aliases": ["新疆天业"], "stock_codes": ["600075.SH"], "description": "氯碱化工和塑料节水器材企业", "country": "CN", "province": "新疆", "city": "石河子", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "kangxin", "name_zh": "康欣新材料科技股份有限公司", "aliases": ["康欣新材"], "stock_codes": ["600076.SH"], "description": "集装箱底板、木质复合材料及木结构房屋企业", "country": "CN", "province": "湖北", "city": "孝感", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "chengxing", "name_zh": "江苏澄星磷化工股份有限公司", "aliases": ["澄星股份"], "stock_codes": ["600078.SH"], "description": "黄磷、磷酸及磷酸盐类系列产品企业", "country": "CN", "province": "江苏", "city": "江阴", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_renfu", "name_zh": "人福医药集团股份公司", "aliases": ["ST人福", "人福医药"], "stock_codes": ["600079.SH"], "description": "麻醉药品、神经系统用药及维吾尔药企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_jinhua", "name_zh": "金花企业(集团)股份有限公司", "aliases": ["ST金花"], "stock_codes": ["600080.SH"], "description": "医药工业及医药商业企业", "country": "CN", "province": "陕西", "city": "西安", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "dongfeng_tech", "name_zh": "东风电子科技股份有限公司", "aliases": ["东风科技"], "stock_codes": ["600081.SH"], "description": "汽车仪表系统、制动系统及汽车电子企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "st_haitai", "name_zh": "天津海泰科技发展股份有限公司", "aliases": ["ST海泰"], "stock_codes": ["600082.SH"], "description": "园区开发及产业投资企业", "country": "CN", "province": "天津", "city": "天津", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_niya", "name_zh": "中信国安葡萄酒业股份有限公司", "aliases": ["*ST尼雅"], "stock_codes": ["600084.SH"], "description": "葡萄酒生产销售企业", "country": "CN", "province": "新疆", "city": "伊犁", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "cssc_provide_ship_accessory", "company_id": "cssc_tech", "node_id": "ship_accessory", "activity_type": "manufacture", "role": "船舶配件制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中船科技主营业务", "quote": "主要产品:工程设计、勘察、咨询和监理、工程总承包、土地整理服务、船舶配件等"}]},
        {"exposure_id": "bright_produce_canned", "company_id": "bright_meat", "node_id": "canned_food", "activity_type": "produce", "role": "罐头食品生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "光明肉业主营业务", "quote": "主要产品为猪肉、牛肉、羊肉、罐头、蜂蜜、大白兔奶糖等"}]},
        {"exposure_id": "bright_produce_meat", "company_id": "bright_meat", "node_id": "meat_product", "activity_type": "produce", "role": "肉类产品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "光明肉业主营业务", "quote": "主要产品为猪肉、牛肉、羊肉、罐头"}]},
        {"exposure_id": "xinjiang_produce_chlor_alkali", "company_id": "xinjiang_tianye", "node_id": "chlor_alkali_product", "activity_type": "produce", "role": "氯碱化工产品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "新疆天业主营业务", "quote": "主营业务:氯碱化工和塑料节水器材"}]},
        {"exposure_id": "kangxin_manufacture_container_floor", "company_id": "kangxin", "node_id": "container_floor", "activity_type": "manufacture", "role": "集装箱底板制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "康欣新材主营业务", "quote": "主要从事集装箱底板等优质、新型木质复合材料的研发、生产和销售"}]},
        {"exposure_id": "chengxing_produce_phosphorus", "company_id": "chengxing", "node_id": "phosphorus_chemical", "activity_type": "produce", "role": "磷化工产品生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "澄星股份主营业务", "quote": "主要业务:黄磷、磷酸及磷酸盐类系列产品的生产和销售"}]},
        {"exposure_id": "renfu_produce_anesthetic", "company_id": "st_renfu", "node_id": "anesthetic_product", "activity_type": "produce", "role": "麻醉药品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "人福医药主营业务", "quote": "宜昌人福枸橼酸芬太尼注射液、枸橼酸舒芬太尼注射液等"}]},
        {"exposure_id": "jinhua_produce_chinese_patent", "company_id": "st_jinhua", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "金花股份主营业务", "quote": "主要业务:医药工业、医药商业"}]},
        {"exposure_id": "dongfeng_tech_manufacture_auto_electronics", "company_id": "dongfeng_tech", "node_id": "automotive_electronics", "activity_type": "manufacture", "role": "汽车电子及零部件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东风科技主营业务", "quote": "主要产品:汽车仪表系统、饰件系统、制动系统、汽车电子系统产品"}]},
        {"exposure_id": "haitai_operate_park", "company_id": "st_haitai", "node_id": "real_estate_development", "activity_type": "operate", "role": "园区开发运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "海泰发展主营业务", "quote": "主营业务涉及地产、高新产业投资、股权投资三个业务板块"}]},
        {"exposure_id": "niya_produce_wine", "company_id": "st_niya", "node_id": "wine", "activity_type": "produce", "role": "葡萄酒生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "尼雅主营业务", "quote": "主营业务:葡萄酒生产销售"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 047 done!")
