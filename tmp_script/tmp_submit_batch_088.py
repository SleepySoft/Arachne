#!/usr/bin/env python3
"""Submit batch 088 to Arachne API."""
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
        "node_id": "air_conditioner_compressor",
        "canonical_name_zh": "空调压缩机",
        "definition": "空调系统中用于压缩和输送制冷剂蒸汽的核心部件，是实现制冷循环的关键设备",
        "entity_type": "component"
    },
    {
        "node_id": "heat_pump",
        "canonical_name_zh": "热泵",
        "definition": "利用逆卡诺循环原理将低温热源热量转移到高温热源的节能装置，可用于供暖和热水",
        "entity_type": "device"
    },
    {
        "node_id": "capacitor",
        "canonical_name_zh": "电容器",
        "definition": "储存电荷的无源电子元件，用于电路中的滤波、耦合、储能等功能",
        "entity_type": "component"
    },
    {
        "node_id": "automotive_interior",
        "canonical_name_zh": "汽车内饰",
        "definition": "汽车内部装饰和功能性部件的总称，包括座椅、仪表板、地毯等",
        "entity_type": "material"
    },
    {
        "node_id": "textile_new_material",
        "canonical_name_zh": "纺织新材料",
        "definition": "采用新型纤维或特殊工艺制成的高性能纺织品材料，具有功能性或环保特性",
        "entity_type": "material"
    },
    {
        "node_id": "engineering_survey",
        "canonical_name_zh": "工程勘察",
        "definition": "为工程建设提供地质、水文、地形等基础资料的专业技术服务",
        "entity_type": "service"
    },
    {
        "node_id": "municipal_design",
        "canonical_name_zh": "市政设计",
        "definition": "对城市道路、桥梁、给排水、燃气等市政基础设施进行规划设计的专业服务",
        "entity_type": "service"
    },
    {
        "node_id": "apparel_brand",
        "canonical_name_zh": "服饰品牌",
        "definition": "具有市场认知度和品牌价值的服装服饰经营品牌，涵盖设计、生产、销售等环节",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "air_conditioner_compressor_to_air_conditioner",
        "from_node": "air_conditioner_compressor",
        "to_node": "air_conditioner",
        "edge_type": "composition",
        "description": "空调压缩机是空调制冷系统的核心动力部件"
    },
    {
        "edge_id": "capacitor_to_electronic_device",
        "from_node": "capacitor",
        "to_node": "electronic_device",
        "edge_type": "composition",
        "description": "电容器是电子设备中储存和调节电能的基础元件"
    },
    {
        "edge_id": "tire_to_automobile",
        "from_node": "tire",
        "to_node": "automobile",
        "edge_type": "composition",
        "description": "轮胎是汽车行走系统的关键部件"
    }
]

COMPANIES = [
    {
        "company_id": "highly",
        "name_zh": "上海海立(集团)股份有限公司",
        "stock_code": "600619.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "家用电器",
        "main_business": "研发,生产和销售空调压缩机,热泵及热泵热水器压缩机"
    },
    {
        "company_id": "tianchen",
        "name_zh": "上海市天宸股份有限公司",
        "stock_code": "600620.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "综合类",
        "main_business": "房地产,物业管理,运输及客运"
    },
    {
        "company_id": "huaxin",
        "name_zh": "上海华鑫股份有限公司",
        "stock_code": "600621.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "证券",
        "main_business": "证券业务为主,少量持有型物业为辅"
    },
    {
        "company_id": "everbright_jiabao",
        "name_zh": "光大嘉宝股份有限公司",
        "stock_code": "600622.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "区域地产",
        "main_business": "商品房,电容器"
    },
    {
        "company_id": "huayi",
        "name_zh": "上海华谊集团股份有限公司",
        "stock_code": "600623.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "化工原料",
        "main_business": "轮胎"
    },
    {
        "company_id": "st_fuhua",
        "name_zh": "上海复旦复华科技股份有限公司",
        "stock_code": "600624.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "化学制药",
        "main_business": "制造业,园区房地产,软件开发"
    },
    {
        "company_id": "shenda",
        "name_zh": "上海申达股份有限公司",
        "stock_code": "600626.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "汽车配件",
        "main_business": "汽车内饰和纺织新材料业务,以及纺织品为主的外贸进出口和国内贸易"
    },
    {
        "company_id": "new_world",
        "name_zh": "上海新世界股份有限公司",
        "stock_code": "600628.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "百货",
        "main_business": "商业"
    },
    {
        "company_id": "arcplus",
        "name_zh": "华东建筑集团股份有限公司",
        "stock_code": "600629.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "建筑工程",
        "main_business": "工程勘察,规划设计,工程设计,市政设计,水利工程设计,风景园林设计"
    },
    {
        "company_id": "dragon_head",
        "name_zh": "上海龙头(集团)股份有限公司",
        "stock_code": "600630.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "服饰",
        "main_business": "三枪,苏牌,菊花,鹅牌民光,幸福钟牌414,海螺"
    }
]

EXPOSURES = [
    {
        "exposure_id": "highly_manufacture_air_conditioner_compressor",
        "company_id": "highly",
        "node_id": "air_conditioner_compressor",
        "activity_type": "manufacture",
        "role": "空调压缩机制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "highly_manufacture_heat_pump",
        "company_id": "highly",
        "node_id": "heat_pump",
        "activity_type": "manufacture",
        "role": "热泵制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tianchen_operate_real_estate_development",
        "company_id": "tianchen",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianchen_provide_service_property_management",
        "company_id": "tianchen",
        "node_id": "property_management",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "tianchen_operate_passenger_transport",
        "company_id": "tianchen",
        "node_id": "passenger_transport",
        "activity_type": "operate",
        "role": "客运运营商",
        "weight": 0.8
    },
    {
        "exposure_id": "huaxin_provide_service_securities_service",
        "company_id": "huaxin",
        "node_id": "securities_service",
        "activity_type": "provide_service",
        "role": "证券服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "huaxin_provide_service_financial_service",
        "company_id": "huaxin",
        "node_id": "financial_service",
        "activity_type": "provide_service",
        "role": "金融服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "everbright_jiabao_operate_real_estate_development",
        "company_id": "everbright_jiabao",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "everbright_jiabao_manufacture_capacitor",
        "company_id": "everbright_jiabao",
        "node_id": "capacitor",
        "activity_type": "manufacture",
        "role": "电容器制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "huayi_produce_tire",
        "company_id": "huayi",
        "node_id": "tire",
        "activity_type": "produce",
        "role": "轮胎生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "huayi_produce_rubber_product",
        "company_id": "huayi",
        "node_id": "rubber_product",
        "activity_type": "produce",
        "role": "橡胶制品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "st_fuhua_operate_manufacturing",
        "company_id": "st_fuhua",
        "node_id": "manufacturing",
        "activity_type": "operate",
        "role": "制造业运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_fuhua_operate_real_estate_development",
        "company_id": "st_fuhua",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "园区房地产运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "st_fuhua_provide_service_software",
        "company_id": "st_fuhua",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件开发服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "shenda_produce_automotive_interior",
        "company_id": "shenda",
        "node_id": "automotive_interior",
        "activity_type": "produce",
        "role": "汽车内饰生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenda_produce_textile_new_material",
        "company_id": "shenda",
        "node_id": "textile_new_material",
        "activity_type": "produce",
        "role": "纺织新材料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenda_produce_textile_product",
        "company_id": "shenda",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "new_world_operate_commercial",
        "company_id": "new_world",
        "node_id": "commercial",
        "activity_type": "operate",
        "role": "商业运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "new_world_operate_retail",
        "company_id": "new_world",
        "node_id": "retail",
        "activity_type": "operate",
        "role": "零售运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "new_world_operate_department_store",
        "company_id": "new_world",
        "node_id": "department_store",
        "activity_type": "operate",
        "role": "百货运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "arcplus_provide_service_engineering_survey",
        "company_id": "arcplus",
        "node_id": "engineering_survey",
        "activity_type": "provide_service",
        "role": "工程勘察服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "arcplus_provide_service_municipal_design",
        "company_id": "arcplus",
        "node_id": "municipal_design",
        "activity_type": "provide_service",
        "role": "市政设计服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "arcplus_provide_service_construction_design",
        "company_id": "arcplus",
        "node_id": "construction_design",
        "activity_type": "provide_service",
        "role": "建筑设计服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "dragon_head_operate_apparel_brand",
        "company_id": "dragon_head",
        "node_id": "apparel_brand",
        "activity_type": "operate",
        "role": "服饰品牌运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "dragon_head_produce_apparel",
        "company_id": "dragon_head",
        "node_id": "apparel",
        "activity_type": "produce",
        "role": "服装生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "dragon_head_produce_textile_product",
        "company_id": "dragon_head",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.85
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
            "evidence": make_evidence(f"tushare batch 088: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 088: " + e["description"]),
        })
    return {
        "batch_id": "batch_088",
        "task_description": "Batch 088: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 088: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_088",
        "task_description": "Batch 088: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 088 Submission")
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
