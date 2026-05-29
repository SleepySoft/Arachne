#!/usr/bin/env python3
"""Submit batch 083 to Arachne API."""
import json, requests
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=30)
    return r.status_code, r.text if r.status_code not in (200, 201) else r.json()

def make_evidence(quote, source_title="Tushare数据"):
    return [{
        "source_title": source_title,
        "quote": quote,
        "source_reference": "tushare",
        "confidence": "HIGH",
        "recorded_at": datetime.now().isoformat()
    }]

NEW_NODES = [
    {
        "node_id": "film_capacitor",
        "canonical_name_zh": "薄膜电容器",
        "definition": "以金属化薄膜为电介质的电容器，具有自愈性好、可靠性高的特点，广泛用于电子电力领域",
        "entity_type": "component"
    },
    {
        "node_id": "corrugated_paperboard",
        "canonical_name_zh": "箱纸板",
        "definition": "用于制造瓦楞纸箱的纸板材料，由面纸和瓦楞芯纸复合而成",
        "entity_type": "material"
    },
    {
        "node_id": "carton",
        "canonical_name_zh": "纸箱",
        "definition": "由瓦楞纸板制成的包装容器，广泛用于商品运输和储存包装",
        "entity_type": "material"
    },
    {
        "node_id": "medium_thick_plate",
        "canonical_name_zh": "中厚板",
        "definition": "厚度在4.5-60mm之间的钢板，用于造船、桥梁、压力容器等重型结构",
        "entity_type": "material"
    },
    {
        "node_id": "hot_rolled_coil",
        "canonical_name_zh": "热轧卷板",
        "definition": "经热轧工艺生产的卷状钢板，是冷轧板、镀锌板等产品的原料",
        "entity_type": "material"
    },
    {
        "node_id": "financial_software",
        "canonical_name_zh": "金融软件",
        "definition": "用于银行、证券、保险等金融机构业务处理和管理的信息系统软件",
        "entity_type": "service"
    },
    {
        "node_id": "beer",
        "canonical_name_zh": "啤酒",
        "definition": "以大麦芽、啤酒花为主要原料经发酵酿制而成的低酒精度饮料",
        "entity_type": "material"
    },
    {
        "node_id": "coal_railway_transport",
        "canonical_name_zh": "煤炭铁路运输",
        "definition": "通过铁路专用线或公共铁路网络进行煤炭长距离运输的物流服务",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "film_capacitor_to_electronic_device",
        "from_node": "film_capacitor",
        "to_node": "electronic_device",
        "edge_type": "composition",
        "description": "薄膜电容器是电子电力设备中储存和调节电能的核心元件"
    },
    {
        "edge_id": "corrugated_paperboard_to_carton",
        "from_node": "corrugated_paperboard",
        "to_node": "carton",
        "edge_type": "material_flow",
        "description": "箱纸板经裁切折叠后制成纸箱包装容器"
    },
    {
        "edge_id": "hot_rolled_coil_to_automobile",
        "from_node": "hot_rolled_coil",
        "to_node": "automobile",
        "edge_type": "material_flow",
        "description": "热轧卷板经冷轧等深加工后用于制造汽车车身和零部件"
    }
]

COMPANIES = [
    {
        "company_id": "faratronic",
        "name_zh": "厦门法拉电子股份有限公司",
        "stock_code": "600563.SH",
        "province": "福建",
        "city": "厦门市",
        "industry": "元器件",
        "main_business": "薄膜电容器,变压器及金属化膜等"
    },
    {
        "company_id": "jichuan",
        "name_zh": "湖北济川药业股份有限公司",
        "stock_code": "600566.SH",
        "province": "湖北",
        "city": "黄冈市",
        "industry": "中成药",
        "main_business": "药品的研发,生产和销售"
    },
    {
        "company_id": "shan_ying",
        "name_zh": "山鹰国际控股股份公司",
        "stock_code": "600567.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "造纸",
        "main_business": "箱纸板,纸箱"
    },
    {
        "company_id": "st_zhongzhu",
        "name_zh": "中珠医疗控股股份有限公司",
        "stock_code": "600568.SH",
        "province": "湖北",
        "city": "潜江市",
        "industry": "医疗保健",
        "main_business": "医疗,医药和房地产"
    },
    {
        "company_id": "anyang_steel",
        "name_zh": "安阳钢铁股份有限公司",
        "stock_code": "600569.SH",
        "province": "河南",
        "city": "安阳市",
        "industry": "普钢",
        "main_business": "中厚板,热轧卷板,高速线材,建材,型材等"
    },
    {
        "company_id": "hundsun",
        "name_zh": "恒生电子股份有限公司",
        "stock_code": "600570.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "软件服务",
        "main_business": "软件及服务,系统集成,硬件销售"
    },
    {
        "company_id": "sunyar",
        "name_zh": "信雅达科技股份有限公司",
        "stock_code": "600571.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "软件服务",
        "main_business": "电子影像处理系统,客户服务中心系统,计算机主机通讯安全系统"
    },
    {
        "company_id": "conba",
        "name_zh": "浙江康恩贝制药股份有限公司",
        "stock_code": "600572.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "中成药",
        "main_business": "以现代植物药为核心,特色化学药为重要支持的产品结构"
    },
    {
        "company_id": "huiquan",
        "name_zh": "福建省燕京惠泉啤酒股份有限公司",
        "stock_code": "600573.SH",
        "province": "福建",
        "city": "泉州市",
        "industry": "啤酒",
        "main_business": "啤酒的生产与销售"
    },
    {
        "company_id": "huaihe_energy",
        "name_zh": "淮河能源(集团)股份有限公司",
        "stock_code": "600575.SH",
        "province": "安徽",
        "city": "淮南市",
        "industry": "火力发电",
        "main_business": "煤炭,集装箱,外贸大宗散货,件杂货等货种的装卸中转以及配煤业务,煤炭铁路运输服务"
    }
]

EXPOSURES = [
    {
        "exposure_id": "faratronic_manufacture_film_capacitor",
        "company_id": "faratronic",
        "node_id": "film_capacitor",
        "activity_type": "manufacture",
        "role": "薄膜电容器制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "faratronic_produce_metallized_film",
        "company_id": "faratronic",
        "node_id": "metallized_film",
        "activity_type": "produce",
        "role": "金属化膜生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "jichuan_produce_pharmaceutical",
        "company_id": "jichuan",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jichuan_produce_chinese_patent_medicine",
        "company_id": "jichuan",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "shan_ying_produce_corrugated_paperboard",
        "company_id": "shan_ying",
        "node_id": "corrugated_paperboard",
        "activity_type": "produce",
        "role": "箱纸板生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shan_ying_produce_carton",
        "company_id": "shan_ying",
        "node_id": "carton",
        "activity_type": "produce",
        "role": "纸箱生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shan_ying_produce_paper",
        "company_id": "shan_ying",
        "node_id": "paper",
        "activity_type": "produce",
        "role": "造纸商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_zhongzhu_provide_service_medical_service",
        "company_id": "st_zhongzhu",
        "node_id": "medical_service",
        "activity_type": "provide_service",
        "role": "医疗服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_zhongzhu_produce_pharmaceutical",
        "company_id": "st_zhongzhu",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_zhongzhu_operate_real_estate_development",
        "company_id": "st_zhongzhu",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "anyang_steel_produce_medium_thick_plate",
        "company_id": "anyang_steel",
        "node_id": "medium_thick_plate",
        "activity_type": "produce",
        "role": "中厚板生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "anyang_steel_produce_hot_rolled_coil",
        "company_id": "anyang_steel",
        "node_id": "hot_rolled_coil",
        "activity_type": "produce",
        "role": "热轧卷板生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "anyang_steel_produce_high_speed_wire_rod",
        "company_id": "anyang_steel",
        "node_id": "high_speed_wire_rod",
        "activity_type": "produce",
        "role": "高速线材生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "anyang_steel_produce_steel",
        "company_id": "anyang_steel",
        "node_id": "steel",
        "activity_type": "produce",
        "role": "钢材生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "hundsun_provide_service_financial_software",
        "company_id": "hundsun",
        "node_id": "financial_software",
        "activity_type": "provide_service",
        "role": "金融软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "hundsun_provide_service_system_integration",
        "company_id": "hundsun",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "hundsun_provide_service_software",
        "company_id": "hundsun",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "sunyar_provide_service_electronic_image_processing",
        "company_id": "sunyar",
        "node_id": "electronic_image_processing",
        "activity_type": "provide_service",
        "role": "电子影像处理系统服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "sunyar_provide_service_customer_service_system",
        "company_id": "sunyar",
        "node_id": "customer_service_system",
        "activity_type": "provide_service",
        "role": "客户服务中心系统服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "sunyar_provide_service_software",
        "company_id": "sunyar",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "conba_produce_modern_botanical_medicine",
        "company_id": "conba",
        "node_id": "modern_botanical_medicine",
        "activity_type": "produce",
        "role": "现代植物药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "conba_produce_chemical_drug",
        "company_id": "conba",
        "node_id": "chemical_drug",
        "activity_type": "produce",
        "role": "化学药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "conba_produce_chinese_patent_medicine",
        "company_id": "conba",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "huiquan_produce_beer",
        "company_id": "huiquan",
        "node_id": "beer",
        "activity_type": "produce",
        "role": "啤酒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "huiquan_produce_beverage",
        "company_id": "huiquan",
        "node_id": "beverage",
        "activity_type": "produce",
        "role": "饮料生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "huaihe_energy_operate_coal",
        "company_id": "huaihe_energy",
        "node_id": "coal",
        "activity_type": "operate",
        "role": "煤炭经营商",
        "weight": 0.95
    },
    {
        "exposure_id": "huaihe_energy_operate_coal_railway_transport",
        "company_id": "huaihe_energy",
        "node_id": "coal_railway_transport",
        "activity_type": "operate",
        "role": "煤炭铁路运输运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "huaihe_energy_operate_bulk_cargo_handling",
        "company_id": "huaihe_energy",
        "node_id": "bulk_cargo_handling",
        "activity_type": "operate",
        "role": "大宗散货装卸运营商",
        "weight": 0.85
    }
]

def build_graph_batch():
    nodes_to_upsert = []
    for n in NEW_NODES:
        nodes_to_upsert.append({
            "node_id": n["node_id"],
            "canonical_name_zh": n["canonical_name_zh"],
            "canonical_name_en": n.get("canonical_name_en"),
            "definition": n["definition"],
            "entity_type": n["entity_type"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 083: " + n["canonical_name_zh"]),
        })
    edges_to_upsert = []
    for e in NEW_EDGES:
        edges_to_upsert.append({
            "edge_id": e["edge_id"],
            "from_node": e["from_node"],
            "to_node": e["to_node"],
            "edge_namespace": "industrial_flow",
            "edge_type": e["edge_type"],
            "description": e["description"],
            "confidence": "HIGH",
            "evidence": make_evidence(f"tushare batch 083: " + e["description"]),
        })
    return {
        "batch_id": "batch_083",
        "task_description": "Batch 083: industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

def build_business_batch():
    companies_to_upsert = []
    for c in COMPANIES:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "name_en": c.get("name_en"),
            "stock_codes": [c["stock_code"]],
            "country": "CN",
            "province": c["province"],
            "city": c["city"],
            "industry": c["industry"],
            "main_business": c["main_business"],
            "company_type": "public",
            "status": "ACTIVE",
            "evidence": make_evidence("tushare: " + c["main_business"]),
        })
    exposures_to_upsert = []
    for exp in EXPOSURES:
        exposures_to_upsert.append({
            "exposure_id": exp["exposure_id"],
            "company_id": exp["company_id"],
            "node_id": exp["node_id"],
            "activity_type": exp["activity_type"],
            "role": exp["role"],
            "weight": exp["weight"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 083: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_083",
        "task_description": "Batch 083: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 083 Submission")
    print("=" * 60)
    graph_batch = build_graph_batch()
    print(f"\nGraph batch: {len(graph_batch['nodes_to_upsert'])} nodes, {len(graph_batch['edges_to_upsert'])} edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, resp = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {resp}")
    else:
        print("Graph batch: nothing to submit")
    biz_batch = build_business_batch()
    print(f"\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, resp = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {resp}")
    print("\nDone.")
