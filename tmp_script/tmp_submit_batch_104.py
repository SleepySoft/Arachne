#!/usr/bin/env python3
"""
Batch 104 Submission Script
Note: Two companies have corrected business descriptions based on web verification:
- 宇通重工 (600817): actual business is sanitation equipment, mining equipment, construction machinery
  (batch data "集成电路产品,家电产品" was incorrect)
- 金开新能 (600821): actual business is photovoltaic and wind power generation
  (batch data "商业零售" was pre-restructuring legacy)
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
    "batch_id": "batch_104_nodes",
    "task_description": "Batch 104:补充缺失的产业节点——装载机、环卫设备、康体设备、加工玻璃、隧道工程",
    "nodes_to_upsert": [
        {
            "node_id": "wheel_loader",
            "canonical_name_zh": "装载机",
            "canonical_name_en": "wheel loader",
            "aliases": ["铲车", "轮式装载机"],
            "definition": "一种装有铲斗、用于铲装土壤、砂石、煤炭等散状物料的土方工程机械，广泛应用于公路、铁路、建筑、水电、港口、矿山等建设工程中。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "厦工股份主营业务",
                    "quote": "主营业务:装载机,挖掘机和小型工程机械等工程机械产品及其配件的制造,加工和销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "sanitation_equipment",
            "canonical_name_zh": "环卫设备",
            "canonical_name_en": "sanitation equipment",
            "aliases": ["环卫车辆", "清洁设备", "环卫机械"],
            "definition": "用于城乡道路清扫保洁、垃圾收集转运、洒水抑尘等环境卫生作业的专业机械设备，包括洗扫车、压缩式垃圾车、洒水车、抑尘车等。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "宇通重工2025年年度报告",
                    "quote": "公司主要业务涵盖环卫设备、矿用装备、基础工程机械三大业务板块...保洁类产品：洗扫车、扫路车、吸尘车、清洗车、洒水车、抑尘车...收转运类产品：压缩式垃圾车、餐厨垃圾车、自装卸式垃圾车"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "fitness_equipment",
            "canonical_name_zh": "康体设备",
            "canonical_name_en": "fitness equipment",
            "aliases": ["健身器材", "体育器材", "康体器材"],
            "definition": "用于体育锻炼、康复训练和身体保健的机械设备及器材，包括跑步机、力量训练器械、动感单车、按摩器材等。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "ST中路主营业务",
                    "quote": "自行车,康体设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "processed_glass",
            "canonical_name_zh": "加工玻璃",
            "canonical_name_en": "processed glass",
            "aliases": ["深加工玻璃", "玻璃深加工产品", "特种玻璃"],
            "definition": "以浮法玻璃原片为基材，经过切割、磨边、钢化、镀膜、中空、夹层、丝印等后续加工工艺制成的具有特定功能或性能的玻璃制品，包括钢化玻璃、夹层玻璃、中空玻璃、镀膜玻璃等。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "耀皮玻璃主营业务",
                    "quote": "主要产品:浮法玻璃,加工玻璃"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "tunnel_engineering",
            "canonical_name_zh": "隧道工程",
            "canonical_name_en": "tunnel engineering",
            "aliases": ["隧道施工", "地下工程", "盾构工程"],
            "definition": "在地下或水下开凿通道的土木工程建设活动，包括隧道设计、盾构掘进、衬砌施工、通风照明系统安装等，广泛应用于城市轨道交通、铁路公路穿越山岭、市政管线等场景。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "隧道股份主营业务",
                    "quote": "投资,设计,施工,运营一体化的城市基础设施建设运营"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "float_glass_to_processed_glass",
            "from_node": "float_glass",
            "to_node": "processed_glass",
            "edge_type": "material_flow",
            "description": "浮法玻璃原片经过切割、钢化、镀膜等深加工工艺制成加工玻璃",
            "evidence": [
                {
                    "source_title": "玻璃深加工工艺常识",
                    "quote": "浮法玻璃原片经过切割、磨边、钢化、镀膜、中空等深加工后，制成具有特定功能的加工玻璃产品。"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 104")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_104_business",
    "task_description": "Batch 104:注册10家公司及其产业节点暴露（含2家经网络核查修正主营业务的公司）",
    "companies_to_upsert": [
        {
            "company_id": "sh_600815",
            "name_zh": "厦工股份",
            "aliases": ["厦门厦工机械股份有限公司"],
            "stock_codes": ["600815.SH"],
            "description": "主营业务:装载机,挖掘机和小型工程机械等工程机械产品及其配件的制造,加工和销售",
            "country": "CN",
            "province": "福建",
            "city": "厦门市",
            "employee_count": 589,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600816",
            "name_zh": "建元信托",
            "aliases": ["建元信托股份有限公司"],
            "stock_codes": ["600816.SH"],
            "description": "主要业务:金融信托业务",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 299,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600817",
            "name_zh": "宇通重工",
            "aliases": ["宇通重工股份有限公司"],
            "stock_codes": ["600817.SH"],
            "description": "主要业务涵盖环卫设备、矿用装备、基础工程机械三大业务板块（经网络核查修正）",
            "country": "CN",
            "province": "河南",
            "city": "郑州市",
            "employee_count": 1960,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600818",
            "name_zh": "ST中路",
            "aliases": ["中路股份有限公司"],
            "stock_codes": ["600818.SH"],
            "description": "自行车,康体设备",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 488,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600819",
            "name_zh": "耀皮玻璃",
            "aliases": ["上海耀皮玻璃集团股份有限公司"],
            "stock_codes": ["600819.SH"],
            "description": "主要产品:浮法玻璃,加工玻璃",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 3876,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600820",
            "name_zh": "隧道股份",
            "aliases": ["上海隧道工程股份有限公司"],
            "stock_codes": ["600820.SH"],
            "description": "投资,设计,施工,运营一体化的城市基础设施建设运营",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 17492,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600821",
            "name_zh": "金开新能",
            "aliases": ["金开新能源股份有限公司"],
            "stock_codes": ["600821.SH"],
            "description": "新能源电力的开发,投资,建设及运营,主要包括光伏发电和风力发电（经网络核查修正）",
            "country": "CN",
            "province": "天津",
            "city": "天津市",
            "employee_count": 563,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600822",
            "name_zh": "上海物贸",
            "aliases": ["上海物资贸易股份有限公司"],
            "stock_codes": ["600822.SH"],
            "description": "主营业务:汽车贸易,化工等生产资料的批发与零售,以及有色金属平台交易",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 866,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600824",
            "name_zh": "益民集团",
            "aliases": ["上海益民商业集团股份有限公司"],
            "stock_codes": ["600824.SH"],
            "description": "主要业务:百货零售业",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 453,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600825",
            "name_zh": "新华传媒",
            "aliases": ["上海新华传媒股份有限公司"],
            "stock_codes": ["600825.SH"],
            "description": "主营业务:主要板块分为图书,音像制品,文教用品,报刊广告和其他",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 1168,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600815 厦工股份
        {
            "exposure_id": "sh_600815_produce_wheel_loader",
            "company_id": "sh_600815",
            "node_id": "wheel_loader",
            "activity_type": "produce",
            "role": "装载机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦工股份主营业务", "quote": "主营业务:装载机,挖掘机和小型工程机械等工程机械产品及其配件的制造,加工和销售"}]
        },
        {
            "exposure_id": "sh_600815_produce_excavator",
            "company_id": "sh_600815",
            "node_id": "excavator",
            "activity_type": "produce",
            "role": "挖掘机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦工股份主营业务", "quote": "主营业务:装载机,挖掘机和小型工程机械等工程机械产品及其配件的制造,加工和销售"}]
        },
        {
            "exposure_id": "sh_600815_produce_construction_machinery",
            "company_id": "sh_600815",
            "node_id": "construction_machinery",
            "activity_type": "produce",
            "role": "工程机械生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦工股份主营业务", "quote": "主营业务:装载机,挖掘机和小型工程机械等工程机械产品..."}]
        },
        # sh_600816 建元信托
        {
            "exposure_id": "sh_600816_provide_trust_service",
            "company_id": "sh_600816",
            "node_id": "trust_service",
            "activity_type": "provide_service",
            "role": "信托服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "建元信托主营业务", "quote": "主要业务:金融信托业务"}]
        },
        # sh_600817 宇通重工（修正后）
        {
            "exposure_id": "sh_600817_produce_sanitation_equipment",
            "company_id": "sh_600817",
            "node_id": "sanitation_equipment",
            "activity_type": "produce",
            "role": "环卫设备生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宇通重工2025年年度报告", "quote": "公司主要业务涵盖环卫设备、矿用装备、基础工程机械三大业务板块"}]
        },
        {
            "exposure_id": "sh_600817_produce_construction_machinery",
            "company_id": "sh_600817",
            "node_id": "construction_machinery",
            "activity_type": "produce",
            "role": "工程机械(矿用装备/基础工程机械)生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宇通重工2025年年度报告", "quote": "主要产品包括多功能旋挖钻机、液压履带式强夯机、重负荷起重机、桥梁检测车等"}]
        },
        # sh_600818 ST中路
        {
            "exposure_id": "sh_600818_produce_bicycle",
            "company_id": "sh_600818",
            "node_id": "bicycle",
            "activity_type": "produce",
            "role": "自行车生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST中路主营业务", "quote": "自行车,康体设备"}]
        },
        {
            "exposure_id": "sh_600818_produce_fitness_equipment",
            "company_id": "sh_600818",
            "node_id": "fitness_equipment",
            "activity_type": "produce",
            "role": "康体设备生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST中路主营业务", "quote": "自行车,康体设备"}]
        },
        # sh_600819 耀皮玻璃
        {
            "exposure_id": "sh_600819_produce_float_glass",
            "company_id": "sh_600819",
            "node_id": "float_glass",
            "activity_type": "produce",
            "role": "浮法玻璃生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "耀皮玻璃主营业务", "quote": "主要产品:浮法玻璃,加工玻璃"}]
        },
        {
            "exposure_id": "sh_600819_produce_processed_glass",
            "company_id": "sh_600819",
            "node_id": "processed_glass",
            "activity_type": "produce",
            "role": "加工玻璃生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "耀皮玻璃主营业务", "quote": "主要产品:浮法玻璃,加工玻璃"}]
        },
        # sh_600820 隧道股份
        {
            "exposure_id": "sh_600820_operate_tunnel_engineering",
            "company_id": "sh_600820",
            "node_id": "tunnel_engineering",
            "activity_type": "operate",
            "role": "隧道工程施工运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "隧道股份主营业务", "quote": "投资,设计,施工,运营一体化的城市基础设施建设运营"}]
        },
        {
            "exposure_id": "sh_600820_operate_municipal_engineering",
            "company_id": "sh_600820",
            "node_id": "municipal_engineering",
            "activity_type": "operate",
            "role": "市政工程施工运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "隧道股份经营范围", "quote": "建筑业,土木工程建设项目总承包,隧道,市政,建筑,公路及桥梁,交通,消防,地基与基础..."}]
        },
        # sh_600821 金开新能（修正后）
        {
            "exposure_id": "sh_600821_operate_solar_power_generation",
            "company_id": "sh_600821",
            "node_id": "solar_power_generation",
            "activity_type": "operate",
            "role": "光伏发电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "金开新能2025年年报", "quote": "公司主营业务为新能源电力的开发,投资,建设及运营,目前主要包括光伏发电和风力发电两个板块"}]
        },
        {
            "exposure_id": "sh_600821_operate_wind_power_generation",
            "company_id": "sh_600821",
            "node_id": "wind_power_generation",
            "activity_type": "operate",
            "role": "风力发电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "金开新能2025年年报", "quote": "公司主营业务为新能源电力的开发,投资,建设及运营,目前主要包括光伏发电和风力发电两个板块"}]
        },
        {
            "exposure_id": "sh_600821_produce_electricity_power",
            "company_id": "sh_600821",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "金开新能2025年年报", "quote": "全年累计发电量84.32亿千瓦时"}]
        },
        # sh_600822 上海物贸
        {
            "exposure_id": "sh_600822_provide_trade_agent",
            "company_id": "sh_600822",
            "node_id": "trade_agent",
            "activity_type": "provide_service",
            "role": "生产资料贸易服务商（汽车/化工）",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海物贸主营业务", "quote": "主营业务:汽车贸易,化工等生产资料的批发与零售,以及有色金属平台交易"}]
        },
        {
            "exposure_id": "sh_600822_operate_nonferrous_metal_mining",
            "company_id": "sh_600822",
            "node_id": "nonferrous_metal_mining",
            "activity_type": "operate",
            "role": "有色金属交易平台运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海物贸主营业务", "quote": "主营业务:...以及有色金属平台交易"}]
        },
        # sh_600824 益民集团
        {
            "exposure_id": "sh_600824_operate_department_store",
            "company_id": "sh_600824",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "益民主营业务", "quote": "主要业务:百货零售业"}]
        },
        # sh_600825 新华传媒
        {
            "exposure_id": "sh_600825_provide_publishing_service",
            "company_id": "sh_600825",
            "node_id": "publishing_service",
            "activity_type": "provide_service",
            "role": "出版服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新华传媒主营业务", "quote": "主营业务:主要板块分为图书,音像制品,文教用品,报刊广告和其他"}]
        },
        {
            "exposure_id": "sh_600825_provide_book_publishing",
            "company_id": "sh_600825",
            "node_id": "book_publishing",
            "activity_type": "provide_service",
            "role": "图书出版服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新华传媒主营业务", "quote": "主营业务:主要板块分为图书,音像制品,文教用品,报刊广告和其他"}]
        },
        {
            "exposure_id": "sh_600825_provide_advertising_service",
            "company_id": "sh_600825",
            "node_id": "advertising_service",
            "activity_type": "provide_service",
            "role": "报刊广告服务商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新华传媒主营业务", "quote": "主营业务:主要板块分为图书,音像制品,文教用品,报刊广告和其他"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 104")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 104 submission completed.")
