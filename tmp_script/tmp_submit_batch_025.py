#!/usr/bin/env python3
"""Batch 025 Submission Script"""
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
        "node_id": "hydrogen_fuel_cell_vehicle",
        "canonical_name_zh": "氢能燃料电池汽车",
        "canonical_name_en": "Hydrogen Fuel Cell Vehicle",
        "aliases": ["氢燃料电池车", "FCV"],
        "definition": "以氢气为燃料，通过燃料电池电化学反应产生电能驱动电机的零排放汽车，具备加氢速度快、续航里程长、低温性能好等优势，是新能源汽车的重要技术路线。",
        "entity_type": "device",
        "evidence": [{"source_title": "美锦能源 主营业务", "quote": "主要产品为:煤炭,焦炭及化产品,天然气,氢能燃料电池汽车等"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "hydrogen_energy",
        "canonical_name_zh": "氢能",
        "canonical_name_en": "Hydrogen Energy",
        "aliases": ["氢气能源", "绿氢"],
        "definition": "以氢气作为能量载体的清洁能源形式，可通过电解水、天然气重整、焦炉煤气提纯或可再生能源制氢等方式获取，用于燃料电池发电、化工原料替代及储能调峰。",
        "entity_type": "material",
        "evidence": [{"source_title": "美锦能源 主营业务", "quote": "氢能燃料电池汽车"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "display_terminal",
        "canonical_name_zh": "显示器终端产品",
        "canonical_name_en": "Display Terminal Product",
        "aliases": ["显示终端", "显示屏"],
        "definition": "面向终端用户的可视化信息显示设备总称，包括液晶显示器、OLED显示器、电子标牌、车载显示屏等，是人机交互的关键界面。",
        "entity_type": "device",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:显示器终端产品,薄膜晶体管液晶显示器件,小尺寸显示器件"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "tft_lcd",
        "canonical_name_zh": "薄膜晶体管液晶显示器件",
        "canonical_name_en": "Thin Film Transistor LCD",
        "aliases": ["TFT-LCD", "液晶面板模组"],
        "definition": "以薄膜晶体管（TFT）作为像素开关驱动的有源矩阵液晶显示器件，通过在玻璃基板上集成TFT阵列与彩色滤光片，实现高分辨率、高亮度的图像显示，是大尺寸电视和显示器的主流技术。",
        "entity_type": "component",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:...薄膜晶体管液晶显示器件"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "small_size_display",
        "canonical_name_zh": "小尺寸显示器件",
        "canonical_name_en": "Small Size Display Device",
        "aliases": ["中小尺寸显示屏", "移动显示模组"],
        "definition": "对角线尺寸通常在10英寸以下的显示器件，主要用于智能手机、平板电脑、车载仪表、可穿戴设备等移动终端，要求高分辨率、低功耗和轻薄化。",
        "entity_type": "component",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:...小尺寸显示器件"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "cotton_lint",
        "canonical_name_zh": "皮棉",
        "canonical_name_en": "Cotton Lint",
        "aliases": ["原棉", "轧花棉"],
        "definition": "籽棉经轧花加工去除棉籽后得到的纤维产品，是纺织工业的主要天然原料，按纤维长度分为细绒棉、长绒棉和粗绒棉。",
        "entity_type": "material",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面,衬衣,皮棉,纺纱"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "yarn",
        "canonical_name_zh": "纱线",
        "canonical_name_en": "Yarn",
        "aliases": ["棉纱", "纺纱"],
        "definition": "将棉花、化纤短纤等纤维原料经梳理、并条、粗纱、细纱等纺纱工序加捻制成的连续细长体，是织造面料的直接原材料。",
        "entity_type": "material",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:...皮棉,纺纱"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "dyed_woven_fabric",
        "canonical_name_zh": "色织面料",
        "canonical_name_en": "Dyed Woven Fabric",
        "aliases": ["色织布", "先染布"],
        "definition": "先将纱线染色，再进行织造的面料，与染整后染色的面料相比，具有色彩层次丰富、色牢度高、立体感强的特点，广泛用于高档衬衫、休闲服装和家纺产品。",
        "entity_type": "material",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面,衬衣"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "dress_shirt",
        "canonical_name_zh": "衬衣",
        "canonical_name_en": "Dress Shirt",
        "aliases": ["衬衫", "正装衬衫"],
        "definition": "以棉、麻、丝或混纺面料制成的前开襟上衣，通常配有领子和袖口，是商务正装和日常休闲的基础服装品类。",
        "entity_type": "material",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面,衬衣"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "av_product",
        "canonical_name_zh": "影音产品",
        "canonical_name_en": "Audio-Visual Product",
        "aliases": ["视听产品", "音响设备"],
        "definition": "用于音频播放、视频显示及家庭影音娱乐的电子设备集合，包括音响、投影仪、功放、播放器及配套周边设备。",
        "entity_type": "device",
        "evidence": [{"source_title": "冠捷科技 主营业务", "quote": "主要业务包括显示器,电视及影音产品的研发,制造,销售与服务"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "beer",
        "canonical_name_zh": "啤酒",
        "canonical_name_en": "Beer",
        "aliases": ["麦酒", "淡色啤酒"],
        "definition": "以大麦芽、啤酒花、水和酵母为主要原料，经糖化、发酵、过滤、灌装制成的低酒精度发酵酒，是全球消费量最大的酒精饮料品类。",
        "entity_type": "material",
        "evidence": [{"source_title": "燕京啤酒 主营业务", "quote": "主营业务:生产和销售啤酒"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "urea",
        "canonical_name_zh": "尿素",
        "canonical_name_en": "Urea",
        "aliases": ["碳酰胺", "氮肥"],
        "definition": "化学式为CO(NH₂)₂的白色晶体，含氮量最高的固体氮肥，由氨和二氧化碳在高温高压下合成，广泛用于农业施肥、饲料添加、车用尾气处理及工业原料。",
        "entity_type": "material",
        "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥,车用尿素"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "compound_fertilizer",
        "canonical_name_zh": "复合肥",
        "canonical_name_en": "Compound Fertilizer",
        "aliases": ["复混肥", "NPK肥"],
        "definition": "含有氮、磷、钾三种营养元素中至少两种的化学肥料，通过化学反应或物理混合制成，养分比例可根据作物和土壤需求调整，施肥效率高于单质肥料。",
        "entity_type": "material",
        "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥,车用尿素"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "vehicle_urea",
        "canonical_name_zh": "车用尿素",
        "canonical_name_en": "Diesel Exhaust Fluid (DEF)",
        "aliases": ["AdBlue", "柴油尾气处理液"],
        "definition": "浓度为32.5%的尿素水溶液，用于柴油车尾气选择性催化还原（SCR）系统，将尾气中的氮氧化物（NOx）还原为无害的氮气和水，是国四国五及以上排放标准柴油车的必备消耗品。",
        "entity_type": "material",
        "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥,车用尿素"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "new_type_electronic_component",
        "canonical_name_zh": "新型电子元器件",
        "canonical_name_en": "New Type Electronic Component",
        "aliases": ["高端元器件", "军用电子元器件"],
        "definition": "采用新材料、新工艺或新结构，具备更高性能、更小尺寸、更高可靠性的电子元器件，包括片式元件、厚薄膜混合集成电路、微波器件、敏感元件等，广泛应用于通信、航空航天和高端装备。",
        "entity_type": "component",
        "evidence": [{"source_title": "振华科技 主营业务", "quote": "主要产品:新型电子元器件,通信整机产品,机电一体化产品"}],
        "confidence": "HIGH", "status": "ACTIVE"
    },
    {
        "node_id": "livestock_breeding",
        "canonical_name_zh": "牲畜饲养",
        "canonical_name_en": "Livestock Breeding",
        "aliases": ["畜禽养殖", "畜牧养殖"],
        "definition": "以猪、牛、羊、家禽等牲畜为对象，通过舍饲或放牧方式进行的规模化养殖活动，为肉类、蛋奶等食品产业提供初级原料。",
        "entity_type": "service",
        "evidence": [{"source_title": "罗牛山 主营业务", "quote": "主要业务:以大农业为主"}],
        "confidence": "HIGH", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 2. INDUSTRIAL EDGES
# ---------------------------------------------------------------------------

edges = [
    {
        "edge_id": "flow_coke_to_hydrogen",
        "from_node": "coke",
        "to_node": "hydrogen_energy",
        "description": "焦炭生产过程中的焦炉煤气经提纯处理可获得氢气，是工业副产氢的重要来源。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "美锦能源 主营业务", "quote": "主要产品为:煤炭,焦炭及化产品,天然气,氢能燃料电池汽车等"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_hydrogen_to_fcv",
        "from_node": "hydrogen_energy",
        "to_node": "hydrogen_fuel_cell_vehicle",
        "description": "氢能在燃料电池汽车中经电化学反应产生电能，驱动车辆行驶。",
        "edge_namespace": "industrial_flow",
        "edge_type": "energy_flow",
        "evidence": [{"source_title": "美锦能源 主营业务", "quote": "氢能燃料电池汽车"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_tft_to_display_terminal",
        "from_node": "tft_lcd",
        "to_node": "display_terminal",
        "description": "薄膜晶体管液晶显示器件（TFT-LCD）是显示器终端产品的核心显示模组。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:显示器终端产品,薄膜晶体管液晶显示器件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_tft_to_lcd_panel",
        "from_node": "tft_lcd",
        "to_node": "lcd_panel",
        "description": "TFT-LCD模组构成液晶面板的核心显示层。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "薄膜晶体管液晶显示器件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_small_display_to_mobile",
        "from_node": "small_size_display",
        "to_node": "mobile_terminal",
        "description": "小尺寸显示器件作为屏幕组件嵌入移动互联终端设备。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "京东方A 主营业务", "quote": "小尺寸显示器件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_cotton_to_yarn",
        "from_node": "cotton_lint",
        "to_node": "yarn",
        "description": "皮棉经清花、梳棉、并条、粗纱、细纱等纺纱工序制成纱线。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:...皮棉,纺纱"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_yarn_to_fabric",
        "from_node": "yarn",
        "to_node": "dyed_woven_fabric",
        "description": "纱线经织造、整理制成色织面料。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面...纺纱"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_fabric_to_shirt",
        "from_node": "dyed_woven_fabric",
        "to_node": "dress_shirt",
        "description": "色织面料经裁剪、缝纫制成衬衣成衣。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面,衬衣"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_urea_to_compound",
        "from_node": "urea",
        "to_node": "compound_fertilizer",
        "description": "尿素作为氮源原料，与磷肥、钾肥及填充料混合或化合制成复合肥。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_urea_to_vehicle_urea",
        "from_node": "urea",
        "to_node": "vehicle_urea",
        "description": "高纯度尿素溶解于去离子水中，配制成32.5%浓度的车用尿素水溶液。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素...车用尿素"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_livestock_to_pig",
        "from_node": "livestock_breeding",
        "to_node": "live_pig",
        "description": "牲畜饲养服务产出生猪等畜禽产品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "罗牛山 主营业务", "quote": "牲畜饲养;牲畜销售;畜禽收购"}],
        "confidence": "HIGH"
    }
]

# ---------------------------------------------------------------------------
# 3. COMPANIES
# ---------------------------------------------------------------------------

companies = [
    {
        "company_id": "meijin_energy",
        "name_zh": "山西美锦能源股份有限公司",
        "aliases": ["美锦能源"],
        "stock_codes": ["000723.SZ"],
        "description": "主要产品包括煤炭、焦炭及化产品、天然气、氢能燃料电池汽车等，是国内焦炭行业的龙头企业之一，同时积极布局氢能源产业链。",
        "country": "CN", "province": "山西", "city": "太原市",
        "founded_year": 1997, "employee_count": 10103,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "boe_technology",
        "name_zh": "京东方科技集团股份有限公司",
        "aliases": ["京东方A", "京东方"],
        "stock_codes": ["000725.SZ"],
        "description": "主要产品包括显示器终端产品、薄膜晶体管液晶显示器件（TFT-LCD）、小尺寸显示器件，是全球领先的半导体显示技术、产品与服务提供商。",
        "country": "CN", "province": "北京", "city": "北京市",
        "founded_year": 1993, "employee_count": 109895,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "lutai_textile",
        "name_zh": "鲁泰纺织股份有限公司",
        "aliases": ["鲁泰A", "鲁泰纺织"],
        "stock_codes": ["000726.SZ"],
        "description": "主要产品包括衬衣色织面料、衬衣、皮棉、纺纱，是全球高端色织面料生产商和衬衫制造商。",
        "country": "CN", "province": "山东", "city": "淄博市",
        "founded_year": 1988, "employee_count": 23988,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "tpv_technology",
        "name_zh": "冠捷电子科技股份有限公司",
        "aliases": ["冠捷科技"],
        "stock_codes": ["000727.SZ"],
        "description": "主要业务包括显示器、电视及影音产品的研发、制造、销售与服务，是全球领先的显示器及智能电视制造商。",
        "country": "CN", "province": "江苏", "city": "南京市",
        "founded_year": 1993, "employee_count": 19417,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "guoyuan_securities",
        "name_zh": "国元证券股份有限公司",
        "aliases": ["国元证券"],
        "stock_codes": ["000728.SZ"],
        "description": "主营业务包括经纪业务、自营投资业务、投行业务、资产管理业务、基金管理业务、期货业务、境外业务等。",
        "country": "CN", "province": "安徽", "city": "合肥市",
        "founded_year": 1997, "employee_count": 3984,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "yanjing_beer",
        "name_zh": "北京燕京啤酒股份有限公司",
        "aliases": ["燕京啤酒"],
        "stock_codes": ["000729.SZ"],
        "description": "主营业务为生产和销售啤酒，是中国大型啤酒企业集团之一。",
        "country": "CN", "province": "北京", "city": "北京市",
        "founded_year": 1997, "employee_count": 19965,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "sichuan_meifeng",
        "name_zh": "四川美丰化工股份有限公司",
        "aliases": ["四川美丰"],
        "stock_codes": ["000731.SZ"],
        "description": "主要产品包括尿素、复合肥、车用尿素等化肥及环保产品。",
        "country": "CN", "province": "四川", "city": "遂宁市",
        "founded_year": 1997, "employee_count": 2473,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "zhenhua_tech",
        "name_zh": "中国振华(集团)科技股份有限公司",
        "aliases": ["振华科技"],
        "stock_codes": ["000733.SZ"],
        "description": "主要产品包括新型电子元器件、通信整机产品、机电一体化产品，服务于国防军工和国民经济关键领域。",
        "country": "CN", "province": "贵州", "city": "贵阳市",
        "founded_year": 1997, "employee_count": 7074,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "luoniushan",
        "name_zh": "罗牛山股份有限公司",
        "aliases": ["罗牛山"],
        "stock_codes": ["000735.SZ"],
        "description": "主要业务以大农业为主，以房地产开发业务、教育产业为辅。",
        "country": "CN", "province": "海南", "city": "海口市",
        "founded_year": 1987, "employee_count": 2722,
        "company_type": "public", "status": "ACTIVE"
    },
    {
        "company_id": "st_zhongdi",
        "name_zh": "中交城市发展控股集团股份有限公司",
        "aliases": ["*ST中地", "中交地产"],
        "stock_codes": ["000736.SZ"],
        "description": "主营业务为房地产开发、经营。",
        "country": "CN", "province": "重庆", "city": "重庆市",
        "founded_year": 1993, "employee_count": 1281,
        "company_type": "public", "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 4. COMPANY NODE EXPOSURES
# ---------------------------------------------------------------------------

exposures = [
    # 美锦能源
    {"exposure_id": "exp_mj_coal", "company_id": "meijin_energy", "node_id": "coal", "activity_type": "produce", "role": "煤炭生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "美锦能源 主营业务", "quote": "主要产品为:煤炭"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mj_coke", "company_id": "meijin_energy", "node_id": "coke", "activity_type": "produce", "role": "焦炭生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "美锦能源 主营业务", "quote": "主要产品为:...焦炭"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mj_natural_gas", "company_id": "meijin_energy", "node_id": "natural_gas", "activity_type": "produce", "role": "天然气生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "美锦能源 主营业务", "quote": "主要产品为:...天然气"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mj_hydrogen", "company_id": "meijin_energy", "node_id": "hydrogen_energy", "activity_type": "produce", "role": "氢能源生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "美锦能源 主营业务", "quote": "氢能燃料电池汽车"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mj_fcv", "company_id": "meijin_energy", "node_id": "hydrogen_fuel_cell_vehicle", "activity_type": "manufacture", "role": "氢燃料电池汽车制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "美锦能源 主营业务", "quote": "氢能燃料电池汽车"}], "status": "ACTIVE"},

    # 京东方A
    {"exposure_id": "exp_boe_display_terminal", "company_id": "boe_technology", "node_id": "display_terminal", "activity_type": "manufacture", "role": "显示器终端产品制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:显示器终端产品"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boe_tft", "company_id": "boe_technology", "node_id": "tft_lcd", "activity_type": "manufacture", "role": "TFT-LCD制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:...薄膜晶体管液晶显示器件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boe_small_display", "company_id": "boe_technology", "node_id": "small_size_display", "activity_type": "manufacture", "role": "小尺寸显示器件制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "京东方A 主营业务", "quote": "主要产品:...小尺寸显示器件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boe_lcd_panel", "company_id": "boe_technology", "node_id": "lcd_panel", "activity_type": "manufacture", "role": "液晶面板制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "京东方A 主营业务", "quote": "薄膜晶体管液晶显示器件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boe_oled", "company_id": "boe_technology", "node_id": "oled_panel", "activity_type": "manufacture", "role": "OLED面板制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "京东方A 经营范围", "quote": "制造电子产品,通信设备...OLED"}], "status": "ACTIVE"},

    # 鲁泰A
    {"exposure_id": "exp_lt_cotton", "company_id": "lutai_textile", "node_id": "cotton_lint", "activity_type": "produce", "role": "皮棉生产商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:...皮棉"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lt_yarn", "company_id": "lutai_textile", "node_id": "yarn", "activity_type": "produce", "role": "纺纱生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:...纺纱"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lt_fabric", "company_id": "lutai_textile", "node_id": "dyed_woven_fabric", "activity_type": "produce", "role": "色织面料制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:衬衣色织面"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lt_shirt", "company_id": "lutai_textile", "node_id": "dress_shirt", "activity_type": "manufacture", "role": "衬衣制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "鲁泰A 主营业务", "quote": "主要产品:...衬衣"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lt_textile", "company_id": "lutai_textile", "node_id": "textile_product", "activity_type": "produce", "role": "纺织品综合制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "鲁泰A 经营范围", "quote": "面料纺织加工;面料印染加工;服装制造"}], "status": "ACTIVE"},

    # 冠捷科技
    {"exposure_id": "exp_tpv_monitor", "company_id": "tpv_technology", "node_id": "lcd_monitor", "activity_type": "manufacture", "role": "显示器制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "冠捷科技 主营业务", "quote": "主要业务包括显示器...产品的研发,制造,销售与服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_tpv_tv", "company_id": "tpv_technology", "node_id": "color_tv", "activity_type": "manufacture", "role": "电视机制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "冠捷科技 主营业务", "quote": "主要业务包括...电视及影音产品的研发,制造,销售与服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_tpv_av", "company_id": "tpv_technology", "node_id": "av_product", "activity_type": "manufacture", "role": "影音产品制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "冠捷科技 主营业务", "quote": "主要业务包括...影音产品的研发,制造,销售与服务"}], "status": "ACTIVE"},

    # 国元证券
    {"exposure_id": "exp_gy_brokerage", "company_id": "guoyuan_securities", "node_id": "securities_brokerage", "activity_type": "operate", "role": "证券经纪服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "国元证券 主营业务", "quote": "主营业务:经纪业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gy_underwriting", "company_id": "guoyuan_securities", "node_id": "securities_underwriting", "activity_type": "operate", "role": "投行承销保荐服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "国元证券 主营业务", "quote": "投行业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gy_proprietary", "company_id": "guoyuan_securities", "node_id": "securities_proprietary_trading", "activity_type": "operate", "role": "证券自营投资商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "国元证券 主营业务", "quote": "自营投资业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gy_asset_mgmt", "company_id": "guoyuan_securities", "node_id": "asset_management_service", "activity_type": "operate", "role": "资产管理服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "国元证券 主营业务", "quote": "资产管理业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_gy_futures", "company_id": "guoyuan_securities", "node_id": "futures_brokerage", "activity_type": "operate", "role": "期货经纪服务商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "国元证券 主营业务", "quote": "期货业务"}], "status": "ACTIVE"},

    # 燕京啤酒
    {"exposure_id": "exp_yj_beer", "company_id": "yanjing_beer", "node_id": "beer", "activity_type": "produce", "role": "啤酒生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "燕京啤酒 主营业务", "quote": "主营业务:生产和销售啤酒"}], "status": "ACTIVE"},

    # 四川美丰
    {"exposure_id": "exp_mf_urea", "company_id": "sichuan_meifeng", "node_id": "urea", "activity_type": "produce", "role": "尿素生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mf_compound", "company_id": "sichuan_meifeng", "node_id": "compound_fertilizer", "activity_type": "produce", "role": "复合肥生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mf_vehicle_urea", "company_id": "sichuan_meifeng", "node_id": "vehicle_urea", "activity_type": "produce", "role": "车用尿素生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥,车用尿素"}], "status": "ACTIVE"},
    {"exposure_id": "exp_mf_chem_fertilizer", "company_id": "sichuan_meifeng", "node_id": "chemical_fertilizer", "activity_type": "produce", "role": "化学肥料综合生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "四川美丰 主营业务", "quote": "主要产品:尿素,复合肥,车用尿素"}], "status": "ACTIVE"},

    # 振华科技
    {"exposure_id": "exp_zh_electronic_comp", "company_id": "zhenhua_tech", "node_id": "new_type_electronic_component", "activity_type": "manufacture", "role": "新型电子元器件制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "振华科技 主营业务", "quote": "主要产品:新型电子元器件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zh_comm_equip", "company_id": "zhenhua_tech", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信整机产品制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "振华科技 主营业务", "quote": "主要产品:...通信整机产品"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zh_electromechanical", "company_id": "zhenhua_tech", "node_id": "electromechanical_product", "activity_type": "manufacture", "role": "机电一体化产品制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "振华科技 主营业务", "quote": "主要产品:...机电一体化产品"}], "status": "ACTIVE"},

    # 罗牛山
    {"exposure_id": "exp_lns_livestock", "company_id": "luoniushan", "node_id": "livestock_breeding", "activity_type": "operate", "role": "牲畜饲养服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "罗牛山 主营业务", "quote": "牲畜饲养;牲畜销售;畜禽收购"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lns_pig", "company_id": "luoniushan", "node_id": "live_pig", "activity_type": "produce", "role": "生猪生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "罗牛山 主营业务", "quote": "牲畜饲养;牲畜销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lns_realestate", "company_id": "luoniushan", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.4, "confidence": "HIGH", "evidence": [{"source_title": "罗牛山 主营业务", "quote": "房地产开发经营"}], "status": "ACTIVE"},
    {"exposure_id": "exp_lns_education", "company_id": "luoniushan", "node_id": "education_service", "activity_type": "operate", "role": "教育产业运营商", "weight": 0.3, "confidence": "HIGH", "evidence": [{"source_title": "罗牛山 主营业务", "quote": "主要业务:以大农业为主,以房地产开发业务,教育产业为辅"}], "status": "ACTIVE"},

    # *ST中地
    {"exposure_id": "exp_zd_realestate", "company_id": "st_zhongdi", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "*ST中地 主营业务", "quote": "主营业务:房地产开发,经营"}], "status": "ACTIVE"}
]

# ---------------------------------------------------------------------------
# 5. SUBMIT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph_batch = {
        "batch_id": "batch_025_graph",
        "task_description": "Batch 025: Industrial nodes and edges for 10 companies (000723-000736). Focus on hydrogen energy, display panels, textile chain, beer, fertilizers, electronic components, and real estate.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }

    business_batch = {
        "batch_id": "batch_025_business",
        "task_description": "Batch 025: Company registrations and node exposures for 10 companies (000723-000736).",
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
