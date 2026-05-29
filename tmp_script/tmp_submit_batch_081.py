#!/usr/bin/env python3
"""Submit batch 081 to Arachne API."""
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
        "node_id": "silicon_ingot",
        "canonical_name_zh": "硅棒",
        "definition": "通过提拉法或浇铸法生长的圆柱形高纯度硅晶体，是制造太阳能电池和半导体芯片的基础材料",
        "entity_type": "material"
    },
    {
        "node_id": "water_purifier_faucet",
        "canonical_name_zh": "净水龙头",
        "definition": "集成了过滤净化功能的龙头设备，用于家庭或商业场所的饮用水净化",
        "entity_type": "device"
    },
    {
        "node_id": "cotton_seed",
        "canonical_name_zh": "棉种",
        "definition": "用于棉花种植的优良种子，是棉花农业生产的基础投入品",
        "entity_type": "material"
    },
    {
        "node_id": "malt",
        "canonical_name_zh": "大麦芽",
        "definition": "大麦经浸麦、发芽、烘干等工序制成的产品，主要用于啤酒酿造和食品工业",
        "entity_type": "material"
    },
    {
        "node_id": "intelligent_textile_equipment",
        "canonical_name_zh": "智能化纺织成套设备",
        "definition": "采用自动化和智能化技术实现纺纱、织造、染整等工序的成套纺织机械设备",
        "entity_type": "system"
    },
    {
        "node_id": "tungsten_concentrate",
        "canonical_name_zh": "钨精矿",
        "definition": "钨矿石经选矿富集后得到的高品位钨矿物产品，是钨冶炼的初始原料",
        "entity_type": "material"
    },
    {
        "node_id": "cemented_carbide",
        "canonical_name_zh": "硬质合金",
        "definition": "以碳化钨为硬质相、钴为粘结相烧结制成的高硬度耐磨材料，用于切削工具和耐磨零件",
        "entity_type": "material"
    },
    {
        "node_id": "gold_jewelry",
        "canonical_name_zh": "黄金珠宝饰品",
        "definition": "以黄金为主要材质制作的珠宝首饰和装饰品",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "silicon_ingot_to_solar_cell",
        "from_node": "silicon_ingot",
        "to_node": "solar_cell",
        "edge_type": "material_flow",
        "description": "硅棒是制造晶体硅太阳能电池的核心原材料"
    },
    {
        "edge_id": "tungsten_concentrate_to_cemented_carbide",
        "from_node": "tungsten_concentrate",
        "to_node": "cemented_carbide",
        "edge_type": "material_flow",
        "description": "钨精矿经冶炼加工后制成硬质合金产品"
    },
    {
        "edge_id": "cemented_carbide_to_cutting_tool",
        "from_node": "cemented_carbide",
        "to_node": "cutting_tool",
        "edge_type": "material_flow",
        "description": "硬质合金是制造切削刀具的主要材料"
    }
]

COMPANIES = [
    {
        "company_id": "st_yijing",
        "name_zh": "亿晶光电科技股份有限公司",
        "stock_code": "600537.SH",
        "province": "江苏",
        "city": "常州市",
        "industry": "电气设备",
        "main_business": "晶体硅太阳能电池片和电池组件的生产和销售以及光伏发电业务"
    },
    {
        "company_id": "guofa",
        "name_zh": "北海国发川山生物股份有限公司",
        "stock_code": "600538.SH",
        "province": "广西",
        "city": "北海市",
        "industry": "医药商业",
        "main_business": "医药制造及医药流通产业,农药产业,酒店和环保"
    },
    {
        "company_id": "shitou",
        "name_zh": "太原狮头水泥股份有限公司",
        "stock_code": "600539.SH",
        "province": "山西",
        "city": "太原市",
        "industry": "互联网",
        "main_business": "净水龙头及配件的生产与销售,污水处理项目工程,河道治理等水技术,环保技术"
    },
    {
        "company_id": "xinsai",
        "name_zh": "新疆赛里木现代农业股份有限公司",
        "stock_code": "600540.SH",
        "province": "新疆",
        "city": "博尔塔拉",
        "industry": "种植业",
        "main_business": "棉花,棉种"
    },
    {
        "company_id": "st_mogao",
        "name_zh": "甘肃莫高实业发展股份有限公司",
        "stock_code": "600543.SH",
        "province": "甘肃",
        "city": "兰州市",
        "industry": "红黄酒",
        "main_business": "大麦芽,葡萄及葡萄酒,甘草系列产品"
    },
    {
        "company_id": "saurer",
        "name_zh": "卓郎智能技术股份有限公司",
        "stock_code": "600545.SH",
        "province": "新疆",
        "city": "乌鲁木齐市",
        "industry": "纺织机械",
        "main_business": "智能化纺织成套设备及核心零部件的研发,生产和销售"
    },
    {
        "company_id": "shanmei_intl",
        "name_zh": "山煤国际能源集团股份有限公司",
        "stock_code": "600546.SH",
        "province": "山西",
        "city": "太原市",
        "industry": "煤炭开采",
        "main_business": "煤炭开采与煤炭贸易业务"
    },
    {
        "company_id": "shandong_gold",
        "name_zh": "山东黄金矿业股份有限公司",
        "stock_code": "600547.SH",
        "province": "山东",
        "city": "济南市",
        "industry": "黄金",
        "main_business": "黄金开采,黄金珠宝饰品"
    },
    {
        "company_id": "shenzhen_expressway",
        "name_zh": "深圳高速公路集团股份有限公司",
        "stock_code": "600548.SH",
        "province": "广东",
        "city": "深圳市",
        "industry": "路桥",
        "main_business": "经营梅观高速,机荷高速,盐坝高速,水官高速以及长沙环路和湖北隔蒲潭大桥"
    },
    {
        "company_id": "xiamen_tungsten",
        "name_zh": "厦门钨业股份有限公司",
        "stock_code": "600549.SH",
        "province": "福建",
        "city": "厦门市",
        "industry": "小金属",
        "main_business": "钨精矿,钨钼中间制品,粉末产品,丝材板材,硬质合金,切削刀具,各种稀土氧化物,稀土金属,稀土发光材料,磁性材料,贮氢合金粉,锂电池"
    }
]

EXPOSURES = [
    {
        "exposure_id": "st_yijing_produce_silicon_ingot",
        "company_id": "st_yijing",
        "node_id": "silicon_ingot",
        "activity_type": "produce",
        "role": "硅棒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_yijing_produce_solar_cell",
        "company_id": "st_yijing",
        "node_id": "solar_cell",
        "activity_type": "produce",
        "role": "太阳能电池片生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_yijing_produce_photovoltaic",
        "company_id": "st_yijing",
        "node_id": "photovoltaic",
        "activity_type": "produce",
        "role": "光伏组件生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "guofa_produce_pesticide",
        "company_id": "guofa",
        "node_id": "pesticide",
        "activity_type": "produce",
        "role": "农药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "guofa_produce_pharmaceutical",
        "company_id": "guofa",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "guofa_operate_hotel_service",
        "company_id": "guofa",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店服务商",
        "weight": 0.8
    },
    {
        "exposure_id": "shitou_manufacture_water_purifier_faucet",
        "company_id": "shitou",
        "node_id": "water_purifier_faucet",
        "activity_type": "manufacture",
        "role": "净水龙头制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "shitou_operate_water_treatment",
        "company_id": "shitou",
        "node_id": "water_treatment",
        "activity_type": "operate",
        "role": "污水处理运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "xinsai_produce_cotton",
        "company_id": "xinsai",
        "node_id": "cotton",
        "activity_type": "produce",
        "role": "棉花生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xinsai_produce_cotton_seed",
        "company_id": "xinsai",
        "node_id": "cotton_seed",
        "activity_type": "produce",
        "role": "棉种生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_mogao_produce_malt",
        "company_id": "st_mogao",
        "node_id": "malt",
        "activity_type": "produce",
        "role": "大麦芽生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_mogao_produce_wine",
        "company_id": "st_mogao",
        "node_id": "wine",
        "activity_type": "produce",
        "role": "葡萄酒生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_mogao_produce_licorice",
        "company_id": "st_mogao",
        "node_id": "licorice",
        "activity_type": "produce",
        "role": "甘草系列产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "saurer_manufacture_intelligent_textile_equipment",
        "company_id": "saurer",
        "node_id": "intelligent_textile_equipment",
        "activity_type": "manufacture",
        "role": "智能化纺织成套设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "saurer_manufacture_textile_machinery",
        "company_id": "saurer",
        "node_id": "textile_machinery",
        "activity_type": "manufacture",
        "role": "纺织机械制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shanmei_intl_operate_coal",
        "company_id": "shanmei_intl",
        "node_id": "coal",
        "activity_type": "operate",
        "role": "煤炭经营商",
        "weight": 0.95
    },
    {
        "exposure_id": "shanmei_intl_operate_coal_mining",
        "company_id": "shanmei_intl",
        "node_id": "coal_mining",
        "activity_type": "operate",
        "role": "煤炭开采运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "shandong_gold_produce_gold",
        "company_id": "shandong_gold",
        "node_id": "gold",
        "activity_type": "produce",
        "role": "黄金生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shandong_gold_produce_gold_jewelry",
        "company_id": "shandong_gold",
        "node_id": "gold_jewelry",
        "activity_type": "produce",
        "role": "黄金珠宝饰品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "shenzhen_expressway_operate_expressway",
        "company_id": "shenzhen_expressway",
        "node_id": "expressway",
        "activity_type": "operate",
        "role": "高速公路运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenzhen_expressway_operate_toll_road",
        "company_id": "shenzhen_expressway",
        "node_id": "toll_road",
        "activity_type": "operate",
        "role": "路桥收费运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "xiamen_tungsten_produce_tungsten_concentrate",
        "company_id": "xiamen_tungsten",
        "node_id": "tungsten_concentrate",
        "activity_type": "produce",
        "role": "钨精矿生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xiamen_tungsten_produce_cemented_carbide",
        "company_id": "xiamen_tungsten",
        "node_id": "cemented_carbide",
        "activity_type": "produce",
        "role": "硬质合金生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xiamen_tungsten_produce_cutting_tool",
        "company_id": "xiamen_tungsten",
        "node_id": "cutting_tool",
        "activity_type": "produce",
        "role": "切削刀具生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "xiamen_tungsten_produce_rare_earth_metal",
        "company_id": "xiamen_tungsten",
        "node_id": "rare_earth_metal",
        "activity_type": "produce",
        "role": "稀土金属生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "xiamen_tungsten_produce_lithium_battery",
        "company_id": "xiamen_tungsten",
        "node_id": "lithium_battery",
        "activity_type": "produce",
        "role": "锂电池生产商",
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
            "evidence": make_evidence(f"tushare batch 081: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 081: " + e["description"]),
        })
    return {
        "batch_id": "batch_081",
        "task_description": "Batch 081: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 081: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_081",
        "task_description": "Batch 081: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 081 Submission")
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
