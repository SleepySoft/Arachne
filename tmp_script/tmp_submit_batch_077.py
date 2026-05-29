#!/usr/bin/env python3
"""Submit batch 077 to Arachne API."""
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
        "node_id": "nonferrous_metal_mining",
        "canonical_name_zh": "有色金属采选",
        "definition": "对有色金属矿床进行开采和选矿加工的生产活动",
        "entity_type": "service"
    },
    {
        "node_id": "civil_construction",
        "canonical_name_zh": "土建施工",
        "definition": "房屋建筑、道路桥梁等土木工程的现场施工建造活动",
        "entity_type": "service"
    },
    {
        "node_id": "textile_weaving",
        "canonical_name_zh": "纺织织造",
        "definition": "将纱线通过织机交织成布匹的纺织加工工序",
        "entity_type": "service"
    },
    {
        "node_id": "train_axle",
        "canonical_name_zh": "车轴",
        "definition": "铁路车辆上用于安装车轮并承受载荷的圆柱形关键零部件",
        "entity_type": "component"
    },
    {
        "node_id": "agricultural_machinery",
        "canonical_name_zh": "农业机械",
        "definition": "用于农业生产过程的机械设备，包括拖拉机、收割机、播种机等",
        "entity_type": "system"
    },
    {
        "node_id": "germanium_product",
        "canonical_name_zh": "锗产品",
        "definition": "以稀有金属锗为原料加工制成的产品，用于光纤、红外光学、半导体等领域",
        "entity_type": "material"
    },
    {
        "node_id": "data_network_product",
        "canonical_name_zh": "数据网络产品",
        "definition": "用于构建数据通信网络的设备和系统，包括路由器、交换机等",
        "entity_type": "device"
    },
    {
        "node_id": "pressure_vessel",
        "canonical_name_zh": "压力容器",
        "definition": "能够承受一定压力的密闭设备，用于储存或反应气体、液体等介质",
        "entity_type": "device"
    }
]

NEW_EDGES = [
    {
        "edge_id": "train_axle_to_rail_transit",
        "from_node": "train_axle",
        "to_node": "rail_transit",
        "edge_type": "composition",
        "description": "车轴是轨道交通车辆走行系统的核心组成部件"
    },
    {
        "edge_id": "germanium_product_to_semiconductor",
        "from_node": "germanium_product",
        "to_node": "semiconductor",
        "edge_type": "material_flow",
        "description": "锗是重要的半导体材料，广泛用于制造半导体器件"
    },
    {
        "edge_id": "pressure_vessel_to_chemical_industry",
        "from_node": "pressure_vessel",
        "to_node": "chemical_industry",
        "edge_type": "composition",
        "description": "压力容器是石油化工等化工行业生产过程中的关键装备"
    }
]

COMPANIES = [
    {
        "company_id": "pengxin_resources",
        "name_zh": "鹏欣环球资源股份有限公司",
        "stock_code": "600490.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "铜",
        "main_business": "有色金属及贵金属的采选业务,冶炼及销售,以及贸易,新能源及金融"
    },
    {
        "company_id": "st_longyuan",
        "name_zh": "龙元建设集团股份有限公司",
        "stock_code": "600491.SH",
        "province": "浙江",
        "city": "宁波市",
        "industry": "建筑工程",
        "main_business": "土建施工,装饰与钢结构,建筑设计及其他"
    },
    {
        "company_id": "fengzhu_textile",
        "name_zh": "福建凤竹纺织科技股份有限公司",
        "stock_code": "600493.SH",
        "province": "福建",
        "city": "泉州市",
        "industry": "纺织",
        "main_business": "织造,染纱,染整加工,污水处理"
    },
    {
        "company_id": "jinxi_axle",
        "name_zh": "晋西车轴股份有限公司",
        "stock_code": "600495.SH",
        "province": "山西",
        "city": "太原市",
        "industry": "运输设备",
        "main_business": "车轴的生产与销售"
    },
    {
        "company_id": "jinggong_steel",
        "name_zh": "长江精工钢结构(集团)股份有限公司",
        "stock_code": "600496.SH",
        "province": "安徽",
        "city": "六安市",
        "industry": "钢加工",
        "main_business": "钢结构行业,农业机械行业"
    },
    {
        "company_id": "chihong",
        "name_zh": "云南驰宏锌锗股份有限公司",
        "stock_code": "600497.SH",
        "province": "云南",
        "city": "曲靖市",
        "industry": "铅锌",
        "main_business": "锌产品,铅产品,银产品,锗产品"
    },
    {
        "company_id": "fiberhome",
        "name_zh": "烽火通信科技股份有限公司",
        "stock_code": "600498.SH",
        "province": "湖北",
        "city": "武汉市",
        "industry": "通信设备",
        "main_business": "通信设备,光纤,光缆及电缆,数据网络产品"
    },
    {
        "company_id": "keda_manufacturing",
        "name_zh": "科达制造股份有限公司",
        "stock_code": "600499.SH",
        "province": "广东",
        "city": "佛山市",
        "industry": "专用机械",
        "main_business": "机械产品,中药产品,自制配件及其他"
    },
    {
        "company_id": "sinochem_intl",
        "name_zh": "中化国际(控股)股份有限公司",
        "stock_code": "600500.SH",
        "province": "上海",
        "city": "上海市",
        "industry": "塑料",
        "main_business": "储罐,焦炭等冶金产品,农药及其他商品,化工物流,塑料原料,橡胶及橡胶制品"
    },
    {
        "company_id": "aerosun",
        "name_zh": "航天晨光股份有限公司",
        "stock_code": "600501.SH",
        "province": "江苏",
        "city": "南京市",
        "industry": "专用机械",
        "main_business": "专用车类产品,波纹管类产品,压力容器类产品"
    }
]

EXPOSURES = [
    {
        "exposure_id": "pengxin_resources_operate_nonferrous_metal_mining",
        "company_id": "pengxin_resources",
        "node_id": "nonferrous_metal_mining",
        "activity_type": "operate",
        "role": "有色金属采选运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "pengxin_resources_produce_nonferrous_metal",
        "company_id": "pengxin_resources",
        "node_id": "nonferrous_metal",
        "activity_type": "produce",
        "role": "有色金属生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "pengxin_resources_produce_precious_metal",
        "company_id": "pengxin_resources",
        "node_id": "precious_metal",
        "activity_type": "produce",
        "role": "贵金属生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_longyuan_operate_civil_construction",
        "company_id": "st_longyuan",
        "node_id": "civil_construction",
        "activity_type": "operate",
        "role": "土建施工运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "st_longyuan_operate_construction",
        "company_id": "st_longyuan",
        "node_id": "construction",
        "activity_type": "operate",
        "role": "建筑施工运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "st_longyuan_provide_service_building_design",
        "company_id": "st_longyuan",
        "node_id": "building_design",
        "activity_type": "provide_service",
        "role": "建筑设计服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "fengzhu_textile_operate_textile_weaving",
        "company_id": "fengzhu_textile",
        "node_id": "textile_weaving",
        "activity_type": "operate",
        "role": "纺织织造运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "fengzhu_textile_produce_textile_product",
        "company_id": "fengzhu_textile",
        "node_id": "textile_product",
        "activity_type": "produce",
        "role": "纺织品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "fengzhu_textile_operate_wastewater_treatment",
        "company_id": "fengzhu_textile",
        "node_id": "wastewater_treatment",
        "activity_type": "operate",
        "role": "污水处理运营商",
        "weight": 0.85
    },
    {
        "exposure_id": "jinxi_axle_manufacture_train_axle",
        "company_id": "jinxi_axle",
        "node_id": "train_axle",
        "activity_type": "manufacture",
        "role": "车轴制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinxi_axle_manufacture_rail_transit_equipment",
        "company_id": "jinxi_axle",
        "node_id": "rail_transit_equipment",
        "activity_type": "manufacture",
        "role": "轨道交通设备制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jinggong_steel_produce_steel_structure",
        "company_id": "jinggong_steel",
        "node_id": "steel_structure",
        "activity_type": "produce",
        "role": "钢结构生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "jinggong_steel_manufacture_agricultural_machinery",
        "company_id": "jinggong_steel",
        "node_id": "agricultural_machinery",
        "activity_type": "manufacture",
        "role": "农业机械制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "chihong_produce_zinc_product",
        "company_id": "chihong",
        "node_id": "zinc_product",
        "activity_type": "produce",
        "role": "锌产品生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "chihong_produce_lead_product",
        "company_id": "chihong",
        "node_id": "lead_product",
        "activity_type": "produce",
        "role": "铅产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "chihong_produce_silver_product",
        "company_id": "chihong",
        "node_id": "silver_product",
        "activity_type": "produce",
        "role": "银产品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "chihong_produce_germanium_product",
        "company_id": "chihong",
        "node_id": "germanium_product",
        "activity_type": "produce",
        "role": "锗产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "fiberhome_manufacture_communication_equipment",
        "company_id": "fiberhome",
        "node_id": "communication_equipment",
        "activity_type": "manufacture",
        "role": "通信设备制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "fiberhome_manufacture_optical_fiber_cable",
        "company_id": "fiberhome",
        "node_id": "optical_fiber_cable",
        "activity_type": "manufacture",
        "role": "光纤光缆制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "fiberhome_manufacture_data_network_product",
        "company_id": "fiberhome",
        "node_id": "data_network_product",
        "activity_type": "manufacture",
        "role": "数据网络产品制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "keda_manufacturing_manufacture_ceramic_machinery",
        "company_id": "keda_manufacturing",
        "node_id": "ceramic_machinery",
        "activity_type": "manufacture",
        "role": "陶瓷机械制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "keda_manufacturing_produce_chinese_patent_medicine",
        "company_id": "keda_manufacturing",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中药产品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "sinochem_intl_provide_service_chemical_logistics",
        "company_id": "sinochem_intl",
        "node_id": "chemical_logistics",
        "activity_type": "provide_service",
        "role": "化工物流服务商",
        "weight": 0.9
    },
    {
        "exposure_id": "sinochem_intl_produce_plastic_raw_material",
        "company_id": "sinochem_intl",
        "node_id": "plastic_raw_material",
        "activity_type": "produce",
        "role": "塑料原料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "sinochem_intl_produce_rubber_product",
        "company_id": "sinochem_intl",
        "node_id": "rubber_product",
        "activity_type": "produce",
        "role": "橡胶制品生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "aerosun_manufacture_special_vehicle",
        "company_id": "aerosun",
        "node_id": "special_vehicle",
        "activity_type": "manufacture",
        "role": "专用车制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "aerosun_manufacture_bellows",
        "company_id": "aerosun",
        "node_id": "bellows",
        "activity_type": "manufacture",
        "role": "波纹管制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "aerosun_manufacture_pressure_vessel",
        "company_id": "aerosun",
        "node_id": "pressure_vessel",
        "activity_type": "manufacture",
        "role": "压力容器制造商",
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
            "evidence": make_evidence(f"tushare batch 077: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch 077: " + e["description"]),
        })
    return {
        "batch_id": "batch_077",
        "task_description": "Batch 077: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch 077: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_077",
        "task_description": "Batch 077: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 077 Submission")
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
