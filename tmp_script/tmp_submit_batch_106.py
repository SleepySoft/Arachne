#!/usr/bin/env python3
"""
Batch 106 Submission Script
Stock codes: 600839, 600841, 600843, 600844, 600845, 600846, 600847, 600848, 601607, 600850
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
    "batch_id": "batch_106_nodes",
    "task_description": "Batch 106:补充缺失的产业节点——压缩机、缝纫机、煤化工产品、服务外包、铅蓄电池、智能建筑",
    "nodes_to_upsert": [
        {
            "node_id": "compressor",
            "canonical_name_zh": "压缩机",
            "canonical_name_en": "compressor",
            "aliases": ["压气机", "空气压缩机", "制冷压缩机"],
            "definition": "将低压气体提升为高压气体的流体机械，通过对气体做功使其压力升高、体积缩小，广泛应用于制冷空调、石油化工、天然气输送、气动工具等领域。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "四川长虹主营业务",
                    "quote": "公司主要从事电视机,冰箱,空调,压缩机,视听产品,电池,手机等产品的生产销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "sewing_machine",
            "canonical_name_zh": "缝纫机",
            "canonical_name_en": "sewing machine",
            "aliases": ["缝衣机", "裁缝机"],
            "definition": "用一根或多根缝纫线，在缝料上形成一种或多种线迹，使一层或多层缝料交织或缝合起来的机器，包括家用缝纫机和工业缝纫机两大类。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "上工申贝主营业务",
                    "quote": "主要产品:缝制设备包括工业缝纫机,家用缝纫机及特种用途工业定制机器等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "coal_chemical_product",
            "canonical_name_zh": "煤化工产品",
            "canonical_name_en": "coal chemical product",
            "aliases": ["煤化产品", "煤炭化工产品"],
            "definition": "以煤炭为原料，通过化学加工方法（气化、液化、焦化、干馏等）转化生产的化学品和能源产品，包括煤制甲醇、煤制烯烃、煤制乙二醇、煤焦油、焦炭及合成氨等。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "金煤科技主营业务",
                    "quote": "主要从事煤化工产品的生产"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "service_outsourcing",
            "canonical_name_zh": "服务外包",
            "canonical_name_en": "service outsourcing",
            "aliases": ["业务流程外包", "ITO", "BPO"],
            "definition": "企业将非核心业务或特定服务流程委托给外部专业服务提供商完成的商业模式，包括信息技术外包（ITO）、业务流程外包（BPO）和知识流程外包（KPO）等。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "宝信软件主营业务",
                    "quote": "主要产品和提供的劳务为软件开发,服务外包,系统集成,工程设计及智能交通"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "lead_acid_battery",
            "canonical_name_zh": "铅蓄电池",
            "canonical_name_en": "lead acid battery",
            "aliases": ["铅酸电池", "铅酸蓄电池"],
            "definition": "以二氧化铅为正极活性物质、海绵状铅为负极活性物质、稀硫酸为电解液的二次电池，具有技术成熟、成本低廉、安全性好、大电流放电能力强等特点，广泛应用于汽车启动、电动自行车、通信基站备用电源等领域。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "万里股份主营业务",
                    "quote": "公司主营业务一直为铅蓄电池的研发,生产,销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "intelligent_building",
            "canonical_name_zh": "智能建筑",
            "canonical_name_en": "intelligent building",
            "aliases": ["智慧建筑", "楼宇智能化"],
            "definition": "通过将建筑物的结构、系统、服务和管理根据用户需求进行最优化组合，利用计算机技术、通信技术、控制技术等对建筑设备进行自动化监控和管理，从而为用户提供一个高效、舒适、便利的人性化建筑环境。",
            "entity_type": "system",
            "evidence": [
                {
                    "source_title": "电科数字主营业务",
                    "quote": "主营业务包括面向IT基础设施的系统集成和专业服务,软件和行业解决方案,IT产品增值销售,智能建筑与机房等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 106")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_106_business",
    "task_description": "Batch 106:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600839",
            "name_zh": "四川长虹",
            "aliases": ["四川长虹电器股份有限公司"],
            "stock_codes": ["600839.SH"],
            "description": "公司主要从事电视机,冰箱,空调,压缩机,视听产品,电池,手机等产品的生产销售,IT产品的销售以及房地产开发等生产经营活动",
            "country": "CN",
            "province": "四川",
            "city": "绵阳市",
            "employee_count": 45376,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600841",
            "name_zh": "动力新科",
            "aliases": ["上海新动力汽车科技股份有限公司"],
            "stock_codes": ["600841.SH"],
            "description": "主营业务:柴油机及其配件的生产及销售",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 1628,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600843",
            "name_zh": "上工申贝",
            "aliases": ["上工申贝(集团)股份有限公司"],
            "stock_codes": ["600843.SH"],
            "description": "主要产品:缝制设备包括工业缝纫机,家用缝纫机及特种用途工业定制机器等",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 4861,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600844",
            "name_zh": "金煤科技",
            "aliases": ["内蒙古金煤化工科技股份有限公司"],
            "stock_codes": ["600844.SH"],
            "description": "主要从事煤化工产品的生产",
            "country": "CN",
            "province": "内蒙古",
            "city": "呼和浩特市",
            "employee_count": 1106,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600845",
            "name_zh": "宝信软件",
            "aliases": ["上海宝信软件股份有限公司"],
            "stock_codes": ["600845.SH"],
            "description": "主要从事计算机,自动化,网络通讯系统及软硬件产品的研究,设计,开发,制造,集成及相应的外包,维修,咨询等服务",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 6060,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600846",
            "name_zh": "同济科技",
            "aliases": ["上海同济科技实业股份有限公司"],
            "stock_codes": ["600846.SH"],
            "description": "商品房,建筑施工",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 3334,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600847",
            "name_zh": "万里股份",
            "aliases": ["重庆万里新能源股份有限公司"],
            "stock_codes": ["600847.SH"],
            "description": "公司主营业务一直为铅蓄电池的研发,生产,销售",
            "country": "CN",
            "province": "重庆",
            "city": "重庆市",
            "employee_count": 368,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600848",
            "name_zh": "上海临港",
            "aliases": ["上海临港控股股份有限公司"],
            "stock_codes": ["600848.SH"],
            "description": "主要业务:科技产业园区开发建设,运营服务",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 1009,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_601607",
            "name_zh": "上海医药",
            "aliases": ["上海医药集团股份有限公司"],
            "stock_codes": ["601607.SH"],
            "description": "医药.原料药和各种剂型的医药产品,保健品,医疗器械及相关产品的研发,制造和销售",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 49608,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600850",
            "name_zh": "电科数字",
            "aliases": ["中电科数字技术股份有限公司"],
            "stock_codes": ["600850.SH"],
            "description": "主营业务包括面向IT基础设施的系统集成和专业服务,软件和行业解决方案,IT产品增值销售,智能建筑与机房等",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 4046,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600839 四川长虹
        {
            "exposure_id": "sh_600839_produce_tv_set",
            "company_id": "sh_600839",
            "node_id": "tv_set",
            "activity_type": "produce",
            "role": "电视机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_produce_refrigerator",
            "company_id": "sh_600839",
            "node_id": "refrigerator",
            "activity_type": "produce",
            "role": "冰箱生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_produce_air_conditioner",
            "company_id": "sh_600839",
            "node_id": "air_conditioner",
            "activity_type": "produce",
            "role": "空调生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_produce_compressor",
            "company_id": "sh_600839",
            "node_id": "compressor",
            "activity_type": "produce",
            "role": "压缩机生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机,视听产品,电池,手机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_produce_battery",
            "company_id": "sh_600839",
            "node_id": "battery",
            "activity_type": "produce",
            "role": "电池生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机,视听产品,电池,手机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_produce_mobile_phone",
            "company_id": "sh_600839",
            "node_id": "mobile_phone",
            "activity_type": "produce",
            "role": "手机生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "公司主要从事电视机,冰箱,空调,压缩机,视听产品,电池,手机等产品的生产销售"}]
        },
        {
            "exposure_id": "sh_600839_operate_real_estate_development",
            "company_id": "sh_600839",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 0.4,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "四川长虹主营业务", "quote": "IT产品的销售以及房地产开发等生产经营活动"}]
        },
        # sh_600841 动力新科
        {
            "exposure_id": "sh_600841_produce_diesel_engine",
            "company_id": "sh_600841",
            "node_id": "diesel_engine",
            "activity_type": "produce",
            "role": "柴油机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "动力新科主营业务", "quote": "主营业务:柴油机及其配件的生产及销售"}]
        },
        # sh_600843 上工申贝
        {
            "exposure_id": "sh_600843_produce_industrial_sewing_machine",
            "company_id": "sh_600843",
            "node_id": "industrial_sewing_machine",
            "activity_type": "produce",
            "role": "工业缝纫机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上工申贝主营业务", "quote": "主要产品:缝制设备包括工业缝纫机,家用缝纫机及特种用途工业定制机器等"}]
        },
        {
            "exposure_id": "sh_600843_produce_sewing_machine",
            "company_id": "sh_600843",
            "node_id": "sewing_machine",
            "activity_type": "produce",
            "role": "家用缝纫机生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上工申贝主营业务", "quote": "主要产品:缝制设备包括工业缝纫机,家用缝纫机及特种用途工业定制机器等"}]
        },
        # sh_600844 金煤科技
        {
            "exposure_id": "sh_600844_produce_coal_chemical_product",
            "company_id": "sh_600844",
            "node_id": "coal_chemical_product",
            "activity_type": "produce",
            "role": "煤化工产品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "金煤科技主营业务", "quote": "主要从事煤化工产品的生产"}]
        },
        # sh_600845 宝信软件
        {
            "exposure_id": "sh_600845_provide_software_development_service",
            "company_id": "sh_600845",
            "node_id": "software_development_service",
            "activity_type": "provide_service",
            "role": "软件开发服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宝信软件主营业务", "quote": "主要从事计算机,自动化,网络通讯系统及软硬件产品的研究,设计,开发,制造,集成及相应的外包,维修,咨询等服务"}]
        },
        {
            "exposure_id": "sh_600845_provide_service_outsourcing",
            "company_id": "sh_600845",
            "node_id": "service_outsourcing",
            "activity_type": "provide_service",
            "role": "服务外包商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宝信软件主营业务", "quote": "主要产品和提供的劳务为软件开发,服务外包,系统集成,工程设计及智能交通"}]
        },
        {
            "exposure_id": "sh_600845_provide_information_system_integration",
            "company_id": "sh_600845",
            "node_id": "information_system_integration",
            "activity_type": "provide_service",
            "role": "系统集成服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宝信软件主营业务", "quote": "主要从事计算机,自动化,网络通讯系统及软硬件产品的研究,设计,开发,制造,集成"}]
        },
        {
            "exposure_id": "sh_600845_provide_intelligent_transport_system",
            "company_id": "sh_600845",
            "node_id": "intelligent_transport_system",
            "activity_type": "provide_service",
            "role": "智能交通解决方案提供商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宝信软件主营业务", "quote": "主要产品和提供的劳务为软件开发,服务外包,系统集成,工程设计及智能交通"}]
        },
        # sh_600846 同济科技
        {
            "exposure_id": "sh_600846_operate_real_estate_development",
            "company_id": "sh_600846",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "同济科技主营业务", "quote": "商品房,建筑施工"}]
        },
        {
            "exposure_id": "sh_600846_provide_construction_engineering",
            "company_id": "sh_600846",
            "node_id": "construction_engineering",
            "activity_type": "provide_service",
            "role": "建筑施工服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "同济科技主营业务", "quote": "商品房,建筑施工"}]
        },
        # sh_600847 万里股份
        {
            "exposure_id": "sh_600847_produce_lead_acid_battery",
            "company_id": "sh_600847",
            "node_id": "lead_acid_battery",
            "activity_type": "produce",
            "role": "铅蓄电池生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "万里股份主营业务", "quote": "公司主营业务一直为铅蓄电池的研发,生产,销售"}]
        },
        # sh_600848 上海临港
        {
            "exposure_id": "sh_600848_operate_tech_park_operation_service",
            "company_id": "sh_600848",
            "node_id": "tech_park_operation_service",
            "activity_type": "operate",
            "role": "科技产业园区运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海临港主营业务", "quote": "主要业务:科技产业园区开发建设,运营服务"}]
        },
        {
            "exposure_id": "sh_600848_operate_property_rental",
            "company_id": "sh_600848",
            "node_id": "property_rental",
            "activity_type": "operate",
            "role": "房屋租赁运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海临港主营业务", "quote": "自有房屋租赁"}]
        },
        # sh_601607 上海医药
        {
            "exposure_id": "sh_601607_produce_pharmaceutical_manufacturing",
            "company_id": "sh_601607",
            "node_id": "pharmaceutical_manufacturing",
            "activity_type": "produce",
            "role": "医药产品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海医药主营业务", "quote": "原料药和各种剂型的医药产品,保健品,医疗器械及相关产品的研发,制造和销售"}]
        },
        {
            "exposure_id": "sh_601607_provide_pharmaceutical_wholesale",
            "company_id": "sh_601607",
            "node_id": "pharmaceutical_wholesale",
            "activity_type": "provide_service",
            "role": "医药批发服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海医药主营业务", "quote": "原料药和各种剂型的医药产品...制造和销售"}]
        },
        {
            "exposure_id": "sh_601607_provide_pharmaceutical_retail",
            "company_id": "sh_601607",
            "node_id": "pharmaceutical_retail",
            "activity_type": "provide_service",
            "role": "医药零售服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海医药主营业务", "quote": "原料药和各种剂型的医药产品...制造和销售"}]
        },
        {
            "exposure_id": "sh_601607_produce_medical_device",
            "company_id": "sh_601607",
            "node_id": "medical_device",
            "activity_type": "produce",
            "role": "医疗器械生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海医药主营业务", "quote": "医疗器械及相关产品的研发,制造和销售"}]
        },
        # sh_600850 电科数字
        {
            "exposure_id": "sh_600850_provide_information_system_integration",
            "company_id": "sh_600850",
            "node_id": "information_system_integration",
            "activity_type": "provide_service",
            "role": "系统集成服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电科数字主营业务", "quote": "主营业务包括面向IT基础设施的系统集成和专业服务"}]
        },
        {
            "exposure_id": "sh_600850_provide_software_development_service",
            "company_id": "sh_600850",
            "node_id": "software_development_service",
            "activity_type": "provide_service",
            "role": "软件解决方案提供商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电科数字主营业务", "quote": "软件和行业解决方案"}]
        },
        {
            "exposure_id": "sh_600850_provide_intelligent_building",
            "company_id": "sh_600850",
            "node_id": "intelligent_building",
            "activity_type": "provide_service",
            "role": "智能建筑服务商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电科数字主营业务", "quote": "智能建筑与机房等"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 106")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 106 submission completed.")
