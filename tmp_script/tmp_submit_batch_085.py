#!/usr/bin/env python3
"""Submit batch 085 to Arachne API."""
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
        "node_id": "flat_glass",
        "canonical_name_zh": "平板玻璃",
        "definition": "通过浮法等工艺生产的平整透明玻璃板材，广泛用于建筑门窗、幕墙、汽车等领域",
        "entity_type": "material"
    },
    {
        "node_id": "sterilization_equipment",
        "canonical_name_zh": "消毒灭菌设备",
        "definition": "用于医疗器械、药品等消毒灭菌处理的专用设备，包括高温高压灭菌器、环氧乙烷灭菌器等",
        "entity_type": "device"
    },
    {
        "node_id": "pharmaceutical_equipment",
        "canonical_name_zh": "制药设备",
        "definition": "用于药品生产过程中的专用机械设备，包括制粒机、压片机、灌装机等",
        "entity_type": "device"
    },
    {
        "node_id": "amino_composite_material",
        "canonical_name_zh": "氨基复合材料",
        "definition": "以氨基树脂为基体的复合材料，具有硬度高、耐磨性好的特点，用于制造餐具和装饰材料",
        "entity_type": "material"
    },
    {
        "node_id": "idc",
        "canonical_name_zh": "互联网数据中心",
        "definition": "提供服务器托管、租用及互联网接入等服务的专业化数据中心设施",
        "entity_type": "service"
    },
    {
        "node_id": "bearing",
        "canonical_name_zh": "轴承",
        "definition": "支承机械旋转体并降低其运动过程中摩擦系数的精密机械零部件",
        "entity_type": "component"
    },
    {
        "node_id": "high_performance_aluminum_sheet",
        "canonical_name_zh": "高性能铝合金板材",
        "definition": "通过合金化及热处理获得高强度、耐腐蚀等优异性能的铝板带材产品",
        "entity_type": "material"
    },
    {
        "node_id": "glyphosate",
        "canonical_name_zh": "草甘膦",
        "definition": "一种广谱灭生性除草剂的主要有效成分，通过抑制植物芳香族氨基酸合成途径起作用",
        "entity_type": "material"
    }
]

NEW_EDGES = [
    {
        "edge_id": "flat_glass_to_construction",
        "from_node": "flat_glass",
        "to_node": "construction",
        "edge_type": "material_flow",
        "description": "平板玻璃是建筑门窗幕墙和室内装修的主要材料"
    },
    {
        "edge_id": "bearing_to_automobile",
        "from_node": "bearing",
        "to_node": "automobile",
        "edge_type": "composition",
        "description": "轴承是汽车发动机、变速箱和车轮等关键部位的精密支撑部件"
    },
    {
        "edge_id": "glyphosate_to_pesticide",
        "from_node": "glyphosate",
        "to_node": "pesticide",
        "edge_type": "material_flow",
        "description": "草甘膦是生产广谱除草剂农药的主要有效成分"
    }
]

COMPANIES = [
    {
        "company_id": "jinjing",
        "name_zh": "山东金晶科技股份有限公司",
        "stock_code": "600586.SH",
        "province": "山东",
        "city": "淄博市",
        "industry": "玻璃",
        "main_business": "玻璃和纯碱的生产与销售"
    },
    {
        "company_id": "shinva",
        "name_zh": "山东新华医疗器械股份有限公司",
        "stock_code": "600587.SH",
        "province": "山东",
        "city": "淄博市",
        "industry": "医疗保健",
        "main_business": "消毒灭菌设备,放射诊断及治疗设备,制药设备,环保设备"
    },
    {
        "company_id": "yonyou",
        "name_zh": "用友网络科技股份有限公司",
        "stock_code": "600588.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "软件服务",
        "main_business": "软件销售,技术服务及培训,软件配套用品销售"
    },
    {
        "company_id": "dawei",
        "name_zh": "大位数据科技(广东)集团股份有限公司",
        "stock_code": "600589.SH",
        "province": "广东",
        "city": "揭阳市",
        "industry": "软件服务",
        "main_business": "氨基复合材料,苯酐及增塑剂等化工材料;互联网数据中心(IDC),云计算,CDN"
    },
    {
        "company_id": "tellhow",
        "name_zh": "泰豪科技股份有限公司",
        "stock_code": "600590.SH",
        "province": "江西",
        "city": "南昌市",
        "industry": "通信设备",
        "main_business": "智能电力,装备信息,智能节能,电机产业"
    },
    {
        "company_id": "longxi",
        "name_zh": "福建龙溪轴承(集团)股份有限公司",
        "stock_code": "600592.SH",
        "province": "福建",
        "city": "漳州市",
        "industry": "机械基件",
        "main_business": "轴承,汽车配件"
    },
    {
        "company_id": "dalian_shengya",
        "name_zh": "大连圣亚旅游控股股份有限公司",
        "stock_code": "600593.SH",
        "province": "辽宁",
        "city": "大连市",
        "industry": "旅游景点",
        "main_business": "景观,餐饮,景点场地出租"
    },
    {
        "company_id": "yibai",
        "name_zh": "贵州益佰制药股份有限公司",
        "stock_code": "600594.SH",
        "province": "贵州",
        "city": "贵阳市",
        "industry": "中成药",
        "main_business": "OTC药,处方药"
    },
    {
        "company_id": "zhongfu",
        "name_zh": "河南中孚实业股份有限公司",
        "stock_code": "600595.SH",
        "province": "河南",
        "city": "郑州市",
        "industry": "铝",
        "main_business": "高性能铝合金板材,易拉罐罐体,罐盖,拉环料,高档双零铝箔毛料,印刷版基"
    },
    {
        "company_id": "xinan",
        "name_zh": "浙江新安化工集团股份有限公司",
        "stock_code": "600596.SH",
        "province": "浙江",
        "city": "杭州市",
        "industry": "化工原料",
        "main_business": "以草甘膦为主的农药产品和有机硅新材料产品"
    }
]

EXPOSURES = [
    {
        "exposure_id": "jinjing_produce_flat_glass",
        "company_id": "jinjing",
        "node_id": "flat_glass",
        "activity_type": "produce",
        "role": "平板玻璃生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinjing_produce_soda_ash",
        "company_id": "jinjing",
        "node_id": "soda_ash",
        "activity_type": "produce",
        "role": "纯碱生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "shinva_manufacture_sterilization_equipment",
        "company_id": "shinva",
        "node_id": "sterilization_equipment",
        "activity_type": "manufacture",
        "role": "消毒灭菌设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "shinva_manufacture_radiotherapy_equipment",
        "company_id": "shinva",
        "node_id": "radiotherapy_equipment",
        "activity_type": "manufacture",
        "role": "放射诊断及治疗设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "shinva_manufacture_pharmaceutical_equipment",
        "company_id": "shinva",
        "node_id": "pharmaceutical_equipment",
        "activity_type": "manufacture",
        "role": "制药设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "yonyou_provide_service_application_software",
        "company_id": "yonyou",
        "node_id": "application_software",
        "activity_type": "provide_service",
        "role": "应用软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "yonyou_provide_service_software",
        "company_id": "yonyou",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "yonyou_provide_service_it_service",
        "company_id": "yonyou",
        "node_id": "it_service",
        "activity_type": "provide_service",
        "role": "IT服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "dawei_produce_amino_composite_material",
        "company_id": "dawei",
        "node_id": "amino_composite_material",
        "activity_type": "produce",
        "role": "氨基复合材料生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "dawei_produce_phthalic_anhydride",
        "company_id": "dawei",
        "node_id": "phthalic_anhydride",
        "activity_type": "produce",
        "role": "苯酐生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "dawei_produce_plasticizer",
        "company_id": "dawei",
        "node_id": "plasticizer",
        "activity_type": "produce",
        "role": "增塑剂生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "dawei_operate_idc",
        "company_id": "dawei",
        "node_id": "idc",
        "activity_type": "operate",
        "role": "互联网数据中心运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "dawei_provide_service_cloud_computing",
        "company_id": "dawei",
        "node_id": "cloud_computing",
        "activity_type": "provide_service",
        "role": "云计算服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "tellhow_manufacture_smart_grid_device",
        "company_id": "tellhow",
        "node_id": "smart_grid_device",
        "activity_type": "manufacture",
        "role": "智能电力设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "tellhow_manufacture_electric_motor",
        "company_id": "tellhow",
        "node_id": "electric_motor",
        "activity_type": "manufacture",
        "role": "电机制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tellhow_provide_service_energy_saving",
        "company_id": "tellhow",
        "node_id": "energy_saving",
        "activity_type": "provide_service",
        "role": "节能服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "longxi_manufacture_bearing",
        "company_id": "longxi",
        "node_id": "bearing",
        "activity_type": "manufacture",
        "role": "轴承制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "longxi_manufacture_automobile_part",
        "company_id": "longxi",
        "node_id": "automobile_part",
        "activity_type": "manufacture",
        "role": "汽车配件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "dalian_shengya_operate_scenic_spot",
        "company_id": "dalian_shengya",
        "node_id": "scenic_spot",
        "activity_type": "operate",
        "role": "景点运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "dalian_shengya_operate_catering_service",
        "company_id": "dalian_shengya",
        "node_id": "catering_service",
        "activity_type": "operate",
        "role": "餐饮服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "dalian_shengya_provide_service_tourism_service",
        "company_id": "dalian_shengya",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "role": "旅游服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "yibai_produce_otc_drug",
        "company_id": "yibai",
        "node_id": "otc_drug",
        "activity_type": "produce",
        "role": "OTC药品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "yibai_produce_prescription_drug",
        "company_id": "yibai",
        "node_id": "prescription_drug",
        "activity_type": "produce",
        "role": "处方药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "yibai_produce_pharmaceutical",
        "company_id": "yibai",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "zhongfu_produce_high_performance_aluminum_sheet",
        "company_id": "zhongfu",
        "node_id": "high_performance_aluminum_sheet",
        "activity_type": "produce",
        "role": "高性能铝合金板材生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "zhongfu_produce_can_body_stock",
        "company_id": "zhongfu",
        "node_id": "can_body_stock",
        "activity_type": "produce",
        "role": "易拉罐料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "zhongfu_produce_aluminum_foil",
        "company_id": "zhongfu",
        "node_id": "aluminum_foil",
        "activity_type": "produce",
        "role": "铝箔生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "xinan_produce_glyphosate",
        "company_id": "xinan",
        "node_id": "glyphosate",
        "activity_type": "produce",
        "role": "草甘膦生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xinan_produce_organosilicon",
        "company_id": "xinan",
        "node_id": "organosilicon",
        "activity_type": "produce",
        "role": "有机硅生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "xinan_produce_pesticide",
        "company_id": "xinan",
        "node_id": "pesticide",
        "activity_type": "produce",
        "role": "农药生产商",
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
            "evidence": make_evidence(f"tushare batch 085: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 085: " + e["description"]),
        })
    return {
        "batch_id": "batch_085",
        "task_description": "Batch 085: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 085: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_085",
        "task_description": "Batch 085: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 085 Submission")
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
