#!/usr/bin/env python3
"""Batch 111 Submission Script"""
import httpx, json
BASE_URL = "http://localhost:8005/api/v1"
def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()
def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

graph_batch = {
    "batch_id": "batch_111_nodes",
    "task_description": "Batch 111:补充汽车配件、造纸、军工、能源、养殖、磁性材料等缺失节点",
    "nodes_to_upsert": [
        {"node_id": "piston", "canonical_name_zh": "活塞", "canonical_name_en": "piston", "aliases": ["发动机活塞"], "definition": "在发动机气缸内做往复运动的圆柱形零件，通过连杆将燃烧产生的气体压力传递给曲轴，实现热能到机械能的转换。", "entity_type": "component", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件,专用数控机床,轻量化汽车零部件,汽车轮毂,汽车空调,减震器,排气系统,油箱,启停电池"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "wheel_hub", "canonical_name_zh": "轮毂", "canonical_name_en": "wheel hub", "aliases": ["汽车轮毂", "轮圈"], "definition": "汽车车轮中心安装车轴的部件，连接制动鼓盘、轮盘和半轴，承受汽车行驶时产生的各种力和力矩。", "entity_type": "component", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...汽车轮毂..."}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "automotive_air_conditioner", "canonical_name_zh": "汽车空调", "canonical_name_en": "automotive air conditioner", "aliases": ["车用空调"], "definition": "安装在汽车内用于调节车厢内温度、湿度、空气清洁度和空气流动的制冷制热系统，为驾驶员和乘客提供舒适的车内环境。", "entity_type": "component", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...汽车空调..."}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "shock_absorber", "canonical_name_zh": "减震器", "canonical_name_en": "shock absorber", "aliases": ["避震器", "阻尼器"], "definition": "汽车悬架系统中用于抑制弹簧吸震后反弹时的振荡及来自路面的冲击，加速车架与车身振动的衰减，以改善汽车行驶平顺性的装置。", "entity_type": "component", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...减震器,排气系统..."}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "coated_paper", "canonical_name_zh": "涂布纸", "canonical_name_en": "coated paper", "aliases": ["轻涂纸", "铜版纸"], "definition": "在原纸表面涂覆一层或多层涂料（如瓷土、碳酸钙、胶乳等）后经干燥和压光处理制成的纸张，具有表面光滑、白度高、印刷适性好的特点，主要用于高档印刷品。", "entity_type": "material", "evidence": [{"source_title": "岳阳林纸主营业务", "quote": "颜料整饰纸,轻涂纸,淋膜原纸和包装纸"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "white_cardboard", "canonical_name_zh": "白卡纸", "canonical_name_en": "white cardboard", "aliases": ["白纸板"], "definition": "一种定量较高、挺度好、白度高的单面或双面涂布白纸板，主要用于制作高档包装盒、烟盒、药品盒、化妆品盒及手提袋等。", "entity_type": "material", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "writing_paper", "canonical_name_zh": "书写纸", "canonical_name_en": "writing paper", "aliases": ["书写用纸"], "definition": "专供书写和办公用途的纸类产品，具有适当的不透明度、平滑度和吸墨性，包括复印纸、打印纸、信纸、笔记本纸等。", "entity_type": "material", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "offset_paper", "canonical_name_zh": "胶印纸", "canonical_name_en": "offset paper", "aliases": ["胶版印刷纸"], "definition": "适用于胶版印刷机印刷的高级文化用纸，具有优良的不透明度、白度和平滑度，主要用于印刷书刊、杂志、画报、商标等彩色或黑白印刷品。", "entity_type": "material", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "armored_vehicle", "canonical_name_zh": "装甲车辆", "canonical_name_en": "armored vehicle", "aliases": ["坦克", "装甲战车"], "definition": "装有装甲防护、具有越野机动能力和一定火力的履带式或轮式战斗车辆，包括主战坦克、步兵战车、装甲输送车等，是现代地面作战的主力装备。", "entity_type": "system", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "坦克装甲车辆及轮式装甲车辆设计,研发,制造,销售及售后服务"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "railway_vehicle", "canonical_name_zh": "铁路车辆", "canonical_name_en": "railway vehicle", "aliases": ["铁道车辆", "火车车厢"], "definition": "在铁路轨道上运行、用于运送旅客或货物的车辆，包括客车、货车、动车组车辆、地铁车辆、轻轨车辆等。", "entity_type": "system", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "铁路车辆,专用汽车,冶金机械"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "metallurgical_machinery", "canonical_name_zh": "冶金机械", "canonical_name_en": "metallurgical machinery", "aliases": ["冶金设备"], "definition": "用于黑色金属和有色金属冶炼、轧制、铸造等生产过程的专用机械设备，包括高炉、转炉、连铸机、轧机、冶炼炉等。", "entity_type": "device", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "铁路车辆,专用汽车,冶金机械"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "industrial_gas", "canonical_name_zh": "工业气体", "canonical_name_en": "industrial gas", "aliases": ["工业用气"], "definition": "用于工业生产过程中的各种气体产品，包括氧气、氮气、氩气、氢气、二氧化碳、乙炔、液化天然气等，广泛应用于冶金、化工、电子、医疗、食品等领域。", "entity_type": "material", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电,水力发电投资业务等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "waste_heat_power_generation", "canonical_name_zh": "余热发电", "canonical_name_en": "waste heat power generation", "aliases": ["余热利用发电"], "definition": "利用工业生产过程中排出的高温废气、废水或废渣中的余热，通过余热锅炉产生蒸汽驱动汽轮发电机组发电的节能技术，是提高能源利用效率的重要方式。", "entity_type": "service", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电,水力发电投资业务等"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "breeding_pig", "canonical_name_zh": "种猪", "canonical_name_en": "breeding pig", "aliases": ["母猪", "公猪", "繁殖猪"], "definition": "专门用于繁殖后代的猪只，具有优良的遗传性状和繁殖性能，是生猪养殖产业链的源头，其品质直接决定商品肉猪的生长性能和肉质。", "entity_type": "material", "evidence": [{"source_title": "新五丰主营业务", "quote": "活大猪,种猪,饲料"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "pork_product", "canonical_name_zh": "猪肉制品", "canonical_name_en": "pork product", "aliases": ["猪肉产品", "冷鲜肉"], "definition": "以生猪屠宰后的猪肉为原料，经过分割、冷却、冷冻或进一步加工制成的食品产品，包括鲜猪肉、冷却猪肉、冷冻猪肉、肉制品、预制菜等。", "entity_type": "material", "evidence": [{"source_title": "新五丰经营范围", "quote": "鲜猪肉,冷却猪肉,冷冻猪肉销售,配送;预制菜(猪肉产品)的生产及销售"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "ferrite", "canonical_name_zh": "铁氧体", "canonical_name_en": "ferrite", "aliases": ["铁氧体磁芯", "磁性陶瓷"], "definition": "一种以氧化铁为主要成分的复合氧化物磁性材料，具有高电阻率、低涡流损耗的特点，广泛用于制造永磁体、软磁元件、微波器件、磁记录材料等。", "entity_type": "material", "evidence": [{"source_title": "北矿科技主营业务", "quote": "烧结铁氧体,粘结铁氧体,烧结磁器件,粘结磁器件"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "magnetic_device", "canonical_name_zh": "磁性器件", "canonical_name_en": "magnetic device", "aliases": ["磁器件"], "definition": "利用磁性材料磁性能实现特定功能的电子元器件，包括电感器、变压器、磁珠、磁环、磁头等，广泛应用于电源、通信、消费电子、汽车电子等领域。", "entity_type": "component", "evidence": [{"source_title": "北矿科技主营业务", "quote": "烧结铁氧体,粘结铁氧体,烧结磁器件,粘结磁器件"}], "confidence": "HIGH", "status": "ACTIVE"}
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 111")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

business_batch = {
    "batch_id": "batch_111_business",
    "task_description": "Batch 111:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {"company_id": "sh_600900", "name_zh": "长江电力", "aliases": ["中国长江电力股份有限公司"], "stock_codes": ["600900.SH"], "description": "主营业务:电力生产,经营和投资;电力生产技术咨询;水电工程检修维护", "country": "CN", "province": "北京", "city": "北京市", "employee_count": 7937, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600960", "name_zh": "渤海汽车", "aliases": ["渤海汽车系统股份有限公司"], "stock_codes": ["600960.SH"], "description": "活塞及组件,专用数控机床,轻量化汽车零部件,汽车轮毂,汽车空调,减震器,排气系统,油箱,启停电池", "country": "CN", "province": "山东", "city": "滨州市", "employee_count": 4428, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600963", "name_zh": "岳阳林纸", "aliases": ["岳阳林纸股份有限公司"], "stock_codes": ["600963.SH"], "description": "颜料整饰纸,轻涂纸,淋膜原纸和包装纸", "country": "CN", "province": "湖南", "city": "岳阳市", "employee_count": 3937, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600966", "name_zh": "博汇纸业", "aliases": ["山东博汇纸业股份有限公司"], "stock_codes": ["600966.SH"], "description": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等", "country": "CN", "province": "山东", "city": "淄博市", "employee_count": 5884, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600967", "name_zh": "内蒙一机", "aliases": ["内蒙古第一机械集团股份有限公司"], "stock_codes": ["600967.SH"], "description": "铁路车辆,专用汽车,冶金机械.坦克装甲车辆及轮式装甲车辆设计,研发,制造,销售及售后服务", "country": "CN", "province": "内蒙古", "city": "包头市", "employee_count": 6705, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600969", "name_zh": "郴电国际", "aliases": ["湖南郴电国际发展股份有限公司"], "stock_codes": ["600969.SH"], "description": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电,水力发电投资业务等", "country": "CN", "province": "湖南", "city": "郴州市", "employee_count": 2566, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600975", "name_zh": "新五丰", "aliases": ["湖南新五丰股份有限公司"], "stock_codes": ["600975.SH"], "description": "活大猪,种猪,饲料", "country": "CN", "province": "湖南", "city": "长沙市", "employee_count": 5375, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600976", "name_zh": "健民集团", "aliases": ["健民药业集团股份有限公司"], "stock_codes": ["600976.SH"], "description": "龙牡壮骨颗粒,健胃消食片,小儿宣肺止咳颗粒,健民咽喉片", "country": "CN", "province": "湖北", "city": "武汉市", "employee_count": 2257, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600980", "name_zh": "北矿科技", "aliases": ["北矿科技股份有限公司"], "stock_codes": ["600980.SH"], "description": "烧结铁氧体,粘结铁氧体,烧结磁器件,粘结磁器件", "country": "CN", "province": "北京", "city": "北京市", "employee_count": 760, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600985", "name_zh": "淮北矿业", "aliases": ["淮北矿业控股股份有限公司"], "stock_codes": ["600985.SH"], "description": "主营业务为民用爆破器材的生产和销售,煤炭采掘,洗选加工,销售,煤化工产品的生产,销售等业务", "country": "CN", "province": "安徽", "city": "淮北市", "employee_count": 39570, "company_type": "public", "status": "ACTIVE"}
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sh_600900_operate_hydro_power_generation", "company_id": "sh_600900", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水电运营商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "长江电力主营业务", "quote": "主营业务:电力生产,经营和投资;电力生产技术咨询;水电工程检修维护"}]},
        {"exposure_id": "sh_600900_produce_electricity_power", "company_id": "sh_600900", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "长江电力主营业务", "quote": "主营业务:电力生产,经营和投资"}]},
        {"exposure_id": "sh_600960_produce_piston", "company_id": "sh_600960", "node_id": "piston", "activity_type": "produce", "role": "活塞生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件,专用数控机床,轻量化汽车零部件,汽车轮毂,汽车空调,减震器,排气系统,油箱,启停电池"}]},
        {"exposure_id": "sh_600960_produce_auto_parts", "company_id": "sh_600960", "node_id": "auto_parts", "activity_type": "produce", "role": "汽车零部件生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件,专用数控机床,轻量化汽车零部件,汽车轮毂,汽车空调,减震器,排气系统,油箱,启停电池"}]},
        {"exposure_id": "sh_600960_produce_wheel_hub", "company_id": "sh_600960", "node_id": "wheel_hub", "activity_type": "produce", "role": "轮毂生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...汽车轮毂..."}]},
        {"exposure_id": "sh_600960_produce_automotive_air_conditioner", "company_id": "sh_600960", "node_id": "automotive_air_conditioner", "activity_type": "produce", "role": "汽车空调生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...汽车空调..."}]},
        {"exposure_id": "sh_600960_produce_shock_absorber", "company_id": "sh_600960", "node_id": "shock_absorber", "activity_type": "produce", "role": "减震器生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "渤海汽车主营业务", "quote": "活塞及组件...减震器..."}]},
        {"exposure_id": "sh_600963_produce_coated_paper", "company_id": "sh_600963", "node_id": "coated_paper", "activity_type": "produce", "role": "涂布纸生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "岳阳林纸主营业务", "quote": "颜料整饰纸,轻涂纸,淋膜原纸和包装纸"}]},
        {"exposure_id": "sh_600963_produce_packaging_paper", "company_id": "sh_600963", "node_id": "packaging_paper", "activity_type": "produce", "role": "包装纸生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "岳阳林纸主营业务", "quote": "颜料整饰纸,轻涂纸,淋膜原纸和包装纸"}]},
        {"exposure_id": "sh_600966_produce_white_cardboard", "company_id": "sh_600966", "node_id": "white_cardboard", "activity_type": "produce", "role": "白卡纸生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}]},
        {"exposure_id": "sh_600966_produce_writing_paper", "company_id": "sh_600966", "node_id": "writing_paper", "activity_type": "produce", "role": "书写纸生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}]},
        {"exposure_id": "sh_600966_produce_offset_paper", "company_id": "sh_600966", "node_id": "offset_paper", "activity_type": "produce", "role": "胶印纸生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "博汇纸业主营业务", "quote": "主要产品有博汇牌白卡纸,书写纸,胶印纸,高档纸板等"}]},
        {"exposure_id": "sh_600967_produce_armored_vehicle", "company_id": "sh_600967", "node_id": "armored_vehicle", "activity_type": "produce", "role": "装甲车辆生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "坦克装甲车辆及轮式装甲车辆设计,研发,制造,销售及售后服务"}]},
        {"exposure_id": "sh_600967_produce_special_purpose_vehicle", "company_id": "sh_600967", "node_id": "special_purpose_vehicle", "activity_type": "produce", "role": "专用汽车生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "铁路车辆,专用汽车,冶金机械"}]},
        {"exposure_id": "sh_600967_produce_railway_vehicle", "company_id": "sh_600967", "node_id": "railway_vehicle", "activity_type": "produce", "role": "铁路车辆生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "铁路车辆,专用汽车,冶金机械"}]},
        {"exposure_id": "sh_600967_produce_metallurgical_machinery", "company_id": "sh_600967", "node_id": "metallurgical_machinery", "activity_type": "produce", "role": "冶金机械生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "内蒙一机主营业务", "quote": "铁路车辆,专用汽车,冶金机械"}]},
        {"exposure_id": "sh_600969_produce_electricity_power", "company_id": "sh_600969", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电,水力发电投资业务等"}]},
        {"exposure_id": "sh_600969_provide_water_supply", "company_id": "sh_600969", "node_id": "water_supply", "activity_type": "provide_service", "role": "供水服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务..."}]},
        {"exposure_id": "sh_600969_provide_industrial_gas", "company_id": "sh_600969", "node_id": "industrial_gas", "activity_type": "provide_service", "role": "工业气体服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体..."}]},
        {"exposure_id": "sh_600969_operate_waste_heat_power_generation", "company_id": "sh_600969", "node_id": "waste_heat_power_generation", "activity_type": "operate", "role": "余热发电运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电..."}]},
        {"exposure_id": "sh_600969_operate_hydro_power_generation", "company_id": "sh_600969", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水力发电运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "郴电国际主营业务", "quote": "主营业务除电力供应外,还包括供水业务以及工业气体,余热发电,水力发电投资业务等"}]},
        {"exposure_id": "sh_600975_produce_live_pig", "company_id": "sh_600975", "node_id": "live_pig", "activity_type": "produce", "role": "活大猪生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "新五丰主营业务", "quote": "活大猪,种猪,饲料"}]},
        {"exposure_id": "sh_600975_produce_breeding_pig", "company_id": "sh_600975", "node_id": "breeding_pig", "activity_type": "produce", "role": "种猪生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "新五丰主营业务", "quote": "活大猪,种猪,饲料"}]},
        {"exposure_id": "sh_600975_produce_feed", "company_id": "sh_600975", "node_id": "feed", "activity_type": "produce", "role": "饲料生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "新五丰主营业务", "quote": "活大猪,种猪,饲料"}]},
        {"exposure_id": "sh_600975_produce_pork_product", "company_id": "sh_600975", "node_id": "pork_product", "activity_type": "produce", "role": "猪肉制品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "新五丰经营范围", "quote": "鲜猪肉,冷却猪肉,冷冻猪肉销售,配送;预制菜(猪肉产品)的生产及销售"}]},
        {"exposure_id": "sh_600976_produce_chinese_patent_medicine", "company_id": "sh_600976", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "健民集团主营业务", "quote": "龙牡壮骨颗粒,健胃消食片,小儿宣肺止咳颗粒,健民咽喉片"}]},
        {"exposure_id": "sh_600980_produce_ferrite", "company_id": "sh_600980", "node_id": "ferrite", "activity_type": "produce", "role": "铁氧体生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "北矿科技主营业务", "quote": "烧结铁氧体,粘结铁氧体,烧结磁器件,粘结磁器件"}]},
        {"exposure_id": "sh_600980_produce_magnetic_device", "company_id": "sh_600980", "node_id": "magnetic_device", "activity_type": "produce", "role": "磁性器件生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "北矿科技主营业务", "quote": "烧结铁氧体,粘结铁氧体,烧结磁器件,粘结磁器件"}]},
        {"exposure_id": "sh_600985_produce_coal", "company_id": "sh_600985", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "淮北矿业主营业务", "quote": "主营业务为民用爆破器材的生产和销售,煤炭采掘,洗选加工,销售,煤化工产品的生产,销售等业务"}]},
        {"exposure_id": "sh_600985_produce_coke", "company_id": "sh_600985", "node_id": "coke", "activity_type": "produce", "role": "焦炭生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "淮北矿业主营业务", "quote": "主营业务为民用爆破器材的生产和销售,煤炭采掘,洗选加工,销售,煤化工产品的生产,销售等业务"}]},
        {"exposure_id": "sh_600985_produce_coal_chemical_product", "company_id": "sh_600985", "node_id": "coal_chemical_product", "activity_type": "produce", "role": "煤化工产品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "淮北矿业主营业务", "quote": "主营业务为民用爆破器材的生产和销售,煤炭采掘,洗选加工,销售,煤化工产品的生产,销售等业务"}]}
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 111")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))
print("\nBatch 111 submission completed.")
