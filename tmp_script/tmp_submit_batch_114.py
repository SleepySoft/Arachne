#!/usr/bin/env python3
"""Batch 114 Submission Script"""
import httpx, json
BASE_URL = "http://localhost:8005/api/v1"
def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()
def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

graph_batch = {
    "batch_id": "batch_114_nodes",
    "task_description": "Batch 114:补充医药、诊断、航空维修、零售、连接器、智能制造、广告媒体等缺失节点",
    "nodes_to_upsert": [
        {"node_id": "anti_infective_drug", "canonical_name_zh": "抗感染药物", "canonical_name_en": "anti-infective drug", "aliases": ["抗生素", "抗菌药"], "definition": "用于治疗细菌、病毒、真菌、寄生虫等病原体感染的药物，包括抗生素、抗病毒药、抗真菌药和抗寄生虫药等，是临床应用最广泛的药物类别之一。", "entity_type": "material", "evidence": [{"source_title": "京新药业主营业务", "quote": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "cardiovascular_drug", "canonical_name_zh": "心脑血管药物", "canonical_name_en": "cardiovascular drug", "aliases": ["心血管药"], "definition": "用于预防、治疗心脑血管疾病（如高血压、冠心病、心绞痛、心肌梗死、心力衰竭、脑卒中等）的药物，包括降压药、降脂药、抗心律失常药、抗凝药、血管扩张药等。", "entity_type": "material", "evidence": [{"source_title": "京新药业主营业务", "quote": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "embroidery_machine", "canonical_name_zh": "绣花机", "canonical_name_en": "embroidery machine", "aliases": ["刺绣机"], "definition": "用于在织物、皮革等材料上进行自动化刺绣图案的机电一体化设备，通过计算机控制针迹运动和换色，可绣制复杂的花纹、文字和LOGO。", "entity_type": "device", "evidence": [{"source_title": "中捷资源主营业务", "quote": "中捷股份主要产品为平缝,曲折缝,包缝,绷缝,特种机,绣花机等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "in_vitro_diagnostic_reagent", "canonical_name_zh": "体外诊断试剂", "canonical_name_en": "in vitro diagnostic reagent", "aliases": ["IVD试剂", "诊断试剂"], "definition": "在体外通过对人体样本（血液、尿液、组织等）进行检测，用于疾病诊断、治疗监测和健康评估的生物化学试剂和试剂盒，是现代医学检验的核心材料。", "entity_type": "material", "evidence": [{"source_title": "科华生物主营业务", "quote": "主要产品:体外临床诊断试剂,医疗仪器"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "medical_instrument", "canonical_name_zh": "医疗仪器", "canonical_name_en": "medical instrument", "aliases": ["医疗器械", "医疗设备"], "definition": "单独或组合使用于人体的仪器、设备、器具、材料或其他物品，用于疾病的诊断、预防、监护、治疗或缓解，以及人体结构或生理过程的检验、替代、调节或支持。", "entity_type": "device", "evidence": [{"source_title": "科华生物主营业务", "quote": "主要产品:体外临床诊断试剂,医疗仪器"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "aircraft_maintenance", "canonical_name_zh": "航空维修", "canonical_name_en": "aircraft maintenance", "aliases": ["飞机维修", "航空机务"], "definition": "对航空器及其部件进行检查、修理、翻修、改装和更换，以保持或恢复其适航状态的专业技术服务，包括航线维护、定期检修、部件修理和发动机大修等。", "entity_type": "service", "evidence": [{"source_title": "海特高新主营业务", "quote": "主要业务:航空维修,检测"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "aviation_testing", "canonical_name_zh": "航空检测", "canonical_name_en": "aviation testing", "aliases": ["航空测试"], "definition": "对航空器及其系统、部件、材料进行的各种性能测试、环境试验、可靠性验证和适航审定试验，确保其满足设计要求和适航标准。", "entity_type": "service", "evidence": [{"source_title": "海特高新主营业务", "quote": "主要业务:航空维修,检测"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "home_appliance_retail", "canonical_name_zh": "家电零售", "canonical_name_en": "home appliance retail", "aliases": ["家用电器销售"], "definition": "通过实体门店、电子商务平台等渠道向消费者销售家用电器产品的零售业务，包括大家电（冰箱、洗衣机、空调、电视等）和小家电（厨房电器、个人护理电器等）。", "entity_type": "service", "evidence": [{"source_title": "ST易购主营业务", "quote": "主要业务:综合电器的连锁销售和服务.主要产品:空调器,通讯,数码,IT,黑色电器,白色电器,安装维修"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "electronics_retail", "canonical_name_zh": "电子产品零售", "canonical_name_en": "electronics retail", "aliases": ["数码零售", "3C零售"], "definition": "通过线上线下渠道向消费者销售电子产品和数码设备的零售业务，包括手机、电脑、平板、相机、智能穿戴设备等消费电子产品。", "entity_type": "service", "evidence": [{"source_title": "ST易购主营业务", "quote": "主要业务:综合电器的连锁销售和服务.主要产品:空调器,通讯,数码,IT,黑色电器,白色电器,安装维修"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "connector", "canonical_name_zh": "连接器", "canonical_name_en": "connector", "aliases": ["接插件", "电连接器"], "definition": "用于实现电路或信号连接的电子元器件，通过机械结构实现电气通路的接通或断开，广泛应用于通信、汽车、消费电子、航空航天、军工等领域。", "entity_type": "component", "evidence": [{"source_title": "航天电器主营业务", "quote": "主要产品:继电器,连接器,手机电池"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "mobile_phone_battery", "canonical_name_zh": "手机电池", "canonical_name_en": "mobile phone battery", "aliases": ["手机锂电池"], "definition": "专门为移动电话提供电能的便携式可充电电池，目前主流为锂离子电池，具有能量密度高、体积小、重量轻、无记忆效应等特点。", "entity_type": "component", "evidence": [{"source_title": "航天电器主营业务", "quote": "主要产品:继电器,连接器,手机电池"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "drill_chuck", "canonical_name_zh": "钻夹头", "canonical_name_en": "drill chuck", "aliases": ["钻床夹头"], "definition": "安装在钻床、电钻等旋转工具主轴上，用于夹持钻头、丝锥、铰刀等刀具的夹紧装置，通过手动或扳手旋转实现刀具的夹紧和松开。", "entity_type": "component", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件,精密铸造制品,锯片,机床及附件,智能制造系统集成及智能装备的研发,生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "power_tool_switch", "canonical_name_zh": "电动工具开关", "canonical_name_en": "power tool switch", "aliases": ["工具开关"], "definition": "用于控制电动工具（如电钻、电锯、电磨等）电源通断、速度调节和功能切换的专用开关器件，具有耐冲击、防尘、防水等特性。", "entity_type": "component", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件,精密铸造制品,锯片,机床及附件,智能制造系统集成及智能装备的研发,生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "intelligent_manufacturing", "canonical_name_zh": "智能制造", "canonical_name_en": "intelligent manufacturing", "aliases": ["智能工厂", "数字化制造"], "definition": "基于新一代信息技术与先进制造技术深度融合的新型生产方式，通过物联网、大数据、人工智能等技术实现制造过程的自感知、自决策、自执行和自适应，提升制造效率、质量和柔性。", "entity_type": "service", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件...智能制造系统集成及智能装备的研发,生产和销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "advertising_media", "canonical_name_zh": "广告媒体", "canonical_name_en": "advertising media", "aliases": ["广告媒介"], "definition": "用于传播广告信息的各类媒介载体和平台，包括电视、广播、报纸、杂志、户外广告、互联网媒体、社交媒体、搜索引擎、楼宇电梯媒体等。", "entity_type": "service", "evidence": [{"source_title": "分众传媒主营业务", "quote": "主要产品:自有品牌,代理产品"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "building_media", "canonical_name_zh": "楼宇媒体", "canonical_name_en": "building media", "aliases": ["电梯媒体", "楼宇广告"], "definition": "安装在办公楼、商住楼、住宅楼等建筑物电梯内外或大堂等公共区域的数字化广告播放设备，通过液晶显示屏或海报框架向楼宇内人群传播广告信息。", "entity_type": "service", "evidence": [{"source_title": "分众传媒经营范围", "quote": "软件和信息技术服务业"}], "confidence": "HIGH", "status": "ACTIVE"}
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 114")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

business_batch = {
    "batch_id": "batch_114_business",
    "task_description": "Batch 114:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {"company_id": "sz_002016", "name_zh": "世荣兆业", "aliases": ["广东世荣兆业股份有限公司"], "stock_codes": ["002016.SZ"], "description": "公司及子公司主要产品为商品住宅及商铺", "country": "CN", "province": "广东", "city": "珠海市", "employee_count": 973, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002019", "name_zh": "亿帆医药", "aliases": ["亿帆医药股份有限公司"], "stock_codes": ["002019.SZ"], "description": "主要业务:医药产品,原料药和高分子材料的研发,生产和销售", "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 4098, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002020", "name_zh": "京新药业", "aliases": ["浙江京新药业股份有限公司"], "stock_codes": ["002020.SZ"], "description": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售", "country": "CN", "province": "浙江", "city": "绍兴市", "employee_count": 3869, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002021", "name_zh": "中捷资源", "aliases": ["中捷资源投资股份有限公司"], "stock_codes": ["002021.SZ"], "description": "中捷股份主要产品为平缝,曲折缝,包缝,绷缝,特种机,绣花机等", "country": "CN", "province": "浙江", "city": "台州市", "employee_count": 1178, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002022", "name_zh": "科华生物", "aliases": ["上海科华生物工程股份有限公司"], "stock_codes": ["002022.SZ"], "description": "主要产品:体外临床诊断试剂,医疗仪器", "country": "CN", "province": "上海", "city": "上海市", "employee_count": 2033, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002023", "name_zh": "海特高新", "aliases": ["四川海特高新技术股份有限公司"], "stock_codes": ["002023.SZ"], "description": "主要业务:航空维修,检测", "country": "CN", "province": "四川", "city": "成都市", "employee_count": 1442, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002024", "name_zh": "ST易购", "aliases": ["苏宁易购集团股份有限公司"], "stock_codes": ["002024.SZ"], "description": "主要业务:综合电器的连锁销售和服务.主要产品:空调器,通讯,数码,IT,黑色电器,白色电器,安装维修", "country": "CN", "province": "江苏", "city": "南京市", "employee_count": 21192, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002025", "name_zh": "航天电器", "aliases": ["贵州航天电器股份有限公司"], "stock_codes": ["002025.SZ"], "description": "主要产品:继电器,连接器,手机电池", "country": "CN", "province": "贵州", "city": "贵阳市", "employee_count": 5805, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002026", "name_zh": "山东威达", "aliases": ["山东威达机械股份有限公司"], "stock_codes": ["002026.SZ"], "description": "主要业务:钻夹头,电动工具开关,粉末冶金件,精密铸造制品,锯片,机床及附件,智能制造系统集成及智能装备的研发,生产和销售", "country": "CN", "province": "山东", "city": "威海市", "employee_count": 3502, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002027", "name_zh": "分众传媒", "aliases": ["分众传媒信息技术股份有限公司"], "stock_codes": ["002027.SZ"], "description": "主要产品:自有品牌,代理产品", "country": "CN", "province": "上海", "city": "上海市", "employee_count": 5042, "company_type": "public", "status": "ACTIVE"}
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sz_002016_operate_real_estate_development", "company_id": "sz_002016", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "世荣兆业主营业务", "quote": "公司及子公司主要产品为商品住宅及商铺"}]},
        {"exposure_id": "sz_002019_produce_pharmaceutical_manufacturing", "company_id": "sz_002019", "node_id": "pharmaceutical_manufacturing", "activity_type": "produce", "role": "医药产品生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "亿帆医药主营业务", "quote": "主要业务:医药产品,原料药和高分子材料的研发,生产和销售"}]},
        {"exposure_id": "sz_002019_produce_active_pharmaceutical_ingredient", "company_id": "sz_002019", "node_id": "active_pharmaceutical_ingredient", "activity_type": "produce", "role": "原料药生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "亿帆医药主营业务", "quote": "主要业务:医药产品,原料药和高分子材料的研发,生产和销售"}]},
        {"exposure_id": "sz_002019_produce_polymer_material", "company_id": "sz_002019", "node_id": "polymer_material", "activity_type": "produce", "role": "高分子材料生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "亿帆医药主营业务", "quote": "主要业务:医药产品,原料药和高分子材料的研发,生产和销售"}]},
        {"exposure_id": "sz_002020_produce_anti_infective_drug", "company_id": "sz_002020", "node_id": "anti_infective_drug", "activity_type": "produce", "role": "抗感染药物生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "京新药业主营业务", "quote": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售"}]},
        {"exposure_id": "sz_002020_produce_cardiovascular_drug", "company_id": "sz_002020", "node_id": "cardiovascular_drug", "activity_type": "produce", "role": "心脑血管药物生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "京新药业主营业务", "quote": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售"}]},
        {"exposure_id": "sz_002020_produce_chinese_patent_medicine", "company_id": "sz_002020", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "京新药业主营业务", "quote": "主营业务:抗感染药物(喹诺酮类,头孢菌素类),心脑血管类药物,特色中药等产品的研发,生产和销售"}]},
        {"exposure_id": "sz_002021_produce_industrial_sewing_machine", "company_id": "sz_002021", "node_id": "industrial_sewing_machine", "activity_type": "produce", "role": "工业缝纫机生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "中捷资源主营业务", "quote": "中捷股份主要产品为平缝,曲折缝,包缝,绷缝,特种机,绣花机等"}]},
        {"exposure_id": "sz_002021_produce_embroidery_machine", "company_id": "sz_002021", "node_id": "embroidery_machine", "activity_type": "produce", "role": "绣花机生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "中捷资源主营业务", "quote": "中捷股份主要产品为平缝,曲折缝,包缝,绷缝,特种机,绣花机等"}]},
        {"exposure_id": "sz_002022_produce_in_vitro_diagnostic_reagent", "company_id": "sz_002022", "node_id": "in_vitro_diagnostic_reagent", "activity_type": "produce", "role": "体外诊断试剂生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "科华生物主营业务", "quote": "主要产品:体外临床诊断试剂,医疗仪器"}]},
        {"exposure_id": "sz_002022_produce_medical_instrument", "company_id": "sz_002022", "node_id": "medical_instrument", "activity_type": "produce", "role": "医疗仪器生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "科华生物主营业务", "quote": "主要产品:体外临床诊断试剂,医疗仪器"}]},
        {"exposure_id": "sz_002023_provide_aircraft_maintenance", "company_id": "sz_002023", "node_id": "aircraft_maintenance", "activity_type": "provide_service", "role": "航空维修服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "海特高新主营业务", "quote": "主要业务:航空维修,检测"}]},
        {"exposure_id": "sz_002023_provide_aviation_testing", "company_id": "sz_002023", "node_id": "aviation_testing", "activity_type": "provide_service", "role": "航空检测服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "海特高新主营业务", "quote": "主要业务:航空维修,检测"}]},
        {"exposure_id": "sz_002024_provide_home_appliance_retail", "company_id": "sz_002024", "node_id": "home_appliance_retail", "activity_type": "provide_service", "role": "家电零售服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "ST易购主营业务", "quote": "主要业务:综合电器的连锁销售和服务.主要产品:空调器,通讯,数码,IT,黑色电器,白色电器,安装维修"}]},
        {"exposure_id": "sz_002024_provide_electronics_retail", "company_id": "sz_002024", "node_id": "electronics_retail", "activity_type": "provide_service", "role": "电子产品零售服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "ST易购主营业务", "quote": "主要业务:综合电器的连锁销售和服务.主要产品:空调器,通讯,数码,IT,黑色电器,白色电器,安装维修"}]},
        {"exposure_id": "sz_002024_provide_logistics_service", "company_id": "sz_002024", "node_id": "logistics_service", "activity_type": "provide_service", "role": "物流服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST易购经营范围", "quote": "仓储,装卸搬运,普通货运"}]},
        {"exposure_id": "sz_002025_produce_relay", "company_id": "sz_002025", "node_id": "relay", "activity_type": "produce", "role": "继电器生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "航天电器主营业务", "quote": "主要产品:继电器,连接器,手机电池"}]},
        {"exposure_id": "sz_002025_produce_connector", "company_id": "sz_002025", "node_id": "connector", "activity_type": "produce", "role": "连接器生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "航天电器主营业务", "quote": "主要产品:继电器,连接器,手机电池"}]},
        {"exposure_id": "sz_002025_produce_mobile_phone_battery", "company_id": "sz_002025", "node_id": "mobile_phone_battery", "activity_type": "produce", "role": "手机电池生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "航天电器主营业务", "quote": "主要产品:继电器,连接器,手机电池"}]},
        {"exposure_id": "sz_002026_produce_drill_chuck", "company_id": "sz_002026", "node_id": "drill_chuck", "activity_type": "produce", "role": "钻夹头生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件...的研发,生产和销售"}]},
        {"exposure_id": "sz_002026_produce_power_tool_switch", "company_id": "sz_002026", "node_id": "power_tool_switch", "activity_type": "produce", "role": "电动工具开关生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件...的研发,生产和销售"}]},
        {"exposure_id": "sz_002026_produce_powder_metallurgy_part", "company_id": "sz_002026", "node_id": "powder_metallurgy_part", "activity_type": "produce", "role": "粉末冶金件生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头,电动工具开关,粉末冶金件...的研发,生产和销售"}]},
        {"exposure_id": "sz_002026_provide_intelligent_manufacturing", "company_id": "sz_002026", "node_id": "intelligent_manufacturing", "activity_type": "provide_service", "role": "智能制造系统服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "山东威达主营业务", "quote": "主要业务:钻夹头...智能制造系统集成及智能装备的研发,生产和销售"}]},
        {"exposure_id": "sz_002027_provide_advertising_media", "company_id": "sz_002027", "node_id": "advertising_media", "activity_type": "provide_service", "role": "广告媒体运营商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "分众传媒主营业务", "quote": "主要产品:自有品牌,代理产品"}]},
        {"exposure_id": "sz_002027_provide_building_media", "company_id": "sz_002027", "node_id": "building_media", "activity_type": "provide_service", "role": "楼宇媒体运营商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "分众传媒经营范围", "quote": "软件和信息技术服务业"}]}
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 114")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))
print("\nBatch 114 submission completed.")
