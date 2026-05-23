"""
Batch 010 产业图与公司视图提交脚本
为 data/stock_batches/batch_010.json 中的10家中国公司构建产业实体图和公司视图。
"""

import asyncio
import httpx
import json

API_BASE = "http://localhost:8000/api/v1"


def ev(source_title: str, quote: str, source_url: str = ""):
    return {"source_title": source_title, "source_url": source_url or None, "quote": quote}


# ============================================================
# 新建产业节点
# ============================================================

NEW_NODES = [
    # ---- 食用油（京粮控股）----
    {
        "node_id": "edible_oil",
        "canonical_name_zh": "食用油",
        "canonical_name_en": "Edible Oil",
        "aliases": ["植物油", "食用植物油", "油脂"],
        "definition": "以大豆、花生、油菜籽、棕榈等植物油料或动物脂肪为原料，经压榨或浸出、精炼等工艺加工制成的可供人类食用的油脂产品，包括大豆油、花生油、菜籽油、棕榈油等。",
        "entity_type": "material",
        "evidence": [ev("京粮控股2024年年度报告", "主营业务为油脂油料加工、油脂油料贸易及食品加工。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 白酒（新金路）----
    {
        "node_id": "liquor",
        "canonical_name_zh": "白酒",
        "canonical_name_en": "Chinese Liquor (Baijiu)",
        "aliases": ["蒸馏酒", "烈酒", "烧酒"],
        "definition": "以粮谷为主要原料，经固态或液态发酵、蒸馏、陈酿、勾调等工艺制成的中国传统蒸馏酒，具有以酯类为主体的复合香味，酒精度一般在38-65度之间。",
        "entity_type": "material",
        "evidence": [ev("新金路2024年年度报告", "主要业务包括白酒生产和销售。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 医疗服务（国际医学）----
    {
        "node_id": "medical_service",
        "canonical_name_zh": "医疗服务",
        "canonical_name_en": "Medical Service",
        "aliases": ["医疗卫生服务", "诊疗服务", "临床医疗服务"],
        "definition": "以医疗机构为主体，为患者提供疾病预防、诊断、治疗、康复及健康管理等综合性医疗卫生服务，包括门诊诊疗、住院治疗、手术服务、医学检验及康复护理等。",
        "entity_type": "service",
        "evidence": [ev("国际医学2024年年度报告", "主要业务为医疗服务。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边
# ============================================================

EDGES = [
    {
        "edge_id": "flow_grain_oil_to_edible_oil",
        "from_node": "grain_oil",
        "to_node": "edible_oil",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "description": "大豆、花生、油菜籽等植物油料经过压榨、浸出和精炼工艺加工成食用油。",
        "evidence": [ev("粮油加工产业常识", "食用油以植物油料为原料，经清理、破碎、轧胚、蒸炒、压榨或浸出、精炼等工序制成。")],
        "confidence": "HIGH",
    },
]


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "st_bios",
        "name_zh": "南华生物医药股份有限公司",
        "name_en": "Nanhua Biomedicine Co., Ltd.",
        "aliases": ["*ST生物"],
        "stock_codes": ["000504.SZ"],
        "description": "以生物医药和节能环保为主业的科技企业，业务涵盖生物制品研发、干细胞及免疫细胞储存、环保技术服务等。",
        "country": "CN", "province": "湖南", "city": "长沙市",
        "founded_year": 1991, "employee_count": 378,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "jingliang",
        "name_zh": "海南京粮控股股份有限公司",
        "name_en": "Hainan Jingliang Holding Co., Ltd.",
        "aliases": ["京粮控股"],
        "stock_codes": ["000505.SZ"],
        "description": "北京市属粮油食品企业，主营油脂油料加工、油脂贸易及食品加工，拥有多个食用油知名品牌。",
        "country": "CN", "province": "海南", "city": "海口市",
        "founded_year": 1988, "employee_count": 2391,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "zhaojin_gold",
        "name_zh": "招金国际黄金股份有限公司",
        "name_en": "Zhaojin International Gold Co., Ltd.",
        "aliases": ["招金黄金"],
        "stock_codes": ["000506.SZ"],
        "description": "以黄金为主业的矿业企业，主要从事黄金矿产资源的勘探、开采、选矿、冶炼及销售，同时涉及自有房产租赁业务。",
        "country": "CN", "province": "山东", "city": "济南市",
        "founded_year": 1988, "employee_count": 1202,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "zhuhai_port",
        "name_zh": "珠海港股份有限公司",
        "name_en": "Zhuhai Port Co., Ltd.",
        "aliases": ["珠海港"],
        "stock_codes": ["000507.SZ"],
        "description": "珠海市港口综合运营商，业务涵盖港口航运、物流供应链、能源环保（风电、光伏、燃气）、港城建设及航运金融。",
        "country": "CN", "province": "广东", "city": "珠海市",
        "founded_year": 1986, "employee_count": 4609,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huasu",
        "name_zh": "华塑控股股份有限公司",
        "name_en": "Huasu Holding Co., Ltd.",
        "aliases": ["华塑控股"],
        "stock_codes": ["000509.SZ"],
        "description": "电子信息显示企业，主营显示器和IOT智能显示终端的研发、生产和销售，产品广泛应用于消费电子、工业控制及物联网领域。",
        "country": "CN", "province": "四川", "city": "南充市",
        "founded_year": 1990, "employee_count": 363,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "xinjinlu",
        "name_zh": "四川新金路集团股份有限公司",
        "name_en": "Sichuan Xinjinlu Group Co., Ltd.",
        "aliases": ["新金路"],
        "stock_codes": ["000510.SZ"],
        "description": "四川省综合性化工企业，主营PVC树脂、烧碱等氯碱化工产品的生产和销售，同时涉及白酒、房地产及天然气业务。",
        "country": "CN", "province": "四川", "city": "德阳市",
        "founded_year": 1992, "employee_count": 2078,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "livzon",
        "name_zh": "丽珠医药集团股份有限公司",
        "name_en": "Livzon Pharmaceutical Group Inc.",
        "aliases": ["丽珠集团"],
        "stock_codes": ["000513.SZ", "1513.HK"],
        "description": "中国综合性医药企业，业务涵盖化学药、生物药、中成药及原料药的生产、营销和科研，在消化道用药、抗病毒药物及辅助生殖用药领域具有优势。",
        "country": "CN", "province": "广东", "city": "珠海市",
        "founded_year": 1985, "employee_count": 8878,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "yu_kaifa",
        "name_zh": "重庆渝开发股份有限公司",
        "name_en": "Chongqing Yu Kaifa Co., Ltd.",
        "aliases": ["渝开发"],
        "stock_codes": ["000514.SZ"],
        "description": "重庆市属房地产开发企业，主营房地产开发和土地整治代理业务。",
        "country": "CN", "province": "重庆", "city": "重庆市",
        "founded_year": 1992, "employee_count": 698,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "international_medical",
        "name_zh": "西安国际医学投资股份有限公司",
        "name_en": "Xi'an International Medical Investment Co., Ltd.",
        "aliases": ["国际医学"],
        "stock_codes": ["000516.SZ"],
        "description": "以医疗服务为核心主业的投资运营企业，运营大型综合医院和专科医院，提供高质量的医疗诊疗、康复护理及健康管理服务。",
        "country": "CN", "province": "陕西", "city": "西安市",
        "founded_year": 1996, "employee_count": 8858,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "rongan_real_estate",
        "name_zh": "荣安地产股份有限公司",
        "name_en": "Rongan Real Estate Co., Ltd.",
        "aliases": ["荣安地产"],
        "stock_codes": ["000517.SZ"],
        "description": "浙江省房地产开发企业，主营业务为房地产开发及物业管理，深耕宁波及长三角区域市场。",
        "country": "CN", "province": "浙江", "city": "宁波市",
        "founded_year": 1989, "employee_count": 258,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- *ST生物 ----
    {
        "exposure_id": "st_bios_manufacture_biological",
        "company_id": "st_bios",
        "node_id": "biological_drug",
        "activity_type": "manufacture",
        "role": "生物医药制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("*ST生物2024年年度报告", "主要业务为生物医药。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "st_bios_provide_eco_restoration",
        "company_id": "st_bios",
        "node_id": "ecological_restoration_service",
        "activity_type": "provide_service",
        "role": "节能环保服务商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("*ST生物2024年年度报告", "主要业务包括节能环保。")],
        "status": "ACTIVE",
    },
    # ---- 京粮控股 ----
    {
        "exposure_id": "jingliang_manufacture_edible_oil",
        "company_id": "jingliang",
        "node_id": "edible_oil",
        "activity_type": "manufacture",
        "role": "食用油加工商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("京粮控股2024年年度报告", "主营业务为油脂油料加工、油脂油料贸易及食品加工。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "jingliang_procure_grain_oil",
        "company_id": "jingliang",
        "node_id": "grain_oil",
        "activity_type": "procure",
        "role": "油料采购商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("京粮控股2024年年度报告", "主营业务包括油脂油料加工及贸易。")],
        "status": "ACTIVE",
    },
    # ---- 招金黄金 ----
    {
        "exposure_id": "zhaojin_produce_gold",
        "company_id": "zhaojin_gold",
        "node_id": "precious_metal",
        "activity_type": "produce",
        "role": "黄金矿业开采商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("招金黄金2024年年度报告", "主营业务以黄金为主要品种的矿业开采、销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhaojin_produce_property",
        "company_id": "zhaojin_gold",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商（自有房产出租）",
        "weight": 0.3, "confidence": "HIGH",
        "evidence": [ev("招金黄金2024年年度报告", "主营业务包括自有房产的出租。")],
        "status": "ACTIVE",
    },
    # ---- 珠海港 ----
    {
        "exposure_id": "zhuhai_provide_container",
        "company_id": "zhuhai_port",
        "node_id": "container_handling_service",
        "activity_type": "provide_service",
        "role": "港口集装箱装卸服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务为港口航运。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhuhai_provide_logistics",
        "company_id": "zhuhai_port",
        "node_id": "logistics_service",
        "activity_type": "provide_service",
        "role": "物流供应链服务商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务包括物流供应链。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhuhai_provide_shipping",
        "company_id": "zhuhai_port",
        "node_id": "shipping_service",
        "activity_type": "provide_service",
        "role": "航运服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务包括港口航运。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhuhai_operate_solar",
        "company_id": "zhuhai_port",
        "node_id": "solar_power_generation",
        "activity_type": "operate",
        "role": "光伏发电运营商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务包括能源环保。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhuhai_operate_wind",
        "company_id": "zhuhai_port",
        "node_id": "wind_power_generation",
        "activity_type": "operate",
        "role": "风力发电运营商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务包括能源环保。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhuhai_provide_gas",
        "company_id": "zhuhai_port",
        "node_id": "natural_gas",
        "activity_type": "provide_service",
        "role": "天然气供应服务商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("珠海港2024年年度报告", "主要业务包括能源环保。")],
        "status": "ACTIVE",
    },
    # ---- 华塑控股 ----
    {
        "exposure_id": "huasu_manufacture_lcd_monitor",
        "company_id": "huasu",
        "node_id": "lcd_monitor",
        "activity_type": "manufacture",
        "role": "显示器制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华塑控股2024年年度报告", "主要产品为显示器。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huasu_manufacture_led_display",
        "company_id": "huasu",
        "node_id": "led_display_screen",
        "activity_type": "manufacture",
        "role": "IOT智能显示终端制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("华塑控股2024年年度报告", "主要产品包括IOT智能显示终端。")],
        "status": "ACTIVE",
    },
    # ---- 新金路 ----
    {
        "exposure_id": "xinjinlu_manufacture_pvc",
        "company_id": "xinjinlu",
        "node_id": "plastic_resin",
        "activity_type": "manufacture",
        "role": "PVC树脂制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("新金路2024年年度报告", "主要业务为生产销售PVC树脂。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xinjinlu_manufacture_caustic",
        "company_id": "xinjinlu",
        "node_id": "caustic_soda",
        "activity_type": "manufacture",
        "role": "烧碱制造商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("新金路2024年年度报告", "主要业务包括烧碱系列化工原料及其加工产品的生产销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xinjinlu_manufacture_liquor",
        "company_id": "xinjinlu",
        "node_id": "liquor",
        "activity_type": "manufacture",
        "role": "白酒制造商",
        "weight": 0.4, "confidence": "HIGH",
        "evidence": [ev("新金路2024年年度报告", "主要业务包括白酒生产和销售。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xinjinlu_produce_property",
        "company_id": "xinjinlu",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商",
        "weight": 0.3, "confidence": "HIGH",
        "evidence": [ev("新金路2024年年度报告", "主要业务包括房地产业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xinjinlu_provide_gas",
        "company_id": "xinjinlu",
        "node_id": "natural_gas",
        "activity_type": "provide_service",
        "role": "天然气加工销售商",
        "weight": 0.3, "confidence": "HIGH",
        "evidence": [ev("新金路2024年年度报告", "主要业务包括天然气加工销售。")],
        "status": "ACTIVE",
    },
    # ---- 丽珠集团 ----
    {
        "exposure_id": "livzon_manufacture_pharma",
        "company_id": "livzon",
        "node_id": "pharmaceutical_product",
        "activity_type": "manufacture",
        "role": "综合性医药产品制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("丽珠集团2024年年度报告", "主要业务为医药产品的生产、营销及科研。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "livzon_manufacture_chemical",
        "company_id": "livzon",
        "node_id": "chemical_drug",
        "activity_type": "manufacture",
        "role": "化学药制造商",
        "weight": 0.9, "confidence": "HIGH",
        "evidence": [ev("丽珠集团2024年年度报告", "主要产品包括丽珠得乐系列、头孢曲松钠等化学药。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "livzon_manufacture_tcm",
        "company_id": "livzon",
        "node_id": "traditional_chinese_medicine",
        "activity_type": "manufacture",
        "role": "中成药制造商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("丽珠集团2024年年度报告", "主要产品包括抗病毒颗粒、参芪扶正注射液等中成药。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "livzon_manufacture_biological",
        "company_id": "livzon",
        "node_id": "biological_drug",
        "activity_type": "manufacture",
        "role": "生物药制造商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("丽珠集团2024年年度报告", "公司设有生物药研发管线，涵盖重组蛋白及单抗类药物。")],
        "status": "ACTIVE",
    },
    # ---- 渝开发 ----
    {
        "exposure_id": "yu_produce_residential",
        "company_id": "yu_kaifa",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("渝开发2024年年度报告", "主要业务为房地产开发。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "yu_provide_construction",
        "company_id": "yu_kaifa",
        "node_id": "construction_service",
        "activity_type": "provide_service",
        "role": "土地整治服务商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("渝开发2024年年度报告", "主要业务包括代理土地整治。")],
        "status": "ACTIVE",
    },
    # ---- 国际医学 ----
    {
        "exposure_id": "international_medical_provide_service",
        "company_id": "international_medical",
        "node_id": "medical_service",
        "activity_type": "provide_service",
        "role": "医疗服务提供商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("国际医学2024年年度报告", "主要业务为医疗服务。")],
        "status": "ACTIVE",
    },
    # ---- 荣安地产 ----
    {
        "exposure_id": "rongan_produce_residential",
        "company_id": "rongan_real_estate",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "住宅开发商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("荣安地产2024年年度报告", "主营业务为房地产开发。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "rongan_produce_commercial",
        "company_id": "rongan_real_estate",
        "node_id": "commercial_property",
        "activity_type": "produce",
        "role": "商业地产开发商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("荣安地产2024年年度报告", "主营业务为房地产开发及物业管理。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "rongan_provide_property_mgmt",
        "company_id": "rongan_real_estate",
        "node_id": "property_management_service",
        "activity_type": "provide_service",
        "role": "物业管理服务商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("荣安地产2024年年度报告", "主营业务为房地产开发及物业管理。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_010_industrial_graph",
        "task_description": "Batch 010: 为10家中国公司构建产业实体图，涵盖生物医药、粮油加工、黄金矿业、港口能源、显示终端、氯碱化工、医药制造、房地产开发及医疗服务等产业链。",
        "nodes_to_upsert": NEW_NODES,
        "edges_to_upsert": EDGES,
        "rejected_or_pending": []
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/batches", json=batch, timeout=120.0)
        print(f"Graph batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


async def submit_business_batch():
    batch = {
        "batch_id": "batch_010_company_views",
        "task_description": "Batch 010: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": COMPANIES,
        "company_node_exposures_to_upsert": EXPOSURES
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/business-batches", json=batch, timeout=120.0)
        print(f"Business batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


async def main():
    print("=" * 70)
    print("Batch 010 产业图与公司视图提交")
    print("=" * 70)
    print(f"新建节点: {len(NEW_NODES)}")
    print(f"新建边: {len(EDGES)}")
    print(f"新建公司: {len(COMPANIES)}")
    print(f"新建暴露关系: {len(EXPOSURES)}")
    print()

    print("=" * 70)
    print("Step 1: 提交产业图 (GraphRegistrationBatch)")
    print("=" * 70)
    graph_result = await submit_graph_batch()

    print("\n" + "=" * 70)
    print("Step 2: 提交公司视图 (BusinessRegistrationBatch)")
    print("=" * 70)
    biz_result = await submit_business_batch()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Graph batch: nodes_created={graph_result.get('nodes_created')}, nodes_updated={graph_result.get('nodes_updated')}, edges_created={graph_result.get('edges_created')}, edges_updated={graph_result.get('edges_updated')}, errors={len(graph_result.get('errors', []))}")
    if graph_result.get('errors'):
        for e in graph_result['errors']:
            print(f"  ERROR: {e}")
    print(f"Business batch: companies_created={biz_result.get('companies_created')}, companies_updated={biz_result.get('companies_updated')}, exposures_created={biz_result.get('exposures_created')}, exposures_updated={biz_result.get('exposures_updated')}, errors={len(biz_result.get('errors', []))}")
    if biz_result.get('errors'):
        for e in biz_result['errors']:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(main())
