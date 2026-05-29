#!/usr/bin/env python3
"""Submit batch 076 to Arachne API."""
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
        "node_id": "light_steel_structure",
        "canonical_name_zh": "轻型钢结构",
        "definition": "以轻型钢材为主要承重构件的建筑结构体系，具有自重轻、施工快、抗震好的特点",
        "entity_type": "material"
    },
    {
        "node_id": "foam_nickel",
        "canonical_name_zh": "泡沫镍",
        "definition": "具有三维多孔网状结构的镍材料，用于电池电极、催化剂载体和过滤材料",
        "entity_type": "material"
    },
    {
        "node_id": "lithium_bromide_chiller",
        "canonical_name_zh": "溴化锂制冷机",
        "definition": "以溴化锂水溶液为工质的吸收式制冷设备，利用热能驱动实现制冷",
        "entity_type": "device"
    },
    {
        "node_id": "heat_exchanger",
        "canonical_name_zh": "高效换热器",
        "definition": "实现两种或多种流体之间热量传递的高效节能设备，广泛应用于电力、化工、暖通等领域",
        "entity_type": "device"
    },
    {
        "node_id": "styrene",
        "canonical_name_zh": "苯乙烯",
        "definition": "重要的基础有机化工原料，用于生产聚苯乙烯、ABS树脂、合成橡胶等高分子材料",
        "entity_type": "material"
    },
    {
        "node_id": "pyrethroid",
        "canonical_name_zh": "菊酯",
        "definition": "模拟天然除虫菊素结构合成的仿生杀虫剂，具有高效、低毒、低残留的特点",
        "entity_type": "material"
    },
    {
        "node_id": "optical_fiber_cable",
        "canonical_name_zh": "光纤光缆",
        "definition": "以光纤为传输介质、用于通信信号长距离传输的线缆产品",
        "entity_type": "component"
    },
    {
        "node_id": "corticosteroid",
        "canonical_name_zh": "皮质激素",
        "definition": "由肾上腺皮质分泌的具有抗炎、免疫抑制等作用的甾体激素类药物",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "light_steel_structure_to_construction",
        "from_node": "light_steel_structure",
        "to_node": "construction",
        "edge_type": "material_flow",
        "description": "轻型钢结构是现代建筑工程建设的重要结构材料"
    },
    {
        "edge_id": "foam_nickel_to_battery",
        "from_node": "foam_nickel",
        "to_node": "battery",
        "edge_type": "composition",
        "description": "泡沫镍是镍氢电池和镍镉电池电极的核心基板材料"
    },
    {
        "edge_id": "optical_fiber_cable_to_communication_equipment",
        "from_node": "optical_fiber_cable",
        "to_node": "communication_equipment",
        "edge_type": "composition",
        "description": "光纤光缆是通信网络传输系统的核心物理介质"
    }
]

COMPANIES = [
    {
        "company_id": "hangxiao",
        "name_zh": "杭萧钢构股份有限公司",
        "stock_code": "600477.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "钢加工",
        "main_business": "轻型钢结构,多高层钢结构,商品销售"
    },
    {
        "company_id": "corun",
        "name_zh": "湖南科力远新能源股份有限公司",
        "stock_code": "600478.SH",
        "province": "湖南",
        "city": "长沙市",
        "industry": "电气设备",
        "main_business": "泡沫镍"
    },
    {
        "company_id": "qianjin_pharma",
        "name_zh": "株洲千金药业股份有限公司",
        "stock_code": "600479.SH",
        "province": "湖南",
        "city": "株洲市",
        "industry": "中成药",
        "main_business": "妇科千金片等中成药的生产与销售"
    },
    {
        "company_id": "lingyun",
        "name_zh": "凌云工业股份有限公司",
        "stock_code": "600480.SH",
        "province": "河北",
        "city": "保定市",
        "industry": "汽车配件",
        "main_business": "汽车金属及塑料零部件,塑料管道系统"
    },
    {
        "company_id": "shuangliang",
        "name_zh": "双良节能系统股份有限公司",
        "stock_code": "600481.SH",
        "province": "江苏",
        "city": "无锡市",
        "industry": "电气设备",
        "main_business": "溴化锂制冷机,高效换热器,空冷器等换热设备和苯乙烯,聚苯乙烯产品"
    },
    {
        "company_id": "funeng",
        "name_zh": "福建福能股份有限公司",
        "stock_code": "600483.SH",
        "province": "福建",
        "city": "福州市",
        "industry": "新型电力",
        "main_business": "电力和纺织业"
    },
    {
        "company_id": "yangnong",
        "name_zh": "江苏扬农化工股份有限公司",
        "stock_code": "600486.SH",
        "province": "江苏",
        "city": "扬州市",
        "industry": "农药化肥",
        "main_business": "卫生用菊酯,农用菊酯"
    },
    {
        "company_id": "hengtong",
        "name_zh": "江苏亨通光电股份有限公司",
        "stock_code": "600487.SH",
        "province": "江苏",
        "city": "苏州市",
        "industry": "通信设备",
        "main_business": "通信网络业务,能源互联业务"
    },
    {
        "company_id": "tianjin_pharma",
        "name_zh": "津药药业股份有限公司",
        "stock_code": "600488.SH",
        "province": "天津",
        "city": "天津市",
        "industry": "化学制药",
        "main_business": "皮质激素,类原料药,心血管类,原料药,水针剂"
    },
    {
        "company_id": "zhongjin_gold",
        "name_zh": "中金黄金股份有限公司",
        "stock_code": "600489.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "黄金",
        "main_business": "黄金的生产与销售"
    }
]

EXPOSURES = [
    {
        "exposure_id": "hangxiao_produce_light_steel_structure",
        "company_id": "hangxiao",
        "node_id": "light_steel_structure",
        "activity_type": "produce",
        "role": "轻型钢结构生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "hangxiao_produce_steel_structure",
        "company_id": "hangxiao",
        "node_id": "steel_structure",
        "activity_type": "produce",
        "role": "钢结构生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "hangxiao_produce_steel",
        "company_id": "hangxiao",
        "node_id": "steel",
        "activity_type": "produce",
        "role": "钢材加工商",
        "weight": 0.85
    },
    {
        "exposure_id": "corun_produce_foam_nickel",
        "company_id": "corun",
        "node_id": "foam_nickel",
        "activity_type": "produce",
        "role": "泡沫镍生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "corun_produce_battery_material",
        "company_id": "corun",
        "node_id": "battery_material",
        "activity_type": "produce",
        "role": "电池材料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "qianjin_pharma_produce_gynecology_chinese_patent_medicine",
        "company_id": "qianjin_pharma",
        "node_id": "gynecology_chinese_patent_medicine",
        "activity_type": "produce",
        "role": "妇科中成药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "qianjin_pharma_produce_chinese_patent_medicine",
        "company_id": "qianjin_pharma",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "lingyun_manufacture_automobile_plastic_part",
        "company_id": "lingyun",
        "node_id": "automobile_plastic_part",
        "activity_type": "manufacture",
        "role": "汽车塑料零部件制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "lingyun_manufacture_automobile_part",
        "company_id": "lingyun",
        "node_id": "automobile_part",
        "activity_type": "manufacture",
        "role": "汽车零部件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "lingyun_manufacture_plastic_pipe",
        "company_id": "lingyun",
        "node_id": "plastic_pipe",
        "activity_type": "manufacture",
        "role": "塑料管道制造商",
        "weight": 0.85
    },
    {
        "exposure_id": "shuangliang_manufacture_lithium_bromide_chiller",
        "company_id": "shuangliang",
        "node_id": "lithium_bromide_chiller",
        "activity_type": "manufacture",
        "role": "溴化锂制冷机制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "shuangliang_manufacture_heat_exchanger",
        "company_id": "shuangliang",
        "node_id": "heat_exchanger",
        "activity_type": "manufacture",
        "role": "换热器制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "shuangliang_manufacture_air_cooler",
        "company_id": "shuangliang",
        "node_id": "air_cooler",
        "activity_type": "manufacture",
        "role": "空冷器制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shuangliang_produce_styrene",
        "company_id": "shuangliang",
        "node_id": "styrene",
        "activity_type": "produce",
        "role": "苯乙烯生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "funeng_operate_power_generation",
        "company_id": "funeng",
        "node_id": "power_generation",
        "activity_type": "operate",
        "role": "电力运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "funeng_produce_textile_product",
        "company_id": "funeng",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "yangnong_produce_pyrethroid",
        "company_id": "yangnong",
        "node_id": "pyrethroid",
        "activity_type": "produce",
        "role": "菊酯生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "yangnong_produce_pesticide",
        "company_id": "yangnong",
        "node_id": "pesticide",
        "activity_type": "produce",
        "role": "农药生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "hengtong_manufacture_optical_fiber_cable",
        "company_id": "hengtong",
        "node_id": "optical_fiber_cable",
        "activity_type": "manufacture",
        "role": "光纤光缆制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "hengtong_manufacture_communication_equipment",
        "company_id": "hengtong",
        "node_id": "communication_equipment",
        "activity_type": "manufacture",
        "role": "通信设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tianjin_pharma_produce_corticosteroid",
        "company_id": "tianjin_pharma",
        "node_id": "corticosteroid",
        "activity_type": "produce",
        "role": "皮质激素生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianjin_pharma_produce_pharmaceutical",
        "company_id": "tianjin_pharma",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "zhongjin_gold_produce_gold",
        "company_id": "zhongjin_gold",
        "node_id": "gold",
        "activity_type": "produce",
        "role": "黄金生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongjin_gold_produce_nonferrous_metal",
        "company_id": "zhongjin_gold",
        "node_id": "nonferrous_metal",
        "activity_type": "produce",
        "role": "有色金属生产商",
        "weight": 0.9
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
            "evidence": make_evidence(f"tushare batch 076: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 076: " + e["description"]),
        })
    return {
        "batch_id": "batch_076",
        "task_description": "Batch 076: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 076: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_076",
        "task_description": "Batch 076: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 076 Submission")
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
