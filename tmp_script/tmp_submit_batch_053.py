#!/usr/bin/env python3
"""Submit batch 053 (600155-600165) to Arachne API."""
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
    {"node_id": "securities_service", "name": "证券服务", "entity_type": "service", "description": "证券经纪、投资银行及资产管理服务", "confidence": "HIGH"},
    {"node_id": "plastic_pipe", "name": "塑料管材", "entity_type": "component", "description": "PVC、PE等塑料管道型材产品", "confidence": "HIGH"},
    {"node_id": "ramie_textile", "name": "苎麻纺织", "entity_type": "material", "description": "苎麻纱线、坯布及麻类纺织品", "confidence": "HIGH"},
    {"node_id": "fluorochemical", "name": "氟化工产品", "entity_type": "material", "description": "氟制冷剂、含氟聚合物及氟精细化学品", "confidence": "HIGH"},
    {"node_id": "vaccine", "name": "疫苗", "entity_type": "material", "description": "人用及兽用疫苗制品", "confidence": "HIGH"},
    {"node_id": "blood_product", "name": "血液制品", "entity_type": "material", "description": "人血白蛋白、免疫球蛋白等血液制品", "confidence": "HIGH"},
    {"node_id": "wind_power", "name": "风力发电", "entity_type": "service", "description": "陆上及海上风力发电项目开发与运营", "confidence": "HIGH"},
    {"node_id": "activated_carbon", "name": "活性炭", "entity_type": "material", "description": "木质及煤质活性炭制品", "confidence": "HIGH"},
    {"node_id": "biomaterial", "name": "生物基材料", "entity_type": "material", "description": "生物基可降解材料及合成树脂产品", "confidence": "HIGH"},
]

NEW_EDGES = [
    {"edge_id": "fluorochemical_to_refrigerant", "from_node": "fluorochemical", "to_node": "refrigerant", "edge_type": "material_flow", "description": "氟化工产品用于制造制冷剂"},
    {"edge_id": "blood_product_to_vaccine", "from_node": "blood_product", "to_node": "vaccine", "edge_type": "material_flow", "description": "血液制品与疫苗同属生物制药领域"},
]

COMPANIES = [
    {"company_id": "huachang_yunxin", "name": "华创云信数字技术股份有限公司", "stock_code": "600155.SH", "province": "北京", "city": "北京", "industry": "证券", "main_business": "证券业务和塑料管型材业务"},
    {"company_id": "huasheng", "name": "湖南华升股份有限公司", "stock_code": "600156.SH", "province": "湖南", "city": "长沙", "industry": "纺织", "main_business": "苎麻等麻类及与棉,丝,化纤混纺的纱线,坯布,印染布,服饰"},
    {"company_id": "yongtai_energy", "name": "永泰能源集团股份有限公司", "stock_code": "600157.SH", "province": "山西", "city": "晋中", "industry": "火力发电", "main_business": "煤矿及其他矿山投资,煤炭洗选加工,电厂投资,新能源开发与投资"},
    {"company_id": "zhongti", "name": "中体产业集团股份有限公司", "stock_code": "600158.SH", "province": "天津", "city": "天津", "industry": "文教休闲", "main_business": "承办体育赛事,健身服务,体育场馆经营,体育培训,赛事运营"},
    {"company_id": "dalong_realestate", "name": "北京市大龙伟业房地产开发股份有限公司", "stock_code": "600159.SH", "province": "北京", "city": "北京", "industry": "区域地产", "main_business": "房地产开发和建筑施工"},
    {"company_id": "juhua", "name": "浙江巨化股份有限公司", "stock_code": "600160.SH", "province": "浙江", "city": "衢州", "industry": "化工原料", "main_business": "氟产品,氨产品,氯碱产品,酸产品,农药产品,生物化学制品"},
    {"company_id": "tiantan_bio", "name": "北京天坛生物制品股份有限公司", "stock_code": "600161.SH", "province": "北京", "city": "北京", "industry": "生物制药", "main_business": "疫苗,血制品,诊断试剂等的生产与销售"},
    {"company_id": "xiangjiang_holdings", "name": "深圳香江控股股份有限公司", "stock_code": "600162.SH", "province": "广东", "city": "深圳", "industry": "全国地产", "main_business": "房地产开发,物业管理,物流,会展及仓储服务"},
    {"company_id": "zhongmin_energy", "name": "中闽能源股份有限公司", "stock_code": "600163.SH", "province": "福建", "city": "福州", "industry": "新型电力", "main_business": "陆上风力发电的项目开发,建设及运营"},
    {"company_id": "st_ningke", "name": "宁夏中科生物科技股份有限公司", "stock_code": "600165.SH", "province": "宁夏", "city": "石嘴山", "industry": "化工原料", "main_business": "活性炭制品的生产及销售,干细胞制备和储存,贸易"},
]

EXPOSURES = [
    ("huachang_yunxin", "securities_service", "provide_service", "证券服务商", 0.9),
    ("huachang_yunxin", "plastic_pipe", "produce", "塑料管材生产商", 0.8),
    ("huasheng", "ramie_textile", "produce", "苎麻纺织品生产商", 0.9),
    ("huasheng", "textile_product", "produce", "纺织品生产商", 0.85),
    ("yongtai_energy", "coal", "produce", "煤炭生产商", 0.95),
    ("yongtai_energy", "power_generation", "operate", "火力发电运营商", 0.9),
    ("zhongti", "sports_service", "provide_service", "体育服务运营商", 0.9),
    ("dalong_realestate", "real_estate_development", "operate", "房地产开发运营商", 0.95),
    ("juhua", "fluorochemical", "produce", "氟化工产品生产商", 0.95),
    ("juhua", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.9),
    ("tiantan_bio", "vaccine", "produce", "疫苗生产商", 0.95),
    ("tiantan_bio", "blood_product", "produce", "血液制品生产商", 0.95),
    ("xiangjiang_holdings", "real_estate_development", "operate", "房地产开发运营商", 0.9),
    ("zhongmin_energy", "wind_power", "operate", "风力发电运营商", 0.95),
    ("st_ningke", "activated_carbon", "produce", "活性炭生产商", 0.85),
    ("st_ningke", "biomaterial", "produce", "生物基材料生产商", 0.8),
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
                "evidence": make_evidence(f"tushare batch 053: {n['name']}"),
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
                "evidence": make_evidence(f"tushare batch 053: {e['description']}"),
            })

    return {
        "batch_id": "batch_053",
        "task_description": "Batch 053: 600155-600165 industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 053: {company_id} -> {node_id}"),
        })

    return {
        "batch_id": "batch_053",
        "task_description": "Batch 053: 600155-600165 companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 053 Submission")
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
