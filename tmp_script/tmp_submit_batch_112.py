#!/usr/bin/env python3
"""Batch 112 Submission Script"""
import httpx, json
BASE_URL = "http://localhost:8005/api/v1"
def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()
def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

graph_batch = {
    "batch_id": "batch_112_nodes",
    "task_description": "Batch 112:补充数字营销、贵金属、雷达通信、钢丝绳、服装辅料、储能等缺失节点",
    "nodes_to_upsert": [
        {"node_id": "digital_marketing", "canonical_name_zh": "数字营销", "canonical_name_en": "digital marketing", "aliases": ["网络营销", "在线营销"], "definition": "利用互联网、移动互联网、社交媒体、搜索引擎、电子邮件等数字化渠道和工具，进行品牌推广、产品销售和客户关系管理的营销方式。", "entity_type": "service", "evidence": [{"source_title": "浙文互联主营业务", "quote": "主要业务为数字营销"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "gold", "canonical_name_zh": "黄金", "canonical_name_en": "gold", "aliases": ["金子", "金"], "definition": "化学元素符号Au，一种贵重金属，具有优良的导电性、延展性和抗腐蚀性，广泛用于珠宝首饰、电子工业、航空航天、投资储备和货币等领域。", "entity_type": "material", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "bismuth", "canonical_name_zh": "铋", "canonical_name_en": "bismuth", "aliases": ["金属铋"], "definition": "化学元素符号Bi，一种银白色至粉红色的脆性金属，是热导率最低的非放射性金属，广泛用于医药、化妆品、低熔点合金、半导体和核工业等领域。", "entity_type": "material", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "palladium", "canonical_name_zh": "钯", "canonical_name_en": "palladium", "aliases": ["金属钯"], "definition": "化学元素符号Pd，一种银白色过渡金属，具有优良的催化性能和储氢能力，广泛用于汽车催化转化器、电子元器件、牙科材料和珠宝等领域。", "entity_type": "material", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "rhodium", "canonical_name_zh": "铑", "canonical_name_en": "rhodium", "aliases": ["金属铑"], "definition": "化学元素符号Rh，一种银白色、坚硬、耐腐蚀的贵金属，具有极高的反射率和优良的催化性能，主要用于汽车催化转化器、化学催化剂、电镀和高温热电偶等领域。", "entity_type": "material", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "radar", "canonical_name_zh": "雷达", "canonical_name_en": "radar", "aliases": ["无线电探测和测距", "雷达系统"], "definition": "利用电磁波探测目标并测定其位置、速度和其他特性的电子设备系统，通过发射无线电波并接收目标反射的回波来实现探测功能，广泛应用于军事、航空、航海、气象和交通等领域。", "entity_type": "device", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "rf_component", "canonical_name_zh": "射频组件", "canonical_name_en": "RF component", "aliases": ["射频器件", "微波组件"], "definition": "用于射频信号产生、放大、滤波、混频、调制解调和传输的电子元器件和模块，是雷达、通信、导航等无线系统的核心组成部分。", "entity_type": "component", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "communication_engineering", "canonical_name_zh": "通信工程", "canonical_name_en": "communication engineering", "aliases": ["通讯工程"], "definition": "从事通信网络、通信系统和通信设备的规划、设计、施工、安装、调试和维护的工程技术服务，涵盖有线通信、无线通信、光纤通信和卫星通信等领域。", "entity_type": "service", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "steel_wire_rope", "canonical_name_zh": "钢丝绳", "canonical_name_en": "steel wire rope", "aliases": ["钢缆", "钢丝索"], "definition": "由多根高强度钢丝按一定规则捻制而成的柔性绳索，具有强度高、自重轻、弹性好、耐磨损等特点，广泛用于起重吊装、矿井提升、桥梁斜拉索、索道和船舶系泊等领域。", "entity_type": "component", "evidence": [{"source_title": "贵绳股份主营业务", "quote": "钢丝绳,钢丝"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "steel_wire", "canonical_name_zh": "钢丝", "canonical_name_en": "steel wire", "aliases": ["钢线"], "definition": "通过拉拔工艺将钢材加工成直径较小的圆形截面的金属线材，根据用途可分为弹簧钢丝、钢丝绳用钢丝、焊丝、切割钢丝、琴钢丝等。", "entity_type": "component", "evidence": [{"source_title": "贵绳股份主营业务", "quote": "钢丝绳,钢丝"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "hemorrhoid_medicine", "canonical_name_zh": "痔疮药", "canonical_name_en": "hemorrhoid medicine", "aliases": ["肛肠用药"], "definition": "用于治疗痔疮及相关肛肠疾病的外用或口服药物制剂，包括痔疮膏、痔疮栓、口服片剂等，具有消炎止痛、止血消肿、促进愈合等功效。", "entity_type": "material", "evidence": [{"source_title": "马应龙主营业务", "quote": "马应龙麝香痔疮膏,马应龙麝香痔疮栓,复方甘草合剂,斯普林"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "energy_storage", "canonical_name_zh": "储能", "canonical_name_en": "energy storage", "aliases": ["电能储存", "能量存储"], "definition": "将电能通过物理或化学方法转化为其他形式的能量储存起来，在需要时再转化为电能释放的技术和系统，包括抽水蓄能、电化学储能（锂电池、液流电池等）、压缩空气储能和飞轮储能等。", "entity_type": "service", "evidence": [{"source_title": "南网储能主营业务", "quote": "水力发电;发电业务,输电业务,供(配)电业务;储能技术服务"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "chip_card", "canonical_name_zh": "芯片卡", "canonical_name_en": "chip card", "aliases": ["IC卡", "智能卡"], "definition": "内嵌集成电路芯片的塑料卡片，可实现数据存储、身份识别、电子支付、安全认证等功能，包括金融IC卡、社保卡、交通卡、门禁卡等。", "entity_type": "component", "evidence": [{"source_title": "东信和平主营业务", "quote": "主要产品:芯片卡,充值卡"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "button", "canonical_name_zh": "钮扣", "canonical_name_en": "button", "aliases": ["纽扣", "扣子"], "definition": "用于服装、箱包等物品开合或装饰的小型配件，材料包括树脂、金属、贝壳、木材、陶瓷等，是服装辅料的重要组成部分。", "entity_type": "component", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "zipper", "canonical_name_zh": "拉链", "canonical_name_en": "zipper", "aliases": ["拉锁"], "definition": "由两条带有齿牙的布带通过拉头啮合或分离来实现开合功能的服装辅料和箱包配件，广泛应用于服装、鞋帽、箱包、帐篷等领域。", "entity_type": "component", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}], "confidence": "HIGH", "status": "ACTIVE"},
        {"node_id": "garment_accessory", "canonical_name_zh": "服装辅料", "canonical_name_en": "garment accessory", "aliases": ["服饰配件", "服装配件"], "definition": "除面料以外用于服装生产和装饰的各类辅助材料，包括钮扣、拉链、衬布、线、标签、垫肩、衣架等，是服装制造不可或缺的配套材料。", "entity_type": "component", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}], "confidence": "HIGH", "status": "ACTIVE"}
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 112")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

business_batch = {
    "batch_id": "batch_112_business",
    "task_description": "Batch 112:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {"company_id": "sh_600986", "name_zh": "浙文互联", "aliases": ["浙文互联集团股份有限公司"], "stock_codes": ["600986.SH"], "description": "主要业务为数字营销", "country": "CN", "province": "浙江", "city": "杭州市", "employee_count": 1123, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600988", "name_zh": "赤峰黄金", "aliases": ["赤峰吉隆黄金矿业集团股份有限公司"], "stock_codes": ["600988.SH"], "description": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属", "country": "CN", "province": "内蒙古", "city": "赤峰市", "employee_count": 6738, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600990", "name_zh": "四创电子", "aliases": ["四创电子股份有限公司"], "stock_codes": ["600990.SH"], "description": "雷达及雷达配套,通信射频组件,通讯工程", "country": "CN", "province": "安徽", "city": "合肥市", "employee_count": 2501, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600992", "name_zh": "贵绳股份", "aliases": ["贵州钢绳股份有限公司"], "stock_codes": ["600992.SH"], "description": "钢丝绳,钢丝", "country": "CN", "province": "贵州", "city": "遵义市", "employee_count": 3442, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600993", "name_zh": "马应龙", "aliases": ["马应龙药业集团股份有限公司"], "stock_codes": ["600993.SH"], "description": "马应龙麝香痔疮膏,马应龙麝香痔疮栓,复方甘草合剂,斯普林", "country": "CN", "province": "湖北", "city": "武汉市", "employee_count": 2654, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600995", "name_zh": "南网储能", "aliases": ["南方电网储能股份有限公司"], "stock_codes": ["600995.SH"], "description": "电力.水力发电;发电业务,输电业务,供(配)电业务;储能技术服务", "country": "CN", "province": "云南", "city": "文山壮族苗族自治州", "employee_count": 2461, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sh_600997", "name_zh": "开滦股份", "aliases": ["开滦能源化工股份有限公司"], "stock_codes": ["600997.SH"], "description": "煤炭及伴生资源开采,原煤洗选加工,煤炭批发,炼焦及其产品的生产销售", "country": "CN", "province": "河北", "city": "唐山市", "employee_count": 13895, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002017", "name_zh": "东信和平", "aliases": ["东信和平科技股份有限公司"], "stock_codes": ["002017.SZ"], "description": "主要产品:芯片卡,充值卡", "country": "CN", "province": "广东", "city": "珠海市", "employee_count": 1471, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002003", "name_zh": "伟星股份", "aliases": ["浙江伟星实业发展股份有限公司"], "stock_codes": ["002003.SZ"], "description": "主要产品:钮扣,拉链,其他服装辅料", "country": "CN", "province": "浙江", "city": "台州市", "employee_count": 10055, "company_type": "public", "status": "ACTIVE"},
        {"company_id": "sz_002004", "name_zh": "华邦健康", "aliases": ["华邦生命健康股份有限公司"], "stock_codes": ["002004.SZ"], "description": "主营业务主要为医药,农药和原料药.主要产品为迪银片,三蕊胶囊,力克肺疾", "country": "CN", "province": "重庆", "city": "重庆市", "employee_count": 12572, "company_type": "public", "status": "ACTIVE"}
    ],
    "company_node_exposures_to_upsert": [
        {"exposure_id": "sh_600986_provide_digital_marketing", "company_id": "sh_600986", "node_id": "digital_marketing", "activity_type": "provide_service", "role": "数字营销服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "浙文互联主营业务", "quote": "主要业务为数字营销"}]},
        {"exposure_id": "sh_600988_produce_gold", "company_id": "sh_600988", "node_id": "gold", "activity_type": "produce", "role": "黄金生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}]},
        {"exposure_id": "sh_600988_produce_silver", "company_id": "sh_600988", "node_id": "silver", "activity_type": "produce", "role": "白银生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}]},
        {"exposure_id": "sh_600988_produce_bismuth", "company_id": "sh_600988", "node_id": "bismuth", "activity_type": "produce", "role": "铋生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}]},
        {"exposure_id": "sh_600988_produce_palladium", "company_id": "sh_600988", "node_id": "palladium", "activity_type": "produce", "role": "钯生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}]},
        {"exposure_id": "sh_600988_produce_rhodium", "company_id": "sh_600988", "node_id": "rhodium", "activity_type": "produce", "role": "铑生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "赤峰黄金主营业务", "quote": "主要从事黄金采选及资源综合回收利用业务,主要产品为黄金,白银,铋,钯,铑等多种稀贵金属"}]},
        {"exposure_id": "sh_600990_produce_radar", "company_id": "sh_600990", "node_id": "radar", "activity_type": "produce", "role": "雷达生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}]},
        {"exposure_id": "sh_600990_produce_rf_component", "company_id": "sh_600990", "node_id": "rf_component", "activity_type": "produce", "role": "射频组件生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}]},
        {"exposure_id": "sh_600990_provide_communication_engineering", "company_id": "sh_600990", "node_id": "communication_engineering", "activity_type": "provide_service", "role": "通信工程服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "四创电子主营业务", "quote": "雷达及雷达配套,通信射频组件,通讯工程"}]},
        {"exposure_id": "sh_600992_produce_steel_wire_rope", "company_id": "sh_600992", "node_id": "steel_wire_rope", "activity_type": "produce", "role": "钢丝绳生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "贵绳股份主营业务", "quote": "钢丝绳,钢丝"}]},
        {"exposure_id": "sh_600992_produce_steel_wire", "company_id": "sh_600992", "node_id": "steel_wire", "activity_type": "produce", "role": "钢丝生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "贵绳股份主营业务", "quote": "钢丝绳,钢丝"}]},
        {"exposure_id": "sh_600993_produce_chinese_patent_medicine", "company_id": "sh_600993", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "马应龙主营业务", "quote": "马应龙麝香痔疮膏,马应龙麝香痔疮栓,复方甘草合剂,斯普林"}]},
        {"exposure_id": "sh_600993_produce_hemorrhoid_medicine", "company_id": "sh_600993", "node_id": "hemorrhoid_medicine", "activity_type": "produce", "role": "痔疮药生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "马应龙主营业务", "quote": "马应龙麝香痔疮膏,马应龙麝香痔疮栓,复方甘草合剂,斯普林"}]},
        {"exposure_id": "sh_600995_produce_electricity_power", "company_id": "sh_600995", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "南网储能主营业务", "quote": "水力发电;发电业务,输电业务,供(配)电业务"}]},
        {"exposure_id": "sh_600995_provide_energy_storage", "company_id": "sh_600995", "node_id": "energy_storage", "activity_type": "provide_service", "role": "储能技术服务商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "南网储能主营业务", "quote": "储能技术服务"}]},
        {"exposure_id": "sh_600997_produce_coal", "company_id": "sh_600997", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "开滦股份主营业务", "quote": "煤炭及伴生资源开采,原煤洗选加工,煤炭批发,炼焦及其产品的生产销售"}]},
        {"exposure_id": "sh_600997_produce_coke", "company_id": "sh_600997", "node_id": "coke", "activity_type": "produce", "role": "焦炭生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "开滦股份主营业务", "quote": "煤炭及伴生资源开采,原煤洗选加工,煤炭批发,炼焦及其产品的生产销售"}]},
        {"exposure_id": "sh_600997_produce_coal_chemical_product", "company_id": "sh_600997", "node_id": "coal_chemical_product", "activity_type": "produce", "role": "煤化工产品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "开滦股份主营业务", "quote": "煤炭及伴生资源开采,原煤洗选加工,煤炭批发,炼焦及其产品的生产销售"}]},
        {"exposure_id": "sz_002017_produce_chip_card", "company_id": "sz_002017", "node_id": "chip_card", "activity_type": "produce", "role": "芯片卡生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "东信和平主营业务", "quote": "主要产品:芯片卡,充值卡"}]},
        {"exposure_id": "sz_002017_produce_smart_card", "company_id": "sz_002017", "node_id": "smart_card", "activity_type": "produce", "role": "智能卡生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东信和平主营业务", "quote": "主要产品:芯片卡,充值卡"}]},
        {"exposure_id": "sz_002003_produce_button", "company_id": "sz_002003", "node_id": "button", "activity_type": "produce", "role": "钮扣生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}]},
        {"exposure_id": "sz_002003_produce_zipper", "company_id": "sz_002003", "node_id": "zipper", "activity_type": "produce", "role": "拉链生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}]},
        {"exposure_id": "sz_002003_produce_garment_accessory", "company_id": "sz_002003", "node_id": "garment_accessory", "activity_type": "produce", "role": "服装辅料生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "伟星股份主营业务", "quote": "主要产品:钮扣,拉链,其他服装辅料"}]},
        {"exposure_id": "sz_002004_produce_pharmaceutical_manufacturing", "company_id": "sz_002004", "node_id": "pharmaceutical_manufacturing", "activity_type": "produce", "role": "医药产品生产商", "weight": 1.0, "confidence": "HIGH", "evidence": [{"source_title": "华邦健康主营业务", "quote": "主营业务主要为医药,农药和原料药"}]},
        {"exposure_id": "sz_002004_produce_pesticide", "company_id": "sz_002004", "node_id": "pesticide", "activity_type": "produce", "role": "农药生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华邦健康主营业务", "quote": "主营业务主要为医药,农药和原料药"}]},
        {"exposure_id": "sz_002004_produce_active_pharmaceutical_ingredient", "company_id": "sz_002004", "node_id": "active_pharmaceutical_ingredient", "activity_type": "produce", "role": "原料药生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "华邦健康主营业务", "quote": "主营业务主要为医药,农药和原料药"}]},
        {"exposure_id": "sz_002004_produce_polymer_material", "company_id": "sz_002004", "node_id": "polymer_material", "activity_type": "produce", "role": "高分子材料生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "亿帆医药经营范围", "quote": "食品添加剂、饲料添加剂、高分子材料(除危险品及易制毒品)、医药中间体的研发、销售"}]}
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 112")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))
print("\nBatch 112 submission completed.")
