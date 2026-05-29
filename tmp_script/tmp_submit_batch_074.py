#!/usr/bin/env python3
"""Submit batch 074 to Arachne API."""
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
        "node_id": "aquatic_feed",
        "canonical_name_zh": "水产饲料",
        "definition": "用于水产养殖的专用饲料，包括鱼饲料、虾饲料、蟹饲料等",
        "entity_type": "material"
    },
    {
        "node_id": "polysilicon",
        "canonical_name_zh": "多晶硅",
        "definition": "纯度较高的硅材料，是制造太阳能电池和半导体器件的基础原料",
        "entity_type": "material"
    },
    {
        "node_id": "solar_cell",
        "canonical_name_zh": "太阳能电池",
        "definition": "将太阳能直接转换为电能的半导体器件，是光伏发电的核心组件",
        "entity_type": "component"
    },
    {
        "node_id": "wig",
        "canonical_name_zh": "假发饰品",
        "definition": "用人发或合成纤维制成的头发饰品，用于装饰或弥补脱发",
        "entity_type": "material"
    },
    {
        "node_id": "upvc_pipe",
        "canonical_name_zh": "UPVC双壁波纹管",
        "definition": "以硬质聚氯乙烯为原料制成的具有波纹结构的双壁塑料管道，用于排水和排污",
        "entity_type": "component"
    },
    {
        "node_id": "titanium_alloy",
        "canonical_name_zh": "钛合金",
        "definition": "以钛为基础加入其他元素组成的合金，具有高强度、耐腐蚀和耐高温特性",
        "entity_type": "material"
    },
    {
        "node_id": "polymer_damping_element",
        "canonical_name_zh": "高分子减振降噪弹性元件",
        "definition": "利用高分子材料的粘弹性特性实现减振降噪功能的弹性元件",
        "entity_type": "component"
    }
]

NEW_EDGES = [
    {
        "edge_id": "polysilicon_to_solar_cell",
        "from_node": "polysilicon",
        "to_node": "solar_cell",
        "edge_type": "material_flow",
        "description": "多晶硅是制造太阳能电池的核心原材料"
    },
    {
        "edge_id": "titanium_alloy_to_aircraft",
        "from_node": "titanium_alloy",
        "to_node": "aircraft",
        "edge_type": "material_flow",
        "description": "钛合金因其高强度和耐腐蚀性广泛用于航空航天器制造"
    },
    {
        "edge_id": "upvc_pipe_to_construction",
        "from_node": "upvc_pipe",
        "to_node": "construction",
        "edge_type": "material_flow",
        "description": "UPVC双壁波纹管是市政工程和建筑排水系统的重要管材"
    }
]

COMPANIES = [
    {
        "company_id": "tongwei",
        "name_zh": "通威股份有限公司",
        "stock_code": "600438.SH",
        "province": "四川",
        "city": "成都市",
        "industry": "电气设备",
        "main_business": "水产饲料,畜禽饲料等的研究,生产和销售,多晶硅,太阳能电池的研发,生产,销售"
    },
    {
        "company_id": "rebecca",
        "name_zh": "河南瑞贝卡发制品股份有限公司",
        "stock_code": "600439.SH",
        "province": "河南",
        "city": "许昌市",
        "industry": "服饰",
        "main_business": "工艺发条,化纤发,女装假发,教习头,男装头套等各种假发饰品"
    },
    {
        "company_id": "sinomach_tongyong",
        "name_zh": "国机通用机械科技股份有限公司",
        "stock_code": "600444.SH",
        "province": "安徽",
        "city": "合肥市",
        "industry": "专用机械",
        "main_business": "UPVC双壁波纹管,PE双壁波纹管"
    },
    {
        "company_id": "jinzheng",
        "name_zh": "深圳市金证科技股份有限公司",
        "stock_code": "600446.SH",
        "province": "广东",
        "city": "深圳市",
        "industry": "软件服务",
        "main_business": "系统集成,软件,硬件,系统维护,金融IT"
    },
    {
        "company_id": "huafang",
        "name_zh": "华纺股份有限公司",
        "stock_code": "600448.SH",
        "province": "山东",
        "city": "滨州市",
        "industry": "纺织",
        "main_business": "印染布,棉布,棉纱,毛条,毛纱,呢绒面料"
    },
    {
        "company_id": "ningxia_jiancai",
        "name_zh": "宁夏建材集团股份有限公司",
        "stock_code": "600449.SH",
        "province": "宁夏",
        "city": "银川市",
        "industry": "水泥",
        "main_business": "水泥,熟料,塑料管材的生产与销售"
    },
    {
        "company_id": "fuling_power",
        "name_zh": "重庆涪陵电力实业股份有限公司",
        "stock_code": "600452.SH",
        "province": "重庆",
        "city": "重庆市",
        "industry": "水力发电",
        "main_business": "电力供应与销售"
    },
    {
        "company_id": "botong",
        "name_zh": "西安博通资讯股份有限公司",
        "stock_code": "600455.SH",
        "province": "陕西",
        "city": "西安市",
        "industry": "文教休闲",
        "main_business": "定制软件,销售自制软件,系统集成,计算机设备销售"
    },
    {
        "company_id": "baoti",
        "name_zh": "宝鸡钛业股份有限公司",
        "stock_code": "600456.SH",
        "province": "陕西",
        "city": "宝鸡市",
        "industry": "小金属",
        "main_business": "各种规格的钛及钛合金板,带,箔,管,棒,线,锻件,铸件等加工材和各种金属复合材产品"
    },
    {
        "company_id": "tmt_newmaterial",
        "name_zh": "株洲时代新材料科技股份有限公司",
        "stock_code": "600458.SH",
        "province": "湖南",
        "city": "株洲市",
        "industry": "塑料",
        "main_business": "高分子减振降噪弹性元件,高分子复合改性材料,特种涂料,新型绝缘材料,桥梁支座,伸缩缝"
    }
]

EXPOSURES = [
    {
        "exposure_id": "tongwei_produce_aquatic_feed",
        "company_id": "tongwei",
        "node_id": "aquatic_feed",
        "activity_type": "produce",
        "role": "水产饲料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tongwei_produce_livestock_feed",
        "company_id": "tongwei",
        "node_id": "livestock_feed",
        "activity_type": "produce",
        "role": "畜禽饲料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "tongwei_produce_polysilicon",
        "company_id": "tongwei",
        "node_id": "polysilicon",
        "activity_type": "produce",
        "role": "多晶硅生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tongwei_produce_solar_cell",
        "company_id": "tongwei",
        "node_id": "solar_cell",
        "activity_type": "produce",
        "role": "太阳能电池生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tongwei_produce_photovoltaic",
        "company_id": "tongwei",
        "node_id": "photovoltaic",
        "activity_type": "produce",
        "role": "光伏产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "rebecca_produce_wig",
        "company_id": "rebecca",
        "node_id": "wig",
        "activity_type": "produce",
        "role": "假发饰品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "rebecca_produce_hair_product",
        "company_id": "rebecca",
        "node_id": "hair_product",
        "activity_type": "produce",
        "role": "发制品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "rebecca_produce_apparel_accessory",
        "company_id": "rebecca",
        "node_id": "apparel_accessory",
        "activity_type": "produce",
        "role": "服饰配饰生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "sinomach_tongyong_manufacture_upvc_pipe",
        "company_id": "sinomach_tongyong",
        "node_id": "upvc_pipe",
        "activity_type": "manufacture",
        "role": "UPVC波纹管制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "sinomach_tongyong_manufacture_pe_pipe",
        "company_id": "sinomach_tongyong",
        "node_id": "pe_pipe",
        "activity_type": "manufacture",
        "role": "PE波纹管制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "sinomach_tongyong_manufacture_plastic_pipe",
        "company_id": "sinomach_tongyong",
        "node_id": "plastic_pipe",
        "activity_type": "manufacture",
        "role": "塑料管道制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinzheng_provide_service_financial_it",
        "company_id": "jinzheng",
        "node_id": "financial_it",
        "activity_type": "provide_service",
        "role": "金融IT服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinzheng_provide_service_software",
        "company_id": "jinzheng",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinzheng_provide_service_system_integration",
        "company_id": "jinzheng",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "huafang_produce_printed_fabric",
        "company_id": "huafang",
        "node_id": "printed_fabric",
        "activity_type": "produce",
        "role": "印染布生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "huafang_produce_cotton_yarn",
        "company_id": "huafang",
        "node_id": "cotton_yarn",
        "activity_type": "produce",
        "role": "棉纱生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "huafang_produce_wool_fabric",
        "company_id": "huafang",
        "node_id": "wool_fabric",
        "activity_type": "produce",
        "role": "呢绒面料生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "huafang_produce_textile_product",
        "company_id": "huafang",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "ningxia_jiancai_produce_cement",
        "company_id": "ningxia_jiancai",
        "node_id": "cement",
        "activity_type": "produce",
        "role": "水泥生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "ningxia_jiancai_produce_plastic_pipe",
        "company_id": "ningxia_jiancai",
        "node_id": "plastic_pipe",
        "activity_type": "produce",
        "role": "塑料管材生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "ningxia_jiancai_produce_building_material",
        "company_id": "ningxia_jiancai",
        "node_id": "building_material",
        "activity_type": "produce",
        "role": "建材生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "fuling_power_operate_power_distribution",
        "company_id": "fuling_power",
        "node_id": "power_distribution",
        "activity_type": "operate",
        "role": "电力配供运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "fuling_power_provide_service_power_supply",
        "company_id": "fuling_power",
        "node_id": "power_supply",
        "activity_type": "provide_service",
        "role": "电力供应服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "botong_provide_service_software",
        "company_id": "botong",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "botong_provide_service_system_integration",
        "company_id": "botong",
        "node_id": "system_integration",
        "activity_type": "provide_service",
        "role": "系统集成服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "baoti_produce_titanium_alloy",
        "company_id": "baoti",
        "node_id": "titanium_alloy",
        "activity_type": "produce",
        "role": "钛合金生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "baoti_produce_nonferrous_metal",
        "company_id": "baoti",
        "node_id": "nonferrous_metal",
        "activity_type": "produce",
        "role": "有色金属生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "baoti_produce_metal_composite",
        "company_id": "baoti",
        "node_id": "metal_composite",
        "activity_type": "produce",
        "role": "金属复合材料生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "tmt_newmaterial_manufacture_polymer_damping_element",
        "company_id": "tmt_newmaterial",
        "node_id": "polymer_damping_element",
        "activity_type": "manufacture",
        "role": "高分子减振降噪元件制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "tmt_newmaterial_manufacture_polymer_composite",
        "company_id": "tmt_newmaterial",
        "node_id": "polymer_composite",
        "activity_type": "manufacture",
        "role": "高分子复合材料制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tmt_newmaterial_manufacture_special_coating",
        "company_id": "tmt_newmaterial",
        "node_id": "special_coating",
        "activity_type": "manufacture",
        "role": "特种涂料制造商",
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
            "evidence": make_evidence(f"tushare batch 074: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 074: " + e["description"]),
        })
    return {
        "batch_id": "batch_074",
        "task_description": "Batch 074: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 074: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_074",
        "task_description": "Batch 074: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 074 Submission")
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
