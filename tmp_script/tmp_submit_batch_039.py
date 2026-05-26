#!/usr/bin/env python3
"""Batch 039: 000950-000962"""
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
    "batch_id": "batch_039_graph",
    "task_description": "Batch 039 graph: riboflavin, non-woven fabric, tin ingot, titanium product, etc.",
    "nodes_to_upsert": [
        {"node_id": "riboflavin", "canonical_name_zh": "核黄素", "canonical_name_en": "Riboflavin", "aliases": ["维生素B2", "VB2"], "definition": "一种水溶性维生素，也是重要的饲料添加剂和医药原料药。", "entity_type": "material", "evidence": [{"source_title": "广济药业主营业务", "quote": "主要产品:核黄素"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "non_woven_fabric", "canonical_name_zh": "无纺布", "canonical_name_en": "Non-woven Fabric", "aliases": ["非织造布", "水刺无纺布"], "definition": "不经传统纺织工艺，由纤维直接通过物理或化学方法粘合而成的片状材料。", "entity_type": "material", "evidence": [{"source_title": "欣龙控股主营业务", "quote": "主要产品:水刺产品、无纺深加工制品、热轧及其衬布产品、贸易"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "tin_ingot", "canonical_name_zh": "锡锭", "canonical_name_en": "Tin Ingot", "aliases": ["精锡", "电解锡"], "definition": "以锡精矿为原料经冶炼提纯后铸成的金属锭，是锡加工的基础原料。", "entity_type": "material", "evidence": [{"source_title": "锡业股份主营业务", "quote": "主要产品:锡锭、阴极铜、锡铅焊料及无铅焊料、锡材、锡基合金、有机锡化工、无机锡化工"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "titanium_product", "canonical_name_zh": "钛产品", "canonical_name_en": "Titanium Product", "aliases": ["钛材", "钛合金制品"], "definition": "以钛或钛合金为原料加工制成的板材、棒材、丝材及制品。", "entity_type": "material", "evidence": [{"source_title": "东方钽业主营业务", "quote": "主要产品:钽金属及合金制品、铌金属及合金制品、铍合金材料、钛金属及合金材料、光伏"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "tin_metal_to_tin_ingot", "from_node": "tin_metal", "to_node": "tin_ingot", "edge_type": "material_flow", "description": "锡金属经冶炼提纯铸造成锡锭产品。", "evidence": [{"source_title": "锡业股份主营业务", "quote": "主要产品:锡锭、阴极铜、锡铅焊料及无铅焊料、锡材、锡基合金、有机锡化工、无机锡化工"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_039_business",
    "task_description": "Batch 039 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "chongqing_pharma", "name_zh": "重药控股股份有限公司", "aliases": ["重药控股"], "stock_codes": ["000950.SZ"], "description": "药品及医疗器械批发和零售企业", "country": "CN", "province": "重庆", "city": "重庆", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "cnhtc", "name_zh": "中国重汽集团济南卡车股份有限公司", "aliases": ["中国重汽"], "stock_codes": ["000951.SZ"], "description": "载重汽车、专用汽车、重型专用车底盘、客车底盘及汽车配件企业", "country": "CN", "province": "山东", "city": "济南", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "guangji_pharma", "name_zh": "湖北广济药业股份有限公司", "aliases": ["广济药业"], "stock_codes": ["000952.SZ"], "description": "核黄素等原料药生产企业", "country": "CN", "province": "湖北", "city": "武穴", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "hehua", "name_zh": "广西河池化工股份有限公司", "aliases": ["河化股份"], "stock_codes": ["000953.SZ"], "description": "尿素等化肥化工产品生产企业", "country": "CN", "province": "广西", "city": "河池", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "xinlong", "name_zh": "欣龙控股(集团)股份有限公司", "aliases": ["欣龙控股"], "stock_codes": ["000955.SZ"], "description": "水刺无纺布、无纺深加工制品及衬布产品企业", "country": "CN", "province": "海南", "city": "海口", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "zhongtong_bus", "name_zh": "中通客车股份有限公司", "aliases": ["中通客车"], "stock_codes": ["000957.SZ"], "description": "客车及零部件产品开发、制造和销售企业", "country": "CN", "province": "山东", "city": "聊城", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "spic_financial", "name_zh": "国家电投集团东方新能源股份有限公司", "aliases": ["电投产融", "东方能源"], "stock_codes": ["000958.SZ"], "description": "发电、供热及电力服务企业", "country": "CN", "province": "河北", "city": "石家庄", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "shougang_steel", "name_zh": "北京首钢股份有限公司", "aliases": ["首钢股份"], "stock_codes": ["000959.SZ"], "description": "钢材、钢坯及钢铁冶炼加工企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "ytc", "name_zh": "云南锡业股份有限公司", "aliases": ["锡业股份"], "stock_codes": ["000960.SZ"], "description": "锡锭、锡材、锡化工及阴极铜生产企业", "country": "CN", "province": "云南", "city": "昆明", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "orient_tantalum", "name_zh": "宁夏东方钽业股份有限公司", "aliases": ["东方钽业"], "stock_codes": ["000962.SZ"], "description": "钽、铌、铍、钛等稀有金属及合金制品生产企业", "country": "CN", "province": "宁夏", "city": "石嘴山", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "chongqing_provide_pharma_distribution", "company_id": "chongqing_pharma", "node_id": "pharmaceutical_distribution", "activity_type": "provide_service", "role": "医药流通服务商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "重药控股主营业务", "quote": "主要业务:药品、医疗器械的批发和零售业务"}]},
        {"exposure_id": "cnhtc_manufacture_truck", "company_id": "cnhtc", "node_id": "truck", "activity_type": "manufacture", "role": "载重汽车制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中国重汽主营业务", "quote": "主要业务:载重汽车、专用汽车、重型专用车底盘、客车底盘、汽车配件"}]},
        {"exposure_id": "cnhtc_manufacture_bus", "company_id": "cnhtc", "node_id": "bus", "activity_type": "manufacture", "role": "客车底盘制造商", "weight": 0.75, "confidence": "HIGH", "evidence": [{"source_title": "中国重汽主营业务", "quote": "主要业务:载重汽车、专用汽车、重型专用车底盘、客车底盘、汽车配件"}]},
        {"exposure_id": "guangji_produce_riboflavin", "company_id": "guangji_pharma", "node_id": "riboflavin", "activity_type": "produce", "role": "核黄素生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "广济药业主营业务", "quote": "主要产品:核黄素"}]},
        {"exposure_id": "hehua_produce_urea", "company_id": "hehua", "node_id": "urea", "activity_type": "produce", "role": "尿素生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "河化股份主营业务", "quote": "主要产品:尿素"}]},
        {"exposure_id": "xinlong_produce_non_woven", "company_id": "xinlong", "node_id": "non_woven_fabric", "activity_type": "produce", "role": "无纺布生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "欣龙控股主营业务", "quote": "主要产品:水刺产品、无纺深加工制品、热轧及其衬布产品、贸易"}]},
        {"exposure_id": "zhongtong_manufacture_bus", "company_id": "zhongtong_bus", "node_id": "bus", "activity_type": "manufacture", "role": "客车制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中通客车主营业务", "quote": "主要业务:以客车为主兼顾零部件产品的开发、制造和销售"}]},
        {"exposure_id": "spic_operate_coal_power", "company_id": "spic_financial", "node_id": "coal_power_generation", "activity_type": "operate", "role": "火电运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "电投产融主营业务", "quote": "主要产品:热力、电力。主要业务:发电、供热、电力服务等"}]},
        {"exposure_id": "shougang_produce_steel_plate", "company_id": "shougang_steel", "node_id": "steel_plate", "activity_type": "produce", "role": "钢材生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "首钢股份主营业务", "quote": "主要产品:钢材、钢坯。主要业务:钢铁冶炼、钢压延加工"}]},
        {"exposure_id": "ytc_produce_tin_ingot", "company_id": "ytc", "node_id": "tin_ingot", "activity_type": "produce", "role": "锡锭生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "锡业股份主营业务", "quote": "主要产品:锡锭、阴极铜、锡铅焊料及无铅焊料、锡材、锡基合金、有机锡化工、无机锡化工"}]},
        {"exposure_id": "orient_produce_tantalum", "company_id": "orient_tantalum", "node_id": "tantalum", "activity_type": "produce", "role": "钽金属制品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东方钽业主营业务", "quote": "主要产品:钽金属及合金制品、铌金属及合金制品、铍合金材料、钛金属及合金材料"}]},
        {"exposure_id": "orient_produce_titanium_product", "company_id": "orient_tantalum", "node_id": "titanium_product", "activity_type": "produce", "role": "钛产品生产商", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "东方钽业主营业务", "quote": "主要产品:钽金属及合金制品、铌金属及合金制品、铍合金材料、钛金属及合金材料"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 039 done!")
