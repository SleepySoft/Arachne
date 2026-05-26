#!/usr/bin/env python3
"""Batch 049: 600101-600111"""
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
    "batch_id": "batch_049_graph",
    "task_description": "Batch 049 graph: paper product, automobile part, western suit, rare earth functional material.",
    "nodes_to_upsert": [
        {"node_id": "paper_product", "canonical_name_zh": "纸制品", "canonical_name_en": "Paper Product", "aliases": ["纸张", "纸板", "纸浆"], "definition": "以植物纤维为原料，经制浆、造纸及后加工制成的各类纸张、纸板和纸浆产品。", "entity_type": "material", "evidence": [{"source_title": "青山纸业主营业务", "quote": "主要产品:纸、卡、浆及副产品、碱、电产品、医药产品、营林业、商业贸易、光电子"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "automobile_part", "canonical_name_zh": "汽车零部件", "canonical_name_en": "Automobile Part", "aliases": ["汽车配件", "汽车零件"], "definition": "构成汽车整车的各类零部件，包括动力总成、底盘系统、内外饰及电子电器等。", "entity_type": "component", "evidence": [{"source_title": "上汽集团主营业务", "quote": "主营业务:整车(含乘用车、商用车)的研发、生产和销售,零部件的研发、生产、销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "western_suit", "canonical_name_zh": "西服", "canonical_name_en": "Western Suit", "aliases": ["西装", "高级定制西服"], "definition": "以西式裁剪工艺制作的男士或女士套装，包括上衣和裤子/裙子，常用于商务及正式场合。", "entity_type": "component", "evidence": [{"source_title": "美尔雅主营业务", "quote": "主要产品:美尔雅高级西服、晚礼服及职业装"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "rare_earth_functional_material", "canonical_name_zh": "稀土功能材料", "canonical_name_en": "Rare Earth Functional Material", "aliases": ["稀土磁性材料", "稀土抛光材料"], "definition": "以稀土元素为主要成分，具有特殊磁、光、电、催化等功能的高性能材料。", "entity_type": "material", "evidence": [{"source_title": "北方稀土主营业务", "quote": "主要生产经营稀土原料产品、稀土功能材料产品(稀土磁性材料、抛光材料、贮氢材料、发光材料、催化材料)"}], "confidence": "HIGH", "status": "ACTIVE"},
    ],
    "edges_to_upsert": [
        {"edge_namespace": "industrial_flow", "edge_id": "rare_earth_to_functional", "from_node": "rare_earth_metal", "to_node": "rare_earth_functional_material", "edge_type": "material_flow", "description": "稀土金属经过加工制备成稀土功能材料。", "evidence": [{"source_title": "北方稀土主营业务", "quote": "主要生产经营稀土原料产品、稀土功能材料产品"}], "confidence": "HIGH"},
    ],
    "rejected_or_pending": [],
}

print("[1/2] Graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

business_batch = {
    "batch_id": "batch_049_business",
    "task_description": "Batch 049 companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {"company_id": "mingxing_power", "name_zh": "四川明星电力股份有限公司", "aliases": ["明星电力"], "stock_codes": ["600101.SH"], "description": "水力发电、电力销售及自来水生产销售企业", "country": "CN", "province": "四川", "city": "遂宁", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "qingshan_paper", "name_zh": "福建省青山纸业股份有限公司", "aliases": ["青山纸业"], "stock_codes": ["600103.SH"], "description": "纸、卡、浆及副产品生产企业", "country": "CN", "province": "福建", "city": "三明", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "saic", "name_zh": "上海汽车集团股份有限公司", "aliases": ["上汽集团"], "stock_codes": ["600104.SH"], "description": "乘用车、商用车及汽车零部件研发、生产和销售企业", "country": "CN", "province": "上海", "city": "上海", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
        {"company_id": "yongding", "name_zh": "永鼎股份有限公司", "aliases": ["永鼎股份"], "stock_codes": ["600105.SH"], "description": "光缆、电缆、电力电缆及开关等通信设备企业", "country": "CN", "province": "江苏", "city": "苏州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "chongqing_bridge", "name_zh": "重庆路桥股份有限公司", "aliases": ["重庆路桥"], "stock_codes": ["600106.SH"], "description": "路桥收费及工程建设企业", "country": "CN", "province": "重庆", "city": "重庆", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "st_meierya", "name_zh": "湖北美尔雅股份有限公司", "aliases": ["*ST尔雅"], "stock_codes": ["600107.SH"], "description": "高级西服、晚礼服及职业装生产企业", "country": "CN", "province": "湖北", "city": "黄石", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "yasheng", "name_zh": "甘肃亚盛实业(集团)股份有限公司", "aliases": ["亚盛集团"], "stock_codes": ["600108.SH"], "description": "农业种植、印染及贸易综合企业", "country": "CN", "province": "甘肃", "city": "兰州", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sinolink", "name_zh": "国金证券股份有限公司", "aliases": ["国金证券"], "stock_codes": ["600109.SH"], "description": "证券经纪、投资银行、证券投资及资产管理企业", "country": "CN", "province": "四川", "city": "成都", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "nuode", "name_zh": "诺德新材料股份有限公司", "aliases": ["诺德股份"], "stock_codes": ["600110.SH"], "description": "高档电解铜箔及动力电池材料企业", "country": "CN", "province": "吉林", "city": "长春", "employee_count": 0, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "china_northern_rare_earth", "name_zh": "中国北方稀土(集团)高科技股份有限公司", "aliases": ["北方稀土"], "stock_codes": ["600111.SH"], "description": "稀土原料、功能材料及应用产品企业", "country": "CN", "province": "内蒙古", "city": "包头", "employee_count": 0, "company_type": "state_owned", "status": "ACTIVE"},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "mingxing_operate_hydro", "company_id": "mingxing_power", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "明星电力主营业务", "quote": "主要业务:水力发电、电力销售和自来水生产、销售"}]},
        {"exposure_id": "qingshan_produce_paper", "company_id": "qingshan_paper", "node_id": "paper_product", "activity_type": "produce", "role": "纸制品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "青山纸业主营业务", "quote": "主要产品:纸、卡、浆及副产品"}]},
        {"exposure_id": "saic_manufacture_passenger_car", "company_id": "saic", "node_id": "passenger_car", "activity_type": "manufacture", "role": "乘用车制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "上汽集团主营业务", "quote": "主营业务:整车(含乘用车、商用车)的研发、生产和销售"}]},
        {"exposure_id": "saic_manufacture_auto_part", "company_id": "saic", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车零部件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "上汽集团主营业务", "quote": "零部件(含动力驱动系统、底盘系统、内外饰系统)的研发、生产、销售"}]},
        {"exposure_id": "yongding_manufacture_optical_cable", "company_id": "yongding", "node_id": "optical_fiber_cable", "activity_type": "manufacture", "role": "光缆电缆制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "永鼎股份主营业务", "quote": "主要产品:光缆、电缆、电力电缆、开关"}]},
        {"exposure_id": "chongqing_operate_highway", "company_id": "chongqing_bridge", "node_id": "highway_operation_service", "activity_type": "operate", "role": "路桥收费运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "重庆路桥主营业务", "quote": "主要业务:路桥收费、工程建设"}]},
        {"exposure_id": "meierya_manufacture_suit", "company_id": "st_meierya", "node_id": "western_suit", "activity_type": "manufacture", "role": "西服制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "美尔雅主营业务", "quote": "主要产品:美尔雅高级西服、晚礼服及职业装"}]},
        {"exposure_id": "yasheng_operate_agriculture", "company_id": "yasheng", "node_id": "agricultural_product", "activity_type": "produce", "role": "农业种植及贸易企业", "weight": 0.75, "confidence": "MEDIUM", "evidence": [{"source_title": "亚盛集团主营业务", "quote": "主要产品:印染、农业、贸易、化工等"}]},
        {"exposure_id": "sinolink_provide_securities", "company_id": "sinolink", "node_id": "securities_service", "activity_type": "provide_service", "role": "综合证券服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国金证券主营业务", "quote": "主营业务:证券经纪业务、投资银行业务、证券投资业务、资产管理业务"}]},
        {"exposure_id": "nuode_produce_copper_foil", "company_id": "nuode", "node_id": "copper_foil", "activity_type": "produce", "role": "电解铜箔生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "诺德股份主营业务", "quote": "主要产品:高档电解铜箔产品、动力电池材料等"}]},
        {"exposure_id": "northern_rare_earth_produce_functional", "company_id": "china_northern_rare_earth", "node_id": "rare_earth_functional_material", "activity_type": "produce", "role": "稀土功能材料生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "北方稀土主营业务", "quote": "主要生产经营稀土原料产品、稀土功能材料产品"}]},
    ],
}

print("[2/2] Business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")
print("Batch 049 done!")
