#!/usr/bin/env python3
"""Submit batch 078 to Arachne API."""
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
        "node_id": "engineering_general_contracting",
        "canonical_name_zh": "工程总承包",
        "definition": "承包单位按照合同约定对工程项目的勘察、设计、采购、施工、试运行等实行全过程或若干阶段承包的建设模式",
        "entity_type": "service"
    },
    {
        "node_id": "equity_investment",
        "canonical_name_zh": "股权投资",
        "definition": "通过购买企业股权以获取长期资本增值和股息收益的投资活动",
        "entity_type": "service"
    },
    {
        "node_id": "rebar",
        "canonical_name_zh": "螺纹钢",
        "definition": "表面带肋的钢筋，广泛用于房屋建筑、桥梁、道路等钢筋混凝土结构中",
        "entity_type": "material"
    },
    {
        "node_id": "leaf_spring",
        "canonical_name_zh": "汽车板簧",
        "definition": "汽车悬架系统中使用的多层钢板叠合而成的弹性元件，用于缓冲和减振",
        "entity_type": "component"
    },
    {
        "node_id": "iron_concentrate",
        "canonical_name_zh": "铁精粉",
        "definition": "铁矿石经破碎、磨矿、磁选等选矿工艺处理后得到的高品位细粒铁粉",
        "entity_type": "material"
    },
    {
        "node_id": "raw_coal",
        "canonical_name_zh": "原煤",
        "definition": "从地下开采出来未经洗选加工的煤炭，是煤炭工业的初级产品",
        "entity_type": "material"
    },
    {
        "node_id": "denim",
        "canonical_name_zh": "牛仔布",
        "definition": "一种粗厚的色织棉斜纹布，主要用于制作牛仔裤、夹克等服装",
        "entity_type": "material"
    },
    {
        "node_id": "pharmaceutical_commerce",
        "canonical_name_zh": "医药商业",
        "definition": "从事药品、医疗器械等医药产品的批发、零售、物流配送等流通服务",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "rebar_to_construction",
        "from_node": "rebar",
        "to_node": "construction",
        "edge_type": "material_flow",
        "description": "螺纹钢是建筑工程钢筋混凝土结构的主要骨架材料"
    },
    {
        "edge_id": "leaf_spring_to_automobile",
        "from_node": "leaf_spring",
        "to_node": "automobile",
        "edge_type": "composition",
        "description": "汽车板簧是汽车悬架系统的关键弹性组件"
    },
    {
        "edge_id": "iron_concentrate_to_steel",
        "from_node": "iron_concentrate",
        "to_node": "steel",
        "edge_type": "material_flow",
        "description": "铁精粉是高炉炼铁的主要原料，经冶炼后成为钢材"
    }
]

COMPANIES = [
    {
        "company_id": "anhui_construction",
        "name_zh": "安徽建工集团股份有限公司",
        "stock_code": "600502.SH",
        "province": "安徽",
        "city": "合肥市",
        "industry": "建筑工程",
        "main_business": "工程总承包,房屋建筑,水利水电,市政,公路,桥梁,隧道,港口航道,机电设备安装"
    },
    {
        "company_id": "huali_family",
        "name_zh": "华丽家族股份有限公司",
        "stock_code": "600503.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "区域地产",
        "main_business": "股权投资"
    },
    {
        "company_id": "xichang_power",
        "name_zh": "四川西昌电力股份有限公司",
        "stock_code": "600505.SH",
        "province": "四川",
        "city": "西昌市",
        "industry": "水力发电",
        "main_business": "电力销售"
    },
    {
        "company_id": "unified_co",
        "name_zh": "统一低碳科技(新疆)股份有限公司",
        "stock_code": "600506.SH",
        "province": "新疆",
        "city": "库尔勒市",
        "industry": "石油加工",
        "main_business": "香梨,其他果品及包装物,杏酒"
    },
    {
        "company_id": "fangda_special_steel",
        "name_zh": "方大特钢科技股份有限公司",
        "stock_code": "600507.SH",
        "province": "江西",
        "city": "南昌市",
        "industry": "特种钢",
        "main_business": "螺纹钢,汽车板簧,弹簧扁钢,铁精粉等"
    },
    {
        "company_id": "shanghai_energy",
        "name_zh": "上海大屯能源股份有限公司",
        "stock_code": "600508.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "煤炭开采",
        "main_business": "原煤,选煤,铁路运输"
    },
    {
        "company_id": "tianfu_energy",
        "name_zh": "新疆天富能源股份有限公司",
        "stock_code": "600509.SH",
        "province": "新疆",
        "city": "石河子市",
        "industry": "火力发电",
        "main_business": "电,热的生产与销售"
    },
    {
        "company_id": "black_peony",
        "name_zh": "黑牡丹(集团)股份有限公司",
        "stock_code": "600510.SH",
        "province": "江苏",
        "city": "常州市",
        "industry": "全国地产",
        "main_business": "牛仔布,服装"
    },
    {
        "company_id": "sinopharm_co",
        "name_zh": "国药集团药业股份有限公司",
        "stock_code": "600511.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "医药商业",
        "main_business": "医药商业,医药工业"
    },
    {
        "company_id": "tengda",
        "name_zh": "腾达建设集团股份有限公司",
        "stock_code": "600512.SH",
        "province": "浙江",
        "city": "台州市",
        "industry": "建筑工程",
        "main_business": "市政,公路工程,一级公路运营"
    }
]

EXPOSURES = [
    {
        "exposure_id": "anhui_construction_operate_engineering_general_contracting",
        "company_id": "anhui_construction",
        "node_id": "engineering_general_contracting",
        "activity_type": "operate",
        "role": "工程总承包商",
        "weight": 0.95
    },
    {
        "exposure_id": "anhui_construction_operate_construction",
        "company_id": "anhui_construction",
        "node_id": "construction",
        "activity_type": "operate",
        "role": "建筑施工运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "anhui_construction_operate_municipal_engineering",
        "company_id": "anhui_construction",
        "node_id": "municipal_engineering",
        "activity_type": "operate",
        "role": "市政工程运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "huali_family_operate_equity_investment",
        "company_id": "huali_family",
        "node_id": "equity_investment",
        "activity_type": "operate",
        "role": "股权投资运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "huali_family_provide_service_financial_service",
        "company_id": "huali_family",
        "node_id": "financial_service",
        "activity_type": "provide_service",
        "role": "金融服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "xichang_power_operate_power_distribution",
        "company_id": "xichang_power",
        "node_id": "power_distribution",
        "activity_type": "operate",
        "role": "电力配供运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "xichang_power_provide_service_power_supply",
        "company_id": "xichang_power",
        "node_id": "power_supply",
        "activity_type": "provide_service",
        "role": "电力供应服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "unified_co_produce_pear",
        "company_id": "unified_co",
        "node_id": "pear",
        "activity_type": "produce",
        "role": "香梨生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "unified_co_produce_fruit",
        "company_id": "unified_co",
        "node_id": "fruit",
        "activity_type": "produce",
        "role": "果品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "unified_co_produce_liquor",
        "company_id": "unified_co",
        "node_id": "liquor",
        "activity_type": "produce",
        "role": "酒类生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "fangda_special_steel_produce_rebar",
        "company_id": "fangda_special_steel",
        "node_id": "rebar",
        "activity_type": "produce",
        "role": "螺纹钢生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "fangda_special_steel_produce_leaf_spring",
        "company_id": "fangda_special_steel",
        "node_id": "leaf_spring",
        "activity_type": "produce",
        "role": "汽车板簧生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "fangda_special_steel_produce_spring_flat_steel",
        "company_id": "fangda_special_steel",
        "node_id": "spring_flat_steel",
        "activity_type": "produce",
        "role": "弹簧扁钢生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "fangda_special_steel_produce_iron_concentrate",
        "company_id": "fangda_special_steel",
        "node_id": "iron_concentrate",
        "activity_type": "produce",
        "role": "铁精粉生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "shanghai_energy_produce_raw_coal",
        "company_id": "shanghai_energy",
        "node_id": "raw_coal",
        "activity_type": "produce",
        "role": "原煤生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shanghai_energy_operate_coal_washing",
        "company_id": "shanghai_energy",
        "node_id": "coal_washing",
        "activity_type": "operate",
        "role": "选煤运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "shanghai_energy_operate_railway_transport",
        "company_id": "shanghai_energy",
        "node_id": "railway_transport",
        "activity_type": "operate",
        "role": "铁路运输运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "tianfu_energy_operate_power_generation",
        "company_id": "tianfu_energy",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "发电运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianfu_energy_provide_service_heating_supply",
        "company_id": "tianfu_energy",
        "node_id": "heating_supply",
        "activity_type": "provide_service",
        "role": "热力供应商",
        "weight": 0.9
    },
    {
        "exposure_id": "black_peony_produce_denim",
        "company_id": "black_peony",
        "node_id": "denim",
        "activity_type": "produce",
        "role": "牛仔布生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "black_peony_produce_apparel",
        "company_id": "black_peony",
        "node_id": "apparel",
        "activity_type": "produce",
        "role": "服装生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "sinopharm_co_operate_pharmaceutical_commerce",
        "company_id": "sinopharm_co",
        "node_id": "pharmaceutical_commerce",
        "activity_type": "operate",
        "role": "医药商业运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "sinopharm_co_produce_pharmaceutical",
        "company_id": "sinopharm_co",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "tengda_operate_municipal_engineering",
        "company_id": "tengda",
        "node_id": "municipal_engineering",
        "activity_type": "operate",
        "role": "市政工程运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "tengda_operate_highway_operation",
        "company_id": "tengda",
        "node_id": "highway_operation",
        "activity_type": "operate",
        "role": "公路运营运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "tengda_operate_expressway",
        "company_id": "tengda",
        "node_id": "expressway",
        "activity_type": "operate",
        "role": "高速公路运营商",
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
            "evidence": make_evidence(f"tushare batch 078: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 078: " + e["description"]),
        })
    return {
        "batch_id": "batch_078",
        "task_description": "Batch 078: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 078: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_078",
        "task_description": "Batch 078: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 078 Submission")
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
