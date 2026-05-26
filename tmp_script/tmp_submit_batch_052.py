#!/usr/bin/env python3
"""Submit batch 052 (600136-600153) to Arachne API."""
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
    {"node_id": "film_tv", "name": "影视传媒", "entity_type": "service", "description": "电视剧、电影及影视节目的制作与发行服务", "confidence": "HIGH"},
    {"node_id": "sports_service", "name": "体育服务", "entity_type": "service", "description": "体育赛事运营、体育场馆管理及体育经纪服务", "confidence": "HIGH"},
    {"node_id": "underwear", "name": "内衣", "entity_type": "material", "description": "针织内衣及贴身服饰产品", "confidence": "HIGH"},
    {"node_id": "tourism_service", "name": "旅游服务", "entity_type": "service", "description": "旅行社、旅游线路及旅游相关配套服务", "confidence": "HIGH"},
    {"node_id": "automobile_clutch", "name": "汽车离合器", "entity_type": "component", "description": "汽车传动系统中的离合器总成及零部件", "confidence": "HIGH"},
    {"node_id": "clean_energy_supply", "name": "清洁能源供应", "entity_type": "service", "description": "清洁供能项目投资、建设及运营服务", "confidence": "HIGH"},
    {"node_id": "shipbuilding", "name": "船舶制造", "entity_type": "system", "description": "民用及军用船舶的设计、建造与修理", "confidence": "HIGH"},
    {"node_id": "solar_cell", "name": "太阳能电池", "entity_type": "component", "description": "硅片、电池片及光伏组件的制造与销售", "confidence": "HIGH"},
    {"node_id": "consumer_battery", "name": "消费类电池", "entity_type": "component", "description": "聚合物电池、铝壳电池等消费电子产品用电池", "confidence": "HIGH"},
    {"node_id": "supply_chain_service", "name": "供应链服务", "entity_type": "service", "description": "大宗商品采购、分销及供应链管理服务", "confidence": "HIGH"},
]

NEW_EDGES = [
    {"edge_id": "solar_cell_to_solar_panel", "from_node": "solar_cell", "to_node": "solar_panel", "edge_type": "composition", "description": "太阳能电池片组装成太阳能板"},
    {"edge_id": "automobile_clutch_to_automobile", "from_node": "automobile_clutch", "to_node": "automobile", "edge_type": "composition", "description": "汽车离合器是汽车传动系统的组成部分"},
]

COMPANIES = [
    {"company_id": "st_mingcheng", "name": "武汉明诚文化体育集团股份有限公司", "stock_code": "600136.SH", "province": "湖北", "city": "武汉", "industry": "房产服务", "main_business": "影视产品制作销售及发行,艺人经纪,体育营销,体育版权贸易,体育场馆运营,赛事运营"},
    {"company_id": "langsha", "name": "四川浪莎控股股份有限公司", "stock_code": "600137.SH", "province": "四川", "city": "宜宾", "industry": "服饰", "main_business": "针织内衣,针织面料制造销售"},
    {"company_id": "cyts", "name": "中青旅控股股份有限公司", "stock_code": "600138.SH", "province": "北京", "city": "北京", "industry": "旅游景点", "main_business": "旅游服务业,科技产品销售及技术服务"},
    {"company_id": "xingfa_group", "name": "湖北兴发化工集团股份有限公司", "stock_code": "600141.SH", "province": "湖北", "city": "宜昌", "industry": "农药化肥", "main_business": "三聚磷酸钠和六偏磷酸钠等磷酸盐产品的生产和销售"},
    {"company_id": "changchun_yidong", "name": "长春一东离合器股份有限公司", "stock_code": "600148.SH", "province": "吉林", "city": "长春", "industry": "汽车配件", "main_business": "汽车离合器的研发、生产与销售"},
    {"company_id": "langfang_dev", "name": "廊坊发展股份有限公司", "stock_code": "600149.SH", "province": "河北", "city": "廊坊", "industry": "综合类", "main_business": "贸易业务,租赁业务,拓展清洁供能项目"},
    {"company_id": "cssc", "name": "中国船舶工业股份有限公司", "stock_code": "600150.SH", "province": "上海", "city": "上海", "industry": "船舶", "main_business": "造船业务,修船业务,动力业务,海洋工程,机电设备"},
    {"company_id": "aerospace_mech", "name": "上海航天汽车机电股份有限公司", "stock_code": "600151.SH", "province": "上海", "city": "上海", "industry": "汽车配件", "main_business": "硅片,电池片,组件环节的技术研发,制造以及销售,电站投资,开发,EPC建设"},
    {"company_id": "victor_tech", "name": "维科技术股份有限公司", "stock_code": "600152.SH", "province": "浙江", "city": "宁波", "industry": "电气设备", "main_business": "消费类电池和小动力电池的研发,生产和销售"},
    {"company_id": "cnd", "name": "厦门建发股份有限公司", "stock_code": "600153.SH", "province": "福建", "city": "厦门", "industry": "仓储物流", "main_business": "以供应链运营和房地产开发为主业的现代服务型企业"},
]

EXPOSURES = [
    ("st_mingcheng", "film_tv", "provide_service", "影视传媒服务商", 0.85),
    ("st_mingcheng", "sports_service", "provide_service", "体育服务运营商", 0.8),
    ("langsha", "underwear", "produce", "内衣制造商", 0.9),
    ("langsha", "textile_product", "produce", "纺织品生产商", 0.85),
    ("cyts", "tourism_service", "provide_service", "旅游服务提供商", 0.95),
    ("xingfa_group", "phosphorus_chemical", "produce", "磷化工产品生产商", 0.95),
    ("xingfa_group", "chemical_fertilizer", "produce", "化学肥料生产商", 0.9),
    ("changchun_yidong", "automobile_clutch", "manufacture", "汽车离合器制造商", 0.95),
    ("changchun_yidong", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
    ("langfang_dev", "trade_agent", "provide_service", "贸易及供能服务商", 0.8),
    ("langfang_dev", "clean_energy_supply", "provide_service", "清洁能源供应商", 0.75),
    ("cssc", "shipbuilding", "manufacture", "船舶制造商", 0.95),
    ("cssc", "ship_accessory", "manufacture", "船舶配件制造商", 0.85),
    ("aerospace_mech", "solar_cell", "manufacture", "太阳能电池制造商", 0.9),
    ("aerospace_mech", "automobile_part", "manufacture", "汽车零部件制造商", 0.8),
    ("victor_tech", "consumer_battery", "manufacture", "消费类电池制造商", 0.9),
    ("victor_tech", "lithium_battery", "manufacture", "锂电池制造商", 0.85),
    ("cnd", "supply_chain_service", "provide_service", "供应链服务商", 0.95),
    ("cnd", "real_estate_development", "operate", "房地产开发运营商", 0.85),
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
                "evidence": make_evidence(f"tushare batch 052: {n['name']}"),
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
                "evidence": make_evidence(f"tushare batch 052: {e['description']}"),
            })

    return {
        "batch_id": "batch_052",
        "task_description": "Batch 052: 600136-600153 industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 052: {company_id} -> {node_id}"),
        })

    return {
        "batch_id": "batch_052",
        "task_description": "Batch 052: 600136-600153 companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 052 Submission")
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
