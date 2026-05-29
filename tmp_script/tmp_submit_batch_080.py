#!/usr/bin/env python3
"""Submit batch 080 to Arachne API."""
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
        "node_id": "ev_material",
        "canonical_name_zh": "电动汽车相关材料",
        "definition": "用于新能源汽车动力电池、电机、电控等系统的关键材料和组件",
        "entity_type": "material"
    },
    {
        "node_id": "smart_factory_equipment",
        "canonical_name_zh": "智能工厂装备",
        "definition": "用于实现工厂自动化、数字化和智能化生产的机械设备和系统",
        "entity_type": "device"
    },
    {
        "node_id": "smart_grid_device",
        "canonical_name_zh": "智能电网设备",
        "definition": "用于电网智能化运行的设备和系统，包括智能电表、配电自动化设备等",
        "entity_type": "device"
    },
    {
        "node_id": "electrostatic_precipitator",
        "canonical_name_zh": "电除尘器",
        "definition": "利用高压静电场使烟气中的粉尘带电并分离收集的环保除尘设备",
        "entity_type": "device"
    },
    {
        "node_id": "polyester_top",
        "canonical_name_zh": "涤纶毛条",
        "definition": "由涤纶短纤维经过梳理、针梳等工序制成的条状纤维束，用于纺纱",
        "entity_type": "material"
    },
    {
        "node_id": "railway_project",
        "canonical_name_zh": "铁路工程",
        "definition": "铁路线路、桥梁、隧道、站场等基础设施的新建、改建和扩建工程",
        "entity_type": "service"
    },
    {
        "node_id": "molded_bottle",
        "canonical_name_zh": "模制瓶",
        "definition": "用模具吹制或压制成型的玻璃瓶，广泛用于药品、化妆品等包装",
        "entity_type": "component"
    },
    {
        "node_id": "electrolytic_lead",
        "canonical_name_zh": "电解铅",
        "definition": "通过电解精炼工艺生产的高纯度铅，用于蓄电池、电缆护套等",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "ev_material_to_electric_vehicle",
        "from_node": "ev_material",
        "to_node": "electric_vehicle",
        "edge_type": "composition",
        "description": "电动汽车相关材料是新能源汽车的核心组成物料"
    },
    {
        "edge_id": "smart_grid_device_to_power_grid",
        "from_node": "smart_grid_device",
        "to_node": "power_grid",
        "edge_type": "composition",
        "description": "智能电网设备是现代电力系统的关键组成设施"
    },
    {
        "edge_id": "electrostatic_precipitator_to_power_plant",
        "from_node": "electrostatic_precipitator",
        "to_node": "power_plant",
        "edge_type": "capability_supply",
        "description": "电除尘器为燃煤电厂提供烟气除尘环保能力"
    }
]

COMPANIES = [
    {
        "company_id": "st_changyuan",
        "name_zh": "长园科技集团股份有限公司",
        "stock_code": "600525.SH",
        "province": "广东",
        "city": "深圳市",
        "industry": "电气设备",
        "main_business": "电动汽车相关材料,智能工厂装备,智能电网设备"
    },
    {
        "company_id": "feida_env",
        "name_zh": "浙江菲达环保科技股份有限公司",
        "stock_code": "600526.SH",
        "province": "浙江",
        "city": "绍兴市",
        "industry": "环境保护",
        "main_business": "电除尘器产品,气力输送产品,脱硫产品"
    },
    {
        "company_id": "jiangnan_gaoxian",
        "name_zh": "江苏江南高纤股份有限公司",
        "stock_code": "600527.SH",
        "province": "江苏",
        "city": "苏州市",
        "industry": "化纤",
        "main_business": "涤纶毛条,涤纶短纤维"
    },
    {
        "company_id": "crec_industrial",
        "name_zh": "中铁高新工业股份有限公司",
        "stock_code": "600528.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "运输设备",
        "main_business": "铁路工程项目,其他工程项目"
    },
    {
        "company_id": "shandong_pharma_glass",
        "name_zh": "山东省药用玻璃股份有限公司",
        "stock_code": "600529.SH",
        "province": "山东",
        "city": "淄博市",
        "industry": "医疗保健",
        "main_business": "模制瓶,安瓿,管瓶,玻璃管,棕色瓶,丁基胶塞,塑料瓶,铝塑盖"
    },
    {
        "company_id": "sjtu_only",
        "name_zh": "上海交大昂立股份有限公司",
        "stock_code": "600530.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "医疗保健",
        "main_business": "食品及保健食品的原料和终端产品的研发,生产,销售"
    },
    {
        "company_id": "yuguang",
        "name_zh": "河南豫光金铅股份有限公司",
        "stock_code": "600531.SH",
        "province": "河南",
        "city": "济源市",
        "industry": "铅锌",
        "main_business": "电解铅及铅合金,白银,黄金"
    },
    {
        "company_id": "qixia",
        "name_zh": "南京栖霞建设股份有限公司",
        "stock_code": "600533.SH",
        "province": "江苏",
        "city": "南京市",
        "industry": "区域地产",
        "main_business": "房地产开发经营"
    },
    {
        "company_id": "tasly",
        "name_zh": "天士力医药集团股份有限公司",
        "stock_code": "600535.SH",
        "province": "天津",
        "city": "天津市",
        "industry": "中成药",
        "main_business": "中药,化学药,生物药"
    },
    {
        "company_id": "css",
        "name_zh": "中国软件与技术服务股份有限公司",
        "stock_code": "600536.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "软件服务",
        "main_business": "系统软件及支撑软件,应用软件及服务,软件出口加工及服务"
    }
]

EXPOSURES = [
    {
        "exposure_id": "st_changyuan_produce_ev_material",
        "company_id": "st_changyuan",
        "node_id": "ev_material",
        "activity_type": "produce",
        "role": "电动汽车材料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_changyuan_manufacture_smart_factory_equipment",
        "company_id": "st_changyuan",
        "node_id": "smart_factory_equipment",
        "activity_type": "manufacture",
        "role": "智能工厂装备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_changyuan_manufacture_smart_grid_device",
        "company_id": "st_changyuan",
        "node_id": "smart_grid_device",
        "activity_type": "manufacture",
        "role": "智能电网设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "feida_env_manufacture_electrostatic_precipitator",
        "company_id": "feida_env",
        "node_id": "electrostatic_precipitator",
        "activity_type": "manufacture",
        "role": "电除尘器制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "feida_env_provide_service_pneumatic_conveying",
        "company_id": "feida_env",
        "node_id": "pneumatic_conveying",
        "activity_type": "provide_service",
        "role": "气力输送服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "feida_env_manufacture_desulfurization_product",
        "company_id": "feida_env",
        "node_id": "desulfurization_product",
        "activity_type": "manufacture",
        "role": "脱硫产品制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jiangnan_gaoxian_produce_polyester_top",
        "company_id": "jiangnan_gaoxian",
        "node_id": "polyester_top",
        "activity_type": "produce",
        "role": "涤纶毛条生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jiangnan_gaoxian_produce_polyester_staple_fiber",
        "company_id": "jiangnan_gaoxian",
        "node_id": "polyester_staple_fiber",
        "activity_type": "produce",
        "role": "涤纶短纤维生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jiangnan_gaoxian_produce_chemical_fiber",
        "company_id": "jiangnan_gaoxian",
        "node_id": "chemical_fiber",
        "activity_type": "produce",
        "role": "化纤产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "crec_industrial_operate_railway_project",
        "company_id": "crec_industrial",
        "node_id": "railway_project",
        "activity_type": "operate",
        "role": "铁路工程运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "crec_industrial_manufacture_rail_transit_equipment",
        "company_id": "crec_industrial",
        "node_id": "rail_transit_equipment",
        "activity_type": "manufacture",
        "role": "轨道交通装备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shandong_pharma_glass_manufacture_molded_bottle",
        "company_id": "shandong_pharma_glass",
        "node_id": "molded_bottle",
        "activity_type": "manufacture",
        "role": "模制瓶制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "shandong_pharma_glass_manufacture_ampoule",
        "company_id": "shandong_pharma_glass",
        "node_id": "ampoule",
        "activity_type": "manufacture",
        "role": "安瓿制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shandong_pharma_glass_manufacture_butyl_rubber_stopper",
        "company_id": "shandong_pharma_glass",
        "node_id": "butyl_rubber_stopper",
        "activity_type": "manufacture",
        "role": "丁基胶塞制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shandong_pharma_glass_manufacture_pharmaceutical_packaging",
        "company_id": "shandong_pharma_glass",
        "node_id": "pharmaceutical_packaging",
        "activity_type": "manufacture",
        "role": "药用包装制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "sjtu_only_produce_health_food",
        "company_id": "sjtu_only",
        "node_id": "health_food",
        "activity_type": "produce",
        "role": "保健食品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sjtu_only_produce_food",
        "company_id": "sjtu_only",
        "node_id": "food",
        "activity_type": "produce",
        "role": "食品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "yuguang_produce_electrolytic_lead",
        "company_id": "yuguang",
        "node_id": "electrolytic_lead",
        "activity_type": "produce",
        "role": "电解铅生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "yuguang_produce_silver_product",
        "company_id": "yuguang",
        "node_id": "silver_product",
        "activity_type": "produce",
        "role": "白银生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "yuguang_produce_gold",
        "company_id": "yuguang",
        "node_id": "gold",
        "activity_type": "produce",
        "role": "黄金生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "qixia_operate_real_estate_development",
        "company_id": "qixia",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "tasly_produce_chinese_patent_medicine",
        "company_id": "tasly",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tasly_produce_chemical_drug",
        "company_id": "tasly",
        "node_id": "chemical_drug",
        "activity_type": "produce",
        "role": "化学药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "tasly_produce_biological_drug",
        "company_id": "tasly",
        "node_id": "biological_drug",
        "activity_type": "produce",
        "role": "生物药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "css_provide_service_system_software",
        "company_id": "css",
        "node_id": "system_software",
        "activity_type": "provide_service",
        "role": "系统软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "css_provide_service_application_software",
        "company_id": "css",
        "node_id": "application_software",
        "activity_type": "provide_service",
        "role": "应用软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "css_provide_service_software_export",
        "company_id": "css",
        "node_id": "software_export",
        "activity_type": "provide_service",
        "role": "软件出口加工服务商",
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
            "evidence": make_evidence(f"tushare batch 080: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 080: " + e["description"]),
        })
    return {
        "batch_id": "batch_080",
        "task_description": "Batch 080: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 080: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_080",
        "task_description": "Batch 080: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 080 Submission")
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
