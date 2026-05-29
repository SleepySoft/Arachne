#!/usr/bin/env python3
"""Submit batch 079 to Arachne API."""
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
        "node_id": "graphite_electrode",
        "canonical_name_zh": "石墨电极",
        "definition": "以石油焦、沥青焦为骨料，煤沥青为粘结剂，经高温石墨化制成的导电电极，用于电弧炉炼钢",
        "entity_type": "component"
    },
    {
        "node_id": "carbon_block",
        "canonical_name_zh": "炭块",
        "definition": "以无烟煤、石油焦等为原料经高温焙烧制成的块状炭素制品，用于高炉内衬等",
        "entity_type": "material"
    },
    {
        "node_id": "low_carbon_energy_saving",
        "canonical_name_zh": "低碳节能",
        "definition": "通过技术创新和管理优化减少碳排放、提高能源利用效率的技术和服务体系",
        "entity_type": "service"
    },
    {
        "node_id": "power_grid_smart_operation",
        "canonical_name_zh": "电网智能运维",
        "definition": "利用物联网、大数据和人工智能技术实现电力电网设备的智能监测、诊断和维护",
        "entity_type": "service"
    },
    {
        "node_id": "maotai_liquor",
        "canonical_name_zh": "茅台酒",
        "definition": "中国贵州省茅台镇特产的大曲酱香型白酒，以其独特的酿造工艺和品质闻名",
        "entity_type": "material"
    },
    {
        "node_id": "semiconductor_packaging_mold",
        "canonical_name_zh": "半导体塑封模具",
        "definition": "用于半导体集成电路封装过程中塑料成型的精密模具",
        "entity_type": "component"
    },
    {
        "node_id": "led_bracket",
        "canonical_name_zh": "LED支架",
        "definition": "用于安装和固定LED芯片并提供电气连接的金属支架，是LED封装的关键部件",
        "entity_type": "component"
    },
    {
        "node_id": "aviation_part",
        "canonical_name_zh": "航空零部件",
        "definition": "用于航空器制造和维修的各种金属和非金属零部件，包括结构件、发动机件等",
        "entity_type": "component"
    }
]

NEW_EDGES = [
    {
        "edge_id": "graphite_electrode_to_steel",
        "from_node": "graphite_electrode",
        "to_node": "steel",
        "edge_type": "material_flow",
        "description": "石墨电极是电弧炉炼钢过程中不可替代的导电材料"
    },
    {
        "edge_id": "semiconductor_packaging_mold_to_semiconductor_device",
        "from_node": "semiconductor_packaging_mold",
        "to_node": "semiconductor_device",
        "edge_type": "composition",
        "description": "半导体塑封模具是集成电路封装生产的关键工艺装备"
    },
    {
        "edge_id": "aviation_part_to_aircraft",
        "from_node": "aviation_part",
        "to_node": "aircraft",
        "edge_type": "composition",
        "description": "航空零部件是航空器机体和系统的基本组成单元"
    }
]

COMPANIES = [
    {
        "company_id": "lianhuan_pharma",
        "name_zh": "江苏联环药业股份有限公司",
        "stock_code": "600513.SH",
        "province": "江苏",
        "city": "扬州市",
        "industry": "化学制药",
        "main_business": "敏迪,爱普列特片,达那唑胶囊,联环尔定"
    },
    {
        "company_id": "hainan_airport",
        "name_zh": "海南机场设施股份有限公司",
        "stock_code": "600515.SH",
        "province": "海南",
        "city": "海口市",
        "industry": "机场",
        "main_business": "商业,酒店业,房地产业"
    },
    {
        "company_id": "fangda_carbon",
        "name_zh": "方大炭素新材料科技股份有限公司",
        "stock_code": "600516.SH",
        "province": "甘肃",
        "city": "兰州市",
        "industry": "矿物制品",
        "main_business": "超高功率石墨电极,高功率石墨电极,普通功率石墨电极,炭块"
    },
    {
        "company_id": "sgcc_yingda",
        "name_zh": "国网英大股份有限公司",
        "stock_code": "600517.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "多元金融",
        "main_business": "低碳节能,中低压电气,电网智能运维,电力工程"
    },
    {
        "company_id": "kangmei",
        "name_zh": "康美药业股份有限公司",
        "stock_code": "600518.SH",
        "province": "广东",
        "city": "揭阳市",
        "industry": "中成药",
        "main_business": "络欣平,诺沙,利乐,中药饮片"
    },
    {
        "company_id": "maotai",
        "name_zh": "贵州茅台酒股份有限公司",
        "stock_code": "600519.SH",
        "province": "贵州",
        "city": "遵义市",
        "industry": "白酒",
        "main_business": "高度茅台酒,低度茅台酒"
    },
    {
        "company_id": "sanjiatech",
        "name_zh": "铜陵三佳科技股份有限公司",
        "stock_code": "600520.SH",
        "province": "安徽",
        "city": "铜陵市",
        "industry": "半导体",
        "main_business": "半导体集成电路塑封模具,化学建材挤出模具,LED支架"
    },
    {
        "company_id": "huahai",
        "name_zh": "浙江华海药业股份有限公司",
        "stock_code": "600521.SH",
        "province": "浙江",
        "city": "台州市",
        "industry": "化学制药",
        "main_business": "普利类产品,沙坦类产品,抗忧郁类产品,抗组胺类产品,制剂"
    },
    {
        "company_id": "zhongtian",
        "name_zh": "江苏中天科技股份有限公司",
        "stock_code": "600522.SH",
        "province": "江苏",
        "city": "南通市",
        "industry": "通信设备",
        "main_business": "电信产品,电力产品,新能源产业"
    },
    {
        "company_id": "guihang",
        "name_zh": "贵州贵航汽车零部件股份有限公司",
        "stock_code": "600523.SH",
        "province": "贵州",
        "city": "贵阳市",
        "industry": "汽车配件",
        "main_business": "汽车摩托车零部件,橡胶塑料制品,航空零部件"
    }
]

EXPOSURES = [
    {
        "exposure_id": "lianhuan_pharma_produce_pharmaceutical",
        "company_id": "lianhuan_pharma",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "化学药品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "lianhuan_pharma_produce_chemical_drug",
        "company_id": "lianhuan_pharma",
        "node_id": "chemical_drug",
        "activity_type": "produce",
        "role": "化学原料药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "hainan_airport_operate_commercial",
        "company_id": "hainan_airport",
        "node_id": "commercial",
        "activity_type": "operate",
        "role": "商业运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "hainan_airport_operate_hotel_service",
        "company_id": "hainan_airport",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "hainan_airport_operate_real_estate_development",
        "company_id": "hainan_airport",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "fangda_carbon_produce_graphite_electrode",
        "company_id": "fangda_carbon",
        "node_id": "graphite_electrode",
        "activity_type": "produce",
        "role": "石墨电极生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "fangda_carbon_produce_carbon_block",
        "company_id": "fangda_carbon",
        "node_id": "carbon_block",
        "activity_type": "produce",
        "role": "炭块生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "fangda_carbon_produce_metallurgical_product",
        "company_id": "fangda_carbon",
        "node_id": "metallurgical_product",
        "activity_type": "produce",
        "role": "冶金产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "sgcc_yingda_provide_service_low_carbon_energy_saving",
        "company_id": "sgcc_yingda",
        "node_id": "low_carbon_energy_saving",
        "activity_type": "provide_service",
        "role": "低碳节能服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "sgcc_yingda_manufacture_medium_low_voltage_electrical",
        "company_id": "sgcc_yingda",
        "node_id": "medium_low_voltage_electrical",
        "activity_type": "manufacture",
        "role": "中低压电气设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "sgcc_yingda_provide_service_power_grid_smart_operation",
        "company_id": "sgcc_yingda",
        "node_id": "power_grid_smart_operation",
        "activity_type": "provide_service",
        "role": "电网智能运维服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "kangmei_produce_chinese_medicine_decoction",
        "company_id": "kangmei",
        "node_id": "chinese_medicine_decoction",
        "activity_type": "produce",
        "role": "中药饮片生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "kangmei_produce_chinese_patent_medicine",
        "company_id": "kangmei",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "maotai_produce_maotai_liquor",
        "company_id": "maotai",
        "node_id": "maotai_liquor",
        "activity_type": "produce",
        "role": "茅台酒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "maotai_produce_liquor",
        "company_id": "maotai",
        "node_id": "liquor",
        "activity_type": "produce",
        "role": "白酒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sanjiatech_manufacture_semiconductor_packaging_mold",
        "company_id": "sanjiatech",
        "node_id": "semiconductor_packaging_mold",
        "activity_type": "manufacture",
        "role": "半导体塑封模具制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "sanjiatech_manufacture_led_bracket",
        "company_id": "sanjiatech",
        "node_id": "led_bracket",
        "activity_type": "manufacture",
        "role": "LED支架制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "huahai_produce_pril_product",
        "company_id": "huahai",
        "node_id": "pril_product",
        "activity_type": "produce",
        "role": "普利类产品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "huahai_produce_sartan_product",
        "company_id": "huahai",
        "node_id": "sartan_product",
        "activity_type": "produce",
        "role": "沙坦类产品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "huahai_produce_pharmaceutical",
        "company_id": "huahai",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "zhongtian_manufacture_telecom_product",
        "company_id": "zhongtian",
        "node_id": "telecom_product",
        "activity_type": "manufacture",
        "role": "电信产品制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongtian_manufacture_power_cable",
        "company_id": "zhongtian",
        "node_id": "power_cable",
        "activity_type": "manufacture",
        "role": "电力电缆制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "zhongtian_produce_new_energy",
        "company_id": "zhongtian",
        "node_id": "new_energy",
        "activity_type": "produce",
        "role": "新能源产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "guihang_manufacture_aviation_part",
        "company_id": "guihang",
        "node_id": "aviation_part",
        "activity_type": "manufacture",
        "role": "航空零部件制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "guihang_manufacture_automobile_part",
        "company_id": "guihang",
        "node_id": "automobile_part",
        "activity_type": "manufacture",
        "role": "汽车零部件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "guihang_produce_rubber_plastic_product",
        "company_id": "guihang",
        "node_id": "rubber_plastic_product",
        "activity_type": "produce",
        "role": "橡胶塑料制品生产商",
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
            "evidence": make_evidence(f"tushare batch 079: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 079: " + e["description"]),
        })
    return {
        "batch_id": "batch_079",
        "task_description": "Batch 079: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 079: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_079",
        "task_description": "Batch 079: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 079 Submission")
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
