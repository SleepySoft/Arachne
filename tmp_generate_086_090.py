#!/usr/bin/env python3
"""Generate tmp_submit_batch_086.py through tmp_submit_batch_090.py."""
import json, os

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

BATCH_086 = {
    "new_nodes": [
        {"node_id": "rice", "canonical_name_zh": "大米", "definition": "稻谷经清理、砻谷、碾米等工序加工后制成的成品粮，是人类主要粮食作物之一", "entity_type": "material"},
        {"node_id": "fireworks", "canonical_name_zh": "烟花", "definition": "以火药为主要原料，点燃后能产生光、色、声、形等效果的娱乐观赏用品", "entity_type": "material"},
        {"node_id": "pcb_product", "canonical_name_zh": "PCB产品", "definition": "印制电路板及其相关产品，用于电子元器件的电气连接和机械支撑", "entity_type": "component"},
        {"node_id": "consumer_electronics", "canonical_name_zh": "消费电子", "definition": "供个人和家庭日常使用的电子设备，包括智能手机、平板电脑、智能穿戴等", "entity_type": "device"},
        {"node_id": "intelligent_security", "canonical_name_zh": "智能安防", "definition": "利用人工智能、物联网等技术实现的安全监控和防护系统", "entity_type": "system"},
        {"node_id": "logistics_park", "canonical_name_zh": "物流园区", "definition": "集中建设物流设施和企业的专业化园区，提供仓储、运输、配送等综合服务", "entity_type": "infrastructure"},
        {"node_id": "wind_power", "canonical_name_zh": "风力发电", "definition": "利用风力驱动风电机组旋转产生电能的可再生能源发电方式", "entity_type": "service"},
        {"node_id": "copper_trade", "canonical_name_zh": "铜贸易", "definition": "从事铜及铜制品的批发、零售和进出口贸易业务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "rice_to_food", "from_node": "rice", "to_node": "food", "edge_type": "material_flow", "description": "大米是人类主食粮食，是重要的食品原料"},
        {"edge_id": "pcb_product_to_electronic_device", "from_node": "pcb_product", "to_node": "electronic_device", "edge_type": "composition", "description": "PCB印制电路板是电子设备中实现电路连接的核心基础部件"},
        {"edge_id": "wind_power_to_power_generation", "from_node": "wind_power", "to_node": "power_generation", "edge_type": "service_flow", "description": "风力发电是可再生能源电力生产的重要方式"},
    ],
    "companies": [
        {"company_id": "bright_dairy", "name_zh": "光明乳业股份有限公司", "stock_code": "600597.SH", "province": "上海", "city": "上海市", "industry": "乳制品", "main_business": "乳制品等,商业"},
        {"company_id": "beidahuang", "name_zh": "黑龙江北大荒农业股份有限公司", "stock_code": "600598.SH", "province": "黑龙江", "city": "哈尔滨市", "industry": "种植业", "main_business": "大米销售,种植业"},
        {"company_id": "st_panda", "name_zh": "熊猫金控股份有限公司", "stock_code": "600599.SH", "province": "湖南", "city": "长沙市", "industry": "化工原料", "main_business": "烟花生产销售以及烟花燃放"},
        {"company_id": "tsingtao", "name_zh": "青岛啤酒股份有限公司", "stock_code": "600600.SH", "province": "山东", "city": "青岛市", "industry": "啤酒", "main_business": "啤酒的生产与销售"},
        {"company_id": "founder_tech", "name_zh": "方正科技集团股份有限公司", "stock_code": "600601.SH", "province": "广东", "city": "珠海市", "industry": "元器件", "main_business": "电子计算机及配件,系统集成,办公设备及消耗材料,PCB产品"},
        {"company_id": "cloud_intelligence", "name_zh": "云赛智联股份有限公司", "stock_code": "600602.SH", "province": "上海", "city": "上海市", "industry": "软件服务", "main_business": "消费电子,特殊电子,智能安防三大产业"},
        {"company_id": "guanghui_logistics", "name_zh": "广汇物流股份有限公司", "stock_code": "600603.SH", "province": "新疆", "city": "乌鲁木齐市", "industry": "区域地产", "main_business": "物流园区投资,经营及配套服务以及北站物流基地项目建设"},
        {"company_id": "shibei", "name_zh": "上海市北高新股份有限公司", "stock_code": "600604.SH", "province": "上海", "city": "上海市", "industry": "园区开发", "main_business": "企业管理,投资管理,房地产开发经营,自有房屋出租,商务信息咨询"},
        {"company_id": "huitong", "name_zh": "上海汇通能源股份有限公司", "stock_code": "600605.SH", "province": "上海", "city": "上海市", "industry": "房产服务", "main_business": "风力发电,有色金属(铜)批发贸易及房产租赁物业管理"},
        {"company_id": "greenland", "name_zh": "绿地控股集团股份有限公司", "stock_code": "600606.SH", "province": "上海", "city": "上海市", "industry": "全国地产", "main_business": "住宅流通业务,住宅开发业务,住宅配套服务"},
    ],
    "exposures": [
        {"exposure_id": "bright_dairy_produce_dairy_product", "company_id": "bright_dairy", "node_id": "dairy_product", "activity_type": "produce", "role": "乳制品生产商", "weight": 0.95},
        {"exposure_id": "bright_dairy_produce_food", "company_id": "bright_dairy", "node_id": "food", "activity_type": "produce", "role": "食品生产商", "weight": 0.9},
        {"exposure_id": "beidahuang_produce_rice", "company_id": "beidahuang", "node_id": "rice", "activity_type": "produce", "role": "大米生产商", "weight": 0.95},
        {"exposure_id": "beidahuang_produce_agricultural_product", "company_id": "beidahuang", "node_id": "agricultural_product", "activity_type": "produce", "role": "农产品生产商", "weight": 0.9},
        {"exposure_id": "st_panda_produce_fireworks", "company_id": "st_panda", "node_id": "fireworks", "activity_type": "produce", "role": "烟花生产商", "weight": 0.95},
        {"exposure_id": "st_panda_operate_entertainment", "company_id": "st_panda", "node_id": "entertainment", "activity_type": "operate", "role": "烟花燃放运营商", "weight": 0.9},
        {"exposure_id": "tsingtao_produce_beer", "company_id": "tsingtao", "node_id": "beer", "activity_type": "produce", "role": "啤酒生产商", "weight": 0.95},
        {"exposure_id": "tsingtao_produce_beverage", "company_id": "tsingtao", "node_id": "beverage", "activity_type": "produce", "role": "饮料生产商", "weight": 0.9},
        {"exposure_id": "founder_tech_manufacture_pcb_product", "company_id": "founder_tech", "node_id": "pcb_product", "activity_type": "manufacture", "role": "PCB产品制造商", "weight": 0.95},
        {"exposure_id": "founder_tech_manufacture_computer", "company_id": "founder_tech", "node_id": "computer", "activity_type": "manufacture", "role": "计算机制造商", "weight": 0.9},
        {"exposure_id": "founder_tech_provide_service_system_integration", "company_id": "founder_tech", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "cloud_intelligence_produce_consumer_electronics", "company_id": "cloud_intelligence", "node_id": "consumer_electronics", "activity_type": "produce", "role": "消费电子生产商", "weight": 0.95},
        {"exposure_id": "cloud_intelligence_provide_service_intelligent_security", "company_id": "cloud_intelligence", "node_id": "intelligent_security", "activity_type": "provide_service", "role": "智能安防服务商", "weight": 0.95},
        {"exposure_id": "cloud_intelligence_provide_service_software", "company_id": "cloud_intelligence", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.9},
        {"exposure_id": "guanghui_logistics_operate_logistics_park", "company_id": "guanghui_logistics", "node_id": "logistics_park", "activity_type": "operate", "role": "物流园区运营商", "weight": 0.95},
        {"exposure_id": "guanghui_logistics_provide_service_logistics", "company_id": "guanghui_logistics", "node_id": "logistics", "activity_type": "provide_service", "role": "物流服务商", "weight": 0.9},
        {"exposure_id": "shibei_operate_real_estate_development", "company_id": "shibei", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "shibei_operate_investment_management", "company_id": "shibei", "node_id": "investment_management", "activity_type": "operate", "role": "投资管理运营商", "weight": 0.85},
        {"exposure_id": "huitong_operate_wind_power", "company_id": "huitong", "node_id": "wind_power", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.95},
        {"exposure_id": "huitong_operate_power_generation", "company_id": "huitong", "node_id": "power_generation", "activity_type": "operate", "role": "发电运营商", "weight": 0.9},
        {"exposure_id": "huitong_operate_copper_trade", "company_id": "huitong", "node_id": "copper_trade", "activity_type": "operate", "role": "铜贸易商", "weight": 0.85},
        {"exposure_id": "greenland_operate_real_estate_development", "company_id": "greenland", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "greenland_operate_residential_circulation", "company_id": "greenland", "node_id": "residential_circulation", "activity_type": "operate", "role": "住宅流通运营商", "weight": 0.9},
        {"exposure_id": "greenland_provide_service_property_management", "company_id": "greenland", "node_id": "property_management", "activity_type": "provide_service", "role": "物业管理服务商", "weight": 0.85},
    ],
}

BATCH_087 = {
    "new_nodes": [
        {"node_id": "garden_design", "canonical_name_zh": "园林设计", "definition": "对园林景观进行规划、设计和营造的专业技术服务，包括植物配置、地形塑造、水景设计等", "entity_type": "service"},
        {"node_id": "transportation", "canonical_name_zh": "运输业", "definition": "利用各种运输工具实现人或货物空间位移的服务行业", "entity_type": "service"},
        {"node_id": "gold_jewelry", "canonical_name_zh": "黄金珠宝首饰", "definition": "以黄金为主要材质，配以宝石、珍珠等装饰制作的首饰饰品", "entity_type": "material"},
        {"node_id": "natural_gas_pipeline", "canonical_name_zh": "天然气长输管道", "definition": "用于长距离输送天然气的压力管道系统，包括输气干线、支线及配套设施", "entity_type": "infrastructure"},
        {"node_id": "city_gas", "canonical_name_zh": "城市燃气", "definition": "通过城市管网向居民、工商业用户供应的天然气、液化石油气等燃气", "entity_type": "service"},
        {"node_id": "polyvinyl_chloride", "canonical_name_zh": "聚氯乙烯", "definition": "由氯乙烯单体聚合而成的热塑性树脂，广泛用于制造管材、型材、薄膜等塑料制品", "entity_type": "material"},
        {"node_id": "caustic_soda", "canonical_name_zh": "烧碱", "definition": "氢氧化钠的工业名称，是重要的基础化工原料，广泛用于造纸、纺织、洗涤剂等行业", "entity_type": "material"},
        {"node_id": "chlorine_product", "canonical_name_zh": "氯产品", "definition": "以氯气为原料生产的各类化工产品，包括含氯溶剂、含氯农药、漂白剂等", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "natural_gas_pipeline_to_city_gas", "from_node": "natural_gas_pipeline", "to_node": "city_gas", "edge_type": "capability_supply", "description": "天然气长输管道为城市燃气供应提供气源输送能力"},
        {"edge_id": "polyvinyl_chloride_to_plastic", "from_node": "polyvinyl_chloride", "to_node": "plastic", "edge_type": "material_flow", "description": "聚氯乙烯是生产塑料制品的重要基础树脂原料"},
        {"edge_id": "caustic_soda_to_chemical_industry", "from_node": "caustic_soda", "to_node": "chemical_industry", "edge_type": "material_flow", "description": "烧碱是化工、造纸、纺织等众多行业的基础原料"},
    ],
    "companies": [
        {"company_id": "st_huke", "name_zh": "上海宽频科技股份有限公司", "stock_code": "600608.SH", "province": "上海", "city": "上海市", "industry": "商贸代理", "main_business": "有色金属,黑色金属,化工原料及生产生活物资等"},
        {"company_id": "jinbei_auto", "name_zh": "沈阳金杯汽车股份有限公司", "stock_code": "600609.SH", "province": "辽宁", "city": "沈阳市", "industry": "汽车配件", "main_business": "汽车及零部件制造"},
        {"company_id": "zhongyida", "name_zh": "上海中毅达股份有限公司", "stock_code": "600610.SH", "province": "上海", "city": "上海市", "industry": "化工原料", "main_business": "园林设计工程"},
        {"company_id": "dazhong_transport", "name_zh": "大众交通(集团)股份有限公司", "stock_code": "600611.SH", "province": "上海", "city": "上海市", "industry": "公共交通", "main_business": "运输业,旅游饮食,服务业,商业,工业"},
        {"company_id": "laofengxiang", "name_zh": "老凤祥股份有限公司", "stock_code": "600612.SH", "province": "上海", "city": "上海市", "industry": "服饰", "main_business": "黄金珠宝首饰,工艺美术品,笔类文具制品的生产经营及销售"},
        {"company_id": "shenqi", "name_zh": "上海神奇制药投资管理股份有限公司", "stock_code": "600613.SH", "province": "上海", "city": "上海市", "industry": "中成药", "main_business": "医药领域投资管理"},
        {"company_id": "xinyuan", "name_zh": "鑫源智造(上海)股份有限公司", "stock_code": "600615.SH", "province": "上海", "city": "上海市", "industry": "铝", "main_business": "涂料,制笔"},
        {"company_id": "jinfeng_wine", "name_zh": "上海金枫酒业股份有限公司", "stock_code": "600616.SH", "province": "上海", "city": "上海市", "industry": "红黄酒", "main_business": "食品销售管理,酒,仓储货运,租赁,出口业务"},
        {"company_id": "guoxin_energy", "name_zh": "山西省国新能源股份有限公司", "stock_code": "600617.SH", "province": "山西", "city": "太原市", "industry": "供气供热", "main_business": "天然气长输管道及城市燃气管网的建设和运营"},
        {"company_id": "chlor_alkali", "name_zh": "上海氯碱化工股份有限公司", "stock_code": "600618.SH", "province": "上海", "city": "上海市", "industry": "化工原料", "main_business": "聚氯乙烯,烧碱,氯产品,粒料及其他"},
    ],
    "exposures": [
        {"exposure_id": "st_huke_trade_nonferrous_metal", "company_id": "st_huke", "node_id": "nonferrous_metal", "activity_type": "procure", "role": "有色金属贸易商", "weight": 0.95},
        {"exposure_id": "st_huke_trade_ferrous_metal", "company_id": "st_huke", "node_id": "ferrous_metal", "activity_type": "procure", "role": "黑色金属贸易商", "weight": 0.9},
        {"exposure_id": "st_huke_trade_chemical_product", "company_id": "st_huke", "node_id": "chemical_product", "activity_type": "procure", "role": "化工原料贸易商", "weight": 0.9},
        {"exposure_id": "jinbei_auto_manufacture_automobile", "company_id": "jinbei_auto", "node_id": "automobile", "activity_type": "manufacture", "role": "汽车制造商", "weight": 0.95},
        {"exposure_id": "jinbei_auto_manufacture_automobile_part", "company_id": "jinbei_auto", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车零部件制造商", "weight": 0.95},
        {"exposure_id": "zhongyida_provide_service_garden_design", "company_id": "zhongyida", "node_id": "garden_design", "activity_type": "provide_service", "role": "园林设计服务商", "weight": 0.95},
        {"exposure_id": "zhongyida_operate_construction", "company_id": "zhongyida", "node_id": "construction", "activity_type": "operate", "role": "园林工程运营商", "weight": 0.9},
        {"exposure_id": "dazhong_transport_operate_transportation", "company_id": "dazhong_transport", "node_id": "transportation", "activity_type": "operate", "role": "运输业运营商", "weight": 0.95},
        {"exposure_id": "dazhong_transport_operate_tourism_catering", "company_id": "dazhong_transport", "node_id": "tourism_catering", "activity_type": "operate", "role": "旅游饮食运营商", "weight": 0.85},
        {"exposure_id": "dazhong_transport_operate_passenger_transport", "company_id": "dazhong_transport", "node_id": "passenger_transport", "activity_type": "operate", "role": "客运运营商", "weight": 0.9},
        {"exposure_id": "laofengxiang_produce_gold_jewelry", "company_id": "laofengxiang", "node_id": "gold_jewelry", "activity_type": "produce", "role": "黄金珠宝首饰生产商", "weight": 0.95},
        {"exposure_id": "laofengxiang_produce_arts_and_crafts", "company_id": "laofengxiang", "node_id": "arts_and_crafts", "activity_type": "produce", "role": "工艺美术品生产商", "weight": 0.85},
        {"exposure_id": "laofengxiang_produce_pen", "company_id": "laofengxiang", "node_id": "pen", "activity_type": "produce", "role": "笔类文具制品生产商", "weight": 0.8},
        {"exposure_id": "shenqi_produce_pharmaceutical", "company_id": "shenqi", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.95},
        {"exposure_id": "shenqi_operate_investment_management", "company_id": "shenqi", "node_id": "investment_management", "activity_type": "operate", "role": "医药投资运营商", "weight": 0.85},
        {"exposure_id": "xinyuan_produce_coating", "company_id": "xinyuan", "node_id": "coating", "activity_type": "produce", "role": "涂料生产商", "weight": 0.95},
        {"exposure_id": "xinyuan_manufacture_pen", "company_id": "xinyuan", "node_id": "pen", "activity_type": "manufacture", "role": "制笔制造商", "weight": 0.9},
        {"exposure_id": "jinfeng_wine_produce_liquor", "company_id": "jinfeng_wine", "node_id": "liquor", "activity_type": "produce", "role": "酒类生产商", "weight": 0.95},
        {"exposure_id": "jinfeng_wine_provide_service_warehousing", "company_id": "jinfeng_wine", "node_id": "warehousing", "activity_type": "provide_service", "role": "仓储货运服务商", "weight": 0.85},
        {"exposure_id": "guoxin_energy_operate_natural_gas_pipeline", "company_id": "guoxin_energy", "node_id": "natural_gas_pipeline", "activity_type": "operate", "role": "天然气长输管道运营商", "weight": 0.95},
        {"exposure_id": "guoxin_energy_operate_city_gas", "company_id": "guoxin_energy", "node_id": "city_gas", "activity_type": "operate", "role": "城市燃气运营商", "weight": 0.95},
        {"exposure_id": "guoxin_energy_provide_service_heating_supply", "company_id": "guoxin_energy", "node_id": "heating_supply", "activity_type": "provide_service", "role": "供热供应商", "weight": 0.85},
        {"exposure_id": "chlor_alkali_produce_polyvinyl_chloride", "company_id": "chlor_alkali", "node_id": "polyvinyl_chloride", "activity_type": "produce", "role": "聚氯乙烯生产商", "weight": 0.95},
        {"exposure_id": "chlor_alkali_produce_caustic_soda", "company_id": "chlor_alkali", "node_id": "caustic_soda", "activity_type": "produce", "role": "烧碱生产商", "weight": 0.95},
        {"exposure_id": "chlor_alkali_produce_chlorine_product", "company_id": "chlor_alkali", "node_id": "chlorine_product", "activity_type": "produce", "role": "氯产品生产商", "weight": 0.9},
        {"exposure_id": "chlor_alkali_produce_chemical_product", "company_id": "chlor_alkali", "node_id": "chemical_product", "activity_type": "produce", "role": "化工产品生产商", "weight": 0.85},
    ],
}

BATCH_088 = {
    "new_nodes": [
        {"node_id": "air_conditioner_compressor", "canonical_name_zh": "空调压缩机", "definition": "空调系统中用于压缩和输送制冷剂蒸汽的核心部件，是实现制冷循环的关键设备", "entity_type": "component"},
        {"node_id": "heat_pump", "canonical_name_zh": "热泵", "definition": "利用逆卡诺循环原理将低温热源热量转移到高温热源的节能装置，可用于供暖和热水", "entity_type": "device"},
        {"node_id": "capacitor", "canonical_name_zh": "电容器", "definition": "储存电荷的无源电子元件，用于电路中的滤波、耦合、储能等功能", "entity_type": "component"},
        {"node_id": "automotive_interior", "canonical_name_zh": "汽车内饰", "definition": "汽车内部装饰和功能性部件的总称，包括座椅、仪表板、地毯等", "entity_type": "material"},
        {"node_id": "textile_new_material", "canonical_name_zh": "纺织新材料", "definition": "采用新型纤维或特殊工艺制成的高性能纺织品材料，具有功能性或环保特性", "entity_type": "material"},
        {"node_id": "engineering_survey", "canonical_name_zh": "工程勘察", "definition": "为工程建设提供地质、水文、地形等基础资料的专业技术服务", "entity_type": "service"},
        {"node_id": "municipal_design", "canonical_name_zh": "市政设计", "definition": "对城市道路、桥梁、给排水、燃气等市政基础设施进行规划设计的专业服务", "entity_type": "service"},
        {"node_id": "apparel_brand", "canonical_name_zh": "服饰品牌", "definition": "具有市场认知度和品牌价值的服装服饰经营品牌，涵盖设计、生产、销售等环节", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "air_conditioner_compressor_to_air_conditioner", "from_node": "air_conditioner_compressor", "to_node": "air_conditioner", "edge_type": "composition", "description": "空调压缩机是空调制冷系统的核心动力部件"},
        {"edge_id": "capacitor_to_electronic_device", "from_node": "capacitor", "to_node": "electronic_device", "edge_type": "composition", "description": "电容器是电子设备中储存和调节电能的基础元件"},
        {"edge_id": "tire_to_automobile", "from_node": "tire", "to_node": "automobile", "edge_type": "composition", "description": "轮胎是汽车行走系统的关键部件"},
    ],
    "companies": [
        {"company_id": "highly", "name_zh": "上海海立(集团)股份有限公司", "stock_code": "600619.SH", "province": "上海", "city": "上海市", "industry": "家用电器", "main_business": "研发,生产和销售空调压缩机,热泵及热泵热水器压缩机"},
        {"company_id": "tianchen", "name_zh": "上海市天宸股份有限公司", "stock_code": "600620.SH", "province": "上海", "city": "上海市", "industry": "综合类", "main_business": "房地产,物业管理,运输及客运"},
        {"company_id": "huaxin", "name_zh": "上海华鑫股份有限公司", "stock_code": "600621.SH", "province": "上海", "city": "上海市", "industry": "证券", "main_business": "证券业务为主,少量持有型物业为辅"},
        {"company_id": "everbright_jiabao", "name_zh": "光大嘉宝股份有限公司", "stock_code": "600622.SH", "province": "上海", "city": "上海市", "industry": "区域地产", "main_business": "商品房,电容器"},
        {"company_id": "huayi", "name_zh": "上海华谊集团股份有限公司", "stock_code": "600623.SH", "province": "上海", "city": "上海市", "industry": "化工原料", "main_business": "轮胎"},
        {"company_id": "st_fuhua", "name_zh": "上海复旦复华科技股份有限公司", "stock_code": "600624.SH", "province": "上海", "city": "上海市", "industry": "化学制药", "main_business": "制造业,园区房地产,软件开发"},
        {"company_id": "shenda", "name_zh": "上海申达股份有限公司", "stock_code": "600626.SH", "province": "上海", "city": "上海市", "industry": "汽车配件", "main_business": "汽车内饰和纺织新材料业务,以及纺织品为主的外贸进出口和国内贸易"},
        {"company_id": "new_world", "name_zh": "上海新世界股份有限公司", "stock_code": "600628.SH", "province": "上海", "city": "上海市", "industry": "百货", "main_business": "商业"},
        {"company_id": "arcplus", "name_zh": "华东建筑集团股份有限公司", "stock_code": "600629.SH", "province": "上海", "city": "上海市", "industry": "建筑工程", "main_business": "工程勘察,规划设计,工程设计,市政设计,水利工程设计,风景园林设计"},
        {"company_id": "dragon_head", "name_zh": "上海龙头(集团)股份有限公司", "stock_code": "600630.SH", "province": "上海", "city": "上海市", "industry": "服饰", "main_business": "三枪,苏牌,菊花,鹅牌民光,幸福钟牌414,海螺"},
    ],
    "exposures": [
        {"exposure_id": "highly_manufacture_air_conditioner_compressor", "company_id": "highly", "node_id": "air_conditioner_compressor", "activity_type": "manufacture", "role": "空调压缩机制造商", "weight": 0.95},
        {"exposure_id": "highly_manufacture_heat_pump", "company_id": "highly", "node_id": "heat_pump", "activity_type": "manufacture", "role": "热泵制造商", "weight": 0.9},
        {"exposure_id": "tianchen_operate_real_estate_development", "company_id": "tianchen", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "tianchen_provide_service_property_management", "company_id": "tianchen", "node_id": "property_management", "activity_type": "provide_service", "role": "物业管理服务商", "weight": 0.85},
        {"exposure_id": "tianchen_operate_passenger_transport", "company_id": "tianchen", "node_id": "passenger_transport", "activity_type": "operate", "role": "客运运营商", "weight": 0.8},
        {"exposure_id": "huaxin_provide_service_securities_service", "company_id": "huaxin", "node_id": "securities_service", "activity_type": "provide_service", "role": "证券服务商", "weight": 0.95},
        {"exposure_id": "huaxin_provide_service_financial_service", "company_id": "huaxin", "node_id": "financial_service", "activity_type": "provide_service", "role": "金融服务商", "weight": 0.9},
        {"exposure_id": "everbright_jiabao_operate_real_estate_development", "company_id": "everbright_jiabao", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "everbright_jiabao_manufacture_capacitor", "company_id": "everbright_jiabao", "node_id": "capacitor", "activity_type": "manufacture", "role": "电容器制造商", "weight": 0.9},
        {"exposure_id": "huayi_produce_tire", "company_id": "huayi", "node_id": "tire", "activity_type": "produce", "role": "轮胎生产商", "weight": 0.95},
        {"exposure_id": "huayi_produce_rubber_product", "company_id": "huayi", "node_id": "rubber_product", "activity_type": "produce", "role": "橡胶制品生产商", "weight": 0.85},
        {"exposure_id": "st_fuhua_operate_manufacturing", "company_id": "st_fuhua", "node_id": "manufacturing", "activity_type": "operate", "role": "制造业运营商", "weight": 0.9},
        {"exposure_id": "st_fuhua_operate_real_estate_development", "company_id": "st_fuhua", "node_id": "real_estate_development", "activity_type": "operate", "role": "园区房地产运营商", "weight": 0.85},
        {"exposure_id": "st_fuhua_provide_service_software", "company_id": "st_fuhua", "node_id": "software", "activity_type": "provide_service", "role": "软件开发服务商", "weight": 0.85},
        {"exposure_id": "shenda_produce_automotive_interior", "company_id": "shenda", "node_id": "automotive_interior", "activity_type": "produce", "role": "汽车内饰生产商", "weight": 0.95},
        {"exposure_id": "shenda_produce_textile_new_material", "company_id": "shenda", "node_id": "textile_new_material", "activity_type": "produce", "role": "纺织新材料生产商", "weight": 0.95},
        {"exposure_id": "shenda_produce_textile_product", "company_id": "shenda", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.9},
        {"exposure_id": "new_world_operate_commercial", "company_id": "new_world", "node_id": "commercial", "activity_type": "operate", "role": "商业运营商", "weight": 0.95},
        {"exposure_id": "new_world_operate_retail", "company_id": "new_world", "node_id": "retail", "activity_type": "operate", "role": "零售运营商", "weight": 0.9},
        {"exposure_id": "new_world_operate_department_store", "company_id": "new_world", "node_id": "department_store", "activity_type": "operate", "role": "百货运营商", "weight": 0.95},
        {"exposure_id": "arcplus_provide_service_engineering_survey", "company_id": "arcplus", "node_id": "engineering_survey", "activity_type": "provide_service", "role": "工程勘察服务商", "weight": 0.95},
        {"exposure_id": "arcplus_provide_service_municipal_design", "company_id": "arcplus", "node_id": "municipal_design", "activity_type": "provide_service", "role": "市政设计服务商", "weight": 0.95},
        {"exposure_id": "arcplus_provide_service_construction_design", "company_id": "arcplus", "node_id": "construction_design", "activity_type": "provide_service", "role": "建筑设计服务商", "weight": 0.95},
        {"exposure_id": "dragon_head_operate_apparel_brand", "company_id": "dragon_head", "node_id": "apparel_brand", "activity_type": "operate", "role": "服饰品牌运营商", "weight": 0.95},
        {"exposure_id": "dragon_head_produce_apparel", "company_id": "dragon_head", "node_id": "apparel", "activity_type": "produce", "role": "服装生产商", "weight": 0.9},
        {"exposure_id": "dragon_head_produce_textile_product", "company_id": "dragon_head", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.85},
    ],
}

BATCH_089 = {
    "new_nodes": [
        {"node_id": "advertising", "canonical_name_zh": "广告", "definition": "通过媒体向公众传播商品、服务或观念信息以促进销售的商业宣传活动", "entity_type": "service"},
        {"node_id": "tunnel_bridge_facility", "canonical_name_zh": "隧桥设施", "definition": "城市隧道、桥梁及其附属设施，是城市交通基础设施的重要组成部分", "entity_type": "infrastructure"},
        {"node_id": "fluoropolymer", "canonical_name_zh": "含氟聚合物", "definition": "分子结构中含有氟原子的合成高分子材料，具有优异的耐化学腐蚀性和耐高温性", "entity_type": "material"},
        {"node_id": "cfc_substitute", "canonical_name_zh": "CFC替代品", "definition": "替代氯氟烃(CFC)的环保型制冷剂，对臭氧层破坏较小或为零", "entity_type": "material"},
        {"node_id": "audio_visual", "canonical_name_zh": "网络视听", "definition": "通过互联网传播的音频和视频内容服务，包括网络剧、网络电影、短视频等", "entity_type": "service"},
        {"node_id": "online_game", "canonical_name_zh": "网络游戏", "definition": "通过互联网进行多人互动的电子游戏，包括端游、手游、页游等形式", "entity_type": "service"},
        {"node_id": "golf", "canonical_name_zh": "高尔夫", "definition": "以球场为基础，提供高尔夫球运动、休闲和配套服务的体育产业", "entity_type": "service"},
        {"node_id": "cultural_supplies", "canonical_name_zh": "文化用品", "definition": "用于文化创作、学习教育和艺术活动的工具和材料，包括文具、绘画用品等", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "tunnel_bridge_facility_to_transportation", "from_node": "tunnel_bridge_facility", "to_node": "transportation", "edge_type": "capability_supply", "description": "隧桥设施为城市交通提供跨越障碍的通行能力"},
        {"edge_id": "fluoropolymer_to_chemical_industry", "from_node": "fluoropolymer", "to_node": "chemical_industry", "edge_type": "material_flow", "description": "含氟聚合物是化工新材料领域的重要产品"},
        {"edge_id": "online_game_to_internet", "from_node": "online_game", "to_node": "internet", "edge_type": "service_flow", "description": "网络游戏是互联网娱乐服务的重要业态"},
    ],
    "companies": [
        {"company_id": "zheshu", "name_zh": "浙报数字文化集团股份有限公司", "stock_code": "600633.SH", "province": "浙江", "city": "杭州市", "industry": "互联网", "main_business": "广告,实业投资,新媒体技术开发,工艺美术品,文化用品,办公用品的销售"},
        {"company_id": "dazhong_public", "name_zh": "上海大众公用事业(集团)股份有限公司", "stock_code": "600635.SH", "province": "上海", "city": "上海市", "industry": "供气供热", "main_business": "城市燃气,城市交通,隧桥设施,污水处理等"},
        {"company_id": "st_guohua", "name_zh": "国新文化控股股份有限公司", "stock_code": "600636.SH", "province": "上海", "city": "上海市", "industry": "文教休闲", "main_business": "含氟聚合物,CFC替代品,氟致冷剂,清洗剂,发泡剂"},
        {"company_id": "oriental_pearl", "name_zh": "东方明珠新媒体股份有限公司", "stock_code": "600637.SH", "province": "上海", "city": "上海市", "industry": "影视音像", "main_business": "网络视听,互联网,游戏等新兴业务"},
        {"company_id": "xinhuangpu", "name_zh": "上海新黄浦实业集团股份有限公司", "stock_code": "600638.SH", "province": "上海", "city": "上海市", "industry": "区域地产", "main_business": "房地产业,工业"},
        {"company_id": "pudong_jinqiao", "name_zh": "上海浦东金桥出口加工区开发股份有限公司", "stock_code": "600639.SH", "province": "上海", "city": "上海市", "industry": "园区开发", "main_business": "房地产销售,房地产租赁"},
        {"company_id": "guomai_culture", "name_zh": "新国脉数字文化股份有限公司", "stock_code": "600640.SH", "province": "上海", "city": "上海市", "industry": "影视音像", "main_business": "旅游预订及酒店经营和输出管理"},
        {"company_id": "xiandao", "name_zh": "上海万业企业股份有限公司", "stock_code": "600641.SH", "province": "上海", "city": "上海市", "industry": "半导体", "main_business": "商品房,酒店,旅游,高尔夫"},
        {"company_id": "shenergy", "name_zh": "申能股份有限公司", "stock_code": "600642.SH", "province": "上海", "city": "上海市", "industry": "火力发电", "main_business": "电力行业,石油天然气行业"},
        {"company_id": "aijian", "name_zh": "上海爱建集团股份有限公司", "stock_code": "600643.SH", "province": "上海", "city": "上海市", "industry": "多元金融", "main_business": "工业,商业,旅游饮食服务业"},
    ],
    "exposures": [
        {"exposure_id": "zheshu_provide_service_advertising", "company_id": "zheshu", "node_id": "advertising", "activity_type": "provide_service", "role": "广告服务商", "weight": 0.95},
        {"exposure_id": "zheshu_provide_service_new_media_technology", "company_id": "zheshu", "node_id": "new_media_technology", "activity_type": "provide_service", "role": "新媒体技术服务商", "weight": 0.9},
        {"exposure_id": "zheshu_produce_cultural_supplies", "company_id": "zheshu", "node_id": "cultural_supplies", "activity_type": "produce", "role": "文化用品生产商", "weight": 0.85},
        {"exposure_id": "dazhong_public_operate_city_gas", "company_id": "dazhong_public", "node_id": "city_gas", "activity_type": "operate", "role": "城市燃气运营商", "weight": 0.95},
        {"exposure_id": "dazhong_public_operate_tunnel_bridge_facility", "company_id": "dazhong_public", "node_id": "tunnel_bridge_facility", "activity_type": "operate", "role": "隧桥设施运营商", "weight": 0.9},
        {"exposure_id": "dazhong_public_operate_sewage_treatment", "company_id": "dazhong_public", "node_id": "sewage_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.9},
        {"exposure_id": "st_guohua_produce_fluoropolymer", "company_id": "st_guohua", "node_id": "fluoropolymer", "activity_type": "produce", "role": "含氟聚合物生产商", "weight": 0.95},
        {"exposure_id": "st_guohua_produce_cfc_substitute", "company_id": "st_guohua", "node_id": "cfc_substitute", "activity_type": "produce", "role": "CFC替代品生产商", "weight": 0.95},
        {"exposure_id": "st_guohua_produce_fluorine_refrigerant", "company_id": "st_guohua", "node_id": "fluorine_refrigerant", "activity_type": "produce", "role": "氟致冷剂生产商", "weight": 0.9},
        {"exposure_id": "oriental_pearl_provide_service_audio_visual", "company_id": "oriental_pearl", "node_id": "audio_visual", "activity_type": "provide_service", "role": "网络视听服务商", "weight": 0.95},
        {"exposure_id": "oriental_pearl_provide_service_online_game", "company_id": "oriental_pearl", "node_id": "online_game", "activity_type": "provide_service", "role": "网络游戏服务商", "weight": 0.9},
        {"exposure_id": "oriental_pearl_provide_service_internet", "company_id": "oriental_pearl", "node_id": "internet", "activity_type": "provide_service", "role": "互联网服务商", "weight": 0.85},
        {"exposure_id": "xinhuangpu_operate_real_estate_development", "company_id": "xinhuangpu", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "xinhuangpu_operate_industrial", "company_id": "xinhuangpu", "node_id": "industrial", "activity_type": "operate", "role": "工业运营商", "weight": 0.8},
        {"exposure_id": "pudong_jinqiao_operate_real_estate_development", "company_id": "pudong_jinqiao", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产销售运营商", "weight": 0.95},
        {"exposure_id": "pudong_jinqiao_operate_real_estate_leasing", "company_id": "pudong_jinqiao", "node_id": "real_estate_leasing", "activity_type": "operate", "role": "房地产租赁运营商", "weight": 0.9},
        {"exposure_id": "guomai_culture_provide_service_tourism_service", "company_id": "guomai_culture", "node_id": "tourism_service", "activity_type": "provide_service", "role": "旅游预订服务商", "weight": 0.95},
        {"exposure_id": "guomai_culture_operate_hotel_service", "company_id": "guomai_culture", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店经营商", "weight": 0.9},
        {"exposure_id": "xiandao_operate_real_estate_development", "company_id": "xiandao", "node_id": "real_estate_development", "activity_type": "operate", "role": "商品房开发商", "weight": 0.95},
        {"exposure_id": "xiandao_operate_hotel_service", "company_id": "xiandao", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.85},
        {"exposure_id": "xiandao_operate_golf", "company_id": "xiandao", "node_id": "golf", "activity_type": "operate", "role": "高尔夫运营商", "weight": 0.8},
        {"exposure_id": "shenergy_operate_power_generation", "company_id": "shenergy", "node_id": "power_generation", "activity_type": "operate", "role": "电力运营商", "weight": 0.95},
        {"exposure_id": "shenergy_operate_oil_gas", "company_id": "shenergy", "node_id": "oil_gas", "activity_type": "operate", "role": "石油天然气运营商", "weight": 0.9},
        {"exposure_id": "aijian_operate_industrial", "company_id": "aijian", "node_id": "industrial", "activity_type": "operate", "role": "工业运营商", "weight": 0.9},
        {"exposure_id": "aijian_operate_commercial", "company_id": "aijian", "node_id": "commercial", "activity_type": "operate", "role": "商业运营商", "weight": 0.85},
        {"exposure_id": "aijian_provide_service_tourism_service", "company_id": "aijian", "node_id": "tourism_service", "activity_type": "provide_service", "role": "旅游饮食服务商", "weight": 0.85},
    ],
}

BATCH_090 = {
    "new_nodes": [
        {"node_id": "power_transformation_equipment", "canonical_name_zh": "输变电设备", "definition": "用于电能输送和电压变换的电力设备总称，包括变压器、开关设备、输电线路等", "entity_type": "device"},
        {"node_id": "ac_motor", "canonical_name_zh": "交流电动机", "definition": "利用交流电产生旋转磁场驱动转子转动的电动机，是工业生产中最常用的动力设备", "entity_type": "component"},
        {"node_id": "carrier_wave_communication", "canonical_name_zh": "载波通信", "definition": "利用高频载波信号传输信息的通信方式，广泛应用于电力线载波通信等领域", "entity_type": "service"},
        {"node_id": "life_science", "canonical_name_zh": "生命科技", "definition": "以生物学、医学为基础，研究生命现象和开发生物技术产品的科学技术领域", "entity_type": "service"},
        {"node_id": "raw_water_supply", "canonical_name_zh": "原水供应", "definition": "从水源地取水并向水厂或用户供应未经处理或初步处理的原水的服务", "entity_type": "service"},
        {"node_id": "lamp_bulb", "canonical_name_zh": "灯泡", "definition": "将电能转换为光能的照明器件，包括白炽灯、节能灯、LED灯等", "entity_type": "component"},
        {"node_id": "automotive_electronics", "canonical_name_zh": "汽车电子", "definition": "应用于汽车上的电子控制系统和电子装置，包括发动机控制、车载娱乐、驾驶辅助等", "entity_type": "component"},
        {"node_id": "security_fire_system", "canonical_name_zh": "安防消防系统集成", "definition": "将安全防范和消防系统进行整合设计、安装和运维的综合服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "power_transformation_equipment_to_power_grid", "from_node": "power_transformation_equipment", "to_node": "power_grid", "edge_type": "composition", "description": "输变电设备是电力输配电网的核心组成装备"},
        {"edge_id": "lamp_bulb_to_lighting", "from_node": "lamp_bulb", "to_node": "lighting", "edge_type": "composition", "description": "灯泡是照明系统的核心发光部件"},
        {"edge_id": "automotive_electronics_to_automobile", "from_node": "automotive_electronics", "to_node": "automobile", "edge_type": "composition", "description": "汽车电子是现代汽车智能化和电气化的核心系统"},
    ],
    "companies": [
        {"company_id": "leshan_power", "name_zh": "乐山电力股份有限公司", "stock_code": "600644.SH", "province": "四川", "city": "乐山市", "industry": "水力发电", "main_business": "电力设施承装,承修,承试,地方电力开发,房地产,输变电设备,电工器材,交流电动机,载波通信"},
        {"company_id": "zhongyuanxiehe", "name_zh": "中源协和细胞基因工程股份有限公司", "stock_code": "600645.SH", "province": "天津", "city": "天津市", "industry": "医疗保健", "main_business": "工业,商业,房地产业,服务业,生命科技"},
        {"company_id": "waigaoqiao", "name_zh": "上海外高桥集团股份有限公司", "stock_code": "600648.SH", "province": "上海", "city": "上海市", "industry": "园区开发", "main_business": "房地产开发与租赁,贸易及物流,酒店经营管理等"},
        {"company_id": "chengtou", "name_zh": "上海城投控股股份有限公司", "stock_code": "600649.SH", "province": "上海", "city": "上海市", "industry": "区域地产", "main_business": "原水供应,污水处理"},
        {"company_id": "jinjiang_online", "name_zh": "上海锦江在线网络服务股份有限公司", "stock_code": "600650.SH", "province": "上海", "city": "上海市", "industry": "公共交通", "main_business": "客房,餐饮,商场,客运,物流"},
        {"company_id": "feile_audio", "name_zh": "上海飞乐音响股份有限公司", "stock_code": "600651.SH", "province": "上海", "city": "上海市", "industry": "电器仪表", "main_business": "灯泡,灯具及光源类产品,电子类产品,IC卡及相关软件开发和系统集成,音响类产品"},
        {"company_id": "shenhua", "name_zh": "上海申华控股股份有限公司", "stock_code": "600653.SH", "province": "上海", "city": "上海市", "industry": "汽车服务", "main_business": "汽车消费相关产业为主导产业,以新能源产业,房地产等投资作为补充"},
        {"company_id": "coa_security", "name_zh": "中安科股份有限公司", "stock_code": "600654.SH", "province": "上海", "city": "上海市", "industry": "仓储物流", "main_business": "安防消防系统集成,产品制造,综合运营服务,汽车电子,线束,电子材料,无线通信设备"},
        {"company_id": "yuyuan", "name_zh": "上海豫园旅游商城(集团)股份有限公司", "stock_code": "600655.SH", "province": "上海", "city": "上海市", "industry": "百货", "main_business": "黄金饰品,百货,饮食,食品,进出口,医药,工艺品,房产"},
        {"company_id": "cinda_realestate", "name_zh": "信达地产股份有限公司", "stock_code": "600657.SH", "province": "北京", "city": "北京市", "industry": "全国地产", "main_business": "房地产开发,投资及投资管理,物业管理"},
    ],
    "exposures": [
        {"exposure_id": "leshan_power_provide_service_power_installation", "company_id": "leshan_power", "node_id": "power_installation", "activity_type": "provide_service", "role": "电力设施承装服务商", "weight": 0.95},
        {"exposure_id": "leshan_power_manufacture_power_transformation_equipment", "company_id": "leshan_power", "node_id": "power_transformation_equipment", "activity_type": "manufacture", "role": "输变电设备制造商", "weight": 0.9},
        {"exposure_id": "leshan_power_produce_ac_motor", "company_id": "leshan_power", "node_id": "ac_motor", "activity_type": "produce", "role": "交流电动机生产商", "weight": 0.85},
        {"exposure_id": "leshan_power_provide_service_carrier_wave_communication", "company_id": "leshan_power", "node_id": "carrier_wave_communication", "activity_type": "provide_service", "role": "载波通信服务商", "weight": 0.85},
        {"exposure_id": "leshan_power_operate_power_generation", "company_id": "leshan_power", "node_id": "power_generation", "activity_type": "operate", "role": "地方电力运营商", "weight": 0.95},
        {"exposure_id": "zhongyuanxiehe_provide_service_life_science", "company_id": "zhongyuanxiehe", "node_id": "life_science", "activity_type": "provide_service", "role": "生命科技服务商", "weight": 0.95},
        {"exposure_id": "zhongyuanxiehe_produce_biotechnology", "company_id": "zhongyuanxiehe", "node_id": "biotechnology", "activity_type": "produce", "role": "生物技术产品生产商", "weight": 0.9},
        {"exposure_id": "waigaoqiao_operate_real_estate_development", "company_id": "waigaoqiao", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "waigaoqiao_provide_service_trade_logistics", "company_id": "waigaoqiao", "node_id": "trade_logistics", "activity_type": "provide_service", "role": "贸易物流服务商", "weight": 0.9},
        {"exposure_id": "waigaoqiao_operate_hotel_service", "company_id": "waigaoqiao", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店经营管理商", "weight": 0.85},
        {"exposure_id": "chengtou_provide_service_raw_water_supply", "company_id": "chengtou", "node_id": "raw_water_supply", "activity_type": "provide_service", "role": "原水供应服务商", "weight": 0.95},
        {"exposure_id": "chengtou_operate_sewage_treatment", "company_id": "chengtou", "node_id": "sewage_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.95},
        {"exposure_id": "jinjiang_online_operate_hotel_service", "company_id": "jinjiang_online", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.95},
        {"exposure_id": "jinjiang_online_operate_catering_service", "company_id": "jinjiang_online", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.9},
        {"exposure_id": "jinjiang_online_operate_passenger_transport", "company_id": "jinjiang_online", "node_id": "passenger_transport", "activity_type": "operate", "role": "客运运营商", "weight": 0.9},
        {"exposure_id": "jinjiang_online_provide_service_logistics", "company_id": "jinjiang_online", "node_id": "logistics", "activity_type": "provide_service", "role": "物流服务商", "weight": 0.85},
        {"exposure_id": "feile_audio_manufacture_lamp_bulb", "company_id": "feile_audio", "node_id": "lamp_bulb", "activity_type": "manufacture", "role": "灯泡制造商", "weight": 0.95},
        {"exposure_id": "feile_audio_manufacture_lighting_fixture", "company_id": "feile_audio", "node_id": "lighting_fixture", "activity_type": "manufacture", "role": "灯具制造商", "weight": 0.9},
        {"exposure_id": "feile_audio_manufacture_audio_equipment", "company_id": "feile_audio", "node_id": "audio_equipment", "activity_type": "manufacture", "role": "音响产品制造商", "weight": 0.9},
        {"exposure_id": "shenhua_provide_service_automotive_service", "company_id": "shenhua", "node_id": "automotive_service", "activity_type": "provide_service", "role": "汽车消费服务商", "weight": 0.95},
        {"exposure_id": "shenhua_produce_new_energy", "company_id": "shenhua", "node_id": "new_energy", "activity_type": "produce", "role": "新能源产品生产商", "weight": 0.85},
        {"exposure_id": "shenhua_operate_real_estate_development", "company_id": "shenhua", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产运营商", "weight": 0.85},
        {"exposure_id": "coa_security_provide_service_security_fire_system", "company_id": "coa_security", "node_id": "security_fire_system", "activity_type": "provide_service", "role": "安防消防系统集成商", "weight": 0.95},
        {"exposure_id": "coa_security_manufacture_automotive_electronics", "company_id": "coa_security", "node_id": "automotive_electronics", "activity_type": "manufacture", "role": "汽车电子制造商", "weight": 0.9},
        {"exposure_id": "coa_security_manufacture_wire_harness", "company_id": "coa_security", "node_id": "wire_harness", "activity_type": "manufacture", "role": "线束制造商", "weight": 0.85},
        {"exposure_id": "coa_security_manufacture_communication_equipment", "company_id": "coa_security", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "无线通信设备制造商", "weight": 0.85},
        {"exposure_id": "yuyuan_produce_gold_ornament", "company_id": "yuyuan", "node_id": "gold_ornament", "activity_type": "produce", "role": "黄金饰品生产商", "weight": 0.95},
        {"exposure_id": "yuyuan_operate_department_store", "company_id": "yuyuan", "node_id": "department_store", "activity_type": "operate", "role": "百货运营商", "weight": 0.95},
        {"exposure_id": "yuyuan_operate_catering_service", "company_id": "yuyuan", "node_id": "catering_service", "activity_type": "operate", "role": "饮食服务商", "weight": 0.9},
        {"exposure_id": "yuyuan_produce_pharmaceutical", "company_id": "yuyuan", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.85},
        {"exposure_id": "cinda_realestate_operate_real_estate_development", "company_id": "cinda_realestate", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "cinda_realestate_operate_real_estate_investment", "company_id": "cinda_realestate", "node_id": "real_estate_investment", "activity_type": "operate", "role": "房地产投资运营商", "weight": 0.9},
        {"exposure_id": "cinda_realestate_provide_service_property_management", "company_id": "cinda_realestate", "node_id": "property_management", "activity_type": "provide_service", "role": "物业管理服务商", "weight": 0.9},
    ],
}

ALL_BATCHES = {
    86: BATCH_086,
    87: BATCH_087,
    88: BATCH_088,
    89: BATCH_089,
    90: BATCH_090,
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
