#!/usr/bin/env python3
"""
Batch 109 Submission Script
Stock codes: 600874, 600875, 600876, 600877, 600879, 600880, 600881, 600882, 600883, 600884
"""

import httpx
import json

BASE_URL = "http://localhost:8005/api/v1"

def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()

def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

# ============================================================
# STEP 1: Create missing industrial nodes
# ============================================================

graph_batch = {
    "batch_id": "batch_109_nodes",
    "task_description": "Batch 109:补充缺失的产业节点——污水处理、收费公路、航天电子设备、奶酪、液态奶、锂离子电池材料",
    "nodes_to_upsert": [
        {
            "node_id": "sewage_treatment",
            "canonical_name_zh": "污水处理",
            "canonical_name_en": "sewage treatment",
            "aliases": ["污水净化", "废水处理"],
            "definition": "采用物理、化学和生物等方法对生活和工业废水进行净化处理，使其达到排放标准或回用要求的环保工程服务，包括污水收集、预处理、生化处理、深度处理和污泥处置等环节。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "创业环保主营业务",
                    "quote": "主要业务:污水处理及污水处理厂建设业务,道路及收费站业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "toll_road",
            "canonical_name_zh": "收费公路",
            "canonical_name_en": "toll road",
            "aliases": ["高速公路收费", "路桥收费"],
            "definition": "通过收取车辆通行费来回收建设投资和运营维护成本的收费性公路或桥梁，包括政府还贷性收费公路和经营性收费公路两种模式，是现代交通基础设施投融资的重要方式。",
            "entity_type": "infrastructure",
            "evidence": [
                {
                    "source_title": "创业环保主营业务",
                    "quote": "主要业务:污水处理及污水处理厂建设业务,道路及收费站业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "aerospace_electronic_equipment",
            "canonical_name_zh": "航天电子设备",
            "canonical_name_en": "aerospace electronic equipment",
            "aliases": ["航天电子装备", "航天器电子设备"],
            "definition": "专门用于航天器（卫星、火箭、飞船、空间站等）的电子设备系统，包括导航系统、测控通信系统、遥感系统、电源系统、姿态控制系统等，要求在极端温度、辐射和真空环境下长期可靠工作。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "航天电子主营业务",
                    "quote": "航天电子设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "cheese",
            "canonical_name_zh": "奶酪",
            "canonical_name_en": "cheese",
            "aliases": ["干酪", "芝士", "起司"],
            "definition": "以牛奶、羊奶等鲜奶为原料，经凝乳酶或酸化使蛋白质凝固、排去乳清后发酵成熟的乳制品，富含蛋白质和钙质，是西式餐饮和烘焙食品的重要原料。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "妙可蓝多主营业务",
                    "quote": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "liquid_milk",
            "canonical_name_zh": "液态奶",
            "canonical_name_en": "liquid milk",
            "aliases": ["液体乳", "巴氏奶", "UHT奶"],
            "definition": "以生鲜牛（羊）乳为原料，经标准化、均质、杀菌等工艺加工制成的液体乳制品，包括巴氏杀菌乳、超高温灭菌乳（UHT奶）、调制乳和发酵乳等，是乳制品消费的主力品类。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "妙可蓝多主营业务",
                    "quote": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "lithium_ion_battery_material",
            "canonical_name_zh": "锂离子电池材料",
            "canonical_name_en": "lithium ion battery material",
            "aliases": ["锂电材料", "锂电池正负极材料", "电池材料"],
            "definition": "用于制造锂离子电池的关键功能性材料，主要包括正极材料（磷酸铁锂、三元材料等）、负极材料（人造石墨、天然石墨、硅基材料等）、电解液和隔膜，直接决定电池的能量密度、循环寿命和安全性能。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "杉杉股份主营业务",
                    "quote": "西服,休闲服,锂离子电池材料,衬衫"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 109")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_109_business",
    "task_description": "Batch 109:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600874",
            "name_zh": "创业环保",
            "aliases": ["天津创业环保集团股份有限公司"],
            "stock_codes": ["600874.SH"],
            "description": "主要业务:污水处理及污水处理厂建设业务,道路及收费站业务",
            "country": "CN",
            "province": "天津",
            "city": "天津市",
            "employee_count": 2330,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600875",
            "name_zh": "东方电气",
            "aliases": ["东方电气股份有限公司"],
            "stock_codes": ["600875.SH"],
            "description": "主要产品为火力发电设备,水力发电设备,风力发电设备,核能发电设备以及燃气发电设备等",
            "country": "CN",
            "province": "四川",
            "city": "成都市",
            "employee_count": 18753,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600876",
            "name_zh": "凯盛新能",
            "aliases": ["凯盛新能源股份有限公司"],
            "stock_codes": ["600876.SH"],
            "description": "浮法平板玻璃的制造和销售",
            "country": "CN",
            "province": "河南",
            "city": "洛阳市",
            "employee_count": 2336,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600877",
            "name_zh": "电科芯片",
            "aliases": ["中电科芯片技术股份有限公司"],
            "stock_codes": ["600877.SH"],
            "description": "集成电路设计,集成电路制造,集成电路销售,5G通信技术服务,物联网技术服务",
            "country": "CN",
            "province": "重庆",
            "city": "重庆市",
            "employee_count": 721,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600879",
            "name_zh": "航天电子",
            "aliases": ["航天时代电子技术股份有限公司"],
            "stock_codes": ["600879.SH"],
            "description": "航天电子设备",
            "country": "CN",
            "province": "湖北",
            "city": "武汉市",
            "employee_count": 12617,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600880",
            "name_zh": "博瑞传播",
            "aliases": ["成都博瑞传播股份有限公司"],
            "stock_codes": ["600880.SH"],
            "description": "主要业务:印刷业务,广告业务,新闻纸销售业务,发行投递业务",
            "country": "CN",
            "province": "四川",
            "city": "成都市",
            "employee_count": 565,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600881",
            "name_zh": "亚泰集团",
            "aliases": ["吉林亚泰(集团)股份有限公司"],
            "stock_codes": ["600881.SH"],
            "description": "水泥,商品房",
            "country": "CN",
            "province": "吉林",
            "city": "长春市",
            "employee_count": 13948,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600882",
            "name_zh": "妙可蓝多",
            "aliases": ["上海妙可蓝多食品科技股份有限公司"],
            "stock_codes": ["600882.SH"],
            "description": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 3232,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600883",
            "name_zh": "博闻科技",
            "aliases": ["云南博闻科技实业股份有限公司"],
            "stock_codes": ["600883.SH"],
            "description": "主要业务:水泥粉磨与销售",
            "country": "CN",
            "province": "云南",
            "city": "保山市",
            "employee_count": 93,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600884",
            "name_zh": "杉杉股份",
            "aliases": ["宁波杉杉股份有限公司"],
            "stock_codes": ["600884.SH"],
            "description": "西服,休闲服,锂离子电池材料,衬衫",
            "country": "CN",
            "province": "浙江",
            "city": "宁波市",
            "employee_count": 7184,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600874 创业环保
        {
            "exposure_id": "sh_600874_provide_sewage_treatment",
            "company_id": "sh_600874",
            "node_id": "sewage_treatment",
            "activity_type": "provide_service",
            "role": "污水处理服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "创业环保主营业务", "quote": "主要业务:污水处理及污水处理厂建设业务,道路及收费站业务"}]
        },
        {
            "exposure_id": "sh_600874_operate_toll_road",
            "company_id": "sh_600874",
            "node_id": "toll_road",
            "activity_type": "operate",
            "role": "收费公路运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "创业环保主营业务", "quote": "主要业务:污水处理及污水处理厂建设业务,道路及收费站业务"}]
        },
        # sh_600875 东方电气
        {
            "exposure_id": "sh_600875_produce_power_generation_equipment",
            "company_id": "sh_600875",
            "node_id": "power_generation_equipment",
            "activity_type": "produce",
            "role": "发电设备生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "东方电气主营业务", "quote": "主要产品为火力发电设备,水力发电设备,风力发电设备,核能发电设备以及燃气发电设备等"}]
        },
        {
            "exposure_id": "sh_600875_produce_thermal_power_generation",
            "company_id": "sh_600875",
            "node_id": "thermal_power_generation",
            "activity_type": "produce",
            "role": "火力发电设备生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "东方电气主营业务", "quote": "主要产品为火力发电设备,水力发电设备,风力发电设备,核能发电设备以及燃气发电设备等"}]
        },
        {
            "exposure_id": "sh_600875_produce_wind_power_generation",
            "company_id": "sh_600875",
            "node_id": "wind_power_generation",
            "activity_type": "produce",
            "role": "风力发电设备生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "东方电气主营业务", "quote": "主要产品为火力发电设备,水力发电设备,风力发电设备,核能发电设备以及燃气发电设备等"}]
        },
        # sh_600876 凯盛新能
        {
            "exposure_id": "sh_600876_produce_float_glass",
            "company_id": "sh_600876",
            "node_id": "float_glass",
            "activity_type": "produce",
            "role": "浮法玻璃生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "凯盛新能主营业务", "quote": "浮法平板玻璃的制造和销售"}]
        },
        {
            "exposure_id": "sh_600876_produce_pv_glass",
            "company_id": "sh_600876",
            "node_id": "pv_glass",
            "activity_type": "produce",
            "role": "光伏玻璃生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "凯盛新能经营范围", "quote": "光伏设备及元器件制造;光伏设备及元器件销售;玻璃制造;技术玻璃制品制造,技术玻璃制品销售;太阳能发电技术服务"}]
        },
        # sh_600877 电科芯片
        {
            "exposure_id": "sh_600877_produce_integrated_circuit",
            "company_id": "sh_600877",
            "node_id": "integrated_circuit",
            "activity_type": "produce",
            "role": "集成电路生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电科芯片经营范围", "quote": "电子元器件制造,集成电路设计,集成电路制造,集成电路销售,5G通信技术服务,物联网技术服务"}]
        },
        # sh_600879 航天电子
        {
            "exposure_id": "sh_600879_produce_aerospace_electronic_equipment",
            "company_id": "sh_600879",
            "node_id": "aerospace_electronic_equipment",
            "activity_type": "produce",
            "role": "航天电子设备生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天电子主营业务", "quote": "航天电子设备"}]
        },
        # sh_600880 博瑞传播
        {
            "exposure_id": "sh_600880_provide_printing_service",
            "company_id": "sh_600880",
            "node_id": "printing_service",
            "activity_type": "provide_service",
            "role": "印刷服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "博瑞传播主营业务", "quote": "主要业务:印刷业务,广告业务,新闻纸销售业务,发行投递业务"}]
        },
        {
            "exposure_id": "sh_600880_provide_advertising_service",
            "company_id": "sh_600880",
            "node_id": "advertising_service",
            "activity_type": "provide_service",
            "role": "广告服务商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "博瑞传播主营业务", "quote": "主要业务:印刷业务,广告业务,新闻纸销售业务,发行投递业务"}]
        },
        {
            "exposure_id": "sh_600880_produce_newsprint",
            "company_id": "sh_600880",
            "node_id": "newsprint",
            "activity_type": "produce",
            "role": "新闻纸销售商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "博瑞传播主营业务", "quote": "主要业务:印刷业务,广告业务,新闻纸销售业务,发行投递业务"}]
        },
        # sh_600881 亚泰集团
        {
            "exposure_id": "sh_600881_produce_cement",
            "company_id": "sh_600881",
            "node_id": "cement",
            "activity_type": "produce",
            "role": "水泥生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "亚泰集团主营业务", "quote": "水泥,商品房"}]
        },
        {
            "exposure_id": "sh_600881_operate_real_estate_development",
            "company_id": "sh_600881",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "亚泰集团主营业务", "quote": "水泥,商品房"}]
        },
        # sh_600882 妙可蓝多
        {
            "exposure_id": "sh_600882_produce_cheese",
            "company_id": "sh_600882",
            "node_id": "cheese",
            "activity_type": "produce",
            "role": "奶酪生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "妙可蓝多主营业务", "quote": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售"}]
        },
        {
            "exposure_id": "sh_600882_produce_liquid_milk",
            "company_id": "sh_600882",
            "node_id": "liquid_milk",
            "activity_type": "produce",
            "role": "液态奶生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "妙可蓝多主营业务", "quote": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售"}]
        },
        {
            "exposure_id": "sh_600882_produce_dairy_product",
            "company_id": "sh_600882",
            "node_id": "dairy_product",
            "activity_type": "produce",
            "role": "乳制品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "妙可蓝多主营业务", "quote": "主营业务:以奶酪,液态奶为核心的特色乳制品的研发,生产和销售"}]
        },
        # sh_600883 博闻科技
        {
            "exposure_id": "sh_600883_produce_cement",
            "company_id": "sh_600883",
            "node_id": "cement",
            "activity_type": "produce",
            "role": "水泥粉磨销售商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "博闻科技主营业务", "quote": "主要业务:水泥粉磨与销售"}]
        },
        # sh_600884 杉杉股份
        {
            "exposure_id": "sh_600884_produce_suit",
            "company_id": "sh_600884",
            "node_id": "suit",
            "activity_type": "produce",
            "role": "西服生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "杉杉股份主营业务", "quote": "西服,休闲服,锂离子电池材料,衬衫"}]
        },
        {
            "exposure_id": "sh_600884_produce_casual_wear",
            "company_id": "sh_600884",
            "node_id": "casual_wear",
            "activity_type": "produce",
            "role": "休闲服生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "杉杉股份主营业务", "quote": "西服,休闲服,锂离子电池材料,衬衫"}]
        },
        {
            "exposure_id": "sh_600884_produce_lithium_ion_battery_material",
            "company_id": "sh_600884",
            "node_id": "lithium_ion_battery_material",
            "activity_type": "produce",
            "role": "锂离子电池材料生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "杉杉股份主营业务", "quote": "西服,休闲服,锂离子电池材料,衬衫"}]
        },
        {
            "exposure_id": "sh_600884_produce_shirt",
            "company_id": "sh_600884",
            "node_id": "shirt",
            "activity_type": "produce",
            "role": "衬衫生产商",
            "weight": 0.5,
            "confidence": "HIGH",
            "evidence": [{"source_title": "杉杉股份主营业务", "quote": "西服,休闲服,锂离子电池材料,衬衫"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 109")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 109 submission completed.")
