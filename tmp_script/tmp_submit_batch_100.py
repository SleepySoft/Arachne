#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 100."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_100.json"

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
    if "underwater_acoustic_equipment" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "underwater_acoustic_equipment",
            "canonical_name_zh": "水声信息传输装备",
            "canonical_name_en": "Underwater Acoustic Equipment",
            "definition": "利用水声通信技术在水下传输信息的专用装备，包括声纳、水声通信机和声信标等",
            "entity_type": "device",
            "evidence": make_evidence("水声信息传输装备", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: underwater_acoustic_equipment")
    if "underwater_weapon_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "underwater_weapon_system",
            "canonical_name_zh": "水下武器系统",
            "canonical_name_en": "Underwater Weapon System",
            "definition": "部署于水下用于攻击或防御的武器系统，包括鱼雷、水雷、深水炸弹及反潜导弹等",
            "entity_type": "system",
            "evidence": make_evidence("水下武器系统专项设备", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: underwater_weapon_system")
    if "ballast_water_power_supply" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ballast_water_power_supply",
            "canonical_name_zh": "压载水电源",
            "canonical_name_en": "Ballast Water Power Supply",
            "definition": "为船舶压载水处理系统提供电力的专用电源设备，确保压载水在排放前得到有效处理",
            "entity_type": "device",
            "evidence": make_evidence("压载水电源", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ballast_water_power_supply")
    if "hydraulic_system" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "hydraulic_system",
            "canonical_name_zh": "液压系统",
            "canonical_name_en": "Hydraulic System",
            "definition": "利用液体压力传递动力的系统，包括液压泵、液压缸、液压阀及管路等组件，广泛应用于工程机械和航空领域",
            "entity_type": "system",
            "evidence": make_evidence("液压行业", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: hydraulic_system")
    if "aluminum_plate_strip" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "aluminum_plate_strip",
            "canonical_name_zh": "铝板带材",
            "canonical_name_en": "Aluminum Plate Strip",
            "definition": "经轧制加工的扁平状铝及铝合金材料，包括铝板、铝带、铝箔等，广泛用于建筑、交通和包装",
            "entity_type": "material",
            "evidence": make_evidence("工业铝板带材", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: aluminum_plate_strip")
    if "aluminum_profile" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "aluminum_profile",
            "canonical_name_zh": "铝型材",
            "canonical_name_en": "Aluminum Profile",
            "definition": "通过挤压工艺制成的具有特定截面形状的铝材，广泛用于建筑幕墙、门窗框架和工业结构件",
            "entity_type": "material",
            "evidence": make_evidence("铝型材", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: aluminum_profile")
    if "aluminum_billet" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "aluminum_billet",
            "canonical_name_zh": "铝铸棒",
            "canonical_name_en": "Aluminum Billet",
            "definition": "通过熔炼铸造制成的圆柱形铝坯料，是挤压铝型材和轧制铝板带材的原材料",
            "entity_type": "material",
            "evidence": make_evidence("铝铸棒的仓储,贸易服务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: aluminum_billet")
    if "steam_supply_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "steam_supply_service",
            "canonical_name_zh": "供汽服务",
            "canonical_name_en": "Steam Supply Service",
            "definition": "通过锅炉或热电联产装置向工业用户供应蒸汽的公用事业服务",
            "entity_type": "service",
            "evidence": make_evidence("供电供汽", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: steam_supply_service")
    if "equity_investment_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "equity_investment_service",
            "canonical_name_zh": "股权投资服务",
            "canonical_name_en": "Equity Investment Service",
            "definition": "通过认购非上市公司股权或参与股权投资基金，为企业提供资本支持和增值服务的业务",
            "entity_type": "service",
            "evidence": make_evidence("股权投资", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: equity_investment_service")
    if "chinese_patent_medicine_pill" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "chinese_patent_medicine_pill",
            "canonical_name_zh": "中药经典名方制剂",
            "canonical_name_en": "Chinese Patent Medicine Pill",
            "definition": "以经典中药方剂为基础，经现代工艺制成的丸剂、散剂等中成药制剂，如安宫牛黄丸、定坤丹等",
            "entity_type": "material",
            "evidence": make_evidence("龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: chinese_patent_medicine_pill")
    if "electromechanical_instrument_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "electromechanical_instrument_product",
            "canonical_name_zh": "机电仪产品",
            "canonical_name_en": "Electromechanical Instrument Product",
            "definition": "集机械、电子和仪表技术于一体的综合性产品，包括工业自动化仪表、控制设备及精密机械装置",
            "entity_type": "component",
            "evidence": make_evidence("机电仪产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: electromechanical_instrument_product")
    if "electronic_information_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "electronic_information_product",
            "canonical_name_zh": "电子信息产品",
            "canonical_name_en": "Electronic Information Product",
            "definition": "利用电子信息技术制造的各类产品，包括通信设备、计算机、消费电子及电子元器件等",
            "entity_type": "component",
            "evidence": make_evidence("电子信息产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: electronic_information_product")
    if "ic_card_telephone" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ic_card_telephone",
            "canonical_name_zh": "IC卡话机",
            "canonical_name_en": "IC Card Telephone",
            "definition": "支持插入IC卡进行计费通话的公用电话终端设备，广泛用于公共场所通信服务",
            "entity_type": "device",
            "evidence": make_evidence("IC卡话机业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ic_card_telephone")
    if "telecom_power_equipment" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "telecom_power_equipment",
            "canonical_name_zh": "电信电源设备",
            "canonical_name_en": "Telecom Power Equipment",
            "definition": "为通信网络设备提供稳定电力供应的专用电源系统，包括开关电源、UPS、蓄电池及配电设备等",
            "entity_type": "device",
            "evidence": make_evidence("电信及电源设备业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: telecom_power_equipment")

    # ---- Graph edges ----
    edges_to_create = []


    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_100_graph",
            "task_description": f"Batch 100 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次100构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 中国海防 (600764.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600764",
        "name_zh": "中国海防",
        "stock_codes": ["600764.SH"],
        "country": "中国",
        "industry": "船舶",
        "main_business": "各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600764_underwater_acoustic_equipment",
        "company_id": "sh_600764",
        "node_id": "underwater_acoustic_equipment",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600764_underwater_weapon_system",
        "company_id": "sh_600764",
        "node_id": "underwater_weapon_system",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600764_ballast_water_power_supply",
        "company_id": "sh_600764",
        "node_id": "ballast_water_power_supply",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600764_ship",
        "company_id": "sh_600764",
        "node_id": "ship",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.")
    })
    # XD中航重 (600765.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600765",
        "name_zh": "XD中航重",
        "stock_codes": ["600765.SH"],
        "country": "中国",
        "industry": "航空",
        "main_business": "液压行业.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("液压行业.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600765_hydraulic_system",
        "company_id": "sh_600765",
        "node_id": "hydraulic_system",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("液压行业.")
    })
    # 宁波富邦 (600768.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600768",
        "name_zh": "宁波富邦",
        "stock_codes": ["600768.SH"],
        "country": "中国",
        "industry": "铝",
        "main_business": "工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600768_aluminum_plate_strip",
        "company_id": "sh_600768",
        "node_id": "aluminum_plate_strip",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600768_aluminum_profile",
        "company_id": "sh_600768",
        "node_id": "aluminum_profile",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600768_aluminum_billet",
        "company_id": "sh_600768",
        "node_id": "aluminum_billet",
        "activity_type": "procure",
        "weight": 0.2,
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600768_warehouse_service",
        "company_id": "sh_600768",
        "node_id": "warehouse_service",
        "activity_type": "operate",
        "weight": 0.1,
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600768_trade_agent",
        "company_id": "sh_600768",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.1,
        "evidence": make_evidence("工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.")
    })
    # 祥龙电业 (600769.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600769",
        "name_zh": "祥龙电业",
        "stock_codes": ["600769.SH"],
        "country": "中国",
        "industry": "水务",
        "main_business": "化工产品,供电供汽,运输.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("化工产品,供电供汽,运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600769_chemical_product",
        "company_id": "sh_600769",
        "node_id": "chemical_product",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("化工产品,供电供汽,运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600769_electricity_power",
        "company_id": "sh_600769",
        "node_id": "electricity_power",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("化工产品,供电供汽,运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600769_steam_supply_service",
        "company_id": "sh_600769",
        "node_id": "steam_supply_service",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("化工产品,供电供汽,运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600769_logistics_service",
        "company_id": "sh_600769",
        "node_id": "logistics_service",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("化工产品,供电供汽,运输.")
    })
    # 综艺股份 (600770.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600770",
        "name_zh": "综艺股份",
        "stock_codes": ["600770.SH"],
        "country": "中国",
        "industry": "综合类",
        "main_business": "信息科技,新能源,股权投资.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("信息科技,新能源,股权投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600770_information_technology_service",
        "company_id": "sh_600770",
        "node_id": "information_technology_service",
        "activity_type": "provide_service",
        "weight": 0.35,
        "evidence": make_evidence("信息科技,新能源,股权投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600770_new_energy",
        "company_id": "sh_600770",
        "node_id": "new_energy",
        "activity_type": "operate",
        "weight": 0.35,
        "evidence": make_evidence("信息科技,新能源,股权投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600770_equity_investment_service",
        "company_id": "sh_600770",
        "node_id": "equity_investment_service",
        "activity_type": "provide_service",
        "weight": 0.3,
        "evidence": make_evidence("信息科技,新能源,股权投资.")
    })
    # 广誉远 (600771.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600771",
        "name_zh": "广誉远",
        "stock_codes": ["600771.SH"],
        "country": "中国",
        "industry": "中成药",
        "main_business": "龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600771_chinese_patent_medicine_pill",
        "company_id": "sh_600771",
        "node_id": "chinese_patent_medicine_pill",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等.")
    })
    # 西藏城投 (600773.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600773",
        "name_zh": "西藏城投",
        "stock_codes": ["600773.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600773_real_estate_development",
        "company_id": "sh_600773",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600773_mining_investment",
        "company_id": "sh_600773",
        "node_id": "mining_investment",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600773_financial_investment_service",
        "company_id": "sh_600773",
        "node_id": "financial_investment_service",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600773_industrial_investment",
        "company_id": "sh_600773",
        "node_id": "industrial_investment",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.")
    })
    # 汉商集团 (600774.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600774",
        "name_zh": "汉商集团",
        "stock_codes": ["600774.SH"],
        "country": "中国",
        "industry": "化学制药",
        "main_business": "零售业,会展业,地产业及旅业等业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("零售业,会展业,地产业及旅业等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600774_department_store",
        "company_id": "sh_600774",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("零售业,会展业,地产业及旅业等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600774_exhibition_service",
        "company_id": "sh_600774",
        "node_id": "exhibition_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("零售业,会展业,地产业及旅业等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600774_real_estate_development",
        "company_id": "sh_600774",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.25,
        "evidence": make_evidence("零售业,会展业,地产业及旅业等业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600774_tourism_service",
        "company_id": "sh_600774",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "weight": 0.25,
        "evidence": make_evidence("零售业,会展业,地产业及旅业等业务.")
    })
    # 南京熊猫 (600775.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600775",
        "name_zh": "南京熊猫",
        "stock_codes": ["600775.SH"],
        "country": "中国",
        "industry": "通信设备",
        "main_business": "移动通信产品,卫星通信产品,机电仪产品,电子信息产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("移动通信产品,卫星通信产品,机电仪产品,电子信息产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600775_mobile_communication_equipment",
        "company_id": "sh_600775",
        "node_id": "mobile_communication_equipment",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信产品,卫星通信产品,机电仪产品,电子信息产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600775_satellite_communication",
        "company_id": "sh_600775",
        "node_id": "satellite_communication",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信产品,卫星通信产品,机电仪产品,电子信息产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600775_electromechanical_instrument_product",
        "company_id": "sh_600775",
        "node_id": "electromechanical_instrument_product",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信产品,卫星通信产品,机电仪产品,电子信息产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600775_electronic_information_product",
        "company_id": "sh_600775",
        "node_id": "electronic_information_product",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信产品,卫星通信产品,机电仪产品,电子信息产品.")
    })
    # 东方通信 (600776.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600776",
        "name_zh": "东方通信",
        "stock_codes": ["600776.SH"],
        "country": "中国",
        "industry": "通信设备",
        "main_business": "移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600776_mobile_communication_equipment",
        "company_id": "sh_600776",
        "node_id": "mobile_communication_equipment",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600776_transmission_equipment",
        "company_id": "sh_600776",
        "node_id": "transmission_equipment",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600776_ic_card_telephone",
        "company_id": "sh_600776",
        "node_id": "ic_card_telephone",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600776_telecom_power_equipment",
        "company_id": "sh_600776",
        "node_id": "telecom_power_equipment",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_100_biz",
            "task_description": f"Batch 100 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次100构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
