#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for batch 129 submission scripts."""
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

NODES_129 = [
    {"node_id": "steel_cord", "canonical_name_zh": "钢帘线", "canonical_name_en": "steel cord", "entity_type": "material", "aliases": [], "definition": "用于轮胎增强的钢丝帘线", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技主营业务")},
    {"node_id": "rubber_hose_steel_wire", "canonical_name_zh": "胶管钢丝", "canonical_name_en": "rubber hose steel wire", "entity_type": "material", "aliases": [], "definition": "用于橡胶软管增强的钢丝", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技经营范围")},
    {"node_id": "galvanized_steel_strand", "canonical_name_zh": "镀锌钢绞线", "canonical_name_en": "galvanized steel strand", "entity_type": "material", "aliases": [], "definition": "表面镀锌处理的钢绞线", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技经营范围")},
    {"node_id": "galvanized_steel_wire", "canonical_name_zh": "镀锌钢丝", "canonical_name_en": "galvanized steel wire", "entity_type": "material", "aliases": [], "definition": "表面镀锌处理的钢丝", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技经营范围")},
    {"node_id": "prestressed_steel_strand", "canonical_name_zh": "预应力钢绞线", "canonical_name_en": "prestressed steel strand", "entity_type": "material", "aliases": [], "definition": "用于预应力混凝土结构的钢绞线", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技经营范围")},
    {"node_id": "printed_circuit_board", "canonical_name_zh": "印刷电路板", "canonical_name_en": "printed circuit board", "entity_type": "component", "aliases": ["PCB"], "definition": "用于电子元器件电气连接的基板", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("天津普林主营业务")},
    {"node_id": "large_span_space_steel_structure", "canonical_name_zh": "大跨度空间钢结构", "canonical_name_en": "large span space steel structure", "entity_type": "component", "aliases": [], "definition": "用于大跨度建筑的空间钢结构体系", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东南网架主营业务")},
    {"node_id": "high_rise_heavy_steel_structure", "canonical_name_zh": "高层重钢结构", "canonical_name_en": "high rise heavy steel structure", "entity_type": "component", "aliases": [], "definition": "用于高层建筑的重型钢结构", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东南网架经营范围")},
    {"node_id": "light_steel_structure", "canonical_name_zh": "轻钢结构", "canonical_name_en": "light steel structure", "entity_type": "component", "aliases": [], "definition": "轻型钢结构建筑体系", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东南网架经营范围")},
    {"node_id": "steel_structure_enclosure", "canonical_name_zh": "钢结构围护产品", "canonical_name_en": "steel structure enclosure", "entity_type": "component", "aliases": [], "definition": "钢结构建筑的围护系统产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("东南网架经营范围")},
    {"node_id": "titanium_dioxide", "canonical_name_zh": "钛白粉", "canonical_name_en": "titanium dioxide", "entity_type": "material", "aliases": [], "definition": "二氧化钛白色颜料，广泛用于涂料、塑料等领域", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("安纳达主营业务")},
    {"node_id": "anatase_titanium_dioxide", "canonical_name_zh": "锐钛型钛白粉", "canonical_name_en": "anatase titanium dioxide", "entity_type": "material", "aliases": [], "definition": "锐钛晶型的钛白粉", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("安纳达经营范围")},
    {"node_id": "rutile_titanium_dioxide", "canonical_name_zh": "金红石型钛白粉", "canonical_name_en": "rutile titanium dioxide", "entity_type": "material", "aliases": [], "definition": "金红石晶型的钛白粉", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("安纳达经营范围")},
    {"node_id": "real_estate_development", "canonical_name_zh": "房地产开发经营", "canonical_name_en": "real estate development", "entity_type": "service", "aliases": [], "definition": "房地产开发建设与经营销售", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("广宇集团主营业务")},
    {"node_id": "commercial_property_management", "canonical_name_zh": "商业物业经营", "canonical_name_en": "commercial property management", "entity_type": "service", "aliases": [], "definition": "商业物业的运营与管理", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("广宇集团经营范围")},
    {"node_id": "full_series_engine", "canonical_name_zh": "全系列发动机", "canonical_name_en": "full series engine", "entity_type": "component", "aliases": [], "definition": "覆盖全功率段的发动机产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("潍柴动力主营业务")},
    {"node_id": "heavy_duty_truck", "canonical_name_zh": "重型汽车", "canonical_name_en": "heavy duty truck", "entity_type": "component", "aliases": [], "definition": "重型载货汽车及底盘", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("潍柴动力经营范围")},
    {"node_id": "light_mini_vehicle", "canonical_name_zh": "轻微型车", "canonical_name_en": "light mini vehicle", "entity_type": "component", "aliases": [], "definition": "轻型及微型汽车", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("潍柴动力经营范围")},
    {"node_id": "automotive_electronics_parts", "canonical_name_zh": "汽车电子及零部件", "canonical_name_en": "automotive electronics parts", "entity_type": "component", "aliases": [], "definition": "汽车电子系统及零部件", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("潍柴动力经营范围")},
    {"node_id": "power_transmission", "canonical_name_zh": "输电", "canonical_name_en": "power transmission", "entity_type": "service", "aliases": [], "definition": "电力的输送与传输服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("电投能源经营范围")},
    {"node_id": "heat_supply", "canonical_name_zh": "供热", "canonical_name_en": "heat supply", "entity_type": "service", "aliases": [], "definition": "热力供应服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("电投能源经营范围")},
    {"node_id": "commercial_bank", "canonical_name_zh": "商业银行", "canonical_name_en": "commercial bank", "entity_type": "service", "aliases": [], "definition": "提供存贷款、结算等金融服务的商业银行", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("中信银行与交通银行主营业务")},
    {"node_id": "home_appliance_smart_control", "canonical_name_zh": "家电智能控制产品", "canonical_name_en": "home appliance smart control", "entity_type": "component", "aliases": [], "definition": "家用电器电子智能控制模块及产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("拓邦股份主营业务")},
    {"node_id": "diamond_wire", "canonical_name_zh": "金刚石线", "canonical_name_en": "diamond wire", "entity_type": "material", "aliases": [], "definition": "用于切割硅材料、蓝宝石等的金刚石切割线", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("恒星科技经营范围")},
]

EDGES_129 = [
    {"edge_id": "steel_cord_steel", "from_node": "steel_cord", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钢帘线由钢材制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "rubber_hose_steel_wire_steel", "from_node": "rubber_hose_steel_wire", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "胶管钢丝由钢材制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "galvanized_steel_strand_steel", "from_node": "galvanized_steel_strand", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "镀锌钢绞线由钢材制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "galvanized_steel_wire_steel", "from_node": "galvanized_steel_wire", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "镀锌钢丝由钢材制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "prestressed_steel_strand_steel", "from_node": "prestressed_steel_strand", "to_node": "steel", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "预应力钢绞线由钢材制成", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "printed_circuit_board_electronic_component", "from_node": "printed_circuit_board", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "印刷电路板属于电子元器件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "large_span_space_steel_structure_construction_material", "from_node": "large_span_space_steel_structure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "大跨度空间钢结构属于建筑材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "high_rise_heavy_steel_structure_construction_material", "from_node": "high_rise_heavy_steel_structure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "高层重钢结构属于建筑材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "light_steel_structure_construction_material", "from_node": "light_steel_structure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "轻钢结构属于建筑材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_structure_enclosure_construction_material", "from_node": "steel_structure_enclosure", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钢结构围护产品属于建筑材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "titanium_dioxide_chemical_product", "from_node": "titanium_dioxide", "to_node": "chemical_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钛白粉是化工产品的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "anatase_titanium_dioxide_titanium_dioxide", "from_node": "anatase_titanium_dioxide", "to_node": "titanium_dioxide", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "锐钛型钛白粉是钛白粉的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "rutile_titanium_dioxide_titanium_dioxide", "from_node": "rutile_titanium_dioxide", "to_node": "titanium_dioxide", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "金红石型钛白粉是钛白粉的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "real_estate_development_real_estate", "from_node": "real_estate_development", "to_node": "real_estate", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "房地产开发经营是房地产业务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "commercial_property_management_property_management", "from_node": "commercial_property_management", "to_node": "property_management", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业物业经营是物业管理的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "full_series_engine_engine", "from_node": "full_series_engine", "to_node": "engine", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "全系列发动机是发动机的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "heavy_duty_truck_automotive", "from_node": "heavy_duty_truck", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "重型汽车是汽车的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "light_mini_vehicle_automotive", "from_node": "light_mini_vehicle", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "轻微型车是汽车的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "automotive_electronics_parts_electronic_component", "from_node": "automotive_electronics_parts", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "汽车电子及零部件属于电子元器件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "power_transmission_power_generation", "from_node": "power_transmission", "to_node": "power_generation", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "输电是发电的配套服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "heat_supply_power_generation", "from_node": "heat_supply", "to_node": "power_generation", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "供热是发电的配套服务", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "commercial_bank_banking_service", "from_node": "commercial_bank", "to_node": "banking_service", "edge_namespace": "industrial_flow", "edge_type": "service_flow", "description": "商业银行是银行服务的一种", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "home_appliance_smart_control_electronic_component", "from_node": "home_appliance_smart_control", "to_node": "electronic_component", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "家电智能控制产品属于电子元器件", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "diamond_wire_metal_product", "from_node": "diamond_wire", "to_node": "metal_product", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "金刚石线属于金属制品", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "heavy_duty_truck_engine", "from_node": "heavy_duty_truck", "to_node": "engine", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "重型汽车搭载发动机", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "light_mini_vehicle_engine", "from_node": "light_mini_vehicle", "to_node": "engine", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "轻微型车搭载发动机", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "printed_circuit_board_integrated_circuit", "from_node": "printed_circuit_board", "to_node": "integrated_circuit", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "印刷电路板用于集成电路封装", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "steel_cord_automotive", "from_node": "steel_cord", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "钢帘线用于汽车轮胎制造", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "prestressed_steel_strand_construction_material", "from_node": "prestressed_steel_strand", "to_node": "construction_material", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "预应力钢绞线用于建筑材料", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
    {"edge_id": "rubber_hose_steel_wire_automotive", "from_node": "rubber_hose_steel_wire", "to_node": "automotive", "edge_namespace": "industrial_flow", "edge_type": "composition", "description": "胶管钢丝用于汽车管路", "evidence": ev("产业知识图谱"), "confidence": "HIGH"},
]

COMPANIES_129 = [
    {"company_id": "sz_002132", "name_zh": "恒星科技", "name_en": "Henan Hengxing Science & Technology Co., Ltd.", "country": "CN", "province": "河南", "city": "郑州市", "stock_codes": ["002132.SZ"], "description": "钢帘线、胶管钢丝、镀锌钢绞线、预应力钢绞线、金刚石线", "founded_year": 1995, "employee_count": 3100},
    {"company_id": "sz_002134", "name_zh": "天津普林", "name_en": "Tianjin Printronics Circuit Corp", "country": "CN", "province": "天津", "city": "天津市", "stock_codes": ["002134.SZ"], "description": "双面和多层印刷电路板", "founded_year": 1988, "employee_count": 1800},
    {"company_id": "sz_002135", "name_zh": "东南网架", "name_en": "Zhejiang Southeast Space Frame Co., Ltd.", "country": "CN", "province": "浙江", "city": "杭州市", "stock_codes": ["002135.SZ"], "description": "大跨度空间钢结构、高层重钢结构、轻钢结构、钢结构围护产品", "founded_year": 2001, "employee_count": 5200},
    {"company_id": "sz_002136", "name_zh": "安纳达", "name_en": "Anhui Annada Titanium Industry Co., Ltd.", "country": "CN", "province": "安徽", "city": "铜陵市", "stock_codes": ["002136.SZ"], "description": "钛白粉（锐钛型、金红石型）", "founded_year": 2005, "employee_count": 850},
    {"company_id": "sz_002133", "name_zh": "广宇集团", "name_en": "Guangyu Group Co., Ltd.", "country": "CN", "province": "浙江", "city": "杭州市", "stock_codes": ["002133.SZ"], "description": "房地产开发经营、商业物业经营", "founded_year": 1984, "employee_count": 550},
    {"company_id": "sz_000338", "name_zh": "潍柴动力", "name_en": "Weichai Power Co., Ltd.", "country": "CN", "province": "山东", "city": "潍坊市", "stock_codes": ["000338.SZ"], "description": "全系列发动机、重型汽车、轻微型车、工程机械、液压产品、汽车电子及零部件", "founded_year": 2002, "employee_count": 42000},
    {"company_id": "sz_002128", "name_zh": "电投能源", "name_en": "China Power Investment Inner Mongolia Energy Co., Ltd.", "country": "CN", "province": "内蒙古", "city": "通辽市", "stock_codes": ["002128.SZ"], "description": "煤炭开采、电力发电、输电、供热", "founded_year": 2001, "employee_count": 15200},
    {"company_id": "sh_601998", "name_zh": "中信银行", "name_en": "China CITIC Bank Corporation Limited", "country": "CN", "province": "北京", "city": "北京市", "stock_codes": ["601998.SH"], "description": "商业银行", "founded_year": 1987, "employee_count": 60000},
    {"company_id": "sz_002139", "name_zh": "拓邦股份", "name_en": "Shenzhen Topband Co., Ltd.", "country": "CN", "province": "广东", "city": "深圳市", "stock_codes": ["002139.SZ"], "description": "家电智能控制产品、充电桩、储能、太阳能发电、风力发电", "founded_year": 1996, "employee_count": 8500},
    {"company_id": "sh_601328", "name_zh": "交通银行", "name_en": "Bank of Communications Co., Ltd.", "country": "CN", "province": "上海", "city": "上海市", "stock_codes": ["601328.SH"], "description": "商业银行", "founded_year": 1987, "employee_count": 96000},
]

EXPOSURES_129 = [
    {"exposure_id": "sz_002132_produce_steel_cord", "company_id": "sz_002132", "node_id": "steel_cord", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:钢帘线")},
    {"exposure_id": "sz_002132_produce_rubber_hose_steel_wire", "company_id": "sz_002132", "node_id": "rubber_hose_steel_wire", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:胶管钢丝")},
    {"exposure_id": "sz_002132_produce_galvanized_steel_strand", "company_id": "sz_002132", "node_id": "galvanized_steel_strand", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:镀锌钢绞线")},
    {"exposure_id": "sz_002132_produce_galvanized_steel_wire", "company_id": "sz_002132", "node_id": "galvanized_steel_wire", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:镀锌钢丝")},
    {"exposure_id": "sz_002132_produce_prestressed_steel_strand", "company_id": "sz_002132", "node_id": "prestressed_steel_strand", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:预应力钢绞线")},
    {"exposure_id": "sz_002132_produce_diamond_wire", "company_id": "sz_002132", "node_id": "diamond_wire", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金刚石线")},
    {"exposure_id": "sz_002132_produce_steel", "company_id": "sz_002132", "node_id": "steel", "activity_type": "produce", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢材")},
    {"exposure_id": "sz_002134_produce_printed_circuit_board", "company_id": "sz_002134", "node_id": "printed_circuit_board", "activity_type": "produce", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:印刷电路板")},
    {"exposure_id": "sz_002134_produce_electronic_component", "company_id": "sz_002134", "node_id": "electronic_component", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电子元器件")},
    {"exposure_id": "sz_002134_produce_integrated_circuit", "company_id": "sz_002134", "node_id": "integrated_circuit", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:集成电路")},
    {"exposure_id": "sz_002134_produce_semiconductor", "company_id": "sz_002134", "node_id": "semiconductor", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:半导体")},
    {"exposure_id": "sz_002134_provide_service_technical_service", "company_id": "sz_002134", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002135_produce_large_span_space_steel_structure", "company_id": "sz_002135", "node_id": "large_span_space_steel_structure", "activity_type": "produce", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:大跨度空间钢结构")},
    {"exposure_id": "sz_002135_produce_high_rise_heavy_steel_structure", "company_id": "sz_002135", "node_id": "high_rise_heavy_steel_structure", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:高层重钢结构")},
    {"exposure_id": "sz_002135_produce_light_steel_structure", "company_id": "sz_002135", "node_id": "light_steel_structure", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:轻钢结构")},
    {"exposure_id": "sz_002135_produce_steel_structure_enclosure", "company_id": "sz_002135", "node_id": "steel_structure_enclosure", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢结构围护产品")},
    {"exposure_id": "sz_002135_produce_construction_material", "company_id": "sz_002135", "node_id": "construction_material", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:建筑材料")},
    {"exposure_id": "sz_002135_produce_steel", "company_id": "sz_002135", "node_id": "steel", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:钢材")},
    {"exposure_id": "sz_002136_produce_titanium_dioxide", "company_id": "sz_002136", "node_id": "titanium_dioxide", "activity_type": "produce", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:钛白粉")},
    {"exposure_id": "sz_002136_produce_anatase_titanium_dioxide", "company_id": "sz_002136", "node_id": "anatase_titanium_dioxide", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:锐钛型钛白粉")},
    {"exposure_id": "sz_002136_produce_rutile_titanium_dioxide", "company_id": "sz_002136", "node_id": "rutile_titanium_dioxide", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金红石型钛白粉")},
    {"exposure_id": "sz_002136_produce_chemical_product", "company_id": "sz_002136", "node_id": "chemical_product", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:化工产品")},
    {"exposure_id": "sz_002136_produce_new_material", "company_id": "sz_002136", "node_id": "new_material", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:新材料")},
    {"exposure_id": "sz_002133_provide_service_real_estate_development", "company_id": "sz_002133", "node_id": "real_estate_development", "activity_type": "provide_service", "weight": 0.35, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:房地产开发经营")},
    {"exposure_id": "sz_002133_provide_service_commercial_property_management", "company_id": "sz_002133", "node_id": "commercial_property_management", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:商业物业经营")},
    {"exposure_id": "sz_002133_provide_service_real_estate", "company_id": "sz_002133", "node_id": "real_estate", "activity_type": "provide_service", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:房地产")},
    {"exposure_id": "sz_002133_provide_service_property_management", "company_id": "sz_002133", "node_id": "property_management", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:物业管理")},
    {"exposure_id": "sz_002133_provide_service_technical_service", "company_id": "sz_002133", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_000338_produce_full_series_engine", "company_id": "sz_000338", "node_id": "full_series_engine", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:全系列发动机")},
    {"exposure_id": "sz_000338_produce_heavy_duty_truck", "company_id": "sz_000338", "node_id": "heavy_duty_truck", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:重型汽车")},
    {"exposure_id": "sz_000338_produce_engine", "company_id": "sz_000338", "node_id": "engine", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:发动机")},
    {"exposure_id": "sz_000338_produce_automotive_electronics_parts", "company_id": "sz_000338", "node_id": "automotive_electronics_parts", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:汽车电子及零部件")},
    {"exposure_id": "sz_000338_produce_hydraulic_product", "company_id": "sz_000338", "node_id": "hydraulic_product", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:液压产品")},
    {"exposure_id": "sz_000338_produce_construction_machinery", "company_id": "sz_000338", "node_id": "construction_machinery", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:工程机械")},
    {"exposure_id": "sz_000338_provide_service_technical_service", "company_id": "sz_000338", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002128_produce_coal_mining", "company_id": "sz_002128", "node_id": "coal_mining", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:煤炭开采")},
    {"exposure_id": "sz_002128_provide_service_power_generation", "company_id": "sz_002128", "node_id": "power_generation", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电力发电")},
    {"exposure_id": "sz_002128_provide_service_power_transmission", "company_id": "sz_002128", "node_id": "power_transmission", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:输电")},
    {"exposure_id": "sz_002128_provide_service_heat_supply", "company_id": "sz_002128", "node_id": "heat_supply", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:供热")},
    {"exposure_id": "sz_002128_produce_coal", "company_id": "sz_002128", "node_id": "coal", "activity_type": "produce", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:煤炭")},
    {"exposure_id": "sz_002128_provide_service_energy_storage_system", "company_id": "sz_002128", "node_id": "energy_storage_system", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:储能")},
    {"exposure_id": "sh_601998_provide_service_commercial_bank", "company_id": "sh_601998", "node_id": "commercial_bank", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:商业银行")},
    {"exposure_id": "sh_601998_provide_service_banking_service", "company_id": "sh_601998", "node_id": "banking_service", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:银行服务")},
    {"exposure_id": "sh_601998_provide_service_insurance", "company_id": "sh_601998", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:保险")},
    {"exposure_id": "sh_601998_provide_service_software_development_service", "company_id": "sh_601998", "node_id": "software_development_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金融科技")},
    {"exposure_id": "sh_601998_provide_service_technical_service", "company_id": "sh_601998", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sz_002139_produce_home_appliance_smart_control", "company_id": "sz_002139", "node_id": "home_appliance_smart_control", "activity_type": "produce", "weight": 0.30, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:家电智能控制产品")},
    {"exposure_id": "sz_002139_produce_electronic_component", "company_id": "sz_002139", "node_id": "electronic_component", "activity_type": "produce", "weight": 0.20, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:电子元器件")},
    {"exposure_id": "sz_002139_produce_charging_pile", "company_id": "sz_002139", "node_id": "charging_pile", "activity_type": "produce", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:充电桩")},
    {"exposure_id": "sz_002139_provide_service_energy_storage_system", "company_id": "sz_002139", "node_id": "energy_storage_system", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:储能")},
    {"exposure_id": "sz_002139_provide_service_solar_power_generation", "company_id": "sz_002139", "node_id": "solar_power_generation", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:太阳能发电")},
    {"exposure_id": "sz_002139_provide_service_wind_power_generation", "company_id": "sz_002139", "node_id": "wind_power_generation", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:风力发电")},
    {"exposure_id": "sz_002139_provide_service_technical_service", "company_id": "sz_002139", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.05, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
    {"exposure_id": "sh_601328_provide_service_commercial_bank", "company_id": "sh_601328", "node_id": "commercial_bank", "activity_type": "provide_service", "weight": 0.40, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("主营业务:商业银行")},
    {"exposure_id": "sh_601328_provide_service_banking_service", "company_id": "sh_601328", "node_id": "banking_service", "activity_type": "provide_service", "weight": 0.25, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:银行服务")},
    {"exposure_id": "sh_601328_provide_service_insurance", "company_id": "sh_601328", "node_id": "insurance", "activity_type": "provide_service", "weight": 0.15, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:保险")},
    {"exposure_id": "sh_601328_provide_service_software_development_service", "company_id": "sh_601328", "node_id": "software_development_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:金融科技")},
    {"exposure_id": "sh_601328_provide_service_technical_service", "company_id": "sh_601328", "node_id": "technical_service", "activity_type": "provide_service", "weight": 0.10, "confidence": "HIGH", "status": "ACTIVE", "evidence": ev("经营范围:技术服务")},
]

write_batch(129, NODES_129, EDGES_129, COMPANIES_129, EXPOSURES_129)
print("Batch 129 generated.")
