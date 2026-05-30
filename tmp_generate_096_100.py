#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batches 091-095 submission scripts."""

import json
import os

BASE = "http://localhost:8005/api/v1"

TEMPLATE = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit batch {batch_num}."""

import json, sys, requests, uuid

BASE = "http://localhost:8005/api/v1"
BATCH_FILE = "data/stock_batches/batch_{batch_num:03d}.json"

def api_post(path, payload):
    url = f"{{BASE}}/{{path}}"
    r = requests.post(url, json=payload)
    if r.status_code not in (200, 201):
        print(f"  POST {{path}} failed: {{r.status_code}} - {{r.text[:200]}}")
    else:
        print(f"  POST {{path}} OK ({{r.status_code}})")
    return r

def make_evidence(quote, title="公司主营业务描述"):
    return [{{"source_title": title, "quote": quote, "confidence": "HIGH", "status": "ACTIVE"}}]

def main():
    with open(BATCH_FILE, encoding="utf-8") as f:
        companies = json.load(f)

    # Fetch existing nodes
    existing_nodes = {{}}
    page = 1
    while True:
        r = requests.get(f"{{BASE}}/nodes?page={{page}}&page_size=1000")
        items = r.json().get("items", [])
        if not items: break
        for n in items:
            existing_nodes[n["node_id"]] = n
        if len(items) < 1000: break
        page += 1
    print(f"Existing nodes: {{len(existing_nodes)}}")

    # Fetch existing edges
    existing_edges = set()
    page = 1
    while True:
        r = requests.get(f"{{BASE}}/edges?page={{page}}&page_size=1000")
        items = r.json().get("items", [])
        if not items: break
        for e in items:
            existing_edges.add((e.get("from_node") or e.get("source_id"), e.get("to_node") or e.get("target_id"), e["edge_type"]))
        if len(items) < 1000: break
        page += 1
    print(f"Existing edges: {{len(existing_edges)}}")

    # ---- Graph nodes ----
    nodes_to_create = []
{nodes_code}

    # ---- Graph edges ----
    edges_to_create = []
{edges_code}

    # ---- Submit graph batch ----
    if nodes_to_create or edges_to_create:
        batch = {{
            "batch_id": f"batch_{batch_num:03d}_graph",
            "task_description": f"Batch {batch_num:03d} industrial nodes and edges",
            "nodes_to_upsert": nodes_to_create,
            "edges_to_upsert": edges_to_create,
            "status": "ACTIVE",
            "evidence": [{{"source_title": "批次{batch_num}构建", "quote": "基于上市公司主营业务提取的工业节点与关系", "confidence": "HIGH", "status": "ACTIVE"}}]
        }}
        r = api_post("batches", batch)
        if r.status_code in (200, 201):
            print(f"Graph batch submitted: {{len(nodes_to_create)}} nodes, {{len(edges_to_create)}} edges")
        else:
            print(f"Graph batch FAILED: {{r.status_code}} {{r.text[:300]}}")
    else:
        print("No new graph nodes/edges to submit.")

    # ---- Companies and exposures ----
    companies_payload = []
    exposures_payload = []
{companies_code}

    if companies_payload:
        biz_batch = {{
            "batch_id": f"batch_{batch_num:03d}_biz",
            "task_description": f"Batch {batch_num:03d} companies and exposures",
            "companies_to_upsert": companies_payload,
            "company_node_exposures_to_upsert": exposures_payload,
            "status": "ACTIVE",
            "evidence": [{{"source_title": "批次{batch_num}构建", "quote": "基于上市公司主营业务提取的公司与节点暴露", "confidence": "HIGH", "status": "ACTIVE"}}]
        }}
        r = api_post("business-batches", biz_batch)
        if r.status_code in (200, 201):
            print(f"Business batch submitted: {{len(companies_payload)}} companies, {{len(exposures_payload)}} exposures")
        else:
            print(f"Business batch FAILED: {{r.status_code}} {{r.text[:300]}}")
    else:
        print("No companies to submit.")

if __name__ == "__main__":
    main()
'''


def build_nodes_code(nodes):
    lines = []
    for n in nodes:
        nid = n['node_id']
        lines.append(f'    if "{nid}" not in existing_nodes:')
        lines.append(f'        nodes_to_create.append({{')
        lines.append(f'            "node_id": "{nid}",')
        lines.append(f'            "canonical_name_zh": "{n["canonical_name_zh"]}",')
        lines.append(f'            "canonical_name_en": "{n["canonical_name_en"]}",')
        lines.append(f'            "definition": "{n["definition"]}",')
        lines.append(f'            "entity_type": "{n["entity_type"]}",')
        lines.append(f'            "evidence": make_evidence("{n["evidence_quote"]}", "{n.get("evidence_title", "公司主营业务描述")}"),')
        lines.append(f'            "confidence": "HIGH", "status": "ACTIVE"')
        lines.append(f'        }})')
        lines.append(f'    else:')
        lines.append(f'        print(f"  Node exists: {nid}")')
    return "\n".join(lines)


def build_edges_code(edges):
    lines = []
    for e in edges:
        sid, tid, etype = e['source_id'], e['target_id'], e['edge_type']
        eid = e['edge_id']
        lines.append(f'    if ("{sid}", "{tid}", "{etype}") not in existing_edges and "{sid}" in existing_nodes and "{tid}" in existing_nodes:')
        lines.append(f'        edges_to_create.append({{')
        lines.append(f'            "edge_id": "{eid}",')
        lines.append(f'            "from_node": "{sid}",')
        lines.append(f'            "to_node": "{tid}",')
        lines.append(f'            "edge_namespace": "{e["edge_namespace"]}",')
        lines.append(f'            "edge_type": "{etype}",')
        lines.append(f'            "description": "{e["description"]}",')
        lines.append(f'            "evidence": make_evidence("{e["evidence_quote"]}"),')
        lines.append(f'            "confidence": "HIGH", "status": "ACTIVE"')
        lines.append(f'        }})')
        lines.append(f'    else:')
        lines.append(f'        print(f"  Edge skip: {eid}")')
    return "\n".join(lines)


def build_companies_code(companies, batch_num):
    lines = []
    for i, c in enumerate(companies):
        ts_code = c['ts_code']
        cid = 'sh_' + ts_code.replace('.SH', '').replace('.SZ', '').lower()
        name = c['name']
        industry = c['industry']
        main = c['main_business']
        lines.append(f'    # {name} ({ts_code})')
        lines.append(f'    c = companies[{i}]')
        lines.append(f'    companies_payload.append({{')
        lines.append(f'        "company_id": "{cid}",')
        lines.append(f'        "name_zh": "{name}",')
        lines.append(f'        "stock_codes": ["{ts_code}"],')
        lines.append(f'        "country": "中国",')
        lines.append(f'        "industry": "{industry}",')
        lines.append(f'        "main_business": "{main}",')
        lines.append(f'        "company_type": "public",')
        lines.append(f'        "status": "ACTIVE",')
        lines.append(f'        "evidence": make_evidence("{main[:120]}")')
        lines.append(f'    }})')
        for exp in c['exposures']:
            eid = f"{cid}_{exp['node_id']}"
            lines.append(f'    exposures_payload.append({{')
            lines.append(f'        "exposure_id": "{eid}",')
            lines.append(f'        "company_id": "{cid}",')
            lines.append(f'        "node_id": "{exp["node_id"]}",')
            lines.append(f'        "activity_type": "{exp["activity_type"]}",')
            lines.append(f'        "weight": {exp["weight"]},')
            lines.append(f'        "evidence": make_evidence("{main[:120]}")')
            lines.append(f'    }})')
    return "\n".join(lines)


# ============ BATCH 096 DATA ============
batch_096_companies = [
    {"ts_code":"600720.SH","name":"中交设计","industry":"建筑工程","main_business":"主营业务:水泥生产,销售及商砼业务.主要产品:水泥,商品熟料,商品混凝土.","exposures":[
        {"node_id":"cement","activity_type":"produce","weight":0.4},
        {"node_id":"ready_mixed_concrete","activity_type":"produce","weight":0.3},
        {"node_id":"cement_product","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600721.SH","name":"百花医药","industry":"生物制药","main_business":"能源及煤化工投资.房地产投资.自营和代理各类商品和技术的进出口.开展边境小额贸易业务.机电产品,五金交电化工,金属材料,农副产品,皮棉,棉短绒.","exposures":[
        {"node_id":"trade_agent","activity_type":"procure","weight":0.3},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.2},
        {"node_id":"electromechanical_product","activity_type":"procure","weight":0.2},
        {"node_id":"metal_material","activity_type":"procure","weight":0.15},
        {"node_id":"agricultural_product","activity_type":"procure","weight":0.15}
    ]},
    {"ts_code":"600722.SH","name":"金牛化工","industry":"化工原料","main_business":"树脂,烧碱,水泥.","exposures":[
        {"node_id":"synthetic_resin","activity_type":"produce","weight":0.35},
        {"node_id":"soda_ash","activity_type":"produce","weight":0.35},
        {"node_id":"cement","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600724.SH","name":"宁波富达","industry":"综合类","main_business":"吸尘器,小家电,水泥,自来水.","exposures":[
        {"node_id":"vacuum_cleaner","activity_type":"produce","weight":0.25},
        {"node_id":"small_home_appliance","activity_type":"produce","weight":0.25},
        {"node_id":"cement","activity_type":"produce","weight":0.25},
        {"node_id":"tap_water_supply","activity_type":"operate","weight":0.25}
    ]},
    {"ts_code":"600725.SH","name":"云维股份","industry":"商贸代理","main_business":"聚乙烯醇,醋酸乙烯,电石,焦炭,甲醇,煤焦油及深加工产品,纯碱,氯化铵,水泥等.","exposures":[
        {"node_id":"pva","activity_type":"procure","weight":0.15},
        {"node_id":"vinyl_acetate","activity_type":"procure","weight":0.1},
        {"node_id":"calcium_carbide","activity_type":"procure","weight":0.1},
        {"node_id":"coke","activity_type":"procure","weight":0.1},
        {"node_id":"methanol","activity_type":"procure","weight":0.1},
        {"node_id":"coal_tar","activity_type":"procure","weight":0.1},
        {"node_id":"soda_ash","activity_type":"procure","weight":0.1},
        {"node_id":"ammonium_chloride","activity_type":"procure","weight":0.1},
        {"node_id":"cement","activity_type":"procure","weight":0.05},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.1}
    ]},
    {"ts_code":"600726.SH","name":"华电能源","industry":"火力发电","main_business":"主要产品:电力,热力.","exposures":[
        {"node_id":"electricity_power","activity_type":"produce","weight":0.6},
        {"node_id":"heat_supply","activity_type":"produce","weight":0.4}
    ]},
    {"ts_code":"600727.SH","name":"鲁北化工","industry":"化工原料","main_business":"磷铵,NPK复合肥,水泥,溴素及溴系列,电,氯碱.","exposures":[
        {"node_id":"ammonium_phosphate","activity_type":"produce","weight":0.2},
        {"node_id":"compound_fertilizer","activity_type":"produce","weight":0.15},
        {"node_id":"cement","activity_type":"produce","weight":0.15},
        {"node_id":"bromine","activity_type":"produce","weight":0.2},
        {"node_id":"chlor_alkali_product","activity_type":"produce","weight":0.2},
        {"node_id":"electricity_power","activity_type":"produce","weight":0.1}
    ]},
    {"ts_code":"600728.SH","name":"佳都科技","industry":"软件服务","main_business":"主营业务:智能安防,智能交通,通信增值,IT综合服务等.","exposures":[
        {"node_id":"intelligent_security_system","activity_type":"provide_service","weight":0.3},
        {"node_id":"intelligent_transport_system","activity_type":"provide_service","weight":0.3},
        {"node_id":"telecom_value_added_service","activity_type":"provide_service","weight":0.2},
        {"node_id":"it_integrated_service","activity_type":"provide_service","weight":0.2}
    ]},
    {"ts_code":"600729.SH","name":"重百集团","industry":"百货","main_business":"商品零售,商品批发.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":0.5},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.5}
    ]},
    {"ts_code":"600730.SH","name":"*ST高科","industry":"文教休闲","main_business":"教育,仓储,房地产,投资管理.","exposures":[
        {"node_id":"education_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"warehouse_service","activity_type":"operate","weight":0.25},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.25},
        {"node_id":"investment_management_service","activity_type":"provide_service","weight":0.25}
    ]},
]

batch_096_nodes = [
    {"node_id":"vacuum_cleaner","canonical_name_zh":"吸尘器","canonical_name_en":"Vacuum Cleaner","definition":"利用负压原理吸取灰尘和杂物的家用或商用清洁电器设备","entity_type":"device","evidence_quote":"吸尘器"},
    {"node_id":"pva","canonical_name_zh":"聚乙烯醇","canonical_name_en":"Polyvinyl Alcohol","definition":"一种水溶性合成高分子材料，由聚醋酸乙烯酯醇解制得，广泛用于纺织浆料、粘合剂、涂料等","entity_type":"material","evidence_quote":"聚乙烯醇"},
    {"node_id":"vinyl_acetate","canonical_name_zh":"醋酸乙烯","canonical_name_en":"Vinyl Acetate","definition":"一种重要的有机化工原料，主要用于生产聚乙烯醇、聚醋酸乙烯酯乳液和乙烯-醋酸乙烯共聚物","entity_type":"material","evidence_quote":"醋酸乙烯"},
    {"node_id":"coal_tar","canonical_name_zh":"煤焦油","canonical_name_en":"Coal Tar","definition":"煤干馏过程中产生的黑色粘稠液体，是重要的化工原料，可提取酚类、萘、蒽等多种化学品","entity_type":"material","evidence_quote":"煤焦油及深加工产品"},
    {"node_id":"ammonium_phosphate","canonical_name_zh":"磷铵","canonical_name_en":"Ammonium Phosphate","definition":"磷酸铵类肥料的总称，包括磷酸一铵和磷酸二铵，是重要的氮磷复合肥料","entity_type":"material","evidence_quote":"磷铵"},
    {"node_id":"bromine","canonical_name_zh":"溴素","canonical_name_en":"Bromine","definition":"一种卤族元素，常温下为红棕色液体，广泛用于阻燃剂、医药中间体、农药和油田化学品","entity_type":"material","evidence_quote":"溴素及溴系列"},
    {"node_id":"intelligent_security_system","canonical_name_zh":"智能安防系统","canonical_name_en":"Intelligent Security System","definition":"综合运用视频监控、人脸识别、行为分析、物联网传感器等技术的安全防护系统","entity_type":"system","evidence_quote":"智能安防"},
    {"node_id":"intelligent_transport_system","canonical_name_zh":"智能交通系统","canonical_name_en":"Intelligent Transport System","definition":"利用信息技术、通信技术、传感器技术和控制技术对交通运输系统进行智能化管理和服务的综合系统","entity_type":"system","evidence_quote":"智能交通"},
    {"node_id":"telecom_value_added_service","canonical_name_zh":"通信增值服务","canonical_name_en":"Telecom Value-Added Service","definition":"在基础通信服务之上提供的附加信息服务，如短信、彩铃、位置服务、移动支付等","entity_type":"service","evidence_quote":"通信增值"},
    {"node_id":"it_integrated_service","canonical_name_zh":"IT综合服务","canonical_name_en":"IT Integrated Service","definition":"为客户提供信息系统规划、建设、运维、优化及技术支持的全生命周期综合服务","entity_type":"service","evidence_quote":"IT综合服务等"},
    {"node_id":"investment_management_service","canonical_name_zh":"投资管理服务","canonical_name_en":"Investment Management Service","definition":"为客户提供资产配置、投资组合管理、风险评估及财务规划的专业金融服务","entity_type":"service","evidence_quote":"投资管理"},
]

batch_096_edges = [
    {"edge_id":"vinyl_acetate_to_pva","source_id":"vinyl_acetate","target_id":"pva","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"醋酸乙烯经聚合和醇解反应可制得聚乙烯醇","evidence_quote":"聚乙烯醇,醋酸乙烯"},
]

# ============ BATCH 097 DATA ============
batch_097_companies = [
    {"ts_code":"600731.SH","name":"湖南海利","industry":"农药化肥","main_business":"农药原药,农药制剂,精细化工产品,泵.","exposures":[
        {"node_id":"pesticide","activity_type":"produce","weight":0.25},
        {"node_id":"pesticide_intermediate","activity_type":"produce","weight":0.25},
        {"node_id":"pesticide_formulation","activity_type":"produce","weight":0.25},
        {"node_id":"pump","activity_type":"produce","weight":0.25}
    ]},
    {"ts_code":"600732.SH","name":"爱旭股份","industry":"电气设备","main_business":"商品房销售,商品房出租.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.5},
        {"node_id":"commercial_housing_rental","activity_type":"operate","weight":0.5}
    ]},
    {"ts_code":"600733.SH","name":"北汽蓝谷","industry":"汽车整车","main_business":"装配新能源汽车动力模块;生产电动乘用车;销售新能源汽车充电设施.","exposures":[
        {"node_id":"new_energy_vehicle","activity_type":"manufacture","weight":0.35},
        {"node_id":"nev_power_module","activity_type":"produce","weight":0.35},
        {"node_id":"nev_charging_facility","activity_type":"procure","weight":0.3}
    ]},
    {"ts_code":"600734.SH","name":"*ST实达","industry":"软件服务","main_business":"移动通讯智能终端业务;物联网周界安防业务.","exposures":[
        {"node_id":"mobile_terminal","activity_type":"produce","weight":0.5},
        {"node_id":"iot_security_system","activity_type":"provide_service","weight":0.5}
    ]},
    {"ts_code":"600735.SH","name":"ST新华锦","industry":"服饰","main_business":"主营业务为发制品+纺织服装+锡材料加工.","exposures":[
        {"node_id":"hair_product","activity_type":"produce","weight":0.35},
        {"node_id":"textile","activity_type":"produce","weight":0.35},
        {"node_id":"tin_material","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600736.SH","name":"苏州高新","industry":"园区开发","main_business":"房地产.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600737.SH","name":"中粮糖业","industry":"食品","main_business":"主要产品:番茄产品,农副产品,水泥产品.","exposures":[
        {"node_id":"tomato_product","activity_type":"produce","weight":0.35},
        {"node_id":"agricultural_product","activity_type":"procure","weight":0.35},
        {"node_id":"cement","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600738.SH","name":"丽尚国潮","industry":"百货","main_business":"主营业务:商品零售,餐饮娱乐.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":0.5},
        {"node_id":"catering_entertainment_service","activity_type":"provide_service","weight":0.5}
    ]},
    {"ts_code":"600739.SH","name":"辽宁成大","industry":"生物制药","main_business":"医药医疗,金融投资,供应链服务(贸易)和能源开发.","exposures":[
        {"node_id":"pharmaceutical_commerce","activity_type":"provide_service","weight":0.25},
        {"node_id":"financial_investment_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"supply_chain_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"energy_development_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600740.SH","name":"山西焦化","industry":"焦炭加工","main_business":"焦炭,其他化工产品.","exposures":[
        {"node_id":"coke","activity_type":"produce","weight":0.5},
        {"node_id":"coking_product","activity_type":"produce","weight":0.5}
    ]},
]

batch_097_nodes = [
    {"node_id":"pesticide_formulation","canonical_name_zh":"农药制剂","canonical_name_en":"Pesticide Formulation","definition":"将农药原药与助剂、溶剂等配制成可供直接使用的农药产品，如乳油、可湿性粉剂、悬浮剂等","entity_type":"material","evidence_quote":"农药原药,农药制剂"},
    {"node_id":"nev_charging_facility","canonical_name_zh":"新能源汽车充电设施","canonical_name_en":"NEV Charging Facility","definition":"为新能源汽车提供电能补充的设施，包括充电桩、充电站、换电站及配套配电系统","entity_type":"infrastructure","evidence_quote":"销售新能源汽车充电设施"},
    {"node_id":"nev_power_module","canonical_name_zh":"新能源汽车动力模块","canonical_name_en":"NEV Power Module","definition":"新能源汽车的核心动力单元，包括电池系统、电机系统和电控系统的集成模块","entity_type":"subsystem","evidence_quote":"装配新能源汽车动力模块"},
    {"node_id":"iot_security_system","canonical_name_zh":"物联网安防系统","canonical_name_en":"IoT Security System","definition":"基于物联网技术的周界防护和入侵检测系统，包括传感器网络、视频监控和报警联动","entity_type":"system","evidence_quote":"物联网周界安防业务"},
    {"node_id":"hair_product","canonical_name_zh":"发制品","canonical_name_en":"Hair Product","definition":"以人发或化纤为原料制成的假发、发套、发片、接发等美发产品","entity_type":"material","evidence_quote":"发制品"},
    {"node_id":"tin_material","canonical_name_zh":"锡材料","canonical_name_en":"Tin Material","definition":"以锡金属为基础的材料产品，包括锡锭、锡合金、锡化合物及锡焊料等","entity_type":"material","evidence_quote":"锡材料加工"},
    {"node_id":"catering_entertainment_service","canonical_name_zh":"餐饮娱乐服务","canonical_name_en":"Catering Entertainment Service","definition":"集餐饮服务和娱乐休闲于一体的商业服务，包括餐厅、酒吧、KTV、影院等","entity_type":"service","evidence_quote":"商品零售,餐饮娱乐"},
    {"node_id":"financial_investment_service","canonical_name_zh":"金融投资服务","canonical_name_en":"Financial Investment Service","definition":"为客户提供证券、基金、信托、股权投资及资产管理等金融投资专业服务","entity_type":"service","evidence_quote":"金融投资"},
    {"node_id":"energy_development_service","canonical_name_zh":"能源开发服务","canonical_name_en":"Energy Development Service","definition":"从事油气、煤炭、新能源等能源资源的勘探、开采、加工及技术服务","entity_type":"service","evidence_quote":"能源开发"},
    {"node_id":"coking_product","canonical_name_zh":"焦化产品","canonical_name_en":"Coking Product","definition":"以煤为原料经高温干馏得到的各类产品，包括焦炭、焦炉煤气、煤焦油、粗苯等","entity_type":"material","evidence_quote":"焦炭,其他化工产品"},
]

batch_097_edges = [
]

# ============ BATCH 098 DATA ============
batch_098_companies = [
    {"ts_code":"600741.SH","name":"华域汽车","industry":"汽车配件","main_business":"独立供应汽车零部件研发,生产及销售.","exposures":[
        {"node_id":"automotive_part","activity_type":"manufacture","weight":0.5},
        {"node_id":"automotive_rd_service","activity_type":"provide_service","weight":0.5}
    ]},
    {"ts_code":"600742.SH","name":"富维股份","industry":"汽车配件","main_business":"车轮,内饰件.","exposures":[
        {"node_id":"automotive_wheel","activity_type":"produce","weight":0.5},
        {"node_id":"automotive_interior","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600743.SH","name":"华远控股","industry":"区域地产","main_business":"房地产开发与经营.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600744.SH","name":"华银电力","industry":"火力发电","main_business":"火力发电,水力发电.","exposures":[
        {"node_id":"thermal_power_generation","activity_type":"produce","weight":0.5},
        {"node_id":"hydro_power","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600745.SH","name":"*ST闻泰","industry":"半导体","main_business":"主要产品:智能终端,虚拟现实,地产和酒店等","exposures":[
        {"node_id":"smart_terminal","activity_type":"produce","weight":0.3},
        {"node_id":"vr_device","activity_type":"produce","weight":0.3},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.2},
        {"node_id":"hotel","activity_type":"operate","weight":0.2}
    ]},
    {"ts_code":"600746.SH","name":"江苏索普","industry":"化工原料","main_business":"ADC发泡剂,漂粉精,氯,碱,电,蒸汽等.","exposures":[
        {"node_id":"adc_blowing_agent","activity_type":"produce","weight":0.25},
        {"node_id":"bleaching_powder","activity_type":"produce","weight":0.25},
        {"node_id":"chlor_alkali_product","activity_type":"produce","weight":0.25},
        {"node_id":"electricity_power","activity_type":"produce","weight":0.15},
        {"node_id":"heat_supply","activity_type":"produce","weight":0.1}
    ]},
    {"ts_code":"600748.SH","name":"上实发展","industry":"全国地产","main_business":"房屋租赁.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600749.SH","name":"西藏旅游","industry":"旅游景点","main_business":"旅游,酒店,设计制作,媒体代理.","exposures":[
        {"node_id":"tourism_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"hotel","activity_type":"operate","weight":0.25},
        {"node_id":"design_production_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"media_agency_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600750.SH","name":"华润江中","industry":"中成药","main_business":"中成药,抗生素制剂,原料药.","exposures":[
        {"node_id":"chinese_medicine_plaster","activity_type":"produce","weight":0.35},
        {"node_id":"antibiotic_preparation","activity_type":"produce","weight":0.35},
        {"node_id":"pharmaceutical_raw_material","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600751.SH","name":"海航科技","industry":"水运","main_business":"IT产品分销及技术解决方案,移动设备及生命周期服务,电子商务供应链解决方案,海航云集市,海航云科技.","exposures":[
        {"node_id":"it_product_distribution","activity_type":"provide_service","weight":0.25},
        {"node_id":"mobile_device_lifecycle_service","activity_type":"provide_service","weight":0.2},
        {"node_id":"ecommerce_supply_chain_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"cloud_service","activity_type":"provide_service","weight":0.3}
    ]},
]

batch_098_nodes = [
    {"node_id":"automotive_wheel","canonical_name_zh":"汽车车轮","canonical_name_en":"Automotive Wheel","definition":"汽车行驶系统的重要组成部分，包括轮辋、轮辐、轮胎及轮毂等总成","entity_type":"component","evidence_quote":"车轮"},
    {"node_id":"thermal_power_generation","canonical_name_zh":"火力发电服务","canonical_name_en":"Thermal Power Generation","definition":"利用煤炭、天然气等化石燃料燃烧产生热能，驱动汽轮机发电的电力生产服务","entity_type":"service","evidence_quote":"火力发电"},
    {"node_id":"vr_device","canonical_name_zh":"虚拟现实设备","canonical_name_en":"VR Device","definition":"能够生成沉浸式虚拟环境的头戴式显示设备及其配套交互设备，如手柄、定位器等","entity_type":"device","evidence_quote":"虚拟现实"},
    {"node_id":"adc_blowing_agent","canonical_name_zh":"ADC发泡剂","canonical_name_en":"ADC Blowing Agent","definition":"偶氮二甲酰胺，一种常用的化学发泡剂，广泛应用于PVC、聚乙烯、聚丙烯等塑料的发泡加工","entity_type":"material","evidence_quote":"ADC发泡剂"},
    {"node_id":"bleaching_powder","canonical_name_zh":"漂粉精","canonical_name_en":"Bleaching Powder","definition":"主要成分为次氯酸钙的高效漂白消毒剂，广泛用于纺织漂白、水处理和卫生消毒","entity_type":"material","evidence_quote":"漂粉精"},
    {"node_id":"media_agency_service","canonical_name_zh":"媒体代理服务","canonical_name_en":"Media Agency Service","definition":"为客户提供广告策划、媒体投放、效果监测及品牌传播策略的代理服务","entity_type":"service","evidence_quote":"媒体代理"},
    {"node_id":"antibiotic_preparation","canonical_name_zh":"抗生素制剂","canonical_name_en":"Antibiotic Preparation","definition":"以抗生素原料药为基础制成的可供临床使用的药品制剂，包括注射剂、口服制剂等","entity_type":"material","evidence_quote":"抗生素制剂"},
    {"node_id":"it_product_distribution","canonical_name_zh":"IT产品分销服务","canonical_name_en":"IT Product Distribution","definition":"从事计算机硬件、软件、网络设备及IT配件的渠道分销和供应链管理服务","entity_type":"service","evidence_quote":"IT产品分销及技术解决方案"},
    {"node_id":"ecommerce_supply_chain_service","canonical_name_zh":"电子商务供应链服务","canonical_name_en":"E-commerce Supply Chain Service","definition":"为电子商务平台提供仓储、物流、配送及供应链信息化管理的综合服务","entity_type":"service","evidence_quote":"电子商务供应链解决方案"},
    {"node_id":"cloud_service","canonical_name_zh":"云服务","canonical_name_en":"Cloud Service","definition":"基于互联网提供计算资源、存储资源、应用软件及平台服务的IT服务形态","entity_type":"service","evidence_quote":"海航云集市,海航云科技"},
    {"node_id":"design_production_service","canonical_name_zh":"设计制作服务","canonical_name_en":"Design Production Service","definition":"为客户提供平面设计、影视制作、展览展示及多媒体内容创作的创意服务","entity_type":"service","evidence_quote":"设计制作"},
    {"node_id":"mobile_device_lifecycle_service","canonical_name_zh":"移动设备生命周期服务","canonical_name_en":"Mobile Device Lifecycle Service","definition":"为移动设备提供采购、部署、运维、回收及数据清除等全生命周期管理服务","entity_type":"service","evidence_quote":"移动设备及生命周期服务"},
]

batch_098_edges = [
]

# ============ BATCH 099 DATA ============
batch_099_companies = [
    {"ts_code":"600753.SH","name":"*ST海钦","industry":"商贸代理","main_business":"大宗商品贸易业务主要以煤炭,焦炭等煤化工产品为主.","exposures":[
        {"node_id":"coal","activity_type":"procure","weight":0.4},
        {"node_id":"coke","activity_type":"procure","weight":0.4},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.2}
    ]},
    {"ts_code":"600754.SH","name":"锦江酒店","industry":"酒店餐饮","main_business":"有限服务型酒店营运及管理业务和食品及餐饮业务.","exposures":[
        {"node_id":"hotel","activity_type":"operate","weight":0.5},
        {"node_id":"hotel_operation_service","activity_type":"operate","weight":0.25},
        {"node_id":"catering_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600755.SH","name":"厦门国贸","industry":"仓储物流","main_business":"供应链管理业务,房地产经营业务,金融服务业务.","exposures":[
        {"node_id":"supply_chain_service","activity_type":"provide_service","weight":0.35},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.3},
        {"node_id":"financial_service","activity_type":"provide_service","weight":0.35}
    ]},
    {"ts_code":"600756.SH","name":"浪潮软件","industry":"软件服务","main_business":"通信及计算机软硬件技术开发,生产,销售;通信及计算机网络工程技术技术咨询,技术培训.","exposures":[
        {"node_id":"software_development_service","activity_type":"provide_service","weight":0.3},
        {"node_id":"computer_hardware","activity_type":"produce","weight":0.3},
        {"node_id":"telecom_software","activity_type":"provide_service","weight":0.2},
        {"node_id":"technical_training_service","activity_type":"provide_service","weight":0.2}
    ]},
    {"ts_code":"600757.SH","name":"长江传媒","industry":"出版业","main_business":"图书,期刊,报纸,音像制品,电子出版物的出版,发行,印制,物资贸易等.","exposures":[
        {"node_id":"book_publishing","activity_type":"produce","weight":0.2},
        {"node_id":"journal_publishing","activity_type":"produce","weight":0.15},
        {"node_id":"newspaper_publishing","activity_type":"produce","weight":0.15},
        {"node_id":"audio_video_product","activity_type":"produce","weight":0.15},
        {"node_id":"electronic_publication","activity_type":"produce","weight":0.15},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.2}
    ]},
    {"ts_code":"600758.SH","name":"辽宁能源","industry":"煤炭开采","main_business":"建筑安装,房地产开发,建筑材料销售.","exposures":[
        {"node_id":"construction_installation_service","activity_type":"provide_service","weight":0.35},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.3},
        {"node_id":"building_material","activity_type":"procure","weight":0.35}
    ]},
    {"ts_code":"600759.SH","name":"ST洲际","industry":"石油开采","main_business":"石油勘探开发业务,房地产开发,物业租赁以及贸易.","exposures":[
        {"node_id":"petroleum_exploration","activity_type":"provide_service","weight":0.3},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.25},
        {"node_id":"property_rental_service","activity_type":"operate","weight":0.25},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.2}
    ]},
    {"ts_code":"600760.SH","name":"中航沈飞","industry":"航空","main_business":"实业投资;航空产品研发,生产,服务保障.","exposures":[
        {"node_id":"aerospace_rd_service","activity_type":"provide_service","weight":0.5},
        {"node_id":"aerospace_product","activity_type":"manufacture","weight":0.5}
    ]},
    {"ts_code":"600761.SH","name":"安徽合力","industry":"工程机械","main_business":"叉车产品.","exposures":[
        {"node_id":"forklift","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600763.SH","name":"通策医疗","industry":"医疗保健","main_business":"口腔,辅助生殖医疗等服务.","exposures":[
        {"node_id":"dental_medical_service","activity_type":"provide_service","weight":0.5},
        {"node_id":"assisted_reproduction_service","activity_type":"provide_service","weight":0.5}
    ]},
]

batch_099_nodes = [
    {"node_id":"financial_service","canonical_name_zh":"金融服务","canonical_name_en":"Financial Service","definition":"为客户提供融资、结算、担保、保险及金融咨询等综合金融服务","entity_type":"service","evidence_quote":"金融服务业务"},
    {"node_id":"computer_hardware","canonical_name_zh":"计算机硬件","canonical_name_en":"Computer Hardware","definition":"计算机系统的物理设备，包括服务器、个人电脑、存储设备、网络设备及外围设备","entity_type":"device","evidence_quote":"通信及计算机软硬件技术开发,生产,销售"},
    {"node_id":"technical_training_service","canonical_name_zh":"技术培训服务","canonical_name_en":"Technical Training Service","definition":"为客户提供通信、计算机及网络技术领域的专业技能培训和认证服务","entity_type":"service","evidence_quote":"技术培训"},
    {"node_id":"book_publishing","canonical_name_zh":"图书出版","canonical_name_en":"Book Publishing","definition":"将作者原稿经编辑、排版、印刷等工序制成图书并发行销售的出版业务","entity_type":"service","evidence_quote":"图书"},
    {"node_id":"journal_publishing","canonical_name_zh":"期刊出版","canonical_name_en":"Journal Publishing","definition":"定期出版发行的杂志、学术期刊等连续出版物的编辑、印刷和发行业务","entity_type":"service","evidence_quote":"期刊"},
    {"node_id":"newspaper_publishing","canonical_name_zh":"报纸出版","canonical_name_en":"Newspaper Publishing","definition":"以新闻、评论和信息为主要内容的定期出版物编辑、印刷和发行业务","entity_type":"service","evidence_quote":"报纸"},
    {"node_id":"audio_video_product","canonical_name_zh":"音像制品","canonical_name_en":"Audio Video Product","definition":"以录音带、录像带、CD、DVD等为载体的音频和视频内容出版物","entity_type":"material","evidence_quote":"音像制品"},
    {"node_id":"electronic_publication","canonical_name_zh":"电子出版物","canonical_name_en":"Electronic Publication","definition":"以数字形式存储和传播的出版物，包括电子书、电子期刊、数据库及多媒体光盘等","entity_type":"material","evidence_quote":"电子出版物"},
    {"node_id":"construction_installation_service","canonical_name_zh":"建筑安装服务","canonical_name_en":"Construction Installation Service","definition":"为建筑工程提供土建施工、机电设备安装、管道敷设及系统调试的综合服务","entity_type":"service","evidence_quote":"建筑安装"},
    {"node_id":"building_material","canonical_name_zh":"建筑材料","canonical_name_en":"Building Material","definition":"用于建筑物建造和装修的各类材料，包括钢材、水泥、玻璃、陶瓷、涂料及保温材料等","entity_type":"material","evidence_quote":"建筑材料销售"},
    {"node_id":"property_rental_service","canonical_name_zh":"物业租赁服务","canonical_name_en":"Property Rental Service","definition":"将自有或受托管理的物业用于出租经营，提供租赁管理、维修维护及配套服务的业务","entity_type":"service","evidence_quote":"物业租赁"},
    {"node_id":"aerospace_rd_service","canonical_name_zh":"航空产品研发服务","canonical_name_en":"Aerospace R&D Service","definition":"从事航空器及相关产品的研发设计、试验验证和技术改进的专业技术服务","entity_type":"service","evidence_quote":"航空产品研发"},
    {"node_id":"forklift","canonical_name_zh":"叉车","canonical_name_en":"Forklift","definition":"一种用于装卸、堆垛和短距离运输托盘货物的工业搬运车辆","entity_type":"device","evidence_quote":"叉车产品"},
    {"node_id":"dental_medical_service","canonical_name_zh":"口腔医疗服务","canonical_name_en":"Dental Medical Service","definition":"为患者提供口腔疾病预防、诊断、治疗及修复的专业医疗服务","entity_type":"service","evidence_quote":"口腔"},
    {"node_id":"assisted_reproduction_service","canonical_name_zh":"辅助生殖医疗服务","canonical_name_en":"Assisted Reproduction Service","definition":"运用医学手段帮助不孕不育夫妇实现生育的医疗服务，包括人工授精、试管婴儿等技术","entity_type":"service","evidence_quote":"辅助生殖医疗"},
]

batch_099_edges = [
]

# ============ BATCH 100 DATA ============
batch_100_companies = [
    {"ts_code":"600764.SH","name":"中国海防","industry":"船舶","main_business":"各类军民用水声信息传输装备,水下武器系统专项设备等军品领域产品,以及压载水电源等民品领域产品.","exposures":[
        {"node_id":"underwater_acoustic_equipment","activity_type":"produce","weight":0.3},
        {"node_id":"underwater_weapon_system","activity_type":"produce","weight":0.3},
        {"node_id":"ballast_water_power_supply","activity_type":"produce","weight":0.2},
        {"node_id":"ship","activity_type":"produce","weight":0.2}
    ]},
    {"ts_code":"600765.SH","name":"XD中航重","industry":"航空","main_business":"液压行业.","exposures":[
        {"node_id":"hydraulic_system","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600768.SH","name":"宁波富邦","industry":"铝","main_business":"工业铝板带材和铝型材生产,加工和销售以及铝铸棒的仓储,贸易服务.","exposures":[
        {"node_id":"aluminum_plate_strip","activity_type":"produce","weight":0.3},
        {"node_id":"aluminum_profile","activity_type":"produce","weight":0.3},
        {"node_id":"aluminum_billet","activity_type":"procure","weight":0.2},
        {"node_id":"warehouse_service","activity_type":"operate","weight":0.1},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.1}
    ]},
    {"ts_code":"600769.SH","name":"祥龙电业","industry":"水务","main_business":"化工产品,供电供汽,运输.","exposures":[
        {"node_id":"chemical_product","activity_type":"produce","weight":0.3},
        {"node_id":"electricity_power","activity_type":"produce","weight":0.25},
        {"node_id":"steam_supply_service","activity_type":"produce","weight":0.25},
        {"node_id":"logistics_service","activity_type":"operate","weight":0.2}
    ]},
    {"ts_code":"600770.SH","name":"综艺股份","industry":"综合类","main_business":"信息科技,新能源,股权投资.","exposures":[
        {"node_id":"information_technology_service","activity_type":"provide_service","weight":0.35},
        {"node_id":"new_energy","activity_type":"operate","weight":0.35},
        {"node_id":"equity_investment_service","activity_type":"provide_service","weight":0.3}
    ]},
    {"ts_code":"600771.SH","name":"广誉远","industry":"中成药","main_business":"龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等.","exposures":[
        {"node_id":"chinese_patent_medicine_pill","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600773.SH","name":"西藏城投","industry":"区域地产","main_business":"房地产开发,销售,咨询服务以及对矿业,金融,实业的投资.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.5},
        {"node_id":"mining_investment","activity_type":"operate","weight":0.15},
        {"node_id":"financial_investment_service","activity_type":"operate","weight":0.15},
        {"node_id":"industrial_investment","activity_type":"operate","weight":0.2}
    ]},
    {"ts_code":"600774.SH","name":"汉商集团","industry":"化学制药","main_business":"零售业,会展业,地产业及旅业等业务.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":0.25},
        {"node_id":"exhibition_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.25},
        {"node_id":"tourism_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600775.SH","name":"南京熊猫","industry":"通信设备","main_business":"移动通信产品,卫星通信产品,机电仪产品,电子信息产品.","exposures":[
        {"node_id":"mobile_communication_equipment","activity_type":"produce","weight":0.25},
        {"node_id":"satellite_communication","activity_type":"produce","weight":0.25},
        {"node_id":"electromechanical_instrument_product","activity_type":"produce","weight":0.25},
        {"node_id":"electronic_information_product","activity_type":"produce","weight":0.25}
    ]},
    {"ts_code":"600776.SH","name":"东方通信","industry":"通信设备","main_business":"移动通信业务,传输设备业务,IC卡话机业务,电信及电源设备业务.","exposures":[
        {"node_id":"mobile_communication_equipment","activity_type":"produce","weight":0.25},
        {"node_id":"transmission_equipment","activity_type":"produce","weight":0.25},
        {"node_id":"ic_card_telephone","activity_type":"produce","weight":0.25},
        {"node_id":"telecom_power_equipment","activity_type":"produce","weight":0.25}
    ]},
]

batch_100_nodes = [
    {"node_id":"underwater_acoustic_equipment","canonical_name_zh":"水声信息传输装备","canonical_name_en":"Underwater Acoustic Equipment","definition":"利用水声通信技术在水下传输信息的专用装备，包括声纳、水声通信机和声信标等","entity_type":"device","evidence_quote":"水声信息传输装备"},
    {"node_id":"underwater_weapon_system","canonical_name_zh":"水下武器系统","canonical_name_en":"Underwater Weapon System","definition":"部署于水下用于攻击或防御的武器系统，包括鱼雷、水雷、深水炸弹及反潜导弹等","entity_type":"system","evidence_quote":"水下武器系统专项设备"},
    {"node_id":"ballast_water_power_supply","canonical_name_zh":"压载水电源","canonical_name_en":"Ballast Water Power Supply","definition":"为船舶压载水处理系统提供电力的专用电源设备，确保压载水在排放前得到有效处理","entity_type":"device","evidence_quote":"压载水电源"},
    {"node_id":"hydraulic_system","canonical_name_zh":"液压系统","canonical_name_en":"Hydraulic System","definition":"利用液体压力传递动力的系统，包括液压泵、液压缸、液压阀及管路等组件，广泛应用于工程机械和航空领域","entity_type":"system","evidence_quote":"液压行业"},
    {"node_id":"aluminum_plate_strip","canonical_name_zh":"铝板带材","canonical_name_en":"Aluminum Plate Strip","definition":"经轧制加工的扁平状铝及铝合金材料，包括铝板、铝带、铝箔等，广泛用于建筑、交通和包装","entity_type":"material","evidence_quote":"工业铝板带材"},
    {"node_id":"aluminum_profile","canonical_name_zh":"铝型材","canonical_name_en":"Aluminum Profile","definition":"通过挤压工艺制成的具有特定截面形状的铝材，广泛用于建筑幕墙、门窗框架和工业结构件","entity_type":"material","evidence_quote":"铝型材"},
    {"node_id":"aluminum_billet","canonical_name_zh":"铝铸棒","canonical_name_en":"Aluminum Billet","definition":"通过熔炼铸造制成的圆柱形铝坯料，是挤压铝型材和轧制铝板带材的原材料","entity_type":"material","evidence_quote":"铝铸棒的仓储,贸易服务"},
    {"node_id":"steam_supply_service","canonical_name_zh":"供汽服务","canonical_name_en":"Steam Supply Service","definition":"通过锅炉或热电联产装置向工业用户供应蒸汽的公用事业服务","entity_type":"service","evidence_quote":"供电供汽"},
    {"node_id":"equity_investment_service","canonical_name_zh":"股权投资服务","canonical_name_en":"Equity Investment Service","definition":"通过认购非上市公司股权或参与股权投资基金，为企业提供资本支持和增值服务的业务","entity_type":"service","evidence_quote":"股权投资"},
    {"node_id":"chinese_patent_medicine_pill","canonical_name_zh":"中药经典名方制剂","canonical_name_en":"Chinese Patent Medicine Pill","definition":"以经典中药方剂为基础，经现代工艺制成的丸剂、散剂等中成药制剂，如安宫牛黄丸、定坤丹等","entity_type":"material","evidence_quote":"龟龄集,定坤丹,牛黄清心丸,安宫牛黄丸,盖天力等"},
    {"node_id":"electromechanical_instrument_product","canonical_name_zh":"机电仪产品","canonical_name_en":"Electromechanical Instrument Product","definition":"集机械、电子和仪表技术于一体的综合性产品，包括工业自动化仪表、控制设备及精密机械装置","entity_type":"component","evidence_quote":"机电仪产品"},
    {"node_id":"electronic_information_product","canonical_name_zh":"电子信息产品","canonical_name_en":"Electronic Information Product","definition":"利用电子信息技术制造的各类产品，包括通信设备、计算机、消费电子及电子元器件等","entity_type":"component","evidence_quote":"电子信息产品"},
    {"node_id":"ic_card_telephone","canonical_name_zh":"IC卡话机","canonical_name_en":"IC Card Telephone","definition":"支持插入IC卡进行计费通话的公用电话终端设备，广泛用于公共场所通信服务","entity_type":"device","evidence_quote":"IC卡话机业务"},
    {"node_id":"telecom_power_equipment","canonical_name_zh":"电信电源设备","canonical_name_en":"Telecom Power Equipment","definition":"为通信网络设备提供稳定电力供应的专用电源系统，包括开关电源、UPS、蓄电池及配电设备等","entity_type":"device","evidence_quote":"电信及电源设备业务"},
]

batch_100_edges = [
]




def generate_batch(batch_num, companies, nodes, edges):
    nodes_code = build_nodes_code(nodes)
    edges_code = build_edges_code(edges)
    companies_code = build_companies_code(companies, batch_num)

    content = TEMPLATE.format(
        batch_num=batch_num,
        nodes_code=nodes_code,
        edges_code=edges_code,
        companies_code=companies_code,
    )

    out_path = f"tmp_script/tmp_submit_batch_{batch_num:03d}.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")


def main():
    os.makedirs("tmp_script", exist_ok=True)
    generate_batch(96, batch_096_companies, batch_096_nodes, batch_096_edges)
    generate_batch(97, batch_097_companies, batch_097_nodes, batch_097_edges)
    generate_batch(98, batch_098_companies, batch_098_nodes, batch_098_edges)
    generate_batch(99, batch_099_companies, batch_099_nodes, batch_099_edges)
    generate_batch(100, batch_100_companies, batch_100_nodes, batch_100_edges)
    print("All 5 batch scripts generated.")


if __name__ == "__main__":
    main()
