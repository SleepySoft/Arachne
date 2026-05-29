#!/usr/bin/env python3
"""Submit batch 073 to Arachne API."""
import json, requests
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=30)
    return r.status_code, r.text if r.status_code not in (200, 201) else r.json()

def make_evidence(quote, source_title="Tushare数据"):
    return [{
        "source_title": source_title,
        "quote": quote,
        "source_reference": "tushare",
        "confidence": "HIGH",
        "recorded_at": datetime.now().isoformat()
    }]

NEW_NODES = [
    {
        "node_id": "funeral_service",
        "canonical_name_zh": "殡葬服务",
        "definition": "为逝者提供遗体处理、安葬、悼念等服务的行业",
        "entity_type": "service"
    },
    {
        "node_id": "artemisinin_series",
        "canonical_name_zh": "蒿甲醚系列产品",
        "definition": "以青蒿素及其衍生物为主要成分的药物系列，主要用于抗疟疾治疗",
        "entity_type": "material"
    },
    {
        "node_id": "notoginseng_series",
        "canonical_name_zh": "三七系列产品",
        "definition": "以三七为主要原料的中药系列产品，具有活血化瘀功效",
        "entity_type": "material"
    },
    {
        "node_id": "nitric_acid",
        "canonical_name_zh": "硝酸",
        "definition": "一种重要的无机强酸，广泛用于制造化肥、炸药、染料等化工产品",
        "entity_type": "material"
    },
    {
        "node_id": "formaldehyde",
        "canonical_name_zh": "甲醛",
        "definition": "一种重要的有机化工原料，用于制造树脂、塑料、纤维等",
        "entity_type": "material"
    },
    {
        "node_id": "carbonless_paper",
        "canonical_name_zh": "无碳纸",
        "definition": "一种无需碳粉即可实现复写的特种纸张，用于多联票据",
        "entity_type": "material"
    },
    {
        "node_id": "navigation_control",
        "canonical_name_zh": "导航控制系统",
        "definition": "用于精确制导和导航控制的电子系统，广泛应用于军事和民用领域",
        "entity_type": "system"
    },
    {
        "node_id": "ammunition_info_system",
        "canonical_name_zh": "弹药信息化系统",
        "definition": "用于弹药制导、控制和信息传输的电子系统",
        "entity_type": "system"
    }
]

NEW_EDGES = [
    {
        "edge_id": "formaldehyde_to_chemical_product",
        "from_node": "formaldehyde",
        "to_node": "chemical_product",
        "edge_type": "material_flow",
        "description": "甲醛是重要的有机化工原料，用于生产多种化工产品"
    },
    {
        "edge_id": "nitric_acid_to_fertilizer",
        "from_node": "nitric_acid",
        "to_node": "fertilizer",
        "edge_type": "material_flow",
        "description": "硝酸是生产氮肥等化肥的重要原料"
    },
    {
        "edge_id": "navigation_control_to_defense_equipment",
        "from_node": "navigation_control",
        "to_node": "defense_equipment",
        "edge_type": "composition",
        "description": "导航控制系统是现代防务装备的核心组成部分"
    }
]

COMPANIES = [
    {
        "company_id": "st_huarong",
        "name_zh": "武汉华嵘控股股份有限公司",
        "stock_code": "600421.SH",
        "province": "湖北",
        "city": "武汉市",
        "industry": "专用机械",
        "main_business": "墓地销售代理,殡葬服务"
    },
    {
        "company_id": "kunyao_group",
        "name_zh": "昆药集团股份有限公司",
        "stock_code": "600422.SH",
        "province": "云南",
        "city": "昆明市",
        "industry": "中成药",
        "main_business": "蒿甲醚系列,三七系列,天麻素系列等中西药生产与销售"
    },
    {
        "company_id": "st_liuhua",
        "name_zh": "柳州化工股份有限公司",
        "stock_code": "600423.SH",
        "province": "广西",
        "city": "柳州市",
        "industry": "农药化肥",
        "main_business": "硝酸铵,尿素,浓硝酸,甲醛,精甲醇,纯碱,氯化铵及碳酸氢铵"
    },
    {
        "company_id": "qingsong_jianhua",
        "name_zh": "新疆青松建材化工(集团)股份有限公司",
        "stock_code": "600425.SH",
        "province": "新疆",
        "city": "阿拉尔市",
        "industry": "水泥",
        "main_business": "建材产品,水泥及水泥制品的生产和销售"
    },
    {
        "company_id": "hualu_hensheng",
        "name_zh": "山东华鲁恒升化工股份有限公司",
        "stock_code": "600426.SH",
        "province": "山东",
        "city": "德州市",
        "industry": "农药化肥",
        "main_business": "尿素,DMF,三甲胺及甲醛的生产和销售"
    },
    {
        "company_id": "cosco_specialized",
        "name_zh": "中远海运特种运输股份有限公司",
        "stock_code": "600428.SH",
        "province": "广东",
        "city": "广州市",
        "industry": "水运",
        "main_business": "航运业务"
    },
    {
        "company_id": "sanyuan",
        "name_zh": "北京三元食品股份有限公司",
        "stock_code": "600429.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "乳制品",
        "main_business": "乳制品生产,加工,销售"
    },
    {
        "company_id": "guanhao",
        "name_zh": "广东冠豪高新技术股份有限公司",
        "stock_code": "600433.SH",
        "province": "广东",
        "city": "湛江市",
        "industry": "造纸",
        "main_business": "无碳纸的生产与销售"
    },
    {
        "company_id": "norinco_nav",
        "name_zh": "北方导航控制技术股份有限公司",
        "stock_code": "600435.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "专用机械",
        "main_business": "导航控制,弹药信息化系统,短波电台和卫星通信系统,军用电连接器"
    },
    {
        "company_id": "pientzehuang",
        "name_zh": "漳州片仔癀药业股份有限公司",
        "stock_code": "600436.SH",
        "province": "福建",
        "city": "漳州市",
        "industry": "中成药",
        "main_business": "片仔癀及其系列产品"
    }
]

EXPOSURES = [
    {
        "exposure_id": "st_huarong_operate_funeral_service",
        "company_id": "st_huarong",
        "node_id": "funeral_service",
        "activity_type": "operate",
        "role": "殡葬服务运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_huarong_operate_cemetery",
        "company_id": "st_huarong",
        "node_id": "cemetery",
        "activity_type": "operate",
        "role": "墓地运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "kunyao_group_produce_artemisinin_series",
        "company_id": "kunyao_group",
        "node_id": "artemisinin_series",
        "activity_type": "produce",
        "role": "蒿甲醚系列产品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "kunyao_group_produce_notoginseng_series",
        "company_id": "kunyao_group",
        "node_id": "notoginseng_series",
        "activity_type": "produce",
        "role": "三七系列产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "kunyao_group_produce_chinese_patent_medicine",
        "company_id": "kunyao_group",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_liuhua_produce_nitric_acid",
        "company_id": "st_liuhua",
        "node_id": "nitric_acid",
        "activity_type": "produce",
        "role": "硝酸生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_liuhua_produce_urea",
        "company_id": "st_liuhua",
        "node_id": "urea",
        "activity_type": "produce",
        "role": "尿素生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_liuhua_produce_formaldehyde",
        "company_id": "st_liuhua",
        "node_id": "formaldehyde",
        "activity_type": "produce",
        "role": "甲醛生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_liuhua_produce_methanol",
        "company_id": "st_liuhua",
        "node_id": "methanol",
        "activity_type": "produce",
        "role": "甲醇生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "qingsong_jianhua_produce_cement",
        "company_id": "qingsong_jianhua",
        "node_id": "cement",
        "activity_type": "produce",
        "role": "水泥生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "qingsong_jianhua_produce_building_material",
        "company_id": "qingsong_jianhua",
        "node_id": "building_material",
        "activity_type": "produce",
        "role": "建材生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "hualu_hensheng_produce_urea",
        "company_id": "hualu_hensheng",
        "node_id": "urea",
        "activity_type": "produce",
        "role": "尿素生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "hualu_hensheng_produce_formaldehyde",
        "company_id": "hualu_hensheng",
        "node_id": "formaldehyde",
        "activity_type": "produce",
        "role": "甲醛生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "hualu_hensheng_produce_chemical_product",
        "company_id": "hualu_hensheng",
        "node_id": "chemical_product",
        "activity_type": "produce",
        "role": "化工产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "cosco_specialized_operate_shipping",
        "company_id": "cosco_specialized",
        "node_id": "shipping",
        "activity_type": "operate",
        "role": "航运运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "cosco_specialized_provide_service_logistics",
        "company_id": "cosco_specialized",
        "node_id": "logistics",
        "activity_type": "provide_service",
        "role": "物流服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "sanyuan_produce_dairy_product",
        "company_id": "sanyuan",
        "node_id": "dairy_product",
        "activity_type": "produce",
        "role": "乳制品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sanyuan_produce_food",
        "company_id": "sanyuan",
        "node_id": "food",
        "activity_type": "produce",
        "role": "食品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "guanhao_produce_carbonless_paper",
        "company_id": "guanhao",
        "node_id": "carbonless_paper",
        "activity_type": "produce",
        "role": "无碳纸生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "guanhao_produce_paper",
        "company_id": "guanhao",
        "node_id": "paper",
        "activity_type": "produce",
        "role": "造纸商",
        "weight": 0.9
    },
    {
        "exposure_id": "norinco_nav_manufacture_navigation_control",
        "company_id": "norinco_nav",
        "node_id": "navigation_control",
        "activity_type": "manufacture",
        "role": "导航控制系统制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "norinco_nav_manufacture_ammunition_info_system",
        "company_id": "norinco_nav",
        "node_id": "ammunition_info_system",
        "activity_type": "manufacture",
        "role": "弹药信息化系统制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "norinco_nav_manufacture_special_vehicle",
        "company_id": "norinco_nav",
        "node_id": "special_vehicle",
        "activity_type": "manufacture",
        "role": "专用车制造商",
        "weight": 0.8
    },
    {
        "exposure_id": "pientzehuang_produce_chinese_patent_medicine",
        "company_id": "pientzehuang",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "pientzehuang_produce_pharmaceutical",
        "company_id": "pientzehuang",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    }
]

def build_graph_batch():
    nodes_to_upsert = []
    for n in NEW_NODES:
        nodes_to_upsert.append({
            "node_id": n["node_id"],
            "canonical_name_zh": n["canonical_name_zh"],
            "canonical_name_en": n.get("canonical_name_en"),
            "definition": n["definition"],
            "entity_type": n["entity_type"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 073: " + n["canonical_name_zh"]),
        })
    edges_to_upsert = []
    for e in NEW_EDGES:
        edges_to_upsert.append({
            "edge_id": e["edge_id"],
            "from_node": e["from_node"],
            "to_node": e["to_node"],
            "edge_namespace": "industrial_flow",
            "edge_type": e["edge_type"],
            "description": e["description"],
            "confidence": "HIGH",
            "evidence": make_evidence(f"tushare batch 073: " + e["description"]),
        })
    return {
        "batch_id": "batch_073",
        "task_description": "Batch 073: industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

def build_business_batch():
    companies_to_upsert = []
    for c in COMPANIES:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "name_en": c.get("name_en"),
            "stock_codes": [c["stock_code"]],
            "country": "CN",
            "province": c["province"],
            "city": c["city"],
            "industry": c["industry"],
            "main_business": c["main_business"],
            "company_type": "public",
            "status": "ACTIVE",
            "evidence": make_evidence("tushare: " + c["main_business"]),
        })
    exposures_to_upsert = []
    for exp in EXPOSURES:
        exposures_to_upsert.append({
            "exposure_id": exp["exposure_id"],
            "company_id": exp["company_id"],
            "node_id": exp["node_id"],
            "activity_type": exp["activity_type"],
            "role": exp["role"],
            "weight": exp["weight"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 073: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_073",
        "task_description": "Batch 073: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 073 Submission")
    print("=" * 60)
    graph_batch = build_graph_batch()
    print(f"\nGraph batch: {len(graph_batch['nodes_to_upsert'])} nodes, {len(graph_batch['edges_to_upsert'])} edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, resp = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {resp}")
    else:
        print("Graph batch: nothing to submit")
    biz_batch = build_business_batch()
    print(f"\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, resp = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {resp}")
    print("\nDone.")
