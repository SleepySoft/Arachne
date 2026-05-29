#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 93."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_093.json"

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
    if "special_vessel" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "special_vessel",
            "canonical_name_zh": "特种船舶",
            "canonical_name_en": "Special Vessel",
            "definition": "为特定用途设计建造的船舶，如工程船、科考船、破冰船、液化气运输船等",
            "entity_type": "system",
            "evidence": make_evidence("特种船", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: special_vessel")
    if "frp_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "frp_product",
            "canonical_name_zh": "玻璃钢制品",
            "canonical_name_en": "FRP Product",
            "definition": "以玻璃纤维及其制品为增强材料、合成树脂为基体材料的复合材料制品",
            "entity_type": "component",
            "evidence": make_evidence("玻璃钢制品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: frp_product")
    if "marine_furniture" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "marine_furniture",
            "canonical_name_zh": "船舶家具",
            "canonical_name_en": "Marine Furniture",
            "definition": "专门为船舶舱室设计制造的家具，具有防火、防腐蚀、固定安装等特性",
            "entity_type": "component",
            "evidence": make_evidence("家具", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: marine_furniture")
    if "synthetic_fiber" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "synthetic_fiber",
            "canonical_name_zh": "合成纤维",
            "canonical_name_en": "Synthetic Fiber",
            "definition": "以石油、天然气等为原料，经化学合成和纺丝工艺制成的人工纤维",
            "entity_type": "material",
            "evidence": make_evidence("合成纤维", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: synthetic_fiber")
    if "petroleum_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "petroleum_product",
            "canonical_name_zh": "石油产品",
            "canonical_name_en": "Petroleum Product",
            "definition": "以原油为原料经炼制加工得到的各类产品，包括汽油、柴油、润滑油、石蜡等",
            "entity_type": "material",
            "evidence": make_evidence("石油产品", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: petroleum_product")
    if "wool_textile" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "wool_textile",
            "canonical_name_zh": "毛纺织品",
            "canonical_name_en": "Wool Textile",
            "definition": "以羊毛或其他动物毛为原料经纺纱织造制成的纺织品",
            "entity_type": "material",
            "evidence": make_evidence("毛纺", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: wool_textile")
    if "ammonium_bicarbonate" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ammonium_bicarbonate",
            "canonical_name_zh": "碳酸氢铵",
            "canonical_name_en": "Ammonium Bicarbonate",
            "definition": "一种白色结晶性氮肥，也可用作食品膨松剂和分析试剂",
            "entity_type": "material",
            "evidence": make_evidence("碳酸氢铵", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ammonium_bicarbonate")
    if "ammonium_chloride" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "ammonium_chloride",
            "canonical_name_zh": "氯化铵",
            "canonical_name_en": "Ammonium Chloride",
            "definition": "一种无机化合物，可用作氮肥、干电池电解质和金属焊接助熔剂",
            "entity_type": "material",
            "evidence": make_evidence("氯化铵", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: ammonium_chloride")
    if "dimethyl_ether" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "dimethyl_ether",
            "canonical_name_zh": "二甲醚",
            "canonical_name_en": "Dimethyl Ether",
            "definition": "一种清洁燃料和化工原料，可由甲醇脱水制得，用作气雾推进剂和替代燃料",
            "entity_type": "material",
            "evidence": make_evidence("二甲醚", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: dimethyl_ether")
    if "melamine" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "melamine",
            "canonical_name_zh": "三聚氰胺",
            "canonical_name_en": "Melamine",
            "definition": "一种有机化合物，主要用于生产三聚氰胺甲醛树脂，也可用于阻燃剂和涂料",
            "entity_type": "material",
            "evidence": make_evidence("三聚氰胺", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: melamine")
    if "sodium_nitrate" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "sodium_nitrate",
            "canonical_name_zh": "硝酸钠",
            "canonical_name_en": "Sodium Nitrate",
            "definition": "一种无机盐，可用作氮肥、金属表面处理剂和食品添加剂（防腐剂）",
            "entity_type": "material",
            "evidence": make_evidence("硝酸钠", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: sodium_nitrate")
    if "sodium_nitrite" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "sodium_nitrite",
            "canonical_name_zh": "亚硝酸钠",
            "canonical_name_en": "Sodium Nitrite",
            "definition": "一种无机盐，主要用于染料工业、金属表面处理及肉制品发色剂",
            "entity_type": "material",
            "evidence": make_evidence("亚硝酸钠", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: sodium_nitrite")
    if "m_phenylenediamine" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "m_phenylenediamine",
            "canonical_name_zh": "间苯二胺",
            "canonical_name_en": "m-Phenylenediamine",
            "definition": "一种重要的有机中间体，主要用于生产染料、环氧树脂固化剂和芳纶纤维",
            "entity_type": "material",
            "evidence": make_evidence("间苯二胺", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: m_phenylenediamine")
    if "n_butylaldehyde" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "n_butylaldehyde",
            "canonical_name_zh": "正丁醛",
            "canonical_name_en": "n-Butylaldehyde",
            "definition": "一种有机化合物，是重要的化工中间体，用于生产增塑剂、溶剂和香料",
            "entity_type": "material",
            "evidence": make_evidence("正丁醛", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: n_butylaldehyde")
    if "isobutylaldehyde" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "isobutylaldehyde",
            "canonical_name_zh": "异丁醛",
            "canonical_name_en": "Isobutylaldehyde",
            "definition": "一种有机化合物，用于生产新戊二醇、异丁酸和香精香料等",
            "entity_type": "material",
            "evidence": make_evidence("异丁醛", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: isobutylaldehyde")
    if "octanol" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "octanol",
            "canonical_name_zh": "辛醇",
            "canonical_name_en": "Octanol",
            "definition": "一种重要的有机化工原料，主要用于生产增塑剂、表面活性剂和溶剂",
            "entity_type": "material",
            "evidence": make_evidence("辛醇", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: octanol")
    if "cyclohexanone" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "cyclohexanone",
            "canonical_name_zh": "环己酮",
            "canonical_name_en": "Cyclohexanone",
            "definition": "一种有机化合物，是生产己内酰胺和己二酸的重要中间体，用于尼龙制造",
            "entity_type": "material",
            "evidence": make_evidence("环己酮", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: cyclohexanone")
    if "inland_river_ferry" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "inland_river_ferry",
            "canonical_name_zh": "内河客滚运输服务",
            "canonical_name_en": "Inland River Ferry Service",
            "definition": "在内河水域提供旅客和车辆滚装运输的服务业务",
            "entity_type": "service",
            "evidence": make_evidence("内河客滚沿海客滚运输", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: inland_river_ferry")
    if "coastal_chemical_transport" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "coastal_chemical_transport",
            "canonical_name_zh": "沿海化工品运输服务",
            "canonical_name_en": "Coastal Chemical Transport Service",
            "definition": "在沿海航线从事危险化学品和化工产品海上运输的服务业务",
            "entity_type": "service",
            "evidence": make_evidence("沿海化工品运输", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: coastal_chemical_transport")

    # ---- Graph edges ----
    edges_to_create = []
    if ("urea", "compound_fertilizer", "material_flow") not in existing_edges and "urea" in existing_nodes and "compound_fertilizer" in existing_nodes:
        edges_to_create.append({
            "edge_id": "urea_to_compound_fertilizer",
            "from_node": "urea",
            "to_node": "compound_fertilizer",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "尿素是生产复合肥的主要氮源原料",
            "evidence": make_evidence("尿素,复合肥"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: urea_to_compound_fertilizer")
    if ("methanol", "dimethyl_ether", "material_flow") not in existing_edges and "methanol" in existing_nodes and "dimethyl_ether" in existing_nodes:
        edges_to_create.append({
            "edge_id": "methanol_to_dimethyl_ether",
            "from_node": "methanol",
            "to_node": "dimethyl_ether",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "甲醇经脱水反应可制得二甲醚",
            "evidence": make_evidence("甲醇,二甲醚"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: methanol_to_dimethyl_ether")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_093_graph",
            "task_description": f"Batch 093 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次93构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # 珠江股份 (600684.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600684",
        "name_zh": "珠江股份",
        "stock_codes": ["600684.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "房地产开发,销售及物业出租.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("房地产开发,销售及物业出租.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600684_real_estate_development",
        "company_id": "sh_600684",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.6,
        "evidence": make_evidence("房地产开发,销售及物业出租.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600684_commercial_property_operation",
        "company_id": "sh_600684",
        "node_id": "commercial_property_operation",
        "activity_type": "operate",
        "weight": 0.4,
        "evidence": make_evidence("房地产开发,销售及物业出租.")
    })
    # 中船防务 (600685.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600685",
        "name_zh": "中船防务",
        "stock_codes": ["600685.SH"],
        "country": "中国",
        "industry": "船舶",
        "main_business": "主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_shipbuilding",
        "company_id": "sh_600685",
        "node_id": "shipbuilding",
        "activity_type": "manufacture",
        "weight": 0.2,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_vessel_repair_service",
        "company_id": "sh_600685",
        "node_id": "vessel_repair_service",
        "activity_type": "provide_service",
        "weight": 0.15,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_special_vessel",
        "company_id": "sh_600685",
        "node_id": "special_vessel",
        "activity_type": "manufacture",
        "weight": 0.15,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_pressure_vessel",
        "company_id": "sh_600685",
        "node_id": "pressure_vessel",
        "activity_type": "manufacture",
        "weight": 0.15,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_frp_product",
        "company_id": "sh_600685",
        "node_id": "frp_product",
        "activity_type": "produce",
        "weight": 0.15,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600685_marine_furniture",
        "company_id": "sh_600685",
        "node_id": "marine_furniture",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.")
    })
    # 金龙汽车 (600686.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600686",
        "name_zh": "金龙汽车",
        "stock_codes": ["600686.SH"],
        "country": "中国",
        "industry": "汽车整车",
        "main_business": "客车产品.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("客车产品.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600686_bus",
        "company_id": "sh_600686",
        "node_id": "bus",
        "activity_type": "manufacture",
        "weight": 1.0,
        "evidence": make_evidence("客车产品.")
    })
    # 上海石化 (600688.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600688",
        "name_zh": "上海石化",
        "stock_codes": ["600688.SH"],
        "country": "中国",
        "industry": "石油加工",
        "main_business": "主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600688_petrochemical_product",
        "company_id": "sh_600688",
        "node_id": "petrochemical_product",
        "activity_type": "produce",
        "weight": 0.25,
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600688_synthetic_fiber",
        "company_id": "sh_600688",
        "node_id": "synthetic_fiber",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600688_synthetic_resin",
        "company_id": "sh_600688",
        "node_id": "synthetic_resin",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600688_petroleum_product",
        "company_id": "sh_600688",
        "node_id": "petroleum_product",
        "activity_type": "produce",
        "weight": 0.2,
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600688_trade_agent",
        "company_id": "sh_600688",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.")
    })
    # 上海三毛 (600689.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600689",
        "name_zh": "上海三毛",
        "stock_codes": ["600689.SH"],
        "country": "中国",
        "industry": "综合类",
        "main_business": "毛纺.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("毛纺.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600689_wool_textile",
        "company_id": "sh_600689",
        "node_id": "wool_textile",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("毛纺.")
    })
    # 海尔智家 (600690.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600690",
        "name_zh": "海尔智家",
        "stock_codes": ["600690.SH"],
        "country": "中国",
        "industry": "家用电器",
        "main_business": "主要产品:电冰箱,空调器.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要产品:电冰箱,空调器.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600690_refrigerator",
        "company_id": "sh_600690",
        "node_id": "refrigerator",
        "activity_type": "manufacture",
        "weight": 0.5,
        "evidence": make_evidence("主要产品:电冰箱,空调器.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600690_air_conditioner",
        "company_id": "sh_600690",
        "node_id": "air_conditioner",
        "activity_type": "manufacture",
        "weight": 0.5,
        "evidence": make_evidence("主要产品:电冰箱,空调器.")
    })
    # 潞化科技 (600691.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600691",
        "name_zh": "潞化科技",
        "stock_codes": ["600691.SH"],
        "country": "中国",
        "industry": "农药化肥",
        "main_business": "尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_urea",
        "company_id": "sh_600691",
        "node_id": "urea",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_methanol",
        "company_id": "sh_600691",
        "node_id": "methanol",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_ammonium_bicarbonate",
        "company_id": "sh_600691",
        "node_id": "ammonium_bicarbonate",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_ammonium_chloride",
        "company_id": "sh_600691",
        "node_id": "ammonium_chloride",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_compound_fertilizer",
        "company_id": "sh_600691",
        "node_id": "compound_fertilizer",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_dimethyl_ether",
        "company_id": "sh_600691",
        "node_id": "dimethyl_ether",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_soda_ash",
        "company_id": "sh_600691",
        "node_id": "soda_ash",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_melamine",
        "company_id": "sh_600691",
        "node_id": "melamine",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_nitric_acid",
        "company_id": "sh_600691",
        "node_id": "nitric_acid",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_sodium_nitrate",
        "company_id": "sh_600691",
        "node_id": "sodium_nitrate",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_sodium_nitrite",
        "company_id": "sh_600691",
        "node_id": "sodium_nitrite",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_m_phenylenediamine",
        "company_id": "sh_600691",
        "node_id": "m_phenylenediamine",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_n_butylaldehyde",
        "company_id": "sh_600691",
        "node_id": "n_butylaldehyde",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_isobutylaldehyde",
        "company_id": "sh_600691",
        "node_id": "isobutylaldehyde",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_octanol",
        "company_id": "sh_600691",
        "node_id": "octanol",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_cyclohexanone",
        "company_id": "sh_600691",
        "node_id": "cyclohexanone",
        "activity_type": "produce",
        "weight": 0.05,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    exposures_payload.append({
        "exposure_id": "sh_600691_special_chemical",
        "company_id": "sh_600691",
        "node_id": "special_chemical",
        "activity_type": "produce",
        "weight": 0.1,
        "evidence": make_evidence("尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工")
    })
    # 亚通股份 (600692.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600692",
        "name_zh": "亚通股份",
        "stock_codes": ["600692.SH"],
        "country": "中国",
        "industry": "区域地产",
        "main_business": "主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600692_inland_river_ferry",
        "company_id": "sh_600692",
        "node_id": "inland_river_ferry",
        "activity_type": "operate",
        "weight": 0.35,
        "evidence": make_evidence("主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600692_coastal_chemical_transport",
        "company_id": "sh_600692",
        "node_id": "coastal_chemical_transport",
        "activity_type": "operate",
        "weight": 0.35,
        "evidence": make_evidence("主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600692_taxi_operation_service",
        "company_id": "sh_600692",
        "node_id": "taxi_operation_service",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.")
    })
    # 东百集团 (600693.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600693",
        "name_zh": "东百集团",
        "stock_codes": ["600693.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "主要业务:商业零售业,进出口贸易,房地产开发.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务:商业零售业,进出口贸易,房地产开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600693_department_store",
        "company_id": "sh_600693",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 0.4,
        "evidence": make_evidence("主要业务:商业零售业,进出口贸易,房地产开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600693_trade_agent",
        "company_id": "sh_600693",
        "node_id": "trade_agent",
        "activity_type": "procure",
        "weight": 0.3,
        "evidence": make_evidence("主要业务:商业零售业,进出口贸易,房地产开发.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600693_real_estate_development",
        "company_id": "sh_600693",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.3,
        "evidence": make_evidence("主要业务:商业零售业,进出口贸易,房地产开发.")
    })
    # 大商股份 (600694.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600694",
        "name_zh": "大商股份",
        "stock_codes": ["600694.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "主营业务:商品零售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:商品零售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600694_department_store",
        "company_id": "sh_600694",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:商品零售.")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_093_biz",
            "task_description": f"Batch 093 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次93构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
