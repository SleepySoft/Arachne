#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 95."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_095.json"

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
    if "diesel_generator_set" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "diesel_generator_set",
            "canonical_name_zh": "柴油发电机组",
            "canonical_name_en": "Diesel Generator Set",
            "definition": "以柴油发动机为动力驱动同步发电机发电的成套发电设备",
            "entity_type": "system",
            "evidence": make_evidence("柴油发电机组", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: diesel_generator_set")
    if "outdoor_power_equipment" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "outdoor_power_equipment",
            "canonical_name_zh": "户外动力设备",
            "canonical_name_en": "Outdoor Power Equipment",
            "definition": "用于户外作业场景的移动式动力机械设备，包括发电机、水泵、割草机等",
            "entity_type": "system",
            "evidence": make_evidence("户外动力设备(OPE)", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: outdoor_power_equipment")
    if "pv_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "pv_product",
            "canonical_name_zh": "光伏产品",
            "canonical_name_en": "Photovoltaic Product",
            "definition": "利用太阳能光伏发电技术制造的各类产品，包括光伏组件、逆变器、支架系统等",
            "entity_type": "material",
            "evidence": make_evidence("清洁能源(含光伏产品)", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: pv_product")
    if "nonferrous_mining_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "nonferrous_mining_service",
            "canonical_name_zh": "有色金属采选服务",
            "canonical_name_en": "Nonferrous Mining Service",
            "definition": "为有色金属矿山提供勘探、开采、选矿等专业技术服务",
            "entity_type": "service",
            "evidence": make_evidence("有色金属采选", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: nonferrous_mining_service")
    if "metal_financial_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "metal_financial_service",
            "canonical_name_zh": "金属金融服务",
            "canonical_name_en": "Metal Financial Service",
            "definition": "围绕金属产业链提供的供应链金融、套期保值、贸易融资等金融服务",
            "entity_type": "service",
            "evidence": make_evidence("金属金融服务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: metal_financial_service")
    if "pharmaceutical_manufacturing" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "pharmaceutical_manufacturing",
            "canonical_name_zh": "医药制造服务",
            "canonical_name_en": "Pharmaceutical Manufacturing Service",
            "definition": "从事药品原料药及制剂的研发、生产和代加工制造服务",
            "entity_type": "service",
            "evidence": make_evidence("流通业,制造业", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: pharmaceutical_manufacturing")
    if "strontium_compound" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "strontium_compound",
            "canonical_name_zh": "锶化合物",
            "canonical_name_en": "Strontium Compound",
            "definition": "以锶元素为核心的各类化合物产品，包括碳酸锶、硝酸锶、氯化锶等",
            "entity_type": "material",
            "evidence": make_evidence("锶系列产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: strontium_compound")
    if "automotive_body_part" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "automotive_body_part",
            "canonical_name_zh": "汽车车身零部件",
            "canonical_name_en": "Automotive Body Part",
            "definition": "构成汽车车身结构的各种冲压件、覆盖件及内外饰零部件",
            "entity_type": "component",
            "evidence": make_evidence("汽车车身零部件", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: automotive_body_part")
    if "digital_medical_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "digital_medical_system",
            "canonical_name_zh": "数字医疗系统",
            "canonical_name_en": "Digital Medical System",
            "definition": "集成医学影像、临床信息、远程诊疗等功能的数字化医疗信息化系统",
            "entity_type": "system",
            "evidence": make_evidence("数字医疗", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: digital_medical_system")
    if "heat_supply" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "heat_supply",
            "canonical_name_zh": "热力供应服务",
            "canonical_name_en": "Heat Supply Service",
            "definition": "通过热电联产或区域锅炉房向用户供应蒸汽和热水的公用事业服务",
            "entity_type": "service",
            "evidence": make_evidence("热力", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: heat_supply")
    if "container_transport_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "container_transport_service",
            "canonical_name_zh": "集装箱运输服务",
            "canonical_name_en": "Container Transport Service",
            "definition": "利用标准化集装箱进行货物陆海联运、堆存、装卸及多式联运的服务",
            "entity_type": "service",
            "evidence": make_evidence("集装箱搬运,拆装箱及相关业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: container_transport_service")

    # ---- Graph edges ----
    edges_to_create = []
    if ("diesel_generator_set", "ship", "composition") not in existing_edges and "diesel_generator_set" in existing_nodes and "ship" in existing_nodes:
        edges_to_create.append({
            "edge_id": "diesel_generator_to_ship",
            "from_node": "diesel_generator_set",
            "to_node": "ship",
            "edge_namespace": "industrial_flow",
            "edge_type": "composition",
            "description": "柴油发电机组可作为船舶辅助发电设备",
            "evidence": make_evidence("船舶制造与航运,柴油发电机组"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: diesel_generator_to_ship")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_095_graph",
            "task_description": f"Batch 095 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次95构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 苏美达 (600710.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600710",
        "name_zh": "苏美达",
        "stock_codes": ["600710.SH"],
        "country": "中国",
        "industry": "商贸代理",
        "main_business": "公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).")
    })
    exposures_payload.append({
        "exposure_id": "sh_600710_shipbuilding",
        "company_id": "sh_600710",
        "node_id": "shipbuilding",
        "activity_type": "manufacture",
        "weight": 0.25,
        "evidence": make_evidence("公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).")
    })
    exposures_payload.append({
        "exposure_id": "sh_600710_diesel_generator_set",
        "company_id": "sh_600710",
        "node_id": "diesel_generator_set",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).")
    })
    exposures_payload.append({
        "exposure_id": "sh_600710_outdoor_power_equipment",
        "company_id": "sh_600710",
        "node_id": "outdoor_power_equipment",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).")
    })
    exposures_payload.append({
        "exposure_id": "sh_600710_pv_product",
        "company_id": "sh_600710",
        "node_id": "pv_product",
        "activity_type": "procure",
        "weight": 0.25,
        "evidence": make_evidence("公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).")
    })
    # 盛屯矿业 (600711.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600711",
        "name_zh": "盛屯矿业",
        "stock_codes": ["600711.SH"],
        "country": "中国",
        "industry": "小金属",
        "main_business": "主要业务为有色金属采选及综合贸易业务金属金融服务",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务为有色金属采选及综合贸易业务金属金融服务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600711_nonferrous_mining_service",
        "company_id": "sh_600711",
        "node_id": "nonferrous_mining_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("主要业务为有色金属采选及综合贸易业务金属金融服务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600711_trade_agent",
        "company_id": "sh_600711",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.25,
        "evidence": make_evidence("主要业务为有色金属采选及综合贸易业务金属金融服务")
    })
    exposures_payload.append({
        "exposure_id": "sh_600711_metal_financial_service",
        "company_id": "sh_600711",
        "node_id": "metal_financial_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("主要业务为有色金属采选及综合贸易业务金属金融服务")
    })
    # 南宁百货 (600712.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600712",
        "name_zh": "南宁百货",
        "stock_codes": ["600712.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "主营业务为批发和零售贸易.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务为批发和零售贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600712_department_store",
        "company_id": "sh_600712",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("主营业务为批发和零售贸易.")
    })
    # 南京医药 (600713.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600713",
        "name_zh": "南京医药",
        "stock_codes": ["600713.SH"],
        "country": "中国",
        "industry": "医药商业",
        "main_business": "流通业,制造业.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("流通业,制造业.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600713_pharmaceutical_distribution",
        "company_id": "sh_600713",
        "node_id": "pharmaceutical_distribution",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("流通业,制造业.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600713_pharmaceutical_manufacturing",
        "company_id": "sh_600713",
        "node_id": "pharmaceutical_manufacturing",
        "activity_type": "manufacture",
        "weight": 0.5,
        "evidence": make_evidence("流通业,制造业.")
    })
    # 金瑞矿业 (600714.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600714",
        "name_zh": "金瑞矿业",
        "stock_codes": ["600714.SH"],
        "country": "中国",
        "industry": "化工原料",
        "main_business": "锶系列产品的研究,生产,开发,加工与销售.煤炭的生产与销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("锶系列产品的研究,生产,开发,加工与销售.煤炭的生产与销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600714_strontium_compound",
        "company_id": "sh_600714",
        "node_id": "strontium_compound",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("锶系列产品的研究,生产,开发,加工与销售.煤炭的生产与销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600714_coal",
        "company_id": "sh_600714",
        "node_id": "coal",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("锶系列产品的研究,生产,开发,加工与销售.煤炭的生产与销售.")
    })
    # 文投控股 (600715.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600715",
        "name_zh": "文投控股",
        "stock_codes": ["600715.SH"],
        "country": "中国",
        "industry": "影视音像",
        "main_business": "汽车车身零部件.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("汽车车身零部件.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600715_film_tv_production_service",
        "company_id": "sh_600715",
        "node_id": "film_tv_production_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("汽车车身零部件.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600715_automotive_body_part",
        "company_id": "sh_600715",
        "node_id": "automotive_body_part",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("汽车车身零部件.")
    })
    # 凤凰股份 (600716.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600716",
        "name_zh": "凤凰股份",
        "stock_codes": ["600716.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "房地产投资及其他实业投资",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产投资及其他实业投资")
    })
    exposures_payload.append({
        "exposure_id": "sh_600716_real_estate_development",
        "company_id": "sh_600716",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("房地产投资及其他实业投资")
    })
    # 天津港 (600717.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600717",
        "name_zh": "天津港",
        "stock_codes": ["600717.SH"],
        "country": "中国",
        "industry": "港口",
        "main_business": "主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_warehouse_service",
        "company_id": "sh_600717",
        "node_id": "warehouse_service",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_logistics_service",
        "company_id": "sh_600717",
        "node_id": "logistics_service",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_port_operation_service",
        "company_id": "sh_600717",
        "node_id": "port_operation_service",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_container_transport_service",
        "company_id": "sh_600717",
        "node_id": "container_transport_service",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_freight_forwarding_service",
        "company_id": "sh_600717",
        "node_id": "freight_forwarding_service",
        "activity_type": "provide_service",
        "weight": 0.15,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    exposures_payload.append({
        "exposure_id": "sh_600717_road_transport_vehicle",
        "company_id": "sh_600717",
        "node_id": "road_transport_vehicle",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询")
    })
    # 东软集团 (600718.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600718",
        "name_zh": "东软集团",
        "stock_codes": ["600718.SH"],
        "country": "中国",
        "industry": "软件服务",
        "main_business": "主营业务:软件及系统集成,数字医疗.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:软件及系统集成,数字医疗.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600718_software_development_service",
        "company_id": "sh_600718",
        "node_id": "software_development_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:软件及系统集成,数字医疗.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600718_digital_medical_system",
        "company_id": "sh_600718",
        "node_id": "digital_medical_system",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:软件及系统集成,数字医疗.")
    })
    # 大连热电 (600719.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600719",
        "name_zh": "大连热电",
        "stock_codes": ["600719.SH"],
        "country": "中国",
        "industry": "供气供热",
        "main_business": "电力,热力.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("电力,热力.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600719_electricity_power",
        "company_id": "sh_600719",
        "node_id": "electricity_power",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("电力,热力.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600719_heat_supply",
        "company_id": "sh_600719",
        "node_id": "heat_supply",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("电力,热力.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_095_biz",
            "task_description": f"Batch 095 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次95构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
