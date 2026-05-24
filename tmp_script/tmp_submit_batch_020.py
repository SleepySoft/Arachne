"""
Batch 020 Submission Script
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
    {"node_id": "clean_material", "canonical_name_zh": "洁净材料", "definition": "具有低污染、可回收或环境友好特性的新型材料，用于替代传统高污染材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "iron_ore", "canonical_name_zh": "铁矿石", "definition": "含有铁元素且具备工业开采价值的天然矿石，是钢铁冶炼的主要原料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "community_life_service", "canonical_name_zh": "社区生活服务", "definition": "为住宅小区居民提供的物业管理、家政、养老和教育等综合性生活服务", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "cemented_carbide", "canonical_name_zh": "硬质合金", "definition": "以碳化钨为主要成分并添加钴等金属粘结剂烧结而成的高硬度耐磨材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "tungsten", "canonical_name_zh": "钨", "definition": "具有高熔点和高硬度的稀有金属，是硬质合金和特种钢的重要合金元素", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "molybdenum", "canonical_name_zh": "钼", "definition": "具有高熔点和良好耐腐蚀性的稀有金属，广泛用于合金钢和催化剂", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "tantalum", "canonical_name_zh": "钽", "definition": "具有高熔点和优良化学稳定性的稀有金属，主要用于电子电容器和医疗器械", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "niobium", "canonical_name_zh": "铌", "definition": "具有高熔点和良好超导性能的稀有金属，用于高温合金和超导材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "rare_refractory_metal", "canonical_name_zh": "稀有难熔金属", "definition": "熔点高、储量稀少的有色金属总称，包括钨、钼、钽、铌等", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pet_bottle", "canonical_name_zh": "PET瓶", "definition": "以聚对苯二甲酸乙二醇酯为原料吹塑成型的透明包装容器，广泛用于饮料包装", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "bottle_preform", "canonical_name_zh": "瓶胚", "definition": "PET瓶的注塑成型半成品，经加热拉伸吹塑后成为最终瓶形容器", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "beverage_packaging", "canonical_name_zh": "饮料包装", "definition": "用于盛装和保护饮料产品的容器及配套包装系统", "entity_type": "component", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "beverage_processing", "canonical_name_zh": "饮料加工", "definition": "将原料水、糖、果汁和添加剂等调配加工成成品饮料的生产过程", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pet_resin", "canonical_name_zh": "PET树脂", "definition": "聚对苯二甲酸乙二醇酯的颗粒状原料，是制造PET瓶和纤维的基础材料", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "formaldehyde", "canonical_name_zh": "甲醛", "definition": "具有刺激性气味的有机化合物，广泛用于生产胶粘剂、树脂和防腐剂", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "impregnated_paper", "canonical_name_zh": "浸渍纸", "definition": "经树脂浸渍和干燥处理后用于人造板表面装饰和功能改性的特种纸张", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "adhesive", "canonical_name_zh": "胶粘剂", "definition": "通过粘附力和内聚力将材料表面连接在一起的物质，广泛用于木材加工和建筑", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "forest_chemical_product", "canonical_name_zh": "林化产品", "definition": "以林木及其剩余物为原料经化学加工得到的产品，包括松香、栲胶和木浆等", "entity_type": "material", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "pipeline_transportation", "canonical_name_zh": "管道运输", "definition": "利用密闭管道输送气体、液体和浆体货物的大宗运输方式", "entity_type": "service", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "natural_gas_pipeline", "canonical_name_zh": "天然气长输管道", "definition": "跨区域输送天然气的加压管道基础设施及配套站场系统", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
    {"node_id": "urban_gas_network", "canonical_name_zh": "城市燃气管网", "definition": "在城市范围内输送和分配燃气的中低压管道网络及调压设施", "entity_type": "infrastructure", "confidence": "LOW", "status": "PENDING"},
]

edges = [
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tungsten_to_carbide", "from_node": "tungsten", "to_node": "cemented_carbide", "edge_type": "material_flow", "description": "钨是硬质合金的主要成分"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tungsten_to_rare", "from_node": "tungsten", "to_node": "rare_refractory_metal", "edge_type": "composition", "description": "钨是稀有难熔金属的成员"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_moly_to_rare", "from_node": "molybdenum", "to_node": "rare_refractory_metal", "edge_type": "composition", "description": "钼是稀有难熔金属的成员"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_tantalum_to_rare", "from_node": "tantalum", "to_node": "rare_refractory_metal", "edge_type": "composition", "description": "钽是稀有难熔金属的成员"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_niobium_to_rare", "from_node": "niobium", "to_node": "rare_refractory_metal", "edge_type": "composition", "description": "铌是稀有难熔金属的成员"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pet_resin_to_preform", "from_node": "pet_resin", "to_node": "bottle_preform", "edge_type": "material_flow", "description": "PET树脂注塑成型为瓶胚"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_preform_to_bottle", "from_node": "bottle_preform", "to_node": "pet_bottle", "edge_type": "material_flow", "description": "瓶胚经拉伸吹塑成为PET瓶"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pet_bottle_to_packaging", "from_node": "pet_bottle", "to_node": "beverage_packaging", "edge_type": "composition", "description": "PET瓶是饮料包装的主要容器形式"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_beverage_to_packaging", "from_node": "beverage_processing", "to_node": "beverage_packaging", "edge_type": "service_flow", "description": "饮料加工需要配套包装容器"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_timber_to_forest_chem", "from_node": "timber", "to_node": "forest_chemical_product", "edge_type": "material_flow", "description": "木材经化学加工得到林化产品"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_forest_chem_to_formaldehyde", "from_node": "forest_chemical_product", "to_node": "formaldehyde", "edge_type": "material_flow", "description": "林化产品可进一步加工成甲醛"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_forest_chem_to_adhesive", "from_node": "forest_chemical_product", "to_node": "adhesive", "edge_type": "material_flow", "description": "林化产品是胶粘剂的重要原料来源"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_formaldehyde_to_adhesive", "from_node": "formaldehyde", "to_node": "adhesive", "edge_type": "material_flow", "description": "甲醛是生产脲醛树脂胶粘剂的主要原料"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_impregnated_to_board", "from_node": "impregnated_paper", "to_node": "artificial_board", "edge_type": "material_flow", "description": "浸渍纸用于人造板表面贴面"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_natgas_to_pipeline", "from_node": "natural_gas", "to_node": "natural_gas_pipeline", "edge_type": "material_flow", "description": "天然气通过长输管道输送"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pipeline_to_city_gas", "from_node": "natural_gas_pipeline", "to_node": "city_gas_supply", "edge_type": "service_flow", "description": "长输管道向城市燃气系统供气"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_pipeline_to_transport", "from_node": "natural_gas_pipeline", "to_node": "pipeline_transportation", "edge_type": "service_flow", "description": "天然气管道提供管道运输服务"},
    {"edge_namespace": "industrial_flow", "edge_id": "flow_urban_to_city_gas", "from_node": "urban_gas_network", "to_node": "city_gas_supply", "edge_type": "service_flow", "description": "城市燃气管网向终端用户供气"},
]

graph_batch = {
    "batch_id": "batch_020_graph",
    "task_description": "Batch 020 industrial nodes and edges registration",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": edges,
    "rejected_or_pending": []
}

print("=== Submitting Graph Batch 020 ===")
post_batch(graph_batch)

# ============================================================
# Step 2: Register companies and exposures
# ============================================================

companies = [
    {"company_id": "taida_share", "name_zh": "泰达股份", "aliases": ["天津泰达资源循环集团股份有限公司"], "stock_codes": ["000652.SZ"], "country": "CN", "province": "天津", "city": "天津市", "employee_count": 1619, "company_type": "public", "description": "综合企业，主营生态环保、区域开发、能源贸易和洁净材料"},
    {"company_id": "jinling_mining", "name_zh": "金岭矿业", "aliases": ["山东金岭矿业股份有限公司"], "stock_codes": ["000655.SZ"], "country": "CN", "province": "山东", "city": "淄博市", "employee_count": 1834, "company_type": "public", "description": "铁矿石采选企业"},
    {"company_id": "st_jinke", "name_zh": "*ST金科", "aliases": ["金科地产集团股份有限公司"], "stock_codes": ["000656.SZ"], "country": "CN", "province": "重庆", "city": "重庆市", "employee_count": 3660, "company_type": "public", "description": "大型房地产企业，主营房地产开发、社区生活服务、酒店经营和新能源发电"},
    {"company_id": "zhongwu_high_tech", "name_zh": "中钨高新", "aliases": ["中钨高新材料股份有限公司"], "stock_codes": ["000657.SZ"], "country": "CN", "province": "海南", "city": "海口市", "employee_count": 8848, "company_type": "public", "description": "稀有金属企业，主营硬质合金和钨钼钽铌等有色金属深加工产品"},
    {"company_id": "zhuhai_zhongfu", "name_zh": "珠海中富", "aliases": ["珠海中富实业股份有限公司"], "stock_codes": ["000659.SZ"], "country": "CN", "province": "广东", "city": "珠海市", "employee_count": 1638, "company_type": "public", "description": "饮料包装企业，主营PET瓶、瓶胚及饮料包装制品"},
    {"company_id": "changchun_high_tech", "name_zh": "长春高新", "aliases": ["长春高新技术产业(集团)股份有限公司"], "stock_codes": ["000661.SZ"], "country": "CN", "province": "吉林", "city": "长春市", "employee_count": 11547, "company_type": "public", "description": "生物医药企业，主营基因重组人生长素和心脑血管药物"},
    {"company_id": "yongan_forestry", "name_zh": "永安林业", "aliases": ["福建省永安林业(集团)股份有限公司"], "stock_codes": ["000663.SZ"], "country": "CN", "province": "福建", "city": "三明市", "employee_count": 386, "company_type": "public", "description": "林业化工企业，主营木材加工、甲醛、浸渍纸和胶粘剂"},
    {"company_id": "hubei_guangdian", "name_zh": "湖北广电", "aliases": ["湖北省广播电视信息网络股份有限公司"], "stock_codes": ["000665.SZ"], "country": "CN", "province": "湖北", "city": "武汉市", "employee_count": 6165, "company_type": "public", "description": "广播电视网络企业，主营有线数字电视网络运营"},
    {"company_id": "st_rongkong", "name_zh": "*ST荣控", "aliases": ["荣丰控股集团股份有限公司"], "stock_codes": ["000668.SZ"], "country": "CN", "province": "山东", "city": "青岛市", "employee_count": 86, "company_type": "public", "description": "房地产开发企业"},
    {"company_id": "st_jinhong", "name_zh": "ST金鸿", "aliases": ["金鸿控股集团股份有限公司"], "stock_codes": ["000669.SZ"], "country": "CN", "province": "湖南", "city": "衡阳市", "employee_count": 852, "company_type": "public", "description": "天然气企业，主营天然气长输管道及城市燃气管网建设和运营"},
]

exposures = [
    {"exposure_id": "taida_operate_eco", "company_id": "taida_share", "node_id": "ecological_restoration_service", "activity_type": "operate", "role": "生态环保服务商", "weight": 0.6},
    {"exposure_id": "taida_operate_real_estate", "company_id": "taida_share", "node_id": "real_estate_development", "activity_type": "operate", "role": "区域开发商", "weight": 0.5},
    {"exposure_id": "taida_operate_trade", "company_id": "taida_share", "node_id": "trade_service", "activity_type": "operate", "role": "能源贸易商", "weight": 0.5},
    {"exposure_id": "taida_manufacture_clean", "company_id": "taida_share", "node_id": "clean_material", "activity_type": "manufacture", "role": "洁净材料制造商", "weight": 0.4},
    {"exposure_id": "jinling_produce_iron_ore", "company_id": "jinling_mining", "node_id": "iron_ore", "activity_type": "produce", "role": "铁矿石生产商", "weight": 0.9},
    {"exposure_id": "st_jinke_operate_real_estate", "company_id": "st_jinke", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9},
    {"exposure_id": "st_jinke_operate_community", "company_id": "st_jinke", "node_id": "community_life_service", "activity_type": "operate", "role": "社区生活服务商", "weight": 0.5},
    {"exposure_id": "st_jinke_operate_hotel", "company_id": "st_jinke", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.3},
    {"exposure_id": "st_jinke_provide_greening", "company_id": "st_jinke", "node_id": "greening_construction_service", "activity_type": "provide_service", "role": "园林服务商", "weight": 0.3},
    {"exposure_id": "st_jinke_operate_construction", "company_id": "st_jinke", "node_id": "construction_service", "activity_type": "operate", "role": "装饰工程施工商", "weight": 0.3},
    {"exposure_id": "st_jinke_operate_solar", "company_id": "st_jinke", "node_id": "solar_power_generation", "activity_type": "operate", "role": "新能源发电运营商", "weight": 0.2},
    {"exposure_id": "zhongwu_manufacture_carbide", "company_id": "zhongwu_high_tech", "node_id": "cemented_carbide", "activity_type": "manufacture", "role": "硬质合金制造商", "weight": 0.9},
    {"exposure_id": "zhongwu_manufacture_tungsten", "company_id": "zhongwu_high_tech", "node_id": "tungsten", "activity_type": "manufacture", "role": "钨制品制造商", "weight": 0.8},
    {"exposure_id": "zhongwu_manufacture_molybdenum", "company_id": "zhongwu_high_tech", "node_id": "molybdenum", "activity_type": "manufacture", "role": "钼制品制造商", "weight": 0.6},
    {"exposure_id": "zhongwu_manufacture_tantalum", "company_id": "zhongwu_high_tech", "node_id": "tantalum", "activity_type": "manufacture", "role": "钽制品制造商", "weight": 0.5},
    {"exposure_id": "zhongwu_manufacture_niobium", "company_id": "zhongwu_high_tech", "node_id": "niobium", "activity_type": "manufacture", "role": "铌制品制造商", "weight": 0.5},
    {"exposure_id": "zhongwu_manufacture_rare_refractory", "company_id": "zhongwu_high_tech", "node_id": "rare_refractory_metal", "activity_type": "manufacture", "role": "稀有难熔金属制造商", "weight": 0.9},
    {"exposure_id": "zhuhai_manufacture_pet_bottle", "company_id": "zhuhai_zhongfu", "node_id": "pet_bottle", "activity_type": "manufacture", "role": "PET瓶制造商", "weight": 0.9},
    {"exposure_id": "zhuhai_manufacture_preform", "company_id": "zhuhai_zhongfu", "node_id": "bottle_preform", "activity_type": "manufacture", "role": "瓶胚制造商", "weight": 0.8},
    {"exposure_id": "zhuhai_manufacture_packaging", "company_id": "zhuhai_zhongfu", "node_id": "beverage_packaging", "activity_type": "manufacture", "role": "饮料包装制造商", "weight": 0.8},
    {"exposure_id": "zhuhai_operate_beverage", "company_id": "zhuhai_zhongfu", "node_id": "beverage_processing", "activity_type": "operate", "role": "饮料加工商", "weight": 0.4},
    {"exposure_id": "zhuhai_manufacture_pet_resin", "company_id": "zhuhai_zhongfu", "node_id": "pet_resin", "activity_type": "manufacture", "role": "PET树脂制造商", "weight": 0.3},
    {"exposure_id": "changchun_manufacture_biological", "company_id": "changchun_high_tech", "node_id": "biological_drug", "activity_type": "manufacture", "role": "基因工程药物制造商", "weight": 0.9},
    {"exposure_id": "changchun_manufacture_pharma", "company_id": "changchun_high_tech", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "药品制造商", "weight": 0.8},
    {"exposure_id": "changchun_manufacture_tcm", "company_id": "changchun_high_tech", "node_id": "traditional_chinese_medicine", "activity_type": "manufacture", "role": "中成药制造商", "weight": 0.5},
    {"exposure_id": "yongan_operate_forestry", "company_id": "yongan_forestry", "node_id": "forestry", "activity_type": "operate", "role": "林业经营商", "weight": 0.7},
    {"exposure_id": "yongan_manufacture_wood", "company_id": "yongan_forestry", "node_id": "wood_product", "activity_type": "manufacture", "role": "木材产品制造商", "weight": 0.6},
    {"exposure_id": "yongan_produce_timber", "company_id": "yongan_forestry", "node_id": "timber", "activity_type": "produce", "role": "原木生产商", "weight": 0.5},
    {"exposure_id": "yongan_manufacture_board", "company_id": "yongan_forestry", "node_id": "artificial_board", "activity_type": "manufacture", "role": "人造板制造商", "weight": 0.4},
    {"exposure_id": "yongan_manufacture_formaldehyde", "company_id": "yongan_forestry", "node_id": "formaldehyde", "activity_type": "manufacture", "role": "甲醛制造商", "weight": 0.5},
    {"exposure_id": "yongan_manufacture_impregnated", "company_id": "yongan_forestry", "node_id": "impregnated_paper", "activity_type": "manufacture", "role": "浸渍纸制造商", "weight": 0.4},
    {"exposure_id": "yongan_manufacture_adhesive", "company_id": "yongan_forestry", "node_id": "adhesive", "activity_type": "manufacture", "role": "胶粘剂制造商", "weight": 0.5},
    {"exposure_id": "yongan_manufacture_forest_chem", "company_id": "yongan_forestry", "node_id": "forest_chemical_product", "activity_type": "manufacture", "role": "林化产品制造商", "weight": 0.5},
    {"exposure_id": "hubei_operate_cable_tv", "company_id": "hubei_guangdian", "node_id": "cable_tv_network_service", "activity_type": "operate", "role": "有线电视网络运营商", "weight": 0.9},
    {"exposure_id": "hubei_manufacture_cable_equip", "company_id": "hubei_guangdian", "node_id": "cable_tv_equipment", "activity_type": "manufacture", "role": "有线电视设备制造商", "weight": 0.4},
    {"exposure_id": "st_rongkong_operate_real_estate", "company_id": "st_rongkong", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9},
    {"exposure_id": "st_jinhong_operate_natgas", "company_id": "st_jinhong", "node_id": "natural_gas", "activity_type": "operate", "role": "天然气运营商", "weight": 0.8},
    {"exposure_id": "st_jinhong_operate_city_gas", "company_id": "st_jinhong", "node_id": "city_gas_supply", "activity_type": "operate", "role": "城市燃气供应商", "weight": 0.9},
    {"exposure_id": "st_jinhong_operate_pipeline", "company_id": "st_jinhong", "node_id": "pipeline_transportation", "activity_type": "operate", "role": "管道运输运营商", "weight": 0.7},
    {"exposure_id": "st_jinhong_operate_gas_pipeline", "company_id": "st_jinhong", "node_id": "natural_gas_pipeline", "activity_type": "operate", "role": "长输管道运营商", "weight": 0.8},
    {"exposure_id": "st_jinhong_operate_urban_network", "company_id": "st_jinhong", "node_id": "urban_gas_network", "activity_type": "operate", "role": "城市管网运营商", "weight": 0.7},
]

business_batch = {
    "batch_id": "batch_020_business",
    "task_description": "Batch 020 companies and node exposures registration",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": companies,
    "company_node_exposures_to_upsert": exposures
}

print("\n=== Submitting Business Batch 020 ===")
post_business_batch(business_batch)
