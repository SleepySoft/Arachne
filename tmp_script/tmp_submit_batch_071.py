#!/usr/bin/env python3
"""Submit batch 071 to Arachne API."""
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
        "node_id": "superhard_material",
        "canonical_name_zh": "超硬材料",
        "definition": "硬度极高的材料，如金刚石、立方氮化硼等，用于切削、磨削工具",
        "entity_type": "material"
    },
    {
        "node_id": "battery_cathode_material",
        "canonical_name_zh": "电池正极材料",
        "definition": "锂离子电池正极活性物质，如钴酸锂、磷酸铁锂、三元材料等",
        "entity_type": "material"
    },
    {
        "node_id": "aeroengine_part",
        "canonical_name_zh": "航空发动机零部件",
        "definition": "航空发动机的核心部件，包括叶片、盘、轴、机匣等",
        "entity_type": "component"
    },
    {
        "node_id": "gas_turbine_part",
        "canonical_name_zh": "燃气轮机零部件",
        "definition": "燃气轮机的关键部件，包括压气机、燃烧室、涡轮等组件",
        "entity_type": "component"
    },
    {
        "node_id": "rare_earth_metal",
        "canonical_name_zh": "稀有稀土金属",
        "definition": "稀土元素及其合金，包括镧、铈、钕、钐等17种元素",
        "entity_type": "material"
    },
    {
        "node_id": "catalytic_material",
        "canonical_name_zh": "催化材料",
        "definition": "用于加速化学反应速率的材料，包括催化剂、催化助剂等",
        "entity_type": "material"
    },
    {
        "node_id": "alloy_structural_steel",
        "canonical_name_zh": "合金结构钢",
        "definition": "在碳素结构钢基础上添加合金元素以提高强度、韧性和耐磨性的钢材",
        "entity_type": "material"
    },
    {
        "node_id": "superalloy",
        "canonical_name_zh": "高温合金",
        "definition": "能在高温氧化和燃气腐蚀条件下长期工作的合金材料，主要用于航空发动机和燃气轮机",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "aeroengine_part_to_aircraft_engine",
        "from_node": "aeroengine_part",
        "to_node": "aircraft_engine",
        "edge_type": "composition",
        "description": "航空发动机零部件是航空发动机的核心组成部件"
    },
    {
        "edge_id": "battery_cathode_material_to_lithium_battery",
        "from_node": "battery_cathode_material",
        "to_node": "lithium_battery",
        "edge_type": "composition",
        "description": "电池正极材料是锂离子电池的关键组成部分"
    },
    {
        "edge_id": "superalloy_to_aircraft_engine",
        "from_node": "superalloy",
        "to_node": "aircraft_engine",
        "edge_type": "material_flow",
        "description": "高温合金材料用于制造航空发动机的热端部件"
    }
]

COMPANIES = [
    {
        "company_id": "minmetals_capital",
        "name_zh": "五矿资本股份有限公司",
        "stock_code": "600390.SH",
        "province": "湖南",
        "city": "长沙市",
        "industry": "多元金融",
        "main_business": "超硬材料,电子基础材料,电池正极材料,证券,期货,信托,金融租赁"
    },
    {
        "company_id": "aeroengine_tech",
        "name_zh": "中国航发航空科技股份有限公司",
        "stock_code": "600391.SH",
        "province": "四川",
        "city": "成都市",
        "industry": "航空",
        "main_business": "航空发动机零部件,燃气轮机零部件,空调壳体件,石油机械零部件"
    },
    {
        "company_id": "shenghe_resources",
        "name_zh": "盛和资源控股股份有限公司",
        "stock_code": "600392.SH",
        "province": "四川",
        "city": "成都市",
        "industry": "小金属",
        "main_business": "稀土矿山开采,稀土产品生产及销售,催化材料生产及销售,稀有稀土金属冶炼与销售"
    },
    {
        "company_id": "panjiang",
        "name_zh": "贵州盘江精煤股份有限公司",
        "stock_code": "600395.SH",
        "province": "贵州",
        "city": "六盘水市",
        "industry": "煤炭开采",
        "main_business": "精煤,混煤的生产与销售"
    },
    {
        "company_id": "huadian_liaoning",
        "name_zh": "华电辽宁能源发展股份有限公司",
        "stock_code": "600396.SH",
        "province": "辽宁",
        "city": "沈阳市",
        "industry": "火力发电",
        "main_business": "电力,热力的生产和供应"
    },
    {
        "company_id": "jiangtungsten",
        "name_zh": "江西江州联合造船有限责任公司",
        "stock_code": "600397.SH",
        "province": "江西",
        "city": "九江市",
        "industry": "专用机械",
        "main_business": "煤炭开采,煤炭精选加工,煤炭经营"
    },
    {
        "company_id": "hla",
        "name_zh": "海澜之家集团股份有限公司",
        "stock_code": "600398.SH",
        "province": "江苏",
        "city": "无锡市",
        "industry": "服饰",
        "main_business": "品牌服饰的经营,包括品牌管理,供应链管理和营销网络管理"
    },
    {
        "company_id": "fushun_special_steel",
        "name_zh": "抚顺特殊钢股份有限公司",
        "stock_code": "600399.SH",
        "province": "辽宁",
        "city": "抚顺市",
        "industry": "特种钢",
        "main_business": "合金结构钢,工模具钢,不锈钢和高温合金的研发制造"
    },
    {
        "company_id": "hongdou",
        "name_zh": "红豆集团股份有限公司",
        "stock_code": "600400.SH",
        "province": "江苏",
        "city": "无锡市",
        "industry": "服饰",
        "main_business": "服装,毛线纱线及印染"
    },
    {
        "company_id": "dayou_energy",
        "name_zh": "河南大有能源股份有限公司",
        "stock_code": "600403.SH",
        "province": "河南",
        "city": "三门峡市",
        "industry": "煤炭开采",
        "main_business": "煤炭生产与经营"
    }
]

EXPOSURES = [
    {
        "exposure_id": "minmetals_capital_produce_superhard_material",
        "company_id": "minmetals_capital",
        "node_id": "superhard_material",
        "activity_type": "produce",
        "role": "超硬材料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "minmetals_capital_produce_battery_cathode_material",
        "company_id": "minmetals_capital",
        "node_id": "battery_cathode_material",
        "activity_type": "produce",
        "role": "电池正极材料生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "minmetals_capital_provide_service_securities_service",
        "company_id": "minmetals_capital",
        "node_id": "securities_service",
        "activity_type": "provide_service",
        "role": "证券服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "minmetals_capital_provide_service_financial_service",
        "company_id": "minmetals_capital",
        "node_id": "financial_service",
        "activity_type": "provide_service",
        "role": "综合金融服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "aeroengine_tech_manufacture_aeroengine_part",
        "company_id": "aeroengine_tech",
        "node_id": "aeroengine_part",
        "activity_type": "manufacture",
        "role": "航空发动机零部件制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "aeroengine_tech_manufacture_gas_turbine_part",
        "company_id": "aeroengine_tech",
        "node_id": "gas_turbine_part",
        "activity_type": "manufacture",
        "role": "燃气轮机零部件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "aeroengine_tech_manufacture_aircraft_engine",
        "company_id": "aeroengine_tech",
        "node_id": "aircraft_engine",
        "activity_type": "manufacture",
        "role": "航空发动机制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "shenghe_resources_produce_rare_earth_metal",
        "company_id": "shenghe_resources",
        "node_id": "rare_earth_metal",
        "activity_type": "produce",
        "role": "稀有稀土金属生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenghe_resources_produce_catalytic_material",
        "company_id": "shenghe_resources",
        "node_id": "catalytic_material",
        "activity_type": "produce",
        "role": "催化材料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "shenghe_resources_operate_rare_earth_mining",
        "company_id": "shenghe_resources",
        "node_id": "rare_earth_mining",
        "activity_type": "operate",
        "role": "稀土矿山开采运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "panjiang_produce_coal",
        "company_id": "panjiang",
        "node_id": "coal",
        "activity_type": "produce",
        "role": "煤炭生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "panjiang_operate_coal_mining",
        "company_id": "panjiang",
        "node_id": "coal_mining",
        "activity_type": "operate",
        "role": "煤炭开采运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "huadian_liaoning_operate_power_generation",
        "company_id": "huadian_liaoning",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "火力发电运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "huadian_liaoning_provide_service_heating_supply",
        "company_id": "huadian_liaoning",
        "node_id": "heating_supply",
        "activity_type": "provide_service",
        "role": "热力供应商",
        "weight": 0.9
    },
    {
        "exposure_id": "jiangtungsten_operate_coal_mining",
        "company_id": "jiangtungsten",
        "node_id": "coal_mining",
        "activity_type": "operate",
        "role": "煤炭开采运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "jiangtungsten_operate_coal",
        "company_id": "jiangtungsten",
        "node_id": "coal",
        "activity_type": "operate",
        "role": "煤炭经营商",
        "weight": 0.9
    },
    {
        "exposure_id": "hla_operate_apparel",
        "company_id": "hla",
        "node_id": "apparel",
        "activity_type": "operate",
        "role": "服装品牌运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "hla_operate_retail",
        "company_id": "hla",
        "node_id": "retail",
        "activity_type": "operate",
        "role": "零售运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "fushun_special_steel_produce_alloy_structural_steel",
        "company_id": "fushun_special_steel",
        "node_id": "alloy_structural_steel",
        "activity_type": "produce",
        "role": "合金结构钢生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "fushun_special_steel_produce_superalloy",
        "company_id": "fushun_special_steel",
        "node_id": "superalloy",
        "activity_type": "produce",
        "role": "高温合金生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "fushun_special_steel_produce_stainless_steel",
        "company_id": "fushun_special_steel",
        "node_id": "stainless_steel",
        "activity_type": "produce",
        "role": "不锈钢生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "fushun_special_steel_produce_steel",
        "company_id": "fushun_special_steel",
        "node_id": "steel",
        "activity_type": "produce",
        "role": "特钢生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "hongdou_produce_apparel",
        "company_id": "hongdou",
        "node_id": "apparel",
        "activity_type": "produce",
        "role": "服装生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "hongdou_produce_textile_product",
        "company_id": "hongdou",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "dayou_energy_operate_coal",
        "company_id": "dayou_energy",
        "node_id": "coal",
        "activity_type": "operate",
        "role": "煤炭经营商",
        "weight": 0.95
    },
    {
        "exposure_id": "dayou_energy_operate_coal_mining",
        "company_id": "dayou_energy",
        "node_id": "coal_mining",
        "activity_type": "operate",
        "role": "煤炭开采运营商",
        "weight": 0.9
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
            "evidence": make_evidence(f"tushare batch 071: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 071: " + e["description"]),
        })
    return {
        "batch_id": "batch_071",
        "task_description": "Batch 071: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 071: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_071",
        "task_description": "Batch 071: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 071 Submission")
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
