#!/usr/bin/env python3
"""
Batch 105 Submission Script
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
    "batch_id": "batch_105_nodes",
    "task_description": "Batch 105:补充缺失的产业节点——超市连锁、典当服务、医药批发、地铁运营、电梯、自动扶梯、日用化工产品",
    "nodes_to_upsert": [
        {
            "node_id": "supermarket_chain",
            "canonical_name_zh": "超市连锁",
            "canonical_name_en": "supermarket chain",
            "aliases": ["连锁超市", "大卖场", "综合超市"],
            "definition": "通过统一品牌、统一采购、统一管理和统一配送体系，在多个地点开设分店进行商品零售的连锁经营模式，销售品类涵盖食品、日用品、生鲜、家电等。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "百联股份主营业务",
                    "quote": "主要业务:连锁超市业务,建材业务,百货业务,房屋出租"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "pawnbroking_service",
            "canonical_name_zh": "典当服务",
            "canonical_name_en": "pawnbroking service",
            "aliases": ["典当行", "质押贷款", "当铺"],
            "definition": "以货币借贷为经营方式，以物品质押为融资条件，向当户提供短期、小额、快速的融资服务，并在约定期限内由当户赎回当物的特种金融服务。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "香溢融通主营业务",
                    "quote": "主要业务:商品销售,餐饮,保险服务,典当"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "pharmaceutical_wholesale",
            "canonical_name_zh": "医药批发",
            "canonical_name_en": "pharmaceutical wholesale",
            "aliases": ["药品批发", "医药流通", "医药分销"],
            "definition": "药品经营企业从药品生产企业或其他药品批发企业采购药品，再销售给药品零售企业、医疗机构或其他药品使用单位的药品流通环节服务。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "人民同泰主营业务",
                    "quote": "主营业务:医药批发,医药零售等医药商业业务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "metro_operation",
            "canonical_name_zh": "地铁运营",
            "canonical_name_en": "metro operation",
            "aliases": ["轨道交通运营", "城市轨道交通", "地铁服务"],
            "definition": "对城市地铁系统进行日常运营管理和维护的服务活动，包括列车调度运行、车站管理、票务服务、设备维护、安全保障等，为城市公共交通提供大运量、快速、准点的轨道客运服务。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "申通地铁主营业务",
                    "quote": "主要业务:地铁运营"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "elevator",
            "canonical_name_zh": "电梯",
            "canonical_name_en": "elevator",
            "aliases": ["升降机", "垂直电梯", "客梯", "货梯"],
            "definition": "以电力驱动、沿固定导轨运行的箱式垂直运输设备，用于建筑物内人员或货物的升降运送，是高层建筑中不可或缺的垂直交通设施。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "上海机电主营业务",
                    "quote": "电梯及自动扶梯产品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "escalator",
            "canonical_name_zh": "自动扶梯",
            "canonical_name_en": "escalator",
            "aliases": ["扶梯", "电扶梯", "滚梯"],
            "definition": "带有循环运行梯级、用于连续输送乘客向上或向下倾斜移动的电力驱动设备，广泛应用于商场、地铁站、机场、大型公共建筑等人流密集场所。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "上海机电主营业务",
                    "quote": "电梯及自动扶梯产品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "daily_chemical_product",
            "canonical_name_zh": "日用化工产品",
            "canonical_name_en": "daily chemical product",
            "aliases": ["洗涤化工", "日用化学品", "清洁用品"],
            "definition": "用于日常生活清洁、护理、美化等用途的化学制品，包括洗涤剂、洗衣粉、洗洁精、化妆品、口腔护理用品、消杀用品等。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "上海九百主营业务",
                    "quote": "主要产品:百货零售批发,洗涤化工产品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "elevator_parts_to_elevator",
            "from_node": "elevator_parts",
            "to_node": "elevator",
            "edge_type": "composition",
            "description": "电梯配件（控制系统、曳引机、门机等）组装构成电梯整机",
            "evidence": [
                {
                    "source_title": "电梯制造常识",
                    "quote": "电梯整机由曳引系统、导向系统、轿厢、门系统、重量平衡系统、电力拖动系统、电气控制系统和安全保护系统等组成。"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 105")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_105_business",
    "task_description": "Batch 105:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600826",
            "name_zh": "兰生股份",
            "aliases": ["东浩兰生会展集团股份有限公司"],
            "stock_codes": ["600826.SH"],
            "description": "主要业务:外贸,工业.主要产品:机电产品,纺织原料及制品,鞋类,塑料及其制品,玩具",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 518,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600827",
            "name_zh": "百联股份",
            "aliases": ["上海百联集团股份有限公司"],
            "stock_codes": ["600827.SH"],
            "description": "主要业务:连锁超市业务,建材业务,百货业务,房屋出租",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 19482,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600828",
            "name_zh": "茂业商业",
            "aliases": ["茂业商业股份有限公司"],
            "stock_codes": ["600828.SH"],
            "description": "主要业务:商品零售",
            "country": "CN",
            "province": "四川",
            "city": "成都市",
            "employee_count": 1180,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600829",
            "name_zh": "人民同泰",
            "aliases": ["哈药集团人民同泰医药股份有限公司"],
            "stock_codes": ["600829.SH"],
            "description": "主营业务:医药批发,医药零售等医药商业业务",
            "country": "CN",
            "province": "黑龙江",
            "city": "哈尔滨市",
            "employee_count": 2870,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600830",
            "name_zh": "香溢融通",
            "aliases": ["香溢融通控股集团股份有限公司"],
            "stock_codes": ["600830.SH"],
            "description": "主要业务:商品销售,餐饮,保险服务,典当",
            "country": "CN",
            "province": "浙江",
            "city": "宁波市",
            "employee_count": 207,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600831",
            "name_zh": "广电网络",
            "aliases": ["陕西广电网络传媒(集团)股份有限公司"],
            "stock_codes": ["600831.SH"],
            "description": "主要业务:从原来传统的有线电视传输业务,集团/家庭网络接入业务,逐步发展为以视频,数据,智慧三大业务为主业",
            "country": "CN",
            "province": "陕西",
            "city": "西安市",
            "employee_count": 6023,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600833",
            "name_zh": "第一医药",
            "aliases": ["上海第一医药股份有限公司"],
            "stock_codes": ["600833.SH"],
            "description": "医药零售及批发",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 818,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600834",
            "name_zh": "申通地铁",
            "aliases": ["上海申通地铁股份有限公司"],
            "stock_codes": ["600834.SH"],
            "description": "主要业务:地铁运营",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 1725,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600835",
            "name_zh": "上海机电",
            "aliases": ["上海机电股份有限公司"],
            "stock_codes": ["600835.SH"],
            "description": "电梯及自动扶梯产品",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 4397,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600838",
            "name_zh": "上海九百",
            "aliases": ["上海九百股份有限公司"],
            "stock_codes": ["600838.SH"],
            "description": "主要产品:百货零售批发,洗涤化工产品",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 163,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600826 兰生股份
        {
            "exposure_id": "sh_600826_provide_foreign_trade_service",
            "company_id": "sh_600826",
            "node_id": "foreign_trade_service",
            "activity_type": "provide_service",
            "role": "外贸服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "兰生股份主营业务", "quote": "主要业务:外贸,工业.主要产品:机电产品,纺织原料及制品,鞋类,塑料及其制品,玩具"}]
        },
        {
            "exposure_id": "sh_600826_produce_electromechanical_product",
            "company_id": "sh_600826",
            "node_id": "electromechanical_product",
            "activity_type": "produce",
            "role": "机电产品生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "兰生股份主营业务", "quote": "主要业务:外贸,工业.主要产品:机电产品,纺织原料及制品,鞋类,塑料及其制品,玩具"}]
        },
        {
            "exposure_id": "sh_600826_produce_textile_product",
            "company_id": "sh_600826",
            "node_id": "textile_product",
            "activity_type": "produce",
            "role": "纺织品生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "兰生股份主营业务", "quote": "主要业务:外贸,工业.主要产品:机电产品,纺织原料及制品,鞋类,塑料及其制品,玩具"}]
        },
        # sh_600827 百联股份
        {
            "exposure_id": "sh_600827_operate_supermarket_chain",
            "company_id": "sh_600827",
            "node_id": "supermarket_chain",
            "activity_type": "operate",
            "role": "连锁超市运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "百联股份主营业务", "quote": "主要业务:连锁超市业务,建材业务,百货业务,房屋出租"}]
        },
        {
            "exposure_id": "sh_600827_operate_department_store",
            "company_id": "sh_600827",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "百联股份主营业务", "quote": "主要业务:连锁超市业务,建材业务,百货业务,房屋出租"}]
        },
        # sh_600828 茂业商业
        {
            "exposure_id": "sh_600828_operate_department_store",
            "company_id": "sh_600828",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "商品零售运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "茂业主营业务", "quote": "主要业务:商品零售"}]
        },
        # sh_600829 人民同泰
        {
            "exposure_id": "sh_600829_provide_pharmaceutical_wholesale",
            "company_id": "sh_600829",
            "node_id": "pharmaceutical_wholesale",
            "activity_type": "provide_service",
            "role": "医药批发服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "人民同泰主营业务", "quote": "主营业务:医药批发,医药零售等医药商业业务"}]
        },
        {
            "exposure_id": "sh_600829_provide_pharmaceutical_retail",
            "company_id": "sh_600829",
            "node_id": "pharmaceutical_retail",
            "activity_type": "provide_service",
            "role": "医药零售服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "人民同泰主营业务", "quote": "主营业务:医药批发,医药零售等医药商业业务"}]
        },
        # sh_600830 香溢融通
        {
            "exposure_id": "sh_600830_operate_department_store",
            "company_id": "sh_600830",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "商品销售运营商",
            "weight": 0.6,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "香溢融通主营业务", "quote": "主要业务:商品销售,餐饮,保险服务,典当"}]
        },
        {
            "exposure_id": "sh_600830_provide_pawnbroking_service",
            "company_id": "sh_600830",
            "node_id": "pawnbroking_service",
            "activity_type": "provide_service",
            "role": "典当服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "香溢融通主营业务", "quote": "主要业务:商品销售,餐饮,保险服务,典当"}]
        },
        # sh_600831 广电网络
        {
            "exposure_id": "sh_600831_provide_cable_tv_network_service",
            "company_id": "sh_600831",
            "node_id": "cable_tv_network_service",
            "activity_type": "provide_service",
            "role": "有线电视网络服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广电网络主营业务", "quote": "主要业务:从原来传统的有线电视传输业务,集团/家庭网络接入业务,逐步发展为以视频,数据,智慧三大业务为主业"}]
        },
        {
            "exposure_id": "sh_600831_provide_broadband_network_service",
            "company_id": "sh_600831",
            "node_id": "broadband_network_service",
            "activity_type": "provide_service",
            "role": "宽带网络接入服务商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广电网络主营业务", "quote": "主要业务:...集团/家庭网络接入业务..."}]
        },
        # sh_600833 第一医药
        {
            "exposure_id": "sh_600833_provide_pharmaceutical_retail",
            "company_id": "sh_600833",
            "node_id": "pharmaceutical_retail",
            "activity_type": "provide_service",
            "role": "医药零售服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "第一医药主营业务", "quote": "医药零售及批发"}]
        },
        {
            "exposure_id": "sh_600833_provide_pharmaceutical_wholesale",
            "company_id": "sh_600833",
            "node_id": "pharmaceutical_wholesale",
            "activity_type": "provide_service",
            "role": "医药批发服务商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "第一医药主营业务", "quote": "医药零售及批发"}]
        },
        # sh_600834 申通地铁
        {
            "exposure_id": "sh_600834_operate_metro_operation",
            "company_id": "sh_600834",
            "node_id": "metro_operation",
            "activity_type": "operate",
            "role": "地铁运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "申通地铁主营业务", "quote": "主要业务:地铁运营"}]
        },
        # sh_600835 上海机电
        {
            "exposure_id": "sh_600835_produce_elevator",
            "company_id": "sh_600835",
            "node_id": "elevator",
            "activity_type": "produce",
            "role": "电梯生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海机电主营业务", "quote": "电梯及自动扶梯产品"}]
        },
        {
            "exposure_id": "sh_600835_produce_escalator",
            "company_id": "sh_600835",
            "node_id": "escalator",
            "activity_type": "produce",
            "role": "自动扶梯生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海机电主营业务", "quote": "电梯及自动扶梯产品"}]
        },
        # sh_600838 上海九百
        {
            "exposure_id": "sh_600838_operate_department_store",
            "company_id": "sh_600838",
            "node_id": "department_store",
            "activity_type": "operate",
            "role": "百货零售批发运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海九百主营业务", "quote": "主要产品:百货零售批发,洗涤化工产品"}]
        },
        {
            "exposure_id": "sh_600838_produce_daily_chemical_product",
            "company_id": "sh_600838",
            "node_id": "daily_chemical_product",
            "activity_type": "produce",
            "role": "洗涤化工产品生产商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "上海九百主营业务", "quote": "主要产品:百货零售批发,洗涤化工产品"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 105")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 105 submission completed.")
