#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 99."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_099.json"

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
    if "financial_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "financial_service",
            "canonical_name_zh": "金融服务",
            "canonical_name_en": "Financial Service",
            "definition": "为客户提供融资、结算、担保、保险及金融咨询等综合金融服务",
            "entity_type": "service",
            "evidence": make_evidence("金融服务业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: financial_service")
    if "computer_hardware" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "computer_hardware",
            "canonical_name_zh": "计算机硬件",
            "canonical_name_en": "Computer Hardware",
            "definition": "计算机系统的物理设备，包括服务器、个人电脑、存储设备、网络设备及外围设备",
            "entity_type": "device",
            "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: computer_hardware")
    if "technical_training_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "technical_training_service",
            "canonical_name_zh": "技术培训服务",
            "canonical_name_en": "Technical Training Service",
            "definition": "为客户提供通信、计算机及网络技术领域的专业技能培训和认证服务",
            "entity_type": "service",
            "evidence": make_evidence("技术培训", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: technical_training_service")
    if "book_publishing" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "book_publishing",
            "canonical_name_zh": "图书出版",
            "canonical_name_en": "Book Publishing",
            "definition": "将作者原稿经编辑、排版、印刷等工序制成图书并发行销售的出版业务",
            "entity_type": "service",
            "evidence": make_evidence("图书", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: book_publishing")
    if "journal_publishing" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "journal_publishing",
            "canonical_name_zh": "期刊出版",
            "canonical_name_en": "Journal Publishing",
            "definition": "定期出版发行的杂志、学术期刊等连续出版物的编辑、印刷和发行业务",
            "entity_type": "service",
            "evidence": make_evidence("期刊", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: journal_publishing")
    if "newspaper_publishing" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "newspaper_publishing",
            "canonical_name_zh": "报纸出版",
            "canonical_name_en": "Newspaper Publishing",
            "definition": "以新闻、评论和信息为主要内容的定期出版物编辑、印刷和发行业务",
            "entity_type": "service",
            "evidence": make_evidence("报纸", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: newspaper_publishing")
    if "audio_video_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "audio_video_product",
            "canonical_name_zh": "音像制品",
            "canonical_name_en": "Audio Video Product",
            "definition": "以录音带、录像带、CD、DVD等为载体的音频和视频内容出版物",
            "entity_type": "material",
            "evidence": make_evidence("音像制品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: audio_video_product")
    if "electronic_publication" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "electronic_publication",
            "canonical_name_zh": "电子出版物",
            "canonical_name_en": "Electronic Publication",
            "definition": "以数字形式存储和传播的出版物，包括电子书、电子期刊、数据库及多媒体光盘等",
            "entity_type": "material",
            "evidence": make_evidence("电子出版物", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: electronic_publication")
    if "construction_installation_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "construction_installation_service",
            "canonical_name_zh": "建筑安装服务",
            "canonical_name_en": "Construction Installation Service",
            "definition": "为建筑工程提供土建施工、机电设备安装、管道敷设及系统调试的综合服务",
            "entity_type": "service",
            "evidence": make_evidence("建筑安装", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: construction_installation_service")
    if "building_material" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "building_material",
            "canonical_name_zh": "建筑材料",
            "canonical_name_en": "Building Material",
            "definition": "用于建筑物建造和装修的各类材料，包括钢材、水泥、玻璃、陶瓷、涂料及保温材料等",
            "entity_type": "material",
            "evidence": make_evidence("建筑材料销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: building_material")
    if "property_rental_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "property_rental_service",
            "canonical_name_zh": "物业租赁服务",
            "canonical_name_en": "Property Rental Service",
            "definition": "将自有或受托管理的物业用于出租经营，提供租赁管理、维修维护及配套服务的业务",
            "entity_type": "service",
            "evidence": make_evidence("物业租赁", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: property_rental_service")
    if "aerospace_rd_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "aerospace_rd_service",
            "canonical_name_zh": "航空产品研发服务",
            "canonical_name_en": "Aerospace R&D Service",
            "definition": "从事航空器及相关产品的研发设计、试验验证和技术改进的专业技术服务",
            "entity_type": "service",
            "evidence": make_evidence("航空产品研发", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: aerospace_rd_service")
    if "forklift" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "forklift",
            "canonical_name_zh": "叉车",
            "canonical_name_en": "Forklift",
            "definition": "一种用于装卸、堆垛和短距离运输托盘货物的工业搬运车辆",
            "entity_type": "device",
            "evidence": make_evidence("叉车产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: forklift")
    if "dental_medical_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "dental_medical_service",
            "canonical_name_zh": "口腔医疗服务",
            "canonical_name_en": "Dental Medical Service",
            "definition": "为患者提供口腔疾病预防、诊断、治疗及修复的专业医疗服务",
            "entity_type": "service",
            "evidence": make_evidence("口腔", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: dental_medical_service")
    if "assisted_reproduction_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "assisted_reproduction_service",
            "canonical_name_zh": "辅助生殖医疗服务",
            "canonical_name_en": "Assisted Reproduction Service",
            "definition": "运用医学手段帮助不孕不育夫妇实现生育的医疗服务，包括人工授精、试管婴儿等技术",
            "entity_type": "service",
            "evidence": make_evidence("辅助生殖医疗", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: assisted_reproduction_service")

    # ---- Graph edges ----
    edges_to_create = []


    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_099_graph",
            "task_description": f"Batch 099 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次99构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # *ST海钦 (600753.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600753",
        "name_zh": "*ST海钦",
        "stock_codes": ["600753.SH"],
        "country": "中国",
        "industry": "商贸代理",
        "main_business": "大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600753_coal",
        "company_id": "sh_600753",
        "node_id": "coal",
        "activity_type": "procure",
        "weight": 0.4,
        "evidence": make_evidence("大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600753_coke",
        "company_id": "sh_600753",
        "node_id": "coke",
        "activity_type": "procure",
        "weight": 0.4,
        "evidence": make_evidence("大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600753_trade_agent",
        "company_id": "sh_600753",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.")
    })
    # 锦江酒店 (600754.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600754",
        "name_zh": "锦江酒店",
        "stock_codes": ["600754.SH"],
        "country": "中国",
        "industry": "酒店餐饮",
        "main_business": "有限服务型酒店营运及管理业务和食品及餐饮业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("有限服务型酒店营运及管理业务和食品及餐饮业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600754_hotel",
        "company_id": "sh_600754",
        "node_id": "hotel",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("有限服务型酒店营运及管理业务和食品及餐饮业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600754_hotel_operation_service",
        "company_id": "sh_600754",
        "node_id": "hotel_operation_service",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("有限服务型酒店营运及管理业务和食品及餐饮业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600754_catering_service",
        "company_id": "sh_600754",
        "node_id": "catering_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("有限服务型酒店营运及管理业务和食品及餐饮业务.")
    })
    # 厦门国贸 (600755.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600755",
        "name_zh": "厦门国贸",
        "stock_codes": ["600755.SH"],
        "country": "中国",
        "industry": "仓储物流",
        "main_business": "供应链管理业务,房地产经营业务,金融服务业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("供应链管理业务,房地产经营业务,金融服务业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600755_supply_chain_service",
        "company_id": "sh_600755",
        "node_id": "supply_chain_service",
        "activity_type": "provide_service",
        "weight": 0.35,
        "evidence": make_evidence("供应链管理业务,房地产经营业务,金融服务业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600755_real_estate_development",
        "company_id": "sh_600755",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("供应链管理业务,房地产经营业务,金融服务业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600755_financial_service",
        "company_id": "sh_600755",
        "node_id": "financial_service",
        "activity_type": "provide_service",
        "weight": 0.35,
        "evidence": make_evidence("供应链管理业务,房地产经营业务,金融服务业务.")
    })
    # 浪潮软件 (600756.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600756",
        "name_zh": "浪潮软件",
        "stock_codes": ["600756.SH"],
        "country": "中国",
        "industry": "软件服务",
        "main_business": "通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600756_software_development_service",
        "company_id": "sh_600756",
        "node_id": "software_development_service",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600756_computer_hardware",
        "company_id": "sh_600756",
        "node_id": "computer_hardware",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600756_telecom_software",
        "company_id": "sh_600756",
        "node_id": "telecom_software",
        "activity_type": "provide_service",
        "weight": 0.2,
        "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600756_technical_training_service",
        "company_id": "sh_600756",
        "node_id": "technical_training_service",
        "activity_type": "provide_service",
        "weight": 0.2,
        "evidence": make_evidence("通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.")
    })
    # 长江传媒 (600757.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600757",
        "name_zh": "长江传媒",
        "stock_codes": ["600757.SH"],
        "country": "中国",
        "industry": "出版业",
        "main_business": "图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_book_publishing",
        "company_id": "sh_600757",
        "node_id": "book_publishing",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_journal_publishing",
        "company_id": "sh_600757",
        "node_id": "journal_publishing",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_newspaper_publishing",
        "company_id": "sh_600757",
        "node_id": "newspaper_publishing",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_audio_video_product",
        "company_id": "sh_600757",
        "node_id": "audio_video_product",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_electronic_publication",
        "company_id": "sh_600757",
        "node_id": "electronic_publication",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600757_trade_agent",
        "company_id": "sh_600757",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.")
    })
    # 辽宁能源 (600758.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600758",
        "name_zh": "辽宁能源",
        "stock_codes": ["600758.SH"],
        "country": "中国",
        "industry": "煤炭开采",
        "main_business": "建筑安装,房地产开发,建筑材料销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("建筑安装,房地产开发,建筑材料销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600758_construction_installation_service",
        "company_id": "sh_600758",
        "node_id": "construction_installation_service",
        "activity_type": "provide_service",
        "weight": 0.35,
        "evidence": make_evidence("建筑安装,房地产开发,建筑材料销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600758_real_estate_development",
        "company_id": "sh_600758",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("建筑安装,房地产开发,建筑材料销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600758_building_material",
        "company_id": "sh_600758",
        "node_id": "building_material",
        "activity_type": "procure",
        "weight": 0.35,
        "evidence": make_evidence("建筑安装,房地产开发,建筑材料销售.")
    })
    # ST洲际 (600759.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600759",
        "name_zh": "ST洲际",
        "stock_codes": ["600759.SH"],
        "country": "中国",
        "industry": "石油开采",
        "main_business": "石油勘探开发业务,房地产开发,物业租赁以及贸易.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("石油勘探开发业务,房地产开发,物业租赁以及贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600759_petroleum_exploration",
        "company_id": "sh_600759",
        "node_id": "petroleum_exploration",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("石油勘探开发业务,房地产开发,物业租赁以及贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600759_real_estate_development",
        "company_id": "sh_600759",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("石油勘探开发业务,房地产开发,物业租赁以及贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600759_property_rental_service",
        "company_id": "sh_600759",
        "node_id": "property_rental_service",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("石油勘探开发业务,房地产开发,物业租赁以及贸易.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600759_trade_agent",
        "company_id": "sh_600759",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("石油勘探开发业务,房地产开发,物业租赁以及贸易.")
    })
    # 中航沈飞 (600760.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600760",
        "name_zh": "中航沈飞",
        "stock_codes": ["600760.SH"],
        "country": "中国",
        "industry": "航空",
        "main_business": "实业投资;航空产品研发,生产,服务保障.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("实业投资;航空产品研发,生产,服务保障.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600760_aerospace_rd_service",
        "company_id": "sh_600760",
        "node_id": "aerospace_rd_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("实业投资;航空产品研发,生产,服务保障.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600760_aerospace_product",
        "company_id": "sh_600760",
        "node_id": "aerospace_product",
        "activity_type": "manufacture",
        "weight": 0.5,
        "evidence": make_evidence("实业投资;航空产品研发,生产,服务保障.")
    })
    # 安徽合力 (600761.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600761",
        "name_zh": "安徽合力",
        "stock_codes": ["600761.SH"],
        "country": "中国",
        "industry": "工程机械",
        "main_business": "叉车产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("叉车产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600761_forklift",
        "company_id": "sh_600761",
        "node_id": "forklift",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("叉车产品.")
    })
    # 通策医疗 (600763.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600763",
        "name_zh": "通策医疗",
        "stock_codes": ["600763.SH"],
        "country": "中国",
        "industry": "医疗保健",
        "main_business": "口腔,辅助生殖医疗等服务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("口腔,辅助生殖医疗等服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600763_dental_medical_service",
        "company_id": "sh_600763",
        "node_id": "dental_medical_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("口腔,辅助生殖医疗等服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600763_assisted_reproduction_service",
        "company_id": "sh_600763",
        "node_id": "assisted_reproduction_service",
        "activity_type": "provide_service",
        "weight": 0.5,
        "evidence": make_evidence("口腔,辅助生殖医疗等服务.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_099_biz",
            "task_description": f"Batch 099 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次99构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
