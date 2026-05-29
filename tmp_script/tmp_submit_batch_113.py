#!/usr/bin/env python3
"""Batch 113 Submission Script"""
import httpx, json
BASE_URL = "http://localhost:8005/api/v1"
def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()
def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

graph_batch = {
    "batch_id": "batch_113_nodes",
    "task_description": "Batch 113:补充建材机械、碳纤维设备、血液制品、激光设备、自动化输送、智能物流、中央空调、电容器纸、包装材料、清洁能源等缺失节点",
    "nodes_to_upsert": [
        {"node_id": "building_material_machinery", "canonical_name_zh": "建材机械", "canonical_name_en": "building material machinery", "aliases": ["建材设备"], "definition": "用于建筑材料生产和加工的专用机械设备，包括水泥生产线设备、玻璃生产线设备、陶瓷机械、砖瓦机械、石材加工设备等。", "entity_type": "device", "evidence": [{"source_title": "精工科技主营业务", "quote": "主要产品:建材机械,纺织机械,工程机械"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "carbon_fiber_equipment", "canonical_name_zh": "碳纤维设备", "canonical_name_en": "carbon fiber equipment", "aliases": ["碳纤维生产设备"], "definition": "用于碳纤维及其复合材料生产的专用设备，包括碳纤维原丝生产线、碳化炉、预氧化炉、复合材料成型设备、拉挤设备等。", "entity_type": "device", "evidence": [{"source_title": "精工科技经营范围", "quote": "高性能纤维及复合材料制造;高性能纤维及复合材料销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "human_serum_albumin", "canonical_name_zh": "人血白蛋白", "canonical_name_en": "human serum albumin", "aliases": ["白蛋白"], "definition": "从健康人血浆中提取的一种血浆蛋白，具有维持血浆胶体渗透压、运输营养物质和药物、抗氧化等重要生理功能，临床广泛用于休克、烧伤、肝硬化腹水、低蛋白血症等治疗。", "entity_type": "material", "evidence": [{"source_title": "华兰生物主营业务", "quote": "主要产品:人血白蛋白,静注丙球"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "intravenous_immunoglobulin", "canonical_name_zh": "静注人免疫球蛋白", "canonical_name_en": "intravenous immunoglobulin", "aliases": ["静注丙球", "IVIG"], "definition": "从大量健康人混合血浆中提取的含有广谱抗体的血液制品，通过静脉注射给药，具有增强免疫力、中和病原体和调节免疫功能的作用，用于治疗原发性免疫缺陷病、自身免疫性疾病等。", "entity_type": "material", "evidence": [{"source_title": "华兰生物主营业务", "quote": "主要产品:人血白蛋白,静注丙球"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "laser_marking_machine", "canonical_name_zh": "激光打标机", "canonical_name_en": "laser marking machine", "aliases": ["激光标记设备"], "definition": "利用高能量密度激光束在各种材料表面进行永久性标记的设备，通过烧蚀、气化或变色等方式在产品表面形成文字、图案、条形码、二维码等标识信息。", "entity_type": "device", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "laser_welding_machine", "canonical_name_zh": "激光焊接机", "canonical_name_en": "laser welding machine", "aliases": ["激光焊机"], "definition": "利用高能量密度激光束作为热源进行材料焊接的加工设备，具有焊缝窄、热影响区小、焊接速度快、变形小、精度高等优点，广泛应用于精密制造领域。", "entity_type": "device", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "cnc_machine", "canonical_name_zh": "数控机床", "canonical_name_en": "CNC machine", "aliases": ["数控设备", "数控加工中心"], "definition": "采用计算机数字控制技术对机床运动和加工过程进行自动控制的机床设备，具有加工精度高、生产效率高、加工质量稳定、适应性强等特点。", "entity_type": "device", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "automated_conveying_system", "canonical_name_zh": "自动化输送系统", "canonical_name_en": "automated conveying system", "aliases": ["自动输送线", "物流输送系统"], "definition": "利用输送带、滚筒、链条、AGV等输送设备，配合自动控制和信息系统，实现物料或产品在工厂、仓库等场所自动搬运和流转的集成系统。", "entity_type": "system", "evidence": [{"source_title": "天奇股份主营业务", "quote": "自动化输送,仓储系统工程"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "warehousing_system", "canonical_name_zh": "仓储系统", "canonical_name_en": "warehousing system", "aliases": ["自动化仓储系统", "智能仓库"], "definition": "由货架、堆垛机、输送设备、分拣系统和仓库管理软件组成的集成化物料存储和 retrieval 系统，可实现货物的自动化存取、管理和配送。", "entity_type": "system", "evidence": [{"source_title": "天奇股份主营业务", "quote": "自动化输送,仓储系统工程"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "intelligent_logistics", "canonical_name_zh": "智能物流", "canonical_name_en": "intelligent logistics", "aliases": ["智慧物流"], "definition": "利用物联网、大数据、人工智能等技术，实现物流全过程的智能化感知、分析、决策和执行的现代物流服务模式，包括智能仓储、智能运输、智能配送和智能供应链管理等。", "entity_type": "service", "evidence": [{"source_title": "传化智联主营业务", "quote": "主要业务:传化网智能物流和化工业务"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "central_air_conditioner", "canonical_name_zh": "中央空调", "canonical_name_en": "central air conditioner", "aliases": ["集中式空调"], "definition": "通过一套集中的冷热源和空气处理设备，为整栋建筑或多个房间提供温度、湿度、空气洁净度和气流速度调节的大型空调系统，广泛应用于商业建筑、办公楼、酒店、医院等场所。", "entity_type": "system", "evidence": [{"source_title": "盾安环境主营业务", "quote": "主要产品:中央空调主机,末端,换热器"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "electrolytic_capacitor_paper", "canonical_name_zh": "电解电容器纸", "canonical_name_en": "electrolytic capacitor paper", "aliases": [ "电容器纸", "电解纸" ], "definition": "专用于铝电解电容器制造的特种纸张，具有高纯度、高孔隙率、低杂质含量的特点，作为隔离层置于阳极箔和阴极箔之间，吸附电解液并提供电化学反应介质。", "entity_type": "material", "evidence": [{"source_title": "凯恩股份主营业务", "quote": "主要产品:电解电容器纸,双面胶带原纸,滤纸原纸"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "filter_paper", "canonical_name_zh": "滤纸", "canonical_name_en": "filter paper", "aliases": ["过滤纸"], "definition": "具有特定孔径结构和过滤性能的特种纸张，用于液体或气体的过滤分离，广泛应用于实验室分析、工业过滤、汽车滤清器、咖啡过滤等领域。", "entity_type": "material", "evidence": [{"source_title": "凯恩股份主营业务", "quote": "主要产品:电解电容器纸,双面胶带原纸,滤纸原纸"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "color_printing_packaging", "canonical_name_zh": "彩印包装", "canonical_name_en": "color printing packaging", "aliases": ["彩色印刷包装"], "definition": "采用彩色印刷工艺在包装材料（如纸张、塑料薄膜、复合材料等）上印制图案、文字和商标后制成的包装产品，具有美观、醒目、提升商品附加值的特点。", "entity_type": "material", "evidence": [{"source_title": "永新股份主营业务", "quote": "彩印包装材料,镀铝包装材料,塑料软包装薄膜"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "aluminized_packaging", "canonical_name_zh": "镀铝包装", "canonical_name_en": "aluminized packaging", "aliases": ["镀铝膜包装", "VMCPP包装"], "definition": "在塑料薄膜或纸张表面通过真空镀铝工艺沉积一层极薄的铝层制成的包装材料，具有优良的阻隔性、遮光性和金属光泽，广泛用于食品、药品和化妆品包装。", "entity_type": "material", "evidence": [{"source_title": "永新股份主营业务", "quote": "彩印包装材料,镀铝包装材料,塑料软包装薄膜"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "clean_energy", "canonical_name_zh": "清洁能源", "canonical_name_en": "clean energy", "aliases": ["绿色能源", "可再生能源"], "definition": "在生产和使用过程中对环境污染较小或零排放的能源形式，包括太阳能、风能、水能、生物质能、地热能、海洋能以及核能等，是替代化石能源、应对气候变化的重要方向。", "entity_type": "service", "evidence": [{"source_title": "协鑫能科主营业务", "quote": "清洁能源项目的开发,投资和运营管理,以及相关领域的综合能源服务"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "integrated_energy_service", "canonical_name_zh": "综合能源服务", "canonical_name_en": "integrated energy service", "aliases": ["综合能源管理"], "definition": "面向用户侧提供电、热、冷、气等多种能源的一体化规划、设计、投资、建设和运营服务，通过多能互补和能源梯级利用，提高能源利用效率、降低用能成本。", "entity_type": "service", "evidence": [{"source_title": "协鑫能科主营业务", "quote": "清洁能源项目的开发,投资和运营管理,以及相关领域的综合能源服务"}], "confidence": "HIGH", "status": "ACTIVE"}
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 113")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

business_batch = {
    "batch_id": "batch_113_business",
    "task_description": "Batch 113:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {"company_id": "sz_002005", "name_zh": "ST德豪", "aliases": ["安徽德豪润达电气股份有限公司"], "stock_codes": ["002005.SZ"], "description": "主要产品:厨房电器产品,居家及个人护理产品", "country": "CN", "province": "安徽", "city": "蚌埠市", "employee_count": 1527, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002006", "name_zh": "精工科技", "aliases": ["浙江精工集成科技股份有限公司"], "stock_codes": ["002006.SZ"], "description": "主要产品:建材机械,纺织机械,工程机械", "country": "CN", "province": "浙江", "city": "绍兴市", "employee_count": 1537, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002007", "name_zh": "华兰生物", "aliases": ["华兰生物工程股份有限公司"], "stock_codes": ["002007.SZ"], "description": "主要产品:人血白蛋白,静注丙球", "country": "CN", "province": "河南", "city": "新乡市", "employee_count": 4117, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002008", "name_zh": "大族激光", "aliases": ["大族激光科技产业集团股份有限公司"], "stock_codes": ["002008.SZ"], "description": "主要产品:激光信息标记设备,激光焊接机,数控设备", "country": "CN", "province": "广东", "city": "深圳市", "employee_count": 16866, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002009", "name_zh": "天奇股份", "aliases": ["天奇自动化工程股份有限公司"], "stock_codes": ["002009.SZ"], "description": "自动化输送,仓储系统工程", "country": "CN", "province": "江苏", "city": "无锡市", "employee_count": 2463, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002010", "name_zh": "传化智联", "aliases": ["传化智联股份有限公司"], "stock_codes": ["002010.SZ"], "description": "主要业务:传化网智能物流和化工业务", "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 4700, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002011", "name_zh": "盾安环境", "aliases": ["浙江盾安人工环境股份有限公司"], "stock_codes": ["002011.SZ"], "description": "主要产品:中央空调主机,末端,换热器", "country": "CN", "province": "浙江", "city": "绍兴市", "employee_count": 13921, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002012", "name_zh": "凯恩股份", "aliases": ["浙江凯恩特种材料股份有限公司"], "stock_codes": ["002012.SZ"], "description": "主要产品:电解电容器纸,双面胶带原纸,滤纸原纸", "country": "CN", "province": "浙江", "city": "丽水市", "employee_count": 281, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002014", "name_zh": "永新股份", "aliases": ["黄山永新股份有限公司"], "stock_codes": ["002014.SZ"], "description": "彩印包装材料,镀铝包装材料,塑料软包装薄膜", "country": "CN", "province": "安徽", "city": "黄山市", "employee_count": 2366, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002015", "name_zh": "协鑫能科", "aliases": ["协鑫能源科技股份有限公司"], "stock_codes": ["002015.SZ"], "description": "清洁能源项目的开发,投资和运营管理,以及相关领域的综合能源服务", "country": "CN", "province": "江苏", "city": "无锡市", "employee_count": 3408, "company_type": "public", "status": "ACTIVE"}
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sz_002005_produce_kitchen_appliance", "company_id": "sz_002005", "node_id": "kitchen_appliance", "activity_type": "produce", "role": "厨房电器生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "ST德豪主营业务", "quote": "主要产品:厨房电器产品,居家及个人护理产品"}]},
        {"exposure_id": "sz_002005_produce_led_lighting", "company_id": "sz_002005", "node_id": "led_lighting", "activity_type": "produce", "role": "LED照明产品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "ST德豪经营范围", "quote": "发光二极管,发射接收管,数码管,半导体LED照明,半导体LED装饰灯,太阳能LED照明,LED显示屏系列"}]},
        {"exposure_id": "sz_002006_produce_building_material_machinery", "company_id": "sz_002006", "node_id": "building_material_machinery", "activity_type": "produce", "role": "建材机械生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "精工科技主营业务", "quote": "主要产品:建材机械,纺织机械,工程机械"}]},
        {"exposure_id": "sz_002006_produce_textile_machinery", "company_id": "sz_002006", "node_id": "textile_machinery", "activity_type": "produce", "role": "纺织机械生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "精工科技主营业务", "quote": "主要产品:建材机械,纺织机械,工程机械"}]},
        {"exposure_id": "sz_002006_produce_construction_machinery", "company_id": "sz_002006", "node_id": "construction_machinery", "activity_type": "produce", "role": "工程机械生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "精工科技主营业务", "quote": "主要产品:建材机械,纺织机械,工程机械"}]},
        {"exposure_id": "sz_002006_produce_carbon_fiber_equipment", "company_id": "sz_002006", "node_id": "carbon_fiber_equipment", "activity_type": "produce", "role": "碳纤维设备生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "精工科技经营范围", "quote": "高性能纤维及复合材料制造;高性能纤维及复合材料销售"}]},
        {"exposure_id": "sz_002007_produce_human_serum_albumin", "company_id": "sz_002007", "node_id": "human_serum_albumin", "activity_type": "produce", "role": "人血白蛋白生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "华兰生物主营业务", "quote": "主要产品:人血白蛋白,静注丙球"}]},
        {"exposure_id": "sz_002007_produce_intravenous_immunoglobulin", "company_id": "sz_002007", "node_id": "intravenous_immunoglobulin", "activity_type": "produce", "role": "静注人免疫球蛋白生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "华兰生物主营业务", "quote": "主要产品:人血白蛋白,静注丙球"}]},
        {"exposure_id": "sz_002007_produce_blood_product", "company_id": "sz_002007", "node_id": "blood_product", "activity_type": "produce", "role": "血液制品生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "华兰生物主营业务", "quote": "主要产品:人血白蛋白,静注丙球"}]},
        {"exposure_id": "sz_002008_produce_laser_marking_machine", "company_id": "sz_002008", "node_id": "laser_marking_machine", "activity_type": "produce", "role": "激光打标机生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}]},
        {"exposure_id": "sz_002008_produce_laser_welding_machine", "company_id": "sz_002008", "node_id": "laser_welding_machine", "activity_type": "produce", "role": "激光焊接机生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}]},
        {"exposure_id": "sz_002008_produce_cnc_machine", "company_id": "sz_002008", "node_id": "cnc_machine", "activity_type": "produce", "role": "数控机床生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "大族激光主营业务", "quote": "主要产品:激光信息标记设备,激光焊接机,数控设备"}]},
        {"exposure_id": "sz_002009_provide_automated_conveying_system", "company_id": "sz_002009", "node_id": "automated_conveying_system", "activity_type": "provide_service", "role": "自动化输送系统服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "天奇股份主营业务", "quote": "自动化输送,仓储系统工程"}]},
        {"exposure_id": "sz_002009_provide_warehousing_system", "company_id": "sz_002009", "node_id": "warehousing_system", "activity_type": "provide_service", "role": "仓储系统服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "天奇股份主营业务", "quote": "自动化输送,仓储系统工程"}]},
        {"exposure_id": "sz_002009_operate_wind_power_generation", "company_id": "sz_002009", "node_id": "wind_power_generation", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.5, "confidence": "MEDIUM", "evidence": [{"source_title": "天奇股份经营范围", "quote": "风力发电机组,零部件的开发,设计,制造及售后服务"}]},
        {"exposure_id": "sz_002010_provide_intelligent_logistics", "company_id": "sz_002010", "node_id": "intelligent_logistics", "activity_type": "provide_service", "role": "智能物流服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "传化智联主营业务", "quote": "主要业务:传化网智能物流和化工业务"}]},
        {"exposure_id": "sz_002010_produce_chemical_product", "company_id": "sz_002010", "node_id": "chemical_product", "activity_type": "produce", "role": "化工产品生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "传化智联主营业务", "quote": "主要业务:传化网智能物流和化工业务"}]},
        {"exposure_id": "sz_002011_produce_central_air_conditioner", "company_id": "sz_002011", "node_id": "central_air_conditioner", "activity_type": "produce", "role": "中央空调生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "盾安环境主营业务", "quote": "主要产品:中央空调主机,末端,换热器"}]},
        {"exposure_id": "sz_002011_produce_heat_exchanger", "company_id": "sz_002011", "node_id": "heat_exchanger", "activity_type": "produce", "role": "换热器生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "盾安环境主营业务", "quote": "主要产品:中央空调主机,末端,换热器"}]},
        {"exposure_id": "sz_002012_produce_electrolytic_capacitor_paper", "company_id": "sz_002012", "node_id": "electrolytic_capacitor_paper", "activity_type": "produce", "role": "电解电容器纸生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "凯恩股份主营业务", "quote": "主要产品:电解电容器纸,双面胶带原纸,滤纸原纸"}]},
        {"exposure_id": "sz_002012_produce_filter_paper", "company_id": "sz_002012", "node_id": "filter_paper", "activity_type": "produce", "role": "滤纸生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "凯恩股份主营业务", "quote": "主要产品:电解电容器纸,双面胶带原纸,滤纸原纸"}]},
        {"exposure_id": "sz_002014_produce_color_printing_packaging", "company_id": "sz_002014", "node_id": "color_printing_packaging", "activity_type": "produce", "role": "彩印包装材料生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "永新股份主营业务", "quote": "彩印包装材料,镀铝包装材料,塑料软包装薄膜"}]},
        {"exposure_id": "sz_002014_produce_aluminized_packaging", "company_id": "sz_002014", "node_id": "aluminized_packaging", "activity_type": "produce", "role": "镀铝包装材料生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "永新股份主营业务", "quote": "彩印包装材料,镀铝包装材料,塑料软包装薄膜"}]},
        {"exposure_id": "sz_002014_produce_plastic_film", "company_id": "sz_002014", "node_id": "plastic_film", "activity_type": "produce", "role": "塑料软包装薄膜生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "永新股份主营业务", "quote": "彩印包装材料,镀铝包装材料,塑料软包装薄膜"}]},
        {"exposure_id": "sz_002015_provide_clean_energy", "company_id": "sz_002015", "node_id": "clean_energy", "activity_type": "provide_service", "role": "清洁能源服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "协鑫能科主营业务", "quote": "清洁能源项目的开发,投资和运营管理,以及相关领域的综合能源服务"}]},
        {"exposure_id": "sz_002015_provide_integrated_energy_service", "company_id": "sz_002015", "node_id": "integrated_energy_service", "activity_type": "provide_service", "role": "综合能源服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "协鑫能科主营业务", "quote": "清洁能源项目的开发,投资和运营管理,以及相关领域的综合能源服务"}]}
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 113")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))
print("\nBatch 113 submission completed.")
