#!/usr/bin/env python3
"""
Batch 102 Submission Script
Manually constructed based on analysis of each company's business.
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
    "batch_id": "batch_102_nodes",
    "task_description": "Batch 102:补充缺失的产业节点——焦炉煤气、文化纸、食品包装原纸、智能卡、证券印刷",
    "nodes_to_upsert": [
        {
            "node_id": "coke_oven_gas",
            "canonical_name_zh": "焦炉煤气",
            "canonical_name_en": "coke oven gas",
            "aliases": ["COG", "焦炉气"],
            "definition": "炼焦过程中煤在焦炉炭化室内经高温干馏产生的可燃气体，主要成分为氢气和甲烷，是焦炭生产的重要副产品，可用于燃料或化工原料。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "云煤能源主营业务",
                    "quote": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "cultural_paper",
            "canonical_name_zh": "文化纸",
            "canonical_name_en": "cultural paper",
            "aliases": ["书写纸", "印刷纸"],
            "definition": "用于书写、印刷、办公和文化传播用途的纸类产品，包括双胶纸、铜版纸、书写纸等，区别于包装纸和新闻纸。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "宜宾纸业主营业务",
                    "quote": "主营业务为生产销售新闻纸,文化纸,食品包装原纸"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "food_packaging_paper",
            "canonical_name_zh": "食品包装原纸",
            "canonical_name_en": "food packaging paper",
            "aliases": ["食品级包装纸", "食品卡纸"],
            "definition": "专门用于食品直接接触包装的纸类原材料，具有良好的阻隔性、安全性和印刷适性，经淋膜或涂布后可制成纸杯、纸碗、食品纸盒等。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "宜宾纸业主营业务",
                    "quote": "主营业务为生产销售新闻纸,文化纸,食品包装原纸"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "smart_card",
            "canonical_name_zh": "智能卡",
            "canonical_name_en": "smart card",
            "aliases": ["IC卡", "芯片卡", "卡类产品"],
            "definition": "内嵌集成电路芯片的塑料卡片，可实现数据存储、身份识别、电子支付等功能，包括金融IC卡、社保卡、交通卡、门禁卡等。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "渤海化学主营业务",
                    "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "security_printing",
            "canonical_name_zh": "证券印刷",
            "canonical_name_en": "security printing",
            "aliases": ["防伪印刷", "有价证券印刷", "票据印刷"],
            "definition": "采用特种纸张、防伪油墨、微缩文字、全息图案等防伪技术，印制钞票、有价证券、重要票据、证件等高安全等级印刷品的专门印刷服务。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "渤海化学主营业务",
                    "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "coal_to_coke",
            "from_node": "coal",
            "to_node": "coke",
            "edge_type": "material_flow",
            "description": "煤炭在高温干馏条件下转化为焦炭",
            "evidence": [
                {
                    "source_title": "炼焦工艺常识",
                    "quote": "焦炭由煤在焦炉中经高温干馏制得，是炼铁的主要还原剂和燃料。"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 102")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_102_business",
    "task_description": "Batch 102:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600790",
            "name_zh": "轻纺城",
            "aliases": ["浙江中国轻纺城集团股份有限公司"],
            "stock_codes": ["600790.SH"],
            "description": "纺织品销售及加工,市场租赁,酒类销售,建材销售",
            "country": "CN",
            "province": "浙江",
            "city": "绍兴市",
            "employee_count": 940,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600791",
            "name_zh": "京能置业",
            "aliases": ["京能置业股份有限公司"],
            "stock_codes": ["600791.SH"],
            "description": "主营业务为房地产开发与经营",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 331,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600792",
            "name_zh": "云煤能源",
            "aliases": ["云南煤业能源股份有限公司"],
            "stock_codes": ["600792.SH"],
            "description": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品",
            "country": "CN",
            "province": "云南",
            "city": "昆明市",
            "employee_count": 1581,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600793",
            "name_zh": "宜宾纸业",
            "aliases": ["宜宾纸业股份有限公司"],
            "stock_codes": ["600793.SH"],
            "description": "生产销售新闻纸,文化纸,食品包装原纸",
            "country": "CN",
            "province": "四川",
            "city": "宜宾市",
            "employee_count": 1662,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600794",
            "name_zh": "保税科技",
            "aliases": ["张家港保税科技(集团)股份有限公司"],
            "stock_codes": ["600794.SH"],
            "description": "液体化工品,固体干散货仓储业务及代理等物流服务业务",
            "country": "CN",
            "province": "江苏",
            "city": "苏州市",
            "employee_count": 489,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600795",
            "name_zh": "国电电力",
            "aliases": ["国电电力发展股份有限公司"],
            "stock_codes": ["600795.SH"],
            "description": "主要产品:电力",
            "country": "CN",
            "province": "辽宁",
            "city": "大连市",
            "employee_count": 37148,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600796",
            "name_zh": "钱江生化",
            "aliases": ["浙江钱江生物化学股份有限公司"],
            "stock_codes": ["600796.SH"],
            "description": "主要产品:杀菌剂类农药,生长调节剂类农药,杀虫剂类农药,兽药",
            "country": "CN",
            "province": "浙江",
            "city": "嘉兴市",
            "employee_count": 2021,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600797",
            "name_zh": "浙大网新",
            "aliases": ["浙大网新科技股份有限公司"],
            "stock_codes": ["600797.SH"],
            "description": "网络设备与终端,软件外包与服务",
            "country": "CN",
            "province": "浙江",
            "city": "杭州市",
            "employee_count": 4793,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600798",
            "name_zh": "宁波海运",
            "aliases": ["宁波海运股份有限公司"],
            "stock_codes": ["600798.SH"],
            "description": "国内沿海,长江中下游,国际船舶普通货物运输",
            "country": "CN",
            "province": "浙江",
            "city": "宁波市",
            "employee_count": 833,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600800",
            "name_zh": "渤海化学",
            "aliases": ["天津渤海化学股份有限公司"],
            "stock_codes": ["600800.SH"],
            "description": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务",
            "country": "CN",
            "province": "天津",
            "city": "天津市",
            "employee_count": 781,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600790 轻纺城
        {
            "exposure_id": "sh_600790_produce_textile_product",
            "company_id": "sh_600790",
            "node_id": "textile_product",
            "activity_type": "produce",
            "role": "纺织品销售加工商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "轻纺城主营业务", "quote": "纺织品销售及加工,市场租赁,酒类销售,建材销售"}]
        },
        {
            "exposure_id": "sh_600790_operate_commercial_property_operation",
            "company_id": "sh_600790",
            "node_id": "commercial_property_operation",
            "activity_type": "operate",
            "role": "纺织品市场运营商（市场租赁）",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "轻纺城主营业务", "quote": "纺织品销售及加工,市场租赁..."}]
        },
        # sh_600791 京能置业
        {
            "exposure_id": "sh_600791_operate_real_estate_development",
            "company_id": "sh_600791",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "京能置业主营业务", "quote": "主营业务为房地产开发与经营"}]
        },
        # sh_600792 云煤能源
        {
            "exposure_id": "sh_600792_produce_coke",
            "company_id": "sh_600792",
            "node_id": "coke",
            "activity_type": "produce",
            "role": "焦炭生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "云煤能源主营业务", "quote": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品"}]
        },
        {
            "exposure_id": "sh_600792_produce_coke_oven_gas",
            "company_id": "sh_600792",
            "node_id": "coke_oven_gas",
            "activity_type": "produce",
            "role": "焦炉煤气生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "云煤能源主营业务", "quote": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品"}]
        },
        {
            "exposure_id": "sh_600792_produce_industrial_steam",
            "company_id": "sh_600792",
            "node_id": "industrial_steam",
            "activity_type": "produce",
            "role": "工业蒸汽生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "云煤能源主营业务", "quote": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品"}]
        },
        {
            "exposure_id": "sh_600792_operate_thermal_power_generation",
            "company_id": "sh_600792",
            "node_id": "thermal_power_generation",
            "activity_type": "operate",
            "role": "余热发电运营商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "云煤能源主营业务", "quote": "生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品"}]
        },
        {
            "exposure_id": "sh_600792_procure_coal",
            "company_id": "sh_600792",
            "node_id": "coal",
            "activity_type": "procure",
            "role": "煤炭采购方（炼焦原料）",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "云煤能源经营范围", "quote": "炼焦;热力生产和供应;煤炭洗选;煤炭及制品销售"}]
        },
        # sh_600793 宜宾纸业
        {
            "exposure_id": "sh_600793_produce_newsprint",
            "company_id": "sh_600793",
            "node_id": "newsprint",
            "activity_type": "produce",
            "role": "新闻纸生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宜宾纸业主营业务", "quote": "主营业务为生产销售新闻纸,文化纸,食品包装原纸"}]
        },
        {
            "exposure_id": "sh_600793_produce_cultural_paper",
            "company_id": "sh_600793",
            "node_id": "cultural_paper",
            "activity_type": "produce",
            "role": "文化纸生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宜宾纸业主营业务", "quote": "主营业务为生产销售新闻纸,文化纸,食品包装原纸"}]
        },
        {
            "exposure_id": "sh_600793_produce_food_packaging_paper",
            "company_id": "sh_600793",
            "node_id": "food_packaging_paper",
            "activity_type": "produce",
            "role": "食品包装原纸生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宜宾纸业主营业务", "quote": "主营业务为生产销售新闻纸,文化纸,食品包装原纸"}]
        },
        # sh_600794 保税科技
        {
            "exposure_id": "sh_600794_operate_warehouse_service",
            "company_id": "sh_600794",
            "node_id": "warehouse_service",
            "activity_type": "operate",
            "role": "仓储服务运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "保税科技主营业务", "quote": "液体化工品,固体干散货仓储业务及代理等物流服务业务"}]
        },
        {
            "exposure_id": "sh_600794_operate_bonded_warehousing_service",
            "company_id": "sh_600794",
            "node_id": "bonded_warehousing_service",
            "activity_type": "operate",
            "role": "保税仓储运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "保税科技主营业务", "quote": "液体化工品,固体干散货仓储业务及代理等物流服务业务"}]
        },
        {
            "exposure_id": "sh_600794_operate_logistics_service",
            "company_id": "sh_600794",
            "node_id": "logistics_service",
            "activity_type": "operate",
            "role": "物流服务运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "保税科技主营业务", "quote": "液体化工品,固体干散货仓储业务及代理等物流服务业务"}]
        },
        # sh_600795 国电电力
        {
            "exposure_id": "sh_600795_operate_thermal_power_generation",
            "company_id": "sh_600795",
            "node_id": "thermal_power_generation",
            "activity_type": "operate",
            "role": "火力发电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "国电电力主营业务", "quote": "主要产品:电力"}]
        },
        {
            "exposure_id": "sh_600795_produce_electricity_power",
            "company_id": "sh_600795",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "国电电力主营业务", "quote": "主要产品:电力"}]
        },
        {
            "exposure_id": "sh_600795_procure_coal",
            "company_id": "sh_600795",
            "node_id": "coal",
            "activity_type": "procure",
            "role": "煤炭采购方（发电燃料）",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "国电电力经营范围", "quote": "电力,热力生产,销售;煤炭产品经营"}]
        },
        # sh_600796 钱江生化
        {
            "exposure_id": "sh_600796_produce_pesticide",
            "company_id": "sh_600796",
            "node_id": "pesticide",
            "activity_type": "produce",
            "role": "农药生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "钱江生化主营业务", "quote": "主要产品:杀菌剂类农药,生长调节剂类农药,杀虫剂类农药,兽药"}]
        },
        {
            "exposure_id": "sh_600796_produce_pesticide_formulation",
            "company_id": "sh_600796",
            "node_id": "pesticide_formulation",
            "activity_type": "produce",
            "role": "农药制剂生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "钱江生化主营业务", "quote": "主要产品:杀菌剂类农药,生长调节剂类农药,杀虫剂类农药,兽药"}]
        },
        {
            "exposure_id": "sh_600796_produce_veterinary_medicine",
            "company_id": "sh_600796",
            "node_id": "veterinary_medicine",
            "activity_type": "produce",
            "role": "兽药生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "钱江生化主营业务", "quote": "主要产品:杀菌剂类农药,生长调节剂类农药,杀虫剂类农药,兽药"}]
        },
        # sh_600797 浙大网新
        {
            "exposure_id": "sh_600797_produce_network_equipment",
            "company_id": "sh_600797",
            "node_id": "network_equipment",
            "activity_type": "produce",
            "role": "网络设备生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "浙大网新主营业务", "quote": "网络设备与终端,软件外包与服务"}]
        },
        {
            "exposure_id": "sh_600797_provide_software_development_service",
            "company_id": "sh_600797",
            "node_id": "software_development_service",
            "activity_type": "provide_service",
            "role": "软件外包与开发服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "浙大网新主营业务", "quote": "网络设备与终端,软件外包与服务"}]
        },
        # sh_600798 宁波海运
        {
            "exposure_id": "sh_600798_operate_shipping_service",
            "company_id": "sh_600798",
            "node_id": "shipping_service",
            "activity_type": "operate",
            "role": "航运服务运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宁波海运主营业务", "quote": "国内沿海,长江中下游,国际船舶普通货物运输"}]
        },
        # sh_600800 渤海化学
        {
            "exposure_id": "sh_600800_produce_smart_card",
            "company_id": "sh_600800",
            "node_id": "smart_card",
            "activity_type": "produce",
            "role": "智能卡生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "渤海化学主营业务", "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"}]
        },
        {
            "exposure_id": "sh_600800_provide_security_printing",
            "company_id": "sh_600800",
            "node_id": "security_printing",
            "activity_type": "provide_service",
            "role": "证券印刷服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "渤海化学主营业务", "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"}]
        },
        {
            "exposure_id": "sh_600800_provide_printing_service",
            "company_id": "sh_600800",
            "node_id": "printing_service",
            "activity_type": "provide_service",
            "role": "包装印刷服务商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "渤海化学主营业务", "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"}]
        },
        {
            "exposure_id": "sh_600800_operate_real_estate_development",
            "company_id": "sh_600800",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发运营商",
            "weight": 0.5,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "渤海化学主营业务", "quote": "卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 102")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 102 submission completed.")
