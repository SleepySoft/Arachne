#!/usr/bin/env python3
"""Batch 040: 000963-000975"""
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
    "batch_id": "batch_040_graph",
    "task_description": "Batch 040 graph: ventilation fan, coalbed methane, non-crystalline alloy, magnetic material, tomato product.",
    "nodes_to_upsert": [
        {"node_id": "ventilation_fan", "canonical_name_zh": "风机", "canonical_name_en": "Ventilation Fan", "aliases": ["通风机", "鼓风机"], "definition": "用于输送气体、提供通风或增压的旋转机械设备，广泛应用于环保、建筑及工业领域。", "entity_type": "device", "evidence": [{"source_title": "盈峰环境主营业务", "quote": "主要产品:风机及配件、冷冻设备、电子元件、漆包线"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "coalbed_methane", "canonical_name_zh": "煤层气", "canonical_name_en": "Coalbed Methane", "aliases": ["煤矿瓦斯", "煤层甲烷"], "definition": "以吸附状态储存于煤层中的非常规天然气，主要成分为甲烷，可通过抽采利用。", "entity_type": "material", "evidence": [{"source_title": "蓝焰控股主营业务", "quote": "主要业务为煤矿瓦斯治理及煤层气勘查、开发与利用。主要产品为煤层气(煤矿瓦斯)"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "non_crystalline_alloy", "canonical_name_zh": "非晶合金", "canonical_name_en": "Amorphous Alloy", "aliases": ["金属玻璃", "非晶纳米晶带材"], "definition": "原子排列长程无序的金属材料，具有优异的软磁性能、耐腐蚀性和高强度。", "entity_type": "material", "evidence": [{"source_title": "安泰科技主营业务", "quote": "主要产品:非晶/纳米晶带材及制品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "magnetic_material", "canonical_name_zh": "磁性材料", "canonical_name_en": "Magnetic Material", "aliases": ["磁材", "永磁材料"], "definition": "具有铁磁性或亚铁磁性的功能材料，广泛用于电机、电子器件及新能源领域。", "entity_type": "material", "evidence": [{"source_title": "中科三环主营业务", "quote": "主要产品:磁材产品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "tomato_product", "canonical_name_zh": "番茄制品", "canonical_name_en": "Tomato Product", "aliases": ["番茄酱", "番茄汁"], "definition": "以番茄为原料加工制成的食品，包括番茄酱、番茄汁、番茄罐头等。", "entity_type": "material", "evidence": [{"source_title": "ST中基主营业务", "quote": "主要业务:番茄制品的加工、销售"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "ontology", "edge_id": "non_crystalline_is_a_magnetic", "from_node": "non_crystalline_alloy", "to_node": "magnetic_material", "edge_type": "is_a", "description": "非晶合金是一种具有优异软磁性能的磁性材料，属于alias/synonym关系中的is_a分类。", "evidence": [{"source_title": "材料分类", "quote": "非晶合金属于软磁材料的一种"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_040_business",
    "task_description": "Batch 040 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "huadong_pharma", "name_zh": "华东医药股份有限公司", "aliases": ["华东医药"], "stock_codes": ["000963.SZ"], "description": "百令胶囊等化学药品及医药产品生产企业", "country": "CN", "province": "浙江", "city": "杭州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "tianbao_infrastructure", "name_zh": "天津市房地产发展(集团)股份有限公司", "aliases": ["天保基建"], "stock_codes": ["000965.SZ"], "description": "房地产开发和销售企业", "country": "CN", "province": "天津", "city": "天津", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "changyuan_power", "name_zh": "国家能源集团长源电力股份有限公司", "aliases": ["长源电力"], "stock_codes": ["000966.SZ"], "description": "电力、热力生产和销售企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "yingfeng_env", "name_zh": "盈峰环境科技集团股份有限公司", "aliases": ["盈峰环境"], "stock_codes": ["000967.SZ"], "description": "风机及配件、冷冻设备、电子元件制造企业", "country": "CN", "province": "浙江", "city": "绍兴", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "lanyan", "name_zh": "山西蓝焰控股股份有限公司", "aliases": ["蓝焰控股"], "stock_codes": ["000968.SZ"], "description": "煤矿瓦斯治理及煤层气勘查、开发与利用企业", "country": "CN", "province": "山西", "city": "晋城", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "at_m", "name_zh": "安泰科技股份有限公司", "aliases": ["安泰科技"], "stock_codes": ["000969.SZ"], "description": "先进金属材料及制品（非晶/纳米晶带材等）研发生产企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "zhongke_sanhuan", "name_zh": "北京中科三环高技术股份有限公司", "aliases": ["中科三环"], "stock_codes": ["000970.SZ"], "description": "磁材产品（烧结钕铁硼、粘结钕铁硼等）研发生产企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_zhongji", "name_zh": "中基健康产业股份有限公司", "aliases": ["*ST中基", "中基健康"], "stock_codes": ["000972.SZ"], "description": "番茄制品加工和销售企业", "country": "CN", "province": "新疆", "city": "乌鲁木齐", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "fosu_tech", "name_zh": "佛山佛塑科技集团股份有限公司", "aliases": ["佛塑科技"], "stock_codes": ["000973.SZ"], "description": "渗析材料、电工材料、光学材料、阻隔材料等高分子功能薄膜企业", "country": "CN", "province": "广东", "city": "佛山", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "shanjin_intl", "name_zh": "山金国际黄金股份有限公司", "aliases": ["山金国际"], "stock_codes": ["000975.SZ"], "description": "有色金属矿采选及黄金生产企业", "country": "CN", "province": "内蒙古", "city": "赤峰", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "huadong_produce_chemical_drug", "company_id": "huadong_pharma", "node_id": "chemical_drug", "activity_type": "produce", "role": "化学药品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华东医药主营业务", "quote": "主要产品:百令胶囊、新赛斯平、泮立苏"}]},
        {"exposure_id": "tianbao_operate_real_estate", "company_id": "tianbao_infrastructure", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "天保基建主营业务", "quote": "主要业务:房地产开发和销售"}]},
        {"exposure_id": "changyuan_operate_coal_power", "company_id": "changyuan_power", "node_id": "coal_power_generation", "activity_type": "operate", "role": "火电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "长源电力主营业务", "quote": "主要业务:电力、热力生产和销售"}]},
        {"exposure_id": "yingfeng_manufacture_ventilation_fan", "company_id": "yingfeng_env", "node_id": "ventilation_fan", "activity_type": "manufacture", "role": "风机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "盈峰环境主营业务", "quote": "主要产品:风机及配件、冷冻设备、电子元件、漆包线"}]},
        {"exposure_id": "lanyan_produce_coalbed_methane", "company_id": "lanyan", "node_id": "coalbed_methane", "activity_type": "produce", "role": "煤层气开发商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "蓝焰控股主营业务", "quote": "主要产品为煤层气(煤矿瓦斯)"}]},
        {"exposure_id": "at_m_produce_non_crystalline", "company_id": "at_m", "node_id": "non_crystalline_alloy", "activity_type": "produce", "role": "非晶合金材料制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "安泰科技主营业务", "quote": "主要产品:非晶/纳米晶带材及制品"}]},
        {"exposure_id": "zhongke_produce_magnetic_material", "company_id": "zhongke_sanhuan", "node_id": "magnetic_material", "activity_type": "produce", "role": "磁性材料制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中科三环主营业务", "quote": "主要产品:磁材产品"}]},
        {"exposure_id": "zhongji_produce_tomato_product", "company_id": "st_zhongji", "node_id": "tomato_product", "activity_type": "produce", "role": "番茄制品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "ST中基主营业务", "quote": "主要业务:番茄制品的加工、销售"}]},
        {"exposure_id": "fosu_produce_plastic_film", "company_id": "fosu_tech", "node_id": "plastic_film", "activity_type": "produce", "role": "高分子功能薄膜制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "佛塑科技主营业务", "quote": "主要产品:渗析材料、电工材料、光学材料、阻隔材料、PET切片材料、PVC压延材料"}]},
        {"exposure_id": "shanjin_produce_gold", "company_id": "shanjin_intl", "node_id": "gold_metal", "activity_type": "produce", "role": "黄金生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "山金国际主营业务", "quote": "主营业务:有色金属矿采选"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 040 done!")
