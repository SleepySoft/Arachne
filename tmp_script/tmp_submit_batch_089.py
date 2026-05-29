#!/usr/bin/env python3
"""Submit batch 089 to Arachne API."""
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
        "node_id": "advertising",
        "canonical_name_zh": "广告",
        "definition": "通过媒体向公众传播商品、服务或观念信息以促进销售的商业宣传活动",
        "entity_type": "service"
    },
    {
        "node_id": "tunnel_bridge_facility",
        "canonical_name_zh": "隧桥设施",
        "definition": "城市隧道、桥梁及其附属设施，是城市交通基础设施的重要组成部分",
        "entity_type": "infrastructure"
    },
    {
        "node_id": "fluoropolymer",
        "canonical_name_zh": "含氟聚合物",
        "definition": "分子结构中含有氟原子的合成高分子材料，具有优异的耐化学腐蚀性和耐高温性",
        "entity_type": "material"
    },
    {
        "node_id": "cfc_substitute",
        "canonical_name_zh": "CFC替代品",
        "definition": "替代氯氟烃(CFC)的环保型制冷剂，对臭氧层破坏较小或为零",
        "entity_type": "material"
    },
    {
        "node_id": "audio_visual",
        "canonical_name_zh": "网络视听",
        "definition": "通过互联网传播的音频和视频内容服务，包括网络剧、网络电影、短视频等",
        "entity_type": "service"
    },
    {
        "node_id": "online_game",
        "canonical_name_zh": "网络游戏",
        "definition": "通过互联网进行多人互动的电子游戏，包括端游、手游、页游等形式",
        "entity_type": "service"
    },
    {
        "node_id": "golf",
        "canonical_name_zh": "高尔夫",
        "definition": "以球场为基础，提供高尔夫球运动、休闲和配套服务的体育产业",
        "entity_type": "service"
    },
    {
        "node_id": "cultural_supplies",
        "canonical_name_zh": "文化用品",
        "definition": "用于文化创作、学习教育和艺术活动的工具和材料，包括文具、绘画用品等",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "tunnel_bridge_facility_to_transportation",
        "from_node": "tunnel_bridge_facility",
        "to_node": "transportation",
        "edge_type": "capability_supply",
        "description": "隧桥设施为城市交通提供跨越障碍的通行能力"
    },
    {
        "edge_id": "fluoropolymer_to_chemical_industry",
        "from_node": "fluoropolymer",
        "to_node": "chemical_industry",
        "edge_type": "material_flow",
        "description": "含氟聚合物是化工新材料领域的重要产品"
    },
    {
        "edge_id": "online_game_to_internet",
        "from_node": "online_game",
        "to_node": "internet",
        "edge_type": "service_flow",
        "description": "网络游戏是互联网娱乐服务的重要业态"
    }
]

COMPANIES = [
    {
        "company_id": "zheshu",
        "name_zh": "浙报数字文化集团股份有限公司",
        "stock_code": "600633.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "互联网",
        "main_business": "广告,实业投资,新媒体技术开发,工艺美术品,文化用品,办公用品的销售"
    },
    {
        "company_id": "dazhong_public",
        "name_zh": "上海大众公用事业(集团)股份有限公司",
        "stock_code": "600635.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "供气供热",
        "main_business": "城市燃气,城市交通,隧桥设施,污水处理等"
    },
    {
        "company_id": "st_guohua",
        "name_zh": "国新文化控股股份有限公司",
        "stock_code": "600636.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "文教休闲",
        "main_business": "含氟聚合物,CFC替代品,氟致冷剂,清洗剂,发泡剂"
    },
    {
        "company_id": "oriental_pearl",
        "name_zh": "东方明珠新媒体股份有限公司",
        "stock_code": "600637.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "影视音像",
        "main_business": "网络视听,互联网,游戏等新兴业务"
    },
    {
        "company_id": "xinhuangpu",
        "name_zh": "上海新黄浦实业集团股份有限公司",
        "stock_code": "600638.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "区域地产",
        "main_business": "房地产业,工业"
    },
    {
        "company_id": "pudong_jinqiao",
        "name_zh": "上海浦东金桥出口加工区开发股份有限公司",
        "stock_code": "600639.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "园区开发",
        "main_business": "房地产销售,房地产租赁"
    },
    {
        "company_id": "guomai_culture",
        "name_zh": "新国脉数字文化股份有限公司",
        "stock_code": "600640.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "影视音像",
        "main_business": "旅游预订及酒店经营和输出管理"
    },
    {
        "company_id": "xiandao",
        "name_zh": "上海万业企业股份有限公司",
        "stock_code": "600641.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "半导体",
        "main_business": "商品房,酒店,旅游,高尔夫"
    },
    {
        "company_id": "shenergy",
        "name_zh": "申能股份有限公司",
        "stock_code": "600642.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "火力发电",
        "main_business": "电力行业,石油天然气行业"
    },
    {
        "company_id": "aijian",
        "name_zh": "上海爱建集团股份有限公司",
        "stock_code": "600643.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "多元金融",
        "main_business": "工业,商业,旅游饮食服务业"
    }
]

EXPOSURES = [
    {
        "exposure_id": "zheshu_provide_service_advertising",
        "company_id": "zheshu",
        "node_id": "advertising",
        "activity_type": "provide_service",
        "role": "广告服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "zheshu_provide_service_new_media_technology",
        "company_id": "zheshu",
        "node_id": "new_media_technology",
        "activity_type": "provide_service",
        "role": "新媒体技术服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "zheshu_produce_cultural_supplies",
        "company_id": "zheshu",
        "node_id": "cultural_supplies",
        "activity_type": "produce",
        "role": "文化用品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "dazhong_public_operate_city_gas",
        "company_id": "dazhong_public",
        "node_id": "city_gas",
        "activity_type": "operate",
        "role": "城市燃气运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "dazhong_public_operate_tunnel_bridge_facility",
        "company_id": "dazhong_public",
        "node_id": "tunnel_bridge_facility",
        "activity_type": "operate",
        "role": "隧桥设施运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "dazhong_public_operate_sewage_treatment",
        "company_id": "dazhong_public",
        "node_id": "sewage_treatment",
        "activity_type": "operate",
        "role": "污水处理运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_guohua_produce_fluoropolymer",
        "company_id": "st_guohua",
        "node_id": "fluoropolymer",
        "activity_type": "produce",
        "role": "含氟聚合物生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_guohua_produce_cfc_substitute",
        "company_id": "st_guohua",
        "node_id": "cfc_substitute",
        "activity_type": "produce",
        "role": "CFC替代品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_guohua_produce_fluorine_refrigerant",
        "company_id": "st_guohua",
        "node_id": "fluorine_refrigerant",
        "activity_type": "produce",
        "role": "氟致冷剂生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "oriental_pearl_provide_service_audio_visual",
        "company_id": "oriental_pearl",
        "node_id": "audio_visual",
        "activity_type": "provide_service",
        "role": "网络视听服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "oriental_pearl_provide_service_online_game",
        "company_id": "oriental_pearl",
        "node_id": "online_game",
        "activity_type": "provide_service",
        "role": "网络游戏服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "oriental_pearl_provide_service_internet",
        "company_id": "oriental_pearl",
        "node_id": "internet",
        "activity_type": "provide_service",
        "role": "互联网服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "xinhuangpu_operate_real_estate_development",
        "company_id": "xinhuangpu",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产开发运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "xinhuangpu_operate_industrial",
        "company_id": "xinhuangpu",
        "node_id": "industrial",
        "activity_type": "operate",
        "role": "工业运营商",
        "weight": 0.8
    },
    {
        "exposure_id": "pudong_jinqiao_operate_real_estate_development",
        "company_id": "pudong_jinqiao",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "房地产销售运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "pudong_jinqiao_operate_real_estate_leasing",
        "company_id": "pudong_jinqiao",
        "node_id": "real_estate_leasing",
        "activity_type": "operate",
        "role": "房地产租赁运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "guomai_culture_provide_service_tourism_service",
        "company_id": "guomai_culture",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "role": "旅游预订服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "guomai_culture_operate_hotel_service",
        "company_id": "guomai_culture",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店经营商",
        "weight": 0.9
    },
    {
        "exposure_id": "xiandao_operate_real_estate_development",
        "company_id": "xiandao",
        "node_id": "real_estate_development",
        "activity_type": "operate",
        "role": "商品房开发商",
        "weight": 0.95
    },
    {
        "exposure_id": "xiandao_operate_hotel_service",
        "company_id": "xiandao",
        "node_id": "hotel_service",
        "activity_type": "operate",
        "role": "酒店运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "xiandao_operate_golf",
        "company_id": "xiandao",
        "node_id": "golf",
        "activity_type": "operate",
        "role": "高尔夫运营商",
        "weight": 0.8
    },
    {
        "exposure_id": "shenergy_operate_power_generation",
        "company_id": "shenergy",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "电力运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "shenergy_operate_oil_gas",
        "company_id": "shenergy",
        "node_id": "oil_gas",
        "activity_type": "operate",
        "role": "石油天然气运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "aijian_operate_industrial",
        "company_id": "aijian",
        "node_id": "industrial",
        "activity_type": "operate",
        "role": "工业运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "aijian_operate_commercial",
        "company_id": "aijian",
        "node_id": "commercial",
        "activity_type": "operate",
        "role": "商业运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "aijian_provide_service_tourism_service",
        "company_id": "aijian",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "role": "旅游饮食服务商",
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
            "evidence": make_evidence(f"tushare batch 089: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 089: " + e["description"]),
        })
    return {
        "batch_id": "batch_089",
        "task_description": "Batch 089: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 089: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_089",
        "task_description": "Batch 089: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 089 Submission")
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
