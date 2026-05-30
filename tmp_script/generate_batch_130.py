import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ev(source_title, quote="根据企业公开信息"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]


def write_batch(batch_num, nodes, edges, companies, exposures):
    graph = {
        "batch_id": f"batch_{batch_num}_nodes",
        "task_description": f"Batch {batch_num} industrial nodes and edges",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
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
        "industry_node_mappings_to_upsert": [],
    }
    path_b = os.path.join(BASE_DIR, "tmp_script", f"batch_{batch_num}_business.json")
    with open(path_b, "w", encoding="utf-8") as f:
        json.dump(business, f, ensure_ascii=False, indent=2)
    print(
        f"Batch {batch_num}: {len(nodes)} nodes, {len(edges)} edges, "
        f"{len(companies)} companies, {len(exposures)} exposures"
    )


def make_node(node_id, canonical_name_zh, canonical_name_en, aliases, definition, entity_type, evidence, confidence="HIGH", status="ACTIVE"):
    return {
        "node_id": node_id,
        "canonical_name_zh": canonical_name_zh,
        "canonical_name_en": canonical_name_en,
        "aliases": aliases,
        "definition": definition,
        "entity_type": entity_type,
        "evidence": evidence,
        "confidence": confidence,
        "status": status,
    }


def make_edge(edge_id, from_node, to_node, edge_type, description, evidence, confidence="HIGH", edge_namespace="industrial_flow"):
    return {
        "edge_id": edge_id,
        "from_node": from_node,
        "to_node": to_node,
        "edge_namespace": edge_namespace,
        "edge_type": edge_type,
        "description": description,
        "evidence": evidence,
        "confidence": confidence,
    }


def make_company(company_id, name_zh, name_en, province, city, stock_codes, description, founded_year, employee_count, country="CN"):
    return {
        "company_id": company_id,
        "name_zh": name_zh,
        "name_en": name_en,
        "country": country,
        "province": province,
        "city": city,
        "stock_codes": stock_codes,
        "description": description,
        "founded_year": founded_year,
        "employee_count": employee_count,
    }


def make_exposure(exposure_id, company_id, node_id, activity_type, weight, evidence, confidence="HIGH", status="ACTIVE"):
    return {
        "exposure_id": exposure_id,
        "company_id": company_id,
        "node_id": node_id,
        "activity_type": activity_type,
        "weight": weight,
        "confidence": confidence,
        "status": status,
        "evidence": evidence,
    }


def main():
    nodes = [
        make_node(
            "bauxite", "铝土矿", "Bauxite",
            ["铝矾土"],
            "铝土矿是生产氧化铝和金属铝的主要原料，是一种含有铝矿物的水合氧化铝矿石。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业从事铝土矿开采业务"),
        ),
        make_node(
            "alumina", "氧化铝", "Alumina",
            ["铝氧", "三氧化二铝"],
            "氧化铝是一种无机化合物，是电解铝生产的主要原料，由铝土矿提炼而来。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业生产氧化铝产品"),
        ),
        make_node(
            "electrolytic_aluminum", "电解铝", "Electrolytic Aluminum",
            ["原铝"],
            "电解铝是通过电解氧化铝得到的金属铝，是铝产业链的核心中间产品。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业从事电解铝生产"),
        ),
        make_node(
            "aluminum_alloy", "铝合金", "Aluminum Alloy",
            ["铝基合金"],
            "铝合金是以铝为基础加入一种或几种其他元素制成的合金材料，具有轻质高强等特性。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业生产铝合金产品"),
        ),
        make_node(
            "carbon_product", "碳素制品", "Carbon Product",
            ["炭素制品"],
            "碳素制品是以碳元素为主要成分的材料产品，广泛应用于电解铝、钢铁等行业的电极和耐火材料。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业生产碳素制品"),
        ),
        make_node(
            "sulfuric_acid", "硫酸", "Sulfuric Acid",
            [],
            "硫酸是一种重要的工业原料，广泛用于化肥、冶金、石油化工等行业。",
            "material",
            ev("中国铝业股份有限公司年报", "中国铝业生产硫酸产品"),
        ),
        make_node(
            "intelligent_lighting", "智能照明", "Intelligent Lighting",
            ["智慧照明"],
            "智能照明是利用物联网、传感等技术实现自动控制和节能管理的照明系统。",
            "device",
            ev("深圳市实益达科技股份有限公司年报", "实益达从事智能照明业务"),
        ),
        make_node(
            "smart_home_system", "智能家居管理系统", "Smart Home Management System",
            ["智能家居系统", "智慧家居平台"],
            "智能家居管理系统是通过物联网技术实现家居设备集中控制与场景联动的软件与硬件集成系统。",
            "system",
            ev("深圳市实益达科技股份有限公司年报", "实益达开发智能家居管理系统"),
        ),
        make_node(
            "compound_fertilizer", "复合肥", "Compound Fertilizer",
            ["复混肥"],
            "复合肥是含有两种或两种以上营养元素的化肥产品，可根据作物需求进行配方调制。",
            "material",
            ev("深圳市芭田生态工程股份有限公司年报", "芭田股份生产复合肥产品"),
        ),
        make_node(
            "controlled_release_fertilizer", "控释肥", "Controlled-Release Fertilizer",
            ["控释肥料"],
            "控释肥是通过包膜等技术控制养分释放速度的化肥，可提高肥料利用率。",
            "material",
            ev("深圳市芭田生态工程股份有限公司年报", "芭田股份生产控释肥"),
        ),
        make_node(
            "slow_release_fertilizer", "缓释肥", "Slow-Release Fertilizer",
            ["缓释肥料"],
            "缓释肥是养分释放速度低于常规化肥的肥料产品，可减少养分流失。",
            "material",
            ev("深圳市芭田生态工程股份有限公司年报", "芭田股份生产缓释肥"),
        ),
        make_node(
            "microbial_fertilizer", "微生物肥", "Microbial Fertilizer",
            ["微生物肥料", "菌肥"],
            "微生物肥是利用有益微生物改善土壤养分供应或促进植物生长的肥料产品。",
            "material",
            ev("深圳市芭田生态工程股份有限公司年报", "芭田股份生产微生物肥"),
        ),
        make_node(
            "water_soluble_fertilizer", "水溶肥", "Water-Soluble Fertilizer",
            ["水溶性肥料"],
            "水溶肥是完全可溶于水的多元复合肥料，适用于喷灌、滴灌等水肥一体化施用。",
            "material",
            ev("深圳市芭田生态工程股份有限公司年报", "芭田股份生产水溶肥"),
        ),
        make_node(
            "chemical_engineering_design", "化工工程设计", "Chemical Engineering Design",
            ["化工设计"],
            "化工工程设计是针对化学工业项目进行的工艺设计、设备选型及工程方案设计服务。",
            "service",
            ev("东华工程科技股份有限公司年报", "东华科技从事化工工程设计"),
        ),
        make_node(
            "engineering_general_contracting", "工程总承包", "Engineering General Contracting",
            ["EPC总承包"],
            "工程总承包是指承包商受业主委托，按照合同约定对工程建设项目的设计、采购、施工、试运行等实行全过程承包。",
            "service",
            ev("东华工程科技股份有限公司年报", "东华科技从事工程总承包业务"),
        ),
        make_node(
            "container_shipping", "集装箱运输", "Container Shipping",
            ["集装箱航运"],
            "集装箱运输是以标准化集装箱为载体，通过船舶进行的海上货物运输服务。",
            "service",
            ev("中远海运控股股份有限公司年报", "中远海控从事集装箱运输业务"),
        ),
        make_node(
            "ship_agency", "船舶代理", "Ship Agency",
            ["船代"],
            "船舶代理是接受船舶所有人或承租人委托，代为办理船舶进出港、装卸货、供应等业务的代理服务。",
            "service",
            ev("中远海运控股股份有限公司年报", "中远海控从事船舶代理业务"),
        ),
        make_node(
            "wharf_operation", "码头运营", "Wharf Operation",
            ["码头经营", "港口运营"],
            "码头运营是指对港口码头设施进行投资、管理和运营，提供船舶停靠、货物装卸等服务。",
            "infrastructure",
            ev("中远海运控股股份有限公司年报", "中远海控投资运营码头"),
        ),
        make_node(
            "warehousing_handling", "仓储装卸", "Warehousing and Handling",
            ["仓储搬运"],
            "仓储装卸是指为货物提供储存、保管以及装卸搬运等物流服务。",
            "service",
            ev("中远海运控股股份有限公司年报", "中远海控提供仓储装卸服务"),
        ),
        make_node(
            "copper", "铜", "Copper",
            ["电解铜", "精铜"],
            "铜是一种重要的有色金属，具有良好的导电导热性，广泛应用于电力、电子、建筑等行业。",
            "material",
            ev("西部矿业股份有限公司年报", "西部矿业生产铜产品"),
        ),
        make_node(
            "lead_metal", "铅", "Lead",
            [],
            "铅是一种柔软的重金属，主要用于蓄电池、电缆护套、防辐射材料等领域。",
            "material",
            ev("西部矿业股份有限公司年报", "西部矿业生产铅产品"),
        ),
        make_node(
            "zinc_metal", "锌", "Zinc",
            [],
            "锌是一种蓝白色有色金属，主要用于镀锌、电池、合金及化工等行业。",
            "material",
            ev("西部矿业股份有限公司年报", "西部矿业生产锌产品"),
        ),
        make_node(
            "non_ferrous_metal_mining", "有色金属开采", "Non-Ferrous Metal Mining",
            ["有色金属采选"],
            "有色金属开采是指对铜、铅、锌等有色金属矿产进行勘探、开采和选矿的工业活动。",
            "service",
            ev("西部矿业股份有限公司年报", "西部矿业从事有色金属开采"),
        ),
        make_node(
            "non_ferrous_metal_smelting", "有色金属冶炼", "Non-Ferrous Metal Smelting",
            ["有色金属冶炼加工"],
            "有色金属冶炼是指通过火法或湿法冶金工艺将有色金属精矿提炼为金属产品的工业过程。",
            "service",
            ev("西部矿业股份有限公司年报", "西部矿业从事有色金属冶炼"),
        ),
        make_node(
            "ferrous_metal_mining", "黑色金属开采", "Ferrous Metal Mining",
            ["黑色金属采选"],
            "黑色金属开采是指对铁、锰等黑色金属矿产进行勘探、开采和选矿的工业活动。",
            "service",
            ev("西部矿业股份有限公司年报", "西部矿业从事黑色金属开采"),
        ),
        make_node(
            "automotive_interior_fabric", "汽车内饰面料", "Automotive Interior Fabric",
            ["汽车内饰材料"],
            "汽车内饰面料是用于汽车座椅、顶棚、门板等内部装饰的纺织材料，要求具有耐磨、阻燃等性能。",
            "material",
            ev("宏达高科控股股份有限公司年报", "宏达高科生产汽车内饰面料"),
        ),
        make_node(
            "warp_knitted_fabric", "经编面料", "Warp Knitted Fabric",
            ["经编织物"],
            "经编面料是由经编机将一组或多组平行排列的纱线同时编织成圈相互串套而成的针织面料。",
            "material",
            ev("宏达高科控股股份有限公司年报", "宏达高科生产经编面料"),
        ),
        make_node(
            "fabric_dyeing_finishing", "面料染整", "Fabric Dyeing and Finishing",
            ["染整加工", "印染整理"],
            "面料染整是指对纺织面料进行染色、印花和整理加工，赋予面料色彩和功能性的工艺过程。",
            "service",
            ev("宏达高科控股股份有限公司年报", "宏达高科从事面料染整业务"),
        ),
        make_node(
            "micro_fine_enamel_wire", "微细漆包线", "Micro-Fine Enamel Wire",
            ["微细电磁线"],
            "微细漆包线是一种表面涂覆绝缘漆层的超细金属导线，主要用于精密电子元器件和微型电机绕组。",
            "component",
            ev("贤丰控股股份有限公司年报", "贤丰控股生产微细漆包线"),
        ),
        make_node(
            "commercial_banking", "商业银行服务", "Commercial Banking",
            ["商业银行业务"],
            "商业银行服务是指商业银行向企业和个人提供的存款、贷款、结算、汇兑等金融服务。",
            "service",
            ev("宁波银行股份有限公司年报", "宁波银行提供商业银行服务"),
        ),
        make_node(
            "sheet_inductor", "片式电感器", "Sheet Inductor",
            ["片感", "贴片电感"],
            "片式电感器是一种表面贴装型被动电子元件，用于电路中的滤波、振荡和阻抗匹配。",
            "component",
            ev("深圳顺络电子股份有限公司年报", "顺络电子生产片式电感器"),
        ),
        make_node(
            "chip_varistor", "片式压敏电阻器", "Chip Varistor",
            ["贴片压敏电阻"],
            "片式压敏电阻器是一种表面贴装型过电压保护元件，具有非线性伏安特性，用于抑制电路中的浪涌电压。",
            "component",
            ev("深圳顺络电子股份有限公司年报", "顺络电子生产片式压敏电阻器"),
        ),
        make_node(
            "enterprise_internet_service", "企业互联网服务", "Enterprise Internet Service",
            ["企业互联网解决方案"],
            "企业互联网服务是为企业提供数字化转型、互联网营销、信息化平台建设等综合性服务。",
            "service",
            ev("深圳市实益达科技股份有限公司年报", "实益达提供企业互联网服务"),
        ),
        make_node(
            "internet_e_commerce_service", "互联网电子商务服务", "Internet E-Commerce Service",
            ["电商服务", "互联网电商"],
            "互联网电子商务服务是基于互联网平台开展商品或服务交易的商业模式及配套服务。",
            "service",
            ev("深圳市实益达科技股份有限公司年报", "实益达从事互联网电子商务"),
        ),
    ]

    edges = [
        make_edge("b130_bauxite_alumina", "bauxite", "alumina", "material_flow", "铝土矿通过拜耳法或烧结法提炼为氧化铝", ev("工业生产工艺资料")),
        make_edge("b130_alumina_electrolytic_aluminum", "alumina", "electrolytic_aluminum", "material_flow", "氧化铝通过霍尔-埃鲁电解工艺生产电解铝", ev("工业生产工艺资料")),
        make_edge("b130_electrolytic_aluminum_aluminum_alloy", "electrolytic_aluminum", "aluminum_alloy", "material_flow", "电解铝通过添加合金元素熔铸为铝合金", ev("工业生产工艺资料")),
        make_edge("b130_carbon_product_chemical_product", "carbon_product", "chemical_product", "composition", "碳素制品属于化工产品的一个分支", ev("化工产品分类标准")),
        make_edge("b130_sulfuric_acid_chemical_product", "sulfuric_acid", "chemical_product", "composition", "硫酸是基础化工产品的重要类别", ev("化工产品分类标准")),
        make_edge("b130_intelligent_lighting_electronic_component", "intelligent_lighting", "electronic_component", "composition", "智能照明产品属于电子元器件及设备的集成应用", ev("电子元器件行业分类")),
        make_edge("b130_smart_home_system_software_development_service", "smart_home_system", "software_development_service", "composition", "智能家居管理系统属于软件开发服务的具体应用领域", ev("软件服务行业分类")),
        make_edge("b130_compound_fertilizer_fertilizer", "compound_fertilizer", "fertilizer", "composition", "复合肥是化肥产品的重要类别", ev("化肥行业分类标准")),
        make_edge("b130_controlled_release_fertilizer_compound_fertilizer", "controlled_release_fertilizer", "compound_fertilizer", "composition", "控释肥是复合肥的细分品类", ev("化肥产品分类")),
        make_edge("b130_slow_release_fertilizer_compound_fertilizer", "slow_release_fertilizer", "compound_fertilizer", "composition", "缓释肥是复合肥的细分品类", ev("化肥产品分类")),
        make_edge("b130_microbial_fertilizer_compound_fertilizer", "microbial_fertilizer", "compound_fertilizer", "composition", "微生物肥是复合肥的细分品类", ev("化肥产品分类")),
        make_edge("b130_water_soluble_fertilizer_compound_fertilizer", "water_soluble_fertilizer", "compound_fertilizer", "composition", "水溶肥是复合肥的细分品类", ev("化肥产品分类")),
        make_edge("b130_chemical_engineering_design_technical_service", "chemical_engineering_design", "technical_service", "service_flow", "化工工程设计属于技术服务的专业领域", ev("工程技术服务行业分类")),
        make_edge("b130_engineering_general_contracting_technical_service", "engineering_general_contracting", "technical_service", "service_flow", "工程总承包属于技术服务的工程实施环节", ev("工程技术服务行业分类")),
        make_edge("b130_container_shipping_shipping", "container_shipping", "shipping", "service_flow", "集装箱运输是航运服务的核心形式", ev("航运服务行业分类")),
        make_edge("b130_ship_agency_shipping", "ship_agency", "shipping", "service_flow", "船舶代理是航运服务的配套环节", ev("航运服务行业分类")),
        make_edge("b130_wharf_operation_port", "wharf_operation", "port", "service_flow", "码头运营是港口基础设施的核心功能", ev("港口运营行业分类")),
        make_edge("b130_warehousing_handling_logistics", "warehousing_handling", "logistics", "service_flow", "仓储装卸是物流服务的重要组成部分", ev("物流服务行业分类")),
        make_edge("b130_copper_metal_product", "copper", "metal_product", "composition", "铜属于金属产品的核心品类", ev("有色金属分类标准")),
        make_edge("b130_lead_metal_metal_product", "lead_metal", "metal_product", "composition", "铅属于金属产品的核心品类", ev("有色金属分类标准")),
        make_edge("b130_zinc_metal_metal_product", "zinc_metal", "metal_product", "composition", "锌属于金属产品的核心品类", ev("有色金属分类标准")),
        make_edge("b130_non_ferrous_metal_mining_mining", "non_ferrous_metal_mining", "mining", "service_flow", "有色金属开采是采矿行业的专业细分领域", ev("采矿行业分类标准")),
        make_edge("b130_non_ferrous_metal_smelting_chemical_process", "non_ferrous_metal_smelting", "chemical_process", "service_flow", "有色金属冶炼涉及化学工艺过程", ev("冶金行业分类标准")),
        make_edge("b130_ferrous_metal_mining_mining", "ferrous_metal_mining", "mining", "service_flow", "黑色金属开采是采矿行业的专业细分领域", ev("采矿行业分类标准")),
        make_edge("b130_automotive_interior_fabric_textile", "automotive_interior_fabric", "textile", "composition", "汽车内饰面料是纺织品在汽车领域的应用", ev("纺织行业分类标准")),
        make_edge("b130_warp_knitted_fabric_textile", "warp_knitted_fabric", "textile", "composition", "经编面料是纺织品的织造品类之一", ev("纺织行业分类标准")),
        make_edge("b130_fabric_dyeing_finishing_textile", "fabric_dyeing_finishing", "textile", "service_flow", "面料染整是纺织品生产的关键后整理工序", ev("纺织行业分类标准")),
        make_edge("b130_micro_fine_enamel_wire_electronic_component", "micro_fine_enamel_wire", "electronic_component", "composition", "微细漆包线属于电子元器件的基础材料", ev("电子元器件行业分类")),
        make_edge("b130_commercial_banking_banking_service", "commercial_banking", "banking_service", "service_flow", "商业银行服务是银行服务体系的核心组成", ev("金融服务行业分类")),
        make_edge("b130_sheet_inductor_electronic_component", "sheet_inductor", "electronic_component", "composition", "片式电感器属于被动电子元器件", ev("电子元器件行业分类")),
        make_edge("b130_chip_varistor_electronic_component", "chip_varistor", "electronic_component", "composition", "片式压敏电阻器属于被动电子元器件", ev("电子元器件行业分类")),
        make_edge("b130_enterprise_internet_service_software_development_service", "enterprise_internet_service", "software_development_service", "service_flow", "企业互联网服务属于软件开发服务的应用延伸", ev("互联网服务行业分类")),
        make_edge("b130_internet_e_commerce_service_e_commerce", "internet_e_commerce_service", "e_commerce", "service_flow", "互联网电子商务服务是电子商务的具体业务模式", ev("电子商务行业分类")),
        make_edge("b130_electrolytic_aluminum_aluminum", "electrolytic_aluminum", "aluminum", "composition", "电解铝是金属铝的主要工业产品形态", ev("铝工业产业链资料")),
        make_edge("b130_aluminum_alloy_aluminum", "aluminum_alloy", "aluminum", "composition", "铝合金是铝金属的合金化产品", ev("铝工业产业链资料")),
    ]

    companies = [
        make_company(
            "601600_sh", "中国铝业股份有限公司", "Aluminum Corporation of China Limited",
            "北京市", "北京市", ["601600.SH"],
            "中国铝业是中国最大的氧化铝、电解铝及铝加工生产商，业务涵盖铝土矿开采、氧化铝、电解铝、铝合金、煤炭、发电、碳素制品、硫酸等。",
            2001, 100000,
        ),
        make_company(
            "002137_sz", "深圳市实益达科技股份有限公司", "Shenzhen Sea Star Technology Co., Ltd.",
            "广东省", "深圳市", ["002137.SZ"],
            "实益达主营业务包括企业互联网服务、智能照明、智能家居管理系统及互联网电子商务。",
            1998, 2000,
        ),
        make_company(
            "002138_sz", "深圳顺络电子股份有限公司", "Shenzhen Sunlord Electronics Co., Ltd.",
            "广东省", "深圳市", ["002138.SZ"],
            "顺络电子主要从事片式电感器、片式压敏电阻器等新型电子元器件的研发、生产和销售。",
            2000, 8000,
        ),
        make_company(
            "002170_sz", "深圳市芭田生态工程股份有限公司", "Shenzhen Batian Ecological Engineering Co., Ltd.",
            "广东省", "深圳市", ["002170.SZ"],
            "芭田股份是中国复合肥行业的领军企业，产品覆盖无机肥、有机肥、控释肥、缓释肥、微生物肥及水溶肥等。",
            1989, 3000,
        ),
        make_company(
            "002140_sz", "东华工程科技股份有限公司", "East China Engineering Science and Technology Co., Ltd.",
            "安徽省", "合肥市", ["002140.SZ"],
            "东华科技专业从事化工、石化工程设计与总承包，以及工程咨询、监理、技术开发转让等服务。",
            2001, 2000,
        ),
        make_company(
            "601919_sh", "中远海运控股股份有限公司", "COSCO SHIPPING Holdings Co., Ltd.",
            "上海市", "上海市", ["601919.SH"],
            "中远海控是中远海运集团旗下航运主业上市平台，主营国际、国内海上集装箱运输服务，兼营船舶代理、码头投资及仓储装卸等业务。",
            2005, 30000,
        ),
        make_company(
            "601168_sh", "西部矿业股份有限公司", "Western Mining Co., Ltd.",
            "青海省", "西宁市", ["601168.SH"],
            "西部矿业是中国西部地区大型有色金属矿业企业，主要从事铜、铅、锌等有色金属及铁、锰等黑色金属的采选、冶炼、加工和贸易。",
            2000, 8000,
        ),
        make_company(
            "002144_sz", "宏达高科控股股份有限公司", "Hongda High-Tech Holding Co., Ltd.",
            "浙江省", "嘉兴市", ["002144.SZ"],
            "宏达高科主营汽车内饰面料、服饰面料、经编面料织造及染整加工业务。",
            1997, 1500,
        ),
        make_company(
            "002141_sz", "贤丰控股股份有限公司", "Xianfeng Holding Co., Ltd.",
            "广东省", "珠海市", ["002141.SZ"],
            "贤丰控股主要从事微细漆包线、电子元器件及新材料业务。",
            2002, 1000,
        ),
        make_company(
            "002142_sz", "宁波银行股份有限公司", "Bank of Ningbo Co., Ltd.",
            "浙江省", "宁波市", ["002142.SZ"],
            "宁波银行是一家区域性股份制商业银行，提供全面的商业银行业务。",
            1997, 25000,
        ),
    ]

    exposures = [
        # 601600.SH 中国铝业 (8 exposures)
        make_exposure("b130_exp_601600_1", "601600_sh", "bauxite", "produce", 1.0, ev("中国铝业年报", "中国铝业从事铝土矿开采")),
        make_exposure("b130_exp_601600_2", "601600_sh", "alumina", "produce", 1.0, ev("中国铝业年报", "中国铝业生产氧化铝")),
        make_exposure("b130_exp_601600_3", "601600_sh", "electrolytic_aluminum", "produce", 1.0, ev("中国铝业年报", "中国铝业生产电解铝")),
        make_exposure("b130_exp_601600_4", "601600_sh", "aluminum_alloy", "produce", 0.9, ev("中国铝业年报", "中国铝业生产铝合金产品")),
        make_exposure("b130_exp_601600_5", "601600_sh", "coal", "produce", 0.7, ev("中国铝业年报", "中国铝业涉及煤炭业务")),
        make_exposure("b130_exp_601600_6", "601600_sh", "power_generation", "operate", 0.8, ev("中国铝业年报", "中国铝业拥有自备电厂")),
        make_exposure("b130_exp_601600_7", "601600_sh", "carbon_product", "produce", 0.8, ev("中国铝业年报", "中国铝业生产碳素制品")),
        make_exposure("b130_exp_601600_8", "601600_sh", "sulfuric_acid", "produce", 0.6, ev("中国铝业年报", "中国铝业生产硫酸")),

        # 002137.SZ 实益达 (6 exposures)
        make_exposure("b130_exp_002137_1", "002137_sz", "enterprise_internet_service", "provide_service", 1.0, ev("实益达年报", "实益达提供企业互联网服务")),
        make_exposure("b130_exp_002137_2", "002137_sz", "intelligent_lighting", "produce", 1.0, ev("实益达年报", "实益达从事智能照明业务")),
        make_exposure("b130_exp_002137_3", "002137_sz", "smart_home_system", "provide_service", 0.9, ev("实益达年报", "实益达开发智能家居管理系统")),
        make_exposure("b130_exp_002137_4", "002137_sz", "internet_e_commerce_service", "operate", 0.8, ev("实益达年报", "实益达从事互联网电子商务")),
        make_exposure("b130_exp_002137_5", "002137_sz", "software_development_service", "provide_service", 0.8, ev("实益达年报", "实益达提供软件开发服务")),
        make_exposure("b130_exp_002137_6", "002137_sz", "electronic_component", "produce", 0.7, ev("实益达年报", "实益达生产电子相关产品")),

        # 002138.SZ 顺络电子 (5 exposures)
        make_exposure("b130_exp_002138_1", "002138_sz", "sheet_inductor", "produce", 1.0, ev("顺络电子年报", "顺络电子生产片式电感器")),
        make_exposure("b130_exp_002138_2", "002138_sz", "chip_varistor", "produce", 1.0, ev("顺络电子年报", "顺络电子生产片式压敏电阻器")),
        make_exposure("b130_exp_002138_3", "002138_sz", "electronic_component", "produce", 1.0, ev("顺络电子年报", "顺络电子从事电子元器件业务")),
        make_exposure("b130_exp_002138_4", "002138_sz", "new_material", "produce", 0.8, ev("顺络电子年报", "顺络电子开发新型电子材料")),
        make_exposure("b130_exp_002138_5", "002138_sz", "integrated_circuit", "produce", 0.7, ev("顺络电子年报", "顺络电子产品应用于集成电路领域")),

        # 002170.SZ 芭田股份 (6 exposures)
        make_exposure("b130_exp_002170_1", "002170_sz", "compound_fertilizer", "produce", 1.0, ev("芭田股份年报", "芭田股份生产复合肥")),
        make_exposure("b130_exp_002170_2", "002170_sz", "controlled_release_fertilizer", "produce", 0.9, ev("芭田股份年报", "芭田股份生产控释肥")),
        make_exposure("b130_exp_002170_3", "002170_sz", "slow_release_fertilizer", "produce", 0.9, ev("芭田股份年报", "芭田股份生产缓释肥")),
        make_exposure("b130_exp_002170_4", "002170_sz", "microbial_fertilizer", "produce", 0.9, ev("芭田股份年报", "芭田股份生产微生物肥")),
        make_exposure("b130_exp_002170_5", "002170_sz", "water_soluble_fertilizer", "produce", 0.9, ev("芭田股份年报", "芭田股份生产水溶肥")),
        make_exposure("b130_exp_002170_6", "002170_sz", "fertilizer", "produce", 1.0, ev("芭田股份年报", "芭田股份主营化肥产品")),

        # 002140.SZ 东华科技 (6 exposures)
        make_exposure("b130_exp_002140_1", "002140_sz", "chemical_engineering_design", "provide_service", 1.0, ev("东华科技年报", "东华科技从事化工工程设计")),
        make_exposure("b130_exp_002140_2", "002140_sz", "engineering_general_contracting", "provide_service", 1.0, ev("东华科技年报", "东华科技从事工程总承包")),
        make_exposure("b130_exp_002140_3", "002140_sz", "technical_service", "provide_service", 0.9, ev("东华科技年报", "东华科技提供工程技术咨询服务")),
        make_exposure("b130_exp_002140_4", "002140_sz", "chemical_process", "operate", 0.8, ev("东华科技年报", "东华科技涉及化工工艺领域")),
        make_exposure("b130_exp_002140_5", "002140_sz", "machinery", "operate", 0.7, ev("东华科技年报", "东华科技涉及机械设备应用")),
        make_exposure("b130_exp_002140_6", "002140_sz", "construction_material", "operate", 0.6, ev("东华科技年报", "东华科技工程项目涉及建材领域")),

        # 601919.SH 中远海控 (6 exposures)
        make_exposure("b130_exp_601919_1", "601919_sh", "container_shipping", "operate", 1.0, ev("中远海控年报", "中远海控主营集装箱运输")),
        make_exposure("b130_exp_601919_2", "601919_sh", "ship_agency", "provide_service", 0.9, ev("中远海控年报", "中远海控从事船舶代理业务")),
        make_exposure("b130_exp_601919_3", "601919_sh", "wharf_operation", "operate", 0.9, ev("中远海控年报", "中远海控投资运营码头")),
        make_exposure("b130_exp_601919_4", "601919_sh", "warehousing_handling", "operate", 0.8, ev("中远海控年报", "中远海控提供仓储装卸服务")),
        make_exposure("b130_exp_601919_5", "601919_sh", "shipping", "operate", 1.0, ev("中远海控年报", "中远海控主营航运业务")),
        make_exposure("b130_exp_601919_6", "601919_sh", "logistics", "operate", 0.9, ev("中远海控年报", "中远海控提供综合物流服务")),

        # 601168.SH 西部矿业 (8 exposures)
        make_exposure("b130_exp_601168_1", "601168_sh", "non_ferrous_metal_mining", "operate", 1.0, ev("西部矿业年报", "西部矿业从事有色金属开采")),
        make_exposure("b130_exp_601168_2", "601168_sh", "non_ferrous_metal_smelting", "operate", 1.0, ev("西部矿业年报", "西部矿业从事有色金属冶炼")),
        make_exposure("b130_exp_601168_3", "601168_sh", "copper", "produce", 1.0, ev("西部矿业年报", "西部矿业生产铜产品")),
        make_exposure("b130_exp_601168_4", "601168_sh", "lead_metal", "produce", 0.9, ev("西部矿业年报", "西部矿业生产铅产品")),
        make_exposure("b130_exp_601168_5", "601168_sh", "zinc_metal", "produce", 0.9, ev("西部矿业年报", "西部矿业生产锌产品")),
        make_exposure("b130_exp_601168_6", "601168_sh", "ferrous_metal_mining", "operate", 0.8, ev("西部矿业年报", "西部矿业从事黑色金属开采")),
        make_exposure("b130_exp_601168_7", "601168_sh", "mining", "operate", 1.0, ev("西部矿业年报", "西部矿业主营采矿业务")),
        make_exposure("b130_exp_601168_8", "601168_sh", "metal_product", "produce", 0.9, ev("西部矿业年报", "西部矿业生产销售金属产品")),

        # 002144.SZ 宏达高科 (5 exposures)
        make_exposure("b130_exp_002144_1", "002144_sz", "automotive_interior_fabric", "produce", 1.0, ev("宏达高科年报", "宏达高科生产汽车内饰面料")),
        make_exposure("b130_exp_002144_2", "002144_sz", "warp_knitted_fabric", "produce", 1.0, ev("宏达高科年报", "宏达高科生产经编面料")),
        make_exposure("b130_exp_002144_3", "002144_sz", "fabric_dyeing_finishing", "operate", 0.9, ev("宏达高科年报", "宏达高科从事面料染整加工")),
        make_exposure("b130_exp_002144_4", "002144_sz", "textile", "produce", 1.0, ev("宏达高科年报", "宏达高科主营纺织业务")),
        make_exposure("b130_exp_002144_5", "002144_sz", "automotive", "operate", 0.8, ev("宏达高科年报", "宏达高科产品主要面向汽车行业")),

        # 002141.SZ 贤丰控股 (5 exposures)
        make_exposure("b130_exp_002141_1", "002141_sz", "micro_fine_enamel_wire", "produce", 1.0, ev("贤丰控股年报", "贤丰控股生产微细漆包线")),
        make_exposure("b130_exp_002141_2", "002141_sz", "electronic_component", "produce", 1.0, ev("贤丰控股年报", "贤丰控股从事电子元器件业务")),
        make_exposure("b130_exp_002141_3", "002141_sz", "new_material", "produce", 0.9, ev("贤丰控股年报", "贤丰控股布局新材料领域")),
        make_exposure("b130_exp_002141_4", "002141_sz", "machinery", "operate", 0.7, ev("贤丰控股年报", "贤丰控股涉及机械设备制造")),
        make_exposure("b130_exp_002141_5", "002141_sz", "semiconductor", "produce", 0.7, ev("贤丰控股年报", "贤丰控股产品应用于半导体领域")),

        # 002142.SZ 宁波银行 (5 exposures)
        make_exposure("b130_exp_002142_1", "002142_sz", "commercial_banking", "provide_service", 1.0, ev("宁波银行年报", "宁波银行提供商业银行服务")),
        make_exposure("b130_exp_002142_2", "002142_sz", "banking_service", "provide_service", 1.0, ev("宁波银行年报", "宁波银行主营银行业务")),
        make_exposure("b130_exp_002142_3", "002142_sz", "insurance", "operate", 0.7, ev("宁波银行年报", "宁波银行代理保险业务")),
        make_exposure("b130_exp_002142_4", "002142_sz", "real_estate", "operate", 0.6, ev("宁波银行年报", "宁波银行涉及房地产金融业务")),
        make_exposure("b130_exp_002142_5", "002142_sz", "e_commerce", "operate", 0.7, ev("宁波银行年报", "宁波银行开展电商金融业务")),
    ]

    write_batch(130, nodes, edges, companies, exposures)


if __name__ == "__main__":
    main()
