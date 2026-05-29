#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 98."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_098.json"

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
    if "automotive_wheel" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "automotive_wheel",
            "canonical_name_zh": "汽车车轮",
            "canonical_name_en": "Automotive Wheel",
            "definition": "汽车行驶系统的重要组成部分，包括轮辋、轮辐、轮胎及轮毂等总成",
            "entity_type": "component",
            "evidence": make_evidence("车轮", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: automotive_wheel")
    if "thermal_power_generation" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "thermal_power_generation",
            "canonical_name_zh": "火力发电服务",
            "canonical_name_en": "Thermal Power Generation",
            "definition": "利用煤炭、天然气等化石燃料燃烧产生热能，驱动汽轮机发电的电力生产服务",
            "entity_type": "service",
            "evidence": make_evidence("火力发电", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: thermal_power_generation")
    if "vr_device" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "vr_device",
            "canonical_name_zh": "虚拟现实设备",
            "canonical_name_en": "VR Device",
            "definition": "能够生成沉浸式虚拟环境的头戴式显示设备及其配套交互设备，如手柄、定位器等",
            "entity_type": "device",
            "evidence": make_evidence("虚拟现实", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: vr_device")
    if "adc_blowing_agent" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "adc_blowing_agent",
            "canonical_name_zh": "ADC发泡剂",
            "canonical_name_en": "ADC Blowing Agent",
            "definition": "偶氮二甲酰胺，一种常用的化学发泡剂，广泛应用于PVC、聚乙烯、聚丙烯等塑料的发泡加工",
            "entity_type": "material",
            "evidence": make_evidence("ADC发泡剂", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: adc_blowing_agent")
    if "bleaching_powder" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "bleaching_powder",
            "canonical_name_zh": "漂粉精",
            "canonical_name_en": "Bleaching Powder",
            "definition": "主要成分为次氯酸钙的高效漂白消毒剂，广泛用于纺织漂白、水处理和卫生消毒",
            "entity_type": "material",
            "evidence": make_evidence("漂粉精", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: bleaching_powder")
    if "media_agency_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "media_agency_service",
            "canonical_name_zh": "媒体代理服务",
            "canonical_name_en": "Media Agency Service",
            "definition": "为客户提供广告策划、媒体投放、效果监测及品牌传播策略的代理服务",
            "entity_type": "service",
            "evidence": make_evidence("媒体代理", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: media_agency_service")
    if "antibiotic_preparation" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "antibiotic_preparation",
            "canonical_name_zh": "抗生素制剂",
            "canonical_name_en": "Antibiotic Preparation",
            "definition": "以抗生素原料药为基础制成的可供临床使用的药品制剂，包括注射剂、口服制剂等",
            "entity_type": "material",
            "evidence": make_evidence("抗生素制剂", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: antibiotic_preparation")
    if "it_product_distribution" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "it_product_distribution",
            "canonical_name_zh": "IT产品分销服务",
            "canonical_name_en": "IT Product Distribution",
            "definition": "从事计算机硬件、软件、网络设备及IT配件的渠道分销和供应链管理服务",
            "entity_type": "service",
            "evidence": make_evidence("IT产品分销及技术解决方案", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: it_product_distribution")
    if "ecommerce_supply_chain_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ecommerce_supply_chain_service",
            "canonical_name_zh": "电子商务供应链服务",
            "canonical_name_en": "E-commerce Supply Chain Service",
            "definition": "为电子商务平台提供仓储、物流、配送及供应链信息化管理的综合服务",
            "entity_type": "service",
            "evidence": make_evidence("电子商务供应链解决方案", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ecommerce_supply_chain_service")
    if "cloud_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "cloud_service",
            "canonical_name_zh": "云服务",
            "canonical_name_en": "Cloud Service",
            "definition": "基于互联网提供计算资源、存储资源、应用软件及平台服务的IT服务形态",
            "entity_type": "service",
            "evidence": make_evidence("海航云集市,海航云科技", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: cloud_service")
    if "design_production_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "design_production_service",
            "canonical_name_zh": "设计制作服务",
            "canonical_name_en": "Design Production Service",
            "definition": "为客户提供平面设计、影视制作、展览展示及多媒体内容创作的创意服务",
            "entity_type": "service",
            "evidence": make_evidence("设计制作", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: design_production_service")
    if "mobile_device_lifecycle_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "mobile_device_lifecycle_service",
            "canonical_name_zh": "移动设备生命周期服务",
            "canonical_name_en": "Mobile Device Lifecycle Service",
            "definition": "为移动设备提供采购、部署、运维、回收及数据清除等全生命周期管理服务",
            "entity_type": "service",
            "evidence": make_evidence("移动设备及生命周期服务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: mobile_device_lifecycle_service")

    # ---- Graph edges ----
    edges_to_create = []


    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_098_graph",
            "task_description": f"Batch 098 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次98构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 华域汽车 (600741.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600741",
        "name_zh": "华域汽车",
        "stock_codes": ["600741.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "独立供应汽车零部件研发,生产及销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("独立供应汽车零部件研发,生产及销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600741_automotive_part",
        "company_id": "sh_600741",
        "node_id": "automotive_part",
        "activity_type": "manufacture",
        "weight": 0.5,
        "evidence": make_evidence("独立供应汽车零部件研发,生产及销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600741_automotive_rd_service",
        "company_id": "sh_600741",
        "node_id": "automotive_rd_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("独立供应汽车零部件研发,生产及销售.")
    })
    # 富维股份 (600742.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600742",
        "name_zh": "富维股份",
        "stock_codes": ["600742.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "车轮,内饰件.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("车轮,内饰件.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600742_automotive_wheel",
        "company_id": "sh_600742",
        "node_id": "automotive_wheel",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("车轮,内饰件.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600742_automotive_interior",
        "company_id": "sh_600742",
        "node_id": "automotive_interior",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("车轮,内饰件.")
    })
    # 华远控股 (600743.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600743",
        "name_zh": "华远控股",
        "stock_codes": ["600743.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "房地产开发与经营.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产开发与经营.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600743_real_estate_development",
        "company_id": "sh_600743",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("房地产开发与经营.")
    })
    # 华银电力 (600744.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600744",
        "name_zh": "华银电力",
        "stock_codes": ["600744.SH"],
        "country": "中国",
        "industry": "火力发电",
        "main_business": "火力发电,水力发电.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("火力发电,水力发电.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600744_thermal_power_generation",
        "company_id": "sh_600744",
        "node_id": "thermal_power_generation",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("火力发电,水力发电.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600744_hydro_power",
        "company_id": "sh_600744",
        "node_id": "hydro_power",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("火力发电,水力发电.")
    })
    # *ST闻泰 (600745.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600745",
        "name_zh": "*ST闻泰",
        "stock_codes": ["600745.SH"],
        "country": "中国",
        "industry": "半导体",
        "main_business": "主要产品:智能终端,虚拟现实,地产和酒店等",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:智能终端,虚拟现实,地产和酒店等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600745_smart_terminal",
        "company_id": "sh_600745",
        "node_id": "smart_terminal",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主要产品:智能终端,虚拟现实,地产和酒店等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600745_vr_device",
        "company_id": "sh_600745",
        "node_id": "vr_device",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("主要产品:智能终端,虚拟现实,地产和酒店等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600745_real_estate_development",
        "company_id": "sh_600745",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主要产品:智能终端,虚拟现实,地产和酒店等")
    })
    exposures_payload.append({
        "exposure_id": "sh_600745_hotel",
        "company_id": "sh_600745",
        "node_id": "hotel",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主要产品:智能终端,虚拟现实,地产和酒店等")
    })
    # 江苏索普 (600746.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600746",
        "name_zh": "江苏索普",
        "stock_codes": ["600746.SH"],
        "country": "中国",
        "industry": "化工原料",
        "main_business": "ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600746_adc_blowing_agent",
        "company_id": "sh_600746",
        "node_id": "adc_blowing_agent",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600746_bleaching_powder",
        "company_id": "sh_600746",
        "node_id": "bleaching_powder",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600746_chlor_alkali_product",
        "company_id": "sh_600746",
        "node_id": "chlor_alkali_product",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600746_electricity_power",
        "company_id": "sh_600746",
        "node_id": "electricity_power",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600746_heat_supply",
        "company_id": "sh_600746",
        "node_id": "heat_supply",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.")
    })
    # 上实发展 (600748.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600748",
        "name_zh": "上实发展",
        "stock_codes": ["600748.SH"],
        "country": "中国",
        "industry": "全国地产",
        "main_business": "房屋租赁.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房屋租赁.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600748_real_estate_development",
        "company_id": "sh_600748",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("房屋租赁.")
    })
    # 西藏旅游 (600749.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600749",
        "name_zh": "西藏旅游",
        "stock_codes": ["600749.SH"],
        "country": "中国",
        "industry": "旅游景点",
        "main_business": "旅游,酒店,设计制作,媒体代理.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("旅游,酒店,设计制作,媒体代理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600749_tourism_service",
        "company_id": "sh_600749",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("旅游,酒店,设计制作,媒体代理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600749_hotel",
        "company_id": "sh_600749",
        "node_id": "hotel",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("旅游,酒店,设计制作,媒体代理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600749_design_production_service",
        "company_id": "sh_600749",
        "node_id": "design_production_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("旅游,酒店,设计制作,媒体代理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600749_media_agency_service",
        "company_id": "sh_600749",
        "node_id": "media_agency_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("旅游,酒店,设计制作,媒体代理.")
    })
    # 华润江中 (600750.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600750",
        "name_zh": "华润江中",
        "stock_codes": ["600750.SH"],
        "country": "中国",
        "industry": "中成药",
        "main_business": "中成药,抗生素制剂,原料药.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("中成药,抗生素制剂,原料药.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600750_chinese_medicine_plaster",
        "company_id": "sh_600750",
        "node_id": "chinese_medicine_plaster",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("中成药,抗生素制剂,原料药.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600750_antibiotic_preparation",
        "company_id": "sh_600750",
        "node_id": "antibiotic_preparation",
        "activity_type": "produce",
        "weight": 0.35,
        "evidence": make_evidence("中成药,抗生素制剂,原料药.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600750_pharmaceutical_raw_material",
        "company_id": "sh_600750",
        "node_id": "pharmaceutical_raw_material",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("中成药,抗生素制剂,原料药.")
    })
    # 海航科技 (600751.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600751",
        "name_zh": "海航科技",
        "stock_codes": ["600751.SH"],
        "country": "中国",
        "industry": "水运",
        "main_business": "IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600751_it_product_distribution",
        "company_id": "sh_600751",
        "node_id": "it_product_distribution",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600751_mobile_device_lifecycle_service",
        "company_id": "sh_600751",
        "node_id": "mobile_device_lifecycle_service",
        "activity_type": "provide_service",
        "weight": 0.2,
        "evidence": make_evidence("IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600751_ecommerce_supply_chain_service",
        "company_id": "sh_600751",
        "node_id": "ecommerce_supply_chain_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600751_cloud_service",
        "company_id": "sh_600751",
        "node_id": "cloud_service",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_098_biz",
            "task_description": f"Batch 098 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次98构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
