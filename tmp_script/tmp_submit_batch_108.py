#!/usr/bin/env python3
"""
Batch 108 Submission Script
Stock codes: 600863, 600864, 600865, 600866, 600867, 600868, 600869, 600871, 600872, 600873
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
    "batch_id": "batch_108_nodes",
    "task_description": "Batch 108:补充缺失的产业节点——核苷酸、重组人胰岛素、大输液制品、碳纤维复合芯导线、石油工程技术服务、氨基酸、有机肥",
    "nodes_to_upsert": [
        {
            "node_id": "nucleotide",
            "canonical_name_zh": "核苷酸",
            "canonical_name_en": "nucleotide",
            "aliases": ["呈味核苷酸", "核糖核苷酸", "脱氧核苷酸"],
            "definition": "由含氮碱基、五碳糖和磷酸基团组成的生物小分子，是核酸（DNA和RNA）的基本组成单位，在食品工业中用作呈味剂（呈味核苷酸二钠，I+G），可显著增强鲜味。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "星湖科技主营业务",
                    "quote": "肌苷,利巴韦林,脯氨酸,腺苷及其他,呈味核苷酸,味精,酱油"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "recombinant_human_insulin",
            "canonical_name_zh": "重组人胰岛素",
            "canonical_name_en": "recombinant human insulin",
            "aliases": ["人胰岛素", "重组胰岛素", "生物合成人胰岛素"],
            "definition": "利用基因重组技术，将人胰岛素基因导入微生物（如大肠杆菌或酵母菌）中表达生产的与人自身胰岛素氨基酸序列完全一致的蛋白质激素，用于治疗糖尿病。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "通化东宝主营业务",
                    "quote": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "infusion_solution",
            "canonical_name_zh": "大输液制品",
            "canonical_name_en": "infusion solution",
            "aliases": ["输液制剂", "静脉输液", "大容量注射剂"],
            "definition": "指容量不小于50ml并直接由静脉滴注输入体内的无菌液体制剂，包括葡萄糖注射液、氯化钠注射液、氨基酸注射液、脂肪乳注射液及各类复方电解质输液等，是临床治疗中用量最大的药品剂型之一。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "通化东宝主营业务",
                    "quote": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "carbon_fiber_composite_conductor",
            "canonical_name_zh": "碳纤维复合芯导线",
            "canonical_name_en": "carbon fiber composite core conductor",
            "aliases": ["碳纤维导线", "复合芯导线", "ACCC导线"],
            "definition": "以碳纤维复合材料棒作为芯体、外层绞合铝线的架空输电导线，具有强度高、重量轻、导电率高、弧垂小、耐高温等优点，可大幅提高输电线路的输送容量并降低线路损耗。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "远东股份主营业务",
                    "quote": "主要产品:电力电缆,电气装备用电线电缆,裸导线,碳纤维复合芯软铝导线等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "petroleum_engineering_service",
            "canonical_name_zh": "石油工程技术服务",
            "canonical_name_en": "petroleum engineering service",
            "aliases": ["油气工程服务", "油服", "石油工程服务"],
            "definition": "为油气勘探、开发、生产全过程提供的技术服务和工程施工服务，包括地球物理勘探、钻井工程、测井录井、固井完井、压裂酸化、油气田地面建设、油气生产运维等。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "石化油服主营业务",
                    "quote": "油气勘探开发工程施工与技术服务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "amino_acid",
            "canonical_name_zh": "氨基酸",
            "canonical_name_en": "amino acid",
            "aliases": ["AA", "氨基羧酸"],
            "definition": "含有氨基和羧基的一类有机化合物，是构成蛋白质的基本单位，在食品工业中用作营养强化剂和鲜味剂（如谷氨酸钠），在饲料工业中作为添加剂，在医药领域用于合成药物和输液制剂。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "梅花生物主营业务",
                    "quote": "味精,氨基酸,有机肥等生物发酵产品的生产及销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "organic_fertilizer",
            "canonical_name_zh": "有机肥",
            "canonical_name_en": "organic fertilizer",
            "aliases": ["有机肥料", "生物有机肥"],
            "definition": "主要来源于植物和（或）动物，施于土壤以提供植物营养为其主要功能的含碳物料，经生物物质、动植物废弃物、植物残体加工而来，含有丰富的有机质和多种营养元素，能改善土壤结构、提高土壤肥力。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "梅花生物主营业务",
                    "quote": "味精,氨基酸,有机肥等生物发酵产品的生产及销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": []
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 108")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_108_business",
    "task_description": "Batch 108:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600863",
            "name_zh": "华能蒙电",
            "aliases": ["内蒙古蒙电华能热电股份有限公司"],
            "stock_codes": ["600863.SH"],
            "description": "电力,热力.火力发电,供应,蒸汽,热水的生产,供应,销售,维护和管理;风力发电以及其他新能源发电和供应",
            "country": "CN",
            "province": "内蒙古",
            "city": "呼和浩特市",
            "employee_count": 5544,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600864",
            "name_zh": "哈投股份",
            "aliases": ["哈尔滨哈投投资股份有限公司"],
            "stock_codes": ["600864.SH"],
            "description": "主营业务:热电业务和证券业务",
            "country": "CN",
            "province": "黑龙江",
            "city": "哈尔滨市",
            "employee_count": 3985,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600865",
            "name_zh": "百大集团",
            "aliases": ["百大集团股份有限公司"],
            "stock_codes": ["600865.SH"],
            "description": "百货,旅游服务",
            "country": "CN",
            "province": "浙江",
            "city": "杭州市",
            "employee_count": 112,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600866",
            "name_zh": "星湖科技",
            "aliases": ["广东肇庆星湖生物科技股份有限公司"],
            "stock_codes": ["600866.SH"],
            "description": "肌苷,利巴韦林,脯氨酸,腺苷及其他,呈味核苷酸,味精,酱油",
            "country": "CN",
            "province": "广东",
            "city": "肇庆市",
            "employee_count": 9293,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600867",
            "name_zh": "通化东宝",
            "aliases": ["通化东宝药业股份有限公司"],
            "stock_codes": ["600867.SH"],
            "description": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等",
            "country": "CN",
            "province": "吉林",
            "city": "通化市",
            "employee_count": 3410,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600868",
            "name_zh": "梅雁吉祥",
            "aliases": ["广东梅雁吉祥水电股份有限公司"],
            "stock_codes": ["600868.SH"],
            "description": "主营业务是电力生产,生产制造加工业",
            "country": "CN",
            "province": "广东",
            "city": "梅州市",
            "employee_count": 1044,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600869",
            "name_zh": "远东股份",
            "aliases": ["远东智慧能源股份有限公司"],
            "stock_codes": ["600869.SH"],
            "description": "主要产品:电力电缆,电气装备用电线电缆,裸导线,碳纤维复合芯软铝导线等",
            "country": "CN",
            "province": "青海",
            "city": "西宁市",
            "employee_count": 8008,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600871",
            "name_zh": "石化油服",
            "aliases": ["中石化石油工程技术服务股份有限公司"],
            "stock_codes": ["600871.SH"],
            "description": "油气勘探开发工程施工与技术服务",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 57076,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600872",
            "name_zh": "中炬高新",
            "aliases": ["中炬高新技术实业(集团)股份有限公司"],
            "stock_codes": ["600872.SH"],
            "description": "主要以调味品,汽车配件,房地产及园区服务为主导",
            "country": "CN",
            "province": "广东",
            "city": "中山市",
            "employee_count": 3910,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600873",
            "name_zh": "梅花生物",
            "aliases": ["梅花生物科技集团股份有限公司"],
            "stock_codes": ["600873.SH"],
            "description": "味精,氨基酸,有机肥等生物发酵产品的生产及销售",
            "country": "CN",
            "province": "西藏",
            "city": "拉萨市",
            "employee_count": 12858,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600863 华能蒙电
        {
            "exposure_id": "sh_600863_operate_thermal_power_generation",
            "company_id": "sh_600863",
            "node_id": "thermal_power_generation",
            "activity_type": "operate",
            "role": "火力发电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华能蒙电主营业务", "quote": "火力发电,供应,蒸汽,热水的生产,供应,销售,维护和管理"}]
        },
        {
            "exposure_id": "sh_600863_operate_wind_power_generation",
            "company_id": "sh_600863",
            "node_id": "wind_power_generation",
            "activity_type": "operate",
            "role": "风力发电运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华能蒙电主营业务", "quote": "风力发电以及其他新能源发电和供应"}]
        },
        {
            "exposure_id": "sh_600863_provide_heat_supply",
            "company_id": "sh_600863",
            "node_id": "heat_supply",
            "activity_type": "provide_service",
            "role": "热力供应服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华能蒙电主营业务", "quote": "火力发电,供应,蒸汽,热水的生产,供应,销售,维护和管理"}]
        },
        {
            "exposure_id": "sh_600863_procure_coal",
            "company_id": "sh_600863",
            "node_id": "coal",
            "activity_type": "procure",
            "role": "煤炭采购方",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "华能蒙电主营业务", "quote": "对煤炭,铁路及配套基础设施项目的投资"}]
        },
        # sh_600864 哈投股份
        {
            "exposure_id": "sh_600864_operate_thermal_power_generation",
            "company_id": "sh_600864",
            "node_id": "thermal_power_generation",
            "activity_type": "operate",
            "role": "热电业务运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "哈投股份主营业务", "quote": "主营业务:热电业务和证券业务"}]
        },
        {
            "exposure_id": "sh_600864_provide_securities_brokerage",
            "company_id": "sh_600864",
            "node_id": "securities_brokerage",
            "activity_type": "provide_service",
            "role": "证券业务服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "哈投股份主营业务", "quote": "主营业务:热电业务和证券业务"}]
        },
        # sh_600865 百大集团
        {
            "exposure_id": "sh_600865_operate_department_store",
            "company_id": "sh_600865",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "百大集团主营业务", "quote": "百货,旅游服务"}]
        },
        {
            "exposure_id": "sh_600865_provide_tourism_service",
            "company_id": "sh_600865",
            "node_id": "tourism_service",
            "activity_type": "provide_service",
            "role": "旅游服务商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "百大集团主营业务", "quote": "百货,旅游服务"}]
        },
        # sh_600866 星湖科技
        {
            "exposure_id": "sh_600866_produce_nucleotide",
            "company_id": "sh_600866",
            "node_id": "nucleotide",
            "activity_type": "produce",
            "role": "核苷酸生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "星湖科技主营业务", "quote": "肌苷,利巴韦林,脯氨酸,腺苷及其他,呈味核苷酸,味精,酱油"}]
        },
        {
            "exposure_id": "sh_600866_produce_monosodium_glutamate",
            "company_id": "sh_600866",
            "node_id": "monosodium_glutamate",
            "activity_type": "produce",
            "role": "味精生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "星湖科技主营业务", "quote": "肌苷,利巴韦林,脯氨酸,腺苷及其他,呈味核苷酸,味精,酱油"}]
        },
        {
            "exposure_id": "sh_600866_produce_soy_sauce",
            "company_id": "sh_600866",
            "node_id": "soy_sauce",
            "activity_type": "produce",
            "role": "酱油生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "星湖科技主营业务", "quote": "肌苷,利巴韦林,脯氨酸,腺苷及其他,呈味核苷酸,味精,酱油"}]
        },
        {
            "exposure_id": "sh_600866_produce_pharmaceutical_raw_material",
            "company_id": "sh_600866",
            "node_id": "pharmaceutical_raw_material",
            "activity_type": "produce",
            "role": "医药原料药生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "星湖科技主营业务", "quote": "肌苷,利巴韦林,脯氨酸,腺苷"}]
        },
        # sh_600867 通化东宝
        {
            "exposure_id": "sh_600867_produce_recombinant_human_insulin",
            "company_id": "sh_600867",
            "node_id": "recombinant_human_insulin",
            "activity_type": "produce",
            "role": "重组人胰岛素生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通化东宝主营业务", "quote": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等"}]
        },
        {
            "exposure_id": "sh_600867_produce_infusion_solution",
            "company_id": "sh_600867",
            "node_id": "infusion_solution",
            "activity_type": "produce",
            "role": "大输液制品生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通化东宝主营业务", "quote": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等"}]
        },
        {
            "exposure_id": "sh_600867_produce_chinese_patent_medicine",
            "company_id": "sh_600867",
            "node_id": "chinese_patent_medicine",
            "activity_type": "produce",
            "role": "中成药生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "通化东宝主营业务", "quote": "主要产品为重组人胰岛素冻干粉及注射液,大输液制品,镇脑宁胶囊,东宝甘泰片,塑钢窗等"}]
        },
        # sh_600868 梅雁吉祥
        {
            "exposure_id": "sh_600868_produce_electricity_power",
            "company_id": "sh_600868",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "梅雁吉祥主营业务", "quote": "主营业务是电力生产,生产制造加工业"}]
        },
        {
            "exposure_id": "sh_600868_provide_manufacturing",
            "company_id": "sh_600868",
            "node_id": "manufacturing",
            "activity_type": "provide_service",
            "role": "制造业加工商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "梅雁吉祥主营业务", "quote": "主营业务是电力生产,生产制造加工业"}]
        },
        # sh_600869 远东股份
        {
            "exposure_id": "sh_600869_produce_power_cable",
            "company_id": "sh_600869",
            "node_id": "power_cable",
            "activity_type": "produce",
            "role": "电力电缆生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "远东股份主营业务", "quote": "主要产品:电力电缆,电气装备用电线电缆,裸导线,碳纤维复合芯软铝导线等"}]
        },
        {
            "exposure_id": "sh_600869_produce_wire_cable",
            "company_id": "sh_600869",
            "node_id": "wire_cable",
            "activity_type": "produce",
            "role": "电线电缆生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "远东股份主营业务", "quote": "主要产品:电力电缆,电气装备用电线电缆,裸导线,碳纤维复合芯软铝导线等"}]
        },
        {
            "exposure_id": "sh_600869_produce_carbon_fiber_composite_conductor",
            "company_id": "sh_600869",
            "node_id": "carbon_fiber_composite_conductor",
            "activity_type": "produce",
            "role": "碳纤维复合芯导线生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "远东股份主营业务", "quote": "主要产品:电力电缆,电气装备用电线电缆,裸导线,碳纤维复合芯软铝导线等"}]
        },
        # sh_600871 石化油服
        {
            "exposure_id": "sh_600871_provide_petroleum_exploration",
            "company_id": "sh_600871",
            "node_id": "petroleum_exploration",
            "activity_type": "provide_service",
            "role": "油气勘探服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "石化油服主营业务", "quote": "油气勘探开发工程施工与技术服务"}]
        },
        {
            "exposure_id": "sh_600871_provide_petroleum_engineering_service",
            "company_id": "sh_600871",
            "node_id": "petroleum_engineering_service",
            "activity_type": "provide_service",
            "role": "石油工程技术服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "石化油服主营业务", "quote": "油气勘探开发工程施工与技术服务"}]
        },
        # sh_600872 中炬高新
        {
            "exposure_id": "sh_600872_produce_food_condiment",
            "company_id": "sh_600872",
            "node_id": "food_condiment",
            "activity_type": "produce",
            "role": "调味品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中炬高新主营业务", "quote": "主要以调味品,汽车配件,房地产及园区服务为主导"}]
        },
        {
            "exposure_id": "sh_600872_produce_auto_parts",
            "company_id": "sh_600872",
            "node_id": "auto_parts",
            "activity_type": "produce",
            "role": "汽车配件生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中炬高新主营业务", "quote": "主要以调味品,汽车配件,房地产及园区服务为主导"}]
        },
        {
            "exposure_id": "sh_600872_operate_real_estate_development",
            "company_id": "sh_600872",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "中炬高新主营业务", "quote": "主要以调味品,汽车配件,房地产及园区服务为主导"}]
        },
        # sh_600873 梅花生物
        {
            "exposure_id": "sh_600873_produce_monosodium_glutamate",
            "company_id": "sh_600873",
            "node_id": "monosodium_glutamate",
            "activity_type": "produce",
            "role": "味精生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "梅花生物主营业务", "quote": "味精,氨基酸,有机肥等生物发酵产品的生产及销售"}]
        },
        {
            "exposure_id": "sh_600873_produce_amino_acid",
            "company_id": "sh_600873",
            "node_id": "amino_acid",
            "activity_type": "produce",
            "role": "氨基酸生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "梅花生物主营业务", "quote": "味精,氨基酸,有机肥等生物发酵产品的生产及销售"}]
        },
        {
            "exposure_id": "sh_600873_produce_organic_fertilizer",
            "company_id": "sh_600873",
            "node_id": "organic_fertilizer",
            "activity_type": "produce",
            "role": "有机肥生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "梅花生物主营业务", "quote": "味精,氨基酸,有机肥等生物发酵产品的生产及销售"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 108")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 108 submission completed.")
