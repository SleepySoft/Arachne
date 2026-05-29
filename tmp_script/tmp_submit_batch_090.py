#!/usr/bin/env python3
"""Submit batch 090 to Arachne API."""
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
        "node_id": "power_transformation_equipment",
        "canonical_name_zh": "输变电设备",
        "definition": "用于电能输送和电压变换的电力设备总称，包括变压器、开关设备、输电线路等",
        "entity_type": "device"
    },
    {
        "node_id": "ac_motor",
        "canonical_name_zh": "交流电动机",
        "definition": "利用交流电产生旋转磁场驱动转子转动的电动机，是工业生产中最常用的动力设备",
        "entity_type": "component"
    },
    {
        "node_id": "carrier_wave_communication",
        "canonical_name_zh": "载波通信",
        "definition": "利用高频载波信号传输信息的通信方式，广泛应用于电力线载波通信等领域",
        "entity_type": "service"
    },
    {
        "node_id": "life_science",
        "canonical_name_zh": "生命科技",
        "definition": "以生物学、医学为基础，研究生命现象和开发生物技术产品的科学技术领域",
        "entity_type": "service"
    },
    {
        "node_id": "raw_water_supply",
        "canonical_name_zh": "原水供应",
        "definition": "从水源地取水并向水厂或用户供应未经处理或初步处理的原水的服务",
        "entity_type": "service"
    },
    {
        "node_id": "lamp_bulb",
        "canonical_name_zh": "灯泡",
        "definition": "将电能转换为光能的照明器件，包括白炽灯、节能灯、LED灯等",
        "entity_type": "component"
    },
    {
        "node_id": "automotive_electronics",
        "canonical_name_zh": "汽车电子",
        "definition": "应用于汽车上的电子控制系统和电子装置，包括发动机控制、车载娱乐、驾驶辅助等",
        "entity_type": "component"
    },
    {
        "node_id": "security_fire_system",
        "canonical_name_zh": "安防消防系统集成",
        "definition": "将安全防范和消防系统进行整合设计、安装和运维的综合服务",
        "entity_type": "service"
    }
]

NEW_EDGES = [
    {
        "edge_id": "power_transformation_equipment_to_power_grid",
        "from_node": "power_transformation_equipment",
        "to_node": "power_grid",
        "edge_type": "composition",
        "description": "输变电设备是电力输配电网的核心组成装备"
    },
    {
        "edge_id": "lamp_bulb_to_lighting",
        "from_node": "lamp_bulb",
        "to_node": "lighting",
        "edge_type": "composition",
        "description": "灯泡是照明系统的核心发光部件"
    },
    {
        "edge_id": "automotive_electronics_to_automobile",
        "from_node": "automotive_electronics",
        "to_node": "automobile",
        "edge_type": "composition",
        "description": "汽车电子是现代汽车智能化和电气化的核心系统"
    }
]

COMPANIES = [
    {
        "company_id": "leshan_power",
        "name_zh": "乐山电力股份有限公司",
        "stock_code": "600644.SH",
        "province": "四川",
        "city": "乐山市",
        "industry": "水力发电",
        "main_business": "电力设施承装,承修,承试,地方电力开发,房地产,输变电设备,电工器材,交流电动机,载波通信"
    },
    {
        "company_id": "zhongyuanxiehe",
        "name_zh": "中源协和细胞基因工程股份有限公司",
        "stock_code": "600645.SH",
        "province": "天津",
        "city": "天津市",
        "industry": "医疗保健",
        "main_business": "工业,商业,房地产业,服务业,生命科技"
    },
    {
        "company_id": "waigaoqiao",
        "name_zh": "上海外高桥集团股份有限公司",
        "stock_code": "600648.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "园区开发",
        "main_business": "房地产开发与租赁,贸易及物流,酒店经营管理等"
    },
    {
        "company_id": "chengtou",
        "name_zh": "上海城投控股股份有限公司",
        "stock_code": "600649.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "区域地产",
        "main_business": "原水供应,污水处理"
    },
    {
        "company_id": "jinjiang_online",
        "name_zh": "上海锦江在线网络服务股份有限公司",
        "stock_code": "600650.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "公共交通",
        "main_business": "客房,餐饮,商场,客运,物流"
    },
    {
        "company_id": "feile_audio",
        "name_zh": "上海飞乐音响股份有限公司",
        "stock_code": "600651.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "电器仪表",
        "main_business": "灯泡,灯具及光源类产品,电子类产品,IC卡及相关软件开发和系统集成,音响类产品"
    },
    {
        "company_id": "shenhua",
        "name_zh": "上海申华控股股份有限公司",
        "stock_code": "600653.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "汽车服务",
        "main_business": "汽车消费相关产业为主导产业,以新能源产业,房地产等投资作为补充"
    },
    {
        "company_id": "coa_security",
        "name_zh": "中安科股份有限公司",
        "stock_code": "600654.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "仓储物流",
        "main_business": "安防消防系统集成,产品制造,综合运营服务,汽车电子,线束,电子材料,无线通信设备"
    },
    {
        "company_id": "yuyuan",
        "name_zh": "上海豫园旅游商城(集团)股份有限公司",
        "stock_code": "600655.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "百货",
        "main_business": "黄金饰品,百货,饮食,食品,进出口,医药,工艺品,房产"
    },
    {
        "company_id": "cinda_realestate",
        "name_zh": "信达地产股份有限公司",
        "stock_code": "600657.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "全国地产",
        "main_business": "房地产开发,投资及投资管理,物业管理"
    }
]

EXPOSURES = [
    {
        "exposure_id": "leshan_power_provide_service_power_installation",
        "company_id": "leshan_power",
        "node_id": "power_installation",
        "activity_type": "provide_service",
        "role": "电力设施承装服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "leshan_power_manufacture_power_transformation_equipment",
        "company_id": "leshan_power",
        "node_id": "power_transformation_equipment",
        "activity_type": "manufacture",
        "role": "输变电设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "leshan_power_produce_ac_motor",
        "company_id": "leshan_power",
        "node_id": "ac_motor",
        "activity_type": "produce",
        "role": "交流电动机生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "leshan_power_provide_service_carrier_wave_communication",
        "company_id": "leshan_power",
        "node_id": "carrier_wave_communication",
        "activity_type": "provide_service",
        "role": "载波通信服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "leshan_power_operate_power_generation",
        "company_id": "leshan_power",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "地方电力运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongyuanxiehe_provide_service_life_science",
        "company_id": "zhongyuanxiehe",
        "node_id": "life_science",
        "activity_type": "provide_service",
        "role": "生命科技服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongyuanxiehe_produce_biotechnology",
        "company_id": "zhongyuanxiehe",
        "node_id": "biotechnology",
        "activity_type": "produce",
        "role": "生物技术产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "waigaoqiao_operate_real_estate_development",
        "company_id": "waigaoqiao",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "waigaoqiao_provide_service_trade_logistics",
        "company_id": "waigaoqiao",
        "node_id": "trade_logistics",
        "activity_type": "provide_service",
        "role": "贸易物流服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "waigaoqiao_operate_hotel_service",
        "company_id": "waigaoqiao",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店经营管理商",
        "weight": 0.85
    },
    {
        "exposure_id": "chengtou_provide_service_raw_water_supply",
        "company_id": "chengtou",
        "node_id": "raw_water_supply",
        "activity_type": "provide_service",
        "role": "原水供应服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "chengtou_operate_sewage_treatment",
        "company_id": "chengtou",
        "node_id": "sewage_treatment",
        "activity_type": "operate",
        "role": "污水处理运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinjiang_online_operate_hotel_service",
        "company_id": "jinjiang_online",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinjiang_online_operate_catering_service",
        "company_id": "jinjiang_online",
        "node_id": "catering_service",
        "activity_type": "operate",
        "role": "餐饮服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinjiang_online_operate_passenger_transport",
        "company_id": "jinjiang_online",
        "node_id": "passenger_transport",
        "activity_type": "operate",
        "role": "客运运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinjiang_online_provide_service_logistics",
        "company_id": "jinjiang_online",
        "node_id": "logistics",
        "activity_type": "provide_service",
        "role": "物流服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "feile_audio_manufacture_lamp_bulb",
        "company_id": "feile_audio",
        "node_id": "lamp_bulb",
        "activity_type": "manufacture",
        "role": "灯泡制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "feile_audio_manufacture_lighting_fixture",
        "company_id": "feile_audio",
        "node_id": "lighting_fixture",
        "activity_type": "manufacture",
        "role": "灯具制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "feile_audio_manufacture_audio_equipment",
        "company_id": "feile_audio",
        "node_id": "audio_equipment",
        "activity_type": "manufacture",
        "role": "音响产品制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shenhua_provide_service_automotive_service",
        "company_id": "shenhua",
        "node_id": "automotive_service",
        "activity_type": "provide_service",
        "role": "汽车消费服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenhua_produce_new_energy",
        "company_id": "shenhua",
        "node_id": "new_energy",
        "activity_type": "produce",
        "role": "新能源产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "shenhua_operate_real_estate_development",
        "company_id": "shenhua",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "coa_security_provide_service_security_fire_system",
        "company_id": "coa_security",
        "node_id": "security_fire_system",
        "activity_type": "provide_service",
        "role": "安防消防系统集成商",
        "weight": 0.95
    },
    {
        "exposure_id": "coa_security_manufacture_automotive_electronics",
        "company_id": "coa_security",
        "node_id": "automotive_electronics",
        "activity_type": "manufacture",
        "role": "汽车电子制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "coa_security_manufacture_wire_harness",
        "company_id": "coa_security",
        "node_id": "wire_harness",
        "activity_type": "manufacture",
        "role": "线束制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "coa_security_manufacture_communication_equipment",
        "company_id": "coa_security",
        "node_id": "communication_equipment",
        "activity_type": "manufacture",
        "role": "无线通信设备制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "yuyuan_produce_gold_ornament",
        "company_id": "yuyuan",
        "node_id": "gold_ornament",
        "activity_type": "produce",
        "role": "黄金饰品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "yuyuan_operate_department_store",
        "company_id": "yuyuan",
        "node_id": "department_store",
        "activity_type": "operate",
        "role": "百货运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "yuyuan_operate_catering_service",
        "company_id": "yuyuan",
        "node_id": "catering_service",
        "activity_type": "operate",
        "role": "饮食服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "yuyuan_produce_pharmaceutical",
        "company_id": "yuyuan",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "cinda_realestate_operate_real_estate_development",
        "company_id": "cinda_realestate",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "cinda_realestate_operate_real_estate_investment",
        "company_id": "cinda_realestate",
        "node_id": "real_estate_investment",
        "activity_type": "operate",
        "role": "房地产投资运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "cinda_realestate_provide_service_property_management",
        "company_id": "cinda_realestate",
        "node_id": "property_management",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
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
            "evidence": make_evidence(f"tushare batch 090: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 090: " + e["description"]),
        })
    return {
        "batch_id": "batch_090",
        "task_description": "Batch 090: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 090: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_090",
        "task_description": "Batch 090: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 090 Submission")
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
