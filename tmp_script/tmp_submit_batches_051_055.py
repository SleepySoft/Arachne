#!/usr/bin/env python3
"""Submit batches 051-055 to Arachne API with correct schema."""
import json, requests, os
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_get(path):
    r = requests.get(f"{BASE}/{path}", timeout=10)
    return r.json() if r.status_code == 200 else None

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=60)
    return r.status_code, r.text

def make_evidence(quote, title="tushare"):
    return [{
        "source_title": title,
        "quote": quote,
    }]

def load_existing():
    with open("tmp_existing_nodes.json", "r", encoding="utf-8") as f:
        nodes = set(json.load(f))
    with open("tmp_existing_edges.json", "r", encoding="utf-8") as f:
        edges = set(json.load(f))
    return nodes, edges

EXISTING_NODES, EXISTING_EDGES = load_existing()

# =============================================================================
# BATCH DATA DEFINITIONS
# =============================================================================

BATCHES = {}

# -----------------------------------------------------------------------------
# BATCH 051 (600125-600135)
# -----------------------------------------------------------------------------
BATCHES["051"] = {
    "new_nodes": [
        {"node_id": "rail_logistics", "canonical_name_zh": "铁路物流", "definition": "铁路货运及物流运输服务", "entity_type": "service"},
        {"node_id": "rice", "canonical_name_zh": "大米", "definition": "稻谷加工而成的食用大米", "entity_type": "material"},
        {"node_id": "flour", "canonical_name_zh": "面粉", "definition": "小麦加工而成的食用面粉", "entity_type": "material"},
        {"node_id": "edible_oil", "canonical_name_zh": "食用油", "definition": "植物或动物油脂加工而成的食用油脂", "entity_type": "material"},
        {"node_id": "trade_agent", "canonical_name_zh": "贸易代理", "definition": "商品进出口代理及贸易经纪服务", "entity_type": "service"},
        {"node_id": "mobile_phone", "canonical_name_zh": "移动电话", "definition": "便携式无线通信终端设备", "entity_type": "device"},
        {"node_id": "beer", "canonical_name_zh": "啤酒", "definition": "以麦芽、啤酒花等发酵酿造的酒精饮料", "entity_type": "material"},
        {"node_id": "tech_park", "canonical_name_zh": "科技园区", "definition": "集聚科技企业的产业园区基础设施", "entity_type": "infrastructure"},
        {"node_id": "environmental_service", "canonical_name_zh": "环保服务", "definition": "大气污染治理、环保咨询及环境治理服务", "entity_type": "service"},
        {"node_id": "photographic_film", "canonical_name_zh": "感光胶片", "definition": "用于摄影成像的感光材料", "entity_type": "material"},
        {"node_id": "solar_pv_material", "canonical_name_zh": "光伏材料", "definition": "太阳能电池用硅片、电池片及组件材料", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "rice_to_flour", "from_node": "rice", "to_node": "flour", "edge_type": "material_flow", "description": "稻谷与小麦均为粮食原料，可并行加工成不同主食产品"},
        {"edge_id": "solar_pv_material_to_photovoltaic_cell", "from_node": "solar_pv_material", "to_node": "photovoltaic_cell", "edge_type": "composition", "description": "光伏材料构成太阳能电池组件"},
    ],
    "companies": [
        {"company_id": "tielong_logistics", "name_zh": "中铁铁龙集装箱物流股份有限公司", "stock_codes": ["600125.SH"], "province": "辽宁", "city": "大连", "description": "铁路客运业务,铁路货运及延伸服务业务,混凝土生产,房地产业务"},
        {"company_id": "hangzhou_steel", "name_zh": "杭州钢铁股份有限公司", "stock_codes": ["600126.SH"], "province": "浙江", "city": "杭州", "description": "棒材,线材,带钢,型材,轻轨等钢铁及其压延产品的生产和销售"},
        {"company_id": "jinjian_rice", "name_zh": "金健米业股份有限公司", "stock_codes": ["600127.SH"], "province": "湖南", "city": "常德", "description": "大米,面粉,面条,食用油的生产与销售"},
        {"company_id": "suhao_hongye", "name_zh": "苏豪弘业股份有限公司", "stock_codes": ["600128.SH"], "province": "江苏", "city": "南京", "description": "服装,玩具,帽类产品,手套,柳编制品,箱包,木雕的进出口贸易"},
        {"company_id": "taiji_group", "name_zh": "重庆太极实业(集团)股份有限公司", "stock_codes": ["600129.SH"], "province": "重庆", "city": "重庆", "description": "曲美,急支糖浆,补肾益寿胶囊,藿香正气口服液等中成药的生产与销售"},
        {"company_id": "bird_mobile", "name_zh": "宁波波导股份有限公司", "stock_codes": ["600130.SH"], "province": "浙江", "city": "宁波", "description": "手机主板及整机的研发,生产和销售"},
        {"company_id": "sgcc_ict", "name_zh": "国网信息通信股份有限公司", "stock_codes": ["600131.SH"], "province": "四川", "city": "阿坝", "description": "水利发电,配套发展与水电有关的输供电业务,电力工程勘察设计咨询"},
        {"company_id": "chongqing_beer", "name_zh": "重庆啤酒股份有限公司", "stock_codes": ["600132.SH"], "province": "重庆", "city": "重庆", "description": "啤酒的生产与销售"},
        {"company_id": "donghu_hitech", "name_zh": "武汉东湖高新集团股份有限公司", "stock_codes": ["600133.SH"], "province": "湖北", "city": "武汉", "description": "科技园区,发电,火电厂烟气脱硫服务等"},
        {"company_id": "lucky_film", "name_zh": "乐凯胶片股份有限公司", "stock_codes": ["600135.SH"], "province": "河北", "city": "保定", "description": "彩纸,彩卷,光伏材料,新型膜材料的生产与销售"},
    ],
    "exposures": [
        ("tielong_logistics", "rail_logistics", "operate", "铁路物流运营商", 0.9),
        ("tielong_logistics", "logistics_service", "provide_service", "综合物流服务商", 0.8),
        ("hangzhou_steel", "steel_plate", "produce", "钢铁板材生产商", 0.95),
        ("jinjian_rice", "rice", "produce", "大米生产商", 0.9),
        ("jinjian_rice", "flour", "produce", "面粉生产商", 0.85),
        ("jinjian_rice", "edible_oil", "produce", "食用油生产商", 0.85),
        ("suhao_hongye", "trade_agent", "provide_service", "进出口贸易代理商", 0.9),
        ("suhao_hongye", "textile_product", "procure", "纺织品贸易商", 0.8),
        ("taiji_group", "chinese_patent_medicine", "produce", "中成药生产商", 0.95),
        ("bird_mobile", "mobile_phone", "manufacture", "移动电话制造商", 0.9),
        ("sgcc_ict", "power_supply", "provide_service", "电力供应及通信服务商", 0.9),
        ("sgcc_ict", "communication_equipment", "manufacture", "通信设备制造商", 0.8),
        ("chongqing_beer", "beer", "produce", "啤酒生产商", 0.95),
        ("donghu_hitech", "tech_park", "operate", "科技园区运营商", 0.85),
        ("donghu_hitech", "environmental_service", "provide_service", "环保服务提供商", 0.8),
        ("donghu_hitech", "power_generation", "operate", "火力发电运营商", 0.75),
        ("lucky_film", "photographic_film", "produce", "感光胶片生产商", 0.85),
        ("lucky_film", "solar_pv_material", "produce", "光伏材料生产商", 0.8),
    ],
}

# -----------------------------------------------------------------------------
# BATCH 052 (600136-600153)
# -----------------------------------------------------------------------------
BATCHES["052"] = {
    "new_nodes": [
        {"node_id": "film_tv", "canonical_name_zh": "影视传媒", "definition": "电视剧、电影及影视节目的制作与发行服务", "entity_type": "service"},
        {"node_id": "sports_service", "canonical_name_zh": "体育服务", "definition": "体育赛事运营、体育场馆管理及体育经纪服务", "entity_type": "service"},
        {"node_id": "underwear", "canonical_name_zh": "内衣", "definition": "针织内衣及贴身服饰产品", "entity_type": "material"},
        {"node_id": "tourism_service", "canonical_name_zh": "旅游服务", "definition": "旅行社、旅游线路及旅游相关配套服务", "entity_type": "service"},
        {"node_id": "automobile_clutch", "canonical_name_zh": "汽车离合器", "definition": "汽车传动系统中的离合器总成及零部件", "entity_type": "component"},
        {"node_id": "clean_energy_supply", "canonical_name_zh": "清洁能源供应", "definition": "清洁供能项目投资、建设及运营服务", "entity_type": "service"},
        {"node_id": "shipbuilding", "canonical_name_zh": "船舶制造", "definition": "民用及军用船舶的设计、建造与修理", "entity_type": "system"},
        {"node_id": "solar_cell", "canonical_name_zh": "太阳能电池", "definition": "硅片、电池片及光伏组件的制造与销售", "entity_type": "component"},
        {"node_id": "consumer_battery", "canonical_name_zh": "消费类电池", "definition": "聚合物电池、铝壳电池等消费电子产品用电池", "entity_type": "component"},
        {"node_id": "supply_chain_service", "canonical_name_zh": "供应链服务", "definition": "大宗商品采购、分销及供应链管理服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "solar_cell_to_solar_panel", "from_node": "solar_cell", "to_node": "solar_panel", "edge_type": "composition", "description": "太阳能电池片组装成太阳能板"},
        {"edge_id": "automobile_clutch_to_automobile", "from_node": "automobile_clutch", "to_node": "automobile", "edge_type": "composition", "description": "汽车离合器是汽车传动系统的组成部分"},
    ],
    "companies": [
        {"company_id": "st_mingcheng", "name_zh": "武汉明诚文化体育集团股份有限公司", "stock_codes": ["600136.SH"], "province": "湖北", "city": "武汉", "description": "影视产品制作销售及发行,艺人经纪,体育营销,体育版权贸易,体育场馆运营,赛事运营"},
        {"company_id": "langsha", "name_zh": "四川浪莎控股股份有限公司", "stock_codes": ["600137.SH"], "province": "四川", "city": "宜宾", "description": "针织内衣,针织面料制造销售"},
        {"company_id": "cyts", "name_zh": "中青旅控股股份有限公司", "stock_codes": ["600138.SH"], "province": "北京", "city": "北京", "description": "旅游服务业,科技产品销售及技术服务"},
        {"company_id": "xingfa_group", "name_zh": "湖北兴发化工集团股份有限公司", "stock_codes": ["600141.SH"], "province": "湖北", "city": "宜昌", "description": "三聚磷酸钠和六偏磷酸钠等磷酸盐产品的生产和销售"},
        {"company_id": "changchun_yidong", "name_zh": "长春一东离合器股份有限公司", "stock_codes": ["600148.SH"], "province": "吉林", "city": "长春", "description": "汽车离合器的研发、生产与销售"},
        {"company_id": "langfang_dev", "name_zh": "廊坊发展股份有限公司", "stock_codes": ["600149.SH"], "province": "河北", "city": "廊坊", "description": "贸易业务,租赁业务,拓展清洁供能项目"},
        {"company_id": "cssc", "name_zh": "中国船舶工业股份有限公司", "stock_codes": ["600150.SH"], "province": "上海", "city": "上海", "description": "造船业务,修船业务,动力业务,海洋工程,机电设备"},
        {"company_id": "aerospace_mech", "name_zh": "上海航天汽车机电股份有限公司", "stock_codes": ["600151.SH"], "province": "上海", "city": "上海", "description": "硅片,电池片,组件环节的技术研发,制造以及销售,电站投资,开发,EPC建设"},
        {"company_id": "victor_tech", "name_zh": "维科技术股份有限公司", "stock_codes": ["600152.SH"], "province": "浙江", "city": "宁波", "description": "消费类电池和小动力电池的研发,生产和销售"},
        {"company_id": "cnd", "name_zh": "厦门建发股份有限公司", "stock_codes": ["600153.SH"], "province": "福建", "city": "厦门", "description": "以供应链运营和房地产开发为主业的现代服务型企业"},
    ],
    "exposures": [
        ("st_mingcheng", "film_tv", "provide_service", "影视传媒服务商", 0.85),
        ("st_mingcheng", "sports_service", "provide_service", "体育服务运营商", 0.8),
        ("langsha", "underwear", "produce", "内衣制造商", 0.9),
        ("langsha", "textile_product", "produce", "纺织品生产商", 0.85),
        ("cyts", "tourism_service", "provide_service", "旅游服务提供商", 0.95),
        ("xingfa_group", "phosphorus_chemical", "produce", "磷化工产品生产商", 0.95),
        ("xingfa_group", "chemical_fertilizer", "produce", "化学肥料生产商", 0.9),
        ("changchun_yidong", "automobile_clutch", "manufacture", "汽车离合器制造商", 0.95),
        ("changchun_yidong", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
        ("langfang_dev", "trade_agent", "provide_service", "贸易及供能服务商", 0.8),
        ("langfang_dev", "clean_energy_supply", "provide_service", "清洁能源供应商", 0.75),
        ("cssc", "shipbuilding", "manufacture", "船舶制造商", 0.95),
        ("cssc", "ship_accessory", "manufacture", "船舶配件制造商", 0.85),
        ("aerospace_mech", "solar_cell", "manufacture", "太阳能电池制造商", 0.9),
        ("aerospace_mech", "automobile_part", "manufacture", "汽车零部件制造商", 0.8),
        ("victor_tech", "consumer_battery", "manufacture", "消费类电池制造商", 0.9),
        ("victor_tech", "lithium_battery", "manufacture", "锂电池制造商", 0.85),
        ("cnd", "supply_chain_service", "provide_service", "供应链服务商", 0.95),
        ("cnd", "real_estate_development", "operate", "房地产开发运营商", 0.85),
    ],
}

# -----------------------------------------------------------------------------
# BATCH 053 (600155-600165)
# -----------------------------------------------------------------------------
BATCHES["053"] = {
    "new_nodes": [
        {"node_id": "securities_service", "canonical_name_zh": "证券服务", "definition": "证券经纪、投资银行及资产管理服务", "entity_type": "service"},
        {"node_id": "plastic_pipe", "canonical_name_zh": "塑料管材", "definition": "PVC、PE等塑料管道型材产品", "entity_type": "component"},
        {"node_id": "ramie_textile", "canonical_name_zh": "苎麻纺织", "definition": "苎麻纱线、坯布及麻类纺织品", "entity_type": "material"},
        {"node_id": "fluorochemical", "canonical_name_zh": "氟化工产品", "definition": "氟制冷剂、含氟聚合物及氟精细化学品", "entity_type": "material"},
        {"node_id": "vaccine", "canonical_name_zh": "疫苗", "definition": "人用及兽用疫苗制品", "entity_type": "material"},
        {"node_id": "blood_product", "canonical_name_zh": "血液制品", "definition": "人血白蛋白、免疫球蛋白等血液制品", "entity_type": "material"},
        {"node_id": "wind_power", "canonical_name_zh": "风力发电", "definition": "陆上及海上风力发电项目开发与运营", "entity_type": "service"},
        {"node_id": "activated_carbon", "canonical_name_zh": "活性炭", "definition": "木质及煤质活性炭制品", "entity_type": "material"},
        {"node_id": "biomaterial", "canonical_name_zh": "生物基材料", "definition": "生物基可降解材料及合成树脂产品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "fluorochemical_to_refrigerant", "from_node": "fluorochemical", "to_node": "refrigerant", "edge_type": "material_flow", "description": "氟化工产品用于制造制冷剂"},
        {"edge_id": "blood_product_to_vaccine", "from_node": "blood_product", "to_node": "vaccine", "edge_type": "material_flow", "description": "血液制品与疫苗同属生物制药领域"},
    ],
    "companies": [
        {"company_id": "huachang_yunxin", "name_zh": "华创云信数字技术股份有限公司", "stock_codes": ["600155.SH"], "province": "北京", "city": "北京", "description": "证券业务和塑料管型材业务"},
        {"company_id": "huasheng", "name_zh": "湖南华升股份有限公司", "stock_codes": ["600156.SH"], "province": "湖南", "city": "长沙", "description": "苎麻等麻类及与棉,丝,化纤混纺的纱线,坯布,印染布,服饰"},
        {"company_id": "yongtai_energy", "name_zh": "永泰能源集团股份有限公司", "stock_codes": ["600157.SH"], "province": "山西", "city": "晋中", "description": "煤矿及其他矿山投资,煤炭洗选加工,电厂投资,新能源开发与投资"},
        {"company_id": "zhongti", "name_zh": "中体产业集团股份有限公司", "stock_codes": ["600158.SH"], "province": "天津", "city": "天津", "description": "承办体育赛事,健身服务,体育场馆经营,体育培训,赛事运营"},
        {"company_id": "dalong_realestate", "name_zh": "北京市大龙伟业房地产开发股份有限公司", "stock_codes": ["600159.SH"], "province": "北京", "city": "北京", "description": "房地产开发和建筑施工"},
        {"company_id": "juhua", "name_zh": "浙江巨化股份有限公司", "stock_codes": ["600160.SH"], "province": "浙江", "city": "衢州", "description": "氟产品,氨产品,氯碱产品,酸产品,农药产品,生物化学制品"},
        {"company_id": "tiantan_bio", "name_zh": "北京天坛生物制品股份有限公司", "stock_codes": ["600161.SH"], "province": "北京", "city": "北京", "description": "疫苗,血制品,诊断试剂等的生产与销售"},
        {"company_id": "xiangjiang_holdings", "name_zh": "深圳香江控股股份有限公司", "stock_codes": ["600162.SH"], "province": "广东", "city": "深圳", "description": "房地产开发,物业管理,物流,会展及仓储服务"},
        {"company_id": "zhongmin_energy", "name_zh": "中闽能源股份有限公司", "stock_codes": ["600163.SH"], "province": "福建", "city": "福州", "description": "陆上风力发电的项目开发,建设及运营"},
        {"company_id": "st_ningke", "name_zh": "宁夏中科生物科技股份有限公司", "stock_codes": ["600165.SH"], "province": "宁夏", "city": "石嘴山", "description": "活性炭制品的生产及销售,干细胞制备和储存,贸易"},
    ],
    "exposures": [
        ("huachang_yunxin", "securities_service", "provide_service", "证券服务商", 0.9),
        ("huachang_yunxin", "plastic_pipe", "produce", "塑料管材生产商", 0.8),
        ("huasheng", "ramie_textile", "produce", "苎麻纺织品生产商", 0.9),
        ("huasheng", "textile_product", "produce", "纺织品生产商", 0.85),
        ("yongtai_energy", "coal", "produce", "煤炭生产商", 0.95),
        ("yongtai_energy", "power_generation", "operate", "火力发电运营商", 0.9),
        ("zhongti", "sports_service", "provide_service", "体育服务运营商", 0.9),
        ("dalong_realestate", "real_estate_development", "operate", "房地产开发运营商", 0.95),
        ("juhua", "fluorochemical", "produce", "氟化工产品生产商", 0.95),
        ("juhua", "chlor_alkali_product", "produce", "氯碱化工产品生产商", 0.9),
        ("tiantan_bio", "vaccine", "produce", "疫苗生产商", 0.95),
        ("tiantan_bio", "blood_product", "produce", "血液制品生产商", 0.95),
        ("xiangjiang_holdings", "real_estate_development", "operate", "房地产开发运营商", 0.9),
        ("zhongmin_energy", "wind_power", "operate", "风力发电运营商", 0.95),
        ("st_ningke", "activated_carbon", "produce", "活性炭生产商", 0.85),
        ("st_ningke", "biomaterial", "produce", "生物基材料生产商", 0.8),
    ],
}

# -----------------------------------------------------------------------------
# BATCH 054 (600166-600177)
# -----------------------------------------------------------------------------
BATCHES["054"] = {
    "new_nodes": [
        {"node_id": "automobile", "canonical_name_zh": "汽车整车", "definition": "乘用车、商用车及新能源汽车整车制造", "entity_type": "system"},
        {"node_id": "heating_supply", "canonical_name_zh": "供热服务", "definition": "城市集中供热、热电联产及清洁能源供暖", "entity_type": "service"},
        {"node_id": "water_treatment", "canonical_name_zh": "水务处理", "definition": "自来水生产供应、污水处理及再生水利用", "entity_type": "service"},
        {"node_id": "construction_machinery", "canonical_name_zh": "工程机械", "definition": "起重机、挖掘机、轧锻设备等重型机械装备", "entity_type": "device"},
        {"node_id": "construction_engineering", "canonical_name_zh": "建筑工程", "definition": "房屋建筑、市政工程及基础设施建设施工", "entity_type": "service"},
        {"node_id": "integrated_circuit", "canonical_name_zh": "集成电路", "definition": "模拟和数模混合集成电路芯片设计与制造", "entity_type": "component"},
        {"node_id": "synthetic_diamond", "canonical_name_zh": "人造金刚石", "definition": "超硬材料、金刚石制品及复合材料", "entity_type": "material"},
        {"node_id": "fiberglass", "canonical_name_zh": "玻璃纤维", "definition": "玻璃纤维及制品、高性能纤维及复合材料", "entity_type": "material"},
        {"node_id": "garment", "canonical_name_zh": "服装", "definition": "西服、衬衫等成衣服饰产品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "fiberglass_to_composite_material", "from_node": "fiberglass", "to_node": "composite_material", "edge_type": "composition", "description": "玻璃纤维是复合材料的重要增强材料"},
        {"edge_id": "synthetic_diamond_to_cutting_tool", "from_node": "synthetic_diamond", "to_node": "cutting_tool", "edge_type": "material_flow", "description": "人造金刚石用于制造切削工具和磨具"},
        {"edge_id": "construction_machinery_to_construction_engineering", "from_node": "construction_machinery", "to_node": "construction_engineering", "edge_type": "capability_supply", "description": "工程机械为建筑工程提供施工能力"},
    ],
    "companies": [
        {"company_id": "foton_motor", "name_zh": "北汽福田汽车股份有限公司", "stock_codes": ["600166.SH"], "province": "北京", "city": "北京", "description": "汽车制造,模具,冲压件,发动机,机械电器设备,智能车载设备"},
        {"company_id": "lianmei", "name_zh": "联美量子股份有限公司", "stock_codes": ["600167.SH"], "province": "辽宁", "city": "沈阳", "description": "供热,供水,房屋租赁,市政建设,工程施工,物业管理"},
        {"company_id": "wuhan_water", "name_zh": "武汉三镇实业控股股份有限公司", "stock_codes": ["600168.SH"], "province": "湖北", "city": "武汉", "description": "自来水生产与供应,城市污水处理"},
        {"company_id": "st_taiyuan", "name_zh": "太原重工股份有限公司", "stock_codes": ["600169.SH"], "province": "山西", "city": "太原", "description": "起重机,挖掘机,轧锻设备,汽车变速箱,油膜轴承"},
        {"company_id": "shanghai_const", "name_zh": "上海建工集团股份有限公司", "stock_codes": ["600170.SH"], "province": "上海", "city": "上海", "description": "一般民用建筑,工业建筑,市政建筑,建筑装饰工程,总承包工程"},
        {"company_id": "belling", "name_zh": "上海贝岭股份有限公司", "stock_codes": ["600171.SH"], "province": "上海", "city": "上海", "description": "模拟和数模混合集成电路及系统解决方案"},
        {"company_id": "yellow_river", "name_zh": "河南黄河旋风股份有限公司", "stock_codes": ["600172.SH"], "province": "河南", "city": "许昌", "description": "人造金刚石,建筑机械,金刚石制品"},
        {"company_id": "wolong_new_energy", "name_zh": "卧龙新能源集团股份有限公司", "stock_codes": ["600173.SH"], "province": "浙江", "city": "绍兴", "description": "房地产开发经营和物业管理"},
        {"company_id": "china_jushi", "name_zh": "中国巨石股份有限公司", "stock_codes": ["600176.SH"], "province": "浙江", "city": "嘉兴", "description": "玻璃纤维的研发,生产与销售"},
        {"company_id": "youngor", "name_zh": "雅戈尔时尚股份有限公司", "stock_codes": ["600177.SH"], "province": "浙江", "city": "宁波", "description": "西服,衬衫等服装制造及房地产开发"},
    ],
    "exposures": [
        ("foton_motor", "automobile", "manufacture", "汽车整车制造商", 0.95),
        ("foton_motor", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
        ("foton_motor", "new_energy_vehicle", "manufacture", "新能源汽车制造商", 0.85),
        ("lianmei", "heating_supply", "provide_service", "供热服务供应商", 0.95),
        ("lianmei", "water_supply", "provide_service", "供水服务供应商", 0.85),
        ("wuhan_water", "water_treatment", "provide_service", "水务处理运营商", 0.95),
        ("st_taiyuan", "construction_machinery", "manufacture", "工程机械制造商", 0.9),
        ("st_taiyuan", "special_steel", "produce", "特种钢生产商", 0.85),
        ("shanghai_const", "construction_engineering", "provide_service", "建筑工程承包商", 0.95),
        ("belling", "integrated_circuit", "manufacture", "集成电路制造商", 0.9),
        ("belling", "semiconductor_device", "manufacture", "半导体器件制造商", 0.85),
        ("yellow_river", "synthetic_diamond", "produce", "人造金刚石生产商", 0.95),
        ("yellow_river", "cutting_tool", "manufacture", "切削工具制造商", 0.8),
        ("wolong_new_energy", "real_estate_development", "operate", "房地产开发运营商", 0.9),
        ("wolong_new_energy", "wind_power_equipment", "manufacture", "风电设备制造商", 0.75),
        ("china_jushi", "fiberglass", "produce", "玻璃纤维生产商", 0.95),
        ("china_jushi", "composite_material", "produce", "复合材料生产商", 0.85),
        ("youngor", "garment", "produce", "服装生产商", 0.9),
        ("youngor", "real_estate_development", "operate", "房地产开发运营商", 0.85),
    ],
}

# -----------------------------------------------------------------------------
# BATCH 055 (600178-600188)
# -----------------------------------------------------------------------------
BATCHES["055"] = {
    "new_nodes": [
        {"node_id": "auto_engine", "canonical_name_zh": "汽车发动机", "definition": "汽油、柴油及新能源汽车用发动机总成", "entity_type": "component"},
        {"node_id": "container_shipping", "canonical_name_zh": "集装箱航运", "definition": "国际及国内集装箱海运、多式联运物流服务", "entity_type": "service"},
        {"node_id": "tire", "canonical_name_zh": "轮胎", "definition": "汽车、工程机械用橡胶轮胎产品", "entity_type": "component"},
        {"node_id": "copper_clad_laminate", "canonical_name_zh": "覆铜板", "definition": "印制电路板用覆铜板和粘结片", "entity_type": "component"},
        {"node_id": "optical_glass", "canonical_name_zh": "光学玻璃", "definition": "光学仪器、防务产品用特种玻璃材料", "entity_type": "material"},
        {"node_id": "defense_equipment", "canonical_name_zh": "防务装备", "definition": "军用光电设备及防务系统集成产品", "entity_type": "system"},
        {"node_id": "duty_free", "canonical_name_zh": "免税商品", "definition": "离岛免税、口岸免税及市内免税商品销售", "entity_type": "service"},
        {"node_id": "monosodium_glutamate", "canonical_name_zh": "味精", "definition": "谷氨酸钠调味品及食品配料", "entity_type": "material"},
        {"node_id": "water_supply_service", "canonical_name_zh": "供水服务", "definition": "城市市政供排水及水务基础设施运营", "entity_type": "service"},
        {"node_id": "coal_mining", "canonical_name_zh": "煤炭开采", "definition": "煤炭开采、洗选加工及煤化工", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "auto_engine_to_automobile", "from_node": "auto_engine", "to_node": "automobile", "edge_type": "composition", "description": "汽车发动机是汽车整车的核心组成部件"},
        {"edge_id": "tire_to_automobile", "from_node": "tire", "to_node": "automobile", "edge_type": "composition", "description": "轮胎是汽车整车的关键配套部件"},
        {"edge_id": "copper_clad_laminate_to_pcb", "from_node": "copper_clad_laminate", "to_node": "printed_circuit_board", "edge_type": "composition", "description": "覆铜板是印制电路板的基础材料"},
        {"edge_id": "optical_glass_to_defense_equipment", "from_node": "optical_glass", "to_node": "defense_equipment", "edge_type": "composition", "description": "光学玻璃用于制造防务装备中的光电系统"},
    ],
    "companies": [
        {"company_id": "dongan_power", "name_zh": "哈尔滨东安汽车动力股份有限公司", "stock_codes": ["600178.SH"], "province": "黑龙江", "city": "哈尔滨", "description": "汽车发动机,变速器,发电机及发电机组的制造与销售"},
        {"company_id": "antong", "name_zh": "安通控股股份有限公司", "stock_codes": ["600179.SH"], "province": "福建", "city": "泉州", "description": "集装箱物流服务,多式联运综合物流服务"},
        {"company_id": "st_ruimao", "name_zh": "瑞茂通供应链管理股份有限公司", "stock_codes": ["600180.SH"], "province": "山东", "city": "烟台", "description": "供应链管理服务,煤炭及制品销售,石油制品销售"},
        {"company_id": "giti_tire", "name_zh": "佳通轮胎股份有限公司", "stock_codes": ["600182.SH"], "province": "黑龙江", "city": "牡丹江", "description": "生产销售轮胎,轮胎原辅材料,生产橡胶工业专用设备"},
        {"company_id": "shengyi_tech", "name_zh": "广东生益科技股份有限公司", "stock_codes": ["600183.SH"], "province": "广东", "city": "东莞", "description": "覆铜板和粘结片,印制线路板的设计,生产和销售"},
        {"company_id": "norinco_optical", "name_zh": "北方光电股份有限公司", "stock_codes": ["600184.SH"], "province": "湖北", "city": "襄阳", "description": "光学玻璃,防务产品,光电系统及智能车载设备"},
        {"company_id": "zhuhai_dutyfree", "name_zh": "珠海珠免集团股份有限公司", "stock_codes": ["600185.SH"], "province": "广东", "city": "珠海", "description": "免税商品销售,房地产开发经营"},
        {"company_id": "lotus_holdings", "name_zh": "莲花控股股份有限公司", "stock_codes": ["600186.SH"], "province": "河南", "city": "周口", "description": "味精,面粉,小麦淀粉及副产品,热力,电力的生产与销售"},
        {"company_id": "st_guozhong", "name_zh": "黑龙江国中水务股份有限公司", "stock_codes": ["600187.SH"], "province": "黑龙江", "city": "哈尔滨", "description": "城市市政供排水"},
        {"company_id": "yankuang_energy", "name_zh": "兖矿能源集团股份有限公司", "stock_codes": ["600188.SH"], "province": "山东", "city": "济宁", "description": "煤炭开采,洗选加工,销售,煤化工,甲醇的生产与销售,电力"},
    ],
    "exposures": [
        ("dongan_power", "auto_engine", "manufacture", "汽车发动机制造商", 0.95),
        ("dongan_power", "automobile_part", "manufacture", "汽车零部件制造商", 0.9),
        ("antong", "container_shipping", "operate", "集装箱航运运营商", 0.95),
        ("antong", "logistics_service", "provide_service", "综合物流服务商", 0.9),
        ("st_ruimao", "supply_chain_service", "provide_service", "供应链服务商", 0.9),
        ("st_ruimao", "coal", "procure", "煤炭贸易商", 0.85),
        ("giti_tire", "tire", "manufacture", "轮胎制造商", 0.95),
        ("shengyi_tech", "copper_clad_laminate", "manufacture", "覆铜板制造商", 0.95),
        ("shengyi_tech", "printed_circuit_board", "manufacture", "印制电路板制造商", 0.9),
        ("norinco_optical", "optical_glass", "produce", "光学玻璃生产商", 0.9),
        ("norinco_optical", "defense_equipment", "manufacture", "防务装备制造商", 0.85),
        ("norinco_optical", "optoelectronic_device", "manufacture", "光电子器件制造商", 0.8),
        ("zhuhai_dutyfree", "duty_free", "operate", "免税商品运营商", 0.95),
        ("zhuhai_dutyfree", "real_estate_development", "operate", "房地产开发运营商", 0.8),
        ("lotus_holdings", "monosodium_glutamate", "produce", "味精生产商", 0.95),
        ("lotus_holdings", "flour", "produce", "面粉生产商", 0.85),
        ("st_guozhong", "water_supply_service", "provide_service", "供水服务运营商", 0.95),
        ("st_guozhong", "water_treatment", "provide_service", "污水处理运营商", 0.9),
        ("yankuang_energy", "coal_mining", "operate", "煤炭开采运营商", 0.95),
        ("yankuang_energy", "coal", "produce", "煤炭生产商", 0.95),
        ("yankuang_energy", "methanol", "produce", "甲醇生产商", 0.85),
    ],
}


# =============================================================================
# SUBMISSION LOGIC
# =============================================================================

def submit_batch(batch_num, data):
    print(f"\n{'='*60}")
    print(f"Batch {batch_num} Submission")
    print(f"{'='*60}")

    # Graph batch
    nodes_to_upsert = []
    for n in data["new_nodes"]:
        if n["node_id"] not in EXISTING_NODES:
            nodes_to_upsert.append({
                "node_id": n["node_id"],
                "canonical_name_zh": n["canonical_name_zh"],
                "definition": n["definition"],
                "entity_type": n["entity_type"],
                "confidence": "HIGH",
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch {batch_num}: {n['canonical_name_zh']}"),
            })

    edges_to_upsert = []
    for e in data["new_edges"]:
        if e["edge_id"] not in EXISTING_EDGES:
            edges_to_upsert.append({
                "edge_id": e["edge_id"],
                "from_node": e["from_node"],
                "to_node": e["to_node"],
                "edge_namespace": "industrial_flow",
                "edge_type": e["edge_type"],
                "description": e["description"],
                "confidence": "MEDIUM",
                "status": "ACTIVE",
                "evidence": make_evidence(f"tushare batch {batch_num}: {e['description']}"),
            })

    graph_batch = {
        "batch_id": f"batch_{batch_num}",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

    print(f"Graph batch: {len(nodes_to_upsert)} new nodes, {len(edges_to_upsert)} new edges")
    if nodes_to_upsert or edges_to_upsert:
        status, text = api_post("batches", graph_batch)
        print(f"  Response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {text[:500]}")
    else:
        print("  Nothing new to submit")

    # Business batch
    companies_to_upsert = []
    for c in data["companies"]:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "stock_codes": c["stock_codes"],
            "country": "CN",
            "province": c["province"],
            "city": c["city"],
            "description": c["description"],
            "company_type": "public",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare: {c['description']}"),
        })

    exposures_to_upsert = []
    for company_id, node_id, activity, role, weight in data["exposures"]:
        exposure_id = f"{company_id}_{activity}_{node_id}"
        exposures_to_upsert.append({
            "exposure_id": exposure_id,
            "company_id": company_id,
            "node_id": node_id,
            "activity_type": activity,
            "role": role,
            "weight": weight,
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch {batch_num}: {company_id} -> {node_id}"),
        })

    biz_batch = {
        "batch_id": f"batch_{batch_num}",
        "task_description": f"Batch {batch_num} companies and exposures",
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

    print(f"Business batch: {len(companies_to_upsert)} companies, {len(exposures_to_upsert)} exposures")
    status, text = api_post("business-batches", biz_batch)
    print(f"  Response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {text[:500]}")

    return status in (200, 201)


if __name__ == "__main__":
    results = {}
    for num in ["051", "052", "053", "054", "055"]:
        ok = submit_batch(num, BATCHES[num])
        results[num] = ok

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for num, ok in results.items():
        print(f"  Batch {num}: {'OK' if ok else 'FAILED'}")
