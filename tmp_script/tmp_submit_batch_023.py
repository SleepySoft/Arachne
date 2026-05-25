#!/usr/bin/env python3
"""Batch 023 Submission Script"""
import json
import requests

BASE_URL = "http://localhost:8000/api/v1"

def submit_graph_batch(batch):
    r = requests.post(f"{BASE_URL}/batches", json=batch)
    return r.status_code, r.json()

def submit_business_batch(batch):
    r = requests.post(f"{BASE_URL}/business-batches", json=batch)
    return r.status_code, r.json()

# ---------------------------------------------------------------------------
# 1. INDUSTRIAL NODES
# ---------------------------------------------------------------------------

nodes = [
    {
        "node_id": "automotive_bumper",
        "canonical_name_zh": "汽车保险杠",
        "canonical_name_en": "Automotive Bumper",
        "aliases": ["保险杠", "前保后保"],
        "definition": "安装在汽车前后端的吸能缓冲外饰件，通常由塑料（PP/EPDM）或金属制成，用于吸收碰撞能量、保护车身及行人安全，是汽车车身外饰系统的关键组成部分。",
        "entity_type": "component",
        "evidence": [{"source_title": "模塑科技 主营业务", "quote": "主要产品:保险杠,防擦条等汽车装饰件"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "automotive_molding_trim",
        "canonical_name_zh": "汽车装饰件",
        "canonical_name_en": "Automotive Molding Trim",
        "aliases": ["汽车外饰件", "防擦条", "饰条"],
        "definition": "安装于汽车车身表面，兼具装饰性与功能性的塑料或金属零部件，包括防擦条、门槛饰板、轮眉、格栅等，用于提升外观品质与空气动力学性能。",
        "entity_type": "component",
        "evidence": [{"source_title": "模塑科技 主营业务", "quote": "主要产品:保险杠,防擦条等汽车装饰件"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "electronic_information_service",
        "canonical_name_zh": "电子信息服务",
        "canonical_name_en": "Electronic Information Service",
        "aliases": ["电子信息产业", "ICT服务"],
        "definition": "以电子信息技术为核心，提供软件开发、信息系统集成、数据处理、网络服务及电子产品销售的技术服务业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "厦门信达 主营业务", "quote": "主要业务:电子信息产业,贸易和房地产开发"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "feed",
        "canonical_name_zh": "饲料",
        "canonical_name_en": "Animal Feed",
        "aliases": ["畜禽饲料", "配合饲料"],
        "definition": "根据畜禽不同生长阶段营养需求，将能量饲料、蛋白饲料、矿物质、维生素及添加剂按配方加工而成的工业化饲养物料，是现代化养殖产业链的上游投入品。",
        "entity_type": "material",
        "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:饲料,肉食品"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "meat_product",
        "canonical_name_zh": "肉食品",
        "canonical_name_en": "Meat Product",
        "aliases": ["肉制品", "肉类加工品"],
        "definition": "以畜禽鲜肉为原料，经屠宰、分割、腌制、熟制、包装等工艺加工而成的食用产品，包括冷鲜肉、冷冻肉、调理肉制品、熟肉制品等。",
        "entity_type": "material",
        "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:饲料,肉食品"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "polyester_chip",
        "canonical_name_zh": "聚酯切片",
        "canonical_name_en": "Polyester Chip",
        "aliases": ["PET切片", "瓶级切片"],
        "definition": "以精对苯二甲酸（PTA）和乙二醇（MEG）为原料，经酯化、缩聚反应制成的聚酯高分子颗粒，是生产涤纶纤维、聚酯瓶片及工程塑料的基础原料。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是精对苯二甲酸(PTA),聚酯切片,聚酯瓶片"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "polyester_bottle_chip",
        "canonical_name_zh": "聚酯瓶片",
        "canonical_name_en": "Polyester Bottle Chip",
        "aliases": ["瓶级PET", "PET瓶片"],
        "definition": "以聚酯切片为原料，经固相缩聚增粘工艺制成的高粘度聚酯切片，专用于吹塑生产碳酸饮料瓶、矿泉水瓶、食用油瓶等PET包装容器。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是...聚酯瓶片"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "poy",
        "canonical_name_zh": "涤纶预取向丝",
        "canonical_name_en": "Partially Oriented Yarn (POY)",
        "aliases": ["POY", "预取向丝"],
        "definition": "聚酯切片经熔融纺丝、高速卷绕制成的部分取向长丝，分子链取向度介于未取向丝与全拉伸丝之间，需进一步加工成FDY或DTY才能用于织造。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是...涤纶预取向丝(POY)"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "fdy",
        "canonical_name_zh": "涤纶全拉伸丝",
        "canonical_name_en": "Fully Drawn Yarn (FDY)",
        "aliases": ["FDY", "全拉伸丝"],
        "definition": "聚酯切片经熔融纺丝、热拉伸定型制成的全取向长丝，可直接用于织造或经编，具有强度高、伸长小、尺寸稳定性好的特点。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶全拉伸丝(FDY)"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "dty",
        "canonical_name_zh": "涤纶拉伸变形丝",
        "canonical_name_en": "Draw Textured Yarn (DTY)",
        "aliases": ["DTY", "弹力丝", "低弹丝"],
        "definition": "以涤纶预取向丝（POY）为原料，经拉伸假捻变形加工制成的具有卷曲弹性的长丝，广泛用于机织、针织面料，赋予织物柔软蓬松的手感。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶拉伸变形丝(DTY)"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "polyester_staple",
        "canonical_name_zh": "涤纶短纤",
        "canonical_name_en": "Polyester Staple Fiber",
        "aliases": ["涤短", "PET短纤"],
        "definition": "聚酯切片经熔融纺丝、集束、拉伸、卷曲、切断等工序制成的短纤维，长度32-51mm，可纯纺或与棉、粘胶等纤维混纺，用于服装、家纺及产业用纺织品。",
        "entity_type": "material",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶短纤"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "ammonium_chloride",
        "canonical_name_zh": "氯化铵",
        "canonical_name_en": "Ammonium Chloride",
        "aliases": ["氯铵", "电盐"],
        "definition": "化学式为NH₄Cl的白色结晶性粉末，联碱法生产纯碱的联产品，主要用作氮肥、干电池电解质、金属焊接助熔剂及医药中间体原料。",
        "entity_type": "material",
        "evidence": [{"source_title": "双环科技 主营业务", "quote": "主要产品:联碱产品"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "special_steel",
        "canonical_name_zh": "特殊钢材",
        "canonical_name_en": "Special Steel",
        "aliases": ["特钢", "合金钢"],
        "definition": "通过添加合金元素（Cr、Ni、Mo、V、W等）或采用特殊冶炼工艺，使钢材具备特定物理化学性能的钢类，包括齿轮钢、轴承钢、弹簧钢、工模具钢、高温合金钢等，用于高端装备制造。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:齿轮钢,轴承钢,弹簧钢,工模具钢,高温合金钢等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "gear_steel",
        "canonical_name_zh": "齿轮钢",
        "canonical_name_en": "Gear Steel",
        "aliases": ["渗碳钢", "齿轮用钢"],
        "definition": "专用于制造齿轮的合金结构钢，要求具备良好的淬透性、渗碳性能、接触疲劳强度和耐磨性，常见牌号包括20CrMnTi、20CrNiMo等。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:齿轮钢...等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "bearing_steel",
        "canonical_name_zh": "轴承钢",
        "canonical_name_en": "Bearing Steel",
        "aliases": ["滚珠轴承钢", "高碳铬钢"],
        "definition": "用于制造滚动轴承套圈和滚动体的专用钢材，要求极高的纯净度、均匀的组织、高硬度与耐磨性，典型牌号为GCr15，是特钢中技术要求最高的品种之一。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...轴承钢...等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "spring_steel",
        "canonical_name_zh": "弹簧钢",
        "canonical_name_en": "Spring Steel",
        "aliases": ["弹性钢", "弹簧用钢"],
        "definition": "用于制造各种弹簧及弹性元件的专用钢材，要求具有高弹性极限、疲劳强度和足够的韧性，常见牌号包括60Si2Mn、50CrVA等。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...弹簧钢...等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "tool_die_steel",
        "canonical_name_zh": "工模具钢",
        "canonical_name_en": "Tool and Die Steel",
        "aliases": ["模具钢", "工具钢"],
        "definition": "用于制造切削工具、冷作模具、热作模具和塑料模具的专用钢材，要求具备高硬度、耐磨性、红硬性和抗热疲劳性能，是机械制造业的基础材料。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...工模具钢...等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "high_temperature_alloy_steel",
        "canonical_name_zh": "高温合金钢",
        "canonical_name_en": "High-Temperature Alloy Steel",
        "aliases": ["耐热合金钢", "高温合金"],
        "definition": "以铁、镍、钴为基体，添加Cr、Mo、W、Al、Ti等合金元素，能在600℃以上高温及应力作用下长期工作的合金材料，广泛用于航空发动机、燃气轮机和核电设备。",
        "entity_type": "material",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...高温合金钢等特殊钢材"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "steel_plate",
        "canonical_name_zh": "板材",
        "canonical_name_en": "Steel Plate",
        "aliases": ["钢板", "中厚板"],
        "definition": "通过热轧或冷轧工艺制成的平板状钢材，按厚度分为薄板（<4mm）和中厚板（≥4mm），广泛应用于船舶、桥梁、建筑、压力容器、汽车等领域。",
        "entity_type": "material",
        "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:板材,棒材,线材,型材四大类"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "steel_bar",
        "canonical_name_zh": "棒材",
        "canonical_name_en": "Steel Bar",
        "aliases": ["圆钢", "棒钢"],
        "definition": "截面为圆形、方形或六角形的长条状钢材，直径通常5-250mm，主要用于机械制造零部件、建筑结构件及轴类零件的原材料。",
        "entity_type": "material",
        "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:板材,棒材,线材,型材四大类"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "steel_wire_rod",
        "canonical_name_zh": "线材",
        "canonical_name_en": "Steel Wire Rod",
        "aliases": ["盘条", "盘圆"],
        "definition": "直径5.5-16mm的热轧圆钢盘卷，是生产钢丝、钢丝绳、钢绞线、焊接钢丝网及各类紧固件的原材料，也可直接用于建筑钢筋。",
        "entity_type": "material",
        "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:板材,棒材,线材,型材四大类"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "steel_section",
        "canonical_name_zh": "型材",
        "canonical_name_en": "Steel Section",
        "aliases": ["型钢", "结构钢"],
        "definition": "具有特定截面形状（如H型、I型、角型、槽型、T型等）的钢材，主要用于建筑钢结构、桥梁、工程机械及车辆底盘等承力结构。",
        "entity_type": "material",
        "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:板材,棒材,线材,型材四大类"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "genetic_testing_service",
        "canonical_name_zh": "基因检测服务",
        "canonical_name_en": "Genetic Testing Service",
        "aliases": ["基因测序服务", "分子诊断服务"],
        "definition": "以高通量测序（NGS）或PCR技术为核心，对DNA/RNA样本进行序列测定与生物信息学分析，为临床诊断、生育健康、肿瘤早筛和药物基因组学提供检测服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "主要业务:以测序为基础的基因检测服务与设备试剂销售"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "gene_sequencing_equipment",
        "canonical_name_zh": "基因测序设备",
        "canonical_name_en": "Gene Sequencing Equipment",
        "aliases": ["测序仪", "基因分析仪"],
        "definition": "用于测定DNA或RNA核苷酸序列的精密仪器，包括样本制备系统、测序反应平台及信号检测模块，是基因检测服务产业链的核心硬件。",
        "entity_type": "device",
        "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "以测序为基础的基因检测服务与设备试剂销售"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "gene_sequencing_reagent",
        "canonical_name_zh": "基因测序试剂",
        "canonical_name_en": "Gene Sequencing Reagent",
        "aliases": ["测序试剂盒", "文库构建试剂"],
        "definition": "基因测序过程中使用的各类化学试剂与消耗品，包括DNA提取试剂、文库构建试剂、测序芯片、荧光染料及配套缓冲液等。",
        "entity_type": "material",
        "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "以测序为基础的基因检测服务与设备试剂销售"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "smart_ecological_operation",
        "canonical_name_zh": "智慧生态运营",
        "canonical_name_en": "Smart Ecological Operation",
        "aliases": ["智慧生态服务", "生态运营管理"],
        "definition": "运用物联网、大数据与人工智能技术，对生态环境（水、土、气、植被）进行智能监测、评估与修复治理的综合性运营服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "ST京蓝 主营业务", "quote": "主营业务:智慧生态运营服务,清洁能源综合服务"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "clean_energy_service",
        "canonical_name_zh": "清洁能源服务",
        "canonical_name_en": "Clean Energy Service",
        "aliases": ["清洁能源运营", "新能源服务"],
        "definition": "围绕清洁能源（太阳能、风能、生物质能等）的开发、投资、建设、运营及技术咨询提供的一站式服务，旨在降低碳排放并优化能源结构。",
        "entity_type": "service",
        "evidence": [{"source_title": "ST京蓝 主营业务", "quote": "清洁能源综合服务"}],
        "confidence": "HIGH", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 2. INDUSTRIAL EDGES
# ---------------------------------------------------------------------------

edges = [
    {
        "edge_id": "flow_bumper_to_car",
        "from_node": "automotive_bumper",
        "to_node": "passenger_car",
        "description": "汽车保险杠作为外饰安全件装配于乘用车前后端，构成车身外饰系统。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "模塑科技 主营业务", "quote": "主要产品:保险杠...等汽车装饰件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_trim_to_car",
        "from_node": "automotive_molding_trim",
        "to_node": "passenger_car",
        "description": "汽车装饰件（防擦条、门槛饰板等）装配于乘用车车身，兼具装饰与功能属性。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "模塑科技 主营业务", "quote": "防擦条等汽车装饰件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_feed_to_pig",
        "from_node": "feed",
        "to_node": "live_pig",
        "description": "饲料作为投入品用于生猪养殖，提供生长所需的营养物质。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:饲料,肉食品"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pig_to_meat",
        "from_node": "live_pig",
        "to_node": "meat_product",
        "description": "生猪经屠宰、分割与加工制成肉食品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:饲料,肉食品"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pta_to_chip",
        "from_node": "pta",
        "to_node": "polyester_chip",
        "description": "精对苯二甲酸（PTA）与乙二醇（MEG）经酯化缩聚反应生成聚酯切片。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是精对苯二甲酸(PTA),聚酯切片"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_chip_to_filament",
        "from_node": "polyester_chip",
        "to_node": "polyester_filament",
        "description": "聚酯切片经熔融纺丝制成涤纶长丝。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是...聚酯切片...涤纶预取向丝(POY),涤纶全拉伸丝(FDY),涤纶拉伸变形丝(DTY),涤纶短纤"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_chip_to_staple",
        "from_node": "polyester_chip",
        "to_node": "polyester_staple",
        "description": "聚酯切片经熔融纺丝、切断制成涤纶短纤。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶短纤"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_chip_to_bottle_chip",
        "from_node": "polyester_chip",
        "to_node": "polyester_bottle_chip",
        "description": "聚酯切片经固相缩聚增粘工艺制成高粘度瓶级切片（聚酯瓶片）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "聚酯瓶片"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_poy_to_fdy",
        "from_node": "poy",
        "to_node": "fdy",
        "description": "涤纶预取向丝（POY）经热拉伸定型加工制成全拉伸丝（FDY）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶预取向丝(POY),涤纶全拉伸丝(FDY)"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_poy_to_dty",
        "from_node": "poy",
        "to_node": "dty",
        "description": "涤纶预取向丝（POY）经拉伸假捻变形加工制成拉伸变形丝（DTY）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶预取向丝(POY)...涤纶拉伸变形丝(DTY)"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_salt_to_soda",
        "from_node": "salt_product",
        "to_node": "soda_ash",
        "description": "原盐（氯化钠）是联碱法生产纯碱的主要原料之一，与氨、二氧化碳反应生成纯碱。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "双环科技 主营业务", "quote": "主要产品:联碱产品"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_soda_to_ammonium",
        "from_node": "soda_ash",
        "to_node": "ammonium_chloride",
        "description": "联碱法工艺中，纯碱与氯化铵为联产品，同时产出。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "双环科技 主营业务", "quote": "主要产品:联碱产品"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "is_a_gear_steel",
        "from_node": "gear_steel",
        "to_node": "special_steel",
        "description": "齿轮钢是特殊钢材的重要品种之一，属于合金结构钢范畴。",
        "edge_namespace": "ontology",
        "edge_type": "is_a",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:齿轮钢...等特殊钢材"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "is_a_bearing_steel",
        "from_node": "bearing_steel",
        "to_node": "special_steel",
        "description": "轴承钢是特殊钢材中技术要求最高的品种之一。",
        "edge_namespace": "ontology",
        "edge_type": "is_a",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...轴承钢...等特殊钢材"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "is_a_spring_steel",
        "from_node": "spring_steel",
        "to_node": "special_steel",
        "description": "弹簧钢是特殊钢材中专用于制造弹性元件的品种。",
        "edge_namespace": "ontology",
        "edge_type": "is_a",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...弹簧钢...等特殊钢材"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "is_a_tool_die_steel",
        "from_node": "tool_die_steel",
        "to_node": "special_steel",
        "description": "工模具钢是特殊钢材中用于制造工具与模具的专用品种。",
        "edge_namespace": "ontology",
        "edge_type": "is_a",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...工模具钢...等特殊钢材"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "is_a_ht_alloy_steel",
        "from_node": "high_temperature_alloy_steel",
        "to_node": "special_steel",
        "description": "高温合金钢是特殊钢材中能在高温环境下长期工作的耐热合金品种。",
        "edge_namespace": "ontology",
        "edge_type": "is_a",
        "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...高温合金钢等特殊钢材"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_reagent_to_testing",
        "from_node": "gene_sequencing_reagent",
        "to_node": "genetic_testing_service",
        "description": "基因测序试剂作为消耗品用于基因检测服务流程中的样本处理与测序反应。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "以测序为基础的基因检测服务与设备试剂销售"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_equipment_to_testing",
        "from_node": "gene_sequencing_equipment",
        "to_node": "genetic_testing_service",
        "description": "基因测序设备为基因检测服务提供核心的测序能力支撑。",
        "edge_namespace": "industrial_flow",
        "edge_type": "capability_supply",
        "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "以测序为基础的基因检测服务与设备试剂销售"}],
        "confidence": "HIGH"
    }
]

# ---------------------------------------------------------------------------
# 3. COMPANIES
# ---------------------------------------------------------------------------

companies = [
    {
        "company_id": "mosu_tech",
        "name_zh": "江南模塑科技股份有限公司",
        "aliases": ["模塑科技"],
        "stock_codes": ["000700.SZ"],
        "description": "主要产品包括保险杠、防擦条等汽车装饰件，同时涉及医疗服务领域。",
        "country": "CN", "province": "江苏", "city": "无锡市",
        "founded_year": 1988, "employee_count": 5880,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "xiamen_xinda",
        "name_zh": "厦门信达股份有限公司",
        "aliases": ["厦门信达"],
        "stock_codes": ["000701.SZ"],
        "description": "主要业务包括电子信息产业、贸易和房地产开发。",
        "country": "CN", "province": "福建", "city": "厦门市",
        "founded_year": 1996, "employee_count": 3998,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhenghong_tech",
        "name_zh": "湖南正虹科技发展股份有限公司",
        "aliases": ["正虹科技"],
        "stock_codes": ["000702.SZ"],
        "description": "主要产品包括饲料和肉食品，涵盖农业产业化的系列开发。",
        "country": "CN", "province": "湖南", "city": "岳阳市",
        "founded_year": 1997, "employee_count": 639,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "hengyi_petrochemical",
        "name_zh": "恒逸石化股份有限公司",
        "aliases": ["恒逸石化"],
        "stock_codes": ["000703.SZ"],
        "description": "公司主要产品是精对苯二甲酸(PTA)、聚酯切片、聚酯瓶片、涤纶预取向丝(POY)、涤纶全拉伸丝(FDY)、涤纶拉伸变形丝(DTY)、涤纶短纤。",
        "country": "CN", "province": "广西", "city": "钦州市",
        "founded_year": 1996, "employee_count": 16014,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhejiang_zhenyuan",
        "name_zh": "浙江震元股份有限公司",
        "aliases": ["浙江震元"],
        "stock_codes": ["000705.SZ"],
        "description": "主要业务为医药商业的批发、零售和医药工业产品销售。",
        "country": "CN", "province": "浙江", "city": "绍兴市",
        "founded_year": 1993, "employee_count": 2073,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "shuanghuan_tech",
        "name_zh": "湖北双环科技股份有限公司",
        "aliases": ["双环科技"],
        "stock_codes": ["000707.SZ"],
        "description": "主要产品为联碱产品（纯碱、氯化铵）。",
        "country": "CN", "province": "湖北", "city": "孝感市",
        "founded_year": 1993, "employee_count": 1222,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "citic_special_steel",
        "name_zh": "中信泰富特钢集团股份有限公司",
        "aliases": ["中信特钢"],
        "stock_codes": ["000708.SZ"],
        "description": "主要产品包括齿轮钢、轴承钢、弹簧钢、工模具钢、高温合金钢等特殊钢材，主要业务为钢铁冶炼、钢材轧制、金属改制、压延加工、钢铁材料检测等。",
        "country": "CN", "province": "湖北", "city": "黄石市",
        "founded_year": 1993, "employee_count": 31584,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "hegang_share",
        "name_zh": "河钢股份有限公司",
        "aliases": ["河钢股份"],
        "stock_codes": ["000709.SZ"],
        "description": "主要产品包括板材、棒材、线材、型材四大类，主要业务为黑色金属冶炼、钢材轧制、金属制品。",
        "country": "CN", "province": "河北", "city": "石家庄市",
        "founded_year": 1997, "employee_count": 29939,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "berry_genomics",
        "name_zh": "成都市贝瑞和康基因技术股份有限公司",
        "aliases": ["贝瑞基因"],
        "stock_codes": ["000710.SZ"],
        "description": "主要业务为以测序为基础的基因检测服务与设备试剂销售。",
        "country": "CN", "province": "四川", "city": "成都市",
        "founded_year": 1997, "employee_count": 1402,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "st_jinglan",
        "name_zh": "铟靶新材(哈尔滨)股份有限公司",
        "aliases": ["ST京蓝", "京蓝科技"],
        "stock_codes": ["000711.SZ"],
        "description": "主营业务包括智慧生态运营服务、清洁能源综合服务、生态功能保护区管理服务、节水管理与技术咨询服务等。",
        "country": "CN", "province": "黑龙江", "city": "哈尔滨市",
        "founded_year": 1993, "employee_count": 537,
        "company_type": "public", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 4. COMPANY NODE EXPOSURES
# ---------------------------------------------------------------------------

exposures = [
    # 模塑科技
    {"exposure_id": "exp_ms_bumper", "company_id": "mosu_tech", "node_id": "automotive_bumper", "activity_type": "manufacture", "role": "汽车保险杠制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "模塑科技 主营业务", "quote": "主要产品:保险杠"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ms_trim", "company_id": "mosu_tech", "node_id": "automotive_molding_trim", "activity_type": "manufacture", "role": "汽车装饰件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "模塑科技 主营业务", "quote": "防擦条等汽车装饰件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ms_medical", "company_id": "mosu_tech", "node_id": "medical_device", "activity_type": "manufacture", "role": "医疗器械制造商", "weight": 0.4, "confidence": "HIGH", "evidence": [{"source_title": "模塑科技 主营业务", "quote": "主要业务:...医疗"}], "status": "ACTIVE"},

    # 厦门信达
    {"exposure_id": "exp_xx_electronic_info", "company_id": "xiamen_xinda", "node_id": "electronic_information_service", "activity_type": "operate", "role": "电子信息服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "厦门信达 主营业务", "quote": "主要业务:电子信息产业"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xx_trade", "company_id": "xiamen_xinda", "node_id": "trade_service", "activity_type": "operate", "role": "贸易商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "厦门信达 主营业务", "quote": "贸易"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xx_realestate", "company_id": "xiamen_xinda", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "厦门信达 主营业务", "quote": "房地产开发"}], "status": "ACTIVE"},

    # 正虹科技
    {"exposure_id": "exp_zh_feed", "company_id": "zhenghong_tech", "node_id": "feed", "activity_type": "produce", "role": "饲料生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:饲料"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zh_meat", "company_id": "zhenghong_tech", "node_id": "meat_product", "activity_type": "produce", "role": "肉食品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "正虹科技 主营业务", "quote": "主要产品:肉食品"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zh_pig", "company_id": "zhenghong_tech", "node_id": "live_pig", "activity_type": "produce", "role": "生猪养殖商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "正虹科技 主营业务", "quote": "农业产业化的系列开发"}], "status": "ACTIVE"},

    # 恒逸石化
    {"exposure_id": "exp_hy_pta", "company_id": "hengyi_petrochemical", "node_id": "pta", "activity_type": "produce", "role": "PTA生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "公司主要产品是精对苯二甲酸(PTA)"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_chip", "company_id": "hengyi_petrochemical", "node_id": "polyester_chip", "activity_type": "produce", "role": "聚酯切片生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "聚酯切片"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_bottle_chip", "company_id": "hengyi_petrochemical", "node_id": "polyester_bottle_chip", "activity_type": "produce", "role": "聚酯瓶片生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "聚酯瓶片"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_poy", "company_id": "hengyi_petrochemical", "node_id": "poy", "activity_type": "produce", "role": "涤纶预取向丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶预取向丝(POY)"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_fdy", "company_id": "hengyi_petrochemical", "node_id": "fdy", "activity_type": "produce", "role": "涤纶全拉伸丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶全拉伸丝(FDY)"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_dty", "company_id": "hengyi_petrochemical", "node_id": "dty", "activity_type": "produce", "role": "涤纶拉伸变形丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶拉伸变形丝(DTY)"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_staple", "company_id": "hengyi_petrochemical", "node_id": "polyester_staple", "activity_type": "produce", "role": "涤纶短纤生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶短纤"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hy_filament", "company_id": "hengyi_petrochemical", "node_id": "polyester_filament", "activity_type": "produce", "role": "涤纶长丝生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "恒逸石化 主营业务", "quote": "涤纶预取向丝(POY),涤纶全拉伸丝(FDY),涤纶拉伸变形丝(DTY)"}], "status": "ACTIVE"},

    # 浙江震元
    {"exposure_id": "exp_zy_distribution", "company_id": "zhejiang_zhenyuan", "node_id": "pharmaceutical_distribution", "activity_type": "operate", "role": "医药批发分销商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "浙江震元 主营业务", "quote": "医药商业的批发"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zy_retail", "company_id": "zhejiang_zhenyuan", "node_id": "pharmaceutical_retail", "activity_type": "operate", "role": "医药零售商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "浙江震元 主营业务", "quote": "零售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zy_pharma_product", "company_id": "zhejiang_zhenyuan", "node_id": "pharmaceutical_product", "activity_type": "manufacture", "role": "医药产品制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "浙江震元 主营业务", "quote": "医药工业产品销售"}], "status": "ACTIVE"},

    # 双环科技
    {"exposure_id": "exp_sh_soda", "company_id": "shuanghuan_tech", "node_id": "soda_ash", "activity_type": "produce", "role": "纯碱生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "双环科技 主营业务", "quote": "主要产品:联碱产品"}], "status": "ACTIVE"},
    {"exposure_id": "exp_sh_ammonium", "company_id": "shuanghuan_tech", "node_id": "ammonium_chloride", "activity_type": "produce", "role": "氯化铵生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "双环科技 主营业务", "quote": "主要产品:联碱产品"}], "status": "ACTIVE"},

    # 中信特钢
    {"exposure_id": "exp_ct_special_steel", "company_id": "citic_special_steel", "node_id": "special_steel", "activity_type": "produce", "role": "特殊钢材综合制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要业务:钢铁冶炼,钢材轧制,金属改制,压延加工,钢铁材料检测等"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ct_gear_steel", "company_id": "citic_special_steel", "node_id": "gear_steel", "activity_type": "produce", "role": "齿轮钢制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:齿轮钢"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ct_bearing_steel", "company_id": "citic_special_steel", "node_id": "bearing_steel", "activity_type": "produce", "role": "轴承钢制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...轴承钢...等特殊钢材"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ct_spring_steel", "company_id": "citic_special_steel", "node_id": "spring_steel", "activity_type": "produce", "role": "弹簧钢制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...弹簧钢...等特殊钢材"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ct_tool_die", "company_id": "citic_special_steel", "node_id": "tool_die_steel", "activity_type": "produce", "role": "工模具钢制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...工模具钢...等特殊钢材"}], "status": "ACTIVE"},
    {"exposure_id": "exp_ct_ht_alloy", "company_id": "citic_special_steel", "node_id": "high_temperature_alloy_steel", "activity_type": "produce", "role": "高温合金钢制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "中信特钢 主营业务", "quote": "主要产品:...高温合金钢等特殊钢材"}], "status": "ACTIVE"},

    # 河钢股份
    {"exposure_id": "exp_hg_plate", "company_id": "hegang_share", "node_id": "steel_plate", "activity_type": "produce", "role": "板材生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:板材"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hg_bar", "company_id": "hegang_share", "node_id": "steel_bar", "activity_type": "produce", "role": "棒材生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:...棒材..."}], "status": "ACTIVE"},
    {"exposure_id": "exp_hg_wire_rod", "company_id": "hegang_share", "node_id": "steel_wire_rod", "activity_type": "produce", "role": "线材生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:...线材..."}], "status": "ACTIVE"},
    {"exposure_id": "exp_hg_section", "company_id": "hegang_share", "node_id": "steel_section", "activity_type": "produce", "role": "型材生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "河钢股份 主营业务", "quote": "主要产品:...型材四大类"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hg_sheet", "company_id": "hegang_share", "node_id": "steel_sheet", "activity_type": "produce", "role": "冷轧钢板生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "河钢股份 经营范围", "quote": "钢材,钢坯...的生产销售"}], "status": "ACTIVE"},

    # 贝瑞基因
    {"exposure_id": "exp_br_testing", "company_id": "berry_genomics", "node_id": "genetic_testing_service", "activity_type": "provide_service", "role": "基因检测服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "以测序为基础的基因检测服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_br_equipment", "company_id": "berry_genomics", "node_id": "gene_sequencing_equipment", "activity_type": "manufacture", "role": "基因测序设备销售商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "设备试剂销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_br_reagent", "company_id": "berry_genomics", "node_id": "gene_sequencing_reagent", "activity_type": "manufacture", "role": "基因测序试剂销售商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "贝瑞基因 主营业务", "quote": "设备试剂销售"}], "status": "ACTIVE"},

    # ST京蓝
    {"exposure_id": "exp_jl_smart_eco", "company_id": "st_jinglan", "node_id": "smart_ecological_operation", "activity_type": "operate", "role": "智慧生态运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "ST京蓝 主营业务", "quote": "智慧生态运营服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_jl_clean_energy", "company_id": "st_jinglan", "node_id": "clean_energy_service", "activity_type": "operate", "role": "清洁能源综合服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST京蓝 主营业务", "quote": "清洁能源综合服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_jl_solid_waste", "company_id": "st_jinglan", "node_id": "solid_waste_treatment", "activity_type": "operate", "role": "固废治理运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "ST京蓝 经营范围", "quote": "固体废物治理"}], "status": "ACTIVE"}
]

# ---------------------------------------------------------------------------
# 5. SUBMIT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph_batch = {
        "batch_id": "batch_023_graph",
        "task_description": "Batch 023: Industrial nodes and edges for 10 companies (000700-000711). Focus on automotive trim, feed-meat chain, polyester fiber, special steel, steel sections, genetic testing, and smart ecology.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }

    business_batch = {
        "batch_id": "batch_023_business",
        "task_description": "Batch 023: Company registrations and node exposures for 10 companies (000700-000711).",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures
    }

    print("Submitting graph batch...")
    status, resp = submit_graph_batch(graph_batch)
    print(f"Graph batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    print("\nSubmitting business batch...")
    status, resp = submit_business_batch(business_batch)
    print(f"Business batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))
