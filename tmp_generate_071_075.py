#!/usr/bin/env python3
"""Generate tmp_submit_batch_071.py through tmp_submit_batch_075.py."""
import json, os

# Use %% placeholders instead of {} to avoid format conflicts
TEMPLATE = '''#!/usr/bin/env python3
"""Submit batch %%NNN%% to Arachne API."""
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

NEW_NODES = %%NEW_NODES%%

NEW_EDGES = %%NEW_EDGES%%

COMPANIES = %%COMPANIES%%

EXPOSURES = %%EXPOSURES%%

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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + e["description"]),
        })
    return {
        "batch_id": "batch_%%NNN%%",
        "task_description": "Batch %%NNN%%: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_%%NNN%%",
        "task_description": "Batch %%NNN%%: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch %%NNN%% Submission")
    print("=" * 60)
    graph_batch = build_graph_batch()
    print(f"\\nGraph batch: {len(graph_batch['nodes_to_upsert'])} nodes, {len(graph_batch['edges_to_upsert'])} edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, resp = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {resp}")
    else:
        print("Graph batch: nothing to submit")
    biz_batch = build_business_batch()
    print(f"\\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, resp = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {resp}")
    print("\\nDone.")
'''

BATCH_071 = {
    "new_nodes": [
        {"node_id": "superhard_material", "canonical_name_zh": "超硬材料", "definition": "硬度极高的材料，如金刚石、立方氮化硼等，用于切削、磨削工具", "entity_type": "material"},
        {"node_id": "battery_cathode_material", "canonical_name_zh": "电池正极材料", "definition": "锂离子电池正极活性物质，如钴酸锂、磷酸铁锂、三元材料等", "entity_type": "material"},
        {"node_id": "aeroengine_part", "canonical_name_zh": "航空发动机零部件", "definition": "航空发动机的核心部件，包括叶片、盘、轴、机匣等", "entity_type": "component"},
        {"node_id": "gas_turbine_part", "canonical_name_zh": "燃气轮机零部件", "definition": "燃气轮机的关键部件，包括压气机、燃烧室、涡轮等组件", "entity_type": "component"},
        {"node_id": "rare_earth_metal", "canonical_name_zh": "稀有稀土金属", "definition": "稀土元素及其合金，包括镧、铈、钕、钐等17种元素", "entity_type": "material"},
        {"node_id": "catalytic_material", "canonical_name_zh": "催化材料", "definition": "用于加速化学反应速率的材料，包括催化剂、催化助剂等", "entity_type": "material"},
        {"node_id": "alloy_structural_steel", "canonical_name_zh": "合金结构钢", "definition": "在碳素结构钢基础上添加合金元素以提高强度、韧性和耐磨性的钢材", "entity_type": "material"},
        {"node_id": "superalloy", "canonical_name_zh": "高温合金", "definition": "能在高温氧化和燃气腐蚀条件下长期工作的合金材料，主要用于航空发动机和燃气轮机", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "aeroengine_part_to_aircraft_engine", "from_node": "aeroengine_part", "to_node": "aircraft_engine", "edge_type": "composition", "description": "航空发动机零部件是航空发动机的核心组成部件"},
        {"edge_id": "battery_cathode_material_to_lithium_battery", "from_node": "battery_cathode_material", "to_node": "lithium_battery", "edge_type": "composition", "description": "电池正极材料是锂离子电池的关键组成部分"},
        {"edge_id": "superalloy_to_aircraft_engine", "from_node": "superalloy", "to_node": "aircraft_engine", "edge_type": "material_flow", "description": "高温合金材料用于制造航空发动机的热端部件"},
    ],
    "companies": [
        {"company_id": "minmetals_capital", "name_zh": "五矿资本股份有限公司", "stock_code": "600390.SH", "province": "湖南", "city": "长沙市", "industry": "多元金融", "main_business": "超硬材料,电子基础材料,电池正极材料,证券,期货,信托,金融租赁"},
        {"company_id": "aeroengine_tech", "name_zh": "中国航发航空科技股份有限公司", "stock_code": "600391.SH", "province": "四川", "city": "成都市", "industry": "航空", "main_business": "航空发动机零部件,燃气轮机零部件,空调壳体件,石油机械零部件"},
        {"company_id": "shenghe_resources", "name_zh": "盛和资源控股股份有限公司", "stock_code": "600392.SH", "province": "四川", "city": "成都市", "industry": "小金属", "main_business": "稀土矿山开采,稀土产品生产及销售,催化材料生产及销售,稀有稀土金属冶炼与销售"},
        {"company_id": "panjiang", "name_zh": "贵州盘江精煤股份有限公司", "stock_code": "600395.SH", "province": "贵州", "city": "六盘水市", "industry": "煤炭开采", "main_business": "精煤,混煤的生产与销售"},
        {"company_id": "huadian_liaoning", "name_zh": "华电辽宁能源发展股份有限公司", "stock_code": "600396.SH", "province": "辽宁", "city": "沈阳市", "industry": "火力发电", "main_business": "电力,热力的生产和供应"},
        {"company_id": "jiangtungsten", "name_zh": "江西江州联合造船有限责任公司", "stock_code": "600397.SH", "province": "江西", "city": "九江市", "industry": "专用机械", "main_business": "煤炭开采,煤炭精选加工,煤炭经营"},
        {"company_id": "hla", "name_zh": "海澜之家集团股份有限公司", "stock_code": "600398.SH", "province": "江苏", "city": "无锡市", "industry": "服饰", "main_business": "品牌服饰的经营,包括品牌管理,供应链管理和营销网络管理"},
        {"company_id": "fushun_special_steel", "name_zh": "抚顺特殊钢股份有限公司", "stock_code": "600399.SH", "province": "辽宁", "city": "抚顺市", "industry": "特种钢", "main_business": "合金结构钢,工模具钢,不锈钢和高温合金的研发制造"},
        {"company_id": "hongdou", "name_zh": "红豆集团股份有限公司", "stock_code": "600400.SH", "province": "江苏", "city": "无锡市", "industry": "服饰", "main_business": "服装,毛线纱线及印染"},
        {"company_id": "dayou_energy", "name_zh": "河南大有能源股份有限公司", "stock_code": "600403.SH", "province": "河南", "city": "三门峡市", "industry": "煤炭开采", "main_business": "煤炭生产与经营"},
    ],
    "exposures": [
        {"exposure_id": "minmetals_capital_produce_superhard_material", "company_id": "minmetals_capital", "node_id": "superhard_material", "activity_type": "produce", "role": "超硬材料生产商", "weight": 0.9},
        {"exposure_id": "minmetals_capital_produce_battery_cathode_material", "company_id": "minmetals_capital", "node_id": "battery_cathode_material", "activity_type": "produce", "role": "电池正极材料生产商", "weight": 0.85},
        {"exposure_id": "minmetals_capital_provide_service_securities_service", "company_id": "minmetals_capital", "node_id": "securities_service", "activity_type": "provide_service", "role": "证券服务商", "weight": 0.95},
        {"exposure_id": "minmetals_capital_provide_service_financial_service", "company_id": "minmetals_capital", "node_id": "financial_service", "activity_type": "provide_service", "role": "综合金融服务商", "weight": 0.9},
        {"exposure_id": "aeroengine_tech_manufacture_aeroengine_part", "company_id": "aeroengine_tech", "node_id": "aeroengine_part", "activity_type": "manufacture", "role": "航空发动机零部件制造商", "weight": 0.95},
        {"exposure_id": "aeroengine_tech_manufacture_gas_turbine_part", "company_id": "aeroengine_tech", "node_id": "gas_turbine_part", "activity_type": "manufacture", "role": "燃气轮机零部件制造商", "weight": 0.9},
        {"exposure_id": "aeroengine_tech_manufacture_aircraft_engine", "company_id": "aeroengine_tech", "node_id": "aircraft_engine", "activity_type": "manufacture", "role": "航空发动机制造商", "weight": 0.85},
        {"exposure_id": "shenghe_resources_produce_rare_earth_metal", "company_id": "shenghe_resources", "node_id": "rare_earth_metal", "activity_type": "produce", "role": "稀有稀土金属生产商", "weight": 0.95},
        {"exposure_id": "shenghe_resources_produce_catalytic_material", "company_id": "shenghe_resources", "node_id": "catalytic_material", "activity_type": "produce", "role": "催化材料生产商", "weight": 0.9},
        {"exposure_id": "shenghe_resources_operate_rare_earth_mining", "company_id": "shenghe_resources", "node_id": "rare_earth_mining", "activity_type": "operate", "role": "稀土矿山开采运营商", "weight": 0.9},
        {"exposure_id": "panjiang_produce_coal", "company_id": "panjiang", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.95},
        {"exposure_id": "panjiang_operate_coal_mining", "company_id": "panjiang", "node_id": "coal_mining", "activity_type": "operate", "role": "煤炭开采运营商", "weight": 0.9},
        {"exposure_id": "huadian_liaoning_operate_power_generation", "company_id": "huadian_liaoning", "node_id": "power_generation", "activity_type": "operate", "role": "火力发电运营商", "weight": 0.95},
        {"exposure_id": "huadian_liaoning_provide_service_heating_supply", "company_id": "huadian_liaoning", "node_id": "heating_supply", "activity_type": "provide_service", "role": "热力供应商", "weight": 0.9},
        {"exposure_id": "jiangtungsten_operate_coal_mining", "company_id": "jiangtungsten", "node_id": "coal_mining", "activity_type": "operate", "role": "煤炭开采运营商", "weight": 0.95},
        {"exposure_id": "jiangtungsten_operate_coal", "company_id": "jiangtungsten", "node_id": "coal", "activity_type": "operate", "role": "煤炭经营商", "weight": 0.9},
        {"exposure_id": "hla_operate_apparel", "company_id": "hla", "node_id": "apparel", "activity_type": "operate", "role": "服装品牌运营商", "weight": 0.95},
        {"exposure_id": "hla_operate_retail", "company_id": "hla", "node_id": "retail", "activity_type": "operate", "role": "零售运营商", "weight": 0.9},
        {"exposure_id": "fushun_special_steel_produce_alloy_structural_steel", "company_id": "fushun_special_steel", "node_id": "alloy_structural_steel", "activity_type": "produce", "role": "合金结构钢生产商", "weight": 0.95},
        {"exposure_id": "fushun_special_steel_produce_superalloy", "company_id": "fushun_special_steel", "node_id": "superalloy", "activity_type": "produce", "role": "高温合金生产商", "weight": 0.95},
        {"exposure_id": "fushun_special_steel_produce_stainless_steel", "company_id": "fushun_special_steel", "node_id": "stainless_steel", "activity_type": "produce", "role": "不锈钢生产商", "weight": 0.9},
        {"exposure_id": "fushun_special_steel_produce_steel", "company_id": "fushun_special_steel", "node_id": "steel", "activity_type": "produce", "role": "特钢生产商", "weight": 0.85},
        {"exposure_id": "hongdou_produce_apparel", "company_id": "hongdou", "node_id": "apparel", "activity_type": "produce", "role": "服装生产商", "weight": 0.95},
        {"exposure_id": "hongdou_produce_textile_product", "company_id": "hongdou", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.9},
        {"exposure_id": "dayou_energy_operate_coal", "company_id": "dayou_energy", "node_id": "coal", "activity_type": "operate", "role": "煤炭经营商", "weight": 0.95},
        {"exposure_id": "dayou_energy_operate_coal_mining", "company_id": "dayou_energy", "node_id": "coal_mining", "activity_type": "operate", "role": "煤炭开采运营商", "weight": 0.9},
    ],
}

BATCH_072 = {
    "new_nodes": [
        {"node_id": "telecom_power_supply", "canonical_name_zh": "通信电源", "definition": "为通信设备提供稳定电力的电源系统，包括开关电源、直流电源等", "entity_type": "device"},
        {"node_id": "photovoltaic_inverter", "canonical_name_zh": "光伏逆变器", "definition": "将太阳能电池板产生的直流电转换为交流电的电力电子设备", "entity_type": "device"},
        {"node_id": "power_grid_automation", "canonical_name_zh": "电网自动化", "definition": "利用计算机、通信和控制技术实现电力系统运行自动化的技术体系", "entity_type": "service"},
        {"node_id": "rail_transit_electrical", "canonical_name_zh": "轨道交通电气", "definition": "轨道交通系统中的电气设备与控制系统，包括牵引供电、信号控制等", "entity_type": "service"},
        {"node_id": "ac_motor", "canonical_name_zh": "交流电机", "definition": "利用交流电能产生旋转运动的电机，广泛应用于工业驱动和发电", "entity_type": "component"},
        {"node_id": "dc_motor", "canonical_name_zh": "直流电机", "definition": "利用直流电能产生旋转运动的电机，具有调速性能好的特点", "entity_type": "component"},
        {"node_id": "commercial_vehicle", "canonical_name_zh": "商用车", "definition": "用于商业运输目的的汽车，包括客车、货车、专用车等", "entity_type": "system"},
        {"node_id": "dairy_product", "canonical_name_zh": "乳制品", "definition": "以乳为主要原料加工制成的食品，包括液态奶、奶粉、酸奶、奶酪等", "entity_type": "material"},
        {"node_id": "antibiotic", "canonical_name_zh": "抗生素", "definition": "由微生物产生的能够抑制或杀灭其他微生物的化学物质，用于医疗抗感染治疗", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "telecom_power_supply_to_communication_equipment", "from_node": "telecom_power_supply", "to_node": "communication_equipment", "edge_type": "composition", "description": "通信电源为通信设备提供稳定电力供应，是其核心组成部分"},
        {"edge_id": "photovoltaic_inverter_to_solar_panel", "from_node": "photovoltaic_inverter", "to_node": "solar_panel", "edge_type": "composition", "description": "光伏逆变器是太阳能光伏发电系统的核心电力转换设备"},
        {"edge_id": "commercial_vehicle_to_automobile", "from_node": "commercial_vehicle", "to_node": "automobile", "edge_type": "composition", "description": "商用车是汽车整车的重要组成部分分类"},
    ],
    "companies": [
        {"company_id": "dianyuan", "name_zh": "北京动力源科技股份有限公司", "stock_code": "600405.SH", "province": "北京", "city": "北京市", "industry": "电气设备", "main_business": "通信电源,高压直流电源,工业电源,应急电源(EPS),不间断电源(UPS),光伏逆变器,高压变频器"},
        {"company_id": "nari", "name_zh": "国电南瑞科技股份有限公司", "stock_code": "600406.SH", "province": "江苏", "city": "南京市", "industry": "电气设备", "main_business": "电网调度自动化,变电站自动化,农村电网自动化,火电厂及工业控制自动化,轨道交通电气"},
        {"company_id": "antai", "name_zh": "山西安泰集团股份有限公司", "stock_code": "600408.SH", "province": "山西", "city": "介休市", "industry": "焦炭加工", "main_business": "煤炭洗选,焦炭,生铁,水泥及其制品,电力的生产与销售"},
        {"company_id": "sanyou_chem", "name_zh": "唐山三友化工股份有限公司", "stock_code": "600409.SH", "province": "河北", "city": "唐山市", "industry": "化纤", "main_business": "纯碱和氯化钙产品的生产与销售"},
        {"company_id": "teamsun", "name_zh": "北京华胜天成科技股份有限公司", "stock_code": "600410.SH", "province": "北京", "city": "北京市", "industry": "软件服务", "main_business": "系统产品及系统集成服务,软件及软件开发业务及专业服务"},
        {"company_id": "yiwu_market", "name_zh": "浙江中国小商品城集团股份有限公司", "stock_code": "600415.SH", "province": "浙江", "city": "义乌市", "industry": "商品城", "main_business": "市场网点经营,酒店服务,商品销售,房地产开发销售"},
        {"company_id": "xiangdian", "name_zh": "湘潭电机股份有限公司", "stock_code": "600416.SH", "province": "湖南", "city": "湘潭市", "industry": "电气设备", "main_business": "交流电机,直流电机,车辆,水泵"},
        {"company_id": "jac", "name_zh": "安徽江淮汽车集团股份有限公司", "stock_code": "600418.SH", "province": "安徽", "city": "合肥市", "industry": "汽车整车", "main_business": "商用车,乘用车及汽车底盘等"},
        {"company_id": "tianrun_dairy", "name_zh": "新疆天润乳业股份有限公司", "stock_code": "600419.SH", "province": "新疆", "city": "乌鲁木齐市", "industry": "乳制品", "main_business": "乳和乳制品,初乳素系列生物保健品"},
        {"company_id": "sinopharm_modern", "name_zh": "上海现代制药股份有限公司", "stock_code": "600420.SH", "province": "上海", "city": "上海市", "industry": "化学制药", "main_business": "抗生素,保肝类,降压类,生化品种"},
    ],
    "exposures": [
        {"exposure_id": "dianyuan_manufacture_telecom_power_supply", "company_id": "dianyuan", "node_id": "telecom_power_supply", "activity_type": "manufacture", "role": "通信电源制造商", "weight": 0.95},
        {"exposure_id": "dianyuan_manufacture_photovoltaic_inverter", "company_id": "dianyuan", "node_id": "photovoltaic_inverter", "activity_type": "manufacture", "role": "光伏逆变器制造商", "weight": 0.9},
        {"exposure_id": "dianyuan_manufacture_ups", "company_id": "dianyuan", "node_id": "ups", "activity_type": "manufacture", "role": "不间断电源制造商", "weight": 0.9},
        {"exposure_id": "dianyuan_manufacture_power_supply", "company_id": "dianyuan", "node_id": "power_supply", "activity_type": "manufacture", "role": "电源设备制造商", "weight": 0.85},
        {"exposure_id": "nari_provide_service_power_grid_automation", "company_id": "nari", "node_id": "power_grid_automation", "activity_type": "provide_service", "role": "电网自动化服务商", "weight": 0.95},
        {"exposure_id": "nari_provide_service_substation_automation", "company_id": "nari", "node_id": "substation_automation", "activity_type": "provide_service", "role": "变电站自动化服务商", "weight": 0.9},
        {"exposure_id": "nari_provide_service_rail_transit_electrical", "company_id": "nari", "node_id": "rail_transit_electrical", "activity_type": "provide_service", "role": "轨道交通电气服务商", "weight": 0.9},
        {"exposure_id": "nari_manufacture_power_distribution_equipment", "company_id": "nari", "node_id": "power_distribution_equipment", "activity_type": "manufacture", "role": "配电设备制造商", "weight": 0.85},
        {"exposure_id": "antai_produce_coke", "company_id": "antai", "node_id": "coke", "activity_type": "produce", "role": "焦炭生产商", "weight": 0.95},
        {"exposure_id": "antai_produce_pig_iron", "company_id": "antai", "node_id": "pig_iron", "activity_type": "produce", "role": "生铁生产商", "weight": 0.9},
        {"exposure_id": "antai_produce_cement", "company_id": "antai", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.9},
        {"exposure_id": "antai_operate_power_generation", "company_id": "antai", "node_id": "power_generation", "activity_type": "operate", "role": "发电运营商", "weight": 0.85},
        {"exposure_id": "sanyou_chem_produce_soda_ash", "company_id": "sanyou_chem", "node_id": "soda_ash", "activity_type": "produce", "role": "纯碱生产商", "weight": 0.95},
        {"exposure_id": "sanyou_chem_produce_chemical_product", "company_id": "sanyou_chem", "node_id": "chemical_product", "activity_type": "produce", "role": "化工产品生产商", "weight": 0.9},
        {"exposure_id": "teamsun_provide_service_software", "company_id": "teamsun", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.95},
        {"exposure_id": "teamsun_provide_service_system_integration", "company_id": "teamsun", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "teamsun_provide_service_it_service", "company_id": "teamsun", "node_id": "it_service", "activity_type": "provide_service", "role": "IT服务商", "weight": 0.9},
        {"exposure_id": "yiwu_market_operate_commodity_market", "company_id": "yiwu_market", "node_id": "commodity_market", "activity_type": "operate", "role": "商品市场运营商", "weight": 0.95},
        {"exposure_id": "yiwu_market_operate_real_estate_development", "company_id": "yiwu_market", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.85},
        {"exposure_id": "yiwu_market_operate_hotel_service", "company_id": "yiwu_market", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店服务商", "weight": 0.8},
        {"exposure_id": "xiangdian_manufacture_ac_motor", "company_id": "xiangdian", "node_id": "ac_motor", "activity_type": "manufacture", "role": "交流电机制造商", "weight": 0.95},
        {"exposure_id": "xiangdian_manufacture_dc_motor", "company_id": "xiangdian", "node_id": "dc_motor", "activity_type": "manufacture", "role": "直流电机制造商", "weight": 0.9},
        {"exposure_id": "xiangdian_manufacture_pump", "company_id": "xiangdian", "node_id": "pump", "activity_type": "manufacture", "role": "水泵制造商", "weight": 0.9},
        {"exposure_id": "jac_manufacture_commercial_vehicle", "company_id": "jac", "node_id": "commercial_vehicle", "activity_type": "manufacture", "role": "商用车制造商", "weight": 0.95},
        {"exposure_id": "jac_manufacture_passenger_car", "company_id": "jac", "node_id": "passenger_car", "activity_type": "manufacture", "role": "乘用车制造商", "weight": 0.9},
        {"exposure_id": "jac_manufacture_automobile", "company_id": "jac", "node_id": "automobile", "activity_type": "manufacture", "role": "汽车整车制造商", "weight": 0.95},
        {"exposure_id": "tianrun_dairy_produce_dairy_product", "company_id": "tianrun_dairy", "node_id": "dairy_product", "activity_type": "produce", "role": "乳制品生产商", "weight": 0.95},
        {"exposure_id": "tianrun_dairy_produce_food", "company_id": "tianrun_dairy", "node_id": "food", "activity_type": "produce", "role": "食品生产商", "weight": 0.85},
        {"exposure_id": "sinopharm_modern_produce_antibiotic", "company_id": "sinopharm_modern", "node_id": "antibiotic", "activity_type": "produce", "role": "抗生素生产商", "weight": 0.95},
        {"exposure_id": "sinopharm_modern_produce_pharmaceutical", "company_id": "sinopharm_modern", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
    ],
}

BATCH_073 = {
    "new_nodes": [
        {"node_id": "funeral_service", "canonical_name_zh": "殡葬服务", "definition": "为逝者提供遗体处理、安葬、悼念等服务的行业", "entity_type": "service"},
        {"node_id": "artemisinin_series", "canonical_name_zh": "蒿甲醚系列产品", "definition": "以青蒿素及其衍生物为主要成分的药物系列，主要用于抗疟疾治疗", "entity_type": "material"},
        {"node_id": "notoginseng_series", "canonical_name_zh": "三七系列产品", "definition": "以三七为主要原料的中药系列产品，具有活血化瘀功效", "entity_type": "material"},
        {"node_id": "nitric_acid", "canonical_name_zh": "硝酸", "definition": "一种重要的无机强酸，广泛用于制造化肥、炸药、染料等化工产品", "entity_type": "material"},
        {"node_id": "formaldehyde", "canonical_name_zh": "甲醛", "definition": "一种重要的有机化工原料，用于制造树脂、塑料、纤维等", "entity_type": "material"},
        {"node_id": "carbonless_paper", "canonical_name_zh": "无碳纸", "definition": "一种无需碳粉即可实现复写的特种纸张，用于多联票据", "entity_type": "material"},
        {"node_id": "navigation_control", "canonical_name_zh": "导航控制系统", "definition": "用于精确制导和导航控制的电子系统，广泛应用于军事和民用领域", "entity_type": "system"},
        {"node_id": "ammunition_info_system", "canonical_name_zh": "弹药信息化系统", "definition": "用于弹药制导、控制和信息传输的电子系统", "entity_type": "system"},
    ],
    "new_edges": [
        {"edge_id": "formaldehyde_to_chemical_product", "from_node": "formaldehyde", "to_node": "chemical_product", "edge_type": "material_flow", "description": "甲醛是重要的有机化工原料，用于生产多种化工产品"},
        {"edge_id": "nitric_acid_to_fertilizer", "from_node": "nitric_acid", "to_node": "fertilizer", "edge_type": "material_flow", "description": "硝酸是生产氮肥等化肥的重要原料"},
        {"edge_id": "navigation_control_to_defense_equipment", "from_node": "navigation_control", "to_node": "defense_equipment", "edge_type": "composition", "description": "导航控制系统是现代防务装备的核心组成部分"},
    ],
    "companies": [
        {"company_id": "st_huarong", "name_zh": "武汉华嵘控股股份有限公司", "stock_code": "600421.SH", "province": "湖北", "city": "武汉市", "industry": "专用机械", "main_business": "墓地销售代理,殡葬服务"},
        {"company_id": "kunyao_group", "name_zh": "昆药集团股份有限公司", "stock_code": "600422.SH", "province": "云南", "city": "昆明市", "industry": "中成药", "main_business": "蒿甲醚系列,三七系列,天麻素系列等中西药生产与销售"},
        {"company_id": "st_liuhua", "name_zh": "柳州化工股份有限公司", "stock_code": "600423.SH", "province": "广西", "city": "柳州市", "industry": "农药化肥", "main_business": "硝酸铵,尿素,浓硝酸,甲醛,精甲醇,纯碱,氯化铵及碳酸氢铵"},
        {"company_id": "qingsong_jianhua", "name_zh": "新疆青松建材化工(集团)股份有限公司", "stock_code": "600425.SH", "province": "新疆", "city": "阿拉尔市", "industry": "水泥", "main_business": "建材产品,水泥及水泥制品的生产和销售"},
        {"company_id": "hualu_hensheng", "name_zh": "山东华鲁恒升化工股份有限公司", "stock_code": "600426.SH", "province": "山东", "city": "德州市", "industry": "农药化肥", "main_business": "尿素,DMF,三甲胺及甲醛的生产和销售"},
        {"company_id": "cosco_specialized", "name_zh": "中远海运特种运输股份有限公司", "stock_code": "600428.SH", "province": "广东", "city": "广州市", "industry": "水运", "main_business": "航运业务"},
        {"company_id": "sanyuan", "name_zh": "北京三元食品股份有限公司", "stock_code": "600429.SH", "province": "北京", "city": "北京市", "industry": "乳制品", "main_business": "乳制品生产,加工,销售"},
        {"company_id": "guanhao", "name_zh": "广东冠豪高新技术股份有限公司", "stock_code": "600433.SH", "province": "广东", "city": "湛江市", "industry": "造纸", "main_business": "无碳纸的生产与销售"},
        {"company_id": "norinco_nav", "name_zh": "北方导航控制技术股份有限公司", "stock_code": "600435.SH", "province": "北京", "city": "北京市", "industry": "专用机械", "main_business": "导航控制,弹药信息化系统,短波电台和卫星通信系统,军用电连接器"},
        {"company_id": "pientzehuang", "name_zh": "漳州片仔癀药业股份有限公司", "stock_code": "600436.SH", "province": "福建", "city": "漳州市", "industry": "中成药", "main_business": "片仔癀及其系列产品"},
    ],
    "exposures": [
        {"exposure_id": "st_huarong_operate_funeral_service", "company_id": "st_huarong", "node_id": "funeral_service", "activity_type": "operate", "role": "殡葬服务运营商", "weight": 0.95},
        {"exposure_id": "st_huarong_operate_cemetery", "company_id": "st_huarong", "node_id": "cemetery", "activity_type": "operate", "role": "墓地运营商", "weight": 0.9},
        {"exposure_id": "kunyao_group_produce_artemisinin_series", "company_id": "kunyao_group", "node_id": "artemisinin_series", "activity_type": "produce", "role": "蒿甲醚系列产品生产商", "weight": 0.95},
        {"exposure_id": "kunyao_group_produce_notoginseng_series", "company_id": "kunyao_group", "node_id": "notoginseng_series", "activity_type": "produce", "role": "三七系列产品生产商", "weight": 0.9},
        {"exposure_id": "kunyao_group_produce_chinese_patent_medicine", "company_id": "kunyao_group", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9},
        {"exposure_id": "st_liuhua_produce_nitric_acid", "company_id": "st_liuhua", "node_id": "nitric_acid", "activity_type": "produce", "role": "硝酸生产商", "weight": 0.95},
        {"exposure_id": "st_liuhua_produce_urea", "company_id": "st_liuhua", "node_id": "urea", "activity_type": "produce", "role": "尿素生产商", "weight": 0.9},
        {"exposure_id": "st_liuhua_produce_formaldehyde", "company_id": "st_liuhua", "node_id": "formaldehyde", "activity_type": "produce", "role": "甲醛生产商", "weight": 0.9},
        {"exposure_id": "st_liuhua_produce_methanol", "company_id": "st_liuhua", "node_id": "methanol", "activity_type": "produce", "role": "甲醇生产商", "weight": 0.85},
        {"exposure_id": "qingsong_jianhua_produce_cement", "company_id": "qingsong_jianhua", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.95},
        {"exposure_id": "qingsong_jianhua_produce_building_material", "company_id": "qingsong_jianhua", "node_id": "building_material", "activity_type": "produce", "role": "建材生产商", "weight": 0.9},
        {"exposure_id": "hualu_hensheng_produce_urea", "company_id": "hualu_hensheng", "node_id": "urea", "activity_type": "produce", "role": "尿素生产商", "weight": 0.95},
        {"exposure_id": "hualu_hensheng_produce_formaldehyde", "company_id": "hualu_hensheng", "node_id": "formaldehyde", "activity_type": "produce", "role": "甲醛生产商", "weight": 0.9},
        {"exposure_id": "hualu_hensheng_produce_chemical_product", "company_id": "hualu_hensheng", "node_id": "chemical_product", "activity_type": "produce", "role": "化工产品生产商", "weight": 0.85},
        {"exposure_id": "cosco_specialized_operate_shipping", "company_id": "cosco_specialized", "node_id": "shipping", "activity_type": "operate", "role": "航运运营商", "weight": 0.95},
        {"exposure_id": "cosco_specialized_provide_service_logistics", "company_id": "cosco_specialized", "node_id": "logistics", "activity_type": "provide_service", "role": "物流服务商", "weight": 0.9},
        {"exposure_id": "sanyuan_produce_dairy_product", "company_id": "sanyuan", "node_id": "dairy_product", "activity_type": "produce", "role": "乳制品生产商", "weight": 0.95},
        {"exposure_id": "sanyuan_produce_food", "company_id": "sanyuan", "node_id": "food", "activity_type": "produce", "role": "食品生产商", "weight": 0.85},
        {"exposure_id": "guanhao_produce_carbonless_paper", "company_id": "guanhao", "node_id": "carbonless_paper", "activity_type": "produce", "role": "无碳纸生产商", "weight": 0.95},
        {"exposure_id": "guanhao_produce_paper", "company_id": "guanhao", "node_id": "paper", "activity_type": "produce", "role": "造纸商", "weight": 0.9},
        {"exposure_id": "norinco_nav_manufacture_navigation_control", "company_id": "norinco_nav", "node_id": "navigation_control", "activity_type": "manufacture", "role": "导航控制系统制造商", "weight": 0.95},
        {"exposure_id": "norinco_nav_manufacture_ammunition_info_system", "company_id": "norinco_nav", "node_id": "ammunition_info_system", "activity_type": "manufacture", "role": "弹药信息化系统制造商", "weight": 0.9},
        {"exposure_id": "norinco_nav_manufacture_special_vehicle", "company_id": "norinco_nav", "node_id": "special_vehicle", "activity_type": "manufacture", "role": "专用车制造商", "weight": 0.8},
        {"exposure_id": "pientzehuang_produce_chinese_patent_medicine", "company_id": "pientzehuang", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.95},
        {"exposure_id": "pientzehuang_produce_pharmaceutical", "company_id": "pientzehuang", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
    ],
}

BATCH_074 = {
    "new_nodes": [
        {"node_id": "aquatic_feed", "canonical_name_zh": "水产饲料", "definition": "用于水产养殖的专用饲料，包括鱼饲料、虾饲料、蟹饲料等", "entity_type": "material"},
        {"node_id": "polysilicon", "canonical_name_zh": "多晶硅", "definition": "纯度较高的硅材料，是制造太阳能电池和半导体器件的基础原料", "entity_type": "material"},
        {"node_id": "solar_cell", "canonical_name_zh": "太阳能电池", "definition": "将太阳能直接转换为电能的半导体器件，是光伏发电的核心组件", "entity_type": "component"},
        {"node_id": "wig", "canonical_name_zh": "假发饰品", "definition": "用人发或合成纤维制成的头发饰品，用于装饰或弥补脱发", "entity_type": "material"},
        {"node_id": "upvc_pipe", "canonical_name_zh": "UPVC双壁波纹管", "definition": "以硬质聚氯乙烯为原料制成的具有波纹结构的双壁塑料管道，用于排水和排污", "entity_type": "component"},
        {"node_id": "titanium_alloy", "canonical_name_zh": "钛合金", "definition": "以钛为基础加入其他元素组成的合金，具有高强度、耐腐蚀和耐高温特性", "entity_type": "material"},
        {"node_id": "polymer_damping_element", "canonical_name_zh": "高分子减振降噪弹性元件", "definition": "利用高分子材料的粘弹性特性实现减振降噪功能的弹性元件", "entity_type": "component"},
    ],
    "new_edges": [
        {"edge_id": "polysilicon_to_solar_cell", "from_node": "polysilicon", "to_node": "solar_cell", "edge_type": "material_flow", "description": "多晶硅是制造太阳能电池的核心原材料"},
        {"edge_id": "titanium_alloy_to_aircraft", "from_node": "titanium_alloy", "to_node": "aircraft", "edge_type": "material_flow", "description": "钛合金因其高强度和耐腐蚀性广泛用于航空航天器制造"},
        {"edge_id": "upvc_pipe_to_construction", "from_node": "upvc_pipe", "to_node": "construction", "edge_type": "material_flow", "description": "UPVC双壁波纹管是市政工程和建筑排水系统的重要管材"},
    ],
    "companies": [
        {"company_id": "tongwei", "name_zh": "通威股份有限公司", "stock_code": "600438.SH", "province": "四川", "city": "成都市", "industry": "电气设备", "main_business": "水产饲料,畜禽饲料等的研究,生产和销售,多晶硅,太阳能电池的研发,生产,销售"},
        {"company_id": "rebecca", "name_zh": "河南瑞贝卡发制品股份有限公司", "stock_code": "600439.SH", "province": "河南", "city": "许昌市", "industry": "服饰", "main_business": "工艺发条,化纤发,女装假发,教习头,男装头套等各种假发饰品"},
        {"company_id": "sinomach_tongyong", "name_zh": "国机通用机械科技股份有限公司", "stock_code": "600444.SH", "province": "安徽", "city": "合肥市", "industry": "专用机械", "main_business": "UPVC双壁波纹管,PE双壁波纹管"},
        {"company_id": "jinzheng", "name_zh": "深圳市金证科技股份有限公司", "stock_code": "600446.SH", "province": "广东", "city": "深圳市", "industry": "软件服务", "main_business": "系统集成,软件,硬件,系统维护,金融IT"},
        {"company_id": "huafang", "name_zh": "华纺股份有限公司", "stock_code": "600448.SH", "province": "山东", "city": "滨州市", "industry": "纺织", "main_business": "印染布,棉布,棉纱,毛条,毛纱,呢绒面料"},
        {"company_id": "ningxia_jiancai", "name_zh": "宁夏建材集团股份有限公司", "stock_code": "600449.SH", "province": "宁夏", "city": "银川市", "industry": "水泥", "main_business": "水泥,熟料,塑料管材的生产与销售"},
        {"company_id": "fuling_power", "name_zh": "重庆涪陵电力实业股份有限公司", "stock_code": "600452.SH", "province": "重庆", "city": "重庆市", "industry": "水力发电", "main_business": "电力供应与销售"},
        {"company_id": "botong", "name_zh": "西安博通资讯股份有限公司", "stock_code": "600455.SH", "province": "陕西", "city": "西安市", "industry": "文教休闲", "main_business": "定制软件,销售自制软件,系统集成,计算机设备销售"},
        {"company_id": "baoti", "name_zh": "宝鸡钛业股份有限公司", "stock_code": "600456.SH", "province": "陕西", "city": "宝鸡市", "industry": "小金属", "main_business": "各种规格的钛及钛合金板,带,箔,管,棒,线,锻件,铸件等加工材和各种金属复合材产品"},
        {"company_id": "tmt_newmaterial", "name_zh": "株洲时代新材料科技股份有限公司", "stock_code": "600458.SH", "province": "湖南", "city": "株洲市", "industry": "塑料", "main_business": "高分子减振降噪弹性元件,高分子复合改性材料,特种涂料,新型绝缘材料,桥梁支座,伸缩缝"},
    ],
    "exposures": [
        {"exposure_id": "tongwei_produce_aquatic_feed", "company_id": "tongwei", "node_id": "aquatic_feed", "activity_type": "produce", "role": "水产饲料生产商", "weight": 0.95},
        {"exposure_id": "tongwei_produce_livestock_feed", "company_id": "tongwei", "node_id": "livestock_feed", "activity_type": "produce", "role": "畜禽饲料生产商", "weight": 0.9},
        {"exposure_id": "tongwei_produce_polysilicon", "company_id": "tongwei", "node_id": "polysilicon", "activity_type": "produce", "role": "多晶硅生产商", "weight": 0.95},
        {"exposure_id": "tongwei_produce_solar_cell", "company_id": "tongwei", "node_id": "solar_cell", "activity_type": "produce", "role": "太阳能电池生产商", "weight": 0.95},
        {"exposure_id": "tongwei_produce_photovoltaic", "company_id": "tongwei", "node_id": "photovoltaic", "activity_type": "produce", "role": "光伏产品生产商", "weight": 0.9},
        {"exposure_id": "rebecca_produce_wig", "company_id": "rebecca", "node_id": "wig", "activity_type": "produce", "role": "假发饰品生产商", "weight": 0.95},
        {"exposure_id": "rebecca_produce_hair_product", "company_id": "rebecca", "node_id": "hair_product", "activity_type": "produce", "role": "发制品生产商", "weight": 0.9},
        {"exposure_id": "rebecca_produce_apparel_accessory", "company_id": "rebecca", "node_id": "apparel_accessory", "activity_type": "produce", "role": "服饰配饰生产商", "weight": 0.85},
        {"exposure_id": "sinomach_tongyong_manufacture_upvc_pipe", "company_id": "sinomach_tongyong", "node_id": "upvc_pipe", "activity_type": "manufacture", "role": "UPVC波纹管制造商", "weight": 0.95},
        {"exposure_id": "sinomach_tongyong_manufacture_pe_pipe", "company_id": "sinomach_tongyong", "node_id": "pe_pipe", "activity_type": "manufacture", "role": "PE波纹管制造商", "weight": 0.9},
        {"exposure_id": "sinomach_tongyong_manufacture_plastic_pipe", "company_id": "sinomach_tongyong", "node_id": "plastic_pipe", "activity_type": "manufacture", "role": "塑料管道制造商", "weight": 0.9},
        {"exposure_id": "jinzheng_provide_service_financial_it", "company_id": "jinzheng", "node_id": "financial_it", "activity_type": "provide_service", "role": "金融IT服务商", "weight": 0.95},
        {"exposure_id": "jinzheng_provide_service_software", "company_id": "jinzheng", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.9},
        {"exposure_id": "jinzheng_provide_service_system_integration", "company_id": "jinzheng", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "huafang_produce_printed_fabric", "company_id": "huafang", "node_id": "printed_fabric", "activity_type": "produce", "role": "印染布生产商", "weight": 0.9},
        {"exposure_id": "huafang_produce_cotton_yarn", "company_id": "huafang", "node_id": "cotton_yarn", "activity_type": "produce", "role": "棉纱生产商", "weight": 0.85},
        {"exposure_id": "huafang_produce_wool_fabric", "company_id": "huafang", "node_id": "wool_fabric", "activity_type": "produce", "role": "呢绒面料生产商", "weight": 0.85},
        {"exposure_id": "huafang_produce_textile_product", "company_id": "huafang", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.9},
        {"exposure_id": "ningxia_jiancai_produce_cement", "company_id": "ningxia_jiancai", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.95},
        {"exposure_id": "ningxia_jiancai_produce_plastic_pipe", "company_id": "ningxia_jiancai", "node_id": "plastic_pipe", "activity_type": "produce", "role": "塑料管材生产商", "weight": 0.85},
        {"exposure_id": "ningxia_jiancai_produce_building_material", "company_id": "ningxia_jiancai", "node_id": "building_material", "activity_type": "produce", "role": "建材生产商", "weight": 0.9},
        {"exposure_id": "fuling_power_operate_power_distribution", "company_id": "fuling_power", "node_id": "power_distribution", "activity_type": "operate", "role": "电力配供运营商", "weight": 0.95},
        {"exposure_id": "fuling_power_provide_service_power_supply", "company_id": "fuling_power", "node_id": "power_supply", "activity_type": "provide_service", "role": "电力供应服务商", "weight": 0.9},
        {"exposure_id": "botong_provide_service_software", "company_id": "botong", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.95},
        {"exposure_id": "botong_provide_service_system_integration", "company_id": "botong", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "baoti_produce_titanium_alloy", "company_id": "baoti", "node_id": "titanium_alloy", "activity_type": "produce", "role": "钛合金生产商", "weight": 0.95},
        {"exposure_id": "baoti_produce_nonferrous_metal", "company_id": "baoti", "node_id": "nonferrous_metal", "activity_type": "produce", "role": "有色金属生产商", "weight": 0.9},
        {"exposure_id": "baoti_produce_metal_composite", "company_id": "baoti", "node_id": "metal_composite", "activity_type": "produce", "role": "金属复合材料生产商", "weight": 0.85},
        {"exposure_id": "tmt_newmaterial_manufacture_polymer_damping_element", "company_id": "tmt_newmaterial", "node_id": "polymer_damping_element", "activity_type": "manufacture", "role": "高分子减振降噪元件制造商", "weight": 0.95},
        {"exposure_id": "tmt_newmaterial_manufacture_polymer_composite", "company_id": "tmt_newmaterial", "node_id": "polymer_composite", "activity_type": "manufacture", "role": "高分子复合材料制造商", "weight": 0.9},
        {"exposure_id": "tmt_newmaterial_manufacture_special_coating", "company_id": "tmt_newmaterial", "node_id": "special_coating", "activity_type": "manufacture", "role": "特种涂料制造商", "weight": 0.85},
    ],
}

BATCH_075 = {
    "new_nodes": [
        {"node_id": "precious_metal_functional_material", "canonical_name_zh": "贵金属特种功能材料", "definition": "以金、银、铂、钯等贵金属为基础，具有特殊电、磁、热、催化等功能特性的材料", "entity_type": "material"},
        {"node_id": "integrated_circuit", "canonical_name_zh": "集成电路", "definition": "将大量晶体管、电阻、电容等电子元件集成在半导体芯片上的电子器件", "entity_type": "component"},
        {"node_id": "semiconductor_discrete_device", "canonical_name_zh": "半导体分立器件", "definition": "具有单一功能的独立半导体器件，如二极管、三极管、晶闸管等", "entity_type": "component"},
        {"node_id": "led_product", "canonical_name_zh": "LED产品", "definition": "基于发光二极管技术的照明和显示产品，具有高效节能的特点", "entity_type": "component"},
        {"node_id": "water_supply", "canonical_name_zh": "自来水供应", "definition": "通过取水、净化、输配等工艺向城市居民和工业用户提供自来水的服务", "entity_type": "service"},
        {"node_id": "city_sewage_treatment", "canonical_name_zh": "城市污水处理", "definition": "对城市生活污水和工业废水进行收集、处理和排放的环保服务", "entity_type": "service"},
        {"node_id": "sea_cucumber", "canonical_name_zh": "海参", "definition": "一种珍贵的海洋棘皮动物，具有高营养和药用价值的海产品", "entity_type": "material"},
        {"node_id": "phosphate_fertilizer", "canonical_name_zh": "磷肥", "definition": "以磷酸盐为主要成分的化肥，为作物提供磷营养，促进根系发育和开花结果", "entity_type": "material"},
        {"node_id": "power_generation_equipment", "canonical_name_zh": "发电设备", "definition": "用于将各种能源转换为电能的机械设备和系统，包括锅炉、汽轮机、发电机等", "entity_type": "device"},
    ],
    "new_edges": [
        {"edge_id": "integrated_circuit_to_electronic_device", "from_node": "integrated_circuit", "to_node": "electronic_device", "edge_type": "composition", "description": "集成电路是电子设备和系统的核心组成部件"},
        {"edge_id": "led_product_to_lighting", "from_node": "led_product", "to_node": "lighting", "edge_type": "composition", "description": "LED产品是现代照明系统的核心发光组件"},
        {"edge_id": "power_generation_equipment_to_power_generation", "from_node": "power_generation_equipment", "to_node": "power_generation", "edge_type": "composition", "description": "发电设备是电力生产系统的核心装备组成"},
    ],
    "companies": [
        {"company_id": "sino_platinum", "name_zh": "贵研铂业股份有限公司", "stock_code": "600459.SH", "province": "云南", "city": "昆明市", "industry": "小金属", "main_business": "贵金属特种功能材料,环保及催化功能材料,信息功能材料,再生资源材料"},
        {"company_id": "silan", "name_zh": "杭州士兰微电子股份有限公司", "stock_code": "600460.SH", "province": "浙江", "city": "杭州市", "industry": "半导体", "main_business": "集成电路,半导体分立器件,LED(发光二极管)产品"},
        {"company_id": "hongcheng_env", "name_zh": "江西洪城环境股份有限公司", "stock_code": "600461.SH", "province": "江西", "city": "南昌市", "industry": "水务", "main_business": "自来水的生产和销售,城市污水处理,燃气能源"},
        {"company_id": "airport_co", "name_zh": "北京空港科技园区股份有限公司", "stock_code": "600463.SH", "province": "北京", "city": "北京市", "industry": "园区开发", "main_business": "园区开发建设,工业地产开发,建筑施工,物业经营与管理"},
        {"company_id": "haodangjia", "name_zh": "山东好当家海洋发展股份有限公司", "stock_code": "600467.SH", "province": "山东", "city": "威海市", "industry": "渔业", "main_business": "海参,牙鲆鱼,鲍鱼,海蛰等各种鲜活海产品和冷冻食品"},
        {"company_id": "baili_elec", "name_zh": "天津百利特精电气股份有限公司", "stock_code": "600468.SH", "province": "天津", "city": "天津市", "industry": "电气设备", "main_business": "输配电及控制设备,泵,钨钼制品"},
        {"company_id": "aeolus", "name_zh": "风神轮胎股份有限公司", "stock_code": "600469.SH", "province": "河南", "city": "焦作市", "industry": "汽车配件", "main_business": "斜交胎,全钢载重子午胎"},
        {"company_id": "liuguo_chem", "name_zh": "安徽六国化工股份有限公司", "stock_code": "600470.SH", "province": "安徽", "city": "铜陵市", "industry": "农药化肥", "main_business": "磷酸二铵"},
        {"company_id": "huaguang", "name_zh": "无锡华光环保能源集团股份有限公司", "stock_code": "600475.SH", "province": "江苏", "city": "无锡市", "industry": "电气设备", "main_business": "节能高效发电设备,环保新能源发电设备,环境工程,电站工程,地方能源供应"},
        {"company_id": "st_xiangyou", "name_zh": "湖南湘邮科技股份有限公司", "stock_code": "600476.SH", "province": "湖南", "city": "长沙市", "industry": "软件服务", "main_business": "系统集成,产品销售,房地产,软件,设计,邮政软件开发"},
    ],
    "exposures": [
        {"exposure_id": "sino_platinum_produce_precious_metal_functional_material", "company_id": "sino_platinum", "node_id": "precious_metal_functional_material", "activity_type": "produce", "role": "贵金属功能材料生产商", "weight": 0.95},
        {"exposure_id": "sino_platinum_produce_catalytic_functional_material", "company_id": "sino_platinum", "node_id": "catalytic_functional_material", "activity_type": "produce", "role": "催化功能材料生产商", "weight": 0.9},
        {"exposure_id": "sino_platinum_produce_nonferrous_metal", "company_id": "sino_platinum", "node_id": "nonferrous_metal", "activity_type": "produce", "role": "有色金属生产商", "weight": 0.9},
        {"exposure_id": "silan_manufacture_integrated_circuit", "company_id": "silan", "node_id": "integrated_circuit", "activity_type": "manufacture", "role": "集成电路制造商", "weight": 0.95},
        {"exposure_id": "silan_manufacture_semiconductor_discrete_device", "company_id": "silan", "node_id": "semiconductor_discrete_device", "activity_type": "manufacture", "role": "半导体分立器件制造商", "weight": 0.9},
        {"exposure_id": "silan_manufacture_led_product", "company_id": "silan", "node_id": "led_product", "activity_type": "manufacture", "role": "LED产品制造商", "weight": 0.9},
        {"exposure_id": "silan_manufacture_electronic_component", "company_id": "silan", "node_id": "electronic_component", "activity_type": "manufacture", "role": "电子元器件制造商", "weight": 0.85},
        {"exposure_id": "hongcheng_env_provide_service_water_supply", "company_id": "hongcheng_env", "node_id": "water_supply", "activity_type": "provide_service", "role": "自来水供应商", "weight": 0.95},
        {"exposure_id": "hongcheng_env_operate_city_sewage_treatment", "company_id": "hongcheng_env", "node_id": "city_sewage_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.9},
        {"exposure_id": "hongcheng_env_provide_service_gas_energy", "company_id": "hongcheng_env", "node_id": "gas_energy", "activity_type": "provide_service", "role": "燃气能源供应商", "weight": 0.85},
        {"exposure_id": "airport_co_operate_industrial_park", "company_id": "airport_co", "node_id": "industrial_park", "activity_type": "operate", "role": "产业园区运营商", "weight": 0.95},
        {"exposure_id": "airport_co_operate_real_estate_development", "company_id": "airport_co", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.9},
        {"exposure_id": "airport_co_operate_construction", "company_id": "airport_co", "node_id": "construction", "activity_type": "operate", "role": "建筑施工运营商", "weight": 0.85},
        {"exposure_id": "haodangjia_produce_sea_cucumber", "company_id": "haodangjia", "node_id": "sea_cucumber", "activity_type": "produce", "role": "海参生产商", "weight": 0.95},
        {"exposure_id": "haodangjia_produce_seafood", "company_id": "haodangjia", "node_id": "seafood", "activity_type": "produce", "role": "海产品生产商", "weight": 0.9},
        {"exposure_id": "haodangjia_operate_aquaculture", "company_id": "haodangjia", "node_id": "aquaculture", "activity_type": "operate", "role": "水产养殖运营商", "weight": 0.9},
        {"exposure_id": "baili_elec_manufacture_power_distribution_equipment", "company_id": "baili_elec", "node_id": "power_distribution_equipment", "activity_type": "manufacture", "role": "输配电设备制造商", "weight": 0.95},
        {"exposure_id": "baili_elec_manufacture_pump", "company_id": "baili_elec", "node_id": "pump", "activity_type": "manufacture", "role": "水泵制造商", "weight": 0.9},
        {"exposure_id": "baili_elec_produce_tungsten_molybdenum_product", "company_id": "baili_elec", "node_id": "tungsten_molybdenum_product", "activity_type": "produce", "role": "钨钼制品生产商", "weight": 0.85},
        {"exposure_id": "aeolus_manufacture_tire", "company_id": "aeolus", "node_id": "tire", "activity_type": "manufacture", "role": "轮胎制造商", "weight": 0.95},
        {"exposure_id": "aeolus_manufacture_automobile_part", "company_id": "aeolus", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车零部件制造商", "weight": 0.9},
        {"exposure_id": "liuguo_chem_produce_phosphate_fertilizer", "company_id": "liuguo_chem", "node_id": "phosphate_fertilizer", "activity_type": "produce", "role": "磷肥生产商", "weight": 0.95},
        {"exposure_id": "liuguo_chem_produce_chemical_product", "company_id": "liuguo_chem", "node_id": "chemical_product", "activity_type": "produce", "role": "化工产品生产商", "weight": 0.9},
        {"exposure_id": "huaguang_manufacture_power_generation_equipment", "company_id": "huaguang", "node_id": "power_generation_equipment", "activity_type": "manufacture", "role": "发电设备制造商", "weight": 0.95},
        {"exposure_id": "huaguang_manufacture_environmental_equipment", "company_id": "huaguang", "node_id": "environmental_equipment", "activity_type": "manufacture", "role": "环保设备制造商", "weight": 0.9},
        {"exposure_id": "huaguang_provide_service_energy_supply", "company_id": "huaguang", "node_id": "energy_supply", "activity_type": "provide_service", "role": "能源供应服务商", "weight": 0.85},
        {"exposure_id": "st_xiangyou_provide_service_software", "company_id": "st_xiangyou", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.95},
        {"exposure_id": "st_xiangyou_provide_service_system_integration", "company_id": "st_xiangyou", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "st_xiangyou_manufacture_postal_equipment", "company_id": "st_xiangyou", "node_id": "postal_equipment", "activity_type": "manufacture", "role": "邮政设备制造商", "weight": 0.85},
    ],
}

ALL_BATCHES = {
    71: BATCH_071,
    72: BATCH_072,
    73: BATCH_073,
    74: BATCH_074,
    75: BATCH_075,
}

os.makedirs("tmp_script", exist_ok=True)

for nnn, data in ALL_BATCHES.items():
    content = TEMPLATE
    content = content.replace("%%NNN%%", f"{nnn:03d}")
    content = content.replace("%%NEW_NODES%%", json.dumps(data["new_nodes"], ensure_ascii=False, indent=4))
    content = content.replace("%%NEW_EDGES%%", json.dumps(data["new_edges"], ensure_ascii=False, indent=4))
    content = content.replace("%%COMPANIES%%", json.dumps(data["companies"], ensure_ascii=False, indent=4))
    content = content.replace("%%EXPOSURES%%", json.dumps(data["exposures"], ensure_ascii=False, indent=4))
    path = f"tmp_script/tmp_submit_batch_{nnn:03d}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {path}")

print("\nAll 5 scripts generated.")
