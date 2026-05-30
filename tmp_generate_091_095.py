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


# ============ BATCH 091 DATA ============
batch_091_companies = [
    {"ts_code":"600658.SH","name":"电子城","industry":"园区开发","main_business":"主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务.","exposures":[
        {"node_id":"tech_park_operation_service","activity_type":"operate","weight":0.5},
        {"node_id":"communication_equipment","activity_type":"manufacture","weight":0.25},
        {"node_id":"printing_material","activity_type":"manufacture","weight":0.15},
        {"node_id":"financial_equipment","activity_type":"manufacture","weight":0.1}
    ]},
    {"ts_code":"600660.SH","name":"福耀玻璃","industry":"汽车配件","main_business":"主营业务:从事浮法玻璃及汽车用玻璃制品的生产及销售.","exposures":[
        {"node_id":"float_glass","activity_type":"produce","weight":0.5},
        {"node_id":"automotive_glass","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600661.SH","name":"昂立教育","industry":"文教休闲","main_business":"主营业务:教育培训.","exposures":[
        {"node_id":"education_service","activity_type":"provide_service","weight":1.0}
    ]},
    {"ts_code":"600662.SH","name":"外服控股","industry":"文教休闲","main_business":"出租汽车服务及其相关业务,旅游服务.","exposures":[
        {"node_id":"taxi_operation_service","activity_type":"operate","weight":0.5},
        {"node_id":"tourism_service","activity_type":"provide_service","weight":0.5}
    ]},
    {"ts_code":"600663.SH","name":"陆家嘴","industry":"园区开发","main_business":"主营业务:房地产投资开发运营","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600664.SH","name":"哈药股份","industry":"化学制药","main_business":"主要产品:中药,西药,保健品.","exposures":[
        {"node_id":"chinese_medicine_preparation","activity_type":"produce","weight":0.35},
        {"node_id":"chemical_drug_preparation","activity_type":"produce","weight":0.35},
        {"node_id":"health_food","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600665.SH","name":"天地源","industry":"全国地产","main_business":"主营业务为房地产开发和经营,自有房屋租赁,物业管理,实业投资,资产管理,国内贸易.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.7},
        {"node_id":"warehouse_service","activity_type":"operate","weight":0.1},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.1}
    ]},
    {"ts_code":"600666.SH","name":"奥瑞德","industry":"元器件","main_business":"蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售","exposures":[
        {"node_id":"sapphire_crystal_material","activity_type":"produce","weight":0.4},
        {"node_id":"single_crystal_furnace","activity_type":"produce","weight":0.3},
        {"node_id":"sapphire_product","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600667.SH","name":"太极实业","industry":"半导体","main_business":"半导体后工序服务业务","exposures":[
        {"node_id":"semiconductor_backend_service","activity_type":"provide_service","weight":0.8},
        {"node_id":"semiconductor_device","activity_type":"manufacture","weight":0.2}
    ]},
    {"ts_code":"600668.SH","name":"尖峰集团","industry":"水泥","main_business":"公司的主营业务以水泥和医药为主,通信电缆,仓储,贸易为辅.","exposures":[
        {"node_id":"cement","activity_type":"produce","weight":0.3},
        {"node_id":"pharmaceutical_intermediate","activity_type":"produce","weight":0.2},
        {"node_id":"telecom_cable","activity_type":"produce","weight":0.2},
        {"node_id":"warehouse_service","activity_type":"operate","weight":0.15},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.15}
    ]},
]

batch_091_nodes = [
    {"node_id":"tech_park_operation_service","canonical_name_zh":"科技产业园区运营服务","canonical_name_en":"Technology Park Operation Service","definition":"为科技产业园区提供整体运营、招商、物业管理及产业配套服务的业务形态","entity_type":"service","evidence_quote":"主要业务:通信设备制造业务,印刷材料制造业务,金融设备制造业务"},
    {"node_id":"automotive_glass","canonical_name_zh":"汽车玻璃","canonical_name_en":"Automotive Glass","definition":"用于汽车车身门窗等部位的专用安全玻璃制品，包括前挡、侧窗、后挡等","entity_type":"component","evidence_quote":"从事浮法玻璃及汽车用玻璃制品的生产及销售"},
    {"node_id":"taxi_operation_service","canonical_name_zh":"出租汽车运营服务","canonical_name_en":"Taxi Operation Service","definition":"以出租汽车为载体，为乘客提供点对点出行运输服务的运营业务","entity_type":"service","evidence_quote":"出租汽车服务及其相关业务"},
    {"node_id":"chinese_medicine_preparation","canonical_name_zh":"中药制剂","canonical_name_en":"Chinese Medicine Preparation","definition":"以中药材为原料，经提取、浓缩、成型等工艺制成的成药制剂","entity_type":"material","evidence_quote":"主要产品:中药"},
    {"node_id":"chemical_drug_preparation","canonical_name_zh":"化学药品制剂","canonical_name_en":"Chemical Drug Preparation","definition":"以化学原料药为基础，经配方、制剂工艺制成的可供临床使用的药品","entity_type":"material","evidence_quote":"主要产品:西药"},
    {"node_id":"health_food","canonical_name_zh":"保健食品","canonical_name_en":"Health Food","definition":"具有特定保健功能，适宜特定人群食用，不以治疗疾病为目的的食品","entity_type":"material","evidence_quote":"主要产品:保健品"},
    {"node_id":"sapphire_crystal_material","canonical_name_zh":"蓝宝石晶体材料","canonical_name_en":"Sapphire Crystal Material","definition":"以氧化铝单晶形式生长的人工蓝宝石材料，具有高硬度、透光性优异等特点","entity_type":"material","evidence_quote":"蓝宝石晶体材料"},
    {"node_id":"single_crystal_furnace","canonical_name_zh":"单晶炉","canonical_name_en":"Single Crystal Furnace","definition":"用于生长单晶材料的高温设备，通过提拉法或泡生法实现晶体生长","entity_type":"device","evidence_quote":"单晶炉及蓝宝石制品的研发,生产和销售"},
    {"node_id":"sapphire_product","canonical_name_zh":"蓝宝石制品","canonical_name_en":"Sapphire Product","definition":"以蓝宝石晶体材料为基础加工而成的各类功能性产品，如衬底、窗口片等","entity_type":"component","evidence_quote":"蓝宝石晶体材料,单晶炉及蓝宝石制品的研发,生产和销售"},
    {"node_id":"semiconductor_backend_service","canonical_name_zh":"半导体后工序服务","canonical_name_en":"Semiconductor Backend Service","definition":"半导体制造流程中晶圆测试、切割、封装、成品测试等后段工序服务","entity_type":"service","evidence_quote":"半导体后工序服务业务"},
    {"node_id":"telecom_cable","canonical_name_zh":"通信电缆","canonical_name_en":"Telecommunication Cable","definition":"用于传输电信号或光信号的线缆产品，包括同轴电缆、光缆等","entity_type":"component","evidence_quote":"通信电缆"},
    {"node_id":"printing_material","canonical_name_zh":"印刷材料","canonical_name_en":"Printing Material","definition":"用于印刷工艺的各类耗材，包括油墨、版材、纸张等","entity_type":"material","evidence_quote":"印刷材料制造业务"},
    {"node_id":"financial_equipment","canonical_name_zh":"金融设备","canonical_name_en":"Financial Equipment","definition":"用于金融业务场景的专用设备，如点钞机、清分机、ATM等","entity_type":"device","evidence_quote":"金融设备制造业务"},
]

batch_091_edges = [
    {"edge_id":"float_glass_to_automotive_glass","source_id":"float_glass","target_id":"automotive_glass","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"浮法玻璃经深加工制成汽车玻璃","evidence_quote":"从事浮法玻璃及汽车用玻璃制品的生产及销售"},
    {"edge_id":"sapphire_material_to_product","source_id":"sapphire_crystal_material","target_id":"sapphire_product","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"蓝宝石晶体材料经加工制成蓝宝石制品","evidence_quote":"蓝宝石晶体材料及蓝宝石制品的研发,生产和销售"},
    {"edge_id":"single_crystal_furnace_to_sapphire","source_id":"single_crystal_furnace","target_id":"sapphire_crystal_material","edge_namespace":"industrial_flow","edge_type":"capability_supply","description":"单晶炉提供晶体生长能力，产出蓝宝石晶体材料","evidence_quote":"单晶炉及蓝宝石制品的研发,生产和销售"},
]

# ============ BATCH 092 DATA ============
batch_092_companies = [
    {"ts_code":"600671.SH","name":"天目药业","industry":"中成药","main_business":"珍珠明目滴眼液,复方鲜竹沥液.","exposures":[
        {"node_id":"ophthalmic_eye_drop","activity_type":"produce","weight":0.5},
        {"node_id":"chinese_patent_medicine_liquid","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600673.SH","name":"东阳光","industry":"综合类","main_business":"亲水箔的生产和销售.","exposures":[
        {"node_id":"hydrophilic_aluminum_foil","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600674.SH","name":"川投能源","industry":"水力发电","main_business":"主要产品:钨系列,高锰,硅锰,铬系列.","exposures":[
        {"node_id":"tungsten_material","activity_type":"produce","weight":0.3},
        {"node_id":"ferromanganese","activity_type":"produce","weight":0.35},
        {"node_id":"ferrochrome","activity_type":"produce","weight":0.35}
    ]},
    {"ts_code":"600675.SH","name":"中华企业","industry":"区域地产","main_business":"房地产投资及其高科技开发,智能化物业管理和商品房经营租赁等业务.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.4},
        {"node_id":"smart_property_management","activity_type":"operate","weight":0.3},
        {"node_id":"commercial_housing_rental","activity_type":"operate","weight":0.3}
    ]},
    {"ts_code":"600676.SH","name":"交运股份","industry":"汽车配件","main_business":"主营业务为运输业与物流服务,汽车零部件制造与汽车后服务及水上旅游服务.","exposures":[
        {"node_id":"logistics_service","activity_type":"operate","weight":0.25},
        {"node_id":"automotive_part","activity_type":"manufacture","weight":0.25},
        {"node_id":"automotive_maintenance_service","activity_type":"provide_service","weight":0.25},
        {"node_id":"water_tourism_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600678.SH","name":"ST金顶","industry":"水泥","main_business":"水泥,混凝土.","exposures":[
        {"node_id":"cement","activity_type":"produce","weight":0.5},
        {"node_id":"ready_mixed_concrete","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600679.SH","name":"上海凤凰","industry":"文教休闲","main_business":"主营收入为自行车及零件(含电动车),医疗器械,酒店服务,房屋租赁等","exposures":[
        {"node_id":"bicycle","activity_type":"produce","weight":0.25},
        {"node_id":"bicycle_part","activity_type":"produce","weight":0.2},
        {"node_id":"electric_bicycle","activity_type":"produce","weight":0.2},
        {"node_id":"medical_device","activity_type":"procure","weight":0.2},
        {"node_id":"hotel","activity_type":"operate","weight":0.15}
    ]},
    {"ts_code":"600681.SH","name":"百川能源","industry":"供气供热","main_business":"主营业务是城镇燃气销售业务,燃气接驳业务和燃气具销售业务","exposures":[
        {"node_id":"city_gas","activity_type":"procure","weight":0.4},
        {"node_id":"city_gas_supply","activity_type":"operate","weight":0.35},
        {"node_id":"gas_appliance","activity_type":"procure","weight":0.25}
    ]},
    {"ts_code":"600682.SH","name":"南京新百","industry":"生物制药","main_business":"主营业务:百货零售.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600683.SH","name":"京投发展","industry":"区域地产","main_business":"主要业务:商业(内贸),外贸进出口.","exposures":[
        {"node_id":"domestic_trade_service","activity_type":"procure","weight":0.5},
        {"node_id":"foreign_trade_service","activity_type":"procure","weight":0.5}
    ]},
]

batch_092_nodes = [
    {"node_id":"ophthalmic_eye_drop","canonical_name_zh":"眼科用滴眼液","canonical_name_en":"Ophthalmic Eye Drop","definition":"用于眼部疾病治疗或保健的液体制剂，通过滴眼方式给药","entity_type":"material","evidence_quote":"珍珠明目滴眼液"},
    {"node_id":"chinese_patent_medicine_liquid","canonical_name_zh":"中成药液体制剂","canonical_name_en":"Chinese Patent Medicine Liquid","definition":"以中药材为原料经提取制成的可供内服或外用的液体制剂","entity_type":"material","evidence_quote":"复方鲜竹沥液"},
    {"node_id":"hydrophilic_aluminum_foil","canonical_name_zh":"亲水铝箔","canonical_name_en":"Hydrophilic Aluminum Foil","definition":"表面经亲水涂层处理的铝箔材料，用于空调换热器等热交换设备","entity_type":"material","evidence_quote":"亲水箔的生产和销售"},
    {"node_id":"tungsten_material","canonical_name_zh":"钨材料","canonical_name_en":"Tungsten Material","definition":"以钨金属为基础的材料产品，包括钨粉、碳化钨、钨合金等","entity_type":"material","evidence_quote":"主要产品:钨系列"},
    {"node_id":"ferromanganese","canonical_name_zh":"锰铁合金","canonical_name_en":"Ferromanganese","definition":"铁与锰的合金材料，主要用于钢铁冶炼中的脱氧剂和合金添加剂","entity_type":"material","evidence_quote":"主要产品:高锰,硅锰"},
    {"node_id":"ferrochrome","canonical_name_zh":"铬铁合金","canonical_name_en":"Ferrochrome","definition":"铁与铬的合金材料，是不锈钢生产的重要原料","entity_type":"material","evidence_quote":"主要产品:铬系列"},
    {"node_id":"smart_property_management","canonical_name_zh":"智能化物业管理服务","canonical_name_en":"Smart Property Management Service","definition":"运用智能化系统为物业提供安防、能耗、设施等综合管理服务","entity_type":"service","evidence_quote":"智能化物业管理和商品房经营租赁等业务"},
    {"node_id":"commercial_housing_rental","canonical_name_zh":"商品房租赁服务","canonical_name_en":"Commercial Housing Rental Service","definition":"将开发的商品房用于长期出租经营，提供租赁管理和配套服务","entity_type":"service","evidence_quote":"商品房经营租赁等业务"},
    {"node_id":"water_tourism_service","canonical_name_zh":"水上旅游服务","canonical_name_en":"Water Tourism Service","definition":"以水域为载体，为游客提供观光、休闲、娱乐等水上旅游体验服务","entity_type":"service","evidence_quote":"水上旅游服务"},
    {"node_id":"bicycle_part","canonical_name_zh":"自行车零部件","canonical_name_en":"Bicycle Part","definition":"构成自行车整车的各类零部件，包括车架、轮组、传动系统、制动系统等","entity_type":"component","evidence_quote":"自行车及零件(含电动车)"},
    {"node_id":"gas_appliance","canonical_name_zh":"燃气具","canonical_name_en":"Gas Appliance","definition":"以燃气为能源的家用或商用器具，包括燃气灶、燃气热水器、燃气壁挂炉等","entity_type":"component","evidence_quote":"燃气具销售业务"},
    {"node_id":"domestic_trade_service","canonical_name_zh":"国内贸易服务","canonical_name_en":"Domestic Trade Service","definition":"在国内市场从事商品采购、分销、批发及零售的贸易服务业务","entity_type":"service","evidence_quote":"商业(内贸)"},
    {"node_id":"foreign_trade_service","canonical_name_zh":"外贸进出口服务","canonical_name_en":"Foreign Trade Service","definition":"从事跨境商品进出口代理、报关、物流及结算等外贸综合服务","entity_type":"service","evidence_quote":"外贸进出口"},
]

batch_092_edges = [
    {"edge_id":"cement_to_concrete","source_id":"cement","target_id":"ready_mixed_concrete","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"水泥是生产混凝土的主要原料","evidence_quote":"水泥,混凝土"},
]

# ============ BATCH 093 DATA ============
batch_093_companies = [
    {"ts_code":"600684.SH","name":"珠江股份","industry":"区域地产","main_business":"房地产开发,销售及物业出租.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.6},
        {"node_id":"commercial_property_operation","activity_type":"operate","weight":0.4}
    ]},
    {"ts_code":"600685.SH","name":"中船防务","industry":"船舶","main_business":"主营业务包括:造船,承包境外机电工程和境内国际招标工程,修船,机电,特种船,压力容器,家具,玻璃钢制品等.","exposures":[
        {"node_id":"shipbuilding","activity_type":"manufacture","weight":0.2},
        {"node_id":"vessel_repair_service","activity_type":"provide_service","weight":0.15},
        {"node_id":"special_vessel","activity_type":"manufacture","weight":0.15},
        {"node_id":"pressure_vessel","activity_type":"manufacture","weight":0.15},
        {"node_id":"frp_product","activity_type":"produce","weight":0.15},
        {"node_id":"marine_furniture","activity_type":"produce","weight":0.2}
    ]},
    {"ts_code":"600686.SH","name":"金龙汽车","industry":"汽车整车","main_business":"客车产品.","exposures":[
        {"node_id":"bus","activity_type":"manufacture","weight":1.0}
    ]},
    {"ts_code":"600688.SH","name":"上海石化","industry":"石油加工","main_business":"主要产品:自制产品,合成纤维,树脂及塑料,中间石化产品,石油产品,贸易及其他项目.","exposures":[
        {"node_id":"petrochemical_product","activity_type":"produce","weight":0.25},
        {"node_id":"synthetic_fiber","activity_type":"produce","weight":0.2},
        {"node_id":"synthetic_resin","activity_type":"produce","weight":0.2},
        {"node_id":"petroleum_product","activity_type":"produce","weight":0.2},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.15}
    ]},
    {"ts_code":"600689.SH","name":"上海三毛","industry":"综合类","main_business":"毛纺.","exposures":[
        {"node_id":"wool_textile","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600690.SH","name":"海尔智家","industry":"家用电器","main_business":"主要产品:电冰箱,空调器.","exposures":[
        {"node_id":"refrigerator","activity_type":"manufacture","weight":0.5},
        {"node_id":"air_conditioner","activity_type":"manufacture","weight":0.5}
    ]},
    {"ts_code":"600691.SH","name":"潞化科技","industry":"农药化肥","main_business":"尿素,甲醇,碳酸氢铵,氯化铵,复合肥,二甲醚,纯碱,三聚氰胺,浓硝酸,稀硝酸,硝酸钠,亚硝酸钠,间苯二胺,正丁醛,异丁醛,辛醇,环己酮等化工","exposures":[
        {"node_id":"urea","activity_type":"produce","weight":0.1},
        {"node_id":"methanol","activity_type":"produce","weight":0.1},
        {"node_id":"ammonium_bicarbonate","activity_type":"produce","weight":0.05},
        {"node_id":"ammonium_chloride","activity_type":"produce","weight":0.05},
        {"node_id":"compound_fertilizer","activity_type":"produce","weight":0.05},
        {"node_id":"dimethyl_ether","activity_type":"produce","weight":0.05},
        {"node_id":"soda_ash","activity_type":"produce","weight":0.05},
        {"node_id":"melamine","activity_type":"produce","weight":0.05},
        {"node_id":"nitric_acid","activity_type":"produce","weight":0.1},
        {"node_id":"sodium_nitrate","activity_type":"produce","weight":0.05},
        {"node_id":"sodium_nitrite","activity_type":"produce","weight":0.05},
        {"node_id":"m_phenylenediamine","activity_type":"produce","weight":0.05},
        {"node_id":"n_butylaldehyde","activity_type":"produce","weight":0.05},
        {"node_id":"isobutylaldehyde","activity_type":"produce","weight":0.05},
        {"node_id":"octanol","activity_type":"produce","weight":0.05},
        {"node_id":"cyclohexanone","activity_type":"produce","weight":0.05},
        {"node_id":"special_chemical","activity_type":"produce","weight":0.1}
    ]},
    {"ts_code":"600692.SH","name":"亚通股份","industry":"区域地产","main_business":"主要业务:内河客滚沿海客滚运输,沿海化工品运输,陆上出租汽车运输.","exposures":[
        {"node_id":"inland_river_ferry","activity_type":"operate","weight":0.35},
        {"node_id":"coastal_chemical_transport","activity_type":"operate","weight":0.35},
        {"node_id":"taxi_operation_service","activity_type":"operate","weight":0.3}
    ]},
    {"ts_code":"600693.SH","name":"东百集团","industry":"百货","main_business":"主要业务:商业零售业,进出口贸易,房地产开发.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":0.4},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.3},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.3}
    ]},
    {"ts_code":"600694.SH","name":"大商股份","industry":"百货","main_business":"主营业务:商品零售.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":1.0}
    ]},
]

batch_093_nodes = [
    {"node_id":"special_vessel","canonical_name_zh":"特种船舶","canonical_name_en":"Special Vessel","definition":"为特定用途设计建造的船舶，如工程船、科考船、破冰船、液化气运输船等","entity_type":"system","evidence_quote":"特种船"},
    {"node_id":"frp_product","canonical_name_zh":"玻璃钢制品","canonical_name_en":"FRP Product","definition":"以玻璃纤维及其制品为增强材料、合成树脂为基体材料的复合材料制品","entity_type":"component","evidence_quote":"玻璃钢制品"},
    {"node_id":"marine_furniture","canonical_name_zh":"船舶家具","canonical_name_en":"Marine Furniture","definition":"专门为船舶舱室设计制造的家具，具有防火、防腐蚀、固定安装等特性","entity_type":"component","evidence_quote":"家具"},
    {"node_id":"synthetic_fiber","canonical_name_zh":"合成纤维","canonical_name_en":"Synthetic Fiber","definition":"以石油、天然气等为原料，经化学合成和纺丝工艺制成的人工纤维","entity_type":"material","evidence_quote":"合成纤维"},
    {"node_id":"petroleum_product","canonical_name_zh":"石油产品","canonical_name_en":"Petroleum Product","definition":"以原油为原料经炼制加工得到的各类产品，包括汽油、柴油、润滑油、石蜡等","entity_type":"material","evidence_quote":"石油产品"},
    {"node_id":"wool_textile","canonical_name_zh":"毛纺织品","canonical_name_en":"Wool Textile","definition":"以羊毛或其他动物毛为原料经纺纱织造制成的纺织品","entity_type":"material","evidence_quote":"毛纺"},
    {"node_id":"ammonium_bicarbonate","canonical_name_zh":"碳酸氢铵","canonical_name_en":"Ammonium Bicarbonate","definition":"一种白色结晶性氮肥，也可用作食品膨松剂和分析试剂","entity_type":"material","evidence_quote":"碳酸氢铵"},
    {"node_id":"ammonium_chloride","canonical_name_zh":"氯化铵","canonical_name_en":"Ammonium Chloride","definition":"一种无机化合物，可用作氮肥、干电池电解质和金属焊接助熔剂","entity_type":"material","evidence_quote":"氯化铵"},
    {"node_id":"dimethyl_ether","canonical_name_zh":"二甲醚","canonical_name_en":"Dimethyl Ether","definition":"一种清洁燃料和化工原料，可由甲醇脱水制得，用作气雾推进剂和替代燃料","entity_type":"material","evidence_quote":"二甲醚"},
    {"node_id":"melamine","canonical_name_zh":"三聚氰胺","canonical_name_en":"Melamine","definition":"一种有机化合物，主要用于生产三聚氰胺甲醛树脂，也可用于阻燃剂和涂料","entity_type":"material","evidence_quote":"三聚氰胺"},
    {"node_id":"sodium_nitrate","canonical_name_zh":"硝酸钠","canonical_name_en":"Sodium Nitrate","definition":"一种无机盐，可用作氮肥、金属表面处理剂和食品添加剂（防腐剂）","entity_type":"material","evidence_quote":"硝酸钠"},
    {"node_id":"sodium_nitrite","canonical_name_zh":"亚硝酸钠","canonical_name_en":"Sodium Nitrite","definition":"一种无机盐，主要用于染料工业、金属表面处理及肉制品发色剂","entity_type":"material","evidence_quote":"亚硝酸钠"},
    {"node_id":"m_phenylenediamine","canonical_name_zh":"间苯二胺","canonical_name_en":"m-Phenylenediamine","definition":"一种重要的有机中间体，主要用于生产染料、环氧树脂固化剂和芳纶纤维","entity_type":"material","evidence_quote":"间苯二胺"},
    {"node_id":"n_butylaldehyde","canonical_name_zh":"正丁醛","canonical_name_en":"n-Butylaldehyde","definition":"一种有机化合物，是重要的化工中间体，用于生产增塑剂、溶剂和香料","entity_type":"material","evidence_quote":"正丁醛"},
    {"node_id":"isobutylaldehyde","canonical_name_zh":"异丁醛","canonical_name_en":"Isobutylaldehyde","definition":"一种有机化合物，用于生产新戊二醇、异丁酸和香精香料等","entity_type":"material","evidence_quote":"异丁醛"},
    {"node_id":"octanol","canonical_name_zh":"辛醇","canonical_name_en":"Octanol","definition":"一种重要的有机化工原料，主要用于生产增塑剂、表面活性剂和溶剂","entity_type":"material","evidence_quote":"辛醇"},
    {"node_id":"cyclohexanone","canonical_name_zh":"环己酮","canonical_name_en":"Cyclohexanone","definition":"一种有机化合物，是生产己内酰胺和己二酸的重要中间体，用于尼龙制造","entity_type":"material","evidence_quote":"环己酮"},
    {"node_id":"inland_river_ferry","canonical_name_zh":"内河客滚运输服务","canonical_name_en":"Inland River Ferry Service","definition":"在内河水域提供旅客和车辆滚装运输的服务业务","entity_type":"service","evidence_quote":"内河客滚沿海客滚运输"},
    {"node_id":"coastal_chemical_transport","canonical_name_zh":"沿海化工品运输服务","canonical_name_en":"Coastal Chemical Transport Service","definition":"在沿海航线从事危险化学品和化工产品海上运输的服务业务","entity_type":"service","evidence_quote":"沿海化工品运输"},
]

batch_093_edges = [
    {"edge_id":"urea_to_compound_fertilizer","source_id":"urea","target_id":"compound_fertilizer","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"尿素是生产复合肥的主要氮源原料","evidence_quote":"尿素,复合肥"},
    {"edge_id":"methanol_to_dimethyl_ether","source_id":"methanol","target_id":"dimethyl_ether","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"甲醇经脱水反应可制得二甲醚","evidence_quote":"甲醇,二甲醚"},
]

# ============ BATCH 094 DATA ============
batch_094_companies = [
    {"ts_code":"600696.SH","name":"*ST岩石","industry":"白酒","main_business":"主营业务:房地产综合开发,商品房销售,商场物业出租及相应物业管理.","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.6},
        {"node_id":"commercial_property_operation","activity_type":"operate","weight":0.4}
    ]},
    {"ts_code":"600697.SH","name":"欧亚集团","industry":"百货","main_business":"主要业务:商业,租赁服务.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":0.5},
        {"node_id":"commercial_property_operation","activity_type":"operate","weight":0.5}
    ]},
    {"ts_code":"600698.SH","name":"湖南天雁","industry":"汽车配件","main_business":"涡轮增压器,发动机进排气门及冷却风扇等发动机零部件的生产和销售","exposures":[
        {"node_id":"turbocharger","activity_type":"produce","weight":0.4},
        {"node_id":"engine_valve","activity_type":"produce","weight":0.3},
        {"node_id":"engine_cooling_fan","activity_type":"produce","weight":0.3}
    ]},
    {"ts_code":"600699.SH","name":"均胜电子","industry":"汽车配件","main_business":"主营业务:汽车零部件","exposures":[
        {"node_id":"automotive_part","activity_type":"manufacture","weight":1.0}
    ]},
    {"ts_code":"600702.SH","name":"舍得酒业","industry":"白酒","main_business":"沱牌酒系列,沱牌大曲系列.主营业务是白酒的制造和销售","exposures":[
        {"node_id":"baijiu","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600703.SH","name":"三安光电","industry":"半导体","main_business":"主营业务:LED外延片及芯片的研发,生产和销售.","exposures":[
        {"node_id":"led_epitaxial_wafer","activity_type":"produce","weight":0.5},
        {"node_id":"led_chip","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600704.SH","name":"物产中大","industry":"仓储物流","main_business":"外贸,房地产.","exposures":[
        {"node_id":"foreign_trade_service","activity_type":"procure","weight":0.5},
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.5}
    ]},
    {"ts_code":"600706.SH","name":"曲江文旅","industry":"旅游景点","main_business":"主营业务:景区运营管理业务,酒店餐饮管理业务,旅行社业务,演出演艺业务,文化旅游商品业务,其他新型旅游业务及园林绿化业务.","exposures":[
        {"node_id":"scenic_area_operation_service","activity_type":"operate","weight":0.2},
        {"node_id":"hotel_operation_service","activity_type":"operate","weight":0.15},
        {"node_id":"travel_agency_service","activity_type":"provide_service","weight":0.15},
        {"node_id":"performance_service","activity_type":"provide_service","weight":0.15},
        {"node_id":"cultural_tourism_product","activity_type":"procure","weight":0.15},
        {"node_id":"scenic_area","activity_type":"operate","weight":0.2}
    ]},
    {"ts_code":"600707.SH","name":"彩虹股份","industry":"元器件","main_business":"主营业务:液晶基板玻璃的研发,生产与销售.","exposures":[
        {"node_id":"lcd_substrate_glass","activity_type":"produce","weight":1.0}
    ]},
    {"ts_code":"600708.SH","name":"光明地产","industry":"全国地产","main_business":"主营业务:房地产综合开发经营,物流产业链","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":0.6},
        {"node_id":"logistics_service","activity_type":"operate","weight":0.4}
    ]},
]

batch_094_nodes = [
    {"node_id":"turbocharger","canonical_name_zh":"涡轮增压器","canonical_name_en":"Turbocharger","definition":"利用发动机排气能量驱动涡轮，压缩进气以提高发动机功率密度的增压装置","entity_type":"component","evidence_quote":"涡轮增压器"},
    {"node_id":"engine_valve","canonical_name_zh":"发动机进排气门","canonical_name_en":"Engine Valve","definition":"控制发动机气缸进气和排气的关键部件，由气门、气门座、弹簧等组成","entity_type":"component","evidence_quote":"发动机进排气门"},
    {"node_id":"engine_cooling_fan","canonical_name_zh":"发动机冷却风扇","canonical_name_en":"Engine Cooling Fan","definition":"用于强制空气流过散热器，帮助发动机维持正常工作温度的风扇组件","entity_type":"component","evidence_quote":"冷却风扇等发动机零部件"},
    {"node_id":"led_epitaxial_wafer","canonical_name_zh":"LED外延片","canonical_name_en":"LED Epitaxial Wafer","definition":"在蓝宝石或碳化硅衬底上通过外延生长工艺制备的含有发光层结构的晶圆片","entity_type":"material","evidence_quote":"LED外延片及芯片的研发,生产和销售"},
    {"node_id":"led_chip","canonical_name_zh":"LED芯片","canonical_name_en":"LED Chip","definition":"将外延片经光刻、刻蚀、蒸镀等工艺制成的具有电致发光功能的半导体芯片","entity_type":"component","evidence_quote":"LED外延片及芯片的研发,生产和销售"},
    {"node_id":"scenic_area_operation_service","canonical_name_zh":"景区运营管理服务","canonical_name_en":"Scenic Area Operation Service","definition":"为旅游景区提供日常运营、游客服务、设施维护、营销推广等综合管理服务","entity_type":"service","evidence_quote":"景区运营管理业务"},
    {"node_id":"travel_agency_service","canonical_name_zh":"旅行社服务","canonical_name_en":"Travel Agency Service","definition":"为游客提供旅游线路设计、票务预订、导游接待等综合性旅行服务","entity_type":"service","evidence_quote":"旅行社业务"},
    {"node_id":"performance_service","canonical_name_zh":"演出演艺服务","canonical_name_en":"Performance Service","definition":"为景区或文化场所提供文艺演出、演艺活动策划及执行的服务业务","entity_type":"service","evidence_quote":"演出演艺业务"},
    {"node_id":"cultural_tourism_product","canonical_name_zh":"文化旅游商品","canonical_name_en":"Cultural Tourism Product","definition":"具有地域文化特色的旅游纪念商品，包括文创产品、地方特产、手工艺品等","entity_type":"material","evidence_quote":"文化旅游商品业务"},
    {"node_id":"lcd_substrate_glass","canonical_name_zh":"液晶基板玻璃","canonical_name_en":"LCD Substrate Glass","definition":"用于液晶显示面板制造的特种玻璃基板，需具备高平整度、低热膨胀系数等特性","entity_type":"material","evidence_quote":"液晶基板玻璃的研发,生产与销售"},
]

batch_094_edges = [
    {"edge_id":"turbocharger_to_engine","source_id":"turbocharger","target_id":"auto_engine","edge_namespace":"industrial_flow","edge_type":"composition","description":"涡轮增压器是汽车发动机总成的组成部分","evidence_quote":"涡轮增压器等发动机零部件"},
    {"edge_id":"engine_valve_to_engine","source_id":"engine_valve","target_id":"auto_engine","edge_namespace":"industrial_flow","edge_type":"composition","description":"进排气门是汽车发动机总成的组成部分","evidence_quote":"发动机进排气门等发动机零部件"},
    {"edge_id":"cooling_fan_to_engine","source_id":"engine_cooling_fan","target_id":"auto_engine","edge_namespace":"industrial_flow","edge_type":"composition","description":"冷却风扇是汽车发动机总成的组成部分","evidence_quote":"冷却风扇等发动机零部件"},
    {"edge_id":"led_wafer_to_chip","source_id":"led_epitaxial_wafer","target_id":"led_chip","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"LED外延片经加工制成LED芯片","evidence_quote":"LED外延片及芯片的研发,生产和销售"},
    {"edge_id":"lcd_glass_to_panel","source_id":"lcd_substrate_glass","target_id":"lcd_panel","edge_namespace":"industrial_flow","edge_type":"material_flow","description":"液晶基板玻璃是液晶显示面板的核心基材","evidence_quote":"液晶基板玻璃的研发,生产与销售"},
]

# ============ BATCH 095 DATA ============
batch_095_companies = [
    {"ts_code":"600710.SH","name":"苏美达","industry":"商贸代理","main_business":"公司主营业务包括产业链,供应链两大类.产业链主要产品或服务包括:船舶制造与航运,柴油发电机组,户外动力设备(OPE),清洁能源(含光伏产品).","exposures":[
        {"node_id":"shipbuilding","activity_type":"manufacture","weight":0.25},
        {"node_id":"diesel_generator_set","activity_type":"produce","weight":0.25},
        {"node_id":"outdoor_power_equipment","activity_type":"produce","weight":0.25},
        {"node_id":"pv_product","activity_type":"procure","weight":0.25}
    ]},
    {"ts_code":"600711.SH","name":"盛屯矿业","industry":"小金属","main_business":"主要业务为有色金属采选及综合贸易业务金属金融服务","exposures":[
        {"node_id":"nonferrous_mining_service","activity_type":"provide_service","weight":0.5},
        {"node_id":"trade_agent","activity_type":"procure","weight":0.25},
        {"node_id":"metal_financial_service","activity_type":"provide_service","weight":0.25}
    ]},
    {"ts_code":"600712.SH","name":"南宁百货","industry":"百货","main_business":"主营业务为批发和零售贸易.","exposures":[
        {"node_id":"department_store","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600713.SH","name":"南京医药","industry":"医药商业","main_business":"流通业,制造业.","exposures":[
        {"node_id":"pharmaceutical_distribution","activity_type":"provide_service","weight":0.5},
        {"node_id":"pharmaceutical_manufacturing","activity_type":"manufacture","weight":0.5}
    ]},
    {"ts_code":"600714.SH","name":"金瑞矿业","industry":"化工原料","main_business":"锶系列产品的研究,生产,开发,加工与销售.煤炭的生产与销售.","exposures":[
        {"node_id":"strontium_compound","activity_type":"produce","weight":0.5},
        {"node_id":"coal","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600715.SH","name":"文投控股","industry":"影视音像","main_business":"汽车车身零部件.","exposures":[
        {"node_id":"film_tv_production_service","activity_type":"provide_service","weight":0.5},
        {"node_id":"automotive_body_part","activity_type":"produce","weight":0.5}
    ]},
    {"ts_code":"600716.SH","name":"凤凰股份","industry":"区域地产","main_business":"房地产投资及其他实业投资","exposures":[
        {"node_id":"real_estate_development","activity_type":"operate","weight":1.0}
    ]},
    {"ts_code":"600717.SH","name":"天津港","industry":"港口","main_business":"主营业务为商品储存,中转联运,汽车运输;装卸搬运;集装箱搬运,拆装箱及相关业务;货运代理;劳务服务;商业及各类物资的批发,零售;经济信息咨询","exposures":[
        {"node_id":"warehouse_service","activity_type":"operate","weight":0.15},
        {"node_id":"logistics_service","activity_type":"operate","weight":0.15},
        {"node_id":"port_operation_service","activity_type":"operate","weight":0.2},
        {"node_id":"container_transport_service","activity_type":"operate","weight":0.2},
        {"node_id":"freight_forwarding_service","activity_type":"provide_service","weight":0.15},
        {"node_id":"road_transport_vehicle","activity_type":"operate","weight":0.15}
    ]},
    {"ts_code":"600718.SH","name":"东软集团","industry":"软件服务","main_business":"主营业务:软件及系统集成,数字医疗.","exposures":[
        {"node_id":"software_development_service","activity_type":"provide_service","weight":0.5},
        {"node_id":"digital_medical_system","activity_type":"provide_service","weight":0.5}
    ]},
    {"ts_code":"600719.SH","name":"大连热电","industry":"供气供热","main_business":"电力,热力.","exposures":[
        {"node_id":"electricity_power","activity_type":"produce","weight":0.5},
        {"node_id":"heat_supply","activity_type":"produce","weight":0.5}
    ]},
]

batch_095_nodes = [
    {"node_id":"diesel_generator_set","canonical_name_zh":"柴油发电机组","canonical_name_en":"Diesel Generator Set","definition":"以柴油发动机为动力驱动同步发电机发电的成套发电设备","entity_type":"system","evidence_quote":"柴油发电机组"},
    {"node_id":"outdoor_power_equipment","canonical_name_zh":"户外动力设备","canonical_name_en":"Outdoor Power Equipment","definition":"用于户外作业场景的移动式动力机械设备，包括发电机、水泵、割草机等","entity_type":"system","evidence_quote":"户外动力设备(OPE)"},
    {"node_id":"pv_product","canonical_name_zh":"光伏产品","canonical_name_en":"Photovoltaic Product","definition":"利用太阳能光伏发电技术制造的各类产品，包括光伏组件、逆变器、支架系统等","entity_type":"material","evidence_quote":"清洁能源(含光伏产品)"},
    {"node_id":"nonferrous_mining_service","canonical_name_zh":"有色金属采选服务","canonical_name_en":"Nonferrous Mining Service","definition":"为有色金属矿山提供勘探、开采、选矿等专业技术服务","entity_type":"service","evidence_quote":"有色金属采选"},
    {"node_id":"metal_financial_service","canonical_name_zh":"金属金融服务","canonical_name_en":"Metal Financial Service","definition":"围绕金属产业链提供的供应链金融、套期保值、贸易融资等金融服务","entity_type":"service","evidence_quote":"金属金融服务"},
    {"node_id":"pharmaceutical_manufacturing","canonical_name_zh":"医药制造服务","canonical_name_en":"Pharmaceutical Manufacturing Service","definition":"从事药品原料药及制剂的研发、生产和代加工制造服务","entity_type":"service","evidence_quote":"流通业,制造业"},
    {"node_id":"strontium_compound","canonical_name_zh":"锶化合物","canonical_name_en":"Strontium Compound","definition":"以锶元素为核心的各类化合物产品，包括碳酸锶、硝酸锶、氯化锶等","entity_type":"material","evidence_quote":"锶系列产品"},
    {"node_id":"automotive_body_part","canonical_name_zh":"汽车车身零部件","canonical_name_en":"Automotive Body Part","definition":"构成汽车车身结构的各种冲压件、覆盖件及内外饰零部件","entity_type":"component","evidence_quote":"汽车车身零部件"},
    {"node_id":"digital_medical_system","canonical_name_zh":"数字医疗系统","canonical_name_en":"Digital Medical System","definition":"集成医学影像、临床信息、远程诊疗等功能的数字化医疗信息化系统","entity_type":"system","evidence_quote":"数字医疗"},
    {"node_id":"heat_supply","canonical_name_zh":"热力供应服务","canonical_name_en":"Heat Supply Service","definition":"通过热电联产或区域锅炉房向用户供应蒸汽和热水的公用事业服务","entity_type":"service","evidence_quote":"热力"},
    {"node_id":"container_transport_service","canonical_name_zh":"集装箱运输服务","canonical_name_en":"Container Transport Service","definition":"利用标准化集装箱进行货物陆海联运、堆存、装卸及多式联运的服务","entity_type":"service","evidence_quote":"集装箱搬运,拆装箱及相关业务"},
]

batch_095_edges = [
    {"edge_id":"diesel_generator_to_ship","source_id":"diesel_generator_set","target_id":"ship","edge_namespace":"industrial_flow","edge_type":"composition","description":"柴油发电机组可作为船舶辅助发电设备","evidence_quote":"船舶制造与航运,柴油发电机组"},
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
    # Fix escaped braces back
    content = content.replace("{{BASE}}", "{BASE}")
    content = content.replace("{{path}}", "{path}")
    content = content.replace("{{r.status_code}}", "{r.status_code}")
    content = content.replace("{{r.text[:200]}}", "{r.text[:200]}")
    content = content.replace("{{r.text[:300]}}", "{r.text[:300]}")
    content = content.replace("{{BASE}}/nodes", "{BASE}/nodes")
    content = content.replace("{{BASE}}/edges", "{BASE}/edges")
    content = content.replace("{{page}}", "{page}")
    content = content.replace("{{page_size}}", "{page_size}")
    content = content.replace("{{len(nodes_to_create)}}", "{len(nodes_to_create)}")
    content = content.replace("{{len(edges_to_create)}}", "{len(edges_to_create)}")
    content = content.replace("{{len(companies_payload)}}", "{len(companies_payload)}")
    content = content.replace("{{len(exposures_payload)}}", "{len(exposures_payload)}")
    content = content.replace("{{batch_num:03d}}", "{batch_num:03d}")
    content = content.replace("{{batch_num}}", "{batch_num}")
    content = content.replace("{{batch_num}}_graph", "{batch_num}_graph")
    content = content.replace("{{batch_num}}_biz", "{batch_num}_biz")

    out_path = f"tmp_script/tmp_submit_batch_{batch_num:03d}.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")


def main():
    os.makedirs("tmp_script", exist_ok=True)
    generate_batch(91, batch_091_companies, batch_091_nodes, batch_091_edges)
    generate_batch(92, batch_092_companies, batch_092_nodes, batch_092_edges)
    generate_batch(93, batch_093_companies, batch_093_nodes, batch_093_edges)
    generate_batch(94, batch_094_companies, batch_094_nodes, batch_094_edges)
    generate_batch(95, batch_095_companies, batch_095_nodes, batch_095_edges)
    print("All 5 batch scripts generated.")


if __name__ == "__main__":
    main()
