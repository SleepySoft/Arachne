#!/usr/bin/env python3
"""Submit batch 075 to Arachne API."""
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
        "node_id": "precious_metal_functional_material",
        "canonical_name_zh": "贵金属特种功能材料",
        "definition": "以金、银、铂、钯等贵金属为基础，具有特殊电、磁、热、催化等功能特性的材料",
        "entity_type": "material"
    },
    {
        "node_id": "integrated_circuit",
        "canonical_name_zh": "集成电路",
        "definition": "将大量晶体管、电阻、电容等电子元件集成在半导体芯片上的电子器件",
        "entity_type": "component"
    },
    {
        "node_id": "semiconductor_discrete_device",
        "canonical_name_zh": "半导体分立器件",
        "definition": "具有单一功能的独立半导体器件，如二极管、三极管、晶闸管等",
        "entity_type": "component"
    },
    {
        "node_id": "led_product",
        "canonical_name_zh": "LED产品",
        "definition": "基于发光二极管技术的照明和显示产品，具有高效节能的特点",
        "entity_type": "component"
    },
    {
        "node_id": "water_supply",
        "canonical_name_zh": "自来水供应",
        "definition": "通过取水、净化、输配等工艺向城市居民和工业用户提供自来水的服务",
        "entity_type": "service"
    },
    {
        "node_id": "city_sewage_treatment",
        "canonical_name_zh": "城市污水处理",
        "definition": "对城市生活污水和工业废水进行收集、处理和排放的环保服务",
        "entity_type": "service"
    },
    {
        "node_id": "sea_cucumber",
        "canonical_name_zh": "海参",
        "definition": "一种珍贵的海洋棘皮动物，具有高营养和药用价值的海产品",
        "entity_type": "material"
    },
    {
        "node_id": "phosphate_fertilizer",
        "canonical_name_zh": "磷肥",
        "definition": "以磷酸盐为主要成分的化肥，为作物提供磷营养，促进根系发育和开花结果",
        "entity_type": "material"
    },
    {
        "node_id": "power_generation_equipment",
        "canonical_name_zh": "发电设备",
        "definition": "用于将各种能源转换为电能的机械设备和系统，包括锅炉、汽轮机、发电机等",
        "entity_type": "device"
    }
]

NEW_EDGES = [
    {
        "edge_id": "integrated_circuit_to_electronic_device",
        "from_node": "integrated_circuit",
        "to_node": "electronic_device",
        "edge_type": "composition",
        "description": "集成电路是电子设备和系统的核心组成部件"
    },
    {
        "edge_id": "led_product_to_lighting",
        "from_node": "led_product",
        "to_node": "lighting",
        "edge_type": "composition",
        "description": "LED产品是现代照明系统的核心发光组件"
    },
    {
        "edge_id": "power_generation_equipment_to_power_generation",
        "from_node": "power_generation_equipment",
        "to_node": "power_generation",
        "edge_type": "composition",
        "description": "发电设备是电力生产系统的核心装备组成"
    }
]

COMPANIES = [
    {
        "company_id": "sino_platinum",
        "name_zh": "贵研铂业股份有限公司",
        "stock_code": "600459.SH",
        "province": "云南",
        "city": "昆明市",
        "industry": "小金属",
        "main_business": "贵金属特种功能材料,环保及催化功能材料,信息功能材料,再生资源材料"
    },
    {
        "company_id": "silan",
        "name_zh": "杭州士兰微电子股份有限公司",
        "stock_code": "600460.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "半导体",
        "main_business": "集成电路,半导体分立器件,LED(发光二极管)产品"
    },
    {
        "company_id": "hongcheng_env",
        "name_zh": "江西洪城环境股份有限公司",
        "stock_code": "600461.SH",
        "province": "江西",
        "city": "南昌市",
        "industry": "水务",
        "main_business": "自来水的生产和销售,城市污水处理,燃气能源"
    },
    {
        "company_id": "airport_co",
        "name_zh": "北京空港科技园区股份有限公司",
        "stock_code": "600463.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "园区开发",
        "main_business": "园区开发建设,工业地产开发,建筑施工,物业经营与管理"
    },
    {
        "company_id": "haodangjia",
        "name_zh": "山东好当家海洋发展股份有限公司",
        "stock_code": "600467.SH",
        "province": "山东",
        "city": "威海市",
        "industry": "渔业",
        "main_business": "海参,牙鲆鱼,鲍鱼,海蛰等各种鲜活海产品和冷冻食品"
    },
    {
        "company_id": "baili_elec",
        "name_zh": "天津百利特精电气股份有限公司",
        "stock_code": "600468.SH",
        "province": "天津",
        "city": "天津市",
        "industry": "电气设备",
        "main_business": "输配电及控制设备,泵,钨钼制品"
    },
    {
        "company_id": "aeolus",
        "name_zh": "风神轮胎股份有限公司",
        "stock_code": "600469.SH",
        "province": "河南",
        "city": "焦作市",
        "industry": "汽车配件",
        "main_business": "斜交胎,全钢载重子午胎"
    },
    {
        "company_id": "liuguo_chem",
        "name_zh": "安徽六国化工股份有限公司",
        "stock_code": "600470.SH",
        "province": "安徽",
        "city": "铜陵市",
        "industry": "农药化肥",
        "main_business": "磷酸二铵"
    },
    {
        "company_id": "huaguang",
        "name_zh": "无锡华光环保能源集团股份有限公司",
        "stock_code": "600475.SH",
        "province": "江苏",
        "city": "无锡市",
        "industry": "电气设备",
        "main_business": "节能高效发电设备,环保新能源发电设备,环境工程,电站工程,地方能源供应"
    },
    {
        "company_id": "st_xiangyou",
        "name_zh": "湖南湘邮科技股份有限公司",
        "stock_code": "600476.SH",
        "province": "湖南",
        "city": "长沙市",
        "industry": "软件服务",
        "main_business": "系统集成,产品销售,房地产,软件,设计,邮政软件开发"
    }
]

EXPOSURES = [
    {
        "exposure_id": "sino_platinum_produce_precious_metal_functional_material",
        "company_id": "sino_platinum",
        "node_id": "precious_metal_functional_material",
        "activity_type": "produce",
        "role": "贵金属功能材料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "sino_platinum_produce_catalytic_functional_material",
        "company_id": "sino_platinum",
        "node_id": "catalytic_functional_material",
        "activity_type": "produce",
        "role": "催化功能材料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "sino_platinum_produce_nonferrous_metal",
        "company_id": "sino_platinum",
        "node_id": "nonferrous_metal",
        "activity_type": "produce",
        "role": "有色金属生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "silan_manufacture_integrated_circuit",
        "company_id": "silan",
        "node_id": "integrated_circuit",
        "activity_type": "manufacture",
        "role": "集成电路制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "silan_manufacture_semiconductor_discrete_device",
        "company_id": "silan",
        "node_id": "semiconductor_discrete_device",
        "activity_type": "manufacture",
        "role": "半导体分立器件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "silan_manufacture_led_product",
        "company_id": "silan",
        "node_id": "led_product",
        "activity_type": "manufacture",
        "role": "LED产品制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "silan_manufacture_electronic_component",
        "company_id": "silan",
        "node_id": "electronic_component",
        "activity_type": "manufacture",
        "role": "电子元器件制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "hongcheng_env_provide_service_water_supply",
        "company_id": "hongcheng_env",
        "node_id": "water_supply",
        "activity_type": "provide_service",
        "role": "自来水供应商",
        "weight": 0.95
    },
    {
        "exposure_id": "hongcheng_env_operate_city_sewage_treatment",
        "company_id": "hongcheng_env",
        "node_id": "city_sewage_treatment",
        "activity_type": "operate",
        "role": "污水处理运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "hongcheng_env_provide_service_gas_energy",
        "company_id": "hongcheng_env",
        "node_id": "gas_energy",
        "activity_type": "provide_service",
        "role": "燃气能源供应商",
        "weight": 0.85
    },
    {
        "exposure_id": "airport_co_operate_industrial_park",
        "company_id": "airport_co",
        "node_id": "industrial_park",
        "activity_type": "operate",
        "role": "产业园区运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "airport_co_operate_real_estate_development",
        "company_id": "airport_co",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "airport_co_operate_construction",
        "company_id": "airport_co",
        "node_id": "construction",
        "activity_type": "operate",
        "role": "建筑施工运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "haodangjia_produce_sea_cucumber",
        "company_id": "haodangjia",
        "node_id": "sea_cucumber",
        "activity_type": "produce",
        "role": "海参生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "haodangjia_produce_seafood",
        "company_id": "haodangjia",
        "node_id": "seafood",
        "activity_type": "produce",
        "role": "海产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "haodangjia_operate_aquaculture",
        "company_id": "haodangjia",
        "node_id": "aquaculture",
        "activity_type": "operate",
        "role": "水产养殖运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "baili_elec_manufacture_power_distribution_equipment",
        "company_id": "baili_elec",
        "node_id": "power_distribution_equipment",
        "activity_type": "manufacture",
        "role": "输配电设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "baili_elec_manufacture_pump",
        "company_id": "baili_elec",
        "node_id": "pump",
        "activity_type": "manufacture",
        "role": "水泵制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "baili_elec_produce_tungsten_molybdenum_product",
        "company_id": "baili_elec",
        "node_id": "tungsten_molybdenum_product",
        "activity_type": "produce",
        "role": "钨钼制品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "aeolus_manufacture_tire",
        "company_id": "aeolus",
        "node_id": "tire",
        "activity_type": "manufacture",
        "role": "轮胎制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "aeolus_manufacture_automobile_part",
        "company_id": "aeolus",
        "node_id": "automobile_part",
        "activity_type": "manufacture",
        "role": "汽车零部件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "liuguo_chem_produce_phosphate_fertilizer",
        "company_id": "liuguo_chem",
        "node_id": "phosphate_fertilizer",
        "activity_type": "produce",
        "role": "磷肥生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "liuguo_chem_produce_chemical_product",
        "company_id": "liuguo_chem",
        "node_id": "chemical_product",
        "activity_type": "produce",
        "role": "化工产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "huaguang_manufacture_power_generation_equipment",
        "company_id": "huaguang",
        "node_id": "power_generation_equipment",
        "activity_type": "manufacture",
        "role": "发电设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "huaguang_manufacture_environmental_equipment",
        "company_id": "huaguang",
        "node_id": "environmental_equipment",
        "activity_type": "manufacture",
        "role": "环保设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "huaguang_provide_service_energy_supply",
        "company_id": "huaguang",
        "node_id": "energy_supply",
        "activity_type": "provide_service",
        "role": "能源供应服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "st_xiangyou_provide_service_software",
        "company_id": "st_xiangyou",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_xiangyou_provide_service_system_integration",
        "company_id": "st_xiangyou",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_xiangyou_manufacture_postal_equipment",
        "company_id": "st_xiangyou",
        "node_id": "postal_equipment",
        "activity_type": "manufacture",
        "role": "邮政设备制造商",
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
            "evidence": make_evidence(f"tushare batch 075: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 075: " + e["description"]),
        })
    return {
        "batch_id": "batch_075",
        "task_description": "Batch 075: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 075: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_075",
        "task_description": "Batch 075: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 075 Submission")
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
