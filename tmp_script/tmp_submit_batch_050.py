#!/usr/bin/env python3
"""Batch 050: 600113-600123"""
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
    "batch_id": "batch_050_graph",
    "task_description": "Batch 050 graph: powder metallurgy part, satellite.",
    "nodes_to_upsert": [
        {"node_id": "powder_metallurgy_part", "canonical_name_zh": "粉末冶金零件", "canonical_name_en": "Powder Metallurgy Part", "aliases": ["粉末冶金件", "金属粉末成型件"], "definition": "以金属粉末为原料，经压制成型和烧结工艺制成的精密机械零件。", "entity_type": "component", "evidence": [{"source_title": "东睦股份主营业务", "quote": "摩托车、空调压缩机、冰箱压缩机、电动工具和轿车粉末冶金零件"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "satellite", "canonical_name_zh": "卫星", "canonical_name_en": "Satellite", "aliases": ["人造卫星", "小卫星"], "definition": "围绕地球或其他天体运行的航天器，用于通信、导航、遥感及科学研究。", "entity_type": "device", "evidence": [{"source_title": "中国卫星主营业务", "quote": "主要产品:小卫星制造、微小卫星制造、部组件制造、卫星应用系统集成与产品制造"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_050_business",
    "task_description": "Batch 050 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "zhejiang_dongri", "name_zh": "浙江东日股份有限公司", "aliases": ["浙江东日"], "stock_codes": ["600113.SH"], "description": "市场租赁、教育设施租赁及房地产企业", "country": "CN", "province": "浙江", "city": "温州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "dongmu", "name_zh": "东睦新材料集团股份有限公司", "aliases": ["东睦股份"], "stock_codes": ["600114.SH"], "description": "粉末冶金零件及机械基件企业", "country": "CN", "province": "浙江", "city": "宁波", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "china_eastern", "name_zh": "中国东方航空股份有限公司", "aliases": ["中国东航"], "stock_codes": ["600115.SH"], "description": "国内及国际航空客货邮行李运输企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "sanxia_water", "name_zh": "重庆三峡水利电力(集团)股份有限公司", "aliases": ["三峡水利"], "stock_codes": ["600116.SH"], "description": "发电及供电企业", "country": "CN", "province": "重庆", "city": "重庆", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "xining_special_steel", "name_zh": "西宁特殊钢股份有限公司", "aliases": ["西宁特钢"], "stock_codes": ["600117.SH"], "description": "碳结钢、碳工钢、合结钢、合工钢、轴承钢、模具钢、不锈钢、弹簧钢等特钢企业", "country": "CN", "province": "青海", "city": "西宁", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "china_satellite", "name_zh": "中国东方红卫星股份有限公司", "aliases": ["中国卫星"], "stock_codes": ["600118.SH"], "description": "小卫星制造、卫星应用及智慧城市企业", "country": "CN", "province": "北京", "city": "北京", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "st_changtou", "name_zh": "长发集团长江投资实业股份有限公司", "aliases": ["*ST长投"], "stock_codes": ["600119.SH"], "description": "房地产开发、商贸经营及宾馆餐饮企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "zhejiang_east", "name_zh": "浙江东方金融控股集团股份有限公司", "aliases": ["浙江东方"], "stock_codes": ["600120.SH"], "description": "商品流通、服装加工、房地产销售及货物运输代理企业", "country": "CN", "province": "浙江", "city": "杭州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "zzcoal", "name_zh": "郑州煤电股份有限公司", "aliases": ["郑州煤电"], "stock_codes": ["600121.SH"], "description": "煤炭开采及电力企业", "country": "CN", "province": "河南", "city": "郑州", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "lanhua", "name_zh": "山西兰花科技创业股份有限公司", "aliases": ["兰花科创"], "stock_codes": ["600123.SH"], "description": "煤炭开采及化肥生产企业", "country": "CN", "province": "山西", "city": "晋城", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "dongri_operate_real_estate", "company_id": "zhejiang_dongri", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产及设施租赁运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "浙江东日主营业务", "quote": "主营业务:市场租赁业务、教育设施租赁及后勤服务、房地产"}]},
        {"exposure_id": "dongmu_manufacture_powder", "company_id": "dongmu", "node_id": "powder_metallurgy_part", "activity_type": "manufacture", "role": "粉末冶金零件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东睦股份主营业务", "quote": "摩托车、空调压缩机、冰箱压缩机、电动工具和轿车粉末冶金零件"}]},
        {"exposure_id": "eastern_operate_airline", "company_id": "china_eastern", "node_id": "air_transport_service", "activity_type": "operate", "role": "航空运输运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中国东航主营业务", "quote": "主要业务:国内和经批准的国际、地区航空客、货、邮、行李运输业务及延伸服务"}]},
        {"exposure_id": "sanxia_operate_hydro", "company_id": "sanxia_water", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水电发供电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "三峡水利主营业务", "quote": "主要业务:发电、供电"}]},
        {"exposure_id": "xining_produce_special_steel", "company_id": "xining_special_steel", "node_id": "special_steel", "activity_type": "produce", "role": "特钢综合生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "西宁特钢主营业务", "quote": "主要产品:碳结钢、碳工钢、合结钢、合工钢、轴承钢、模具钢、不锈钢、弹簧钢"}]},
        {"exposure_id": "china_sat_manufacture_satellite", "company_id": "china_satellite", "node_id": "satellite", "activity_type": "manufacture", "role": "小卫星制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "中国卫星主营业务", "quote": "主要产品:小卫星制造、微小卫星制造、部组件制造、卫星应用系统集成与产品制造"}]},
        {"exposure_id": "changtou_operate_logistics", "company_id": "st_changtou", "node_id": "logistics_service", "activity_type": "provide_service", "role": "商贸及物流服务商", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "长投主营业务", "quote": "主要业务:房地产开发经营、商贸经营、宾馆餐饮、劳务服务"}]},
        {"exposure_id": "zhejiang_east_provide_trade", "company_id": "zhejiang_east", "node_id": "logistics_service", "activity_type": "provide_service", "role": "商品流通及货运代理服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "浙江东方主营业务", "quote": "主要业务:商品流通、服装加工业务、房地产销售、货物运输代理及其他"}]},
        {"exposure_id": "zzcoal_produce_coal", "company_id": "zzcoal", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "郑州煤电主营业务", "quote": "主要产品:煤炭、电力"}]},
        {"exposure_id": "lanhua_produce_coal", "company_id": "lanhua", "node_id": "coal", "activity_type": "produce", "role": "煤炭及化肥生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "兰花科创主营业务", "quote": "主要产品:煤炭、化肥"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 050 done!")
