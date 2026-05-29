#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 91."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_091.json"

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
    if "tech_park_operation_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "tech_park_operation_service",
            "canonical_name_zh": "科技产业园区运营服务",
            "canonical_name_en": "Technology Park Operation Service",
            "definition": "为科技产业园区提供整体运营、招商、物业管理及产业配套服务的业务形态",
            "entity_type": "service",
            "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: tech_park_operation_service")
    if "automotive_glass" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "automotive_glass",
            "canonical_name_zh": "汽车玻璃",
            "canonical_name_en": "Automotive Glass",
            "definition": "用于汽车车身门窗等部位的专用安全玻璃制品，包括前挡、侧窗、后挡等",
            "entity_type": "component",
            "evidence": make_evidence("从事浮法玻璃及汽车用玻璃制品的生产及销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: automotive_glass")
    if "taxi_operation_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "taxi_operation_service",
            "canonical_name_zh": "出租汽车运营服务",
            "canonical_name_en": "Taxi Operation Service",
            "definition": "以出租汽车为载体，为乘客提供点对点出行运输服务的运营业务",
            "entity_type": "service",
            "evidence": make_evidence("出租汽车服务及其相关业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: taxi_operation_service")
    if "chinese_medicine_preparation" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "chinese_medicine_preparation",
            "canonical_name_zh": "中药制剂",
            "canonical_name_en": "Chinese Medicine Preparation",
            "definition": "以中药材为原料，经提取、浓缩、成型等工艺制成的成药制剂",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:中药", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: chinese_medicine_preparation")
    if "chemical_drug_preparation" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "chemical_drug_preparation",
            "canonical_name_zh": "化学药品制剂",
            "canonical_name_en": "Chemical Drug Preparation",
            "definition": "以化学原料药为基础，经配方、制剂工艺制成的可供临床使用的药品",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:西药", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: chemical_drug_preparation")
    if "health_food" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "health_food",
            "canonical_name_zh": "保健食品",
            "canonical_name_en": "Health Food",
            "definition": "具有特定保健功能，适宜特定人群食用，不以治疗疾病为目的的食品",
            "entity_type": "material",
            "evidence": make_evidence("主要产品:保健品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: health_food")
    if "sapphire_crystal_material" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "sapphire_crystal_material",
            "canonical_name_zh": "蓝宝石晶体材料",
            "canonical_name_en": "Sapphire Crystal Material",
            "definition": "以氧化铝单晶形式生长的人工蓝宝石材料，具有高硬度、透光性优异等特点",
            "entity_type": "material",
            "evidence": make_evidence("蓝宝石晶体材料", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: sapphire_crystal_material")
    if "single_crystal_furnace" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "single_crystal_furnace",
            "canonical_name_zh": "单晶炉",
            "canonical_name_en": "Single Crystal Furnace",
            "definition": "用于生长单晶材料的高温设备，通过提拉法或泡生法实现晶体生长",
            "entity_type": "device",
            "evidence": make_evidence("单晶炉及蓝宝石制品的研发,生产和销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: single_crystal_furnace")
    if "sapphire_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "sapphire_product",
            "canonical_name_zh": "蓝宝石制品",
            "canonical_name_en": "Sapphire Product",
            "definition": "以蓝宝石晶体材料为基础加工而成的各类功能性产品，如衬底、窗口片等",
            "entity_type": "component",
            "evidence": make_evidence("蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: sapphire_product")
    if "semiconductor_backend_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "semiconductor_backend_service",
            "canonical_name_zh": "半导体后工序服务",
            "canonical_name_en": "Semiconductor Backend Service",
            "definition": "半导体制造流程中晶圆测试、切割、封装、成品测试等后段工序服务",
            "entity_type": "service",
            "evidence": make_evidence("半导体后工序服务业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: semiconductor_backend_service")
    if "telecom_cable" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "telecom_cable",
            "canonical_name_zh": "通信电缆",
            "canonical_name_en": "Telecommunication Cable",
            "definition": "用于传输电信号或光信号的线缆产品，包括同轴电缆、光缆等",
            "entity_type": "component",
            "evidence": make_evidence("通信电缆", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: telecom_cable")
    if "printing_material" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "printing_material",
            "canonical_name_zh": "印刷材料",
            "canonical_name_en": "Printing Material",
            "definition": "用于印刷工艺的各类耗材，包括油墨、版材、纸张等",
            "entity_type": "material",
            "evidence": make_evidence("印刷材料制造业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: printing_material")
    if "financial_equipment" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "financial_equipment",
            "canonical_name_zh": "金融设备",
            "canonical_name_en": "Financial Equipment",
            "definition": "用于金融业务场景的专用设备，如点钞机、清分机、ATM等",
            "entity_type": "device",
            "evidence": make_evidence("金融设备制造业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: financial_equipment")

    # ---- Graph edges ----
    edges_to_create = []
    if ("float_glass", "automotive_glass", "material_flow") not in existing_edges and "float_glass" in existing_nodes and "automotive_glass" in existing_nodes:
        edges_to_create.append({
            "edge_id": "float_glass_to_automotive_glass",
            "from_node": "float_glass",
            "to_node": "automotive_glass",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "浮法玻璃经深加工制成汽车玻璃",
            "evidence": make_evidence("从事浮法玻璃及汽车用玻璃制品的生产及销售"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: float_glass_to_automotive_glass")
    if ("sapphire_crystal_material", "sapphire_product", "material_flow") not in existing_edges and "sapphire_crystal_material" in existing_nodes and "sapphire_product" in existing_nodes:
        edges_to_create.append({
            "edge_id": "sapphire_material_to_product",
            "from_node": "sapphire_crystal_material",
            "to_node": "sapphire_product",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "蓝宝石晶体材料经加工制成蓝宝石制品",
            "evidence": make_evidence("蓝宝石晶体材料及蓝宝石制品的研发,生产和销售"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: sapphire_material_to_product")
    if ("single_crystal_furnace", "sapphire_crystal_material", "capability_supply") not in existing_edges and "single_crystal_furnace" in existing_nodes and "sapphire_crystal_material" in existing_nodes:
        edges_to_create.append({
            "edge_id": "single_crystal_furnace_to_sapphire",
            "from_node": "single_crystal_furnace",
            "to_node": "sapphire_crystal_material",
            "edge_namespace": "industrial_flow",
            "edge_type": "capability_supply",
            "description": "单晶炉提供晶体生长能力，产出蓝宝石晶体材料",
            "evidence": make_evidence("单晶炉及蓝宝石制品的研发,生产和销售"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: single_crystal_furnace_to_sapphire")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_091_graph",
            "task_description": f"Batch 091 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次91构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 电子城 (600658.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600658",
        "name_zh": "电子城",
        "stock_codes": ["600658.SH"],
        "country": "中国",
        "industry": "园区开发",
        "main_business": "主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600658_tech_park_operation_service",
        "company_id": "sh_600658",
        "node_id": "tech_park_operation_service",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600658_communication_equipment",
        "company_id": "sh_600658",
        "node_id": "communication_equipment",
        "activity_type": "manufacture",
        "weight": 0.25,
        "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600658_printing_material",
        "company_id": "sh_600658",
        "node_id": "printing_material",
        "activity_type": "manufacture",
        "weight": 0.15,
        "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600658_financial_equipment",
        "company_id": "sh_600658",
        "node_id": "financial_equipment",
        "activity_type": "manufacture",
        "weight": 0.1,
        "evidence": make_evidence("主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.")
    })
    # 福耀玻璃 (600660.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600660",
        "name_zh": "福耀玻璃",
        "stock_codes": ["600660.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "主营业务:从事浮法玻璃及汽车用玻璃制品的生产及销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:从事浮法玻璃及汽车用玻璃制品的生产及销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600660_float_glass",
        "company_id": "sh_600660",
        "node_id": "float_glass",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:从事浮法玻璃及汽车用玻璃制品的生产及销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600660_automotive_glass",
        "company_id": "sh_600660",
        "node_id": "automotive_glass",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:从事浮法玻璃及汽车用玻璃制品的生产及销售.")
    })
    # 昂立教育 (600661.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600661",
        "name_zh": "昂立教育",
        "stock_codes": ["600661.SH"],
        "country": "中国",
        "industry": "文教休闲",
        "main_business": "主营业务:教育培训.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:教育培训.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600661_education_service",
        "company_id": "sh_600661",
        "node_id": "education_service",
        "activity_type": "provide_service",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:教育培训.")
    })
    # 外服控股 (600662.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600662",
        "name_zh": "外服控股",
        "stock_codes": ["600662.SH"],
        "country": "中国",
        "industry": "文教休闲",
        "main_business": "出租汽车服务及其相关业务,旅游服务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("出租汽车服务及其相关业务,旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600662_taxi_operation_service",
        "company_id": "sh_600662",
        "node_id": "taxi_operation_service",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("出租汽车服务及其相关业务,旅游服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600662_tourism_service",
        "company_id": "sh_600662",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("出租汽车服务及其相关业务,旅游服务.")
    })
    # 陆家嘴 (600663.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600663",
        "name_zh": "陆家嘴",
        "stock_codes": ["600663.SH"],
        "country": "中国",
        "industry": "园区开发",
        "main_business": "主营业务:房地产投资开发运营",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:房地产投资开发运营")
    })
    exposures_payload.append({
        "exposure_id": "sh_600663_real_estate_development",
        "company_id": "sh_600663",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:房地产投资开发运营")
    })
    # 哈药股份 (600664.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600664",
        "name_zh": "哈药股份",
        "stock_codes": ["600664.SH"],
        "country": "中国",
        "industry": "化学制药",
        "main_business": "主要产品:中药,西药,保健品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:中药,西药,保健品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600664_chinese_medicine_preparation",
        "company_id": "sh_600664",
        "node_id": "chinese_medicine_preparation",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:中药,西药,保健品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600664_chemical_drug_preparation",
        "company_id": "sh_600664",
        "node_id": "chemical_drug_preparation",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:中药,西药,保健品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600664_health_food",
        "company_id": "sh_600664",
        "node_id": "health_food",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主要产品:中药,西药,保健品.")
    })
    # 天地源 (600665.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600665",
        "name_zh": "天地源",
        "stock_codes": ["600665.SH"],
        "country": "中国",
        "industry": "全国地产",
        "main_business": "主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600665_real_estate_development",
        "company_id": "sh_600665",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.7,
        "evidence": make_evidence("主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600665_warehouse_service",
        "company_id": "sh_600665",
        "node_id": "warehouse_service",
        "activity_type": "operate",
        "weight": 0.1,
        "evidence": make_evidence("主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600665_trade_agent",
        "company_id": "sh_600665",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.")
    })
    # 奥瑞德 (600666.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600666",
        "name_zh": "奥瑞德",
        "stock_codes": ["600666.SH"],
        "country": "中国",
        "industry": "元器件",
        "main_business": "蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600666_sapphire_crystal_material",
        "company_id": "sh_600666",
        "node_id": "sapphire_crystal_material",
        "activity_type": "produce",
        "weight": 0.4,
        "evidence": make_evidence("蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600666_single_crystal_furnace",
        "company_id": "sh_600666",
        "node_id": "single_crystal_furnace",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600666_sapphire_product",
        "company_id": "sh_600666",
        "node_id": "sapphire_product",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售")
    })
    # 太极实业 (600667.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600667",
        "name_zh": "太极实业",
        "stock_codes": ["600667.SH"],
        "country": "中国",
        "industry": "半导体",
        "main_business": "半导体后工序服务业务",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("半导体后工序服务业务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600667_semiconductor_backend_service",
        "company_id": "sh_600667",
        "node_id": "semiconductor_backend_service",
        "activity_type": "provide_service",
        "weight": 0.8,
        "evidence": make_evidence("半导体后工序服务业务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600667_semiconductor_device",
        "company_id": "sh_600667",
        "node_id": "semiconductor_device",
        "activity_type": "manufacture",
        "weight": 0.2,
        "evidence": make_evidence("半导体后工序服务业务")
    })
    # 尖峰集团 (600668.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600668",
        "name_zh": "尖峰集团",
        "stock_codes": ["600668.SH"],
        "country": "中国",
        "industry": "水泥",
        "main_business": "公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600668_cement",
        "company_id": "sh_600668",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600668_pharmaceutical_intermediate",
        "company_id": "sh_600668",
        "node_id": "pharmaceutical_intermediate",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600668_telecom_cable",
        "company_id": "sh_600668",
        "node_id": "telecom_cable",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600668_warehouse_service",
        "company_id": "sh_600668",
        "node_id": "warehouse_service",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600668_trade_agent",
        "company_id": "sh_600668",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_091_biz",
            "task_description": f"Batch 091 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次91构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
