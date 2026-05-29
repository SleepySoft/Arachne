#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 92."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_092.json"

def api_post(path, payload):
    url = f"{BASE}/{path}"
    r = requests.post(url, json=payload)
    if r.status_code not in (200, 201):
        print(f"  POST {path} failed: {r.status_code} - {r.text[:200]}")
    else:
        print(f"  POST {path} OK ({r.status_code})")
    return r

def make_evidence(quote, title="公司主营业务描述"):
    return [{"source_title": title, "quote": quote, "confidence": "HIGH", "status": "ACTIVE"}]

def main():
    with open(BATCH_FILE, encoding="utf-8") as f:
        companies = json.load(f)

    # Fetch existing nodes
    existing_nodes = {}
    page = 1
    while True:
        r = requests.get(f"{BASE}/nodes?page={page}&page_size=1000")
        items = r.json().get("items", [])
        if not items: break
        for n in items:
            existing_nodes[n["node_id"]] = n
        if len(items) < 1000: break
        page += 1
    print(f"Existing nodes: {len(existing_nodes)}")

    # Fetch existing edges
    existing_edges = set()
    page = 1
    while True:
        r = requests.get(f"{BASE}/edges?page={page}&page_size=1000")
        items = r.json().get("items", [])
        if not items: break
        for e in items:
            existing_edges.add((e.get("from_node") or e.get("source_id"), e.get("to_node") or e.get("target_id"), e["edge_type"]))
        if len(items) < 1000: break
        page += 1
    print(f"Existing edges: {len(existing_edges)}")

    # ---- Graph nodes ----
    nodes_to_create = []
    if "ophthalmic_eye_drop" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ophthalmic_eye_drop",
            "canonical_name_zh": "眼科用滴眼液",
            "canonical_name_en": "Ophthalmic Eye Drop",
            "definition": "用于眼部疾病治疗或保健的液体制剂，通过滴眼方式给药",
            "entity_type": "material",
            "evidence": make_evidence("珍珠明目滴眼液", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ophthalmic_eye_drop")
    if "chinese_patent_medicine_liquid" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "chinese_patent_medicine_liquid",
            "canonical_name_zh": "中成药液体制剂",
            "canonical_name_en": "Chinese Patent Medicine Liquid",
            "definition": "以中药材为原料经提取制成的可供内服或外用的液体制剂",
            "entity_type": "material",
            "evidence": make_evidence("复方鲜竹沥液", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: chinese_patent_medicine_liquid")
    if "hydrophilic_aluminum_foil" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "hydrophilic_aluminum_foil",
            "canonical_name_zh": "亲水铝箔",
            "canonical_name_en": "Hydrophilic Aluminum Foil",
            "definition": "表面经亲水涂层处理的铝箔材料，用于空调换热器等热交换设备",
            "entity_type": "material",
            "evidence": make_evidence("亲水箔的生产和销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: hydrophilic_aluminum_foil")
    if "tungsten_material" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "tungsten_material",
            "canonical_name_zh": "钨材料",
            "canonical_name_en": "Tungsten Material",
            "definition": "以钨金属为基础的材料产品，包括钨粉、碳化钨、钨合金等",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:钨系列", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: tungsten_material")
    if "ferromanganese" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ferromanganese",
            "canonical_name_zh": "锰铁合金",
            "canonical_name_en": "Ferromanganese",
            "definition": "铁与锰的合金材料，主要用于钢铁冶炼中的脱氧剂和合金添加剂",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:高锰,硅锰", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ferromanganese")
    if "ferrochrome" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ferrochrome",
            "canonical_name_zh": "铬铁合金",
            "canonical_name_en": "Ferrochrome",
            "definition": "铁与铬的合金材料，是不锈钢生产的重要原料",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:铬系列", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ferrochrome")
    if "smart_property_management" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "smart_property_management",
            "canonical_name_zh": "智能化物业管理服务",
            "canonical_name_en": "Smart Property Management Service",
            "definition": "运用智能化系统为物业提供安防、能耗、设施等综合管理服务",
            "entity_type": "service",
            "evidence": make_evidence("智能化物业管理和商品房经营租赁等业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: smart_property_management")
    if "commercial_housing_rental" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "commercial_housing_rental",
            "canonical_name_zh": "商品房租赁服务",
            "canonical_name_en": "Commercial Housing Rental Service",
            "definition": "将开发的商品房用于长期出租经营，提供租赁管理和配套服务",
            "entity_type": "service",
            "evidence": make_evidence("商品房经营租赁等业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: commercial_housing_rental")
    if "water_tourism_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "water_tourism_service",
            "canonical_name_zh": "水上旅游服务",
            "canonical_name_en": "Water Tourism Service",
            "definition": "以水域为载体，为游客提供观光、休闲、娱乐等水上旅游体验服务",
            "entity_type": "service",
            "evidence": make_evidence("水上旅游服务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: water_tourism_service")
    if "bicycle_part" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "bicycle_part",
            "canonical_name_zh": "自行车零部件",
            "canonical_name_en": "Bicycle Part",
            "definition": "构成自行车整车的各类零部件，包括车架、轮组、传动系统、制动系统等",
            "entity_type": "component",
            "evidence": make_evidence("自行车及零件(含电动车)", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: bicycle_part")
    if "gas_appliance" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "gas_appliance",
            "canonical_name_zh": "燃气具",
            "canonical_name_en": "Gas Appliance",
            "definition": "以燃气为能源的家用或商用器具，包括燃气灶、燃气热水器、燃气壁挂炉等",
            "entity_type": "component",
            "evidence": make_evidence("燃气具销售业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: gas_appliance")
    if "domestic_trade_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "domestic_trade_service",
            "canonical_name_zh": "国内贸易服务",
            "canonical_name_en": "Domestic Trade Service",
            "definition": "在国内市场从事商品采购、分销、批发及零售的贸易服务业务",
            "entity_type": "service",
            "evidence": make_evidence("商业(内贸)", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: domestic_trade_service")
    if "foreign_trade_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "foreign_trade_service",
            "canonical_name_zh": "外贸进出口服务",
            "canonical_name_en": "Foreign Trade Service",
            "definition": "从事跨境商品进出口代理、报关、物流及结算等外贸综合服务",
            "entity_type": "service",
            "evidence": make_evidence("外贸进出口", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: foreign_trade_service")

    # ---- Graph edges ----
    edges_to_create = []
    if ("cement", "ready_mixed_concrete", "material_flow") not in existing_edges and "cement" in existing_nodes and "ready_mixed_concrete" in existing_nodes:
        edges_to_create.append({
            "edge_id": "cement_to_concrete",
            "from_node": "cement",
            "to_node": "ready_mixed_concrete",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "水泥是生产混凝土的主要原料",
            "evidence": make_evidence("水泥,混凝土"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: cement_to_concrete")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_092_graph",
            "task_description": f"Batch 092 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次92构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
        }
        r = api_post("batches", batch)
        if r.status_code in (200, 201):
            print(f"Graph batch submitted: {len(nodes_to_create)} nodes, {len(edges_to_create)} edges")
        else:
            print(f"Graph batch FAILED: {r.status_code} {r.text[:300]}")
    else:
        print("No new graph nodes/edges to submit.")

    # ---- Companies and exposures ----
    companies_payload = []
    exposures_payload = []
    # 天目药业 (600671.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600671",
        "name_zh": "天目药业",
        "stock_codes": ["600671.SH"],
        "country": "中国",
        "industry": "中成药",
        "main_business": "珍珠明目滴眼液,复方鲜竹沥液.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("珍珠明目滴眼液,复方鲜竹沥液.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600671_ophthalmic_eye_drop",
        "company_id": "sh_600671",
        "node_id": "ophthalmic_eye_drop",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("珍珠明目滴眼液,复方鲜竹沥液.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600671_chinese_patent_medicine_liquid",
        "company_id": "sh_600671",
        "node_id": "chinese_patent_medicine_liquid",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("珍珠明目滴眼液,复方鲜竹沥液.")
    })
    # 东阳光 (600673.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600673",
        "name_zh": "东阳光",
        "stock_codes": ["600673.SH"],
        "country": "中国",
        "industry": "综合类",
        "main_business": "亲水箔的生产和销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("亲水箔的生产和销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600673_hydrophilic_aluminum_foil",
        "company_id": "sh_600673",
        "node_id": "hydrophilic_aluminum_foil",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("亲水箔的生产和销售.")
    })
    # 川投能源 (600674.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600674",
        "name_zh": "川投能源",
        "stock_codes": ["600674.SH"],
        "country": "中国",
        "industry": "水力发电",
        "main_business": "主要产品:钨系列,高锰,硅锰,铬系列.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:钨系列,高锰,硅锰,铬系列.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600674_tungsten_material",
        "company_id": "sh_600674",
        "node_id": "tungsten_material",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主要产品:钨系列,高锰,硅锰,铬系列.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600674_ferromanganese",
        "company_id": "sh_600674",
        "node_id": "ferromanganese",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:钨系列,高锰,硅锰,铬系列.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600674_ferrochrome",
        "company_id": "sh_600674",
        "node_id": "ferrochrome",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:钨系列,高锰,硅锰,铬系列.")
    })
    # 中华企业 (600675.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600675",
        "name_zh": "中华企业",
        "stock_codes": ["600675.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600675_real_estate_development",
        "company_id": "sh_600675",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.4,
        "evidence": make_evidence("房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600675_smart_property_management",
        "company_id": "sh_600675",
        "node_id": "smart_property_management",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600675_commercial_housing_rental",
        "company_id": "sh_600675",
        "node_id": "commercial_housing_rental",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.")
    })
    # 交运股份 (600676.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600676",
        "name_zh": "交运股份",
        "stock_codes": ["600676.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600676_logistics_service",
        "company_id": "sh_600676",
        "node_id": "logistics_service",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600676_automotive_part",
        "company_id": "sh_600676",
        "node_id": "automotive_part",
        "activity_type": "manufacture",
        "weight": 0.25,
        "evidence": make_evidence("主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600676_automotive_maintenance_service",
        "company_id": "sh_600676",
        "node_id": "automotive_maintenance_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600676_water_tourism_service",
        "company_id": "sh_600676",
        "node_id": "water_tourism_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.")
    })
    # ST金顶 (600678.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600678",
        "name_zh": "ST金顶",
        "stock_codes": ["600678.SH"],
        "country": "中国",
        "industry": "水泥",
        "main_business": "水泥,混凝土.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("水泥,混凝土.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600678_cement",
        "company_id": "sh_600678",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("水泥,混凝土.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600678_ready_mixed_concrete",
        "company_id": "sh_600678",
        "node_id": "ready_mixed_concrete",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("水泥,混凝土.")
    })
    # 上海凤凰 (600679.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600679",
        "name_zh": "上海凤凰",
        "stock_codes": ["600679.SH"],
        "country": "中国",
        "industry": "文教休闲",
        "main_business": "主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600679_bicycle",
        "company_id": "sh_600679",
        "node_id": "bicycle",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600679_bicycle_part",
        "company_id": "sh_600679",
        "node_id": "bicycle_part",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600679_electric_bicycle",
        "company_id": "sh_600679",
        "node_id": "electric_bicycle",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600679_medical_device",
        "company_id": "sh_600679",
        "node_id": "medical_device",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600679_hotel",
        "company_id": "sh_600679",
        "node_id": "hotel",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等")
    })
    # 百川能源 (600681.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600681",
        "name_zh": "百川能源",
        "stock_codes": ["600681.SH"],
        "country": "中国",
        "industry": "供气供热",
        "main_business": "主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600681_city_gas",
        "company_id": "sh_600681",
        "node_id": "city_gas",
        "activity_type": "procure",
        "weight": 0.4,
        "evidence": make_evidence("主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600681_city_gas_supply",
        "company_id": "sh_600681",
        "node_id": "city_gas_supply",
        "activity_type": "operate",
        "weight": 0.35,
        "evidence": make_evidence("主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600681_gas_appliance",
        "company_id": "sh_600681",
        "node_id": "gas_appliance",
        "activity_type": "procure",
        "weight": 0.25,
        "evidence": make_evidence("主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务")
    })
    # 南京新百 (600682.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600682",
        "name_zh": "南京新百",
        "stock_codes": ["600682.SH"],
        "country": "中国",
        "industry": "生物制药",
        "main_business": "主营业务:百货零售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:百货零售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600682_department_store",
        "company_id": "sh_600682",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:百货零售.")
    })
    # 京投发展 (600683.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600683",
        "name_zh": "京投发展",
        "stock_codes": ["600683.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "主要业务:商业(内贸),外贸进出口.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务:商业(内贸),外贸进出口.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600683_domestic_trade_service",
        "company_id": "sh_600683",
        "node_id": "domestic_trade_service",
        "activity_type": "procure",
        "weight": 0.5,
        "evidence": make_evidence("主要业务:商业(内贸),外贸进出口.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600683_foreign_trade_service",
        "company_id": "sh_600683",
        "node_id": "foreign_trade_service",
        "activity_type": "procure",
        "weight": 0.5,
        "evidence": make_evidence("主要业务:商业(内贸),外贸进出口.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_092_biz",
            "task_description": f"Batch 092 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次92构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
        }
        r = api_post("business-batches", biz_batch)
        if r.status_code in (200, 201):
            print(f"Business batch submitted: {len(companies_payload)} companies, {len(exposures_payload)} exposures")
        else:
            print(f"Business batch FAILED: {r.status_code} {r.text[:300]}")
    else:
        print("No companies to submit.")

if __name__ == "__main__":
    main()
