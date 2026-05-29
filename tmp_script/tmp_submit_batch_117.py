#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, subprocess, os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(BASE_DIR, "cli", "arachne_cli.py")
PY = os.path.join(BASE_DIR, "backend", "venv", "Scripts", "python.exe")

def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

NODES = [
    {"node_id": "textile_garment", "canonical_name_zh": "纺织服装", "canonical_name_en": "textile and garment", "entity_type": "material", "aliases": [], "definition": "纺织品和服装产品的统称", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("苏豪汇鸿主营业务")},
    {"node_id": "textile_raw_material", "canonical_name_zh": "纺织原料", "canonical_name_en": "textile raw material", "entity_type": "material", "aliases": [], "definition": "用于纺织生产的各类原料，包括棉花、化纤、羊毛等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("苏豪汇鸿经营范围")},
    {"node_id": "electronic_equipment", "canonical_name_zh": "电子设备", "canonical_name_en": "electronic equipment", "entity_type": "device", "aliases": [], "definition": "利用电子技术实现特定功能的设备和器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("苏豪汇鸿经营范围")},
    {"node_id": "steam", "canonical_name_zh": "蒸汽", "canonical_name_en": "steam", "entity_type": "material", "aliases": [], "definition": "水加热至沸腾产生的气态水，广泛用于工业动力和供热", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("宁波能源主营业务")},
    {"node_id": "microwave_oven", "canonical_name_zh": "微波炉", "canonical_name_en": "microwave oven", "entity_type": "device", "aliases": [], "definition": "利用微波加热食物的厨房电器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("惠而浦经营范围")},
    {"node_id": "air_purifier", "canonical_name_zh": "空气净化器", "canonical_name_en": "air purifier", "entity_type": "device", "aliases": [], "definition": "过滤和净化室内空气的电器设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("惠而浦经营范围")},
    {"node_id": "asphalt_concrete_pavers", "canonical_name_zh": "沥青混凝土摊铺机", "canonical_name_en": "asphalt concrete paver", "entity_type": "device", "aliases": [], "definition": "用于铺设沥青混凝土路面的工程机械", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("建设机械主营业务")},
    {"node_id": "stabilized_soil_mixer", "canonical_name_zh": "稳定土拌和机", "canonical_name_en": "stabilized soil mixer", "entity_type": "device", "aliases": [], "definition": "用于拌和稳定土材料的工程机械", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("建设机械主营业务")},
    {"node_id": "hoisting_machinery", "canonical_name_zh": "起重机械", "canonical_name_en": "hoisting machinery", "entity_type": "device", "aliases": [], "definition": "用于垂直升降或垂直升降并水平移动重物的机电设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("建设机械经营范围")},
    {"node_id": "mining_machinery", "canonical_name_zh": "矿山机械", "canonical_name_en": "mining machinery", "entity_type": "device", "aliases": [], "definition": "用于矿山开采、选矿等作业的机械设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("建设机械经营范围")},
    {"node_id": "textile_printing_dyeing", "canonical_name_zh": "纺织印染", "canonical_name_en": "textile printing and dyeing", "entity_type": "service", "aliases": [], "definition": "对纺织品进行印花、染色等加工处理的生产活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("航民股份主营业务")},
    {"node_id": "woven_fabric", "canonical_name_zh": "织造布", "canonical_name_en": "woven fabric", "entity_type": "material", "aliases": [], "definition": "通过经纬纱交织而成的织物", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("航民股份主营业务")},
    {"node_id": "electric_power", "canonical_name_zh": "电力", "canonical_name_en": "electric power", "entity_type": "material", "aliases": [], "definition": "以电能形式存在的二次能源", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("华电国际主营业务")},
    {"node_id": "port", "canonical_name_zh": "港口", "canonical_name_en": "port", "entity_type": "infrastructure", "aliases": [], "definition": "具有船舶进出、停泊、靠泊，旅客上下，货物装卸、驳运、储存等功能，由一定范围的水域和陆域组成的区域", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("南京港主营业务")},
    {"node_id": "refined_oil_product", "canonical_name_zh": "成品油", "canonical_name_en": "refined oil product", "entity_type": "material", "aliases": [], "definition": "原油经炼制加工后得到的各类石油产品，包括汽油、柴油、煤油等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("南京港经营范围")},
    {"node_id": "liquid_chemical", "canonical_name_zh": "液体化工品", "canonical_name_en": "liquid chemical", "entity_type": "material", "aliases": [], "definition": "以液态形式存在的化工原料和产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("南京港经营范围")},
    {"node_id": "cement_production_line", "canonical_name_zh": "水泥生产线", "canonical_name_en": "cement production line", "entity_type": "system", "aliases": [], "definition": "用于水泥熟料生产和水泥粉磨的成套设备和工艺系统", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材国际主营业务")},
    {"node_id": "cement_equipment", "canonical_name_zh": "水泥设备", "canonical_name_en": "cement equipment", "entity_type": "device", "aliases": [], "definition": "用于水泥生产过程的各类机械设备和装置", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材国际经营范围")},
    {"node_id": "concrete_product", "canonical_name_zh": "混凝土制品", "canonical_name_en": "concrete product", "entity_type": "material", "aliases": [], "definition": "以混凝土为主要材料制成的各类建筑构件和制品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材国际主营业务")},
    {"node_id": "engineering_contracting", "canonical_name_zh": "工程总承包", "canonical_name_en": "engineering contracting", "entity_type": "service", "aliases": [], "definition": "受业主委托，按照合同约定对工程建设项目的设计、采购、施工、试运行等实行全过程或若干阶段的承包", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中材国际经营范围")},
    {"node_id": "vegetable_seed", "canonical_name_zh": "蔬菜种子", "canonical_name_en": "vegetable seed", "entity_type": "material", "aliases": [], "definition": "用于蔬菜种植的各类种子", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("登海种业主营业务")},
    {"node_id": "flower", "canonical_name_zh": "花卉", "canonical_name_en": "flower", "entity_type": "material", "aliases": [], "definition": "具有观赏价值的植物及其繁殖材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("登海种业主营业务")},
    {"node_id": "crop_seed", "canonical_name_zh": "农作物种子", "canonical_name_en": "crop seed", "entity_type": "material", "aliases": [], "definition": "用于农作物种植的各类种子，包括粮食作物、经济作物等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("登海种业经营范围")},
]

EDGES = [
    {"edge_id": "textile_garment_textile_raw_material", "from_node": "textile_garment", "to_node": "textile_raw_material", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "纺织服装以纺织原料为生产材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "textile_raw_material_textile_weaving", "from_node": "textile_raw_material", "to_node": "textile_weaving", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "纺织原料用于纺织织造", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steam_thermal_power_generation", "from_node": "steam", "to_node": "thermal_power_generation", "edge_namespace": "industrial_flow", "edge_type": "energy_flow", "description": "蒸汽是火力发电的工质", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "microwave_oven_kitchen_appliance", "from_node": "microwave_oven", "to_node": "kitchen_appliance", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "微波炉是厨房电器的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "air_purifier_home_appliance", "from_node": "air_purifier", "to_node": "home_appliance_steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "空气净化器属于家用电器", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "asphalt_concrete_pavers_construction_machinery", "from_node": "asphalt_concrete_pavers", "to_node": "construction_machinery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "沥青混凝土摊铺机是工程机械的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "stabilized_soil_mixer_construction_machinery", "from_node": "stabilized_soil_mixer", "to_node": "construction_machinery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "稳定土拌和机是工程机械的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "hoisting_machinery_construction_machinery", "from_node": "hoisting_machinery", "to_node": "construction_machinery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "起重机械是工程机械的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "mining_machinery_construction_machinery", "from_node": "mining_machinery", "to_node": "construction_machinery", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "矿山机械属于工程机械范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "textile_printing_dyeing_textile_garment", "from_node": "textile_printing_dyeing", "to_node": "textile_garment", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "纺织印染服务于纺织服装生产", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "woven_fabric_textile_garment", "from_node": "woven_fabric", "to_node": "textile_garment", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "织造布是纺织服装的原材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "dye_textile_printing_dyeing", "from_node": "dye", "to_node": "textile_printing_dyeing", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "染料是纺织印染的重要原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "electric_power_power_generation_equipment", "from_node": "electric_power", "to_node": "power_generation_equipment", "edge_namespace": "industrial_flow", "edge_type": "energy_flow", "description": "电力由发电设备生产", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "port_crude_oil", "from_node": "port", "to_node": "crude_oil", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "港口为原油提供装卸储存服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "refined_oil_product_crude_oil", "from_node": "refined_oil_product", "to_node": "crude_oil", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "成品油由原油炼制而来", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "cement_production_line_cement_equipment", "from_node": "cement_production_line", "to_node": "cement_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "水泥生产线由水泥设备组成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "concrete_product_cement", "from_node": "concrete_product", "to_node": "cement", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "混凝土制品以水泥为原料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "engineering_contracting_construction_engineering", "from_node": "engineering_contracting", "to_node": "construction_engineering", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "工程总承包是建筑工程的实施方式", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "crop_seed_corn_seed", "from_node": "crop_seed", "to_node": "corn_seed", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "玉米种子是农作物种子的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "vegetable_seed_crop_seed", "from_node": "vegetable_seed", "to_node": "crop_seed", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "蔬菜种子是农作物种子的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

BUSINESS = {
    "batch_id": "batch_117_business",
    "task_description": "Batch 117 business registration for 10 A-share companies",
    "companies_to_upsert": [
        {"company_id": "sh_600981", "name_zh": "苏豪汇鸿", "name_en": "Jiangsu Soho Highhope Group Co., Ltd.", "country": "CN", "province": "江苏", "city": "南京市", "stock_codes": ["600981.SH"], "description": "纺织品及服装的进出口业务", "founded_year": 1992, "employee_count": 3305},
        {"company_id": "sh_600982", "name_zh": "宁波能源", "name_en": "Ningbo Energy Group Co., Ltd.", "country": "CN", "province": "浙江", "city": "宁波市", "stock_codes": ["600982.SH"], "description": "电力、蒸汽、热力供应及发电业务", "founded_year": 1995, "employee_count": 1510},
        {"company_id": "sh_600983", "name_zh": "惠而浦", "name_en": "Whirlpool (China) Co., Ltd.", "country": "CN", "province": "安徽", "city": "合肥市", "stock_codes": ["600983.SH"], "description": "洗衣机、冰箱、微波炉等家用电器制造销售", "founded_year": 2000, "employee_count": 2423},
        {"company_id": "sh_600984", "name_zh": "建设机械", "name_en": "Shaanxi Construction Machinery Co., Ltd.", "country": "CN", "province": "陕西", "city": "西安市", "stock_codes": ["600984.SH"], "description": "沥青混凝土摊铺机、稳定土拌和机等工程机械", "founded_year": 2001, "employee_count": 3546},
        {"company_id": "sh_600987", "name_zh": "航民股份", "name_en": "Zhejiang Hangmin Co., Ltd.", "country": "CN", "province": "浙江", "city": "杭州市", "stock_codes": ["600987.SH"], "description": "印染及印染纺织品、染料、电力、蒸汽、织造布、黄金饰品", "founded_year": 1998, "employee_count": 9322},
        {"company_id": "sh_600027", "name_zh": "华电国际", "name_en": "Huadian Power International Corp., Ltd.", "country": "CN", "province": "山东", "city": "济南市", "stock_codes": ["600027.SH"], "description": "火力发电及电力和热力供应", "founded_year": 1994, "employee_count": 30595},
        {"company_id": "sz_002039", "name_zh": "黔源电力", "name_en": "Guizhou Qianyuan Power Co., Ltd.", "country": "CN", "province": "贵州", "city": "贵阳市", "stock_codes": ["002039.SZ"], "description": "水力、火力发电站的开发建设与经营管理", "founded_year": 1993, "employee_count": 828},
        {"company_id": "sz_002040", "name_zh": "南京港", "name_en": "Nanjing Port Co., Ltd.", "country": "CN", "province": "江苏", "city": "南京市", "stock_codes": ["002040.SZ"], "description": "原油、成品油、液体化工产品的装卸、储存等港口服务", "founded_year": 2001, "employee_count": 981},
        {"company_id": "sh_600970", "name_zh": "中材国际", "name_en": "China National Materials International Engineering Co., Ltd.", "country": "CN", "province": "江苏", "city": "南京市", "stock_codes": ["600970.SH"], "description": "大中型新型干法水泥生产线的建设和工程总承包", "founded_year": 2001, "employee_count": 15201},
        {"company_id": "sz_002041", "name_zh": "登海种业", "name_en": "Shandong Denghai Seeds Co., Ltd.", "country": "CN", "province": "山东", "city": "烟台市", "stock_codes": ["002041.SZ"], "description": "玉米种、蔬菜种、花卉等农作物种子的选育、生产和销售", "founded_year": 2000, "employee_count": 822},
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sh_600981_produce_textile_garment", "company_id": "sh_600981", "node_id": "textile_garment", "activity_type": "produce", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:纺织品及服装进出口")},
        {"exposure_id": "sh_600981_produce_textile_raw_material", "company_id": "sh_600981", "node_id": "textile_raw_material", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:纺织原料及制成品")},
        {"exposure_id": "sh_600981_produce_electronic_equipment", "company_id": "sh_600981", "node_id": "electronic_equipment", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电子设备研发")},
        {"exposure_id": "sh_600982_provide_service_electric_power", "company_id": "sh_600982", "node_id": "electric_power", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电力生产")},
        {"exposure_id": "sh_600982_provide_service_steam", "company_id": "sh_600982", "node_id": "steam", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:蒸汽电力电量")},
        {"exposure_id": "sh_600982_provide_service_heat_supply", "company_id": "sh_600982", "node_id": "heat_supply", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:热力供应")},
        {"exposure_id": "sh_600982_operate_thermal_power_generation", "company_id": "sh_600982", "node_id": "thermal_power_generation", "activity_type": "operate", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发电业务")},
        {"exposure_id": "sh_600983_produce_washing_machine", "company_id": "sh_600983", "node_id": "washing_machine", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:全自动洗衣机")},
        {"exposure_id": "sh_600983_produce_refrigerator", "company_id": "sh_600983", "node_id": "refrigerator", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:冰箱")},
        {"exposure_id": "sh_600983_produce_microwave_oven", "company_id": "sh_600983", "node_id": "microwave_oven", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:微波炉")},
        {"exposure_id": "sh_600983_produce_air_purifier", "company_id": "sh_600983", "node_id": "air_purifier", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:空气净化器")},
        {"exposure_id": "sh_600983_produce_kitchen_appliance", "company_id": "sh_600983", "node_id": "kitchen_appliance", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:厨房电器")},
        {"exposure_id": "sh_600984_produce_asphalt_concrete_pavers", "company_id": "sh_600984", "node_id": "asphalt_concrete_pavers", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:沥青混凝土摊铺机")},
        {"exposure_id": "sh_600984_produce_stabilized_soil_mixer", "company_id": "sh_600984", "node_id": "stabilized_soil_mixer", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:全液压稳定土拌和机")},
        {"exposure_id": "sh_600984_produce_construction_machinery", "company_id": "sh_600984", "node_id": "construction_machinery", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:工程建筑机械")},
        {"exposure_id": "sh_600984_produce_hoisting_machinery", "company_id": "sh_600984", "node_id": "hoisting_machinery", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:起重机械成套装备")},
        {"exposure_id": "sh_600984_produce_mining_machinery", "company_id": "sh_600984", "node_id": "mining_machinery", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:矿山机械成套装备")},
        {"exposure_id": "sh_600987_operate_textile_printing_dyeing", "company_id": "sh_600987", "node_id": "textile_printing_dyeing", "activity_type": "operate", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:印染")},
        {"exposure_id": "sh_600987_produce_textile_garment", "company_id": "sh_600987", "node_id": "textile_garment", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:印染纺织品")},
        {"exposure_id": "sh_600987_produce_woven_fabric", "company_id": "sh_600987", "node_id": "woven_fabric", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:织造布")},
        {"exposure_id": "sh_600987_produce_gold_jewelry", "company_id": "sh_600987", "node_id": "gold_jewelry", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:黄金饰品加工批发")},
        {"exposure_id": "sh_600987_provide_service_electricity_supply", "company_id": "sh_600987", "node_id": "electricity_supply", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电力")},
        {"exposure_id": "sh_600987_provide_service_steam", "company_id": "sh_600987", "node_id": "steam", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:蒸汽")},
        {"exposure_id": "sh_600987_produce_dye", "company_id": "sh_600987", "node_id": "dye", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:染料")},
        {"exposure_id": "sh_600027_operate_thermal_power_generation", "company_id": "sh_600027", "node_id": "thermal_power_generation", "activity_type": "operate", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:火力发电")},
        {"exposure_id": "sh_600027_provide_service_electric_power", "company_id": "sh_600027", "node_id": "electric_power", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发电业务输电业务供配电业务")},
        {"exposure_id": "sh_600027_provide_service_heat_supply", "company_id": "sh_600027", "node_id": "heat_supply", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:热力生产和供应")},
        {"exposure_id": "sh_600027_provide_service_electricity_supply", "company_id": "sh_600027", "node_id": "electricity_supply", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:供电业务")},
        {"exposure_id": "sz_002039_operate_hydro_power", "company_id": "sz_002039", "node_id": "hydro_power", "activity_type": "operate", "weight": 0.50, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:水力发电")},
        {"exposure_id": "sz_002039_operate_thermal_power_generation", "company_id": "sz_002039", "node_id": "thermal_power_generation", "activity_type": "operate", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:火力发电")},
        {"exposure_id": "sz_002039_provide_service_electric_power", "company_id": "sz_002039", "node_id": "electric_power", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主要产品:电力")},
        {"exposure_id": "sz_002040_operate_port", "company_id": "sz_002040", "node_id": "port", "activity_type": "operate", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:港口经营")},
        {"exposure_id": "sz_002040_provide_service_crude_oil", "company_id": "sz_002040", "node_id": "crude_oil", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:原油装卸储存")},
        {"exposure_id": "sz_002040_provide_service_refined_oil_product", "company_id": "sz_002040", "node_id": "refined_oil_product", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:成品油装卸储存")},
        {"exposure_id": "sz_002040_provide_service_liquid_chemical", "company_id": "sz_002040", "node_id": "liquid_chemical", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:液体化工产品装卸储存")},
        {"exposure_id": "sh_600970_provide_service_cement_production_line", "company_id": "sh_600970", "node_id": "cement_production_line", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:大中型新型干法水泥生产线建设")},
        {"exposure_id": "sh_600970_provide_service_engineering_contracting", "company_id": "sh_600970", "node_id": "engineering_contracting", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:工程总承包")},
        {"exposure_id": "sh_600970_produce_cement_equipment", "company_id": "sh_600970", "node_id": "cement_equipment", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:装备采购与制造")},
        {"exposure_id": "sh_600970_produce_concrete_product", "company_id": "sh_600970", "node_id": "concrete_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:混凝土制品研发生产销售")},
        {"exposure_id": "sh_600970_provide_service_construction_engineering", "company_id": "sh_600970", "node_id": "construction_engineering", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建设安装工程")},
        {"exposure_id": "sz_002041_produce_corn_seed", "company_id": "sz_002041", "node_id": "corn_seed", "activity_type": "produce", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:玉米种")},
        {"exposure_id": "sz_002041_produce_vegetable_seed", "company_id": "sz_002041", "node_id": "vegetable_seed", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:蔬菜种")},
        {"exposure_id": "sz_002041_produce_flower", "company_id": "sz_002041", "node_id": "flower", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:花卉")},
        {"exposure_id": "sz_002041_produce_crop_seed", "company_id": "sz_002041", "node_id": "crop_seed", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:农作物新品种的选育生产销售")},
        {"exposure_id": "sz_002041_provide_service_technical_service", "company_id": "sz_002041", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:农业高新技术研发及成果转让")},
    ],
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
}

def submit():
    batch = {"batch_id": "batch_117_nodes", "task_description": "Batch 117 industrial nodes and edges", "nodes_to_upsert": NODES, "edges_to_upsert": EDGES}
    path = os.path.join(BASE_DIR, "tmp_script", "batch_117_nodes.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    r1 = subprocess.run([PY, CLI_PATH, "submit", path], capture_output=True, text=True)
    print("[GRAPH]", r1.stdout[:500], r1.stderr[:500])

    path2 = os.path.join(BASE_DIR, "tmp_script", "batch_117_business.json")
    with open(path2, "w", encoding="utf-8") as f:
        json.dump(BUSINESS, f, ensure_ascii=False, indent=2)
    r2 = subprocess.run([PY, CLI_PATH, "business-batch", path2], capture_output=True, text=True)
    print("[BUSINESS]", r2.stdout[:500], r2.stderr[:500])

if __name__ == "__main__":
    submit()
