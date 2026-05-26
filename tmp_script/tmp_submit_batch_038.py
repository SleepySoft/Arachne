#!/usr/bin/env python3
"""Batch 038: 000930-000949"""
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
    "batch_id": "batch_038_graph",
    "task_description": "Batch 038 graph: starch, fuel ethanol, MSG, citric acid, alumina, aluminum product.",
    "nodes_to_upsert": [
        {"node_id": "starch", "canonical_name_zh": "淀粉", "canonical_name_en": "Starch", "aliases": ["玉米淀粉", "食用淀粉"], "definition": "由葡萄糖分子聚合而成的多糖，是重要的食品原料和工业原料。", "entity_type": "material", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "fuel_ethanol", "canonical_name_zh": "燃料乙醇", "canonical_name_en": "Fuel Ethanol", "aliases": ["车用乙醇汽油"], "definition": "以生物质为原料生产的可作为汽油添加剂或替代品的乙醇燃料。", "entity_type": "material", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "monosodium_glutamate", "canonical_name_zh": "味精", "canonical_name_en": "Monosodium Glutamate", "aliases": ["谷氨酸钠", "味素"], "definition": "以粮食为原料经发酵提纯制成的鲜味调味品。", "entity_type": "material", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "citric_acid", "canonical_name_zh": "柠檬酸", "canonical_name_en": "Citric Acid", "aliases": ["枸橼酸"], "definition": "一种重要的有机酸，广泛用于食品、饮料、医药及化工行业。", "entity_type": "material", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "alumina", "canonical_name_zh": "氧化铝", "canonical_name_en": "Alumina", "aliases": ["铝氧", "刚玉"], "definition": "铝的氧化物，是电解铝生产的主要原料，也用于陶瓷、耐火材料等领域。", "entity_type": "material", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "aluminum_product", "canonical_name_zh": "铝产品", "canonical_name_en": "Aluminum Product", "aliases": ["铝材", "铝制品"], "definition": "以铝或铝合金为原料加工制成的板材、型材、箔材及铸件等产品。", "entity_type": "material", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "starch_to_fuel_ethanol", "from_node": "starch", "to_node": "fuel_ethanol", "edge_type": "material_flow", "description": "淀粉等生物质原料经发酵工艺可生产燃料乙醇。", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇"}], "confidence": "HIGH"},
        {"edge_namespace": "industrial_flow", "edge_id": "alumina_to_aluminum_product", "from_node": "alumina", "to_node": "aluminum_product", "edge_type": "material_flow", "description": "氧化铝通过电解等工艺加工成铝产品。", "evidence": [{"source_title": "神火股份主营业务", "quote": "氧化铝、铝产品的生产、加工和销售"}], "confidence": "HIGH"},
        {"edge_namespace": "industrial_flow", "edge_id": "coal_to_alumina", "from_node": "coal", "to_node": "alumina", "edge_type": "energy_flow", "description": "煤炭燃烧提供氧化铝冶炼所需的热能和电力。", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_038_business",
    "task_description": "Batch 038 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "cofco_tech", "name_zh": "中粮生物科技股份有限公司", "aliases": ["中粮科技"], "stock_codes": ["000930.SZ"], "description": "淀粉、淀粉糖、燃料乙醇、味精、柠檬酸等农产品深加工企业", "country": "CN", "province": "安徽", "city": "蚌埠", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "zhongguancun", "name_zh": "北京中关村科技发展(控股)股份有限公司", "aliases": ["中关村"], "stock_codes": ["000931.SZ"], "description": "信息化服务、生物医药、房地产开发及金融投资企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "valin_steel", "name_zh": "湖南华菱钢铁股份有限公司", "aliases": ["华菱钢铁"], "stock_codes": ["000932.SZ"], "description": "宽厚板、热轧卷板、冷轧卷板、线棒材、螺纹钢、无缝钢管等综合钢铁企业", "country": "CN", "province": "湖南", "city": "长沙", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "shenhuo", "name_zh": "河南神火煤电股份有限公司", "aliases": ["神火股份"], "stock_codes": ["000933.SZ"], "description": "煤炭、氧化铝及铝产品生产、加工和销售企业", "country": "CN", "province": "河南", "city": "商丘", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sichuan_shuangma", "name_zh": "四川双马水泥股份有限公司", "aliases": ["四川双马"], "stock_codes": ["000935.SZ"], "description": "水泥及电力生产销售企业", "country": "CN", "province": "四川", "city": "成都", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "huaxi_share", "name_zh": "江苏华西村股份有限公司", "aliases": ["华西股份"], "stock_codes": ["000936.SZ"], "description": "化工原料、化学纤维品制造及国内贸易企业", "country": "CN", "province": "江苏", "city": "江阴", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "jizhong_energy", "name_zh": "冀中能源股份有限公司", "aliases": ["冀中能源"], "stock_codes": ["000937.SZ"], "description": "煤炭、化工、建材及电力业务企业", "country": "CN", "province": "河北", "city": "邢台", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "unisplendour", "name_zh": "紫光股份有限公司", "aliases": ["紫光股份"], "stock_codes": ["000938.SZ"], "description": "信息产品、通讯产品、IT服务及增值分销企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "nantian_info", "name_zh": "云南南天电子信息产业股份有限公司", "aliases": ["南天信息"], "stock_codes": ["000948.SZ"], "description": "银行系统、金融终端及网络产品等软件开发与集成服务企业", "country": "CN", "province": "云南", "city": "昆明", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "xinxiang_chemical", "name_zh": "新乡化纤股份有限公司", "aliases": ["新乡化纤"], "stock_codes": ["000949.SZ"], "description": "粘胶长丝和粘胶短纤维生产与销售企业", "country": "CN", "province": "河南", "city": "新乡", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "cofco_produce_starch", "company_id": "cofco_tech", "node_id": "starch", "activity_type": "produce", "role": "淀粉生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇"}]},
        {"exposure_id": "cofco_produce_fuel_ethanol", "company_id": "cofco_tech", "node_id": "fuel_ethanol", "activity_type": "produce", "role": "燃料乙醇生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇"}]},
        {"exposure_id": "cofco_produce_msg", "company_id": "cofco_tech", "node_id": "monosodium_glutamate", "activity_type": "produce", "role": "味精生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}]},
        {"exposure_id": "cofco_produce_citric_acid", "company_id": "cofco_tech", "node_id": "citric_acid", "activity_type": "produce", "role": "柠檬酸生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中粮科技主营业务", "quote": "主要产品包括淀粉、淀粉糖、燃料乙醇、食用酒精、消毒及医用酒精、味精、柠檬酸、糊精"}]},
        {"exposure_id": "zhongguancun_produce_chemical_drug", "company_id": "zhongguancun", "node_id": "chemical_drug", "activity_type": "produce", "role": "生物医药企业", "weight": 0.7, "confidence": "MEDIUM", "evidence": [{"source_title": "中关村主营业务", "quote": "主要业务:信息化服务、生物医药、房地产开发、金融投资"}]},
        {"exposure_id": "valin_produce_steel_plate", "company_id": "valin_steel", "node_id": "steel_plate", "activity_type": "produce", "role": "钢板生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华菱钢铁主营业务", "quote": "主要产品:宽厚板、热轧卷板、冷轧卷板、线棒材、螺纹钢、无缝钢管等"}]},
        {"exposure_id": "shenhuo_produce_coal", "company_id": "shenhuo", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}]},
        {"exposure_id": "shenhuo_produce_alumina", "company_id": "shenhuo", "node_id": "alumina", "activity_type": "produce", "role": "氧化铝生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}]},
        {"exposure_id": "shenhuo_produce_aluminum_product", "company_id": "shenhuo", "node_id": "aluminum_product", "activity_type": "produce", "role": "铝产品生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "神火股份主营业务", "quote": "主要业务:煤炭、发电(基本为自发自用)、氧化铝、铝产品的生产、加工和销售"}]},
        {"exposure_id": "shuangma_produce_cement", "company_id": "sichuan_shuangma", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "四川双马主营业务", "quote": "主要产品:水泥、电力"}]},
        {"exposure_id": "huaxi_produce_viscose_fiber", "company_id": "huaxi_share", "node_id": "viscose_fiber", "activity_type": "produce", "role": "粘胶纤维生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "华西股份主营业务", "quote": "主营业务:危险化学品的销售、化工原料、化学纤维品的制造"}]},
        {"exposure_id": "jizhong_produce_coal", "company_id": "jizhong_energy", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "冀中能源主营业务", "quote": "主要业务:煤炭、化工、建材及电力等四项业务"}]},
        {"exposure_id": "unisplendour_manufacture_it_equipment", "company_id": "unisplendour", "node_id": "it_equipment", "activity_type": "manufacture", "role": "IT设备与通讯产品供应商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "紫光股份主营业务", "quote": "主营业务:信息产品、通讯产品、IT服务、医疗电子、增值分销、国际贸易"}]},
        {"exposure_id": "nantian_provide_software_service", "company_id": "nantian_info", "node_id": "software_service", "activity_type": "provide_service", "role": "金融信息化软件服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "南天信息主营业务", "quote": "主要产品:银行系统用的开放式系统小型机、金融终端系统、网络产品、专业存折打印机"}]},
        {"exposure_id": "xinxiang_produce_viscose_filament", "company_id": "xinxiang_chemical", "node_id": "viscose_filament", "activity_type": "produce", "role": "粘胶长丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "新乡化纤主营业务", "quote": "主要业务:粘胶长丝和粘胶短纤维的生产与销售"}]},
        {"exposure_id": "xinxiang_produce_viscose_staple", "company_id": "xinxiang_chemical", "node_id": "viscose_staple", "activity_type": "produce", "role": "粘胶短纤维生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "新乡化纤主营业务", "quote": "主要业务:粘胶长丝和粘胶短纤维的生产与销售"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 038 done!")
