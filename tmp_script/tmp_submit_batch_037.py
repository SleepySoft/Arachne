#!/usr/bin/env python3
"""Batch 037: 000919-000929"""
import json, urllib.request, urllib.error
API_BASE = "http://localhost:8005/api/v1"

def api_post(path, data):
    url = f"{API_BASE}{path}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code} on {path}: {e.read().decode()[:500]}")
        raise

graph_batch = {
    "batch_id": "batch_037_graph",
    "task_description": "Batch 037 graph: motor, RO membrane, steel cord, railway vehicle, malt.",
    "nodes_to_upsert": [
        {"node_id": "electric_motor", "canonical_name_zh": "电动机", "canonical_name_en": "Electric Motor", "aliases": ["电机", "驱动电机"], "definition": "将电能转换为机械能的旋转动力设备，广泛应用于工业、交通及家电领域。", "entity_type": "device", "evidence": [{"source_title": "佳电股份主营业务", "quote": "主要产品:继电器及继电保护装置类产品、控制保护屏产品、自动化及控制装置类产品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "composite_ro_membrane", "canonical_name_zh": "复合反渗透膜", "canonical_name_en": "Composite Reverse Osmosis Membrane", "aliases": ["RO膜", "反渗透膜"], "definition": "具有选择性分离功能的薄膜材料，用于水处理、海水淡化及工业纯水制备。", "entity_type": "material", "evidence": [{"source_title": "沃顿科技主营业务", "quote": "主要产品:铁路运输货车新造车、铁路车辆用弹簧、摇枕及侧架、棕纤维床垫、复合反渗透膜"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "steel_cord", "canonical_name_zh": "钢帘线", "canonical_name_en": "Steel Cord", "aliases": ["轮胎钢丝", "子午线轮胎钢帘线"], "definition": "由多根高强度钢丝捻制而成的线材，主要用于子午线轮胎的骨架材料。", "entity_type": "material", "evidence": [{"source_title": "福星股份主营业务", "quote": "主营业务:金属丝、绳及其制品的制造、销售和出口业务;商品房销售。主要产品:子午轮胎钢帘线、钢丝绳系列"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "railway_freight_car", "canonical_name_zh": "铁路货车", "canonical_name_en": "Railway Freight Car", "aliases": ["铁路车辆", "货运列车车厢"], "definition": "用于铁路运输的货运车辆，包括敞车、棚车、罐车及特种车辆。", "entity_type": "device", "evidence": [{"source_title": "沃顿科技主营业务", "quote": "主要产品:铁路运输货车新造车、铁路车辆用弹簧、摇枕及侧架"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "malt", "canonical_name_zh": "麦芽", "canonical_name_en": "Malt", "aliases": ["啤酒麦芽"], "definition": "经发芽、烘干处理的大麦，是啤酒酿造的核心原料。", "entity_type": "material", "evidence": [{"source_title": "兰州黄河主营业务", "quote": "主要产品:啤酒、麦芽、饮料"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "malt_to_beer", "from_node": "malt", "to_node": "beer", "edge_type": "material_flow", "description": "麦芽是酿造啤酒的核心原料，经过糖化和发酵制成啤酒。", "evidence": [{"source_title": "兰州黄河主营业务", "quote": "主要产品:啤酒、麦芽、饮料"}], "confidence": "HIGH"},
        {"edge_namespace": "industrial_flow", "edge_id": "steel_cord_to_tire", "from_node": "steel_cord", "to_node": "automotive_tire", "edge_type": "composition", "description": "钢帘线是子午线轮胎的骨架增强材料。", "evidence": [{"source_title": "福星股份主营业务", "quote": "主要产品:子午轮胎钢帘线、钢丝绳系列"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_037_business",
    "task_description": "Batch 037 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "jinling_pharm", "name_zh": "金陵药业股份有限公司", "aliases": ["金陵药业"], "stock_codes": ["000919.SZ"], "description": "脉络宁注射液等药品生产企业", "country": "CN", "province": "江苏", "city": "南京", "employee_count": 5716, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "wodun_tech", "name_zh": "沃顿科技股份有限公司", "aliases": ["沃顿科技"], "stock_codes": ["000920.SZ"], "description": "复合反渗透膜、棕纤维床垫及铁路车辆配件生产企业", "country": "CN", "province": "贵州", "city": "贵阳", "employee_count": 1508, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "hisense_appliance", "name_zh": "海信家电集团股份有限公司", "aliases": ["海信家电"], "stock_codes": ["000921.SZ"], "description": "冰箱、空调、冷柜等家电产品制造企业", "country": "CN", "province": "广东", "city": "佛山", "employee_count": 37759, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "jiadian_motor", "name_zh": "哈尔滨电气集团佳木斯电机股份有限公司", "aliases": ["佳电股份"], "stock_codes": ["000922.SZ"], "description": "电机、继电器及继电保护装置等电气设备制造企业", "country": "CN", "province": "黑龙江", "city": "佳木斯", "employee_count": 1952, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "hegang_resources", "name_zh": "河钢资源股份有限公司", "aliases": ["河钢资源"], "stock_codes": ["000923.SZ"], "description": "矿业开发、矿产品加工及工程机械配件生产销售企业", "country": "CN", "province": "河北", "city": "张家口", "employee_count": 4036, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "zhonghe_tech", "name_zh": "浙江众合科技股份有限公司", "aliases": ["众合科技"], "stock_codes": ["000925.SZ"], "description": "半导体节能材料、节能减排及轨道交通业务企业", "country": "CN", "province": "浙江", "city": "杭州", "employee_count": 1807, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "fuxing_share", "name_zh": "湖北福星科技股份有限公司", "aliases": ["福星股份"], "stock_codes": ["000926.SZ"], "description": "子午轮胎钢帘线、钢丝绳及房地产开发企业", "country": "CN", "province": "湖北", "city": "孝感", "employee_count": 2272, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "china_railway_materials", "name_zh": "中国铁路物资股份有限公司", "aliases": ["中国铁物"], "stock_codes": ["000927.SZ"], "description": "轨道交通物资供应链管理及轨道运维技术服务企业", "country": "CN", "province": "天津", "city": "天津", "employee_count": 4155, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sinosteel_intl", "name_zh": "中钢国际工程技术股份有限公司", "aliases": ["中钢国际"], "stock_codes": ["000928.SZ"], "description": "钢铁、电力、煤焦化工和矿山项目建设为主的工业工程服务企业", "country": "CN", "province": "吉林", "city": "吉林", "employee_count": 1833, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "st_lanhuang", "name_zh": "兰州黄河企业股份有限公司", "aliases": ["*ST兰黄", "兰州黄河"], "stock_codes": ["000929.SZ"], "description": "啤酒、麦芽及饮料生产企业", "country": "CN", "province": "甘肃", "city": "兰州", "employee_count": 809, "company_type": "public", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "jinling_produce_chemical_drug", "company_id": "jinling_pharm", "node_id": "chemical_drug", "activity_type": "produce", "role": "化学药品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "金陵药业主营业务", "quote": "主要产品:脉络宁注射液、速力菲"}]},
        {"exposure_id": "jinling_produce_pharma_product", "company_id": "jinling_pharm", "node_id": "pharmaceutical_product", "activity_type": "produce", "role": "医药产品制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "金陵药业主营业务", "quote": "主要产品:脉络宁注射液、速力菲"}]},
        {"exposure_id": "wodun_produce_ro_membrane", "company_id": "wodun_tech", "node_id": "composite_ro_membrane", "activity_type": "produce", "role": "复合反渗透膜生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "沃顿科技主营业务", "quote": "主要产品:复合反渗透膜"}]},
        {"exposure_id": "wodun_manufacture_railway_car", "company_id": "wodun_tech", "node_id": "railway_freight_car", "activity_type": "manufacture", "role": "铁路货车制造商", "weight": 0.7, "confidence": "MEDIUM", "evidence": [{"source_title": "沃顿科技主营业务", "quote": "主要产品:铁路运输货车新造车"}]},
        {"exposure_id": "hisense_manufacture_refrigerator", "company_id": "hisense_appliance", "node_id": "refrigerator", "activity_type": "manufacture", "role": "冰箱制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "海信家电主营业务", "quote": "主要产品:冰箱、空调、冷柜"}]},
        {"exposure_id": "hisense_manufacture_air_conditioner", "company_id": "hisense_appliance", "node_id": "air_conditioner", "activity_type": "manufacture", "role": "空调制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "海信家电主营业务", "quote": "主要产品:冰箱、空调、冷柜"}]},
        {"exposure_id": "jiadian_manufacture_electric_motor", "company_id": "jiadian_motor", "node_id": "electric_motor", "activity_type": "manufacture", "role": "电动机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "佳电股份主营业务", "quote": "主要产品:继电器及继电保护装置类产品、控制保护屏产品、自动化及控制装置类产品"}]},
        {"exposure_id": "hegang_produce_iron_ore", "company_id": "hegang_resources", "node_id": "iron_ore", "activity_type": "produce", "role": "铁矿石生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "河钢资源主营业务", "quote": "主营业务:矿业开发及矿产品加工、销售和工程机械产品及配件的生产、销售"}]},
        {"exposure_id": "zhonghe_manufacture_semiconductor", "company_id": "zhonghe_tech", "node_id": "semiconductor_device", "activity_type": "manufacture", "role": "半导体节能材料制造商", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "众合科技主营业务", "quote": "主要产品:半导体节能材料、节能减排和轨道交通业务"}]},
        {"exposure_id": "fuxing_produce_steel_cord", "company_id": "fuxing_share", "node_id": "steel_cord", "activity_type": "produce", "role": "钢帘线生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "福星股份主营业务", "quote": "主要产品:子午轮胎钢帘线、钢丝绳系列"}]},
        {"exposure_id": "china_railway_provide_logistics", "company_id": "china_railway_materials", "node_id": "logistics_service", "activity_type": "provide_service", "role": "轨道交通供应链服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中国铁物主营业务", "quote": "主营业务:为以面向轨道交通产业为主的物资供应链管理及轨道运维技术服务和工程建设物资生产制造及集成服务"}]},
        {"exposure_id": "sinosteel_provide_engineering", "company_id": "sinosteel_intl", "node_id": "engineering_construction_service", "activity_type": "provide_service", "role": "工业工程总承包服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中钢国际主营业务", "quote": "主要业务:以钢铁、电力、煤焦化工和矿山项目建设为主的工业工程和工业服务"}]},
        {"exposure_id": "lanhuang_produce_beer", "company_id": "st_lanhuang", "node_id": "beer", "activity_type": "produce", "role": "啤酒生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "兰州黄河主营业务", "quote": "主要产品:啤酒、麦芽、饮料"}]},
        {"exposure_id": "lanhuang_produce_malt", "company_id": "st_lanhuang", "node_id": "malt", "activity_type": "produce", "role": "麦芽生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "兰州黄河主营业务", "quote": "主要产品:啤酒、麦芽、饮料"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 037 done!")
