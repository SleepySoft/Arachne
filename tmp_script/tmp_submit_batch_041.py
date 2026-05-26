#!/usr/bin/env python3
"""Batch 041: 000977-000990"""
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
    "batch_id": "batch_041_graph",
    "task_description": "Batch 041 graph: CVT, DCT, hybrid power, electric drive, coking coal, petroleum resin.",
    "nodes_to_upsert": [
        {"node_id": "cvt_transmission", "canonical_name_zh": "无级变速器", "canonical_name_en": "CVT Transmission", "aliases": ["CVT", "无级变速箱"], "definition": "通过钢带和可变直径带轮实现无级变速的自动变速器，用于汽车传动系统。", "entity_type": "component", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "dct_transmission", "canonical_name_zh": "双离合变速器", "canonical_name_en": "DCT Transmission", "aliases": ["DCT", "双离合变速箱"], "definition": "采用两组离合器交替换挡的自动变速器，兼具手动变速器的效率和自动变速器的便利性。", "entity_type": "component", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "hybrid_power_system", "canonical_name_zh": "混合动力系统", "canonical_name_en": "Hybrid Power System", "aliases": ["混动系统"], "definition": "由内燃机和电动机组合驱动的车辆动力系统，可实现能量回收和多种驱动模式切换。", "entity_type": "subsystem", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "electric_drive_system", "canonical_name_zh": "电驱动系统", "canonical_name_en": "Electric Drive System", "aliases": ["电驱系统", "电动车驱动系统"], "definition": "以电动机为核心，配合减速器和电控单元构成的车辆动力驱动系统。", "entity_type": "subsystem", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "coking_coal", "canonical_name_zh": "焦煤", "canonical_name_en": "Coking Coal", "aliases": ["冶金煤"], "definition": "具有粘结性、可用于高炉炼焦的烟煤，是钢铁冶炼的关键原料。", "entity_type": "material", "evidence": [{"source_title": "山西焦煤主营业务", "quote": "主要产品为焦煤、肥煤、瘦煤、贫瘦煤等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "petroleum_resin", "canonical_name_zh": "石油树脂", "canonical_name_en": "Petroleum Resin", "aliases": ["碳五碳九树脂"], "definition": "以石油裂解副产物为原料合成的热塑性树脂，用于胶粘剂、涂料和橡胶助剂。", "entity_type": "material", "evidence": [{"source_title": "大庆华科主营业务", "quote": "主要产品:聚丙烯、石油树脂"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "donkey_hide_gelatin", "canonical_name_zh": "驴胶补血产品", "canonical_name_en": "Donkey-hide Gelatin Product", "aliases": ["阿胶制品", "驴胶颗粒"], "definition": "以驴皮为主要原料熬制加工而成的补血养颜中成药制品。", "entity_type": "material", "evidence": [{"source_title": "九芝堂主营业务", "quote": "主要产品:驴胶补血颗粒、斯奇康注射液"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "coking_coal_to_steel_plate", "from_node": "coking_coal", "to_node": "steel_plate", "edge_type": "material_flow", "description": "焦煤经高温干馏制成焦炭，焦炭是高炉炼钢的重要还原剂和热源。", "evidence": [{"source_title": "钢铁冶炼常识", "quote": "焦炭由焦煤炼制而成，是高炉炼铁的主要原料"}], "confidence": "HIGH"},
        {"edge_namespace": "industrial_flow", "edge_id": "cvt_to_automotive", "from_node": "cvt_transmission", "to_node": "automotive_part", "edge_type": "composition", "description": "无级变速器是汽车传动系统的核心组成部分。", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_041_business",
    "task_description": "Batch 041 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "inspur", "name_zh": "浪潮电子信息产业股份有限公司", "aliases": ["浪潮信息"], "stock_codes": ["000977.SZ"], "description": "服务器、微型计算机及软件系统企业", "country": "CN", "province": "山东", "city": "济南", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "guilin_tourism", "name_zh": "桂林旅游股份有限公司", "aliases": ["桂林旅游"], "stock_codes": ["000978.SZ"], "description": "漓江游船、景区、酒店、客运及高尔夫旅游服务企业", "country": "CN", "province": "广西", "city": "桂林", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "zhongtai_auto", "name_zh": "众泰汽车股份有限公司", "aliases": ["众泰汽车"], "stock_codes": ["000980.SZ"], "description": "汽车整车、摩托车发动机、模具及汽车配件企业", "country": "CN", "province": "浙江", "city": "金华", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "shanzi_hitech", "name_zh": "山子高科技股份有限公司", "aliases": ["山子高科"], "stock_codes": ["000981.SZ"], "description": "无级变速器、双离合变速器、混合动力及电驱动系统企业", "country": "CN", "province": "甘肃", "city": "兰州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "shanxi_coking", "name_zh": "山西焦煤能源集团股份有限公司", "aliases": ["山西焦煤"], "stock_codes": ["000983.SZ"], "description": "焦煤、肥煤、瘦煤、贫瘦煤等煤炭开采销售企业", "country": "CN", "province": "山西", "city": "太原", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "daqing_huake", "name_zh": "大庆华科股份有限公司", "aliases": ["大庆华科"], "stock_codes": ["000985.SZ"], "description": "精细化工产品、聚丙烯及石油树脂生产企业", "country": "CN", "province": "黑龙江", "city": "大庆", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "yuexiu_capital", "name_zh": "广州越秀资本控股集团股份有限公司", "aliases": ["越秀资本"], "stock_codes": ["000987.SZ"], "description": "证券、融资租赁、不良资产处置、私募股权投资及期货企业", "country": "CN", "province": "广东", "city": "广州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "huagong_tech", "name_zh": "华工科技产业股份有限公司", "aliases": ["华工科技"], "stock_codes": ["000988.SZ"], "description": "精密激光加工设备、食品安全溯源及全息防伪产品企业", "country": "CN", "province": "湖北", "city": "武汉", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "jiuzhitang", "name_zh": "九芝堂股份有限公司", "aliases": ["九芝堂"], "stock_codes": ["000989.SZ"], "description": "驴胶补血颗粒、斯奇康注射液等中成药生产企业", "country": "CN", "province": "湖南", "city": "长沙", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "chengzhi", "name_zh": "诚志股份有限公司", "aliases": ["诚志股份"], "stock_codes": ["000990.SZ"], "description": "生命科学、信息产品及精细化工企业", "country": "CN", "province": "江西", "city": "南昌", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "inspur_manufacture_server", "company_id": "inspur", "node_id": "server_hardware", "activity_type": "manufacture", "role": "服务器制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "浪潮信息主营业务", "quote": "主要产品:服务器、微型计算机、软件系统"}]},
        {"exposure_id": "guilin_operate_tourism", "company_id": "guilin_tourism", "node_id": "tourism_service", "activity_type": "operate", "role": "旅游服务运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "桂林旅游主营业务", "quote": "经营业务:漓江游船客运、景区游览、酒店服务、客运服务、高尔夫球场经营"}]},
        {"exposure_id": "zhongtai_manufacture_vehicle", "company_id": "zhongtai_auto", "node_id": "automotive_part", "activity_type": "manufacture", "role": "汽车整车及配件制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "众泰汽车主营业务", "quote": "主要业务:汽车整车、摩托车发动机、模具、汽车配件、汽车仪表"}]},
        {"exposure_id": "shanzi_manufacture_cvt", "company_id": "shanzi_hitech", "node_id": "cvt_transmission", "activity_type": "manufacture", "role": "无级变速器制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}]},
        {"exposure_id": "shanzi_manufacture_dct", "company_id": "shanzi_hitech", "node_id": "dct_transmission", "activity_type": "manufacture", "role": "双离合变速器制造商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}]},
        {"exposure_id": "shanzi_manufacture_hybrid", "company_id": "shanzi_hitech", "node_id": "hybrid_power_system", "activity_type": "manufacture", "role": "混合动力系统制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "山子高科主营业务", "quote": "主要产品:无级变速器(CVT)、双离合变速器(DCT)、混合动力系统、电驱动系统"}]},
        {"exposure_id": "shanxi_produce_coking_coal", "company_id": "shanxi_coking", "node_id": "coking_coal", "activity_type": "produce", "role": "焦煤生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "山西焦煤主营业务", "quote": "主要产品为焦煤、肥煤、瘦煤、贫瘦煤等"}]},
        {"exposure_id": "daqing_produce_petroleum_resin", "company_id": "daqing_huake", "node_id": "petroleum_resin", "activity_type": "produce", "role": "石油树脂生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "大庆华科主营业务", "quote": "主要产品:聚丙烯、石油树脂"}]},
        {"exposure_id": "daqing_produce_polypropylene", "company_id": "daqing_huake", "node_id": "polypropylene", "activity_type": "produce", "role": "聚丙烯生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "大庆华科主营业务", "quote": "主要产品:聚丙烯、石油树脂"}]},
        {"exposure_id": "jiuzhitang_produce_chinese_patent", "company_id": "jiuzhitang", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "九芝堂主营业务", "quote": "主要产品:驴胶补血颗粒、斯奇康注射液"}]},
        {"exposure_id": "jiuzhitang_produce_donkey_gelatin", "company_id": "jiuzhitang", "node_id": "donkey_hide_gelatin", "activity_type": "produce", "role": "驴胶补血产品生产商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "九芝堂主营业务", "quote": "主要产品:驴胶补血颗粒、斯奇康注射液"}]},
        {"exposure_id": "chengzhi_produce_chemical", "company_id": "chengzhi", "node_id": "chemical_product", "activity_type": "produce", "role": "精细化工产品生产商", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "诚志股份主营业务", "quote": "主要产品:生命科学、信息产品、精细化工"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 041 done!")
