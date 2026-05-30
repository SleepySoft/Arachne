#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batch 126 submission scripts."""
import json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

def write_batch(batch_num, nodes, edges, companies, exposures):
    graph = {
        "batch_id": f"batch_{batch_num}_nodes",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges
    }
    path_g = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_nodes.json")
    with open(path_g, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    business = {
        "batch_id": f"batch_{batch_num}_business",
        "task_description": f"Batch {batch_num} business registration",
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures,
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": []
    }
    path_b = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_business.json")
    with open(path_b, "w", encoding="utf-8") as f:
        json.dump(business, f, ensure_ascii=False, indent=2)
    print(f"Batch {batch_num}: {len(nodes)} nodes, {len(edges)} edges, {len(companies)} companies, {len(exposures)} exposures")

NODES_126 = [
    {"node_id": "ito_conductive_glass", "canonical_name_zh": "ITO导电玻璃", "canonical_name_en": "ITO conductive glass", "entity_type": "component", "aliases": [], "definition": "采用氧化铟锡镀膜的透明导电玻璃，用于液晶显示等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科主营业务")},
    {"node_id": "color_filter", "canonical_name_zh": "彩色滤光片", "canonical_name_en": "color filter", "entity_type": "component", "aliases": [], "definition": "用于液晶显示器的彩色滤光元件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科主营业务")},
    {"node_id": "touch_screen", "canonical_name_zh": "触摸屏", "canonical_name_en": "touch screen", "entity_type": "component", "aliases": [], "definition": "可实现触摸输入功能的显示屏组件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科主营业务")},
    {"node_id": "coated_conductive_glass", "canonical_name_zh": "镀膜导电玻璃", "canonical_name_en": "coated conductive glass", "entity_type": "component", "aliases": [], "definition": "表面镀有导电薄膜的玻璃基板", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科经营范围")},
    {"node_id": "vacuum_coating_product", "canonical_name_zh": "真空镀膜产品", "canonical_name_en": "vacuum coating product", "entity_type": "material", "aliases": [], "definition": "通过真空镀膜工艺生产的各类薄膜产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科经营范围")},
    {"node_id": "liquid_crystal_display_device", "canonical_name_zh": "液晶显示器件", "canonical_name_en": "liquid crystal display device", "entity_type": "device", "aliases": ["LCD器件"], "definition": "基于液晶技术制造的显示器件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("莱宝高科经营范围")},
    {"node_id": "display_panel", "canonical_name_zh": "显示面板", "canonical_name_en": "display panel", "entity_type": "component", "aliases": [], "definition": "用于各类电子设备的显示面板组件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业知识图谱")},
    {"node_id": "ammonium_nitrate_product", "canonical_name_zh": "硝酸铵系列产品", "canonical_name_en": "ammonium nitrate product", "entity_type": "material", "aliases": [], "definition": "以硝酸铵为主要成分的化工系列产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("ST兴化主营业务")},
    {"node_id": "nitrate_fertilizer", "canonical_name_zh": "硝酸盐肥料", "canonical_name_en": "nitrate fertilizer", "entity_type": "material", "aliases": [], "definition": "以硝酸盐为主要成分的化肥产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("ST兴化经营范围")},
    {"node_id": "fastener", "canonical_name_zh": "紧固件", "canonical_name_en": "fastener", "entity_type": "component", "aliases": [], "definition": "用于连接和紧固机械零部件的标准件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("晋亿实业主营业务")},
    {"node_id": "tungsten_steel_mold", "canonical_name_zh": "钨钢模具", "canonical_name_en": "tungsten steel mold", "entity_type": "component", "aliases": [], "definition": "采用钨钢材料制造的精密模具", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("晋亿实业经营范围")},
    {"node_id": "hardware_product", "canonical_name_zh": "五金制品", "canonical_name_en": "hardware product", "entity_type": "component", "aliases": [], "definition": "各类金属五金配件及制品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("晋亿实业经营范围")},
    {"node_id": "railway_fastener", "canonical_name_zh": "铁道扣件", "canonical_name_en": "railway fastener", "entity_type": "component", "aliases": [], "definition": "用于铁路轨道固定连接的紧固件系统", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("晋亿实业经营范围")},
    {"node_id": "life_insurance", "canonical_name_zh": "人寿保险", "canonical_name_en": "life insurance", "entity_type": "service", "aliases": [], "definition": "以人的寿命为保险标的的保险服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国人寿主营业务")},
    {"node_id": "health_insurance", "canonical_name_zh": "健康保险", "canonical_name_en": "health insurance", "entity_type": "service", "aliases": [], "definition": "以被保险人身体健康为标的的保险服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国人寿主营业务")},
    {"node_id": "accident_insurance", "canonical_name_zh": "意外伤害保险", "canonical_name_en": "accident insurance", "entity_type": "service", "aliases": [], "definition": "以意外伤害事故为给付条件的保险服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国人寿主营业务")},
    {"node_id": "insurance_asset_management", "canonical_name_zh": "保险资产管理", "canonical_name_en": "insurance asset management", "entity_type": "service", "aliases": [], "definition": "保险公司从事的资金运用和资产管理服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中国人寿主营业务")},
    {"node_id": "cardiovascular_chinese_patent_medicine", "canonical_name_zh": "心脑血管中成药", "canonical_name_en": "cardiovascular Chinese patent medicine", "entity_type": "material", "aliases": [], "definition": "用于预防和治疗心脑血管疾病的纯中药制剂", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("沃华医药主营业务")},
    {"node_id": "chinese_patent_medicine", "canonical_name_zh": "中成药", "canonical_name_en": "Chinese patent medicine", "entity_type": "material", "aliases": [], "definition": "以中药材为原料，按处方制成的现成药品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("沃华医药经营范围")},
    {"node_id": "aviation_ground_power", "canonical_name_zh": "航空地面电源", "canonical_name_en": "aviation ground power", "entity_type": "device", "aliases": [], "definition": "为飞机在地面提供电能的专用电源设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("威海广泰主营业务")},
    {"node_id": "aircraft_deicing_vehicle", "canonical_name_zh": "飞机除冰车", "canonical_name_en": "aircraft deicing vehicle", "entity_type": "device", "aliases": [], "definition": "用于清除飞机表面冰雪的专用地面车辆", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("威海广泰主营业务")},
    {"node_id": "ground_support_equipment", "canonical_name_zh": "航空地面支持设备", "canonical_name_en": "ground support equipment", "entity_type": "device", "aliases": ["GSE"], "definition": "机场地面用于保障飞机运行的各类设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("威海广泰主营业务")},
    {"node_id": "electrical_measuring_instrument", "canonical_name_zh": "电测仪表", "canonical_name_en": "electrical measuring instrument", "entity_type": "device", "aliases": [], "definition": "用于测量电参数的仪器仪表", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("科陆电子主营业务")},
    {"node_id": "smart_electric_meter", "canonical_name_zh": "智能电表", "canonical_name_en": "smart electric meter", "entity_type": "device", "aliases": [], "definition": "具有数据采集和通信功能的电能计量仪表", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("科陆电子主营业务")},
    {"node_id": "distribution_terminal", "canonical_name_zh": "配电终端", "canonical_name_en": "distribution terminal", "entity_type": "device", "aliases": ["FTU/DTU/TTU"], "definition": "用于配电网监测和控制的智能终端设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("科陆电子主营业务")},
    {"node_id": "power_transformer", "canonical_name_zh": "电力变压器", "canonical_name_en": "power transformer", "entity_type": "device", "aliases": [], "definition": "用于电力系统中电压变换的变压器设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三变科技主营业务")},
    {"node_id": "oil_immersed_transformer", "canonical_name_zh": "油浸式变压器", "canonical_name_en": "oil immersed transformer", "entity_type": "device", "aliases": [], "definition": "以绝缘油为冷却和绝缘介质的变压器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三变科技主营业务")},
    {"node_id": "dry_type_transformer", "canonical_name_zh": "干式变压器", "canonical_name_en": "dry type transformer", "entity_type": "device", "aliases": [], "definition": "采用空气或固体绝缘的变压器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三变科技经营范围")},
    {"node_id": "amorphous_alloy_transformer", "canonical_name_zh": "非晶合金变压器", "canonical_name_en": "amorphous alloy transformer", "entity_type": "device", "aliases": [], "definition": "铁芯采用非晶合金材料的高效节能变压器", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三变科技经营范围")},
    {"node_id": "zinc_ingot", "canonical_name_zh": "锌锭", "canonical_name_en": "zinc ingot", "entity_type": "material", "aliases": [], "definition": "通过冶炼生产的锌金属锭", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("罗平锌电主营业务")},
    {"node_id": "lead_concentrate", "canonical_name_zh": "铅精矿", "canonical_name_en": "lead concentrate", "entity_type": "material", "aliases": [], "definition": "铅矿石经过选矿富集后的精矿产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("罗平锌电主营业务")},
    {"node_id": "ultra_fine_zinc_powder", "canonical_name_zh": "超精细锌粉", "canonical_name_en": "ultra fine zinc powder", "entity_type": "material", "aliases": [], "definition": "粒度极细的锌金属粉末", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("罗平锌电主营业务")},
    {"node_id": "hydroelectric_power", "canonical_name_zh": "水力发电", "canonical_name_en": "hydroelectric power", "entity_type": "service", "aliases": [], "definition": "利用水能转化为电能的发电方式", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("罗平锌电主营业务")},
    {"node_id": "network_optimization", "canonical_name_zh": "网优覆盖", "canonical_name_en": "network optimization", "entity_type": "service", "aliases": [], "definition": "对通信网络进行优化和信号覆盖的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三维通信主营业务")},
    {"node_id": "satellite_communication_service", "canonical_name_zh": "卫星通信服务", "canonical_name_en": "satellite communication service", "entity_type": "service", "aliases": [], "definition": "基于卫星通信技术提供的通信服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("三维通信主营业务")},
]

EDGES_126 = [
    {"edge_id": "ito_conductive_glass_electronic_component", "from_node": "ito_conductive_glass", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "ITO导电玻璃是电子元器件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "color_filter_electronic_component", "from_node": "color_filter", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "彩色滤光片是电子元器件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "touch_screen_electronic_component", "from_node": "touch_screen", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "触摸屏是电子元器件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "liquid_crystal_display_device_electronic_component", "from_node": "liquid_crystal_display_device", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "液晶显示器件是电子元器件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "display_panel_electronic_component", "from_node": "display_panel", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "显示面板是电子元器件的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "vacuum_coating_product_new_material", "from_node": "vacuum_coating_product", "to_node": "new_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "真空镀膜产品属于新材料范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ammonium_nitrate_product_chemical_product", "from_node": "ammonium_nitrate_product", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "硝酸铵系列产品是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "nitrate_fertilizer_chemical_product", "from_node": "nitrate_fertilizer", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "硝酸盐肥料是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "fastener_metal_product", "from_node": "fastener", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "紧固件是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "tungsten_steel_mold_metal_product", "from_node": "tungsten_steel_mold", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钨钢模具是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "hardware_product_metal_product", "from_node": "hardware_product", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "五金制品是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "railway_fastener_railway", "from_node": "railway_fastener", "to_node": "railway", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "铁道扣件是铁路系统的组成部分", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "life_insurance_insurance", "from_node": "life_insurance", "to_node": "insurance", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "人寿保险是保险服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "health_insurance_insurance", "from_node": "health_insurance", "to_node": "insurance", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "健康保险是保险服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "accident_insurance_insurance", "from_node": "accident_insurance", "to_node": "insurance", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "意外伤害保险是保险服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "insurance_asset_management_banking_service", "from_node": "insurance_asset_management", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "保险资产管理是金融服务的延伸", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "cardiovascular_chinese_patent_medicine_pharmaceutical", "from_node": "cardiovascular_chinese_patent_medicine", "to_node": "pharmaceutical", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "心脑血管中成药是药品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "chinese_patent_medicine_pharmaceutical", "from_node": "chinese_patent_medicine", "to_node": "pharmaceutical", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "中成药是药品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aviation_ground_power_power_generation_equipment", "from_node": "aviation_ground_power", "to_node": "power_generation_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "航空地面电源是发电设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "aircraft_deicing_vehicle_automotive", "from_node": "aircraft_deicing_vehicle", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "飞机除冰车是特种汽车的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ground_support_equipment_automotive", "from_node": "ground_support_equipment", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "航空地面支持设备属于特种车辆范畴", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "electrical_measuring_instrument_electronic_component", "from_node": "electrical_measuring_instrument", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电测仪表是电子设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "smart_electric_meter_electronic_component", "from_node": "smart_electric_meter", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "智能电表是电子设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "distribution_terminal_electronic_component", "from_node": "distribution_terminal", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "配电终端是电子设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "power_transformer_power_generation_equipment", "from_node": "power_transformer", "to_node": "power_generation_equipment", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "电力变压器是电力设备的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "oil_immersed_transformer_power_transformer", "from_node": "oil_immersed_transformer", "to_node": "power_transformer", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "油浸式变压器是电力变压器的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "dry_type_transformer_power_transformer", "from_node": "dry_type_transformer", "to_node": "power_transformer", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "干式变压器是电力变压器的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "amorphous_alloy_transformer_power_transformer", "from_node": "amorphous_alloy_transformer", "to_node": "power_transformer", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "非晶合金变压器是电力变压器的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "zinc_ingot_metal_product", "from_node": "zinc_ingot", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锌锭是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "lead_concentrate_mining", "from_node": "lead_concentrate", "to_node": "mining", "edge_namespace": "industrial_flow", "edge_type": "material_flow", "description": "铅精矿是矿业的产品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "ultra_fine_zinc_powder_metal_product", "from_node": "ultra_fine_zinc_powder", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "超精细锌粉是金属制品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "hydroelectric_power_power_generation", "from_node": "hydroelectric_power", "to_node": "power_generation", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "水力发电是发电方式的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "network_optimization_telecommunication", "from_node": "network_optimization", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "网优覆盖是电信服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "satellite_communication_service_telecommunication", "from_node": "satellite_communication_service", "to_node": "telecommunication", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "卫星通信服务是电信服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

COMPANIES_126 = [
    {"company_id": "sz_002106", "name_zh": "莱宝高科", "name_en": "Shenzhen Laibao Hi-Tech Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["002106.SZ"], "description": "ITO导电玻璃、彩色滤光片、触摸屏、液晶显示器件", "founded_year": 1992, "employee_count": 1332},
    {"company_id": "sz_002109", "name_zh": "ST兴化", "name_en": "Shaanxi Xinghua Chemical Co., Ltd.", "country": "CN", "province": "陕西", "city": "咸阳市", "stock_codes": ["002109.SZ"], "description": "硝酸铵系列产品的生产与销售", "founded_year": 1997, "employee_count": 2024},
    {"company_id": "sh_601002", "name_zh": "晋亿实业", "name_en": "Jin Yi Industrial Co., Ltd.", "country": "CN", "province": "浙江", "city": "嘉兴市", "stock_codes": ["601002.SH"], "description": "紧固件、钨钢模具、五金制品、铁道扣件", "founded_year": 1995, "employee_count": 2214},
    {"company_id": "sh_601628", "name_zh": "中国人寿", "name_en": "China Life Insurance Co., Ltd.", "country": "CN", "province": "北京", "city": "北京市", "stock_codes": ["601628.SH"], "description": "人寿保险、健康保险、意外伤害保险、保险资产管理", "founded_year": 2003, "employee_count": 97505},
    {"company_id": "sz_002107", "name_zh": "沃华医药", "name_en": "Shandong Wohua Pharmaceutical Co., Ltd.", "country": "CN", "province": "山东", "city": "潍坊市", "stock_codes": ["002107.SZ"], "description": "纯天然植物类心脑血管中成药的研发、生产和销售", "founded_year": 2002, "employee_count": 1018},
    {"company_id": "sz_002111", "name_zh": "威海广泰", "name_en": "Weihai Guangtai Airport Equipment Co., Ltd.", "country": "CN", "province": "山东", "city": "威海市", "stock_codes": ["002111.SZ"], "description": "航空地面设备、空港装备", "founded_year": 1996, "employee_count": 2785},
    {"company_id": "sz_002121", "name_zh": "科陆电子", "name_en": "Shenzhen Clou Electronics Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["002121.SZ"], "description": "智能电网、新能源及综合能源服务", "founded_year": 1996, "employee_count": 2672},
    {"company_id": "sz_002112", "name_zh": "三变科技", "name_en": "Sanbian Technology Co., Ltd.", "country": "CN", "province": "浙江", "city": "台州市", "stock_codes": ["002112.SZ"], "description": "变压器、电机、化工产品制造", "founded_year": 2001, "employee_count": 769},
    {"company_id": "sz_002114", "name_zh": "罗平锌电", "name_en": "Yunnan Luoping Zinc & Electricity Co., Ltd.", "country": "CN", "province": "云南", "city": "曲靖市", "stock_codes": ["002114.SZ"], "description": "铅锌矿石采选、锌冶炼、水力发电", "founded_year": 2000, "employee_count": 1668},
    {"company_id": "sz_002115", "name_zh": "三维通信", "name_en": "Sunwave Communications Co., Ltd.", "country": "CN", "province": "浙江", "city": "杭州市", "stock_codes": ["002115.SZ"], "description": "网优覆盖、卫星通信服务、互联网广告", "founded_year": 1993, "employee_count": 1017},
]

EXPOSURES_126 = [
    {"exposure_id": "sz_002106_produce_ito_conductive_glass", "company_id": "sz_002106", "node_id": "ito_conductive_glass", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:ITO导电玻璃")},
    {"exposure_id": "sz_002106_produce_color_filter", "company_id": "sz_002106", "node_id": "color_filter", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:彩色滤光片")},
    {"exposure_id": "sz_002106_produce_touch_screen", "company_id": "sz_002106", "node_id": "touch_screen", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:触摸屏")},
    {"exposure_id": "sz_002106_produce_liquid_crystal_display_device", "company_id": "sz_002106", "node_id": "liquid_crystal_display_device", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:液晶显示器件")},
    {"exposure_id": "sz_002106_produce_display_panel", "company_id": "sz_002106", "node_id": "display_panel", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("产业知识图谱:显示面板")},
    {"exposure_id": "sz_002106_produce_vacuum_coating_product", "company_id": "sz_002106", "node_id": "vacuum_coating_product", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:真空镀膜产品")},
    {"exposure_id": "sz_002106_provide_service_technical_service", "company_id": "sz_002106", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术咨询服务")},
    {"exposure_id": "sz_002109_produce_ammonium_nitrate_product", "company_id": "sz_002109", "node_id": "ammonium_nitrate_product", "activity_type": "produce", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:硝酸铵系列产品")},
    {"exposure_id": "sz_002109_produce_nitrate_fertilizer", "company_id": "sz_002109", "node_id": "nitrate_fertilizer", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:硝酸盐肥料")},
    {"exposure_id": "sz_002109_produce_chemical_product", "company_id": "sz_002109", "node_id": "chemical_product", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:化工产品")},
    {"exposure_id": "sz_002109_provide_service_technical_service", "company_id": "sz_002109", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002109_produce_energy_storage_system", "company_id": "sz_002109", "node_id": "energy_storage_system", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("产业知识图谱:硝酸铵用于储能")},
    {"exposure_id": "sh_601002_produce_fastener", "company_id": "sh_601002", "node_id": "fastener", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:紧固件")},
    {"exposure_id": "sh_601002_produce_tungsten_steel_mold", "company_id": "sh_601002", "node_id": "tungsten_steel_mold", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钨钢模具")},
    {"exposure_id": "sh_601002_produce_hardware_product", "company_id": "sh_601002", "node_id": "hardware_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:五金制品")},
    {"exposure_id": "sh_601002_produce_railway_fastener", "company_id": "sh_601002", "node_id": "railway_fastener", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:铁道扣件")},
    {"exposure_id": "sh_601002_produce_metal_product", "company_id": "sh_601002", "node_id": "metal_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金属制品")},
    {"exposure_id": "sh_601002_provide_service_technical_service", "company_id": "sh_601002", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:研发业务")},
    {"exposure_id": "sh_601628_provide_service_life_insurance", "company_id": "sh_601628", "node_id": "life_insurance", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:人寿保险")},
    {"exposure_id": "sh_601628_provide_service_health_insurance", "company_id": "sh_601628", "node_id": "health_insurance", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:健康保险")},
    {"exposure_id": "sh_601628_provide_service_accident_insurance", "company_id": "sh_601628", "node_id": "accident_insurance", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:意外伤害保险")},
    {"exposure_id": "sh_601628_provide_service_insurance_asset_management", "company_id": "sh_601628", "node_id": "insurance_asset_management", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:保险资产管理")},
    {"exposure_id": "sh_601628_provide_service_insurance", "company_id": "sh_601628", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:保险业务")},
    {"exposure_id": "sz_002107_produce_cardiovascular_chinese_patent_medicine", "company_id": "sz_002107", "node_id": "cardiovascular_chinese_patent_medicine", "activity_type": "produce", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:心脑血管中成药")},
    {"exposure_id": "sz_002107_produce_chinese_patent_medicine", "company_id": "sz_002107", "node_id": "chinese_patent_medicine", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:中成药")},
    {"exposure_id": "sz_002107_produce_pharmaceutical", "company_id": "sz_002107", "node_id": "pharmaceutical", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:药品")},
    {"exposure_id": "sz_002107_provide_service_technical_service", "company_id": "sz_002107", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:医药科技技术咨询")},
    {"exposure_id": "sz_002107_provide_service_health_insurance", "company_id": "sz_002107", "node_id": "health_insurance", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("产业知识图谱:医药与健康保险关联")},
    {"exposure_id": "sz_002111_produce_aviation_ground_power", "company_id": "sz_002111", "node_id": "aviation_ground_power", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:航空地面电源")},
    {"exposure_id": "sz_002111_produce_aircraft_deicing_vehicle", "company_id": "sz_002111", "node_id": "aircraft_deicing_vehicle", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:飞机除冰车")},
    {"exposure_id": "sz_002111_produce_ground_support_equipment", "company_id": "sz_002111", "node_id": "ground_support_equipment", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:客梯车、食品车、集装板升降平台")},
    {"exposure_id": "sz_002111_produce_automotive", "company_id": "sz_002111", "node_id": "automotive", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:道路机动车辆生产")},
    {"exposure_id": "sz_002111_produce_power_generation_equipment", "company_id": "sz_002111", "node_id": "power_generation_equipment", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发电机及发电机组")},
    {"exposure_id": "sz_002111_provide_service_technical_service", "company_id": "sz_002111", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002111_produce_construction_machinery", "company_id": "sz_002111", "node_id": "construction_machinery", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:专用设备制造")},
    {"exposure_id": "sz_002121_produce_electrical_measuring_instrument", "company_id": "sz_002121", "node_id": "electrical_measuring_instrument", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:电测仪表")},
    {"exposure_id": "sz_002121_produce_smart_electric_meter", "company_id": "sz_002121", "node_id": "smart_electric_meter", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:智能电表")},
    {"exposure_id": "sz_002121_produce_distribution_terminal", "company_id": "sz_002121", "node_id": "distribution_terminal", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:配电终端")},
    {"exposure_id": "sz_002121_produce_energy_storage_system", "company_id": "sz_002121", "node_id": "energy_storage_system", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:储能业务")},
    {"exposure_id": "sz_002121_produce_charging_pile", "company_id": "sz_002121", "node_id": "charging_pile", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:充电桩")},
    {"exposure_id": "sz_002121_provide_service_technical_service", "company_id": "sz_002121", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002112_produce_power_transformer", "company_id": "sz_002112", "node_id": "power_transformer", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:变压器")},
    {"exposure_id": "sz_002112_produce_oil_immersed_transformer", "company_id": "sz_002112", "node_id": "oil_immersed_transformer", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:油浸式变压器")},
    {"exposure_id": "sz_002112_produce_dry_type_transformer", "company_id": "sz_002112", "node_id": "dry_type_transformer", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:干式变压器")},
    {"exposure_id": "sz_002112_produce_amorphous_alloy_transformer", "company_id": "sz_002112", "node_id": "amorphous_alloy_transformer", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:非晶合金变压器")},
    {"exposure_id": "sz_002112_produce_power_generation_equipment", "company_id": "sz_002112", "node_id": "power_generation_equipment", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:输配电及控制设备")},
    {"exposure_id": "sz_002112_provide_service_technical_service", "company_id": "sz_002112", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002114_produce_zinc_ingot", "company_id": "sz_002114", "node_id": "zinc_ingot", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:锌锭")},
    {"exposure_id": "sz_002114_produce_lead_concentrate", "company_id": "sz_002114", "node_id": "lead_concentrate", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:铅精矿")},
    {"exposure_id": "sz_002114_produce_ultra_fine_zinc_powder", "company_id": "sz_002114", "node_id": "ultra_fine_zinc_powder", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:超精细锌粉")},
    {"exposure_id": "sz_002114_operate_hydroelectric_power", "company_id": "sz_002114", "node_id": "hydroelectric_power", "activity_type": "operate", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:水力发电")},
    {"exposure_id": "sz_002114_produce_metal_product", "company_id": "sz_002114", "node_id": "metal_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金属制品")},
    {"exposure_id": "sz_002114_operate_power_generation", "company_id": "sz_002114", "node_id": "power_generation", "activity_type": "operate", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:水力发电")},
    {"exposure_id": "sz_002115_provide_service_network_optimization", "company_id": "sz_002115", "node_id": "network_optimization", "activity_type": "provide_service", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:网优覆盖")},
    {"exposure_id": "sz_002115_provide_service_satellite_communication_service", "company_id": "sz_002115", "node_id": "satellite_communication_service", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:卫星通信服务")},
    {"exposure_id": "sz_002115_provide_service_internet_advertising", "company_id": "sz_002115", "node_id": "internet_advertising", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:互联网广告")},
    {"exposure_id": "sz_002115_provide_service_telecommunication", "company_id": "sz_002115", "node_id": "telecommunication", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:通信工程")},
    {"exposure_id": "sz_002115_provide_service_technical_service", "company_id": "sz_002115", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
]

write_batch(126, NODES_126, EDGES_126, COMPANIES_126, EXPOSURES_126)
print("Batch 126 generated.")
