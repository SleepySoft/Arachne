#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 97."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_097.json"

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
    if "pesticide_formulation" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "pesticide_formulation",
            "canonical_name_zh": "农药制剂",
            "canonical_name_en": "Pesticide Formulation",
            "definition": "将农药原药与助剂、溶剂等配制成可供直接使用的农药产品，如乳油、可湿性粉剂、悬浮剂等",
            "entity_type": "material",
            "evidence": make_evidence("农药原药,农药制剂", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: pesticide_formulation")
    if "nev_charging_facility" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "nev_charging_facility",
            "canonical_name_zh": "新能源汽车充电设施",
            "canonical_name_en": "NEV Charging Facility",
            "definition": "为新能源汽车提供电能补充的设施，包括充电桩、充电站、换电站及配套配电系统",
            "entity_type": "infrastructure",
            "evidence": make_evidence("销售新能源汽车充电设施", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: nev_charging_facility")
    if "nev_power_module" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "nev_power_module",
            "canonical_name_zh": "新能源汽车动力模块",
            "canonical_name_en": "NEV Power Module",
            "definition": "新能源汽车的核心动力单元，包括电池系统、电机系统和电控系统的集成模块",
            "entity_type": "subsystem",
            "evidence": make_evidence("装配新能源汽车动力模块", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: nev_power_module")
    if "iot_security_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "iot_security_system",
            "canonical_name_zh": "物联网安防系统",
            "canonical_name_en": "IoT Security System",
            "definition": "基于物联网技术的周界防护和入侵检测系统，包括传感器网络、视频监控和报警联动",
            "entity_type": "system",
            "evidence": make_evidence("物联网周界安防业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: iot_security_system")
    if "hair_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "hair_product",
            "canonical_name_zh": "发制品",
            "canonical_name_en": "Hair Product",
            "definition": "以人发或化纤为原料制成的假发、发套、发片、接发等美发产品",
            "entity_type": "material",
            "evidence": make_evidence("发制品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: hair_product")
    if "tin_material" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "tin_material",
            "canonical_name_zh": "锡材料",
            "canonical_name_en": "Tin Material",
            "definition": "以锡金属为基础的材料产品，包括锡锭、锡合金、锡化合物及锡焊料等",
            "entity_type": "material",
            "evidence": make_evidence("锡材料加工", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: tin_material")
    if "catering_entertainment_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "catering_entertainment_service",
            "canonical_name_zh": "餐饮娱乐服务",
            "canonical_name_en": "Catering Entertainment Service",
            "definition": "集餐饮服务和娱乐休闲于一体的商业服务，包括餐厅、酒吧、KTV、影院等",
            "entity_type": "service",
            "evidence": make_evidence("商品零售,餐饮娱乐", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: catering_entertainment_service")
    if "financial_investment_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "financial_investment_service",
            "canonical_name_zh": "金融投资服务",
            "canonical_name_en": "Financial Investment Service",
            "definition": "为客户提供证券、基金、信托、股权投资及资产管理等金融投资专业服务",
            "entity_type": "service",
            "evidence": make_evidence("金融投资", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: financial_investment_service")
    if "energy_development_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "energy_development_service",
            "canonical_name_zh": "能源开发服务",
            "canonical_name_en": "Energy Development Service",
            "definition": "从事油气、煤炭、新能源等能源资源的勘探、开采、加工及技术服务",
            "entity_type": "service",
            "evidence": make_evidence("能源开发", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: energy_development_service")
    if "coking_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "coking_product",
            "canonical_name_zh": "焦化产品",
            "canonical_name_en": "Coking Product",
            "definition": "以煤为原料经高温干馏得到的各类产品，包括焦炭、焦炉煤气、煤焦油、粗苯等",
            "entity_type": "material",
            "evidence": make_evidence("焦炭,其他化工产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: coking_product")

    # ---- Graph edges ----
    edges_to_create = []


    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_097_graph",
            "task_description": f"Batch 097 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次97构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 湖南海利 (600731.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600731",
        "name_zh": "湖南海利",
        "stock_codes": ["600731.SH"],
        "country": "中国",
        "industry": "农药化肥",
        "main_business": "农药原药,农药制剂,精细化工产品,泵.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("农药原药,农药制剂,精细化工产品,泵.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600731_pesticide",
        "company_id": "sh_600731",
        "node_id": "pesticide",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("农药原药,农药制剂,精细化工产品,泵.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600731_pesticide_intermediate",
        "company_id": "sh_600731",
        "node_id": "pesticide_intermediate",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("农药原药,农药制剂,精细化工产品,泵.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600731_pesticide_formulation",
        "company_id": "sh_600731",
        "node_id": "pesticide_formulation",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("农药原药,农药制剂,精细化工产品,泵.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600731_pump",
        "company_id": "sh_600731",
        "node_id": "pump",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("农药原药,农药制剂,精细化工产品,泵.")
    })
    # 爱旭股份 (600732.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600732",
        "name_zh": "爱旭股份",
        "stock_codes": ["600732.SH"],
        "country": "中国",
        "industry": "电气设备",
        "main_business": "商品房销售,商品房出租.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("商品房销售,商品房出租.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600732_real_estate_development",
        "company_id": "sh_600732",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("商品房销售,商品房出租.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600732_commercial_housing_rental",
        "company_id": "sh_600732",
        "node_id": "commercial_housing_rental",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("商品房销售,商品房出租.")
    })
    # 北汽蓝谷 (600733.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600733",
        "name_zh": "北汽蓝谷",
        "stock_codes": ["600733.SH"],
        "country": "中国",
        "industry": "汽车整车",
        "main_business": "装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600733_new_energy_vehicle",
        "company_id": "sh_600733",
        "node_id": "new_energy_vehicle",
        "activity_type": "manufacture",
        "weight": 0.35,
        "evidence": make_evidence("装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600733_nev_power_module",
        "company_id": "sh_600733",
        "node_id": "nev_power_module",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600733_nev_charging_facility",
        "company_id": "sh_600733",
        "node_id": "nev_charging_facility",
        "activity_type": "procure",
        "weight": 0.3,
        "evidence": make_evidence("装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.")
    })
    # *ST实达 (600734.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600734",
        "name_zh": "*ST实达",
        "stock_codes": ["600734.SH"],
        "country": "中国",
        "industry": "软件服务",
        "main_business": "移动通讯智能终端业务;物联网周界安防业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("移动通讯智能终端业务;物联网周界安防业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600734_mobile_terminal",
        "company_id": "sh_600734",
        "node_id": "mobile_terminal",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("移动通讯智能终端业务;物联网周界安防业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600734_iot_security_system",
        "company_id": "sh_600734",
        "node_id": "iot_security_system",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("移动通讯智能终端业务;物联网周界安防业务.")
    })
    # ST新华锦 (600735.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600735",
        "name_zh": "ST新华锦",
        "stock_codes": ["600735.SH"],
        "country": "中国",
        "industry": "服饰",
        "main_business": "主营业务为发制品+纺织服装+锡材料加工.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务为发制品+纺织服装+锡材料加工.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600735_hair_product",
        "company_id": "sh_600735",
        "node_id": "hair_product",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主营业务为发制品+纺织服装+锡材料加工.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600735_textile",
        "company_id": "sh_600735",
        "node_id": "textile",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主营业务为发制品+纺织服装+锡材料加工.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600735_tin_material",
        "company_id": "sh_600735",
        "node_id": "tin_material",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主营业务为发制品+纺织服装+锡材料加工.")
    })
    # 苏州高新 (600736.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600736",
        "name_zh": "苏州高新",
        "stock_codes": ["600736.SH"],
        "country": "中国",
        "industry": "园区开发",
        "main_business": "房地产.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600736_real_estate_development",
        "company_id": "sh_600736",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("房地产.")
    })
    # 中粮糖业 (600737.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600737",
        "name_zh": "中粮糖业",
        "stock_codes": ["600737.SH"],
        "country": "中国",
        "industry": "食品",
        "main_business": "主要产品:番茄产品,农副产品,水泥产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:番茄产品,农副产品,水泥产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600737_tomato_product",
        "company_id": "sh_600737",
        "node_id": "tomato_product",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:番茄产品,农副产品,水泥产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600737_agricultural_product",
        "company_id": "sh_600737",
        "node_id": "agricultural_product",
        "activity_type": "procure",
        "weight": 0.35,
        "evidence": make_evidence("主要产品:番茄产品,农副产品,水泥产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600737_cement",
        "company_id": "sh_600737",
        "node_id": "cement",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主要产品:番茄产品,农副产品,水泥产品.")
    })
    # 丽尚国潮 (600738.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600738",
        "name_zh": "丽尚国潮",
        "stock_codes": ["600738.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "主营业务:商品零售,餐饮娱乐.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:商品零售,餐饮娱乐.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600738_department_store",
        "company_id": "sh_600738",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:商品零售,餐饮娱乐.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600738_catering_entertainment_service",
        "company_id": "sh_600738",
        "node_id": "catering_entertainment_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:商品零售,餐饮娱乐.")
    })
    # 辽宁成大 (600739.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600739",
        "name_zh": "辽宁成大",
        "stock_codes": ["600739.SH"],
        "country": "中国",
        "industry": "生物制药",
        "main_business": "医药医疗,金融投资,供应链服务(贸易)和能源开发.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("医药医疗,金融投资,供应链服务(贸易)和能源开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600739_pharmaceutical_commerce",
        "company_id": "sh_600739",
        "node_id": "pharmaceutical_commerce",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("医药医疗,金融投资,供应链服务(贸易)和能源开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600739_financial_investment_service",
        "company_id": "sh_600739",
        "node_id": "financial_investment_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("医药医疗,金融投资,供应链服务(贸易)和能源开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600739_supply_chain_service",
        "company_id": "sh_600739",
        "node_id": "supply_chain_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("医药医疗,金融投资,供应链服务(贸易)和能源开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600739_energy_development_service",
        "company_id": "sh_600739",
        "node_id": "energy_development_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("医药医疗,金融投资,供应链服务(贸易)和能源开发.")
    })
    # 山西焦化 (600740.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600740",
        "name_zh": "山西焦化",
        "stock_codes": ["600740.SH"],
        "country": "中国",
        "industry": "焦炭加工",
        "main_business": "焦炭,其他化工产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("焦炭,其他化工产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600740_coke",
        "company_id": "sh_600740",
        "node_id": "coke",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("焦炭,其他化工产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600740_coking_product",
        "company_id": "sh_600740",
        "node_id": "coking_product",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("焦炭,其他化工产品.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_097_biz",
            "task_description": f"Batch 097 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次97构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
