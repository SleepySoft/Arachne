#!/usr/bin/env python3
"""Generate tmp_submit_batch_076.py through tmp_submit_batch_080.py."""
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

BATCH_076 = {
    "new_nodes": [
        {"node_id": "light_steel_structure", "canonical_name_zh": "轻型钢结构", "definition": "以轻型钢材为主要承重构件的建筑结构体系，具有自重轻、施工快、抗震好的特点", "entity_type": "material"},
        {"node_id": "foam_nickel", "canonical_name_zh": "泡沫镍", "definition": "具有三维多孔网状结构的镍材料，用于电池电极、催化剂载体和过滤材料", "entity_type": "material"},
        {"node_id": "lithium_bromide_chiller", "canonical_name_zh": "溴化锂制冷机", "definition": "以溴化锂水溶液为工质的吸收式制冷设备，利用热能驱动实现制冷", "entity_type": "device"},
        {"node_id": "heat_exchanger", "canonical_name_zh": "高效换热器", "definition": "实现两种或多种流体之间热量传递的高效节能设备，广泛应用于电力、化工、暖通等领域", "entity_type": "device"},
        {"node_id": "styrene", "canonical_name_zh": "苯乙烯", "definition": "重要的基础有机化工原料，用于生产聚苯乙烯、ABS树脂、合成橡胶等高分子材料", "entity_type": "material"},
        {"node_id": "pyrethroid", "canonical_name_zh": "菊酯", "definition": "模拟天然除虫菊素结构合成的仿生杀虫剂，具有高效、低毒、低残留的特点", "entity_type": "material"},
        {"node_id": "optical_fiber_cable", "canonical_name_zh": "光纤光缆", "definition": "以光纤为传输介质、用于通信信号长距离传输的线缆产品", "entity_type": "component"},
        {"node_id": "corticosteroid", "canonical_name_zh": "皮质激素", "definition": "由肾上腺皮质分泌的具有抗炎、免疫抑制等作用的甾体激素类药物", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "light_steel_structure_to_construction", "from_node": "light_steel_structure", "to_node": "construction", "edge_type": "material_flow", "description": "轻型钢结构是现代建筑工程建设的重要结构材料"},
        {"edge_id": "foam_nickel_to_battery", "from_node": "foam_nickel", "to_node": "battery", "edge_type": "composition", "description": "泡沫镍是镍氢电池和镍镉电池电极的核心基板材料"},
        {"edge_id": "optical_fiber_cable_to_communication_equipment", "from_node": "optical_fiber_cable", "to_node": "communication_equipment", "edge_type": "composition", "description": "光纤光缆是通信网络传输系统的核心物理介质"},
    ],
    "companies": [
        {"company_id": "hangxiao", "name_zh": "杭萧钢构股份有限公司", "stock_code": "600477.SH", "province": "浙江", "city": "杭州市", "industry": "钢加工", "main_business": "轻型钢结构,多高层钢结构,商品销售"},
        {"company_id": "corun", "name_zh": "湖南科力远新能源股份有限公司", "stock_code": "600478.SH", "province": "湖南", "city": "长沙市", "industry": "电气设备", "main_business": "泡沫镍"},
        {"company_id": "qianjin_pharma", "name_zh": "株洲千金药业股份有限公司", "stock_code": "600479.SH", "province": "湖南", "city": "株洲市", "industry": "中成药", "main_business": "妇科千金片等中成药的生产与销售"},
        {"company_id": "lingyun", "name_zh": "凌云工业股份有限公司", "stock_code": "600480.SH", "province": "河北", "city": "保定市", "industry": "汽车配件", "main_business": "汽车金属及塑料零部件,塑料管道系统"},
        {"company_id": "shuangliang", "name_zh": "双良节能系统股份有限公司", "stock_code": "600481.SH", "province": "江苏", "city": "无锡市", "industry": "电气设备", "main_business": "溴化锂制冷机,高效换热器,空冷器等换热设备和苯乙烯,聚苯乙烯产品"},
        {"company_id": "funeng", "name_zh": "福建福能股份有限公司", "stock_code": "600483.SH", "province": "福建", "city": "福州市", "industry": "新型电力", "main_business": "电力和纺织业"},
        {"company_id": "yangnong", "name_zh": "江苏扬农化工股份有限公司", "stock_code": "600486.SH", "province": "江苏", "city": "扬州市", "industry": "农药化肥", "main_business": "卫生用菊酯,农用菊酯"},
        {"company_id": "hengtong", "name_zh": "江苏亨通光电股份有限公司", "stock_code": "600487.SH", "province": "江苏", "city": "苏州市", "industry": "通信设备", "main_business": "通信网络业务,能源互联业务"},
        {"company_id": "tianjin_pharma", "name_zh": "津药药业股份有限公司", "stock_code": "600488.SH", "province": "天津", "city": "天津市", "industry": "化学制药", "main_business": "皮质激素,类原料药,心血管类,原料药,水针剂"},
        {"company_id": "zhongjin_gold", "name_zh": "中金黄金股份有限公司", "stock_code": "600489.SH", "province": "北京", "city": "北京市", "industry": "黄金", "main_business": "黄金的生产与销售"},
    ],
    "exposures": [
        {"exposure_id": "hangxiao_produce_light_steel_structure", "company_id": "hangxiao", "node_id": "light_steel_structure", "activity_type": "produce", "role": "轻型钢结构生产商", "weight": 0.95},
        {"exposure_id": "hangxiao_produce_steel_structure", "company_id": "hangxiao", "node_id": "steel_structure", "activity_type": "produce", "role": "钢结构生产商", "weight": 0.9},
        {"exposure_id": "hangxiao_produce_steel", "company_id": "hangxiao", "node_id": "steel", "activity_type": "produce", "role": "钢材加工商", "weight": 0.85},
        {"exposure_id": "corun_produce_foam_nickel", "company_id": "corun", "node_id": "foam_nickel", "activity_type": "produce", "role": "泡沫镍生产商", "weight": 0.95},
        {"exposure_id": "corun_produce_battery_material", "company_id": "corun", "node_id": "battery_material", "activity_type": "produce", "role": "电池材料生产商", "weight": 0.9},
        {"exposure_id": "qianjin_pharma_produce_gynecology_chinese_patent_medicine", "company_id": "qianjin_pharma", "node_id": "gynecology_chinese_patent_medicine", "activity_type": "produce", "role": "妇科中成药生产商", "weight": 0.95},
        {"exposure_id": "qianjin_pharma_produce_chinese_patent_medicine", "company_id": "qianjin_pharma", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9},
        {"exposure_id": "lingyun_manufacture_automobile_plastic_part", "company_id": "lingyun", "node_id": "automobile_plastic_part", "activity_type": "manufacture", "role": "汽车塑料零部件制造商", "weight": 0.95},
        {"exposure_id": "lingyun_manufacture_automobile_part", "company_id": "lingyun", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车零部件制造商", "weight": 0.9},
        {"exposure_id": "lingyun_manufacture_plastic_pipe", "company_id": "lingyun", "node_id": "plastic_pipe", "activity_type": "manufacture", "role": "塑料管道制造商", "weight": 0.85},
        {"exposure_id": "shuangliang_manufacture_lithium_bromide_chiller", "company_id": "shuangliang", "node_id": "lithium_bromide_chiller", "activity_type": "manufacture", "role": "溴化锂制冷机制造商", "weight": 0.95},
        {"exposure_id": "shuangliang_manufacture_heat_exchanger", "company_id": "shuangliang", "node_id": "heat_exchanger", "activity_type": "manufacture", "role": "换热器制造商", "weight": 0.95},
        {"exposure_id": "shuangliang_manufacture_air_cooler", "company_id": "shuangliang", "node_id": "air_cooler", "activity_type": "manufacture", "role": "空冷器制造商", "weight": 0.9},
        {"exposure_id": "shuangliang_produce_styrene", "company_id": "shuangliang", "node_id": "styrene", "activity_type": "produce", "role": "苯乙烯生产商", "weight": 0.9},
        {"exposure_id": "funeng_operate_power_generation", "company_id": "funeng", "node_id": "power_generation", "activity_type": "operate", "role": "电力运营商", "weight": 0.95},
        {"exposure_id": "funeng_produce_textile_product", "company_id": "funeng", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.85},
        {"exposure_id": "yangnong_produce_pyrethroid", "company_id": "yangnong", "node_id": "pyrethroid", "activity_type": "produce", "role": "菊酯生产商", "weight": 0.95},
        {"exposure_id": "yangnong_produce_pesticide", "company_id": "yangnong", "node_id": "pesticide", "activity_type": "produce", "role": "农药生产商", "weight": 0.9},
        {"exposure_id": "hengtong_manufacture_optical_fiber_cable", "company_id": "hengtong", "node_id": "optical_fiber_cable", "activity_type": "manufacture", "role": "光纤光缆制造商", "weight": 0.95},
        {"exposure_id": "hengtong_manufacture_communication_equipment", "company_id": "hengtong", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.9},
        {"exposure_id": "tianjin_pharma_produce_corticosteroid", "company_id": "tianjin_pharma", "node_id": "corticosteroid", "activity_type": "produce", "role": "皮质激素生产商", "weight": 0.95},
        {"exposure_id": "tianjin_pharma_produce_pharmaceutical", "company_id": "tianjin_pharma", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "zhongjin_gold_produce_gold", "company_id": "zhongjin_gold", "node_id": "gold", "activity_type": "produce", "role": "黄金生产商", "weight": 0.95},
        {"exposure_id": "zhongjin_gold_produce_nonferrous_metal", "company_id": "zhongjin_gold", "node_id": "nonferrous_metal", "activity_type": "produce", "role": "有色金属生产商", "weight": 0.9},
    ],
}

BATCH_077 = {
    "new_nodes": [
        {"node_id": "nonferrous_metal_mining", "canonical_name_zh": "有色金属采选", "definition": "对有色金属矿床进行开采和选矿加工的生产活动", "entity_type": "service"},
        {"node_id": "civil_construction", "canonical_name_zh": "土建施工", "definition": "房屋建筑、道路桥梁等土木工程的现场施工建造活动", "entity_type": "service"},
        {"node_id": "textile_weaving", "canonical_name_zh": "纺织织造", "definition": "将纱线通过织机交织成布匹的纺织加工工序", "entity_type": "service"},
        {"node_id": "train_axle", "canonical_name_zh": "车轴", "definition": "铁路车辆上用于安装车轮并承受载荷的圆柱形关键零部件", "entity_type": "component"},
        {"node_id": "agricultural_machinery", "canonical_name_zh": "农业机械", "definition": "用于农业生产过程的机械设备，包括拖拉机、收割机、播种机等", "entity_type": "system"},
        {"node_id": "germanium_product", "canonical_name_zh": "锗产品", "definition": "以稀有金属锗为原料加工制成的产品，用于光纤、红外光学、半导体等领域", "entity_type": "material"},
        {"node_id": "data_network_product", "canonical_name_zh": "数据网络产品", "definition": "用于构建数据通信网络的设备和系统，包括路由器、交换机等", "entity_type": "device"},
        {"node_id": "pressure_vessel", "canonical_name_zh": "压力容器", "definition": "能够承受一定压力的密闭设备，用于储存或反应气体、液体等介质", "entity_type": "device"},
    ],
    "new_edges": [
        {"edge_id": "train_axle_to_rail_transit", "from_node": "train_axle", "to_node": "rail_transit", "edge_type": "composition", "description": "车轴是轨道交通车辆走行系统的核心组成部件"},
        {"edge_id": "germanium_product_to_semiconductor", "from_node": "germanium_product", "to_node": "semiconductor", "edge_type": "material_flow", "description": "锗是重要的半导体材料，广泛用于制造半导体器件"},
        {"edge_id": "pressure_vessel_to_chemical_industry", "from_node": "pressure_vessel", "to_node": "chemical_industry", "edge_type": "composition", "description": "压力容器是石油化工等化工行业生产过程中的关键装备"},
    ],
    "companies": [
        {"company_id": "pengxin_resources", "name_zh": "鹏欣环球资源股份有限公司", "stock_code": "600490.SH", "province": "上海", "city": "上海市", "industry": "铜", "main_business": "有色金属及贵金属的采选业务,冶炼及销售,以及贸易,新能源及金融"},
        {"company_id": "st_longyuan", "name_zh": "龙元建设集团股份有限公司", "stock_code": "600491.SH", "province": "浙江", "city": "宁波市", "industry": "建筑工程", "main_business": "土建施工,装饰与钢结构,建筑设计及其他"},
        {"company_id": "fengzhu_textile", "name_zh": "福建凤竹纺织科技股份有限公司", "stock_code": "600493.SH", "province": "福建", "city": "泉州市", "industry": "纺织", "main_business": "织造,染纱,染整加工,污水处理"},
        {"company_id": "jinxi_axle", "name_zh": "晋西车轴股份有限公司", "stock_code": "600495.SH", "province": "山西", "city": "太原市", "industry": "运输设备", "main_business": "车轴的生产与销售"},
        {"company_id": "jinggong_steel", "name_zh": "长江精工钢结构(集团)股份有限公司", "stock_code": "600496.SH", "province": "安徽", "city": "六安市", "industry": "钢加工", "main_business": "钢结构行业,农业机械行业"},
        {"company_id": "chihong", "name_zh": "云南驰宏锌锗股份有限公司", "stock_code": "600497.SH", "province": "云南", "city": "曲靖市", "industry": "铅锌", "main_business": "锌产品,铅产品,银产品,锗产品"},
        {"company_id": "fiberhome", "name_zh": "烽火通信科技股份有限公司", "stock_code": "600498.SH", "province": "湖北", "city": "武汉市", "industry": "通信设备", "main_business": "通信设备,光纤,光缆及电缆,数据网络产品"},
        {"company_id": "keda_manufacturing", "name_zh": "科达制造股份有限公司", "stock_code": "600499.SH", "province": "广东", "city": "佛山市", "industry": "专用机械", "main_business": "机械产品,中药产品,自制配件及其他"},
        {"company_id": "sinochem_intl", "name_zh": "中化国际(控股)股份有限公司", "stock_code": "600500.SH", "province": "上海", "city": "上海市", "industry": "塑料", "main_business": "储罐,焦炭等冶金产品,农药及其他商品,化工物流,塑料原料,橡胶及橡胶制品"},
        {"company_id": "aerosun", "name_zh": "航天晨光股份有限公司", "stock_code": "600501.SH", "province": "江苏", "city": "南京市", "industry": "专用机械", "main_business": "专用车类产品,波纹管类产品,压力容器类产品"},
    ],
    "exposures": [
        {"exposure_id": "pengxin_resources_operate_nonferrous_metal_mining", "company_id": "pengxin_resources", "node_id": "nonferrous_metal_mining", "activity_type": "operate", "role": "有色金属采选运营商", "weight": 0.95},
        {"exposure_id": "pengxin_resources_produce_nonferrous_metal", "company_id": "pengxin_resources", "node_id": "nonferrous_metal", "activity_type": "produce", "role": "有色金属生产商", "weight": 0.95},
        {"exposure_id": "pengxin_resources_produce_precious_metal", "company_id": "pengxin_resources", "node_id": "precious_metal", "activity_type": "produce", "role": "贵金属生产商", "weight": 0.9},
        {"exposure_id": "st_longyuan_operate_civil_construction", "company_id": "st_longyuan", "node_id": "civil_construction", "activity_type": "operate", "role": "土建施工运营商", "weight": 0.95},
        {"exposure_id": "st_longyuan_operate_construction", "company_id": "st_longyuan", "node_id": "construction", "activity_type": "operate", "role": "建筑施工运营商", "weight": 0.9},
        {"exposure_id": "st_longyuan_provide_service_building_design", "company_id": "st_longyuan", "node_id": "building_design", "activity_type": "provide_service", "role": "建筑设计服务商", "weight": 0.85},
        {"exposure_id": "fengzhu_textile_operate_textile_weaving", "company_id": "fengzhu_textile", "node_id": "textile_weaving", "activity_type": "operate", "role": "纺织织造运营商", "weight": 0.95},
        {"exposure_id": "fengzhu_textile_produce_textile_product", "company_id": "fengzhu_textile", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品生产商", "weight": 0.9},
        {"exposure_id": "fengzhu_textile_operate_wastewater_treatment", "company_id": "fengzhu_textile", "node_id": "wastewater_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.85},
        {"exposure_id": "jinxi_axle_manufacture_train_axle", "company_id": "jinxi_axle", "node_id": "train_axle", "activity_type": "manufacture", "role": "车轴制造商", "weight": 0.95},
        {"exposure_id": "jinxi_axle_manufacture_rail_transit_equipment", "company_id": "jinxi_axle", "node_id": "rail_transit_equipment", "activity_type": "manufacture", "role": "轨道交通设备制造商", "weight": 0.9},
        {"exposure_id": "jinggong_steel_produce_steel_structure", "company_id": "jinggong_steel", "node_id": "steel_structure", "activity_type": "produce", "role": "钢结构生产商", "weight": 0.95},
        {"exposure_id": "jinggong_steel_manufacture_agricultural_machinery", "company_id": "jinggong_steel", "node_id": "agricultural_machinery", "activity_type": "manufacture", "role": "农业机械制造商", "weight": 0.9},
        {"exposure_id": "chihong_produce_zinc_product", "company_id": "chihong", "node_id": "zinc_product", "activity_type": "produce", "role": "锌产品生产商", "weight": 0.95},
        {"exposure_id": "chihong_produce_lead_product", "company_id": "chihong", "node_id": "lead_product", "activity_type": "produce", "role": "铅产品生产商", "weight": 0.9},
        {"exposure_id": "chihong_produce_silver_product", "company_id": "chihong", "node_id": "silver_product", "activity_type": "produce", "role": "银产品生产商", "weight": 0.9},
        {"exposure_id": "chihong_produce_germanium_product", "company_id": "chihong", "node_id": "germanium_product", "activity_type": "produce", "role": "锗产品生产商", "weight": 0.85},
        {"exposure_id": "fiberhome_manufacture_communication_equipment", "company_id": "fiberhome", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.95},
        {"exposure_id": "fiberhome_manufacture_optical_fiber_cable", "company_id": "fiberhome", "node_id": "optical_fiber_cable", "activity_type": "manufacture", "role": "光纤光缆制造商", "weight": 0.95},
        {"exposure_id": "fiberhome_manufacture_data_network_product", "company_id": "fiberhome", "node_id": "data_network_product", "activity_type": "manufacture", "role": "数据网络产品制造商", "weight": 0.9},
        {"exposure_id": "keda_manufacturing_manufacture_ceramic_machinery", "company_id": "keda_manufacturing", "node_id": "ceramic_machinery", "activity_type": "manufacture", "role": "陶瓷机械制造商", "weight": 0.95},
        {"exposure_id": "keda_manufacturing_produce_chinese_patent_medicine", "company_id": "keda_manufacturing", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中药产品生产商", "weight": 0.85},
        {"exposure_id": "sinochem_intl_provide_service_chemical_logistics", "company_id": "sinochem_intl", "node_id": "chemical_logistics", "activity_type": "provide_service", "role": "化工物流服务商", "weight": 0.9},
        {"exposure_id": "sinochem_intl_produce_plastic_raw_material", "company_id": "sinochem_intl", "node_id": "plastic_raw_material", "activity_type": "produce", "role": "塑料原料生产商", "weight": 0.9},
        {"exposure_id": "sinochem_intl_produce_rubber_product", "company_id": "sinochem_intl", "node_id": "rubber_product", "activity_type": "produce", "role": "橡胶制品生产商", "weight": 0.85},
        {"exposure_id": "aerosun_manufacture_special_vehicle", "company_id": "aerosun", "node_id": "special_vehicle", "activity_type": "manufacture", "role": "专用车制造商", "weight": 0.95},
        {"exposure_id": "aerosun_manufacture_bellows", "company_id": "aerosun", "node_id": "bellows", "activity_type": "manufacture", "role": "波纹管制造商", "weight": 0.9},
        {"exposure_id": "aerosun_manufacture_pressure_vessel", "company_id": "aerosun", "node_id": "pressure_vessel", "activity_type": "manufacture", "role": "压力容器制造商", "weight": 0.9},
    ],
}

BATCH_078 = {
    "new_nodes": [
        {"node_id": "engineering_general_contracting", "canonical_name_zh": "工程总承包", "definition": "承包单位按照合同约定对工程项目的勘察、设计、采购、施工、试运行等实行全过程或若干阶段承包的建设模式", "entity_type": "service"},
        {"node_id": "equity_investment", "canonical_name_zh": "股权投资", "definition": "通过购买企业股权以获取长期资本增值和股息收益的投资活动", "entity_type": "service"},
        {"node_id": "rebar", "canonical_name_zh": "螺纹钢", "definition": "表面带肋的钢筋，广泛用于房屋建筑、桥梁、道路等钢筋混凝土结构中", "entity_type": "material"},
        {"node_id": "leaf_spring", "canonical_name_zh": "汽车板簧", "definition": "汽车悬架系统中使用的多层钢板叠合而成的弹性元件，用于缓冲和减振", "entity_type": "component"},
        {"node_id": "iron_concentrate", "canonical_name_zh": "铁精粉", "definition": "铁矿石经破碎、磨矿、磁选等选矿工艺处理后得到的高品位细粒铁粉", "entity_type": "material"},
        {"node_id": "raw_coal", "canonical_name_zh": "原煤", "definition": "从地下开采出来未经洗选加工的煤炭，是煤炭工业的初级产品", "entity_type": "material"},
        {"node_id": "denim", "canonical_name_zh": "牛仔布", "definition": "一种粗厚的色织棉斜纹布，主要用于制作牛仔裤、夹克等服装", "entity_type": "material"},
        {"node_id": "pharmaceutical_commerce", "canonical_name_zh": "医药商业", "definition": "从事药品、医疗器械等医药产品的批发、零售、物流配送等流通服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "rebar_to_construction", "from_node": "rebar", "to_node": "construction", "edge_type": "material_flow", "description": "螺纹钢是建筑工程钢筋混凝土结构的主要骨架材料"},
        {"edge_id": "leaf_spring_to_automobile", "from_node": "leaf_spring", "to_node": "automobile", "edge_type": "composition", "description": "汽车板簧是汽车悬架系统的关键弹性组件"},
        {"edge_id": "iron_concentrate_to_steel", "from_node": "iron_concentrate", "to_node": "steel", "edge_type": "material_flow", "description": "铁精粉是高炉炼铁的主要原料，经冶炼后成为钢材"},
    ],
    "companies": [
        {"company_id": "anhui_construction", "name_zh": "安徽建工集团股份有限公司", "stock_code": "600502.SH", "province": "安徽", "city": "合肥市", "industry": "建筑工程", "main_business": "工程总承包,房屋建筑,水利水电,市政,公路,桥梁,隧道,港口航道,机电设备安装"},
        {"company_id": "huali_family", "name_zh": "华丽家族股份有限公司", "stock_code": "600503.SH", "province": "上海", "city": "上海市", "industry": "区域地产", "main_business": "股权投资"},
        {"company_id": "xichang_power", "name_zh": "四川西昌电力股份有限公司", "stock_code": "600505.SH", "province": "四川", "city": "西昌市", "industry": "水力发电", "main_business": "电力销售"},
        {"company_id": "unified_co", "name_zh": "统一低碳科技(新疆)股份有限公司", "stock_code": "600506.SH", "province": "新疆", "city": "库尔勒市", "industry": "石油加工", "main_business": "香梨,其他果品及包装物,杏酒"},
        {"company_id": "fangda_special_steel", "name_zh": "方大特钢科技股份有限公司", "stock_code": "600507.SH", "province": "江西", "city": "南昌市", "industry": "特种钢", "main_business": "螺纹钢,汽车板簧,弹簧扁钢,铁精粉等"},
        {"company_id": "shanghai_energy", "name_zh": "上海大屯能源股份有限公司", "stock_code": "600508.SH", "province": "上海", "city": "上海市", "industry": "煤炭开采", "main_business": "原煤,选煤,铁路运输"},
        {"company_id": "tianfu_energy", "name_zh": "新疆天富能源股份有限公司", "stock_code": "600509.SH", "province": "新疆", "city": "石河子市", "industry": "火力发电", "main_business": "电,热的生产与销售"},
        {"company_id": "black_peony", "name_zh": "黑牡丹(集团)股份有限公司", "stock_code": "600510.SH", "province": "江苏", "city": "常州市", "industry": "全国地产", "main_business": "牛仔布,服装"},
        {"company_id": "sinopharm_co", "name_zh": "国药集团药业股份有限公司", "stock_code": "600511.SH", "province": "北京", "city": "北京市", "industry": "医药商业", "main_business": "医药商业,医药工业"},
        {"company_id": "tengda", "name_zh": "腾达建设集团股份有限公司", "stock_code": "600512.SH", "province": "浙江", "city": "台州市", "industry": "建筑工程", "main_business": "市政,公路工程,一级公路运营"},
    ],
    "exposures": [
        {"exposure_id": "anhui_construction_operate_engineering_general_contracting", "company_id": "anhui_construction", "node_id": "engineering_general_contracting", "activity_type": "operate", "role": "工程总承包商", "weight": 0.95},
        {"exposure_id": "anhui_construction_operate_construction", "company_id": "anhui_construction", "node_id": "construction", "activity_type": "operate", "role": "建筑施工运营商", "weight": 0.95},
        {"exposure_id": "anhui_construction_operate_municipal_engineering", "company_id": "anhui_construction", "node_id": "municipal_engineering", "activity_type": "operate", "role": "市政工程运营商", "weight": 0.9},
        {"exposure_id": "huali_family_operate_equity_investment", "company_id": "huali_family", "node_id": "equity_investment", "activity_type": "operate", "role": "股权投资运营商", "weight": 0.95},
        {"exposure_id": "huali_family_provide_service_financial_service", "company_id": "huali_family", "node_id": "financial_service", "activity_type": "provide_service", "role": "金融服务商", "weight": 0.85},
        {"exposure_id": "xichang_power_operate_power_distribution", "company_id": "xichang_power", "node_id": "power_distribution", "activity_type": "operate", "role": "电力配供运营商", "weight": 0.95},
        {"exposure_id": "xichang_power_provide_service_power_supply", "company_id": "xichang_power", "node_id": "power_supply", "activity_type": "provide_service", "role": "电力供应服务商", "weight": 0.9},
        {"exposure_id": "unified_co_produce_pear", "company_id": "unified_co", "node_id": "pear", "activity_type": "produce", "role": "香梨生产商", "weight": 0.95},
        {"exposure_id": "unified_co_produce_fruit", "company_id": "unified_co", "node_id": "fruit", "activity_type": "produce", "role": "果品生产商", "weight": 0.9},
        {"exposure_id": "unified_co_produce_liquor", "company_id": "unified_co", "node_id": "liquor", "activity_type": "produce", "role": "酒类生产商", "weight": 0.85},
        {"exposure_id": "fangda_special_steel_produce_rebar", "company_id": "fangda_special_steel", "node_id": "rebar", "activity_type": "produce", "role": "螺纹钢生产商", "weight": 0.95},
        {"exposure_id": "fangda_special_steel_produce_leaf_spring", "company_id": "fangda_special_steel", "node_id": "leaf_spring", "activity_type": "produce", "role": "汽车板簧生产商", "weight": 0.95},
        {"exposure_id": "fangda_special_steel_produce_spring_flat_steel", "company_id": "fangda_special_steel", "node_id": "spring_flat_steel", "activity_type": "produce", "role": "弹簧扁钢生产商", "weight": 0.9},
        {"exposure_id": "fangda_special_steel_produce_iron_concentrate", "company_id": "fangda_special_steel", "node_id": "iron_concentrate", "activity_type": "produce", "role": "铁精粉生产商", "weight": 0.9},
        {"exposure_id": "shanghai_energy_produce_raw_coal", "company_id": "shanghai_energy", "node_id": "raw_coal", "activity_type": "produce", "role": "原煤生产商", "weight": 0.95},
        {"exposure_id": "shanghai_energy_operate_coal_washing", "company_id": "shanghai_energy", "node_id": "coal_washing", "activity_type": "operate", "role": "选煤运营商", "weight": 0.9},
        {"exposure_id": "shanghai_energy_operate_railway_transport", "company_id": "shanghai_energy", "node_id": "railway_transport", "activity_type": "operate", "role": "铁路运输运营商", "weight": 0.85},
        {"exposure_id": "tianfu_energy_operate_power_generation", "company_id": "tianfu_energy", "node_id": "power_generation", "activity_type": "operate", "role": "发电运营商", "weight": 0.95},
        {"exposure_id": "tianfu_energy_provide_service_heating_supply", "company_id": "tianfu_energy", "node_id": "heating_supply", "activity_type": "provide_service", "role": "热力供应商", "weight": 0.9},
        {"exposure_id": "black_peony_produce_denim", "company_id": "black_peony", "node_id": "denim", "activity_type": "produce", "role": "牛仔布生产商", "weight": 0.95},
        {"exposure_id": "black_peony_produce_apparel", "company_id": "black_peony", "node_id": "apparel", "activity_type": "produce", "role": "服装生产商", "weight": 0.9},
        {"exposure_id": "sinopharm_co_operate_pharmaceutical_commerce", "company_id": "sinopharm_co", "node_id": "pharmaceutical_commerce", "activity_type": "operate", "role": "医药商业运营商", "weight": 0.95},
        {"exposure_id": "sinopharm_co_produce_pharmaceutical", "company_id": "sinopharm_co", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "tengda_operate_municipal_engineering", "company_id": "tengda", "node_id": "municipal_engineering", "activity_type": "operate", "role": "市政工程运营商", "weight": 0.95},
        {"exposure_id": "tengda_operate_highway_operation", "company_id": "tengda", "node_id": "highway_operation", "activity_type": "operate", "role": "公路运营运营商", "weight": 0.9},
        {"exposure_id": "tengda_operate_expressway", "company_id": "tengda", "node_id": "expressway", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.85},
    ],
}

BATCH_079 = {
    "new_nodes": [
        {"node_id": "graphite_electrode", "canonical_name_zh": "石墨电极", "definition": "以石油焦、沥青焦为骨料，煤沥青为粘结剂，经高温石墨化制成的导电电极，用于电弧炉炼钢", "entity_type": "component"},
        {"node_id": "carbon_block", "canonical_name_zh": "炭块", "definition": "以无烟煤、石油焦等为原料经高温焙烧制成的块状炭素制品，用于高炉内衬等", "entity_type": "material"},
        {"node_id": "low_carbon_energy_saving", "canonical_name_zh": "低碳节能", "definition": "通过技术创新和管理优化减少碳排放、提高能源利用效率的技术和服务体系", "entity_type": "service"},
        {"node_id": "power_grid_smart_operation", "canonical_name_zh": "电网智能运维", "definition": "利用物联网、大数据和人工智能技术实现电力电网设备的智能监测、诊断和维护", "entity_type": "service"},
        {"node_id": "maotai_liquor", "canonical_name_zh": "茅台酒", "definition": "中国贵州省茅台镇特产的大曲酱香型白酒，以其独特的酿造工艺和品质闻名", "entity_type": "material"},
        {"node_id": "semiconductor_packaging_mold", "canonical_name_zh": "半导体塑封模具", "definition": "用于半导体集成电路封装过程中塑料成型的精密模具", "entity_type": "component"},
        {"node_id": "led_bracket", "canonical_name_zh": "LED支架", "definition": "用于安装和固定LED芯片并提供电气连接的金属支架，是LED封装的关键部件", "entity_type": "component"},
        {"node_id": "aviation_part", "canonical_name_zh": "航空零部件", "definition": "用于航空器制造和维修的各种金属和非金属零部件，包括结构件、发动机件等", "entity_type": "component"},
    ],
    "new_edges": [
        {"edge_id": "graphite_electrode_to_steel", "from_node": "graphite_electrode", "to_node": "steel", "edge_type": "material_flow", "description": "石墨电极是电弧炉炼钢过程中不可替代的导电材料"},
        {"edge_id": "semiconductor_packaging_mold_to_semiconductor_device", "from_node": "semiconductor_packaging_mold", "to_node": "semiconductor_device", "edge_type": "composition", "description": "半导体塑封模具是集成电路封装生产的关键工艺装备"},
        {"edge_id": "aviation_part_to_aircraft", "from_node": "aviation_part", "to_node": "aircraft", "edge_type": "composition", "description": "航空零部件是航空器机体和系统的基本组成单元"},
    ],
    "companies": [
        {"company_id": "lianhuan_pharma", "name_zh": "江苏联环药业股份有限公司", "stock_code": "600513.SH", "province": "江苏", "city": "扬州市", "industry": "化学制药", "main_business": "敏迪,爱普列特片,达那唑胶囊,联环尔定"},
        {"company_id": "hainan_airport", "name_zh": "海南机场设施股份有限公司", "stock_code": "600515.SH", "province": "海南", "city": "海口市", "industry": "机场", "main_business": "商业,酒店业,房地产业"},
        {"company_id": "fangda_carbon", "name_zh": "方大炭素新材料科技股份有限公司", "stock_code": "600516.SH", "province": "甘肃", "city": "兰州市", "industry": "矿物制品", "main_business": "超高功率石墨电极,高功率石墨电极,普通功率石墨电极,炭块"},
        {"company_id": "sgcc_yingda", "name_zh": "国网英大股份有限公司", "stock_code": "600517.SH", "province": "上海", "city": "上海市", "industry": "多元金融", "main_business": "低碳节能,中低压电气,电网智能运维,电力工程"},
        {"company_id": "kangmei", "name_zh": "康美药业股份有限公司", "stock_code": "600518.SH", "province": "广东", "city": "揭阳市", "industry": "中成药", "main_business": "络欣平,诺沙,利乐,中药饮片"},
        {"company_id": "maotai", "name_zh": "贵州茅台酒股份有限公司", "stock_code": "600519.SH", "province": "贵州", "city": "遵义市", "industry": "白酒", "main_business": "高度茅台酒,低度茅台酒"},
        {"company_id": "sanjiatech", "name_zh": "铜陵三佳科技股份有限公司", "stock_code": "600520.SH", "province": "安徽", "city": "铜陵市", "industry": "半导体", "main_business": "半导体集成电路塑封模具,化学建材挤出模具,LED支架"},
        {"company_id": "huahai", "name_zh": "浙江华海药业股份有限公司", "stock_code": "600521.SH", "province": "浙江", "city": "台州市", "industry": "化学制药", "main_business": "普利类产品,沙坦类产品,抗忧郁类产品,抗组胺类产品,制剂"},
        {"company_id": "zhongtian", "name_zh": "江苏中天科技股份有限公司", "stock_code": "600522.SH", "province": "江苏", "city": "南通市", "industry": "通信设备", "main_business": "电信产品,电力产品,新能源产业"},
        {"company_id": "guihang", "name_zh": "贵州贵航汽车零部件股份有限公司", "stock_code": "600523.SH", "province": "贵州", "city": "贵阳市", "industry": "汽车配件", "main_business": "汽车摩托车零部件,橡胶塑料制品,航空零部件"},
    ],
    "exposures": [
        {"exposure_id": "lianhuan_pharma_produce_pharmaceutical", "company_id": "lianhuan_pharma", "node_id": "pharmaceutical", "activity_type": "produce", "role": "化学药品生产商", "weight": 0.95},
        {"exposure_id": "lianhuan_pharma_produce_chemical_drug", "company_id": "lianhuan_pharma", "node_id": "chemical_drug", "activity_type": "produce", "role": "化学原料药生产商", "weight": 0.9},
        {"exposure_id": "hainan_airport_operate_commercial", "company_id": "hainan_airport", "node_id": "commercial", "activity_type": "operate", "role": "商业运营商", "weight": 0.95},
        {"exposure_id": "hainan_airport_operate_hotel_service", "company_id": "hainan_airport", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店服务商", "weight": 0.9},
        {"exposure_id": "hainan_airport_operate_real_estate_development", "company_id": "hainan_airport", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.9},
        {"exposure_id": "fangda_carbon_produce_graphite_electrode", "company_id": "fangda_carbon", "node_id": "graphite_electrode", "activity_type": "produce", "role": "石墨电极生产商", "weight": 0.95},
        {"exposure_id": "fangda_carbon_produce_carbon_block", "company_id": "fangda_carbon", "node_id": "carbon_block", "activity_type": "produce", "role": "炭块生产商", "weight": 0.9},
        {"exposure_id": "fangda_carbon_produce_metallurgical_product", "company_id": "fangda_carbon", "node_id": "metallurgical_product", "activity_type": "produce", "role": "冶金产品生产商", "weight": 0.85},
        {"exposure_id": "sgcc_yingda_provide_service_low_carbon_energy_saving", "company_id": "sgcc_yingda", "node_id": "low_carbon_energy_saving", "activity_type": "provide_service", "role": "低碳节能服务商", "weight": 0.95},
        {"exposure_id": "sgcc_yingda_manufacture_medium_low_voltage_electrical", "company_id": "sgcc_yingda", "node_id": "medium_low_voltage_electrical", "activity_type": "manufacture", "role": "中低压电气设备制造商", "weight": 0.9},
        {"exposure_id": "sgcc_yingda_provide_service_power_grid_smart_operation", "company_id": "sgcc_yingda", "node_id": "power_grid_smart_operation", "activity_type": "provide_service", "role": "电网智能运维服务商", "weight": 0.95},
        {"exposure_id": "kangmei_produce_chinese_medicine_decoction", "company_id": "kangmei", "node_id": "chinese_medicine_decoction", "activity_type": "produce", "role": "中药饮片生产商", "weight": 0.95},
        {"exposure_id": "kangmei_produce_chinese_patent_medicine", "company_id": "kangmei", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9},
        {"exposure_id": "maotai_produce_maotai_liquor", "company_id": "maotai", "node_id": "maotai_liquor", "activity_type": "produce", "role": "茅台酒生产商", "weight": 0.95},
        {"exposure_id": "maotai_produce_liquor", "company_id": "maotai", "node_id": "liquor", "activity_type": "produce", "role": "白酒生产商", "weight": 0.95},
        {"exposure_id": "sanjiatech_manufacture_semiconductor_packaging_mold", "company_id": "sanjiatech", "node_id": "semiconductor_packaging_mold", "activity_type": "manufacture", "role": "半导体塑封模具制造商", "weight": 0.95},
        {"exposure_id": "sanjiatech_manufacture_led_bracket", "company_id": "sanjiatech", "node_id": "led_bracket", "activity_type": "manufacture", "role": "LED支架制造商", "weight": 0.9},
        {"exposure_id": "huahai_produce_pril_product", "company_id": "huahai", "node_id": "pril_product", "activity_type": "produce", "role": "普利类产品生产商", "weight": 0.95},
        {"exposure_id": "huahai_produce_sartan_product", "company_id": "huahai", "node_id": "sartan_product", "activity_type": "produce", "role": "沙坦类产品生产商", "weight": 0.95},
        {"exposure_id": "huahai_produce_pharmaceutical", "company_id": "huahai", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "zhongtian_manufacture_telecom_product", "company_id": "zhongtian", "node_id": "telecom_product", "activity_type": "manufacture", "role": "电信产品制造商", "weight": 0.95},
        {"exposure_id": "zhongtian_manufacture_power_cable", "company_id": "zhongtian", "node_id": "power_cable", "activity_type": "manufacture", "role": "电力电缆制造商", "weight": 0.9},
        {"exposure_id": "zhongtian_produce_new_energy", "company_id": "zhongtian", "node_id": "new_energy", "activity_type": "produce", "role": "新能源产品生产商", "weight": 0.9},
        {"exposure_id": "guihang_manufacture_aviation_part", "company_id": "guihang", "node_id": "aviation_part", "activity_type": "manufacture", "role": "航空零部件制造商", "weight": 0.95},
        {"exposure_id": "guihang_manufacture_automobile_part", "company_id": "guihang", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车零部件制造商", "weight": 0.9},
        {"exposure_id": "guihang_produce_rubber_plastic_product", "company_id": "guihang", "node_id": "rubber_plastic_product", "activity_type": "produce", "role": "橡胶塑料制品生产商", "weight": 0.85},
    ],
}

BATCH_080 = {
    "new_nodes": [
        {"node_id": "ev_material", "canonical_name_zh": "电动汽车相关材料", "definition": "用于新能源汽车动力电池、电机、电控等系统的关键材料和组件", "entity_type": "material"},
        {"node_id": "smart_factory_equipment", "canonical_name_zh": "智能工厂装备", "definition": "用于实现工厂自动化、数字化和智能化生产的机械设备和系统", "entity_type": "device"},
        {"node_id": "smart_grid_device", "canonical_name_zh": "智能电网设备", "definition": "用于电网智能化运行的设备和系统，包括智能电表、配电自动化设备等", "entity_type": "device"},
        {"node_id": "electrostatic_precipitator", "canonical_name_zh": "电除尘器", "definition": "利用高压静电场使烟气中的粉尘带电并分离收集的环保除尘设备", "entity_type": "device"},
        {"node_id": "polyester_top", "canonical_name_zh": "涤纶毛条", "definition": "由涤纶短纤维经过梳理、针梳等工序制成的条状纤维束，用于纺纱", "entity_type": "material"},
        {"node_id": "railway_project", "canonical_name_zh": "铁路工程", "definition": "铁路线路、桥梁、隧道、站场等基础设施的新建、改建和扩建工程", "entity_type": "service"},
        {"node_id": "molded_bottle", "canonical_name_zh": "模制瓶", "definition": "用模具吹制或压制成型的玻璃瓶，广泛用于药品、化妆品等包装", "entity_type": "component"},
        {"node_id": "electrolytic_lead", "canonical_name_zh": "电解铅", "definition": "通过电解精炼工艺生产的高纯度铅，用于蓄电池、电缆护套等", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "ev_material_to_electric_vehicle", "from_node": "ev_material", "to_node": "electric_vehicle", "edge_type": "composition", "description": "电动汽车相关材料是新能源汽车的核心组成物料"},
        {"edge_id": "smart_grid_device_to_power_grid", "from_node": "smart_grid_device", "to_node": "power_grid", "edge_type": "composition", "description": "智能电网设备是现代电力系统的关键组成设施"},
        {"edge_id": "electrostatic_precipitator_to_power_plant", "from_node": "electrostatic_precipitator", "to_node": "power_plant", "edge_type": "capability_supply", "description": "电除尘器为燃煤电厂提供烟气除尘环保能力"},
    ],
    "companies": [
        {"company_id": "st_changyuan", "name_zh": "长园科技集团股份有限公司", "stock_code": "600525.SH", "province": "广东", "city": "深圳市", "industry": "电气设备", "main_business": "电动汽车相关材料,智能工厂装备,智能电网设备"},
        {"company_id": "feida_env", "name_zh": "浙江菲达环保科技股份有限公司", "stock_code": "600526.SH", "province": "浙江", "city": "绍兴市", "industry": "环境保护", "main_business": "电除尘器产品,气力输送产品,脱硫产品"},
        {"company_id": "jiangnan_gaoxian", "name_zh": "江苏江南高纤股份有限公司", "stock_code": "600527.SH", "province": "江苏", "city": "苏州市", "industry": "化纤", "main_business": "涤纶毛条,涤纶短纤维"},
        {"company_id": "crec_industrial", "name_zh": "中铁高新工业股份有限公司", "stock_code": "600528.SH", "province": "北京", "city": "北京市", "industry": "运输设备", "main_business": "铁路工程项目,其他工程项目"},
        {"company_id": "shandong_pharma_glass", "name_zh": "山东省药用玻璃股份有限公司", "stock_code": "600529.SH", "province": "山东", "city": "淄博市", "industry": "医疗保健", "main_business": "模制瓶,安瓿,管瓶,玻璃管,棕色瓶,丁基胶塞,塑料瓶,铝塑盖"},
        {"company_id": "sjtu_only", "name_zh": "上海交大昂立股份有限公司", "stock_code": "600530.SH", "province": "上海", "city": "上海市", "industry": "医疗保健", "main_business": "食品及保健食品的原料和终端产品的研发,生产,销售"},
        {"company_id": "yuguang", "name_zh": "河南豫光金铅股份有限公司", "stock_code": "600531.SH", "province": "河南", "city": "济源市", "industry": "铅锌", "main_business": "电解铅及铅合金,白银,黄金"},
        {"company_id": "qixia", "name_zh": "南京栖霞建设股份有限公司", "stock_code": "600533.SH", "province": "江苏", "city": "南京市", "industry": "区域地产", "main_business": "房地产开发经营"},
        {"company_id": "tasly", "name_zh": "天士力医药集团股份有限公司", "stock_code": "600535.SH", "province": "天津", "city": "天津市", "industry": "中成药", "main_business": "中药,化学药,生物药"},
        {"company_id": "css", "name_zh": "中国软件与技术服务股份有限公司", "stock_code": "600536.SH", "province": "北京", "city": "北京市", "industry": "软件服务", "main_business": "系统软件及支撑软件,应用软件及服务,软件出口加工及服务"},
    ],
    "exposures": [
        {"exposure_id": "st_changyuan_produce_ev_material", "company_id": "st_changyuan", "node_id": "ev_material", "activity_type": "produce", "role": "电动汽车材料生产商", "weight": 0.95},
        {"exposure_id": "st_changyuan_manufacture_smart_factory_equipment", "company_id": "st_changyuan", "node_id": "smart_factory_equipment", "activity_type": "manufacture", "role": "智能工厂装备制造商", "weight": 0.95},
        {"exposure_id": "st_changyuan_manufacture_smart_grid_device", "company_id": "st_changyuan", "node_id": "smart_grid_device", "activity_type": "manufacture", "role": "智能电网设备制造商", "weight": 0.95},
        {"exposure_id": "feida_env_manufacture_electrostatic_precipitator", "company_id": "feida_env", "node_id": "electrostatic_precipitator", "activity_type": "manufacture", "role": "电除尘器制造商", "weight": 0.95},
        {"exposure_id": "feida_env_provide_service_pneumatic_conveying", "company_id": "feida_env", "node_id": "pneumatic_conveying", "activity_type": "provide_service", "role": "气力输送服务商", "weight": 0.9},
        {"exposure_id": "feida_env_manufacture_desulfurization_product", "company_id": "feida_env", "node_id": "desulfurization_product", "activity_type": "manufacture", "role": "脱硫产品制造商", "weight": 0.9},
        {"exposure_id": "jiangnan_gaoxian_produce_polyester_top", "company_id": "jiangnan_gaoxian", "node_id": "polyester_top", "activity_type": "produce", "role": "涤纶毛条生产商", "weight": 0.95},
        {"exposure_id": "jiangnan_gaoxian_produce_polyester_staple_fiber", "company_id": "jiangnan_gaoxian", "node_id": "polyester_staple_fiber", "activity_type": "produce", "role": "涤纶短纤维生产商", "weight": 0.95},
        {"exposure_id": "jiangnan_gaoxian_produce_chemical_fiber", "company_id": "jiangnan_gaoxian", "node_id": "chemical_fiber", "activity_type": "produce", "role": "化纤产品生产商", "weight": 0.9},
        {"exposure_id": "crec_industrial_operate_railway_project", "company_id": "crec_industrial", "node_id": "railway_project", "activity_type": "operate", "role": "铁路工程运营商", "weight": 0.95},
        {"exposure_id": "crec_industrial_manufacture_rail_transit_equipment", "company_id": "crec_industrial", "node_id": "rail_transit_equipment", "activity_type": "manufacture", "role": "轨道交通装备制造商", "weight": 0.9},
        {"exposure_id": "shandong_pharma_glass_manufacture_molded_bottle", "company_id": "shandong_pharma_glass", "node_id": "molded_bottle", "activity_type": "manufacture", "role": "模制瓶制造商", "weight": 0.95},
        {"exposure_id": "shandong_pharma_glass_manufacture_ampoule", "company_id": "shandong_pharma_glass", "node_id": "ampoule", "activity_type": "manufacture", "role": "安瓿制造商", "weight": 0.9},
        {"exposure_id": "shandong_pharma_glass_manufacture_butyl_rubber_stopper", "company_id": "shandong_pharma_glass", "node_id": "butyl_rubber_stopper", "activity_type": "manufacture", "role": "丁基胶塞制造商", "weight": 0.9},
        {"exposure_id": "shandong_pharma_glass_manufacture_pharmaceutical_packaging", "company_id": "shandong_pharma_glass", "node_id": "pharmaceutical_packaging", "activity_type": "manufacture", "role": "药用包装制造商", "weight": 0.95},
        {"exposure_id": "sjtu_only_produce_health_food", "company_id": "sjtu_only", "node_id": "health_food", "activity_type": "produce", "role": "保健食品生产商", "weight": 0.95},
        {"exposure_id": "sjtu_only_produce_food", "company_id": "sjtu_only", "node_id": "food", "activity_type": "produce", "role": "食品生产商", "weight": 0.9},
        {"exposure_id": "yuguang_produce_electrolytic_lead", "company_id": "yuguang", "node_id": "electrolytic_lead", "activity_type": "produce", "role": "电解铅生产商", "weight": 0.95},
        {"exposure_id": "yuguang_produce_silver_product", "company_id": "yuguang", "node_id": "silver_product", "activity_type": "produce", "role": "白银生产商", "weight": 0.9},
        {"exposure_id": "yuguang_produce_gold", "company_id": "yuguang", "node_id": "gold", "activity_type": "produce", "role": "黄金生产商", "weight": 0.9},
        {"exposure_id": "qixia_operate_real_estate_development", "company_id": "qixia", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "tasly_produce_chinese_patent_medicine", "company_id": "tasly", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中药生产商", "weight": 0.95},
        {"exposure_id": "tasly_produce_chemical_drug", "company_id": "tasly", "node_id": "chemical_drug", "activity_type": "produce", "role": "化学药生产商", "weight": 0.9},
        {"exposure_id": "tasly_produce_biological_drug", "company_id": "tasly", "node_id": "biological_drug", "activity_type": "produce", "role": "生物药生产商", "weight": 0.9},
        {"exposure_id": "css_provide_service_system_software", "company_id": "css", "node_id": "system_software", "activity_type": "provide_service", "role": "系统软件服务商", "weight": 0.95},
        {"exposure_id": "css_provide_service_application_software", "company_id": "css", "node_id": "application_software", "activity_type": "provide_service", "role": "应用软件服务商", "weight": 0.95},
        {"exposure_id": "css_provide_service_software_export", "company_id": "css", "node_id": "software_export", "activity_type": "provide_service", "role": "软件出口加工服务商", "weight": 0.9},
    ],
}

ALL_BATCHES = {
    76: BATCH_076,
    77: BATCH_077,
    78: BATCH_078,
    79: BATCH_079,
    80: BATCH_080,
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
