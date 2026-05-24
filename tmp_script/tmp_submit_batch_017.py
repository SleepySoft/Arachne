"""
Batch 017 Submission Script
Manually designed industrial graph and company views for 10 companies.
"""
import requests
import json

BASE = "http://localhost:8000/api/v1"

def post_batch(batch):
    r = requests.post(f"{BASE}/batches", json=batch)
    print("batch nodes/edges status:", r.status_code)
    print(r.json())
    return r.status_code == 201

def post_business_batch(batch):
    r = requests.post(f"{BASE}/business-batches", json=batch)
    print("business batch status:", r.status_code)
    print(r.json())
    return r.status_code == 201

# ============================================================
# Step 1: Register new industrial nodes and edges
# ============================================================

nodes = [
    {"node_id": "sports_shoes", "canonical_name_zh": "运动鞋", "definition": "专为体育运动设计制造的鞋类产品，具有缓冲、支撑和防滑等功能", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "casting_machine", "canonical_name_zh": "铸造机械", "definition": "用于金属铸造成型的机械设备，包括造型机、浇注机和清理设备等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rubber_plastic_machine", "canonical_name_zh": "橡塑机械", "definition": "用于橡胶和塑料加工的专用机械设备，包括混炼机、挤出机和注塑机等", "entity_type": "device", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "embroidery_product", "canonical_name_zh": "绣品", "definition": "以针线在织物上绣制图案形成的装饰工艺品或日用品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "paper_pulp", "canonical_name_zh": "纸浆", "definition": "植物纤维经化学或机械处理后形成的悬浮液或浆状物，是造纸工业的原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "non_ferrous_metal_mining", "canonical_name_zh": "有色金属采矿", "definition": "对铜、铅、锌、银等有色金属矿产进行勘探、开采和选矿的生产活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "silver", "canonical_name_zh": "银", "definition": "具有优良导电导热性和延展性的贵金属，广泛用于电子、珠宝和投资领域", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "solid_waste_treatment", "canonical_name_zh": "固废处理", "definition": "对工业和生活固体废弃物进行收集、运输、处理和处置的环保服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "advertising_service", "canonical_name_zh": "广告服务", "definition": "为客户进行市场调研、创意策划、媒体投放和效果评估的营销传播服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "vocational_education", "canonical_name_zh": "职业教育", "definition": "为受教育者提供从事某种职业所必需的知识和技能培训的教育服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "early_childhood_education", "canonical_name_zh": "幼教", "definition": "对学龄前儿童进行保育和教育的专业服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "land_development", "canonical_name_zh": "土地开发", "definition": "对国有土地进行征用、拆迁、基础设施建设和场地平整，使其达到建设条件的经营活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "oil_extraction", "canonical_name_zh": "石油开采", "definition": "利用钻井和采油工程从地下油藏中提取原油的生产活动", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aluminum_smelting", "canonical_name_zh": "铝冶炼", "definition": "以氧化铝为原料，通过电解法生产原铝的冶金工艺过程", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aluminum_liquid", "canonical_name_zh": "铝液", "definition": "电解铝生产得到的液态原铝，可直接用于铸造或进一步加工成铝锭", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aluminum_ingot", "canonical_name_zh": "铝锭", "definition": "将铝液浇铸成固定形状和重量的固态铝块，是铝加工的中间产品", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "aluminum_alloy", "canonical_name_zh": "铝合金", "definition": "以铝为基础加入一种或几种其他元素制成的合金材料，具有轻质高强的特点", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_rubber_to_shoes", "from_node": "rubber", "to_node": "sports_shoes", "edge_type": "material_flow", "description": "橡胶是运动鞋鞋底的主要原材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pulp_to_paper", "from_node": "paper_pulp", "to_node": "paper_product", "edge_type": "material_flow", "description": "纸浆是造纸的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pulp_to_packaging", "from_node": "paper_pulp", "to_node": "paper_packaging_product", "edge_type": "material_flow", "description": "纸浆是纸包装制品的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_mining_to_ore", "from_node": "non_ferrous_metal_mining", "to_node": "lead_zinc_ore", "edge_type": "service_flow", "description": "有色金属采矿活动产出铅锌矿石"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_mining_to_precious", "from_node": "non_ferrous_metal_mining", "to_node": "precious_metal", "edge_type": "service_flow", "description": "有色金属采矿活动产出贵金属"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_mining_to_silver", "from_node": "non_ferrous_metal_mining", "to_node": "silver", "edge_type": "service_flow", "description": "有色金属采矿活动产出银"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_solid_to_hazard", "from_node": "solid_waste_treatment", "to_node": "hazardous_waste_treatment_service", "edge_type": "service_flow", "description": "固废处理是危废处理的上游环节"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_vocational_to_edu", "from_node": "vocational_education", "to_node": "education_service", "edge_type": "service_flow", "description": "职业教育是教育服务的细分领域"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_early_to_edu", "from_node": "early_childhood_education", "to_node": "education_service", "edge_type": "service_flow", "description": "幼教是教育服务的细分领域"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ad_to_newmedia", "from_node": "advertising_service", "to_node": "new_media_service", "edge_type": "service_flow", "description": "广告服务是新媒体运营的重要变现模式"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_land_to_development", "from_node": "land", "to_node": "land_development", "edge_type": "material_flow", "description": "土地是土地开发的原材料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_land_dev_to_real_estate", "from_node": "land_development", "to_node": "real_estate_development", "edge_type": "service_flow", "description": "土地开发是房地产开发的前置环节"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_extraction_to_crude", "from_node": "oil_extraction", "to_node": "crude_oil", "edge_type": "service_flow", "description": "石油开采活动产出原油"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_smelting_to_liquid", "from_node": "aluminum_smelting", "to_node": "aluminum_liquid", "edge_type": "service_flow", "description": "铝冶炼产出液态原铝"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_liquid_to_ingot", "from_node": "aluminum_liquid", "to_node": "aluminum_ingot", "edge_type": "material_flow", "description": "铝液浇铸成为铝锭"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ingot_to_alloy", "from_node": "aluminum_ingot", "to_node": "aluminum_alloy", "edge_type": "material_flow", "description": "铝锭进一步加工成铝合金"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_ingot_to_panel", "from_node": "aluminum_ingot", "to_node": "aluminum_panel", "edge_type": "material_flow", "description": "铝锭加工成铝板/铝型材"},
]

graph_batch = {
    "batch_id": "batch_017_graph",
    "task_description": "Batch 017 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 017 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "qingdao_doublestar", "name_zh": "青岛双星", "aliases": ["青岛双星股份有限公司"], "stock_codes": ["000599.SZ"], "country": "CN", "province": "山东", "city": "青岛市", "employee_count": 5161, "company_type": "public", "description": "综合制造企业，主营轮胎、运动鞋、铸造机械、橡塑机械和绣品"},
    {"company_id": "jiantou_energy", "name_zh": "建投能源", "aliases": ["河北建投能源投资股份有限公司"], "stock_codes": ["000600.SZ"], "country": "CN", "province": "河北", "city": "石家庄市", "employee_count": 5758, "company_type": "public", "description": "能源投资企业，主营电力生产为主的能源项目投资建设和运营管理"},
    {"company_id": "shaoneng", "name_zh": "韶能股份", "aliases": ["广东韶能集团股份有限公司"], "stock_codes": ["000601.SZ"], "country": "CN", "province": "广东", "city": "韶关市", "employee_count": 4630, "company_type": "public", "description": "综合能源企业，主营电力生产、纸浆造纸及非电制造业"},
    {"company_id": "shengda_resources", "name_zh": "盛达资源", "aliases": ["盛达金属资源股份有限公司"], "stock_codes": ["000603.SZ"], "country": "CN", "province": "北京", "city": "北京市", "employee_count": 1392, "company_type": "public", "description": "有色金属矿采选企业，主营银、铅、锌等有色金属的采选与销售"},
    {"company_id": "bohai_share", "name_zh": "渤海股份", "aliases": ["渤海水业股份有限公司"], "stock_codes": ["000605.SZ"], "country": "CN", "province": "北京", "city": "北京市", "employee_count": 1261, "company_type": "public", "description": "水务环保企业，主营供水服务、供暖服务、环境治理及固废危废处理"},
    {"company_id": "huamei_holdings", "name_zh": "华媒控股", "aliases": ["浙江华媒控股股份有限公司"], "stock_codes": ["000607.SZ"], "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 2426, "company_type": "public", "description": "文化传媒企业，主营教育、广告及新媒体业务"},
    {"company_id": "sunshine_property", "name_zh": "阳光股份", "aliases": ["阳光新业地产股份有限公司"], "stock_codes": ["000608.SZ"], "country": "CN", "province": "广西", "city": "南宁市", "employee_count": 336, "company_type": "public", "description": "房地产开发企业"},
    {"company_id": "st_zhongdi", "name_zh": "*ST中迪", "aliases": ["北京中迪投资股份有限公司"], "stock_codes": ["000609.SZ"], "country": "CN", "province": "北京", "city": "北京市", "employee_count": 89, "company_type": "public", "description": "房地产企业，主营土地一级开发和房地产投资"},
    {"company_id": "st_xi_lv", "name_zh": "*ST西旅", "aliases": ["西安旅游股份有限公司"], "stock_codes": ["000610.SZ"], "country": "CN", "province": "陕西", "city": "西安市", "employee_count": 1158, "company_type": "public", "description": "旅游企业，主营旅游业务和石油开采"},
    {"company_id": "jiaozuo_wanfang", "name_zh": "焦作万方", "aliases": ["焦作万方铝业股份有限公司"], "stock_codes": ["000612.SZ"], "country": "CN", "province": "河南", "city": "焦作市", "employee_count": 2123, "company_type": "public", "description": "铝冶炼加工企业，主营铝液、铝锭和铝合金产品"},
]

exposures = [
    {"exposure_id": "qingdao_manufacture_tire", "company_id": "qingdao_doublestar", "node_id": "tire", "activity_type": "manufacture", "role": "轮胎制造商", "weight": 0.8},
    {"exposure_id": "qingdao_manufacture_sports_shoes", "company_id": "qingdao_doublestar", "node_id": "sports_shoes", "activity_type": "manufacture", "role": "运动鞋制造商", "weight": 0.5},
    {"exposure_id": "qingdao_manufacture_casting", "company_id": "qingdao_doublestar", "node_id": "casting_machine", "activity_type": "manufacture", "role": "铸造机械制造商", "weight": 0.3},
    {"exposure_id": "qingdao_manufacture_rubber_plastic", "company_id": "qingdao_doublestar", "node_id": "rubber_plastic_machine", "activity_type": "manufacture", "role": "橡塑机械制造商", "weight": 0.3},
    {"exposure_id": "qingdao_manufacture_embroidery", "company_id": "qingdao_doublestar", "node_id": "embroidery_product", "activity_type": "manufacture", "role": "绣品制造商", "weight": 0.2},
    {"exposure_id": "jiantou_produce_elec", "company_id": "jiantou_energy", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.9},
    {"exposure_id": "jiantou_operate_plant", "company_id": "jiantou_energy", "node_id": "power_plant_operation", "activity_type": "operate", "role": "电厂运营商", "weight": 0.9},
    {"exposure_id": "jiantou_operate_coal", "company_id": "jiantou_energy", "node_id": "coal_power_generation", "activity_type": "operate", "role": "燃煤发电运营商", "weight": 0.7},
    {"exposure_id": "jiantou_operate_gas", "company_id": "jiantou_energy", "node_id": "gas_power_generation", "activity_type": "operate", "role": "燃气发电运营商", "weight": 0.5},
    {"exposure_id": "shaoneng_produce_elec", "company_id": "shaoneng", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.8},
    {"exposure_id": "shaoneng_manufacture_pulp", "company_id": "shaoneng", "node_id": "paper_pulp", "activity_type": "manufacture", "role": "纸浆制造商", "weight": 0.5},
    {"exposure_id": "shaoneng_manufacture_paper", "company_id": "shaoneng", "node_id": "paper_product", "activity_type": "manufacture", "role": "纸制品制造商", "weight": 0.4},
    {"exposure_id": "shengda_operate_mining", "company_id": "shengda_resources", "node_id": "non_ferrous_metal_mining", "activity_type": "operate", "role": "有色金属采矿商", "weight": 0.9},
    {"exposure_id": "shengda_produce_ore", "company_id": "shengda_resources", "node_id": "lead_zinc_ore", "activity_type": "produce", "role": "铅锌矿石生产商", "weight": 0.8},
    {"exposure_id": "shengda_produce_metal", "company_id": "shengda_resources", "node_id": "lead_zinc_metal", "activity_type": "produce", "role": "铅锌金属生产商", "weight": 0.7},
    {"exposure_id": "shengda_produce_silver", "company_id": "shengda_resources", "node_id": "silver", "activity_type": "produce", "role": "银生产商", "weight": 0.6},
    {"exposure_id": "shengda_produce_precious", "company_id": "shengda_resources", "node_id": "precious_metal", "activity_type": "produce", "role": "贵金属生产商", "weight": 0.5},
    {"exposure_id": "bohai_operate_tap_water", "company_id": "bohai_share", "node_id": "tap_water_supply", "activity_type": "operate", "role": "供水服务商", "weight": 0.7},
    {"exposure_id": "bohai_produce_heat", "company_id": "bohai_share", "node_id": "heating_supply", "activity_type": "produce", "role": "供暖服务商", "weight": 0.7},
    {"exposure_id": "bohai_operate_wastewater", "company_id": "bohai_share", "node_id": "waste_water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.5},
    {"exposure_id": "bohai_operate_hazard", "company_id": "bohai_share", "node_id": "hazardous_waste_treatment_service", "activity_type": "operate", "role": "危废处理运营商", "weight": 0.4},
    {"exposure_id": "bohai_operate_solid", "company_id": "bohai_share", "node_id": "solid_waste_treatment", "activity_type": "operate", "role": "固废处理运营商", "weight": 0.4},
    {"exposure_id": "huamei_provide_education", "company_id": "huamei_holdings", "node_id": "education_service", "activity_type": "provide_service", "role": "教育服务商", "weight": 0.6},
    {"exposure_id": "huamei_provide_vocational", "company_id": "huamei_holdings", "node_id": "vocational_education", "activity_type": "provide_service", "role": "职业教育服务商", "weight": 0.4},
    {"exposure_id": "huamei_provide_early", "company_id": "huamei_holdings", "node_id": "early_childhood_education", "activity_type": "provide_service", "role": "幼教服务商", "weight": 0.3},
    {"exposure_id": "huamei_operate_ad", "company_id": "huamei_holdings", "node_id": "advertising_service", "activity_type": "operate", "role": "广告服务商", "weight": 0.7},
    {"exposure_id": "huamei_operate_newmedia", "company_id": "huamei_holdings", "node_id": "new_media_service", "activity_type": "operate", "role": "新媒体运营商", "weight": 0.6},
    {"exposure_id": "sunshine_operate_real_estate", "company_id": "sunshine_property", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9},
    {"exposure_id": "st_zhongdi_operate_land_dev", "company_id": "st_zhongdi", "node_id": "land_development", "activity_type": "operate", "role": "土地开发商", "weight": 0.8},
    {"exposure_id": "st_zhongdi_operate_real_estate", "company_id": "st_zhongdi", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.6},
    {"exposure_id": "st_xilv_operate_tourism", "company_id": "st_xi_lv", "node_id": "tourism_service", "activity_type": "operate", "role": "旅游服务商", "weight": 0.6},
    {"exposure_id": "st_xilv_operate_hotel", "company_id": "st_xi_lv", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.5},
    {"exposure_id": "st_xilv_operate_catering", "company_id": "st_xi_lv", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.4},
    {"exposure_id": "st_xilv_operate_oil_extraction", "company_id": "st_xi_lv", "node_id": "oil_extraction", "activity_type": "operate", "role": "石油开采商", "weight": 0.4},
    {"exposure_id": "st_xilv_produce_crude", "company_id": "st_xi_lv", "node_id": "crude_oil", "activity_type": "produce", "role": "原油生产商", "weight": 0.3},
    {"exposure_id": "jiaozuo_operate_smelting", "company_id": "jiaozuo_wanfang", "node_id": "aluminum_smelting", "activity_type": "operate", "role": "铝冶炼运营商", "weight": 0.9},
    {"exposure_id": "jiaozuo_manufacture_al_liquid", "company_id": "jiaozuo_wanfang", "node_id": "aluminum_liquid", "activity_type": "manufacture", "role": "铝液生产商", "weight": 0.8},
    {"exposure_id": "jiaozuo_manufacture_al_ingot", "company_id": "jiaozuo_wanfang", "node_id": "aluminum_ingot", "activity_type": "manufacture", "role": "铝锭制造商", "weight": 0.8},
    {"exposure_id": "jiaozuo_manufacture_al_alloy", "company_id": "jiaozuo_wanfang", "node_id": "aluminum_alloy", "activity_type": "manufacture", "role": "铝合金制造商", "weight": 0.7},
    {"exposure_id": "jiaozuo_manufacture_al_panel", "company_id": "jiaozuo_wanfang", "node_id": "aluminum_panel", "activity_type": "manufacture", "role": "铝板制造商", "weight": 0.6},
]

business_batch = {
    "batch_id": "batch_017_business",
    "task_description": "Batch 017 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 017 ===")
post_business_batch(business_batch)
