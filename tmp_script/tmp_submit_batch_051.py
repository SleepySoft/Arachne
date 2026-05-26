#!/usr/bin/env python3
"""Submit batch 051 (600125-600135) to Arachne API."""
import json, requests
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_get(path):
    r = requests.get(f"{BASE}/{path}", timeout=10)
    return r.json() if r.status_code == 200 else None

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=30)
    return r.status_code, r.text

def make_evidence(quote, source="tushare"):
    return [{
        "evidence_id": f"ev_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(quote) & 0xFFFFFF:06x}",
        "source_text": quote,
        "source_reference": source,
        "confidence": "MEDIUM",
        "recorded_at": datetime.now().isoformat()
    }]

def load_existing():
    with open("tmp_existing_nodes.json", "r", encoding="utf-8") as f:
        nodes = set(json.load(f))
    with open("tmp_existing_edges.json", "r", encoding="utf-8") as f:
        edges = set(json.load(f))
    return nodes, edges

EXISTING_NODES, EXISTING_EDGES = load_existing()

# =============================================================================
# BATCH 051 DATA
# =============================================================================

NEW_NODES = [
    {"node_id": "rail_logistics", "name": "铁路物流", "entity_type": "service", "description": "铁路货运及物流运输服务", "confidence": "HIGH"},
    {"node_id": "rice", "name": "大米", "entity_type": "material", "description": "稻谷加工而成的食用大米", "confidence": "HIGH"},
    {"node_id": "flour", "name": "面粉", "entity_type": "material", "description": "小麦加工而成的食用面粉", "confidence": "HIGH"},
    {"node_id": "edible_oil", "name": "食用油", "entity_type": "material", "description": "植物或动物油脂加工而成的食用油脂", "confidence": "HIGH"},
    {"node_id": "trade_agent", "name": "贸易代理", "entity_type": "service", "description": "商品进出口代理及贸易经纪服务", "confidence": "HIGH"},
    {"node_id": "mobile_phone", "name": "移动电话", "entity_type": "device", "description": "便携式无线通信终端设备", "confidence": "HIGH"},
    {"node_id": "beer", "name": "啤酒", "entity_type": "material", "description": "以麦芽、啤酒花等发酵酿造的酒精饮料", "confidence": "HIGH"},
    {"node_id": "tech_park", "name": "科技园区", "entity_type": "infrastructure", "description": "集聚科技企业的产业园区基础设施", "confidence": "HIGH"},
    {"node_id": "environmental_service", "name": "环保服务", "entity_type": "service", "description": "大气污染治理、环保咨询及环境治理服务", "confidence": "HIGH"},
    {"node_id": "photographic_film", "name": "感光胶片", "entity_type": "material", "description": "用于摄影成像的感光材料", "confidence": "HIGH"},
    {"node_id": "solar_pv_material", "name": "光伏材料", "entity_type": "material", "description": "太阳能电池用硅片、电池片及组件材料", "confidence": "HIGH"},
]

NEW_EDGES = [
    {"edge_id": "rice_to_flour", "from_node": "rice", "to_node": "flour", "edge_type": "material_flow", "description": "稻谷与小麦均为粮食原料，可并行加工成不同主食产品"},
    {"edge_id": "solar_pv_material_to_photovoltaic_cell", "from_node": "solar_pv_material", "to_node": "photovoltaic_cell", "edge_type": "composition", "description": "光伏材料构成太阳能电池组件"},
]

COMPANIES = [
    {"company_id": "tielong_logistics", "name": "中铁铁龙集装箱物流股份有限公司", "stock_code": "600125.SH", "province": "辽宁", "city": "大连", "industry": "铁路物流", "main_business": "铁路客运业务,铁路货运及延伸服务业务,混凝土生产,房地产业务"},
    {"company_id": "hangzhou_steel", "name": "杭州钢铁股份有限公司", "stock_code": "600126.SH", "province": "浙江", "city": "杭州", "industry": "普钢", "main_business": "棒材,线材,带钢,型材,轻轨等钢铁及其压延产品的生产和销售"},
    {"company_id": "jinjian_rice", "name": "金健米业股份有限公司", "stock_code": "600127.SH", "province": "湖南", "city": "常德", "industry": "农业综合", "main_business": "大米,面粉,面条,食用油的生产与销售"},
    {"company_id": "suhao_hongye", "name": "苏豪弘业股份有限公司", "stock_code": "600128.SH", "province": "江苏", "city": "南京", "industry": "商贸代理", "main_business": "服装,玩具,帽类产品,手套,柳编制品,箱包,木雕的进出口贸易"},
    {"company_id": "taiji_group", "name": "重庆太极实业(集团)股份有限公司", "stock_code": "600129.SH", "province": "重庆", "city": "重庆", "industry": "中成药", "main_business": "曲美,急支糖浆,补肾益寿胶囊,藿香正气口服液等中成药的生产与销售"},
    {"company_id": "bird_mobile", "name": "宁波波导股份有限公司", "stock_code": "600130.SH", "province": "浙江", "city": "宁波", "industry": "元器件", "main_business": "手机主板及整机的研发,生产和销售"},
    {"company_id": "sgcc_ict", "name": "国网信息通信股份有限公司", "stock_code": "600131.SH", "province": "四川", "city": "阿坝", "industry": "通信设备", "main_business": "水利发电,配套发展与水电有关的输供电业务,电力工程勘察设计咨询"},
    {"company_id": "chongqing_beer", "name": "重庆啤酒股份有限公司", "stock_code": "600132.SH", "province": "重庆", "city": "重庆", "industry": "啤酒", "main_business": "啤酒的生产与销售"},
    {"company_id": "donghu_hitech", "name": "武汉东湖高新集团股份有限公司", "stock_code": "600133.SH", "province": "湖北", "city": "武汉", "industry": "环境保护", "main_business": "科技园区,发电,火电厂烟气脱硫服务等"},
    {"company_id": "lucky_film", "name": "乐凯胶片股份有限公司", "stock_code": "600135.SH", "province": "河北", "city": "保定", "industry": "塑料", "main_business": "彩纸,彩卷,光伏材料,新型膜材料的生产与销售"},
]

EXPOSURES = [
    ("tielong_logistics", "rail_logistics", "operate", "铁路物流运营商", 0.9),
    ("tielong_logistics", "logistics_service", "provide_service", "综合物流服务商", 0.8),
    ("hangzhou_steel", "steel_plate", "produce", "钢铁板材生产商", 0.95),
    ("jinjian_rice", "rice", "produce", "大米生产商", 0.9),
    ("jinjian_rice", "flour", "produce", "面粉生产商", 0.85),
    ("jinjian_rice", "edible_oil", "produce", "食用油生产商", 0.85),
    ("suhao_hongye", "trade_agent", "provide_service", "进出口贸易代理商", 0.9),
    ("suhao_hongye", "textile_product", "trade", "纺织品贸易商", 0.8),
    ("taiji_group", "chinese_patent_medicine", "produce", "中成药生产商", 0.95),
    ("bird_mobile", "mobile_phone", "manufacture", "移动电话制造商", 0.9),
    ("sgcc_ict", "power_supply", "provide_service", "电力供应及通信服务商", 0.9),
    ("sgcc_ict", "communication_equipment", "manufacture", "通信设备制造商", 0.8),
    ("chongqing_beer", "beer", "produce", "啤酒生产商", 0.95),
    ("donghu_hitech", "tech_park", "operate", "科技园区运营商", 0.85),
    ("donghu_hitech", "environmental_service", "provide_service", "环保服务提供商", 0.8),
    ("donghu_hitech", "power_generation", "operate", "火力发电运营商", 0.75),
    ("lucky_film", "photographic_film", "produce", "感光胶片生产商", 0.85),
    ("lucky_film", "solar_pv_material", "produce", "光伏材料生产商", 0.8),
]

# =============================================================================
# BUILD & SUBMIT
# =============================================================================

def build_graph_batch():
    nodes_to_upsert = []
    for n in NEW_NODES:
        if n["node_id"] not in EXISTING_NODES:
            nodes_to_upsert.append({
                "node_id": n["node_id"],
                "name": n["name"],
                "entity_type": n["entity_type"],
                "description": n["description"],
                "confidence": n["confidence"],
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch 051: {n['name']}"),
            })

    edges_to_upsert = []
    for e in NEW_EDGES:
        if e["edge_id"] not in EXISTING_EDGES:
            edges_to_upsert.append({
                "edge_id": e["edge_id"],
                "from_node": e["from_node"],
                "to_node": e["to_node"],
                "edge_namespace": "industrial_flow",
                "edge_type": e["edge_type"],
                "description": e["description"],
                "confidence": "MEDIUM",
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch 051: {e['description']}"),
            })

    return {
        "batch_id": "batch_051",
        "task_description": "Batch 051: 600125-600135 industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

def build_business_batch():
    companies_to_upsert = []
    for c in COMPANIES:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name": c["name"],
            "stock_code": c["stock_code"],
            "country": "中国",
            "province": c["province"],
            "city": c["city"],
            "industry": c["industry"],
            "main_business": c["main_business"],
            "company_type": "listed",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare: {c['main_business']}"),
        })

    exposures_to_upsert = []
    for company_id, node_id, activity, role, weight in EXPOSURES:
        exposure_id = f"{company_id}_{activity}_{node_id}"
        exposures_to_upsert.append({
            "exposure_id": exposure_id,
            "company_id": company_id,
            "node_id": node_id,
            "activity_type": activity,
            "role_description": role,
            "weight": weight,
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 051: {company_id} -> {node_id}"),
        })

    return {
        "batch_id": "batch_051",
        "task_description": "Batch 051: 600125-600135 companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 051 Submission")
    print("=" * 60)

    # Submit graph batch
    graph_batch = build_graph_batch()
    print(f"\nGraph batch: {len(graph_batch['nodes_to_upsert'])} new nodes, {len(graph_batch['edges_to_upsert'])} new edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, text = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {text}")
    else:
        print("Graph batch: nothing new to submit")

    # Submit business batch
    biz_batch = build_business_batch()
    print(f"\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, text = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {text}")

    print("\nDone.")
