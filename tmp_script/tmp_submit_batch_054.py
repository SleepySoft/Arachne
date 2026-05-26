#!/usr/bin/env python3
"""Submit batch 054 (600166-600177) to Arachne API."""
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

NEW_NODES = [
    {"node_id": "automobile", "name": "汽车整车", "entity_type": "system", "description": "乘用车、商用车及新能源汽车整车制造", "confidence": "HIGH"},
    {"node_id": "heating_supply", "name": "供热服务", "entity_type": "service", "description": "城市集中供热、热电联产及清洁能源供暖", "confidence": "HIGH"},
    {"node_id": "water_treatment", "name": "水务处理", "entity_type": "service", "description": "自来水生产供应、污水处理及再生水利用", "confidence": "HIGH"},
    {"node_id": "construction_machinery", "name": "工程机械", "entity_type": "device", "description": "起重机、挖掘机、轧锻设备等重型机械装备", "confidence": "HIGH"},
    {"node_id": "construction_engineering", "name": "建筑工程", "entity_type": "service", "description": "房屋建筑、市政工程及基础设施建设施工", "confidence": "HIGH"},
    {"node_id": "integrated_circuit", "name": "集成电路", "entity_type": "component", "description": "模拟和数模混合集成电路芯片设计与制造", "confidence": "HIGH"},
    {"node_id": "synthetic_diamond", "name": "人造金刚石", "entity_type": "material", "description": "超硬材料、金刚石制品及复合材料", "confidence": "HIGH"},
    {"node_id": "fiberglass", "name": "玻璃纤维", "entity_type": "material", "description": "玻璃纤维及制品、高性能纤维及复合材料", "confidence": "HIGH"},
    {"node_id": "garment", "name": "服装", "entity_type": "material", "description": "西服、衬衫等成衣服饰产品", "confidence": "HIGH"},
]

NEW_EDGES = [
    {"edge_id": "fiberglass_to_composite_material", "from_node": "fiberglass", "to_node": "composite_material", "edge_type": "composition", "description": "玻璃纤维是复合材料的重要增强材料"},
    {"edge_id": "synthetic_diamond_to_cutting_tool", "from_node": "synthetic_diamond", "to_node": "cutting_tool", "edge_type": "material_flow", "description": "人造金刚石用于制造切削工具和磨具"},
    {"edge_id": "construction_machinery_to_construction_engineering", "from_node": "construction_machinery", "to_node": "construction_engineering", "edge_type": "capability_supply", "description": "工程机械为建筑工程提供施工能力"},
]

COMPANIES = [
    {"company_id": "foton_motor", "name": "北汽福田汽车股份有限公司", "stock_code": "600166.SH", "province": "北京", "city": "北京", "industry": "汽车整车", "main_business": "汽车制造,模具,冲压件,发动机,机械电器设备,智能车载设备"},
    {"company_id": "lianmei", "name": "联美量子股份有限公司", "stock_code": "600167.SH", "province": "辽宁", "city": "沈阳", "industry": "供气供热", "main_business": "供热,供水,房屋租赁,市政建设,工程施工,物业管理"},
    {"company_id": "wuhan_water", "name": "武汉三镇实业控股股份有限公司", "stock_code": "600168.SH", "province": "湖北", "city": "武汉", "industry": "水务", "main_business": "自来水生产与供应,城市污水处理"},
    {"company_id": "st_taiyuan", "name": "太原重工股份有限公司", "stock_code": "600169.SH", "province": "山西", "city": "太原", "industry": "工程机械", "main_business": "起重机,挖掘机,轧锻设备,汽车变速箱,油膜轴承"},
    {"company_id": "shanghai_const", "name": "上海建工集团股份有限公司", "stock_code": "600170.SH", "province": "上海", "city": "上海", "industry": "建筑工程", "main_business": "一般民用建筑,工业建筑,市政建筑,建筑装饰工程,总承包工程"},
    {"company_id": "belling", "name": "上海贝岭股份有限公司", "stock_code": "600171.SH", "province": "上海", "city": "上海", "industry": "半导体", "main_business": "模拟和数模混合集成电路及系统解决方案"},
    {"company_id": "yellow_river", "name": "河南黄河旋风股份有限公司", "stock_code": "600172.SH", "province": "河南", "city": "许昌", "industry": "矿物制品", "main_business": "人造金刚石,建筑机械,金刚石制品"},
    {"company_id": "wolong_new_energy", "name": "卧龙新能源集团股份有限公司", "stock_code": "600173.SH", "province": "浙江", "city": "绍兴", "industry": "全国地产", "main_business": "房地产开发经营和物业管理"},
    {"company_id": "china_jushi", "name": "中国巨石股份有限公司", "stock_code": "600176.SH", "province": "浙江", "city": "嘉兴", "industry": "玻璃", "main_business": "玻璃纤维的研发,生产与销售"},
    {"company_id": "youngor", "name": "雅戈尔时尚股份有限公司", "stock_code": "600177.SH", "province": "浙江", "city": "宁波", "industry": "服饰", "main_business": "西服,衬衫等服装制造及房地产开发"},
]

EXPOSURES = [
    ("foton_motor", "automobile", "manufacture", "汽车整车制造商", 0.95),
    ("foton_motor", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
    ("foton_motor", "new_energy_vehicle", "manufacture", "新能源汽车制造商", 0.85),
    ("lianmei", "heating_supply", "provide_service", "供热服务供应商", 0.95),
    ("lianmei", "water_supply", "provide_service", "供水服务供应商", 0.85),
    ("wuhan_water", "water_treatment", "provide_service", "水务处理运营商", 0.95),
    ("st_taiyuan", "construction_machinery", "manufacture", "工程机械制造商", 0.9),
    ("st_taiyuan", "special_steel", "produce", "特种钢生产商", 0.85),
    ("shanghai_const", "construction_engineering", "provide_service", "建筑工程承包商", 0.95),
    ("belling", "integrated_circuit", "manufacture", "集成电路制造商", 0.9),
    ("belling", "semiconductor_device", "manufacture", "半导体器件制造商", 0.85),
    ("yellow_river", "synthetic_diamond", "produce", "人造金刚石生产商", 0.95),
    ("yellow_river", "cutting_tool", "manufacture", "切削工具制造商", 0.8),
    ("wolong_new_energy", "real_estate_development", "operate", "房地产开发运营商", 0.9),
    ("wolong_new_energy", "wind_power_equipment", "manufacture", "风电设备制造商", 0.75),
    ("china_jushi", "fiberglass", "produce", "玻璃纤维生产商", 0.95),
    ("china_jushi", "composite_material", "produce", "复合材料生产商", 0.85),
    ("youngor", "garment", "produce", "服装生产商", 0.9),
    ("youngor", "real_estate_development", "operate", "房地产开发运营商", 0.85),
]

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
                "evidence": make_evidence(f"tushare batch 054: {n['name']}"),
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
                "evidence": make_evidence(f"tushare batch 054: {e['description']}"),
            })

    return {
        "batch_id": "batch_054",
        "task_description": "Batch 054: 600166-600177 industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 054: {company_id} -> {node_id}"),
        })

    return {
        "batch_id": "batch_054",
        "task_description": "Batch 054: 600166-600177 companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 054 Submission")
    print("=" * 60)

    graph_batch = build_graph_batch()
    print(f"\nGraph batch: {len(graph_batch['nodes_to_upsert'])} new nodes, {len(graph_batch['edges_to_upsert'])} new edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, text = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {text}")
    else:
        print("Graph batch: nothing new to submit")

    biz_batch = build_business_batch()
    print(f"\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, text = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {text}")

    print("\nDone.")
