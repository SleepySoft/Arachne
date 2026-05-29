#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 96."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_096.json"

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
    if "vacuum_cleaner" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "vacuum_cleaner",
            "canonical_name_zh": "吸尘器",
            "canonical_name_en": "Vacuum Cleaner",
            "definition": "利用负压原理吸取灰尘和杂物的家用或商用清洁电器设备",
            "entity_type": "device",
            "evidence": make_evidence("吸尘器", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: vacuum_cleaner")
    if "pva" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "pva",
            "canonical_name_zh": "聚乙烯醇",
            "canonical_name_en": "Polyvinyl Alcohol",
            "definition": "一种水溶性合成高分子材料，由聚醋酸乙烯酯醇解制得，广泛用于纺织浆料、粘合剂、涂料等",
            "entity_type": "material",
            "evidence": make_evidence("聚乙烯醇", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: pva")
    if "vinyl_acetate" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "vinyl_acetate",
            "canonical_name_zh": "醋酸乙烯",
            "canonical_name_en": "Vinyl Acetate",
            "definition": "一种重要的有机化工原料，主要用于生产聚乙烯醇、聚醋酸乙烯酯乳液和乙烯-醋酸乙烯共聚物",
            "entity_type": "material",
            "evidence": make_evidence("醋酸乙烯", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: vinyl_acetate")
    if "coal_tar" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "coal_tar",
            "canonical_name_zh": "煤焦油",
            "canonical_name_en": "Coal Tar",
            "definition": "煤干馏过程中产生的黑色粘稠液体，是重要的化工原料，可提取酚类、萘、蒽等多种化学品",
            "entity_type": "material",
            "evidence": make_evidence("煤焦油及深加工产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: coal_tar")
    if "ammonium_phosphate" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ammonium_phosphate",
            "canonical_name_zh": "磷铵",
            "canonical_name_en": "Ammonium Phosphate",
            "definition": "磷酸铵类肥料的总称，包括磷酸一铵和磷酸二铵，是重要的氮磷复合肥料",
            "entity_type": "material",
            "evidence": make_evidence("磷铵", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ammonium_phosphate")
    if "bromine" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "bromine",
            "canonical_name_zh": "溴素",
            "canonical_name_en": "Bromine",
            "definition": "一种卤族元素，常温下为红棕色液体，广泛用于阻燃剂、医药中间体、农药和油田化学品",
            "entity_type": "material",
            "evidence": make_evidence("溴素及溴系列", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: bromine")
    if "intelligent_security_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "intelligent_security_system",
            "canonical_name_zh": "智能安防系统",
            "canonical_name_en": "Intelligent Security System",
            "definition": "综合运用视频监控、人脸识别、行为分析、物联网传感器等技术的安全防护系统",
            "entity_type": "system",
            "evidence": make_evidence("智能安防", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: intelligent_security_system")
    if "intelligent_transport_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "intelligent_transport_system",
            "canonical_name_zh": "智能交通系统",
            "canonical_name_en": "Intelligent Transport System",
            "definition": "利用信息技术、通信技术、传感器技术和控制技术对交通运输系统进行智能化管理和服务的综合系统",
            "entity_type": "system",
            "evidence": make_evidence("智能交通", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: intelligent_transport_system")
    if "telecom_value_added_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "telecom_value_added_service",
            "canonical_name_zh": "通信增值服务",
            "canonical_name_en": "Telecom Value-Added Service",
            "definition": "在基础通信服务之上提供的附加信息服务，如短信、彩铃、位置服务、移动支付等",
            "entity_type": "service",
            "evidence": make_evidence("通信增值", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: telecom_value_added_service")
    if "it_integrated_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "it_integrated_service",
            "canonical_name_zh": "IT综合服务",
            "canonical_name_en": "IT Integrated Service",
            "definition": "为客户提供信息系统规划、建设、运维、优化及技术支持的全生命周期综合服务",
            "entity_type": "service",
            "evidence": make_evidence("IT综合服务等", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: it_integrated_service")
    if "investment_management_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "investment_management_service",
            "canonical_name_zh": "投资管理服务",
            "canonical_name_en": "Investment Management Service",
            "definition": "为客户提供资产配置、投资组合管理、风险评估及财务规划的专业金融服务",
            "entity_type": "service",
            "evidence": make_evidence("投资管理", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: investment_management_service")

    # ---- Graph edges ----
    edges_to_create = []
    if ("vinyl_acetate", "pva", "material_flow") not in existing_edges and "vinyl_acetate" in existing_nodes and "pva" in existing_nodes:
        edges_to_create.append({
            "edge_id": "vinyl_acetate_to_pva",
            "from_node": "vinyl_acetate",
            "to_node": "pva",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "醋酸乙烯经聚合和醇解反应可制得聚乙烯醇",
            "evidence": make_evidence("聚乙烯醇,醋酸乙烯"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: vinyl_acetate_to_pva")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_096_graph",
            "task_description": f"Batch 096 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次96构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 中交设计 (600720.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600720",
        "name_zh": "中交设计",
        "stock_codes": ["600720.SH"],
        "country": "中国",
        "industry": "建筑工程",
        "main_business": "主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600720_cement",
        "company_id": "sh_600720",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.4,
        "evidence": make_evidence("主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600720_ready_mixed_concrete",
        "company_id": "sh_600720",
        "node_id": "ready_mixed_concrete",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600720_cement_product",
        "company_id": "sh_600720",
        "node_id": "cement_product",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.")
    })
    # 百花医药 (600721.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600721",
        "name_zh": "百花医药",
        "stock_codes": ["600721.SH"],
        "country": "中国",
        "industry": "生物制药",
        "main_business": "能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600721_trade_agent",
        "company_id": "sh_600721",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.3,
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600721_real_estate_development",
        "company_id": "sh_600721",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600721_electromechanical_product",
        "company_id": "sh_600721",
        "node_id": "electromechanical_product",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600721_metal_material",
        "company_id": "sh_600721",
        "node_id": "metal_material",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600721_agricultural_product",
        "company_id": "sh_600721",
        "node_id": "agricultural_product",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.")
    })
    # 金牛化工 (600722.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600722",
        "name_zh": "金牛化工",
        "stock_codes": ["600722.SH"],
        "country": "中国",
        "industry": "化工原料",
        "main_business": "树脂,烧碱,水泥.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("树脂,烧碱,水泥.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600722_synthetic_resin",
        "company_id": "sh_600722",
        "node_id": "synthetic_resin",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("树脂,烧碱,水泥.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600722_soda_ash",
        "company_id": "sh_600722",
        "node_id": "soda_ash",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("树脂,烧碱,水泥.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600722_cement",
        "company_id": "sh_600722",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("树脂,烧碱,水泥.")
    })
    # 宁波富达 (600724.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600724",
        "name_zh": "宁波富达",
        "stock_codes": ["600724.SH"],
        "country": "中国",
        "industry": "综合类",
        "main_business": "吸尘器,小家电,水泥,自来水.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("吸尘器,小家电,水泥,自来水.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600724_vacuum_cleaner",
        "company_id": "sh_600724",
        "node_id": "vacuum_cleaner",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("吸尘器,小家电,水泥,自来水.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600724_small_home_appliance",
        "company_id": "sh_600724",
        "node_id": "small_home_appliance",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("吸尘器,小家电,水泥,自来水.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600724_cement",
        "company_id": "sh_600724",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("吸尘器,小家电,水泥,自来水.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600724_tap_water_supply",
        "company_id": "sh_600724",
        "node_id": "tap_water_supply",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("吸尘器,小家电,水泥,自来水.")
    })
    # 云维股份 (600725.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600725",
        "name_zh": "云维股份",
        "stock_codes": ["600725.SH"],
        "country": "中国",
        "industry": "商贸代理",
        "main_business": "聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_pva",
        "company_id": "sh_600725",
        "node_id": "pva",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_vinyl_acetate",
        "company_id": "sh_600725",
        "node_id": "vinyl_acetate",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_calcium_carbide",
        "company_id": "sh_600725",
        "node_id": "calcium_carbide",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_coke",
        "company_id": "sh_600725",
        "node_id": "coke",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_methanol",
        "company_id": "sh_600725",
        "node_id": "methanol",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_coal_tar",
        "company_id": "sh_600725",
        "node_id": "coal_tar",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_soda_ash",
        "company_id": "sh_600725",
        "node_id": "soda_ash",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_ammonium_chloride",
        "company_id": "sh_600725",
        "node_id": "ammonium_chloride",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_cement",
        "company_id": "sh_600725",
        "node_id": "cement",
        "activity_type": "procure",
        "weight": 0.05,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600725_trade_agent",
        "company_id": "sh_600725",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.")
    })
    # 华电能源 (600726.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600726",
        "name_zh": "华电能源",
        "stock_codes": ["600726.SH"],
        "country": "中国",
        "industry": "火力发电",
        "main_business": "主要产品:电力,热力.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:电力,热力.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600726_electricity_power",
        "company_id": "sh_600726",
        "node_id": "electricity_power",
        "activity_type": "produce",
        "weight": 0.6,
        "evidence": make_evidence("主要产品:电力,热力.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600726_heat_supply",
        "company_id": "sh_600726",
        "node_id": "heat_supply",
        "activity_type": "produce",
        "weight": 0.4,
        "evidence": make_evidence("主要产品:电力,热力.")
    })
    # 鲁北化工 (600727.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600727",
        "name_zh": "鲁北化工",
        "stock_codes": ["600727.SH"],
        "country": "中国",
        "industry": "化工原料",
        "main_business": "磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_ammonium_phosphate",
        "company_id": "sh_600727",
        "node_id": "ammonium_phosphate",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_compound_fertilizer",
        "company_id": "sh_600727",
        "node_id": "compound_fertilizer",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_cement",
        "company_id": "sh_600727",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_bromine",
        "company_id": "sh_600727",
        "node_id": "bromine",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_chlor_alkali_product",
        "company_id": "sh_600727",
        "node_id": "chlor_alkali_product",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600727_electricity_power",
        "company_id": "sh_600727",
        "node_id": "electricity_power",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.")
    })
    # 佳都科技 (600728.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600728",
        "name_zh": "佳都科技",
        "stock_codes": ["600728.SH"],
        "country": "中国",
        "industry": "软件服务",
        "main_business": "主营业务:智能安防,智能交通,通信增值,IT综合服务等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:智能安防,智能交通,通信增值,IT综合服务等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600728_intelligent_security_system",
        "company_id": "sh_600728",
        "node_id": "intelligent_security_system",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("主营业务:智能安防,智能交通,通信增值,IT综合服务等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600728_intelligent_transport_system",
        "company_id": "sh_600728",
        "node_id": "intelligent_transport_system",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("主营业务:智能安防,智能交通,通信增值,IT综合服务等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600728_telecom_value_added_service",
        "company_id": "sh_600728",
        "node_id": "telecom_value_added_service",
        "activity_type": "provide_service",
        "weight": 0.2,
        "evidence": make_evidence("主营业务:智能安防,智能交通,通信增值,IT综合服务等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600728_it_integrated_service",
        "company_id": "sh_600728",
        "node_id": "it_integrated_service",
        "activity_type": "provide_service",
        "weight": 0.2,
        "evidence": make_evidence("主营业务:智能安防,智能交通,通信增值,IT综合服务等.")
    })
    # 重百集团 (600729.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600729",
        "name_zh": "重百集团",
        "stock_codes": ["600729.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "商品零售,商品批发.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("商品零售,商品批发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600729_department_store",
        "company_id": "sh_600729",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("商品零售,商品批发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600729_trade_agent",
        "company_id": "sh_600729",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.5,
        "evidence": make_evidence("商品零售,商品批发.")
    })
    # *ST高科 (600730.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600730",
        "name_zh": "*ST高科",
        "stock_codes": ["600730.SH"],
        "country": "中国",
        "industry": "文教休闲",
        "main_business": "教育,仓储,房地产,投资管理.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("教育,仓储,房地产,投资管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600730_education_service",
        "company_id": "sh_600730",
        "node_id": "education_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("教育,仓储,房地产,投资管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600730_warehouse_service",
        "company_id": "sh_600730",
        "node_id": "warehouse_service",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("教育,仓储,房地产,投资管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600730_real_estate_development",
        "company_id": "sh_600730",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("教育,仓储,房地产,投资管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600730_investment_management_service",
        "company_id": "sh_600730",
        "node_id": "investment_management_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("教育,仓储,房地产,投资管理.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_096_biz",
            "task_description": f"Batch 096 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次96构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
