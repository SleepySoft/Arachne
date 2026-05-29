#!/usr/bin/env python3
"""Submit batch 072 to Arachne API."""
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
        "node_id": "telecom_power_supply",
        "canonical_name_zh": "通信电源",
        "definition": "为通信设备提供稳定电力的电源系统，包括开关电源、直流电源等",
        "entity_type": "device"
    },
    {
        "node_id": "photovoltaic_inverter",
        "canonical_name_zh": "光伏逆变器",
        "definition": "将太阳能电池板产生的直流电转换为交流电的电力电子设备",
        "entity_type": "device"
    },
    {
        "node_id": "power_grid_automation",
        "canonical_name_zh": "电网自动化",
        "definition": "利用计算机、通信和控制技术实现电力系统运行自动化的技术体系",
        "entity_type": "service"
    },
    {
        "node_id": "rail_transit_electrical",
        "canonical_name_zh": "轨道交通电气",
        "definition": "轨道交通系统中的电气设备与控制系统，包括牵引供电、信号控制等",
        "entity_type": "service"
    },
    {
        "node_id": "ac_motor",
        "canonical_name_zh": "交流电机",
        "definition": "利用交流电能产生旋转运动的电机，广泛应用于工业驱动和发电",
        "entity_type": "component"
    },
    {
        "node_id": "dc_motor",
        "canonical_name_zh": "直流电机",
        "definition": "利用直流电能产生旋转运动的电机，具有调速性能好的特点",
        "entity_type": "component"
    },
    {
        "node_id": "commercial_vehicle",
        "canonical_name_zh": "商用车",
        "definition": "用于商业运输目的的汽车，包括客车、货车、专用车等",
        "entity_type": "system"
    },
    {
        "node_id": "dairy_product",
        "canonical_name_zh": "乳制品",
        "definition": "以乳为主要原料加工制成的食品，包括液态奶、奶粉、酸奶、奶酪等",
        "entity_type": "material"
    },
    {
        "node_id": "antibiotic",
        "canonical_name_zh": "抗生素",
        "definition": "由微生物产生的能够抑制或杀灭其他微生物的化学物质，用于医疗抗感染治疗",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "telecom_power_supply_to_communication_equipment",
        "from_node": "telecom_power_supply",
        "to_node": "communication_equipment",
        "edge_type": "composition",
        "description": "通信电源为通信设备提供稳定电力供应，是其核心组成部分"
    },
    {
        "edge_id": "photovoltaic_inverter_to_solar_panel",
        "from_node": "photovoltaic_inverter",
        "to_node": "solar_panel",
        "edge_type": "composition",
        "description": "光伏逆变器是太阳能光伏发电系统的核心电力转换设备"
    },
    {
        "edge_id": "commercial_vehicle_to_automobile",
        "from_node": "commercial_vehicle",
        "to_node": "automobile",
        "edge_type": "composition",
        "description": "商用车是汽车整车的重要组成部分分类"
    }
]

COMPANIES = [
    {
        "company_id": "dianyuan",
        "name_zh": "北京动力源科技股份有限公司",
        "stock_code": "600405.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "电气设备",
        "main_business": "通信电源,高压直流电源,工业电源,应急电源(EPS),不间断电源(UPS),光伏逆变器,高压变频器"
    },
    {
        "company_id": "nari",
        "name_zh": "国电南瑞科技股份有限公司",
        "stock_code": "600406.SH",
        "province": "江苏",
        "city": "南京市",
        "industry": "电气设备",
        "main_business": "电网调度自动化,变电站自动化,农村电网自动化,火电厂及工业控制自动化,轨道交通电气"
    },
    {
        "company_id": "antai",
        "name_zh": "山西安泰集团股份有限公司",
        "stock_code": "600408.SH",
        "province": "山西",
        "city": "介休市",
        "industry": "焦炭加工",
        "main_business": "煤炭洗选,焦炭,生铁,水泥及其制品,电力的生产与销售"
    },
    {
        "company_id": "sanyou_chem",
        "name_zh": "唐山三友化工股份有限公司",
        "stock_code": "600409.SH",
        "province": "河北",
        "city": "唐山市",
        "industry": "化纤",
        "main_business": "纯碱和氯化钙产品的生产与销售"
    },
    {
        "company_id": "teamsun",
        "name_zh": "北京华胜天成科技股份有限公司",
        "stock_code": "600410.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "软件服务",
        "main_business": "系统产品及系统集成服务,软件及软件开发业务及专业服务"
    },
    {
        "company_id": "yiwu_market",
        "name_zh": "浙江中国小商品城集团股份有限公司",
        "stock_code": "600415.SH",
        "province": "浙江",
        "city": "义乌市",
        "industry": "商品城",
        "main_business": "市场网点经营,酒店服务,商品销售,房地产开发销售"
    },
    {
        "company_id": "xiangdian",
        "name_zh": "湘潭电机股份有限公司",
        "stock_code": "600416.SH",
        "province": "湖南",
        "city": "湘潭市",
        "industry": "电气设备",
        "main_business": "交流电机,直流电机,车辆,水泵"
    },
    {
        "company_id": "jac",
        "name_zh": "安徽江淮汽车集团股份有限公司",
        "stock_code": "600418.SH",
        "province": "安徽",
        "city": "合肥市",
        "industry": "汽车整车",
        "main_business": "商用车,乘用车及汽车底盘等"
    },
    {
        "company_id": "tianrun_dairy",
        "name_zh": "新疆天润乳业股份有限公司",
        "stock_code": "600419.SH",
        "province": "新疆",
        "city": "乌鲁木齐市",
        "industry": "乳制品",
        "main_business": "乳和乳制品,初乳素系列生物保健品"
    },
    {
        "company_id": "sinopharm_modern",
        "name_zh": "上海现代制药股份有限公司",
        "stock_code": "600420.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "化学制药",
        "main_business": "抗生素,保肝类,降压类,生化品种"
    }
]

EXPOSURES = [
    {
        "exposure_id": "dianyuan_manufacture_telecom_power_supply",
        "company_id": "dianyuan",
        "node_id": "telecom_power_supply",
        "activity_type": "manufacture",
        "role": "通信电源制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "dianyuan_manufacture_photovoltaic_inverter",
        "company_id": "dianyuan",
        "node_id": "photovoltaic_inverter",
        "activity_type": "manufacture",
        "role": "光伏逆变器制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "dianyuan_manufacture_ups",
        "company_id": "dianyuan",
        "node_id": "ups",
        "activity_type": "manufacture",
        "role": "不间断电源制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "dianyuan_manufacture_power_supply",
        "company_id": "dianyuan",
        "node_id": "power_supply",
        "activity_type": "manufacture",
        "role": "电源设备制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "nari_provide_service_power_grid_automation",
        "company_id": "nari",
        "node_id": "power_grid_automation",
        "activity_type": "provide_service",
        "role": "电网自动化服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "nari_provide_service_substation_automation",
        "company_id": "nari",
        "node_id": "substation_automation",
        "activity_type": "provide_service",
        "role": "变电站自动化服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "nari_provide_service_rail_transit_electrical",
        "company_id": "nari",
        "node_id": "rail_transit_electrical",
        "activity_type": "provide_service",
        "role": "轨道交通电气服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "nari_manufacture_power_distribution_equipment",
        "company_id": "nari",
        "node_id": "power_distribution_equipment",
        "activity_type": "manufacture",
        "role": "配电设备制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "antai_produce_coke",
        "company_id": "antai",
        "node_id": "coke",
        "activity_type": "produce",
        "role": "焦炭生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "antai_produce_pig_iron",
        "company_id": "antai",
        "node_id": "pig_iron",
        "activity_type": "produce",
        "role": "生铁生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "antai_produce_cement",
        "company_id": "antai",
        "node_id": "cement",
        "activity_type": "produce",
        "role": "水泥生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "antai_operate_power_generation",
        "company_id": "antai",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "发电运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "sanyou_chem_produce_soda_ash",
        "company_id": "sanyou_chem",
        "node_id": "soda_ash",
        "activity_type": "produce",
        "role": "纯碱生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sanyou_chem_produce_chemical_product",
        "company_id": "sanyou_chem",
        "node_id": "chemical_product",
        "activity_type": "produce",
        "role": "化工产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "teamsun_provide_service_software",
        "company_id": "teamsun",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "teamsun_provide_service_system_integration",
        "company_id": "teamsun",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "teamsun_provide_service_it_service",
        "company_id": "teamsun",
        "node_id": "it_service",
        "activity_type": "provide_service",
        "role": "IT服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "yiwu_market_operate_commodity_market",
        "company_id": "yiwu_market",
        "node_id": "commodity_market",
        "activity_type": "operate",
        "role": "商品市场运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "yiwu_market_operate_real_estate_development",
        "company_id": "yiwu_market",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "yiwu_market_operate_hotel_service",
        "company_id": "yiwu_market",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店服务商",
        "weight": 0.8
    },
    {
        "exposure_id": "xiangdian_manufacture_ac_motor",
        "company_id": "xiangdian",
        "node_id": "ac_motor",
        "activity_type": "manufacture",
        "role": "交流电机制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "xiangdian_manufacture_dc_motor",
        "company_id": "xiangdian",
        "node_id": "dc_motor",
        "activity_type": "manufacture",
        "role": "直流电机制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "xiangdian_manufacture_pump",
        "company_id": "xiangdian",
        "node_id": "pump",
        "activity_type": "manufacture",
        "role": "水泵制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jac_manufacture_commercial_vehicle",
        "company_id": "jac",
        "node_id": "commercial_vehicle",
        "activity_type": "manufacture",
        "role": "商用车制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "jac_manufacture_passenger_car",
        "company_id": "jac",
        "node_id": "passenger_car",
        "activity_type": "manufacture",
        "role": "乘用车制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jac_manufacture_automobile",
        "company_id": "jac",
        "node_id": "automobile",
        "activity_type": "manufacture",
        "role": "汽车整车制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianrun_dairy_produce_dairy_product",
        "company_id": "tianrun_dairy",
        "node_id": "dairy_product",
        "activity_type": "produce",
        "role": "乳制品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianrun_dairy_produce_food",
        "company_id": "tianrun_dairy",
        "node_id": "food",
        "activity_type": "produce",
        "role": "食品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "sinopharm_modern_produce_antibiotic",
        "company_id": "sinopharm_modern",
        "node_id": "antibiotic",
        "activity_type": "produce",
        "role": "抗生素生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sinopharm_modern_produce_pharmaceutical",
        "company_id": "sinopharm_modern",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
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
            "evidence": make_evidence(f"tushare batch 072: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 072: " + e["description"]),
        })
    return {
        "batch_id": "batch_072",
        "task_description": "Batch 072: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 072: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_072",
        "task_description": "Batch 072: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 072 Submission")
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
