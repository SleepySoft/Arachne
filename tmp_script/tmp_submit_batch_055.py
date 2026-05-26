#!/usr/bin/env python3
"""Submit batch 055 (600178-600188) to Arachne API."""
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
    {"node_id": "auto_engine", "name": "汽车发动机", "entity_type": "component", "description": "汽油、柴油及新能源汽车用发动机总成", "confidence": "HIGH"},
    {"node_id": "container_shipping", "name": "集装箱航运", "entity_type": "service", "description": "国际及国内集装箱海运、多式联运物流服务", "confidence": "HIGH"},
    {"node_id": "tire", "name": "轮胎", "entity_type": "component", "description": "汽车、工程机械用橡胶轮胎产品", "confidence": "HIGH"},
    {"node_id": "copper_clad_laminate", "name": "覆铜板", "entity_type": "component", "description": "印制电路板用覆铜板和粘结片", "confidence": "HIGH"},
    {"node_id": "optical_glass", "name": "光学玻璃", "entity_type": "material", "description": "光学仪器、防务产品用特种玻璃材料", "confidence": "HIGH"},
    {"node_id": "defense_equipment", "name": "防务装备", "entity_type": "system", "description": "军用光电设备及防务系统集成产品", "confidence": "HIGH"},
    {"node_id": "duty_free", "name": "免税商品", "entity_type": "service", "description": "离岛免税、口岸免税及市内免税商品销售", "confidence": "HIGH"},
    {"node_id": "monosodium_glutamate", "name": "味精", "entity_type": "material", "description": "谷氨酸钠调味品及食品配料", "confidence": "HIGH"},
    {"node_id": "water_supply_service", "name": "供水服务", "entity_type": "service", "description": "城市市政供排水及水务基础设施运营", "confidence": "HIGH"},
    {"node_id": "coal_mining", "name": "煤炭开采", "entity_type": "service", "description": "煤炭开采、洗选加工及煤化工", "confidence": "HIGH"},
]

NEW_EDGES = [
    {"edge_id": "auto_engine_to_automobile", "from_node": "auto_engine", "to_node": "automobile", "edge_type": "composition", "description": "汽车发动机是汽车整车的核心组成部件"},
    {"edge_id": "tire_to_automobile", "from_node": "tire", "to_node": "automobile", "edge_type": "composition", "description": "轮胎是汽车整车的关键配套部件"},
    {"edge_id": "copper_clad_laminate_to_pcb", "from_node": "copper_clad_laminate", "to_node": "printed_circuit_board", "edge_type": "composition", "description": "覆铜板是印制电路板的基础材料"},
    {"edge_id": "optical_glass_to_defense_equipment", "from_node": "optical_glass", "to_node": "defense_equipment", "edge_type": "composition", "description": "光学玻璃用于制造防务装备中的光电系统"},
]

COMPANIES = [
    {"company_id": "dongan_power", "name": "哈尔滨东安汽车动力股份有限公司", "stock_code": "600178.SH", "province": "黑龙江", "city": "哈尔滨", "industry": "汽车配件", "main_business": "汽车发动机,变速器,发电机及发电机组的制造与销售"},
    {"company_id": "antong", "name": "安通控股股份有限公司", "stock_code": "600179.SH", "province": "福建", "city": "泉州", "industry": "水运", "main_business": "集装箱物流服务,多式联运综合物流服务"},
    {"company_id": "st_ruimao", "name": "瑞茂通供应链管理股份有限公司", "stock_code": "600180.SH", "province": "山东", "city": "烟台", "industry": "仓储物流", "main_business": "供应链管理服务,煤炭及制品销售,石油制品销售"},
    {"company_id": "giti_tire", "name": "佳通轮胎股份有限公司", "stock_code": "600182.SH", "province": "黑龙江", "city": "牡丹江", "industry": "汽车配件", "main_business": "生产销售轮胎,轮胎原辅材料,生产橡胶工业专用设备"},
    {"company_id": "shengyi_tech", "name": "广东生益科技股份有限公司", "stock_code": "600183.SH", "province": "广东", "city": "东莞", "industry": "元器件", "main_business": "覆铜板和粘结片,印制线路板的设计,生产和销售"},
    {"company_id": "norinco_optical", "name": "北方光电股份有限公司", "stock_code": "600184.SH", "province": "湖北", "city": "襄阳", "industry": "专用机械", "main_business": "光学玻璃,防务产品,光电系统及智能车载设备"},
    {"company_id": "zhuhai_dutyfree", "name": "珠海珠免集团股份有限公司", "stock_code": "600185.SH", "province": "广东", "city": "珠海", "industry": "旅游服务", "main_business": "免税商品销售,房地产开发经营"},
    {"company_id": "lotus_holdings", "name": "莲花控股股份有限公司", "stock_code": "600186.SH", "province": "河南", "city": "周口", "industry": "食品", "main_business": "味精,面粉,小麦淀粉及副产品,热力,电力的生产与销售"},
    {"company_id": "st_guozhong", "name": "黑龙江国中水务股份有限公司", "stock_code": "600187.SH", "province": "黑龙江", "city": "哈尔滨", "industry": "水务", "main_business": "城市市政供排水"},
    {"company_id": "yankuang_energy", "name": "兖矿能源集团股份有限公司", "stock_code": "600188.SH", "province": "山东", "city": "济宁", "industry": "煤炭开采", "main_business": "煤炭开采,洗选加工,销售,煤化工,甲醇的生产与销售,电力"},
]

EXPOSURES = [
    ("dongan_power", "auto_engine", "manufacture", "汽车发动机制造商", 0.95),
    ("dongan_power", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
    ("antong", "container_shipping", "operate", "集装箱航运运营商", 0.95),
    ("antong", "logistics_service", "provide_service", "综合物流服务商", 0.9),
    ("st_ruimao", "supply_chain_service", "provide_service", "供应链服务商", 0.9),
    ("st_ruimao", "coal", "trade", "煤炭贸易商", 0.85),
    ("giti_tire", "tire", "manufacture", "轮胎制造商", 0.95),
    ("shengyi_tech", "copper_clad_laminate", "manufacture", "覆铜板制造商", 0.95),
    ("shengyi_tech", "printed_circuit_board", "manufacture", "印制电路板制造商", 0.9),
    ("norinco_optical", "optical_glass", "produce", "光学玻璃生产商", 0.9),
    ("norinco_optical", "defense_equipment", "manufacture", "防务装备制造商", 0.85),
    ("norinco_optical", "optoelectronic_device", "manufacture", "光电子器件制造商", 0.8),
    ("zhuhai_dutyfree", "duty_free", "operate", "免税商品运营商", 0.95),
    ("zhuhai_dutyfree", "real_estate_development", "operate", "房地产开发运营商", 0.8),
    ("lotus_holdings", "monosodium_glutamate", "produce", "味精生产商", 0.95),
    ("lotus_holdings", "flour", "produce", "面粉生产商", 0.85),
    ("st_guozhong", "water_supply_service", "provide_service", "供水服务运营商", 0.95),
    ("st_guozhong", "water_treatment", "provide_service", "污水处理运营商", 0.9),
    ("yankuang_energy", "coal_mining", "operate", "煤炭开采运营商", 0.95),
    ("yankuang_energy", "coal", "produce", "煤炭生产商", 0.95),
    ("yankuang_energy", "methanol", "produce", "甲醇生产商", 0.85),
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
                "evidence": make_evidence(f"tushare batch 055: {n['name']}"),
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
                "evidence": make_evidence(f"tushare batch 055: {e['description']}"),
            })

    return {
        "batch_id": "batch_055",
        "task_description": "Batch 055: 600178-600188 industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 055: {company_id} -> {node_id}"),
        })

    return {
        "batch_id": "batch_055",
        "task_description": "Batch 055: 600178-600188 companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 055 Submission")
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
