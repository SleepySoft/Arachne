#!/usr/bin/env python3
"""
Batch 103 Submission Script
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
    "batch_id": "batch_103_nodes",
    "task_description": "Batch 103:补充缺失的产业节点——水泥熟料、拖拉机、长材、轮轴、配制酒、工业丝",
    "nodes_to_upsert": [
        {
            "node_id": "clinker",
            "canonical_name_zh": "水泥熟料",
            "canonical_name_en": "clinker",
            "aliases": ["熟料", "硅酸盐水泥熟料"],
            "definition": "以石灰石和粘土为主要原料，经破碎、配料、磨细制成生料，喂入水泥窑中煅烧而成的半成品，是生产硅酸盐水泥的核心中间产品。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "福建水泥主营业务",
                    "quote": "主要产品:水泥,商品熟料"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "tractor",
            "canonical_name_zh": "拖拉机",
            "canonical_name_en": "tractor",
            "aliases": ["农用拖拉机", "轮式拖拉机"],
            "definition": "一种用于牵引和驱动各种农业机械、运输工具或执行其他作业的自走式动力机械，是农业生产中的核心装备。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "悦达投资主营业务",
                    "quote": "主要产品:公路经营,物资贸易,生物制药,拖拉机"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "long_steel_product",
            "canonical_name_zh": "长材",
            "canonical_name_en": "long steel product",
            "aliases": ["型钢", "棒线材", "螺纹钢", "线材"],
            "definition": "长度远大于截面尺寸的钢材产品，包括型钢、螺纹钢、线材等，主要用于建筑结构、钢筋混凝土、桥梁、机械制造等领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "马钢股份主营业务",
                    "quote": "主要产品:钢材,大致可分为板材,长材和轮轴三大类"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "railway_wheel_axle",
            "canonical_name_zh": "轮轴",
            "canonical_name_en": "railway wheel and axle",
            "aliases": ["车轮车轴", "铁道车辆轮轴", "火车轮对"],
            "definition": "由车轮和车轴组装而成的铁道车辆走行部核心部件，承受车辆载荷并在轨道上滚动运行，是轨道交通安全的关键零部件。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "马钢股份主营业务",
                    "quote": "主要产品:钢材,大致可分为板材,长材和轮轴三大类"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "mixed_liquor",
            "canonical_name_zh": "配制酒",
            "canonical_name_en": "mixed liquor",
            "aliases": ["露酒", "调制酒", "保健酒"],
            "definition": "以发酵酒、蒸馏酒或食用酒精为酒基，加入可食用的辅料或食品添加剂，进行调配、混合或再加工制成的饮料酒，如竹叶青酒、劲酒等。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "山西汾酒经营范围",
                    "quote": "主营:汾酒,竹叶青酒及其系列酒的生产,销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "industrial_yarn",
            "canonical_name_zh": "工业丝",
            "canonical_name_en": "industrial yarn",
            "aliases": ["工业长丝", "高强工业丝", "涤纶工业丝"],
            "definition": "具有高强度、高模量、耐磨损等特性的化学纤维长丝，主要用于轮胎帘子布、传送带、缆绳、土工格栅、安全绳等工业领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "神马股份主营业务",
                    "quote": "主要产品:帘子布,工业丝"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "clinker_to_cement",
            "from_node": "clinker",
            "to_node": "cement",
            "edge_type": "material_flow",
            "description": "水泥熟料掺加适量石膏和混合材料后粉磨制成水泥",
            "evidence": [
                {
                    "source_title": "水泥生产工艺常识",
                    "quote": "水泥熟料加入适量石膏和混合材后粉磨即可制成水泥成品。"
                }
            ],
            "confidence": "HIGH"
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "industrial_yarn_to_tire_cord_fabric",
            "from_node": "industrial_yarn",
            "to_node": "tire_cord_fabric",
            "edge_type": "material_flow",
            "description": "工业丝经过织造加工制成轮胎帘子布",
            "evidence": [
                {
                    "source_title": "轮胎帘子布生产工艺",
                    "quote": "轮胎帘子布以涤纶或锦纶工业丝为原料，经织造和浸胶处理制成。"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 103")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_103_business",
    "task_description": "Batch 103:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600801",
            "name_zh": "华新建材",
            "aliases": ["华新建材集团股份有限公司"],
            "stock_codes": ["600801.SH"],
            "description": "水泥及其制品生产,销售",
            "country": "CN",
            "province": "湖北",
            "city": "黄石市",
            "employee_count": 21889,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600802",
            "name_zh": "福建水泥",
            "aliases": ["福建水泥股份有限公司"],
            "stock_codes": ["600802.SH"],
            "description": "主要产品:水泥,商品熟料",
            "country": "CN",
            "province": "福建",
            "city": "福州市",
            "employee_count": 1436,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600803",
            "name_zh": "新奥股份",
            "aliases": ["新奥天然气股份有限公司"],
            "stock_codes": ["600803.SH"],
            "description": "液化天然气生产/销售与投资,能源技术工程服务,甲醇等能源化工产品生产,煤炭的开采,洗选与贸易",
            "country": "CN",
            "province": "河北",
            "city": "石家庄市",
            "employee_count": 37142,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600805",
            "name_zh": "悦达投资",
            "aliases": ["江苏悦达投资股份有限公司"],
            "stock_codes": ["600805.SH"],
            "description": "主要产品:公路经营,物资贸易,生物制药,拖拉机",
            "country": "CN",
            "province": "江苏",
            "city": "盐城市",
            "employee_count": 2682,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600807",
            "name_zh": "济高发展",
            "aliases": ["济南高新发展股份有限公司"],
            "stock_codes": ["600807.SH"],
            "description": "主要业务:房地产+商业",
            "country": "CN",
            "province": "山东",
            "city": "济南市",
            "employee_count": 565,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600808",
            "name_zh": "马钢股份",
            "aliases": ["马鞍山钢铁股份有限公司"],
            "stock_codes": ["600808.SH"],
            "description": "主营业务:钢铁产品的生产和销售.主要产品:钢材,大致可分为板材,长材和轮轴三大类",
            "country": "CN",
            "province": "安徽",
            "city": "马鞍山市",
            "employee_count": 16780,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600809",
            "name_zh": "山西汾酒",
            "aliases": ["山西杏花村汾酒厂股份有限公司"],
            "stock_codes": ["600809.SH"],
            "description": "主要产品:白酒,配制酒",
            "country": "CN",
            "province": "山西",
            "city": "吕梁市",
            "employee_count": 13931,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600810",
            "name_zh": "神马股份",
            "aliases": ["神马实业股份有限公司"],
            "stock_codes": ["600810.SH"],
            "description": "主要产品:帘子布,工业丝",
            "country": "CN",
            "province": "河南",
            "city": "平顶山市",
            "employee_count": 8131,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600812",
            "name_zh": "华北制药",
            "aliases": ["华北制药股份有限公司"],
            "stock_codes": ["600812.SH"],
            "description": "主要产品包括抗感染原料药(中间体)及制剂,维生素等近600余个品规",
            "country": "CN",
            "province": "河北",
            "city": "石家庄市",
            "employee_count": 10088,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600814",
            "name_zh": "杭州解百",
            "aliases": ["杭州解百集团股份有限公司"],
            "stock_codes": ["600814.SH"],
            "description": "主要业务:商品销售业务,广告业务",
            "country": "CN",
            "province": "浙江",
            "city": "杭州市",
            "employee_count": 963,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600801 华新建材
        {
            "exposure_id": "sh_600801_produce_cement",
            "company_id": "sh_600801",
            "node_id": "cement",
            "activity_type": "produce",
            "role": "水泥生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华新建材主营业务", "quote": "主营业务;水泥及其制品生产,销售"}]
        },
        {
            "exposure_id": "sh_600801_produce_cement_product",
            "company_id": "sh_600801",
            "node_id": "cement_product",
            "activity_type": "produce",
            "role": "水泥制品生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华新建材主营业务", "quote": "主营业务;水泥及其制品生产,销售"}]
        },
        {
            "exposure_id": "sh_600801_produce_clinker",
            "company_id": "sh_600801",
            "node_id": "clinker",
            "activity_type": "produce",
            "role": "水泥熟料生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华新建材经营范围", "quote": "水泥生产;水泥制品制造;水泥制品销售"}]
        },
        # sh_600802 福建水泥
        {
            "exposure_id": "sh_600802_produce_cement",
            "company_id": "sh_600802",
            "node_id": "cement",
            "activity_type": "produce",
            "role": "水泥生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "福建水泥主营业务", "quote": "主要产品:水泥,商品熟料"}]
        },
        {
            "exposure_id": "sh_600802_produce_clinker",
            "company_id": "sh_600802",
            "node_id": "clinker",
            "activity_type": "produce",
            "role": "商品熟料生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "福建水泥主营业务", "quote": "主要产品:水泥,商品熟料"}]
        },
        # sh_600803 新奥股份
        {
            "exposure_id": "sh_600803_produce_lng",
            "company_id": "sh_600803",
            "node_id": "lng",
            "activity_type": "produce",
            "role": "液化天然气生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新奥股份主营业务", "quote": "主营业务:液化天然气生产/销售与投资..."}]
        },
        {
            "exposure_id": "sh_600803_produce_methanol",
            "company_id": "sh_600803",
            "node_id": "methanol",
            "activity_type": "produce",
            "role": "甲醇生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新奥股份主营业务", "quote": "...甲醇等能源化工产品生产,销售与贸易..."}]
        },
        {
            "exposure_id": "sh_600803_operate_coal_mining",
            "company_id": "sh_600803",
            "node_id": "coal_mining",
            "activity_type": "operate",
            "role": "煤炭开采运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新奥股份主营业务", "quote": "...煤炭的开采,洗选与贸易..."}]
        },
        {
            "exposure_id": "sh_600803_produce_coal",
            "company_id": "sh_600803",
            "node_id": "coal",
            "activity_type": "produce",
            "role": "煤炭生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新奥股份主营业务", "quote": "...煤炭的开采,洗选与贸易..."}]
        },
        # sh_600805 悦达投资
        {
            "exposure_id": "sh_600805_operate_highway_operation_service",
            "company_id": "sh_600805",
            "node_id": "highway_operation_service",
            "activity_type": "operate",
            "role": "公路经营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "悦达投资主营业务", "quote": "主要产品:公路经营,物资贸易,生物制药,拖拉机"}]
        },
        {
            "exposure_id": "sh_600805_provide_trade_agent",
            "company_id": "sh_600805",
            "node_id": "trade_agent",
            "activity_type": "provide_service",
            "role": "物资贸易服务商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "悦达投资主营业务", "quote": "主要产品:公路经营,物资贸易,生物制药,拖拉机"}]
        },
        {
            "exposure_id": "sh_600805_produce_biological_drug",
            "company_id": "sh_600805",
            "node_id": "biological_drug",
            "activity_type": "produce",
            "role": "生物制药生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "悦达投资主营业务", "quote": "主要产品:公路经营,物资贸易,生物制药,拖拉机"}]
        },
        {
            "exposure_id": "sh_600805_produce_tractor",
            "company_id": "sh_600805",
            "node_id": "tractor",
            "activity_type": "produce",
            "role": "拖拉机生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "悦达投资主营业务", "quote": "主要产品:公路经营,物资贸易,生物制药,拖拉机"}]
        },
        # sh_600807 济高发展
        {
            "exposure_id": "sh_600807_operate_real_estate_development",
            "company_id": "sh_600807",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "济高发展主营业务", "quote": "主要业务:房地产+商业"}]
        },
        # sh_600808 马钢股份
        {
            "exposure_id": "sh_600808_produce_steel_plate",
            "company_id": "sh_600808",
            "node_id": "steel_plate",
            "activity_type": "produce",
            "role": "板材生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "马钢股份主营业务", "quote": "主要产品:钢材,大致可分为板材,长材和轮轴三大类"}]
        },
        {
            "exposure_id": "sh_600808_produce_long_steel_product",
            "company_id": "sh_600808",
            "node_id": "long_steel_product",
            "activity_type": "produce",
            "role": "长材生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "马钢股份主营业务", "quote": "主要产品:钢材,大致可分为板材,长材和轮轴三大类"}]
        },
        {
            "exposure_id": "sh_600808_produce_railway_wheel_axle",
            "company_id": "sh_600808",
            "node_id": "railway_wheel_axle",
            "activity_type": "produce",
            "role": "轮轴生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "马钢股份主营业务", "quote": "主要产品:钢材,大致可分为板材,长材和轮轴三大类"}]
        },
        # sh_600809 山西汾酒
        {
            "exposure_id": "sh_600809_produce_baijiu",
            "company_id": "sh_600809",
            "node_id": "baijiu",
            "activity_type": "produce",
            "role": "白酒生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "山西汾酒主营业务", "quote": "主营:汾酒,竹叶青酒及其系列酒的生产,销售"}]
        },
        {
            "exposure_id": "sh_600809_produce_liquor",
            "company_id": "sh_600809",
            "node_id": "liquor",
            "activity_type": "produce",
            "role": "酒类生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "山西汾酒主营业务", "quote": "主营:汾酒,竹叶青酒及其系列酒的生产,销售"}]
        },
        {
            "exposure_id": "sh_600809_produce_mixed_liquor",
            "company_id": "sh_600809",
            "node_id": "mixed_liquor",
            "activity_type": "produce",
            "role": "配制酒生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "山西汾酒经营范围", "quote": "主营:汾酒,竹叶青酒及其系列酒的生产,销售"}]
        },
        # sh_600810 神马股份
        {
            "exposure_id": "sh_600810_produce_tire_cord_fabric",
            "company_id": "sh_600810",
            "node_id": "tire_cord_fabric",
            "activity_type": "produce",
            "role": "轮胎帘子布生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "神马股份主营业务", "quote": "主要产品:帘子布,工业丝"}]
        },
        {
            "exposure_id": "sh_600810_produce_industrial_yarn",
            "company_id": "sh_600810",
            "node_id": "industrial_yarn",
            "activity_type": "produce",
            "role": "工业丝生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "神马股份主营业务", "quote": "主要产品:帘子布,工业丝"}]
        },
        # sh_600812 华北制药
        {
            "exposure_id": "sh_600812_produce_active_pharmaceutical_ingredient",
            "company_id": "sh_600812",
            "node_id": "active_pharmaceutical_ingredient",
            "activity_type": "produce",
            "role": "原料药生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华北制药主营业务", "quote": "主要产品包括抗感染原料药(中间体)及制剂,维生素等近600余个品规"}]
        },
        {
            "exposure_id": "sh_600812_produce_pharmaceutical_intermediate",
            "company_id": "sh_600812",
            "node_id": "pharmaceutical_intermediate",
            "activity_type": "produce",
            "role": "医药中间体生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华北制药主营业务", "quote": "主要产品包括抗感染原料药(中间体)及制剂..."}]
        },
        {
            "exposure_id": "sh_600812_produce_antibiotic",
            "company_id": "sh_600812",
            "node_id": "antibiotic",
            "activity_type": "produce",
            "role": "抗生素生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华北制药主营业务", "quote": "其中青霉素,硫酸链霉素,阿莫西林,头孢拉定...等品种的产销量居世界前列"}]
        },
        {
            "exposure_id": "sh_600812_produce_vitamin",
            "company_id": "sh_600812",
            "node_id": "vitamin",
            "activity_type": "produce",
            "role": "维生素生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华北制药主营业务", "quote": "主要产品包括抗感染原料药(中间体)及制剂,维生素等近600余个品规"}]
        },
        # sh_600814 杭州解百
        {
            "exposure_id": "sh_600814_operate_department_store",
            "company_id": "sh_600814",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "杭州解百主营业务", "quote": "主要业务:商品销售业务,广告业务"}]
        },
        {
            "exposure_id": "sh_600814_provide_advertising_service",
            "company_id": "sh_600814",
            "node_id": "advertising_service",
            "activity_type": "provide_service",
            "role": "广告服务商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "杭州解百主营业务", "quote": "主要业务:商品销售业务,广告业务"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 103")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 103 submission completed.")
