#!/usr/bin/env python3
"""
Batch 035 Submission Script
Companies: 000893, 000895, 001896, 000897, 000898, 000899, 000900, 000901, 000902, 000903
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
# 1. Industrial Graph Registration Batch (nodes + edges)
# ========================================================================
graph_batch = {
    "batch_id": "batch_035_graph",
    "task_description": "Batch 035 industrial graph nodes and edges: potassium ore, phosphate ore, aerospace products, connected vehicle devices, and related flows.",
    "nodes_to_upsert": [
        {
            "node_id": "potassium_ore",
            "canonical_name_zh": "钾盐矿石",
            "canonical_name_en": "Potassium Ore",
            "aliases": ["钾盐矿", "钾矿石"],
            "definition": "含有可溶性钾盐的矿物矿石，是生产氯化钾等钾肥产品的主要原料。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "亚钾国际主营业务分析",
                    "source_url": None,
                    "quote": "主营业务为钾盐矿开采、加工，钾肥生产及销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "phosphate_ore",
            "canonical_name_zh": "磷矿石",
            "canonical_name_en": "Phosphate Ore",
            "aliases": ["磷矿", "磷酸盐矿"],
            "definition": "含有磷酸盐矿物的矿石，是生产磷肥、复合肥及磷化工产品的基础原料。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新洋丰主营业务分析",
                    "source_url": None,
                    "quote": "主要业务:磷复肥、新型肥料的研发、生产和销售"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "aerospace_application_product",
            "canonical_name_zh": "航天应用产品",
            "canonical_name_en": "Aerospace Application Product",
            "aliases": ["航天应用设备", "航天产品"],
            "definition": "基于航天技术开发的终端应用产品，包括卫星导航、遥感设备、航天测控终端等。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "航天科技主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "connected_vehicle_device",
            "canonical_name_zh": "车联网设备",
            "canonical_name_en": "Connected Vehicle Device",
            "aliases": ["车载联网设备", "V2X设备"],
            "definition": "用于实现车辆与外部环境（车、路、人、云）信息交互的智能车载通信与感知设备。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "航天科技主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "flow_potassium_ore_to_chloride",
            "from_node": "potassium_ore",
            "to_node": "potassium_chloride",
            "edge_type": "material_flow",
            "description": "钾盐矿石经过开采和加工，生产出氯化钾产品。",
            "evidence": [
                {
                    "source_title": "亚钾国际主营业务分析",
                    "source_url": None,
                    "quote": "主营业务为钾盐矿开采、加工，钾肥生产及销售"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "flow_phosphate_ore_to_compound_fertilizer",
            "from_node": "phosphate_ore",
            "to_node": "compound_fertilizer",
            "edge_type": "material_flow",
            "description": "磷矿石经过加工处理，用于生产复合肥等磷肥产品。",
            "evidence": [
                {
                    "source_title": "新洋丰主营业务分析",
                    "source_url": None,
                    "quote": "主要业务:磷复肥、新型肥料的研发、生产和销售"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "flow_iron_ore_to_steel_plate",
            "from_node": "iron_ore",
            "to_node": "steel_plate",
            "edge_type": "material_flow",
            "description": "铁矿石经过冶炼和轧制，生产出钢板产品。",
            "evidence": [
                {
                    "source_title": "鞍钢股份主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:热轧板、冷轧板、镀锌板、彩涂板、中厚板"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "flow_iron_ore_to_steel_bar",
            "from_node": "iron_ore",
            "to_node": "steel_bar",
            "edge_type": "material_flow",
            "description": "铁矿石经过冶炼和轧制，生产出钢筋/棒材产品。",
            "evidence": [
                {
                    "source_title": "鞍钢股份主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:大型材、重轨、线材、无缝钢管"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "ontology",
            "edge_id": "compound_fertilizer_is_a_chemical_fertilizer",
            "from_node": "compound_fertilizer",
            "to_node": "chemical_fertilizer",
            "edge_type": "is_a",
            "description": "复合肥是一种化学肥料，含有两种或两种以上营养元素。",
            "evidence": [
                {
                    "source_title": "化肥分类常识",
                    "source_url": None,
                    "quote": "复合肥是指含有氮、磷、钾三种元素中至少两种的化学肥料"
                }
            ],
            "confidence": "HIGH",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "aerospace_product_to_satellite_comm",
            "from_node": "aerospace_application_product",
            "to_node": "satellite_communication",
            "edge_type": "composition",
            "description": "航天应用产品（如通信终端、测控设备）构成卫星通信系统的关键组成部分。",
            "evidence": [
                {
                    "source_title": "航天科技主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"
                }
            ],
            "confidence": "MEDIUM",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "connected_vehicle_to_automotive_electronics",
            "from_node": "connected_vehicle_device",
            "to_node": "automotive_electronics",
            "edge_type": "composition",
            "description": "车联网设备是汽车电子系统的组成部分，实现车辆的网联化功能。",
            "evidence": [
                {
                    "source_title": "航天科技主营业务分析",
                    "source_url": None,
                    "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"
                }
            ],
            "confidence": "MEDIUM",
        },
    ],
    "rejected_or_pending": [],
}

print("[1/2] Submitting graph batch...")
graph_result = api_post("/batches", graph_batch)
print(f"Graph batch result: nodes={graph_result.get('nodes_created',0)}, edges={graph_result.get('edges_created',0)}")

# ========================================================================
# 2. Business Registration Batch (companies + exposures)
# ========================================================================
business_batch = {
    "batch_id": "batch_035_business",
    "task_description": "Batch 035 company registrations and node exposures for 10 listed companies.",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        {
            "company_id": "asia_potash",
            "name_zh": "亚钾国际投资(广州)股份有限公司",
            "aliases": ["亚钾国际"],
            "stock_codes": ["000893.SZ"],
            "description": "钾盐矿开采、加工及钾肥生产销售企业",
            "country": "CN",
            "province": "广东",
            "city": "广州",
            "employee_count": 5808,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "shuanghui_dev",
            "name_zh": "河南双汇投资发展股份有限公司",
            "aliases": ["双汇发展"],
            "stock_codes": ["000895.SZ"],
            "description": "高温肉制品、低温肉制品及鲜冻猪产品生产销售企业",
            "country": "CN",
            "province": "河南",
            "city": "漯河",
            "employee_count": 46352,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "yuneng_holdings",
            "name_zh": "河南豫能控股股份有限公司",
            "aliases": ["豫能控股"],
            "stock_codes": ["001896.SZ"],
            "description": "火电项目投资管理和能源销售企业",
            "country": "CN",
            "province": "河南",
            "city": "郑州",
            "employee_count": 3457,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "tianjin_jinbin",
            "name_zh": "天津津滨发展股份有限公司",
            "aliases": ["津滨发展"],
            "stock_codes": ["000897.SZ"],
            "description": "商品销售、房屋租赁及房地产开发企业",
            "country": "CN",
            "province": "天津",
            "city": "天津",
            "employee_count": 297,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "angang_steel",
            "name_zh": "鞍钢股份有限公司",
            "aliases": ["鞍钢股份"],
            "stock_codes": ["000898.SZ"],
            "description": "热轧板、冷轧板、镀锌板、彩涂板、中厚板、大型材、重轨、线材、无缝钢管、冷轧硅钢等综合钢铁生产企业",
            "country": "CN",
            "province": "辽宁",
            "city": "鞍山",
            "employee_count": 23990,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "ganeng_power",
            "name_zh": "江西赣能股份有限公司",
            "aliases": ["赣能股份"],
            "stock_codes": ["000899.SZ"],
            "description": "火力发电和水力发电企业",
            "country": "CN",
            "province": "江西",
            "city": "南昌",
            "employee_count": 1022,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "modern_investment",
            "name_zh": "现代投资股份有限公司",
            "aliases": ["现代投资"],
            "stock_codes": ["000900.SZ"],
            "description": "高等级公路经营和投资企业",
            "country": "CN",
            "province": "湖南",
            "city": "长沙",
            "employee_count": 2767,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "aerospace_tech",
            "name_zh": "航天科技控股集团股份有限公司",
            "aliases": ["航天科技"],
            "stock_codes": ["000901.SZ"],
            "description": "车联网及工业物联网、航天应用产品、汽车电子、电力设备研发生产企业",
            "country": "CN",
            "province": "黑龙江",
            "city": "哈尔滨",
            "employee_count": 6043,
            "company_type": "state_owned",
            "status": "ACTIVE",
        },
        {
            "company_id": "xinyangfeng",
            "name_zh": "新洋丰农业科技股份有限公司",
            "aliases": ["新洋丰"],
            "stock_codes": ["000902.SZ"],
            "description": "磷复肥、新型肥料研发、生产和销售企业",
            "country": "CN",
            "province": "湖北",
            "city": "荆门",
            "employee_count": 8315,
            "company_type": "public",
            "status": "ACTIVE",
        },
        {
            "company_id": "st_yundong",
            "name_zh": "昆明云内动力股份有限公司",
            "aliases": ["ST云动", "云内动力"],
            "stock_codes": ["000903.SZ"],
            "description": "柴油发动机及柴油机配件生产企业",
            "country": "CN",
            "province": "云南",
            "city": "昆明",
            "employee_count": 2594,
            "company_type": "public",
            "status": "ACTIVE",
        },
    ],
    "company_node_exposures_to_upsert": [
        # 亚钾国际
        {
            "exposure_id": "asia_potash_produce_potassium_chloride",
            "company_id": "asia_potash",
            "node_id": "potassium_chloride",
            "activity_type": "produce",
            "role": "氯化钾生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "亚钾国际主营业务", "quote": "主营业务为钾盐矿开采、加工，钾肥生产及销售"}],
        },
        {
            "exposure_id": "asia_potash_produce_chemical_fertilizer",
            "company_id": "asia_potash",
            "node_id": "chemical_fertilizer",
            "activity_type": "produce",
            "role": "化肥生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "亚钾国际主营业务", "quote": "主营业务为钾盐矿开采、加工，钾肥生产及销售"}],
        },
        # 双汇发展
        {
            "exposure_id": "shuanghui_produce_meat_product",
            "company_id": "shuanghui_dev",
            "node_id": "meat_product",
            "activity_type": "produce",
            "role": "肉类产品生产商",
            "weight": 0.95,
            "confidence": "HIGH",
            "evidence": [{"source_title": "双汇发展主营业务", "quote": "主要产品:高温肉制品、低温肉制品、鲜冻猪产品"}],
        },
        # 豫能控股
        {
            "exposure_id": "yuneng_operate_coal_power",
            "company_id": "yuneng_holdings",
            "node_id": "coal_power_generation",
            "activity_type": "operate",
            "role": "火电运营商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "豫能控股主营业务", "quote": "主要业务:火电项目的投资管理、能源销售、新能源项目投资建设"}],
        },
        {
            "exposure_id": "yuneng_operate_hydro_power",
            "company_id": "yuneng_holdings",
            "node_id": "hydro_power_generation",
            "activity_type": "operate",
            "role": "水电运营商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "豫能控股主营业务", "quote": "主要业务:火电项目的投资管理、能源销售、新能源项目投资建设"}],
        },
        # 津滨发展
        {
            "exposure_id": "jinbin_operate_real_estate",
            "company_id": "tianjin_jinbin",
            "node_id": "real_estate_development",
            "activity_type": "operate",
            "role": "房地产开发商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "津滨发展主营业务", "quote": "主要业务:商品销售、房屋租赁、房屋土地销售"}],
        },
        # 鞍钢股份
        {
            "exposure_id": "angang_produce_steel_plate",
            "company_id": "angang_steel",
            "node_id": "steel_plate",
            "activity_type": "produce",
            "role": "钢板生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鞍钢股份主营业务", "quote": "主要产品:热轧板、冷轧板、镀锌板、彩涂板、中厚板"}],
        },
        {
            "exposure_id": "angang_produce_steel_bar",
            "company_id": "angang_steel",
            "node_id": "steel_bar",
            "activity_type": "produce",
            "role": "棒材/钢筋生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "鞍钢股份主营业务", "quote": "主要产品:大型材、重轨、线材、无缝钢管"}],
        },
        {
            "exposure_id": "angang_produce_special_steel",
            "company_id": "angang_steel",
            "node_id": "special_steel",
            "activity_type": "produce",
            "role": "特钢生产商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "鞍钢股份主营业务", "quote": "主要产品:冷轧硅钢等"}],
        },
        # 赣能股份
        {
            "exposure_id": "ganeng_operate_coal_power",
            "company_id": "ganeng_power",
            "node_id": "coal_power_generation",
            "activity_type": "operate",
            "role": "火电运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "赣能股份主营业务", "quote": "主要业务:火力、水力发电"}],
        },
        {
            "exposure_id": "ganeng_operate_hydro_power",
            "company_id": "ganeng_power",
            "node_id": "hydro_power_generation",
            "activity_type": "operate",
            "role": "水电运营商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "赣能股份主营业务", "quote": "主要业务:火力、水力发电"}],
        },
        {
            "exposure_id": "ganeng_produce_electricity",
            "company_id": "ganeng_power",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "赣能股份主营业务", "quote": "主要业务:火力、水力发电"}],
        },
        # 现代投资
        {
            "exposure_id": "modern_operate_highway",
            "company_id": "modern_investment",
            "node_id": "highway_operation_service",
            "activity_type": "operate",
            "role": "高速公路运营商",
            "weight": 0.95,
            "confidence": "HIGH",
            "evidence": [{"source_title": "现代投资主营业务", "quote": "主要业务:经营高等级公路"}],
        },
        # 航天科技
        {
            "exposure_id": "aerospace_manufacture_auto_electronics",
            "company_id": "aerospace_tech",
            "node_id": "automotive_electronics",
            "activity_type": "manufacture",
            "role": "汽车电子制造商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天科技主营业务", "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"}],
        },
        {
            "exposure_id": "aerospace_manufacture_aerospace_product",
            "company_id": "aerospace_tech",
            "node_id": "aerospace_application_product",
            "activity_type": "manufacture",
            "role": "航天应用产品制造商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航天科技主营业务", "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"}],
        },
        {
            "exposure_id": "aerospace_manufacture_connected_vehicle",
            "company_id": "aerospace_tech",
            "node_id": "connected_vehicle_device",
            "activity_type": "manufacture",
            "role": "车联网设备制造商",
            "weight": 0.75,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "航天科技主营业务", "quote": "主要产品:车联网及工业物联网、航天应用产品、汽车电子、电力设备"}],
        },
        # 新洋丰
        {
            "exposure_id": "xinyangfeng_produce_compound_fertilizer",
            "company_id": "xinyangfeng",
            "node_id": "compound_fertilizer",
            "activity_type": "produce",
            "role": "复合肥生产商",
            "weight": 0.95,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新洋丰主营业务", "quote": "主要业务:磷复肥、新型肥料的研发、生产和销售"}],
        },
        {
            "exposure_id": "xinyangfeng_produce_chemical_fertilizer",
            "company_id": "xinyangfeng",
            "node_id": "chemical_fertilizer",
            "activity_type": "produce",
            "role": "化肥生产商",
            "weight": 0.85,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新洋丰主营业务", "quote": "主要业务:磷复肥、新型肥料的研发、生产和销售"}],
        },
        # ST云动
        {
            "exposure_id": "yundong_manufacture_diesel_engine",
            "company_id": "st_yundong",
            "node_id": "diesel_engine",
            "activity_type": "manufacture",
            "role": "柴油发动机制造商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST云动主营业务", "quote": "主要产品:系列柴油机、柴油机配件及其他轻卡、农用运输车"}],
        },
        {
            "exposure_id": "yundong_manufacture_automotive_part",
            "company_id": "st_yundong",
            "node_id": "automotive_part",
            "activity_type": "manufacture",
            "role": "汽车配件制造商",
            "weight": 0.7,
            "confidence": "MEDIUM",
            "evidence": [{"source_title": "ST云动主营业务", "quote": "主要产品:系列柴油机、柴油机配件及其他轻卡、农用运输车"}],
        },
    ],
}

print("[2/2] Submitting business batch...")
business_result = api_post("/business-batches", business_batch)
print(f"Business batch result: companies={business_result.get('companies_created',0)}, exposures={business_result.get('exposures_created',0)}")

print("\nBatch 035 submission complete!")
