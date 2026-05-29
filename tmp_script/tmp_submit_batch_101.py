#!/usr/bin/env python3
"""
Batch 101 Submission Script
Manually constructed based on analysis of each company's business.
"""

import httpx
import json
from datetime import datetime

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
    "batch_id": "batch_101_nodes",
    "task_description": "Batch 101:补充缺失的产业节点——钢绞线",
    "nodes_to_upsert": [
        {
            "node_id": "steel_strand",
            "canonical_name_zh": "钢绞线",
            "canonical_name_en": "steel strand",
            "aliases": ["预应力钢绞线", "钢绞线束"],
            "definition": "由多根高强度冷拉光圆钢丝或刻痕钢丝按一定规则绞合而成的钢铁制品，广泛应用于预应力混凝土结构、桥梁拉索、岩土锚固、大型建筑等领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新钢股份主营业务描述",
                    "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品."
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "steel_wire_rod_to_steel_strand",
            "from_node": "steel_wire_rod",
            "to_node": "steel_strand",
            "edge_type": "material_flow",
            "description": "线材（盘条）经过拉拔、绞合等工艺加工成钢绞线",
            "evidence": [
                {
                    "source_title": "钢绞线生产工艺常识",
                    "quote": "钢绞线以高碳钢盘条为原料，经表面处理后冷拔成钢丝，再将若干根钢丝绞合而成。"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 101")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_101_business",
    "task_description": "Batch 101:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600777",
            "name_zh": "新潮能源",
            "aliases": ["*ST新潮", "山东新潮能源股份有限公司"],
            "stock_codes": ["600777.SH"],
            "description": "主营业务为原油及天然气的勘探、开采和销售",
            "country": "CN",
            "province": "山东",
            "city": "烟台市",
            "employee_count": 272,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600778",
            "name_zh": "友好集团",
            "aliases": ["新疆友好(集团)股份有限公司"],
            "stock_codes": ["600778.SH"],
            "description": "主要业务:商业,公用事业(供暖),酒店服务业,外贸出口,工业,房地产行业,广告业,旅游业",
            "country": "CN",
            "province": "新疆",
            "city": "乌鲁木齐市",
            "employee_count": 2327,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600779",
            "name_zh": "水井坊",
            "aliases": ["四川水井坊股份有限公司"],
            "stock_codes": ["600779.SH"],
            "description": "主要产品:高档酒,中低档酒,药业,印刷包装产品",
            "country": "CN",
            "province": "四川",
            "city": "成都市",
            "employee_count": 2015,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600780",
            "name_zh": "通宝能源",
            "aliases": ["山西通宝能源股份有限公司"],
            "stock_codes": ["600780.SH"],
            "description": "主营业务包括:火力发电,配电业务及燃气业务等",
            "country": "CN",
            "province": "山西",
            "city": "太原市",
            "employee_count": 4303,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600782",
            "name_zh": "新钢股份",
            "aliases": ["新余钢铁股份有限公司"],
            "stock_codes": ["600782.SH"],
            "description": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品",
            "country": "CN",
            "province": "江西",
            "city": "新余市",
            "employee_count": 11596,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600783",
            "name_zh": "鲁信创投",
            "aliases": ["鲁信创业投资集团股份有限公司"],
            "stock_codes": ["600783.SH"],
            "description": "创业投资业务;兼营磨料磨具,涂附磨具等",
            "country": "CN",
            "province": "山东",
            "city": "淄博市",
            "employee_count": 271,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600784",
            "name_zh": "鲁银投资",
            "aliases": ["鲁银投资集团股份有限公司"],
            "stock_codes": ["600784.SH"],
            "description": "主要业务:钢铁,医药,纺织;兼营羊绒制品,盐及盐化工产品",
            "country": "CN",
            "province": "山东",
            "city": "济南市",
            "employee_count": 2601,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600785",
            "name_zh": "新华百货",
            "aliases": ["银川新华百货商业集团股份有限公司"],
            "stock_codes": ["600785.SH"],
            "description": "商业零售业务,乳制品生产销售",
            "country": "CN",
            "province": "宁夏",
            "city": "银川市",
            "employee_count": 8329,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600787",
            "name_zh": "中储股份",
            "aliases": ["中储发展股份有限公司"],
            "stock_codes": ["600787.SH"],
            "description": "主要业务:期现货交割物流,大宗商品供应链,物流+互联网,消费品物流,工程物流,金融物流",
            "country": "CN",
            "province": "天津",
            "city": "天津市",
            "employee_count": 5141,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600789",
            "name_zh": "鲁抗医药",
            "aliases": ["山东鲁抗医药股份有限公司"],
            "stock_codes": ["600789.SH"],
            "description": "普药及半合抗原料药,普药及半合抗制剂,兽用抗生素",
            "country": "CN",
            "province": "山东",
            "city": "济宁市",
            "employee_count": 6388,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600777 新潮能源
        {
            "exposure_id": "sh_600777_produce_crude_oil",
            "company_id": "sh_600777",
            "node_id": "crude_oil",
            "activity_type": "produce",
            "role": "原油生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新潮能源主营业务", "quote": "主营业务为:原油及天然气的勘探,开采和销售"}]
        },
        {
            "exposure_id": "sh_600777_produce_natural_gas",
            "company_id": "sh_600777",
            "node_id": "natural_gas",
            "activity_type": "produce",
            "role": "天然气生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新潮能源主营业务", "quote": "主营业务为:原油及天然气的勘探,开采和销售"}]
        },
        {
            "exposure_id": "sh_600777_operate_petroleum_exploration",
            "company_id": "sh_600777",
            "node_id": "petroleum_exploration",
            "activity_type": "operate",
            "role": "油气勘探开采运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新潮能源主营业务", "quote": "主营业务为:原油及天然气的勘探,开采和销售"}]
        },
        # sh_600778 友好集团
        {
            "exposure_id": "sh_600778_operate_department_store",
            "company_id": "sh_600778",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "友好集团主营业务", "quote": "主要业务:商业..."}]
        },
        {
            "exposure_id": "sh_600778_provide_heating_supply",
            "company_id": "sh_600778",
            "node_id": "heating_supply",
            "activity_type": "provide_service",
            "role": "供热服务商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "友好集团主营业务", "quote": "主要业务:商业,公用事业(供暖),酒店服务业..."}]
        },
        {
            "exposure_id": "sh_600778_operate_hotel",
            "company_id": "sh_600778",
            "node_id": "hotel",
            "activity_type": "operate",
            "role": "酒店运营商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "友好集团主营业务", "quote": "主要业务:商业,公用事业(供暖),酒店服务业..."}]
        },
        {
            "exposure_id": "sh_600778_provide_tourism_service",
            "company_id": "sh_600778",
            "node_id": "tourism_service",
            "activity_type": "provide_service",
            "role": "旅游服务商",
            "weight": 0.5,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "友好集团主营业务", "quote": "主要业务:...旅游业"}]
        },
        # sh_600779 水井坊
        {
            "exposure_id": "sh_600779_produce_baijiu",
            "company_id": "sh_600779",
            "node_id": "baijiu",
            "activity_type": "produce",
            "role": "白酒生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "水井坊主营业务", "quote": "主要产品:高档酒,中低档酒..."}]
        },
        {
            "exposure_id": "sh_600779_produce_liquor",
            "company_id": "sh_600779",
            "node_id": "liquor",
            "activity_type": "produce",
            "role": "酒类生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "水井坊主营业务", "quote": "主要产品:高档酒,中低档酒,药业,印刷包装产品"}]
        },
        # sh_600780 通宝能源
        {
            "exposure_id": "sh_600780_operate_thermal_power_generation",
            "company_id": "sh_600780",
            "node_id": "thermal_power_generation",
            "activity_type": "operate",
            "role": "火力发电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通宝能源主营业务", "quote": "主营业务包括:火力发电,配电业务及燃气业务等"}]
        },
        {
            "exposure_id": "sh_600780_produce_electricity_power",
            "company_id": "sh_600780",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通宝能源主营业务", "quote": "主营业务包括:火力发电,配电业务及燃气业务等"}]
        },
        {
            "exposure_id": "sh_600780_procure_coal",
            "company_id": "sh_600780",
            "node_id": "coal",
            "activity_type": "procure",
            "role": "煤炭采购方（火力发电燃料）",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通宝能源主营业务", "quote": "主营业务包括:火力发电..."}]
        },
        # sh_600782 新钢股份
        {
            "exposure_id": "sh_600782_produce_medium_thick_plate",
            "company_id": "sh_600782",
            "node_id": "medium_thick_plate",
            "activity_type": "produce",
            "role": "中厚板生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新钢股份主营业务", "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品"}]
        },
        {
            "exposure_id": "sh_600782_produce_hot_rolled_coil",
            "company_id": "sh_600782",
            "node_id": "hot_rolled_coil",
            "activity_type": "produce",
            "role": "热轧卷板生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新钢股份主营业务", "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品"}]
        },
        {
            "exposure_id": "sh_600782_produce_steel_sheet",
            "company_id": "sh_600782",
            "node_id": "steel_sheet",
            "activity_type": "produce",
            "role": "冷轧钢板生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新钢股份主营业务", "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品"}]
        },
        {
            "exposure_id": "sh_600782_produce_steel_bar",
            "company_id": "sh_600782",
            "node_id": "steel_bar",
            "activity_type": "produce",
            "role": "棒材生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新钢股份主营业务", "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品"}]
        },
        {
            "exposure_id": "sh_600782_produce_steel_strand",
            "company_id": "sh_600782",
            "node_id": "steel_strand",
            "activity_type": "produce",
            "role": "钢绞线生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新钢股份主营业务", "quote": "主要产品:中厚板,热轧卷板,冷轧卷板,线棒材,钢绞线等钢材产品"}]
        },
        # sh_600783 鲁信创投
        {
            "exposure_id": "sh_600783_provide_equity_investment_service",
            "company_id": "sh_600783",
            "node_id": "equity_investment_service",
            "activity_type": "provide_service",
            "role": "创业投资服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鲁信创投主营业务", "quote": "创业投资业务"}]
        },
        {
            "exposure_id": "sh_600783_produce_abrasive_material",
            "company_id": "sh_600783",
            "node_id": "abrasive_material",
            "activity_type": "produce",
            "role": "磨料生产商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁信创投经营范围", "quote": "磨料磨具,涂附磨具...的生产,销售"}]
        },
        {
            "exposure_id": "sh_600783_produce_coated_abrasive",
            "company_id": "sh_600783",
            "node_id": "coated_abrasive",
            "activity_type": "produce",
            "role": "涂附磨具生产商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁信创投经营范围", "quote": "磨料磨具,涂附磨具...的生产,销售"}]
        },
        # sh_600784 鲁银投资
        {
            "exposure_id": "sh_600784_produce_steel_rebar",
            "company_id": "sh_600784",
            "node_id": "steel_rebar",
            "activity_type": "produce",
            "role": "钢材(螺纹钢)生产商",
            "weight": 0.8,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁银投资主营业务", "quote": "主要业务:钢铁..."}]
        },
        {
            "exposure_id": "sh_600784_produce_pharmaceutical_raw_material",
            "company_id": "sh_600784",
            "node_id": "pharmaceutical_raw_material",
            "activity_type": "produce",
            "role": "医药原料药生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁银投资主营业务", "quote": "主要业务:钢铁,医药,纺织"}]
        },
        {
            "exposure_id": "sh_600784_produce_textile_product",
            "company_id": "sh_600784",
            "node_id": "textile_product",
            "activity_type": "produce",
            "role": "纺织品生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁银投资主营业务", "quote": "主要业务:钢铁,医药,纺织"}]
        },
        {
            "exposure_id": "sh_600784_produce_cashmere_product",
            "company_id": "sh_600784",
            "node_id": "cashmere_product",
            "activity_type": "produce",
            "role": "羊绒制品生产商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁银投资经营范围", "quote": "羊绒制品的生产,销售"}]
        },
        {
            "exposure_id": "sh_600784_produce_salt_product",
            "company_id": "sh_600784",
            "node_id": "salt_product",
            "activity_type": "produce",
            "role": "盐产品生产商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鲁银投资经营范围", "quote": "盐及盐化工产品(不含化学危险品)生产,销售,运输"}]
        },
        # sh_600785 新华百货
        {
            "exposure_id": "sh_600785_operate_department_store",
            "company_id": "sh_600785",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新华百货主营业务", "quote": "商业零售业务,乳制品生产销售"}]
        },
        {
            "exposure_id": "sh_600785_produce_dairy_product",
            "company_id": "sh_600785",
            "node_id": "dairy_product",
            "activity_type": "produce",
            "role": "乳制品生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "新华百货主营业务", "quote": "商业零售业务,乳制品生产销售"}]
        },
        # sh_600787 中储股份
        {
            "exposure_id": "sh_600787_operate_warehouse_service",
            "company_id": "sh_600787",
            "node_id": "warehouse_service",
            "activity_type": "operate",
            "role": "仓储服务运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中储股份主营业务", "quote": "主要业务:期现货交割物流,大宗商品供应链,物流+互联网,消费品物流,工程物流,金融物流"}]
        },
        {
            "exposure_id": "sh_600787_operate_logistics_service",
            "company_id": "sh_600787",
            "node_id": "logistics_service",
            "activity_type": "operate",
            "role": "物流服务运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中储股份主营业务", "quote": "主要业务:期现货交割物流,大宗商品供应链..."}]
        },
        {
            "exposure_id": "sh_600787_provide_supply_chain_service",
            "company_id": "sh_600787",
            "node_id": "supply_chain_service",
            "activity_type": "provide_service",
            "role": "供应链服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中储股份主营业务", "quote": "主要业务:...大宗商品供应链..."}]
        },
        # sh_600789 鲁抗医药
        {
            "exposure_id": "sh_600789_produce_active_pharmaceutical_ingredient",
            "company_id": "sh_600789",
            "node_id": "active_pharmaceutical_ingredient",
            "activity_type": "produce",
            "role": "化学原料药生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鲁抗医药主营业务", "quote": "普药及半合抗原料药,普药及半合抗制剂,兽用抗生素"}]
        },
        {
            "exposure_id": "sh_600789_produce_antibiotic",
            "company_id": "sh_600789",
            "node_id": "antibiotic",
            "activity_type": "produce",
            "role": "抗生素生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鲁抗医药主营业务", "quote": "普药及半合抗原料药,普药及半合抗制剂,兽用抗生素"}]
        },
        {
            "exposure_id": "sh_600789_produce_antibiotic_preparation",
            "company_id": "sh_600789",
            "node_id": "antibiotic_preparation",
            "activity_type": "produce",
            "role": "抗生素制剂生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鲁抗医药主营业务", "quote": "普药及半合抗原料药,普药及半合抗制剂,兽用抗生素"}]
        },
        {
            "exposure_id": "sh_600789_produce_veterinary_medicine",
            "company_id": "sh_600789",
            "node_id": "veterinary_medicine",
            "activity_type": "produce",
            "role": "兽药生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鲁抗医药主营业务", "quote": "普药及半合抗原料药,普药及半合抗制剂,兽用抗生素"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 101")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 101 submission completed.")
