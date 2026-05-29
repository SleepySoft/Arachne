#!/usr/bin/env python3
"""Submit batch 087 to Arachne API."""
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
        "node_id": "garden_design",
        "canonical_name_zh": "园林设计",
        "definition": "对园林景观进行规划、设计和营造的专业技术服务，包括植物配置、地形塑造、水景设计等",
        "entity_type": "service"
    },
    {
        "node_id": "transportation",
        "canonical_name_zh": "运输业",
        "definition": "利用各种运输工具实现人或货物空间位移的服务行业",
        "entity_type": "service"
    },
    {
        "node_id": "gold_jewelry",
        "canonical_name_zh": "黄金珠宝首饰",
        "definition": "以黄金为主要材质，配以宝石、珍珠等装饰制作的首饰饰品",
        "entity_type": "material"
    },
    {
        "node_id": "natural_gas_pipeline",
        "canonical_name_zh": "天然气长输管道",
        "definition": "用于长距离输送天然气的压力管道系统，包括输气干线、支线及配套设施",
        "entity_type": "infrastructure"
    },
    {
        "node_id": "city_gas",
        "canonical_name_zh": "城市燃气",
        "definition": "通过城市管网向居民、工商业用户供应的天然气、液化石油气等燃气",
        "entity_type": "service"
    },
    {
        "node_id": "polyvinyl_chloride",
        "canonical_name_zh": "聚氯乙烯",
        "definition": "由氯乙烯单体聚合而成的热塑性树脂，广泛用于制造管材、型材、薄膜等塑料制品",
        "entity_type": "material"
    },
    {
        "node_id": "caustic_soda",
        "canonical_name_zh": "烧碱",
        "definition": "氢氧化钠的工业名称，是重要的基础化工原料，广泛用于造纸、纺织、洗涤剂等行业",
        "entity_type": "material"
    },
    {
        "node_id": "chlorine_product",
        "canonical_name_zh": "氯产品",
        "definition": "以氯气为原料生产的各类化工产品，包括含氯溶剂、含氯农药、漂白剂等",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "natural_gas_pipeline_to_city_gas",
        "from_node": "natural_gas_pipeline",
        "to_node": "city_gas",
        "edge_type": "capability_supply",
        "description": "天然气长输管道为城市燃气供应提供气源输送能力"
    },
    {
        "edge_id": "polyvinyl_chloride_to_plastic",
        "from_node": "polyvinyl_chloride",
        "to_node": "plastic",
        "edge_type": "material_flow",
        "description": "聚氯乙烯是生产塑料制品的重要基础树脂原料"
    },
    {
        "edge_id": "caustic_soda_to_chemical_industry",
        "from_node": "caustic_soda",
        "to_node": "chemical_industry",
        "edge_type": "material_flow",
        "description": "烧碱是化工、造纸、纺织等众多行业的基础原料"
    }
]

COMPANIES = [
    {
        "company_id": "st_huke",
        "name_zh": "上海宽频科技股份有限公司",
        "stock_code": "600608.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "商贸代理",
        "main_business": "有色金属,黑色金属,化工原料及生产生活物资等"
    },
    {
        "company_id": "jinbei_auto",
        "name_zh": "沈阳金杯汽车股份有限公司",
        "stock_code": "600609.SH",
        "province": "辽宁",
        "city": "沈阳市",
        "industry": "汽车配件",
        "main_business": "汽车及零部件制造"
    },
    {
        "company_id": "zhongyida",
        "name_zh": "上海中毅达股份有限公司",
        "stock_code": "600610.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "化工原料",
        "main_business": "园林设计工程"
    },
    {
        "company_id": "dazhong_transport",
        "name_zh": "大众交通(集团)股份有限公司",
        "stock_code": "600611.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "公共交通",
        "main_business": "运输业,旅游饮食,服务业,商业,工业"
    },
    {
        "company_id": "laofengxiang",
        "name_zh": "老凤祥股份有限公司",
        "stock_code": "600612.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "服饰",
        "main_business": "黄金珠宝首饰,工艺美术品,笔类文具制品的生产经营及销售"
    },
    {
        "company_id": "shenqi",
        "name_zh": "上海神奇制药投资管理股份有限公司",
        "stock_code": "600613.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "中成药",
        "main_business": "医药领域投资管理"
    },
    {
        "company_id": "xinyuan",
        "name_zh": "鑫源智造(上海)股份有限公司",
        "stock_code": "600615.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "铝",
        "main_business": "涂料,制笔"
    },
    {
        "company_id": "jinfeng_wine",
        "name_zh": "上海金枫酒业股份有限公司",
        "stock_code": "600616.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "红黄酒",
        "main_business": "食品销售管理,酒,仓储货运,租赁,出口业务"
    },
    {
        "company_id": "guoxin_energy",
        "name_zh": "山西省国新能源股份有限公司",
        "stock_code": "600617.SH",
        "province": "山西",
        "city": "太原市",
        "industry": "供气供热",
        "main_business": "天然气长输管道及城市燃气管网的建设和运营"
    },
    {
        "company_id": "chlor_alkali",
        "name_zh": "上海氯碱化工股份有限公司",
        "stock_code": "600618.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "化工原料",
        "main_business": "聚氯乙烯,烧碱,氯产品,粒料及其他"
    }
]

EXPOSURES = [
    {
        "exposure_id": "st_huke_trade_nonferrous_metal",
        "company_id": "st_huke",
        "node_id": "nonferrous_metal",
        "activity_type": "procure",
        "role": "有色金属贸易商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_huke_trade_ferrous_metal",
        "company_id": "st_huke",
        "node_id": "ferrous_metal",
        "activity_type": "procure",
        "role": "黑色金属贸易商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_huke_trade_chemical_product",
        "company_id": "st_huke",
        "node_id": "chemical_product",
        "activity_type": "procure",
        "role": "化工原料贸易商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinbei_auto_manufacture_automobile",
        "company_id": "jinbei_auto",
        "node_id": "automobile",
        "activity_type": "manufacture",
        "role": "汽车制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinbei_auto_manufacture_automobile_part",
        "company_id": "jinbei_auto",
        "node_id": "automobile_part",
        "activity_type": "manufacture",
        "role": "汽车零部件制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongyida_provide_service_garden_design",
        "company_id": "zhongyida",
        "node_id": "garden_design",
        "activity_type": "provide_service",
        "role": "园林设计服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongyida_operate_construction",
        "company_id": "zhongyida",
        "node_id": "construction",
        "activity_type": "operate",
        "role": "园林工程运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "dazhong_transport_operate_transportation",
        "company_id": "dazhong_transport",
        "node_id": "transportation",
        "activity_type": "operate",
        "role": "运输业运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "dazhong_transport_operate_tourism_catering",
        "company_id": "dazhong_transport",
        "node_id": "tourism_catering",
        "activity_type": "operate",
        "role": "旅游饮食运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "dazhong_transport_operate_passenger_transport",
        "company_id": "dazhong_transport",
        "node_id": "passenger_transport",
        "activity_type": "operate",
        "role": "客运运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "laofengxiang_produce_gold_jewelry",
        "company_id": "laofengxiang",
        "node_id": "gold_jewelry",
        "activity_type": "produce",
        "role": "黄金珠宝首饰生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "laofengxiang_produce_arts_and_crafts",
        "company_id": "laofengxiang",
        "node_id": "arts_and_crafts",
        "activity_type": "produce",
        "role": "工艺美术品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "laofengxiang_produce_pen",
        "company_id": "laofengxiang",
        "node_id": "pen",
        "activity_type": "produce",
        "role": "笔类文具制品生产商",
        "weight": 0.8
    },
    {
        "exposure_id": "shenqi_produce_pharmaceutical",
        "company_id": "shenqi",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenqi_operate_investment_management",
        "company_id": "shenqi",
        "node_id": "investment_management",
        "activity_type": "operate",
        "role": "医药投资运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "xinyuan_produce_coating",
        "company_id": "xinyuan",
        "node_id": "coating",
        "activity_type": "produce",
        "role": "涂料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xinyuan_manufacture_pen",
        "company_id": "xinyuan",
        "node_id": "pen",
        "activity_type": "manufacture",
        "role": "制笔制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinfeng_wine_produce_liquor",
        "company_id": "jinfeng_wine",
        "node_id": "liquor",
        "activity_type": "produce",
        "role": "酒类生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinfeng_wine_provide_service_warehousing",
        "company_id": "jinfeng_wine",
        "node_id": "warehousing",
        "activity_type": "provide_service",
        "role": "仓储货运服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "guoxin_energy_operate_natural_gas_pipeline",
        "company_id": "guoxin_energy",
        "node_id": "natural_gas_pipeline",
        "activity_type": "operate",
        "role": "天然气长输管道运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "guoxin_energy_operate_city_gas",
        "company_id": "guoxin_energy",
        "node_id": "city_gas",
        "activity_type": "operate",
        "role": "城市燃气运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "guoxin_energy_provide_service_heating_supply",
        "company_id": "guoxin_energy",
        "node_id": "heating_supply",
        "activity_type": "provide_service",
        "role": "供热供应商",
        "weight": 0.85
    },
    {
        "exposure_id": "chlor_alkali_produce_polyvinyl_chloride",
        "company_id": "chlor_alkali",
        "node_id": "polyvinyl_chloride",
        "activity_type": "produce",
        "role": "聚氯乙烯生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "chlor_alkali_produce_caustic_soda",
        "company_id": "chlor_alkali",
        "node_id": "caustic_soda",
        "activity_type": "produce",
        "role": "烧碱生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "chlor_alkali_produce_chlorine_product",
        "company_id": "chlor_alkali",
        "node_id": "chlorine_product",
        "activity_type": "produce",
        "role": "氯产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "chlor_alkali_produce_chemical_product",
        "company_id": "chlor_alkali",
        "node_id": "chemical_product",
        "activity_type": "produce",
        "role": "化工产品生产商",
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
            "evidence": make_evidence(f"tushare batch 087: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 087: " + e["description"]),
        })
    return {
        "batch_id": "batch_087",
        "task_description": "Batch 087: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 087: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_087",
        "task_description": "Batch 087: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 087 Submission")
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
