"""
Batch 009 产业图与公司视图提交脚本
为 data/stock_batches/batch_009.json 中的10家中国公司构建产业实体图和公司视图。
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
    # ---- 锡金属（兴业银锡）----
    {
        "node_id": "tin_metal",
        "canonical_name_zh": "锡金属",
        "canonical_name_en": "Tin Metal",
        "aliases": ["锡锭", "精锡"],
        "definition": "一种银白色有光泽的低熔点金属，由锡矿石经采选冶炼制得，具有良好的延展性、抗腐蚀性和焊接性，广泛用于电子焊料、马口铁、化工催化剂及合金材料。",
        "entity_type": "material",
        "evidence": [ev("兴业银锡2024年年度报告", "主营业务以有色金属采选、冶炼、加工、销售为主业。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 高速公路运营服务（粤高速A）----
    {
        "node_id": "highway_operation_service",
        "canonical_name_zh": "高速公路运营服务",
        "canonical_name_en": "Highway Operation Service",
        "aliases": ["高速公路收费运营", "高速公路管理服务"],
        "definition": "对高速公路及特大桥梁等交通基础设施进行收费运营、养护管理、安全监控和配套服务的业务，为道路使用者提供通行服务并获取通行费收入。",
        "entity_type": "service",
        "evidence": [ev("粤高速A2024年年度报告", "主要业务为高速公路和特大桥梁的商业开发和经营。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 机制纸（ST晨鸣）----
    {
        "node_id": "paper_product",
        "canonical_name_zh": "机制纸",
        "canonical_name_en": "Machine-Made Paper",
        "aliases": ["文化用纸", "铜版纸", "新闻纸", "白卡纸"],
        "definition": "以木材、竹子、芦苇或废纸等为原料，通过制浆、造纸机械连续生产制造的纸张产品，包括文化用纸（铜版纸、双胶纸）、包装用纸（白卡纸、箱板纸）及特种纸等。",
        "entity_type": "material",
        "evidence": [ev("ST晨鸣2024年年度报告", "主要产品及劳务分别为机制纸、建筑材料、电及汽及其他。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
    # ---- 健康管理服务（国新健康）----
    {
        "node_id": "health_management_service",
        "canonical_name_zh": "健康管理服务",
        "canonical_name_en": "Health Management Service",
        "aliases": ["健康保障服务", "医保管理服务", "医疗大数据服务"],
        "definition": "运用信息技术和数据分析手段，为医保基金、医疗机构、商业保险公司及参保人员提供的综合健康管理服务，包括医保基金监管、医疗大数据分析、医药福利管理（PBM）及第三方理赔服务等。",
        "entity_type": "service",
        "evidence": [ev("国新健康2024年年度报告", "主要业务涵盖医保基金综合管理服务、健康医疗大数据服务、医药福利管理服务(PBM)、商业健康保险第三方服务(TPA)、医疗人工智能服务等五大领域。")],
        "confidence": "HIGH", "status": "ACTIVE",
    },
]


# ============================================================
# 新建产业流边（本批次无新增产业流边）
# ============================================================

EDGES = []


# ============================================================
# 公司信息
# ============================================================

COMPANIES = [
    {
        "company_id": "dongeejiao",
        "name_zh": "东阿阿胶股份有限公司",
        "name_en": "Dong-E-E-Jiao Co., Ltd.",
        "aliases": ["东阿阿胶"],
        "stock_codes": ["000423.SZ"],
        "description": "中国阿胶行业龙头企业，主营阿胶及系列产品的研发、生产和销售，产品涵盖阿胶块、阿胶糕、阿胶口服液及保健食品等。",
        "country": "CN", "province": "山东", "city": "聊城市",
        "founded_year": 1994, "employee_count": 4345,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "xcmg",
        "name_zh": "徐工集团工程机械股份有限公司",
        "name_en": "XCMG Construction Machinery Co., Ltd.",
        "aliases": ["徐工机械"],
        "stock_codes": ["000425.SZ"],
        "description": "中国工程机械行业领军企业之一，主营压实机械、铲运机械、路面机械、筑路机械及起重机械等产品的研发、制造和销售。",
        "country": "CN", "province": "江苏", "city": "徐州市",
        "founded_year": 1993, "employee_count": 27791,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "xingye_yinxin",
        "name_zh": "内蒙古兴业银锡矿业股份有限公司",
        "name_en": "Inner Mongolia Xingye Silver & Tin Mining Co., Ltd.",
        "aliases": ["兴业银锡"],
        "stock_codes": ["000426.SZ"],
        "description": "以锡、银、锌等有色金属采选冶炼为主业的矿业企业，拥有内蒙古地区优质有色金属矿产资源。",
        "country": "CN", "province": "内蒙古", "city": "赤峰市",
        "founded_year": 1996, "employee_count": 1062,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "huatian_hotel",
        "name_zh": "华天酒店集团股份有限公司",
        "name_en": "Huatian Hotel Group Co., Ltd.",
        "aliases": ["华天酒店"],
        "stock_codes": ["000428.SZ"],
        "description": "湖南省酒店行业龙头企业，业务涵盖酒店服务、房地产开发、酒店资产运营及生产制造业，拥有华天大酒店等知名品牌。",
        "country": "CN", "province": "湖南", "city": "长沙市",
        "founded_year": 1996, "employee_count": 2683,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "guangdong_expressway",
        "name_zh": "广东省高速公路发展股份有限公司",
        "name_en": "Guangdong Expressway Development Co., Ltd.",
        "aliases": ["粤高速A"],
        "stock_codes": ["000429.SZ"],
        "description": "广东省高速公路投资运营企业，主营高速公路和特大桥梁的商业开发、收费运营及养护管理。",
        "country": "CN", "province": "广东", "city": "广州市",
        "founded_year": 1997, "employee_count": 3029,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "zhangjiajie",
        "name_zh": "张家界旅游集团股份有限公司",
        "name_en": "Zhangjiajie Tourism Group Co., Ltd.",
        "aliases": ["张家界"],
        "stock_codes": ["000430.SZ"],
        "description": "张家界市旅游行业龙头企业，业务涵盖旅游景区经营、旅游客运、旅行社经营、旅游客运索道经营及酒店经营。",
        "country": "CN", "province": "湖南", "city": "张家界市",
        "founded_year": 1992, "employee_count": 935,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "chenming_paper",
        "name_zh": "山东晨鸣纸业集团股份有限公司",
        "name_en": "Shandong Chenming Paper Holdings Ltd.",
        "aliases": ["ST晨鸣", "晨鸣纸业"],
        "stock_codes": ["000488.SZ"],
        "description": "中国大型造纸企业之一，主营机制纸的生产和销售，产品涵盖文化用纸、铜版纸、白卡纸及包装用纸等。",
        "country": "CN", "province": "山东", "city": "潍坊市",
        "founded_year": 1993, "employee_count": 8992,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "shandong_road_bridge",
        "name_zh": "山东高速路桥集团股份有限公司",
        "name_en": "Shandong Hi-Speed Road & Bridge Co., Ltd.",
        "aliases": ["山东路桥"],
        "stock_codes": ["000498.SZ"],
        "description": "山东省路桥工程建设骨干企业，主营公路、桥梁、隧道等交通基础设施的施工建设和养护业务。",
        "country": "CN", "province": "山东", "city": "济南市",
        "founded_year": 1994, "employee_count": 29136,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "wushang_group",
        "name_zh": "武商集团股份有限公司",
        "name_en": "Wushang Group Co., Ltd.",
        "aliases": ["武商集团"],
        "stock_codes": ["000501.SZ"],
        "description": "湖北省大型商业零售企业，主营百货商场和购物中心运营，拥有武商MALL等知名商业品牌。",
        "country": "CN", "province": "湖北", "city": "武汉市",
        "founded_year": 1991, "employee_count": 7255,
        "company_type": "public", "status": "ACTIVE",
    },
    {
        "company_id": "guoxin_health",
        "name_zh": "国新健康保障服务集团股份有限公司",
        "name_en": "Guoxin Health Management Service Group Co., Ltd.",
        "aliases": ["国新健康"],
        "stock_codes": ["000503.SZ"],
        "description": "中国健康保障服务领域的科技企业，主营业务涵盖医保基金综合管理服务、健康医疗大数据服务、医药福利管理（PBM）、商业健康保险第三方服务（TPA）及医疗人工智能服务。",
        "country": "CN", "province": "山东", "city": "青岛市",
        "founded_year": 1987, "employee_count": 1279,
        "company_type": "public", "status": "ACTIVE",
    },
]


# ============================================================
# 公司节点暴露
# ============================================================

EXPOSURES = [
    # ---- 东阿阿胶 ----
    {
        "exposure_id": "dongeejiao_manufacture_tcm",
        "company_id": "dongeejiao",
        "node_id": "traditional_chinese_medicine",
        "activity_type": "manufacture",
        "role": "阿胶及中成药制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("东阿阿胶2024年年度报告", "主要产品为阿胶及系列产品。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "dongeejiao_manufacture_supplement",
        "company_id": "dongeejiao",
        "node_id": "dietary_supplement",
        "activity_type": "manufacture",
        "role": "保健食品制造商",
        "weight": 0.7, "confidence": "HIGH",
        "evidence": [ev("东阿阿胶2024年年度报告", "主要产品包括保健食品。")],
        "status": "ACTIVE",
    },
    # ---- 徐工机械 ----
    {
        "exposure_id": "xcmg_manufacture_machinery",
        "company_id": "xcmg",
        "node_id": "construction_machinery",
        "activity_type": "manufacture",
        "role": "工程机械制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("徐工机械2024年年度报告", "主要产品包括压实机械、铲运机械、路面机械、筑路机械。")],
        "status": "ACTIVE",
    },
    # ---- 兴业银锡 ----
    {
        "exposure_id": "xingye_produce_tin",
        "company_id": "xingye_yinxin",
        "node_id": "tin_metal",
        "activity_type": "produce",
        "role": "锡金属采选冶一体化企业",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("兴业银锡2024年年度报告", "主营业务以有色金属采选、冶炼、加工、销售为主业。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xingye_produce_precious",
        "company_id": "xingye_yinxin",
        "node_id": "precious_metal",
        "activity_type": "produce",
        "role": "贵金属（银）生产商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("兴业银锡2024年年度报告", "公司名称为兴业银锡，银为主要产品之一。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "xingye_produce_lead_zinc",
        "company_id": "xingye_yinxin",
        "node_id": "lead_zinc_metal",
        "activity_type": "produce",
        "role": "铅锌金属生产商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("兴业银锡2024年年度报告", "主营业务以有色金属采选、冶炼、加工、销售为主业，所属行业为铅锌。")],
        "status": "ACTIVE",
    },
    # ---- 华天酒店 ----
    {
        "exposure_id": "huatian_operate_hotel",
        "company_id": "huatian_hotel",
        "node_id": "hotel_operation_service",
        "activity_type": "operate",
        "role": "酒店运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("华天酒店2024年年度报告", "主营业务为酒店服务。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "huatian_produce_property",
        "company_id": "huatian_hotel",
        "node_id": "residential_property",
        "activity_type": "produce",
        "role": "房地产开发商",
        "weight": 0.5, "confidence": "HIGH",
        "evidence": [ev("华天酒店2024年年度报告", "主营业务包括房地产。")],
        "status": "ACTIVE",
    },
    # ---- 粤高速A ----
    {
        "exposure_id": "expressway_operate_highway",
        "company_id": "guangdong_expressway",
        "node_id": "highway_operation_service",
        "activity_type": "operate",
        "role": "高速公路运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("粤高速A2024年年度报告", "主要业务为高速公路和特大桥梁的商业开发和经营。")],
        "status": "ACTIVE",
    },
    # ---- 张家界 ----
    {
        "exposure_id": "zhangjiajie_operate_tourism",
        "company_id": "zhangjiajie",
        "node_id": "tourism_service",
        "activity_type": "operate",
        "role": "旅游景区综合运营商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("张家界2024年年度报告", "主营业务包括旅游景区经营、旅游客运、旅行社经营、旅游客运索道经营。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "zhangjiajie_operate_hotel",
        "company_id": "zhangjiajie",
        "node_id": "hotel_operation_service",
        "activity_type": "operate",
        "role": "酒店运营商",
        "weight": 0.6, "confidence": "HIGH",
        "evidence": [ev("张家界2024年年度报告", "主营业务包括酒店经营。")],
        "status": "ACTIVE",
    },
    # ---- ST晨鸣 ----
    {
        "exposure_id": "chenming_manufacture_paper",
        "company_id": "chenming_paper",
        "node_id": "paper_product",
        "activity_type": "manufacture",
        "role": "机制纸制造商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("ST晨鸣2024年年度报告", "主要产品及劳务分别为机制纸、建筑材料、电及汽及其他。")],
        "status": "ACTIVE",
    },
    # ---- 山东路桥 ----
    {
        "exposure_id": "shandong_provide_construction",
        "company_id": "shandong_road_bridge",
        "node_id": "construction_service",
        "activity_type": "provide_service",
        "role": "路桥工程施工服务商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("山东路桥2024年年度报告", "主营业务为路桥工程施工和养护施工。")],
        "status": "ACTIVE",
    },
    # ---- 武商集团 ----
    {
        "exposure_id": "wushang_provide_retail",
        "company_id": "wushang_group",
        "node_id": "chain_retail_service",
        "activity_type": "provide_service",
        "role": "百货商业零售商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("武商集团2024年年度报告", "主要业务为商业。")],
        "status": "ACTIVE",
    },
    # ---- 国新健康 ----
    {
        "exposure_id": "guoxin_provide_health_mgmt",
        "company_id": "guoxin_health",
        "node_id": "health_management_service",
        "activity_type": "provide_service",
        "role": "健康保障服务提供商",
        "weight": 1.0, "confidence": "HIGH",
        "evidence": [ev("国新健康2024年年度报告", "主要业务涵盖医保基金综合管理服务、健康医疗大数据服务、医药福利管理服务(PBM)、商业健康保险第三方服务(TPA)、医疗人工智能服务等五大领域。")],
        "status": "ACTIVE",
    },
    {
        "exposure_id": "guoxin_provide_big_data",
        "company_id": "guoxin_health",
        "node_id": "big_data_service",
        "activity_type": "provide_service",
        "role": "健康医疗大数据服务商",
        "weight": 0.8, "confidence": "HIGH",
        "evidence": [ev("国新健康2024年年度报告", "主要业务包括健康医疗大数据服务、医疗人工智能服务。")],
        "status": "ACTIVE",
    },
]


# ============================================================
# 提交逻辑
# ============================================================

async def submit_graph_batch():
    batch = {
        "batch_id": "batch_009_industrial_graph",
        "task_description": "Batch 009: 为10家中国公司构建产业实体图，涵盖中成药、工程机械、锡金属、酒店服务、高速公路运营、旅游、机制纸、路桥工程、百货零售及健康管理服务等产业链。",
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
        "batch_id": "batch_009_company_views",
        "task_description": "Batch 009: 为10家中国公司创建公司视图，建立公司与产业节点的暴露关系。",
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
    print("Batch 009 产业图与公司视图提交")
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
