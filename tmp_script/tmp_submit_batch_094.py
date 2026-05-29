#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch 94."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_094.json"

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
    if "turbocharger" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "turbocharger",
            "canonical_name_zh": "涡轮增压器",
            "canonical_name_en": "Turbocharger",
            "definition": "利用发动机排气能量驱动涡轮，压缩进气以提高发动机功率密度的增压装置",
            "entity_type": "component",
            "evidence": make_evidence("涡轮增压器", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: turbocharger")
    if "engine_valve" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "engine_valve",
            "canonical_name_zh": "发动机进排气门",
            "canonical_name_en": "Engine Valve",
            "definition": "控制发动机气缸进气和排气的关键部件，由气门、气门座、弹簧等组成",
            "entity_type": "component",
            "evidence": make_evidence("发动机进排气门", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: engine_valve")
    if "engine_cooling_fan" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "engine_cooling_fan",
            "canonical_name_zh": "发动机冷却风扇",
            "canonical_name_en": "Engine Cooling Fan",
            "definition": "用于强制空气流过散热器，帮助发动机维持正常工作温度的风扇组件",
            "entity_type": "component",
            "evidence": make_evidence("冷却风扇等发动机零部件", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: engine_cooling_fan")
    if "led_epitaxial_wafer" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "led_epitaxial_wafer",
            "canonical_name_zh": "LED外延片",
            "canonical_name_en": "LED Epitaxial Wafer",
            "definition": "在蓝宝石或碳化硅衬底上通过外延生长工艺制备的含有发光层结构的晶圆片",
            "entity_type": "material",
            "evidence": make_evidence("LED外延片及芯片的研发,生产和销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: led_epitaxial_wafer")
    if "led_chip" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "led_chip",
            "canonical_name_zh": "LED芯片",
            "canonical_name_en": "LED Chip",
            "definition": "将外延片经光刻、刻蚀、蒸镀等工艺制成的具有电致发光功能的半导体芯片",
            "entity_type": "component",
            "evidence": make_evidence("LED外延片及芯片的研发,生产和销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: led_chip")
    if "scenic_area_operation_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "scenic_area_operation_service",
            "canonical_name_zh": "景区运营管理服务",
            "canonical_name_en": "Scenic Area Operation Service",
            "definition": "为旅游景区提供日常运营、游客服务、设施维护、营销推广等综合管理服务",
            "entity_type": "service",
            "evidence": make_evidence("景区运营管理业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: scenic_area_operation_service")
    if "travel_agency_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "travel_agency_service",
            "canonical_name_zh": "旅行社服务",
            "canonical_name_en": "Travel Agency Service",
            "definition": "为游客提供旅游线路设计、票务预订、导游接待等综合性旅行服务",
            "entity_type": "service",
            "evidence": make_evidence("旅行社业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: travel_agency_service")
    if "performance_service" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "performance_service",
            "canonical_name_zh": "演出演艺服务",
            "canonical_name_en": "Performance Service",
            "definition": "为景区或文化场所提供文艺演出、演艺活动策划及执行的服务业务",
            "entity_type": "service",
            "evidence": make_evidence("演出演艺业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: performance_service")
    if "cultural_tourism_product" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "cultural_tourism_product",
            "canonical_name_zh": "文化旅游商品",
            "canonical_name_en": "Cultural Tourism Product",
            "definition": "具有地域文化特色的旅游纪念商品，包括文创产品、地方特产、手工艺品等",
            "entity_type": "material",
            "evidence": make_evidence("文化旅游商品业务", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: cultural_tourism_product")
    if "lcd_substrate_glass" not in existing_nodes:
        nodes_to_create.append({
            "node_id": "lcd_substrate_glass",
            "canonical_name_zh": "液晶基板玻璃",
            "canonical_name_en": "LCD Substrate Glass",
            "definition": "用于液晶显示面板制造的特种玻璃基板，需具备高平整度、低热膨胀系数等特性",
            "entity_type": "material",
            "evidence": make_evidence("液晶基板玻璃的研发,生产与销售", "公司主营业务描述"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Node exists: lcd_substrate_glass")

    # ---- Graph edges ----
    edges_to_create = []
    if ("turbocharger", "auto_engine", "composition") not in existing_edges and "turbocharger" in existing_nodes and "auto_engine" in existing_nodes:
        edges_to_create.append({
            "edge_id": "turbocharger_to_engine",
            "from_node": "turbocharger",
            "to_node": "auto_engine",
            "edge_namespace": "industrial_flow",
            "edge_type": "composition",
            "description": "涡轮增压器是汽车发动机总成的组成部分",
            "evidence": make_evidence("涡轮增压器等发动机零部件"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: turbocharger_to_engine")
    if ("engine_valve", "auto_engine", "composition") not in existing_edges and "engine_valve" in existing_nodes and "auto_engine" in existing_nodes:
        edges_to_create.append({
            "edge_id": "engine_valve_to_engine",
            "from_node": "engine_valve",
            "to_node": "auto_engine",
            "edge_namespace": "industrial_flow",
            "edge_type": "composition",
            "description": "进排气门是汽车发动机总成的组成部分",
            "evidence": make_evidence("发动机进排气门等发动机零部件"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: engine_valve_to_engine")
    if ("engine_cooling_fan", "auto_engine", "composition") not in existing_edges and "engine_cooling_fan" in existing_nodes and "auto_engine" in existing_nodes:
        edges_to_create.append({
            "edge_id": "cooling_fan_to_engine",
            "from_node": "engine_cooling_fan",
            "to_node": "auto_engine",
            "edge_namespace": "industrial_flow",
            "edge_type": "composition",
            "description": "冷却风扇是汽车发动机总成的组成部分",
            "evidence": make_evidence("冷却风扇等发动机零部件"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: cooling_fan_to_engine")
    if ("led_epitaxial_wafer", "led_chip", "material_flow") not in existing_edges and "led_epitaxial_wafer" in existing_nodes and "led_chip" in existing_nodes:
        edges_to_create.append({
            "edge_id": "led_wafer_to_chip",
            "from_node": "led_epitaxial_wafer",
            "to_node": "led_chip",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "LED外延片经加工制成LED芯片",
            "evidence": make_evidence("LED外延片及芯片的研发,生产和销售"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: led_wafer_to_chip")
    if ("lcd_substrate_glass", "lcd_panel", "material_flow") not in existing_edges and "lcd_substrate_glass" in existing_nodes and "lcd_panel" in existing_nodes:
        edges_to_create.append({
            "edge_id": "lcd_glass_to_panel",
            "from_node": "lcd_substrate_glass",
            "to_node": "lcd_panel",
            "edge_namespace": "industrial_flow",
            "edge_type": "material_flow",
            "description": "液晶基板玻璃是液晶显示面板的核心基材",
            "evidence": make_evidence("液晶基板玻璃的研发,生产与销售"),
            "confidence": "HIGH", "status": "ACTIVE"
        })
    else:
        print(f"  Edge skip: lcd_glass_to_panel")

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {
            "batch_id": f"batch_094_graph",
            "task_description": f"Batch 094 industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次94构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}]
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
    # *ST岩石 (600696.SH)
    c = companies[0]
    companies_payload.append({
        "company_id": "sh_600696",
        "name_zh": "*ST岩石",
        "stock_codes": ["600696.SH"],
        "country": "中国",
        "industry": "白酒",
        "main_business": "主营业务:房地产综合开发,商品房销售,商场物业出租及相应物业管理.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:房地产综合开发,商品房销售,商场物业出租及相应物业管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600696_real_estate_development",
        "company_id": "sh_600696",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.6,
        "evidence": make_evidence("主营业务:房地产综合开发,商品房销售,商场物业出租及相应物业管理.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600696_commercial_property_operation",
        "company_id": "sh_600696",
        "node_id": "commercial_property_operation",
        "activity_type": "operate",
        "weight": 0.4,
        "evidence": make_evidence("主营业务:房地产综合开发,商品房销售,商场物业出租及相应物业管理.")
    })
    # 欧亚集团 (600697.SH)
    c = companies[1]
    companies_payload.append({
        "company_id": "sh_600697",
        "name_zh": "欧亚集团",
        "stock_codes": ["600697.SH"],
        "country": "中国",
        "industry": "百货",
        "main_business": "主要业务:商业,租赁服务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主要业务:商业,租赁服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600697_department_store",
        "company_id": "sh_600697",
        "node_id": "department_store",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("主要业务:商业,租赁服务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600697_commercial_property_operation",
        "company_id": "sh_600697",
        "node_id": "commercial_property_operation",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("主要业务:商业,租赁服务.")
    })
    # 湖南天雁 (600698.SH)
    c = companies[2]
    companies_payload.append({
        "company_id": "sh_600698",
        "name_zh": "湖南天雁",
        "stock_codes": ["600698.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600698_turbocharger",
        "company_id": "sh_600698",
        "node_id": "turbocharger",
        "activity_type": "produce",
        "weight": 0.4,
        "evidence": make_evidence("涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600698_engine_valve",
        "company_id": "sh_600698",
        "node_id": "engine_valve",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600698_engine_cooling_fan",
        "company_id": "sh_600698",
        "node_id": "engine_cooling_fan",
        "activity_type": "produce",
        "weight": 0.3,
        "evidence": make_evidence("涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售")
    })
    # 均胜电子 (600699.SH)
    c = companies[3]
    companies_payload.append({
        "company_id": "sh_600699",
        "name_zh": "均胜电子",
        "stock_codes": ["600699.SH"],
        "country": "中国",
        "industry": "汽车配件",
        "main_business": "主营业务:汽车零部件",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:汽车零部件")
    })
    exposures_payload.append({
        "exposure_id": "sh_600699_automotive_part",
        "company_id": "sh_600699",
        "node_id": "automotive_part",
        "activity_type": "manufacture",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:汽车零部件")
    })
    # 舍得酒业 (600702.SH)
    c = companies[4]
    companies_payload.append({
        "company_id": "sh_600702",
        "name_zh": "舍得酒业",
        "stock_codes": ["600702.SH"],
        "country": "中国",
        "industry": "白酒",
        "main_business": "沱牌酒系列,沱牌大曲系列.主营业务是白酒的制造和销售",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("沱牌酒系列,沱牌大曲系列.主营业务是白酒的制造和销售")
    })
    exposures_payload.append({
        "exposure_id": "sh_600702_baijiu",
        "company_id": "sh_600702",
        "node_id": "baijiu",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("沱牌酒系列,沱牌大曲系列.主营业务是白酒的制造和销售")
    })
    # 三安光电 (600703.SH)
    c = companies[5]
    companies_payload.append({
        "company_id": "sh_600703",
        "name_zh": "三安光电",
        "stock_codes": ["600703.SH"],
        "country": "中国",
        "industry": "半导体",
        "main_business": "主营业务:LED外延片及芯片的研发,生产和销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:LED外延片及芯片的研发,生产和销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600703_led_epitaxial_wafer",
        "company_id": "sh_600703",
        "node_id": "led_epitaxial_wafer",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:LED外延片及芯片的研发,生产和销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600703_led_chip",
        "company_id": "sh_600703",
        "node_id": "led_chip",
        "activity_type": "produce",
        "weight": 0.5,
        "evidence": make_evidence("主营业务:LED外延片及芯片的研发,生产和销售.")
    })
    # 物产中大 (600704.SH)
    c = companies[6]
    companies_payload.append({
        "company_id": "sh_600704",
        "name_zh": "物产中大",
        "stock_codes": ["600704.SH"],
        "country": "中国",
        "industry": "仓储物流",
        "main_business": "外贸,房地产.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("外贸,房地产.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600704_foreign_trade_service",
        "company_id": "sh_600704",
        "node_id": "foreign_trade_service",
        "activity_type": "procure",
        "weight": 0.5,
        "evidence": make_evidence("外贸,房地产.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600704_real_estate_development",
        "company_id": "sh_600704",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.5,
        "evidence": make_evidence("外贸,房地产.")
    })
    # 曲江文旅 (600706.SH)
    c = companies[7]
    companies_payload.append({
        "company_id": "sh_600706",
        "name_zh": "曲江文旅",
        "stock_codes": ["600706.SH"],
        "country": "中国",
        "industry": "旅游景点",
        "main_business": "主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_scenic_area_operation_service",
        "company_id": "sh_600706",
        "node_id": "scenic_area_operation_service",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_hotel_operation_service",
        "company_id": "sh_600706",
        "node_id": "hotel_operation_service",
        "activity_type": "operate",
        "weight": 0.15,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_travel_agency_service",
        "company_id": "sh_600706",
        "node_id": "travel_agency_service",
        "activity_type": "provide_service",
        "weight": 0.15,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_performance_service",
        "company_id": "sh_600706",
        "node_id": "performance_service",
        "activity_type": "provide_service",
        "weight": 0.15,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_cultural_tourism_product",
        "company_id": "sh_600706",
        "node_id": "cultural_tourism_product",
        "activity_type": "procure",
        "weight": 0.15,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600706_scenic_area",
        "company_id": "sh_600706",
        "node_id": "scenic_area",
        "activity_type": "operate",
        "weight": 0.2,
        "evidence": make_evidence("主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.")
    })
    # 彩虹股份 (600707.SH)
    c = companies[8]
    companies_payload.append({
        "company_id": "sh_600707",
        "name_zh": "彩虹股份",
        "stock_codes": ["600707.SH"],
        "country": "中国",
        "industry": "元器件",
        "main_business": "主营业务:液晶基板玻璃的研发,生产与销售.",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:液晶基板玻璃的研发,生产与销售.")
    })
    exposures_payload.append({
        "exposure_id": "sh_600707_lcd_substrate_glass",
        "company_id": "sh_600707",
        "node_id": "lcd_substrate_glass",
        "activity_type": "produce",
        "weight": 1.0,
        "evidence": make_evidence("主营业务:液晶基板玻璃的研发,生产与销售.")
    })
    # 光明地产 (600708.SH)
    c = companies[9]
    companies_payload.append({
        "company_id": "sh_600708",
        "name_zh": "光明地产",
        "stock_codes": ["600708.SH"],
        "country": "中国",
        "industry": "全国地产",
        "main_business": "主营业务:房地产综合开发经营,物流产业链",
        "company_type": "public",
        "status": "ACTIVE",
        "evidence": make_evidence("主营业务:房地产综合开发经营,物流产业链")
    })
    exposures_payload.append({
        "exposure_id": "sh_600708_real_estate_development",
        "company_id": "sh_600708",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "weight": 0.6,
        "evidence": make_evidence("主营业务:房地产综合开发经营,物流产业链")
    })
    exposures_payload.append({
        "exposure_id": "sh_600708_logistics_service",
        "company_id": "sh_600708",
        "node_id": "logistics_service",
        "activity_type": "operate",
        "weight": 0.4,
        "evidence": make_evidence("主营业务:房地产综合开发经营,物流产业链")
    })

    if companies_payload:
        biz_batch = {
            "batch_id": f"batch_094_biz",
            "task_description": f"Batch 094 companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{"source_title": "批次94构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}]
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
