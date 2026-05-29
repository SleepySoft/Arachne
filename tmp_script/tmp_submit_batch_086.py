#!/usr/bin/env python3
"""Submit batch 086 to Arachne API."""
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
        "node_id": "rice",
        "canonical_name_zh": "大米",
        "definition": "稻谷经清理、砻谷、碾米等工序加工后制成的成品粮，是人类主要粮食作物之一",
        "entity_type": "material"
    },
    {
        "node_id": "fireworks",
        "canonical_name_zh": "烟花",
        "definition": "以火药为主要原料，点燃后能产生光、色、声、形等效果的娱乐观赏用品",
        "entity_type": "material"
    },
    {
        "node_id": "pcb_product",
        "canonical_name_zh": "PCB产品",
        "definition": "印制电路板及其相关产品，用于电子元器件的电气连接和机械支撑",
        "entity_type": "component"
    },
    {
        "node_id": "consumer_electronics",
        "canonical_name_zh": "消费电子",
        "definition": "供个人和家庭日常使用的电子设备，包括智能手机、平板电脑、智能穿戴等",
        "entity_type": "device"
    },
    {
        "node_id": "intelligent_security",
        "canonical_name_zh": "智能安防",
        "definition": "利用人工智能、物联网等技术实现的安全监控和防护系统",
        "entity_type": "system"
    },
    {
        "node_id": "logistics_park",
        "canonical_name_zh": "物流园区",
        "definition": "集中建设物流设施和企业的专业化园区，提供仓储、运输、配送等综合服务",
        "entity_type": "infrastructure"
    },
    {
        "node_id": "wind_power",
        "canonical_name_zh": "风力发电",
        "definition": "利用风力驱动风电机组旋转产生电能的可再生能源发电方式",
        "entity_type": "service"
    },
    {
        "node_id": "copper_trade",
        "canonical_name_zh": "铜贸易",
        "definition": "从事铜及铜制品的批发、零售和进出口贸易业务",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "rice_to_food",
        "from_node": "rice",
        "to_node": "food",
        "edge_type": "material_flow",
        "description": "大米是人类主食粮食，是重要的食品原料"
    },
    {
        "edge_id": "pcb_product_to_electronic_device",
        "from_node": "pcb_product",
        "to_node": "electronic_device",
        "edge_type": "composition",
        "description": "PCB印制电路板是电子设备中实现电路连接的核心基础部件"
    },
    {
        "edge_id": "wind_power_to_power_generation",
        "from_node": "wind_power",
        "to_node": "power_generation",
        "edge_type": "service_flow",
        "description": "风力发电是可再生能源电力生产的重要方式"
    }
]

COMPANIES = [
    {
        "company_id": "bright_dairy",
        "name_zh": "光明乳业股份有限公司",
        "stock_code": "600597.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "乳制品",
        "main_business": "乳制品等,商业"
    },
    {
        "company_id": "beidahuang",
        "name_zh": "黑龙江北大荒农业股份有限公司",
        "stock_code": "600598.SH",
        "province": "黑龙江",
        "city": "哈尔滨市",
        "industry": "种植业",
        "main_business": "大米销售,种植业"
    },
    {
        "company_id": "st_panda",
        "name_zh": "熊猫金控股份有限公司",
        "stock_code": "600599.SH",
        "province": "湖南",
        "city": "长沙市",
        "industry": "化工原料",
        "main_business": "烟花生产销售以及烟花燃放"
    },
    {
        "company_id": "tsingtao",
        "name_zh": "青岛啤酒股份有限公司",
        "stock_code": "600600.SH",
        "province": "山东",
        "city": "青岛市",
        "industry": "啤酒",
        "main_business": "啤酒的生产与销售"
    },
    {
        "company_id": "founder_tech",
        "name_zh": "方正科技集团股份有限公司",
        "stock_code": "600601.SH",
        "province": "广东",
        "city": "珠海市",
        "industry": "元器件",
        "main_business": "电子计算机及配件,系统集成,办公设备及消耗材料,PCB产品"
    },
    {
        "company_id": "cloud_intelligence",
        "name_zh": "云赛智联股份有限公司",
        "stock_code": "600602.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "软件服务",
        "main_business": "消费电子,特殊电子,智能安防三大产业"
    },
    {
        "company_id": "guanghui_logistics",
        "name_zh": "广汇物流股份有限公司",
        "stock_code": "600603.SH",
        "province": "新疆",
        "city": "乌鲁木齐市",
        "industry": "区域地产",
        "main_business": "物流园区投资,经营及配套服务以及北站物流基地项目建设"
    },
    {
        "company_id": "shibei",
        "name_zh": "上海市北高新股份有限公司",
        "stock_code": "600604.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "园区开发",
        "main_business": "企业管理,投资管理,房地产开发经营,自有房屋出租,商务信息咨询"
    },
    {
        "company_id": "huitong",
        "name_zh": "上海汇通能源股份有限公司",
        "stock_code": "600605.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "房产服务",
        "main_business": "风力发电,有色金属(铜)批发贸易及房产租赁物业管理"
    },
    {
        "company_id": "greenland",
        "name_zh": "绿地控股集团股份有限公司",
        "stock_code": "600606.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "全国地产",
        "main_business": "住宅流通业务,住宅开发业务,住宅配套服务"
    }
]

EXPOSURES = [
    {
        "exposure_id": "bright_dairy_produce_dairy_product",
        "company_id": "bright_dairy",
        "node_id": "dairy_product",
        "activity_type": "produce",
        "role": "乳制品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "bright_dairy_produce_food",
        "company_id": "bright_dairy",
        "node_id": "food",
        "activity_type": "produce",
        "role": "食品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "beidahuang_produce_rice",
        "company_id": "beidahuang",
        "node_id": "rice",
        "activity_type": "produce",
        "role": "大米生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "beidahuang_produce_agricultural_product",
        "company_id": "beidahuang",
        "node_id": "agricultural_product",
        "activity_type": "produce",
        "role": "农产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_panda_produce_fireworks",
        "company_id": "st_panda",
        "node_id": "fireworks",
        "activity_type": "produce",
        "role": "烟花生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_panda_operate_entertainment",
        "company_id": "st_panda",
        "node_id": "entertainment",
        "activity_type": "operate",
        "role": "烟花燃放运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "tsingtao_produce_beer",
        "company_id": "tsingtao",
        "node_id": "beer",
        "activity_type": "produce",
        "role": "啤酒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tsingtao_produce_beverage",
        "company_id": "tsingtao",
        "node_id": "beverage",
        "activity_type": "produce",
        "role": "饮料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "founder_tech_manufacture_pcb_product",
        "company_id": "founder_tech",
        "node_id": "pcb_product",
        "activity_type": "manufacture",
        "role": "PCB产品制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "founder_tech_manufacture_computer",
        "company_id": "founder_tech",
        "node_id": "computer",
        "activity_type": "manufacture",
        "role": "计算机制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "founder_tech_provide_service_system_integration",
        "company_id": "founder_tech",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "cloud_intelligence_produce_consumer_electronics",
        "company_id": "cloud_intelligence",
        "node_id": "consumer_electronics",
        "activity_type": "produce",
        "role": "消费电子生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "cloud_intelligence_provide_service_intelligent_security",
        "company_id": "cloud_intelligence",
        "node_id": "intelligent_security",
        "activity_type": "provide_service",
        "role": "智能安防服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "cloud_intelligence_provide_service_software",
        "company_id": "cloud_intelligence",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "guanghui_logistics_operate_logistics_park",
        "company_id": "guanghui_logistics",
        "node_id": "logistics_park",
        "activity_type": "operate",
        "role": "物流园区运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "guanghui_logistics_provide_service_logistics",
        "company_id": "guanghui_logistics",
        "node_id": "logistics",
        "activity_type": "provide_service",
        "role": "物流服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "shibei_operate_real_estate_development",
        "company_id": "shibei",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "shibei_operate_investment_management",
        "company_id": "shibei",
        "node_id": "investment_management",
        "activity_type": "operate",
        "role": "投资管理运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "huitong_operate_wind_power",
        "company_id": "huitong",
        "node_id": "wind_power",
        "activity_type": "operate",
        "role": "风力发电运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "huitong_operate_power_generation",
        "company_id": "huitong",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "发电运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "huitong_operate_copper_trade",
        "company_id": "huitong",
        "node_id": "copper_trade",
        "activity_type": "operate",
        "role": "铜贸易商",
        "weight": 0.85
    },
    {
        "exposure_id": "greenland_operate_real_estate_development",
        "company_id": "greenland",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "greenland_operate_residential_circulation",
        "company_id": "greenland",
        "node_id": "residential_circulation",
        "activity_type": "operate",
        "role": "住宅流通运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "greenland_provide_service_property_management",
        "company_id": "greenland",
        "node_id": "property_management",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
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
            "evidence": make_evidence(f"tushare batch 086: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 086: " + e["description"]),
        })
    return {
        "batch_id": "batch_086",
        "task_description": "Batch 086: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 086: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_086",
        "task_description": "Batch 086: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 086 Submission")
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
