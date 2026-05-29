#!/usr/bin/env python3
"""Submit batch 084 to Arachne API."""
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
        "node_id": "enameled_wire",
        "canonical_name_zh": "漆包电磁线",
        "definition": "表面涂覆绝缘漆的铜或铝导线，用于电机、变压器等电气设备的绕组",
        "entity_type": "material"
    },
    {
        "node_id": "power_cable",
        "canonical_name_zh": "电线电缆",
        "definition": "用于传输和分配电能的导线及其绝缘护套的组合产品",
        "entity_type": "component"
    },
    {
        "node_id": "desulfurization_byproduct",
        "canonical_name_zh": "脱硫副产品",
        "definition": "燃煤电厂烟气脱硫过程中产生的副产物，如石膏等",
        "entity_type": "material"
    },
    {
        "node_id": "chemical_equipment",
        "canonical_name_zh": "化工装备",
        "definition": "用于化工生产过程的专用机械设备，包括反应釜、换热器、塔器等",
        "entity_type": "device"
    },
    {
        "node_id": "industrial_motor",
        "canonical_name_zh": "工业驱动及控制电机",
        "definition": "用于驱动工业生产机械设备的电动机及其控制系统",
        "entity_type": "component"
    },
    {
        "node_id": "electric_bicycle",
        "canonical_name_zh": "电动自行车",
        "definition": "以蓄电池为辅助能源，在普通自行车基础上安装电机和控制系统的两轮交通工具",
        "entity_type": "system"
    },
    {
        "node_id": "mining_automation",
        "canonical_name_zh": "矿山自动化",
        "definition": "利用自动化技术实现矿山采掘、运输、通风等过程的无人化或少人化运行",
        "entity_type": "service"
    },
    {
        "node_id": "ocean_engineering",
        "canonical_name_zh": "海洋工程",
        "definition": "在海洋环境中进行的油气开发、海上风电等工程建设和运维服务",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "enameled_wire_to_motor",
        "from_node": "enameled_wire",
        "to_node": "motor",
        "edge_type": "composition",
        "description": "漆包电磁线是电机和变压器绕组的核心导电材料"
    },
    {
        "edge_id": "industrial_motor_to_industrial_equipment",
        "from_node": "industrial_motor",
        "to_node": "industrial_equipment",
        "edge_type": "composition",
        "description": "工业电机是驱动各类工业机械设备的核心动力部件"
    },
    {
        "edge_id": "ocean_engineering_to_offshore_oil",
        "from_node": "ocean_engineering",
        "to_node": "offshore_oil",
        "edge_type": "capability_supply",
        "description": "海洋工程为海上油气开发提供平台建设和运维服务能力"
    }
]

COMPANIES = [
    {
        "company_id": "xiangyuan",
        "name_zh": "浙江祥源文旅股份有限公司",
        "stock_code": "600576.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "旅游景点",
        "main_business": "房地产开发,连锁酒店经营投资"
    },
    {
        "company_id": "jinda",
        "name_zh": "铜陵精达特种电磁线股份有限公司",
        "stock_code": "600577.SH",
        "province": "安徽",
        "city": "铜陵市",
        "industry": "电气设备",
        "main_business": "漆包电磁线,裸铜线和电线电缆的制造和销售"
    },
    {
        "company_id": "jingneng_power",
        "name_zh": "北京京能电力股份有限公司",
        "stock_code": "600578.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "火力发电",
        "main_business": "发电量,供热量,脱硫副产品"
    },
    {
        "company_id": "sinochem_equip",
        "name_zh": "中化装备科技(青岛)股份有限公司",
        "stock_code": "600579.SH",
        "province": "山东",
        "city": "青岛市",
        "industry": "化工机械",
        "main_business": "化工装备的研发,生产和销售"
    },
    {
        "company_id": "wolong",
        "name_zh": "卧龙电气驱动集团股份有限公司",
        "stock_code": "600580.SH",
        "province": "浙江",
        "city": "绍兴市",
        "industry": "电气设备",
        "main_business": "工业驱动及控制电机,中高压电机,家用电器电机,微电机,电动自行车,蓄电池"
    },
    {
        "company_id": "st_bayi",
        "name_zh": "新疆八一钢铁股份有限公司",
        "stock_code": "600581.SH",
        "province": "新疆",
        "city": "乌鲁木齐市",
        "industry": "普钢",
        "main_business": "高速线材,螺纹钢,热轧板卷,冷轧薄板,中厚板等建筑及工业用钢"
    },
    {
        "company_id": "tiandi",
        "name_zh": "天地科技股份有限公司",
        "stock_code": "600582.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "专用机械",
        "main_business": "矿山自动化,机械化设备,煤炭洗选装备,矿井生产技术服务与经营,地下特殊工程施工"
    },
    {
        "company_id": "cooec",
        "name_zh": "海洋石油工程股份有限公司",
        "stock_code": "600583.SH",
        "province": "天津",
        "city": "天津市",
        "industry": "石油开采",
        "main_business": "海洋工程"
    },
    {
        "company_id": "jcet",
        "name_zh": "江苏长电科技股份有限公司",
        "stock_code": "600584.SH",
        "province": "江苏",
        "city": "无锡市",
        "industry": "半导体",
        "main_business": "集成电路封装测试,分立器件制造销售"
    },
    {
        "company_id": "conch",
        "name_zh": "安徽海螺水泥股份有限公司",
        "stock_code": "600585.SH",
        "province": "安徽",
        "city": "芜湖市",
        "industry": "水泥",
        "main_business": "水泥的生产与销售"
    }
]

EXPOSURES = [
    {
        "exposure_id": "xiangyuan_operate_real_estate_development",
        "company_id": "xiangyuan",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "xiangyuan_operate_hotel_service",
        "company_id": "xiangyuan",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "连锁酒店运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "xiangyuan_operate_tourism_investment",
        "company_id": "xiangyuan",
        "node_id": "tourism_investment",
        "activity_type": "operate",
        "role": "文旅投资运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "jinda_produce_enameled_wire",
        "company_id": "jinda",
        "node_id": "enameled_wire",
        "activity_type": "produce",
        "role": "漆包电磁线生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinda_produce_bare_copper_wire",
        "company_id": "jinda",
        "node_id": "bare_copper_wire",
        "activity_type": "produce",
        "role": "裸铜线生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinda_produce_power_cable",
        "company_id": "jinda",
        "node_id": "power_cable",
        "activity_type": "produce",
        "role": "电线电缆生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "jingneng_power_operate_power_generation",
        "company_id": "jingneng_power",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "发电运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "jingneng_power_provide_service_heating_supply",
        "company_id": "jingneng_power",
        "node_id": "heating_supply",
        "activity_type": "provide_service",
        "role": "热力供应商",
        "weight": 0.9
    },
    {
        "exposure_id": "jingneng_power_produce_desulfurization_byproduct",
        "company_id": "jingneng_power",
        "node_id": "desulfurization_byproduct",
        "activity_type": "produce",
        "role": "脱硫副产品生产商",
        "weight": 0.8
    },
    {
        "exposure_id": "sinochem_equip_manufacture_chemical_equipment",
        "company_id": "sinochem_equip",
        "node_id": "chemical_equipment",
        "activity_type": "manufacture",
        "role": "化工装备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "sinochem_equip_operate_chemical_industry",
        "company_id": "sinochem_equip",
        "node_id": "chemical_industry",
        "activity_type": "operate",
        "role": "化工行业服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "wolong_manufacture_industrial_motor",
        "company_id": "wolong",
        "node_id": "industrial_motor",
        "activity_type": "manufacture",
        "role": "工业电机制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "wolong_manufacture_medium_high_voltage_motor",
        "company_id": "wolong",
        "node_id": "medium_high_voltage_motor",
        "activity_type": "manufacture",
        "role": "中高压电机制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "wolong_manufacture_household_appliance_motor",
        "company_id": "wolong",
        "node_id": "household_appliance_motor",
        "activity_type": "manufacture",
        "role": "家用电器电机制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "wolong_manufacture_electric_bicycle",
        "company_id": "wolong",
        "node_id": "electric_bicycle",
        "activity_type": "manufacture",
        "role": "电动自行车制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "st_bayi_produce_high_speed_wire_rod",
        "company_id": "st_bayi",
        "node_id": "high_speed_wire_rod",
        "activity_type": "produce",
        "role": "高速线材生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_bayi_produce_rebar",
        "company_id": "st_bayi",
        "node_id": "rebar",
        "activity_type": "produce",
        "role": "螺纹钢生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_bayi_produce_hot_rolled_coil",
        "company_id": "st_bayi",
        "node_id": "hot_rolled_coil",
        "activity_type": "produce",
        "role": "热轧卷板生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_bayi_produce_steel",
        "company_id": "st_bayi",
        "node_id": "steel",
        "activity_type": "produce",
        "role": "钢铁生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tiandi_provide_service_mining_automation",
        "company_id": "tiandi",
        "node_id": "mining_automation",
        "activity_type": "provide_service",
        "role": "矿山自动化服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "tiandi_manufacture_coal_washing_equipment",
        "company_id": "tiandi",
        "node_id": "coal_washing_equipment",
        "activity_type": "manufacture",
        "role": "煤炭洗选装备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tiandi_operate_coal_mining",
        "company_id": "tiandi",
        "node_id": "coal_mining",
        "activity_type": "operate",
        "role": "煤炭开采运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "cooec_operate_ocean_engineering",
        "company_id": "cooec",
        "node_id": "ocean_engineering",
        "activity_type": "operate",
        "role": "海洋工程运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "cooec_provide_service_offshore_oil",
        "company_id": "cooec",
        "node_id": "offshore_oil",
        "activity_type": "provide_service",
        "role": "海上油气工程服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "jcet_provide_service_integrated_circuit_packaging",
        "company_id": "jcet",
        "node_id": "integrated_circuit_packaging",
        "activity_type": "provide_service",
        "role": "集成电路封装测试服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "jcet_manufacture_semiconductor_device",
        "company_id": "jcet",
        "node_id": "semiconductor_device",
        "activity_type": "manufacture",
        "role": "半导体分立器件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "conch_produce_cement",
        "company_id": "conch",
        "node_id": "cement",
        "activity_type": "produce",
        "role": "水泥生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "conch_produce_building_material",
        "company_id": "conch",
        "node_id": "building_material",
        "activity_type": "produce",
        "role": "建材生产商",
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
            "evidence": make_evidence(f"tushare batch 084: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 084: " + e["description"]),
        })
    return {
        "batch_id": "batch_084",
        "task_description": "Batch 084: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 084: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_084",
        "task_description": "Batch 084: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 084 Submission")
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
