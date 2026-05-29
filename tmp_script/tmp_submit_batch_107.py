#!/usr/bin/env python3
"""
Batch 107 Submission Script
Stock codes: 600851, 600853, 600854, 600855, 600857, 600858, 600859, 600860, 600861, 600862
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
    "batch_id": "batch_107_nodes",
    "task_description": "Batch 107:补充缺失的产业节点——长毛绒纺织、公路桥梁施工、安保服务、气体储运装备、人力资源服务、航空新材料",
    "nodes_to_upsert": [
        {
            "node_id": "plush_textile",
            "canonical_name_zh": "长毛绒纺织",
            "canonical_name_en": "plush textile",
            "aliases": ["长毛绒", "绒类织物", "毛绒面料"],
            "definition": "以起毛组织或割绒工艺在织物表面形成致密、丰满绒毛层的纺织面料，具有手感柔软、保暖性强、光泽柔和等特点，广泛用于玩具、服装、家居装饰等领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "海欣股份主营业务",
                    "quote": "长毛绒纺织,医药,金融投资等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "highway_bridge_construction",
            "canonical_name_zh": "公路桥梁施工",
            "canonical_name_en": "highway bridge construction",
            "aliases": ["路桥施工", "公路桥梁建设"],
            "definition": "按照工程设计要求，对公路、桥梁、隧道等交通基础设施进行土建施工、结构安装和路面铺设的工程建设服务，涵盖路基、路面、桥梁、涵洞、隧道、交通设施等分项工程。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "龙建股份主营业务",
                    "quote": "主要业务:公路桥梁施工建设"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "security_service",
            "canonical_name_zh": "安保服务",
            "canonical_name_en": "security service",
            "aliases": ["安防服务", "安全服务", "安保业务"],
            "definition": "为社会公共安全领域提供的专业化安全保护服务，包括视频监控系统、入侵报警系统、门禁控制系统、安保人员派遣、安全风险评估、大型活动安保等。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "航天长峰主营业务",
                    "quote": "主营业务为安保业务,医疗器械与工程服务业务以及电子信息业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "gas_storage_equipment",
            "canonical_name_zh": "气体储运装备",
            "canonical_name_en": "gas storage and transportation equipment",
            "aliases": ["气体储运设备", "储气装备", "气瓶"],
            "definition": "用于压缩气体、液化气体（如天然气、氢气、氧气、二氧化碳等）的储存、运输和配送的专用压力容器及配套设备，包括低温储罐、高压气瓶、长管拖车、液化气体罐车等。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "京城股份主营业务",
                    "quote": "气体储运装备业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "human_resource_service",
            "canonical_name_zh": "人力资源服务",
            "canonical_name_en": "human resource service",
            "aliases": ["HR服务", "人才服务", "劳务派遣"],
            "definition": "为企业或个人提供的人力资源管理外包服务，包括人才招聘、劳务派遣、薪酬管理、社保代理、培训发展、猎头服务、人力资源咨询等，帮助企业优化人力资源配置和管理效率。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "北京人力主营业务",
                    "quote": "职业中介活动;人力资源服务;薪酬管理服务;劳务服务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "aviation_new_material",
            "canonical_name_zh": "航空新材料",
            "canonical_name_en": "aviation new material",
            "aliases": ["航空先进材料", "航空复合材料"],
            "definition": "专门用于航空器制造的高性能结构材料和功能材料，包括碳纤维复合材料、高温合金、钛合金、特种陶瓷、隐身材料等，具有轻质、高强、耐高温、耐腐蚀等优异性能。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "中航高科主营业务",
                    "quote": "航空新材料,高端智能装备技术开发"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 107")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_107_business",
    "task_description": "Batch 107:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600851",
            "name_zh": "海欣股份",
            "aliases": ["上海海欣集团股份有限公司"],
            "stock_codes": ["600851.SH"],
            "description": "长毛绒纺织,医药,金融投资等",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 715,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600853",
            "name_zh": "龙建股份",
            "aliases": ["龙建路桥股份有限公司"],
            "stock_codes": ["600853.SH"],
            "description": "主要业务:公路桥梁施工建设",
            "country": "CN",
            "province": "黑龙江",
            "city": "哈尔滨市",
            "employee_count": 6174,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600854",
            "name_zh": "春兰股份",
            "aliases": ["江苏春兰制冷设备股份有限公司"],
            "stock_codes": ["600854.SH"],
            "description": "空调器",
            "country": "CN",
            "province": "江苏",
            "city": "泰州市",
            "employee_count": 98,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600855",
            "name_zh": "航天长峰",
            "aliases": ["北京航天长峰股份有限公司"],
            "stock_codes": ["600855.SH"],
            "description": "主营业务为安保业务,医疗器械与工程服务业务以及电子信息业务",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 1298,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600857",
            "name_zh": "宁波中百",
            "aliases": ["宁波中百股份有限公司"],
            "stock_codes": ["600857.SH"],
            "description": "商业,软件业务",
            "country": "CN",
            "province": "浙江",
            "city": "宁波市",
            "employee_count": 108,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600858",
            "name_zh": "银座股份",
            "aliases": ["银座集团股份有限公司"],
            "stock_codes": ["600858.SH"],
            "description": "主要业务:商品零售,供电,供汽",
            "country": "CN",
            "province": "山东",
            "city": "济南市",
            "employee_count": 8817,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600859",
            "name_zh": "王府井",
            "aliases": ["王府井集团股份有限公司"],
            "stock_codes": ["600859.SH"],
            "description": "主要业务:百货零售",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 11240,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600860",
            "name_zh": "京城股份",
            "aliases": ["北京京城机电股份有限公司"],
            "stock_codes": ["600860.SH"],
            "description": "气体储运装备业务",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 1348,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600861",
            "name_zh": "北京人力",
            "aliases": ["北京国际人力资本集团股份有限公司"],
            "stock_codes": ["600861.SH"],
            "description": "人力资源服务",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 3721,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600862",
            "name_zh": "中航高科",
            "aliases": ["中航航空高科技股份有限公司"],
            "stock_codes": ["600862.SH"],
            "description": "航空新材料,高端智能装备,轨道交通,汽车,医疗器械,装备制造,房地产,创新创业投资等",
            "country": "CN",
            "province": "江苏",
            "city": "南通市",
            "employee_count": 1056,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600851 海欣股份
        {
            "exposure_id": "sh_600851_produce_plush_textile",
            "company_id": "sh_600851",
            "node_id": "plush_textile",
            "activity_type": "produce",
            "role": "长毛绒纺织生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "海欣股份主营业务", "quote": "长毛绒纺织,医药,金融投资等"}]
        },
        {
            "exposure_id": "sh_600851_produce_pharmaceutical_manufacturing",
            "company_id": "sh_600851",
            "node_id": "pharmaceutical_manufacturing",
            "activity_type": "produce",
            "role": "医药产品生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "海欣股份主营业务", "quote": "长毛绒纺织,医药,金融投资等"}]
        },
        {
            "exposure_id": "sh_600851_provide_financial_investment",
            "company_id": "sh_600851",
            "node_id": "financial_investment",
            "activity_type": "provide_service",
            "role": "金融投资服务商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "海欣股份主营业务", "quote": "长毛绒纺织,医药,金融投资等"}]
        },
        # sh_600853 龙建股份
        {
            "exposure_id": "sh_600853_provide_highway_bridge_construction",
            "company_id": "sh_600853",
            "node_id": "highway_bridge_construction",
            "activity_type": "provide_service",
            "role": "公路桥梁施工服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "龙建股份主营业务", "quote": "主要业务:公路桥梁施工建设"}]
        },
        {
            "exposure_id": "sh_600853_provide_bridge_construction",
            "company_id": "sh_600853",
            "node_id": "bridge_construction",
            "activity_type": "provide_service",
            "role": "桥梁建设服务商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "龙建股份主营业务", "quote": "主要业务:公路桥梁施工建设"}]
        },
        # sh_600854 春兰股份
        {
            "exposure_id": "sh_600854_produce_air_conditioner",
            "company_id": "sh_600854",
            "node_id": "air_conditioner",
            "activity_type": "produce",
            "role": "空调器生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "春兰股份主营业务", "quote": "空调器"}]
        },
        {
            "exposure_id": "sh_600854_produce_compressor",
            "company_id": "sh_600854",
            "node_id": "compressor",
            "activity_type": "produce",
            "role": "压缩机生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "春兰股份主营业务", "quote": "生产销售空调等制冷产品,空调用红外线遥控,专用集成电路,电子原器件,制冷压缩机等动力机械"}]
        },
        # sh_600855 航天长峰
        {
            "exposure_id": "sh_600855_provide_security_service",
            "company_id": "sh_600855",
            "node_id": "security_service",
            "activity_type": "provide_service",
            "role": "安保服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天长峰主营业务", "quote": "主营业务为安保业务,医疗器械与工程服务业务以及电子信息业务"}]
        },
        {
            "exposure_id": "sh_600855_produce_medical_device",
            "company_id": "sh_600855",
            "node_id": "medical_device",
            "activity_type": "produce",
            "role": "医疗器械生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天长峰主营业务", "quote": "主营业务为安保业务,医疗器械与工程服务业务以及电子信息业务"}]
        },
        {
            "exposure_id": "sh_600855_produce_electronic_information",
            "company_id": "sh_600855",
            "node_id": "electronic_information",
            "activity_type": "produce",
            "role": "电子信息产品生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天长峰主营业务", "quote": "主营业务为安保业务,医疗器械与工程服务业务以及电子信息业务"}]
        },
        # sh_600857 宁波中百
        {
            "exposure_id": "sh_600857_operate_department_store",
            "company_id": "sh_600857",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宁波中百主营业务", "quote": "商业,软件业务"}]
        },
        {
            "exposure_id": "sh_600857_provide_software_development_service",
            "company_id": "sh_600857",
            "node_id": "software_development_service",
            "activity_type": "provide_service",
            "role": "软件服务商",
            "weight": 0.5,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "宁波中百主营业务", "quote": "商业,软件业务"}]
        },
        # sh_600858 银座股份
        {
            "exposure_id": "sh_600858_operate_department_store",
            "company_id": "sh_600858",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "商品零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "银座股份主营业务", "quote": "主要业务:商品零售,供电,供汽"}]
        },
        {
            "exposure_id": "sh_600858_produce_electricity_power",
            "company_id": "sh_600858",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "供电服务商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "银座股份主营业务", "quote": "主要业务:商品零售,供电,供汽"}]
        },
        {
            "exposure_id": "sh_600858_produce_steam_supply",
            "company_id": "sh_600858",
            "node_id": "steam_supply",
            "activity_type": "produce",
            "role": "供汽服务商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "银座股份主营业务", "quote": "主要业务:商品零售,供电,供汽"}]
        },
        # sh_600859 王府井
        {
            "exposure_id": "sh_600859_operate_department_store",
            "company_id": "sh_600859",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "王府井主营业务", "quote": "主要业务:百货零售"}]
        },
        # sh_600860 京城股份
        {
            "exposure_id": "sh_600860_produce_gas_storage_equipment",
            "company_id": "sh_600860",
            "node_id": "gas_storage_equipment",
            "activity_type": "produce",
            "role": "气体储运装备生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "京城股份主营业务", "quote": "气体储运装备业务"}]
        },
        # sh_600861 北京人力
        {
            "exposure_id": "sh_600861_provide_human_resource_service",
            "company_id": "sh_600861",
            "node_id": "human_resource_service",
            "activity_type": "provide_service",
            "role": "人力资源服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "北京人力主营业务", "quote": "职业中介活动;人力资源服务;薪酬管理服务;劳务服务"}]
        },
        # sh_600862 中航高科
        {
            "exposure_id": "sh_600862_produce_aviation_new_material",
            "company_id": "sh_600862",
            "node_id": "aviation_new_material",
            "activity_type": "produce",
            "role": "航空新材料生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中航高科主营业务", "quote": "航空新材料,高端智能装备技术开发"}]
        },
        {
            "exposure_id": "sh_600862_produce_intelligent_equipment",
            "company_id": "sh_600862",
            "node_id": "intelligent_equipment",
            "activity_type": "produce",
            "role": "高端智能装备生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中航高科主营业务", "quote": "航空新材料,高端智能装备技术开发,及其航空,轨道交通,汽车,医疗器械,装备制造等领域相关产品的研发,制造,销售及技术服务"}]
        },
        {
            "exposure_id": "sh_600862_produce_medical_device",
            "company_id": "sh_600862",
            "node_id": "medical_device",
            "activity_type": "produce",
            "role": "医疗器械生产商",
            "weight": 0.5,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "中航高科主营业务", "quote": "航空新材料,高端智能装备技术开发,及其航空,轨道交通,汽车,医疗器械,装备制造等领域相关产品的研发,制造,销售及技术服务"}]
        },
        {
            "exposure_id": "sh_600862_operate_real_estate_development",
            "company_id": "sh_600862",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 0.4,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "中航高科主营业务", "quote": "房地产,创新创业投资等"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 107")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 107 submission completed.")
