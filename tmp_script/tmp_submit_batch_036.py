#!/usr/bin/env python3
"""
Batch 036 Submission Script
Companies: 000905, 000906, 000908, 000909, 000910, 000911, 000912, 000913, 000915, 000917
"""
import json
import urllib.request
import urllib.error

API_BASE = "http://localhost:8005/api/v1"


def api_post(path, data):
    url = f"{API_BASE}{path}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"ERROR {e.code} on {path}: {err[:500]}")
        raise


# ========================================================================
# 1. Industrial Graph Registration Batch
# ========================================================================
graph_batch = {
    "batch_id": "batch_036_graph",
    "task_description": "Batch 036 industrial graph nodes and edges: wood floor, motorcycle, mechanism paper, and related flows.",
    "nodes_to_upsert": [
        {
            "node_id": "wood_floor",
            "canonical_name_zh": "木地板",
            "canonical_name_en": "Wood Floor",
            "aliases": ["实木地板", "复合木地板"],
            "definition": "以木材或木质复合材料为主要基材加工而成的地面铺装材料，包括实木地板、强化木地板和实木复合地板等。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "大亚圣象主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:中高密度板、木地板产品等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "motorcycle",
            "canonical_name_zh": "摩托车整车",
            "canonical_name_en": "Motorcycle",
            "aliases": ["摩托整车", "两轮摩托车"],
            "definition": "以内燃机或电动机为动力的两轮或三轮机动车辆整车产品。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "钱江摩托主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:摩托车整车、摩托车配件及加工"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "mechanism_paper",
            "canonical_name_zh": "机制纸",
            "canonical_name_en": "Machine-made Paper",
            "aliases": ["工业用纸", "机制纸张"],
            "definition": "采用机械化连续生产工艺制造的各种纸张产品，包括文化用纸、包装用纸和生活用纸等。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "广糖主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:机制糖、机制纸、蔗渣浆"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "artificial_board_to_wood_floor",
            "from_node": "artificial_board",
            "to_node": "wood_floor",
            "edge_type": "composition",
            "description": "人造板（中高密度纤维板、刨花板）是木地板产品的主要基材组成部分。",
            "evidence": [
                {
                    "source_title": "大亚圣象主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:中高密度板、木地板产品等"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "bagasse_pulp_to_mechanism_paper",
            "from_node": "bagasse_pulp",
            "to_node": "mechanism_paper",
            "edge_type": "material_flow",
            "description": "蔗渣浆作为造纸原料，经过制浆和造纸工艺生产出机制纸产品。",
            "evidence": [
                {
                    "source_title": "广糖主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:机制糖、机制纸、蔗渣浆"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "motorcycle_engine_to_motorcycle",
            "from_node": "motorcycle_engine",
            "to_node": "motorcycle",
            "edge_type": "composition",
            "description": "摩托车发动机是摩托车整车的核心动力组成部分。",
            "evidence": [
                {
                    "source_title": "钱江摩托主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:摩托车整车、摩托车配件及加工"
                }
            ],
            "confidence": "HIGH",
        },
    ],
    "rejected_or_pending": [],
}

print("[1/2] Submitting graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph batch result: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

# ========================================================================
# 2. Business Registration Batch
# ========================================================================
business_batch = {
    "batch_id": "batch_036_business",
    "task_description": "Batch 036 company registrations and node exposures for 10 listed companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {
            "company_id": "xiamen_port",
            "name_zh": "厦门港务发展股份有限公司",
            "aliases": ["厦门港务"],
            "stock_codes": ["000905.SZ"],
            "description": "港口经营、装卸搬运及供应链管理服务企业",
            "country": "CN",
            "province": "福建",
            "city": "厦门",
            "employee_count": 4631,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "zheshang_zhongtuo",
            "name_zh": "浙商中拓集团股份有限公司",
            "aliases": ["浙商中拓"],
            "stock_codes": ["000906.SZ"],
            "description": "金属矿石、金属材料及供应链管理服务企业",
            "country": "CN",
            "province": "浙江",
            "city": "杭州",
            "employee_count": 2408,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "st_jingfeng",
            "name_zh": "石药集团湖南景峰医药股份有限公司",
            "aliases": ["ST景峰"],
            "stock_codes": ["000908.SZ"],
            "description": "化学药品注射剂及医药产品研发制造企业",
            "country": "CN",
            "province": "湖南",
            "city": "常德",
            "employee_count": 547,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "st_shuyuan",
            "name_zh": "数源科技股份有限公司",
            "aliases": ["*ST数源", "数源科技"],
            "stock_codes": ["000909.SZ"],
            "description": "彩色电视机制造及房地产开发企业",
            "country": "CN",
            "province": "浙江",
            "city": "杭州",
            "employee_count": 353,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "dare_power",
            "name_zh": "大亚圣象家居股份有限公司",
            "aliases": ["大亚圣象"],
            "stock_codes": ["000910.SZ"],
            "description": "中高密度板、木地板等家居装饰材料制造企业",
            "country": "CN",
            "province": "江苏",
            "city": "镇江",
            "employee_count": 5064,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "st_guangtang",
            "name_zh": "广西农投糖业集团股份有限公司",
            "aliases": ["*ST广糖", "广糖"],
            "stock_codes": ["000911.SZ"],
            "description": "机制糖、机制纸及蔗渣浆生产销售企业",
            "country": "CN",
            "province": "广西",
            "city": "南宁",
            "employee_count": 2603,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "lutianhua",
            "name_zh": "四川泸天化股份有限公司",
            "aliases": ["泸天化"],
            "stock_codes": ["000912.SZ"],
            "description": "尿素及化肥化工原料生产销售企业",
            "country": "CN",
            "province": "四川",
            "city": "泸州",
            "employee_count": 2869,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "qianjiang_motor",
            "name_zh": "浙江钱江摩托股份有限公司",
            "aliases": ["钱江摩托"],
            "stock_codes": ["000913.SZ"],
            "description": "摩托车整车及摩托车配件制造企业",
            "country": "CN",
            "province": "浙江",
            "city": "台州",
            "employee_count": 5602,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "huatiedayin",
            "name_zh": "山东华特达因健康股份有限公司",
            "aliases": ["华特达因"],
            "stock_codes": ["000915.SZ"],
            "description": "环保产品、药品及电子信息产品企业",
            "country": "CN",
            "province": "山东",
            "city": "临沂",
            "employee_count": 1759,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "dian_guang_media",
            "name_zh": "湖南电广传媒股份有限公司",
            "aliases": ["电广传媒"],
            "stock_codes": ["000917.SZ"],
            "description": "有线电视网络、广告代理、影视制作及文旅投资企业",
            "country": "CN",
            "province": "湖南",
            "city": "长沙",
            "employee_count": 2383,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
    ],
    "company_node_exposures_to_upsert": [
        # 厦门港务
        {
            "exposure_id": "xiamen_port_operate_port",
            "company_id": "xiamen_port",
            "node_id": "port_operation_service",
            "activity_type": "operate",
            "role": "港口运营服务商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦门港务主营业务", "quote": "主要业务:厦门大桥、海沧大桥过桥费的征收及经营、维护与管理、建材产品的生产和销售、工程施工"}],
        },
        # 浙商中拓
        {
            "exposure_id": "zhongtuo_provide_logistics",
            "company_id": "zheshang_zhongtuo",
            "node_id": "logistics_service",
            "activity_type": "provide_service",
            "role": "供应链及物流服务商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "浙商中拓主营业务", "quote": "一般项目:金属矿石销售、供应链管理服务等"}],
        },
        # ST景峰
        {
            "exposure_id": "jingfeng_produce_chemical_drug",
            "company_id": "st_jingfeng",
            "node_id": "chemical_drug",
            "activity_type": "produce",
            "role": "化学药品生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST景峰主营业务", "quote": "主要产品:参芎葡萄糖注射液和玻璃酸钠注射液，分别为心脑血管领域和骨科领域的知名品种"}],
        },
        {
            "exposure_id": "jingfeng_produce_pharma_product",
            "company_id": "st_jingfeng",
            "node_id": "pharmaceutical_product",
            "activity_type": "produce",
            "role": "医药产品制造商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST景峰主营业务", "quote": "主营业务:医药产品的研发、制造与销售"}],
        },
        # *ST数源
        {
            "exposure_id": "shuyuan_manufacture_color_tv",
            "company_id": "st_shuyuan",
            "node_id": "color_tv",
            "activity_type": "manufacture",
            "role": "彩色电视机制造商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "数源科技主营业务", "quote": "主要产品:彩电"}],
        },
        # 大亚圣象
        {
            "exposure_id": "dare_manufacture_wood_floor",
            "company_id": "dare_power",
            "node_id": "wood_floor",
            "activity_type": "manufacture",
            "role": "木地板制造商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "大亚圣象主营业务", "quote": "主要产品:中高密度板、木地板产品等"}],
        },
        {
            "exposure_id": "dare_manufacture_artificial_board",
            "company_id": "dare_power",
            "node_id": "artificial_board",
            "activity_type": "manufacture",
            "role": "人造板制造商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "大亚圣象主营业务", "quote": "主要产品:中高密度板、木地板产品等"}],
        },
        # *ST广糖
        {
            "exposure_id": "guangtang_produce_white_sugar",
            "company_id": "st_guangtang",
            "node_id": "white_sugar",
            "activity_type": "produce",
            "role": "白砂糖生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广糖主营业务", "quote": "主要产品:机制糖、机制纸、蔗渣浆"}],
        },
        {
            "exposure_id": "guangtang_produce_mechanism_paper",
            "company_id": "st_guangtang",
            "node_id": "mechanism_paper",
            "activity_type": "produce",
            "role": "机制纸生产商",
            "weight": 0.75,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广糖主营业务", "quote": "主要产品:机制糖、机制纸、蔗渣浆"}],
        },
        # 泸天化
        {
            "exposure_id": "lutianhua_produce_urea",
            "company_id": "lutianhua",
            "node_id": "urea",
            "activity_type": "produce",
            "role": "尿素生产商",
            "weight": 0.95,
            "confidence": "HIGH",
            "evidence": [{"source_title": "泸天化主营业务", "quote": "主要产品:化肥化工原料的生产与销售，主要产品:尿素"}],
        },
        {
            "exposure_id": "lutianhua_produce_chemical_fertilizer",
            "company_id": "lutianhua",
            "node_id": "chemical_fertilizer",
            "activity_type": "produce",
            "role": "化肥生产商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "泸天化主营业务", "quote": "主要产品:化肥化工原料的生产与销售"}],
        },
        # 钱江摩托
        {
            "exposure_id": "qianjiang_manufacture_motorcycle",
            "company_id": "qianjiang_motor",
            "node_id": "motorcycle",
            "activity_type": "manufacture",
            "role": "摩托车整车制造商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "钱江摩托主营业务", "quote": "主要产品:摩托车整车、摩托车配件及加工"}],
        },
        {
            "exposure_id": "qianjiang_manufacture_motorcycle_engine",
            "company_id": "qianjiang_motor",
            "node_id": "motorcycle_engine",
            "activity_type": "manufacture",
            "role": "摩托车发动机制造商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "钱江摩托主营业务", "quote": "主要产品:摩托车整车、摩托车配件及加工"}],
        },
        # 华特达因
        {
            "exposure_id": "huatiedayin_produce_chemical_drug",
            "company_id": "huatiedayin",
            "node_id": "chemical_drug",
            "activity_type": "produce",
            "role": "化学药品生产商",
            "weight": 0.8,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "华特达因主营业务", "quote": "主要产品:环保产品、药品、电子信息产品、科技园区管理"}],
        },
        # 电广传媒
        {
            "exposure_id": "dian_guang_operate_film_tv",
            "company_id": "dian_guang_media",
            "node_id": "film_television",
            "activity_type": "operate",
            "role": "影视内容制作运营商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电广传媒主营业务", "quote": "文创:广告代理、高铁自媒体广告、电影、电视剧等"}],
        },
        {
            "exposure_id": "dian_guang_provide_advertising",
            "company_id": "dian_guang_media",
            "node_id": "advertising_service",
            "activity_type": "provide_service",
            "role": "广告服务提供商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "电广传媒主营业务", "quote": "文创:广告代理、高铁自媒体广告、电影、电视剧等"}],
        },
    ],
}

print("[2/2] Submitting business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business batch result: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")

print("\nBatch 036 submission complete!")
