# -*- coding: utf-8 -*-
"""
Construct industrial graph for batch_001 companies.
Submit nodes and edges to Neo4j via GraphRegistrationBatch API.
"""
import json
import urllib.request
import uuid

API_BASE = "http://localhost:8000/api/v1"

def api_post(path, payload):
    url = f"{API_BASE}{path}"
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP Error {e.code}: {error_body}")
        raise

# Define all industrial nodes needed for batch_001
# Each company gets upstream inputs and downstream outputs

NODES = [
    # ST国华 (000004) - mobile app security
    {"node_id": "server_hardware", "canonical_name_zh": "服务器硬件", "canonical_name_en": "Server Hardware", "node_type": "equipment", "description": "计算服务器、网络设备等IT基础设施"},
    {"node_id": "operating_system", "canonical_name_zh": "操作系统", "canonical_name_en": "Operating System", "node_type": "software", "description": "服务器及终端操作系统软件"},
    {"node_id": "security_database", "canonical_name_zh": "安全数据库", "canonical_name_en": "Security Database", "node_type": "service", "description": "漏洞库、威胁情报、移动应用样本数据"},
    {"node_id": "mobile_app_security_service", "canonical_name_zh": "移动应用安全服务", "canonical_name_en": "Mobile App Security Service", "node_type": "service", "description": "移动应用加固、防逆向、防篡改、隐私合规检测等安全服务"},
    {"node_id": "emergency_security_service", "canonical_name_zh": "应急安全技术服务", "canonical_name_en": "Emergency Security Service", "node_type": "service", "description": "应急安全技术服务及双预警系统"},

    # 中国宝安 (000009) - new energy materials
    {"node_id": "natural_graphite", "canonical_name_zh": "天然石墨", "canonical_name_en": "Natural Graphite", "node_type": "raw_material", "description": "天然鳞片石墨，锂电池负极材料原料"},
    {"node_id": "needle_coke", "canonical_name_zh": "针状焦", "canonical_name_en": "Needle Coke", "node_type": "raw_material", "description": "人造石墨负极材料核心原料，由石油焦或煤沥青制得"},
    {"node_id": "lithium_salt", "canonical_name_zh": "锂盐", "canonical_name_en": "Lithium Salt", "node_type": "raw_material", "description": "碳酸锂、氢氧化锂等锂电池正极材料原料"},
    {"node_id": "lithium_battery_anode", "canonical_name_zh": "锂电池负极材料", "canonical_name_en": "Lithium Battery Anode Material", "node_type": "intermediate", "description": "锂离子电池负极材料，包括天然石墨、人造石墨、硅基负极"},
    {"node_id": "lithium_battery_cathode", "canonical_name_zh": "锂电池正极材料", "canonical_name_en": "Lithium Battery Cathode Material", "node_type": "intermediate", "description": "锂离子电池正极材料，包括三元材料、磷酸铁锂等"},

    # 南玻A (000012) - glass manufacturing
    {"node_id": "quartz_sand", "canonical_name_zh": "石英砂", "canonical_name_en": "Quartz Sand", "node_type": "raw_material", "description": "玻璃核心原料，低铁石英砂用于光伏玻璃"},
    {"node_id": "soda_ash", "canonical_name_zh": "纯碱", "canonical_name_en": "Soda Ash", "node_type": "raw_material", "description": "玻璃熔制关键化工原料"},
    {"node_id": "natural_gas", "canonical_name_zh": "天然气", "canonical_name_en": "Natural Gas", "node_type": "energy", "description": "清洁能源燃料，用于玻璃熔炉加热"},
    {"node_id": "float_glass", "canonical_name_zh": "浮法玻璃", "canonical_name_en": "Float Glass", "node_type": "product", "description": "平板玻璃原片，建筑及深加工基础材料"},
    {"node_id": "pv_glass", "canonical_name_zh": "光伏玻璃", "canonical_name_en": "Photovoltaic Glass", "node_type": "product", "description": "光伏压延玻璃，用于太阳能电池组件封装"},
    {"node_id": "engineering_glass", "canonical_name_zh": "工程玻璃", "canonical_name_en": "Engineering Glass", "node_type": "product", "description": "LOW-E中空玻璃、镀膜玻璃等建筑节能玻璃"},
    {"node_id": "electronic_glass", "canonical_name_zh": "电子玻璃", "canonical_name_en": "Electronic Glass", "node_type": "product", "description": "超薄电子玻璃，用于智能手机、车载显示等"},

    # 深华发A (000020) - LCD monitor assembly
    {"node_id": "lcd_panel", "canonical_name_zh": "液晶面板", "canonical_name_en": "LCD Panel", "node_type": "component", "description": "液晶显示面板及模组"},
    {"node_id": "plastic_resin", "canonical_name_zh": "塑胶原料", "canonical_name_en": "Plastic Resin", "node_type": "raw_material", "description": "ABS、PP、PC等塑胶原材料"},
    {"node_id": "lcd_monitor", "canonical_name_zh": "液晶显示器", "canonical_name_en": "LCD Monitor", "node_type": "product", "description": "液晶显示器整机，包括电竞显示器、工控显示等"},
    {"node_id": "injection_molding_part", "canonical_name_zh": "注塑件", "canonical_name_en": "Injection Molding Part", "node_type": "component", "description": "精密注塑件，家电外壳及结构件"},

    # 深科技 (000021) - semiconductor packaging & EMS
    {"node_id": "memory_wafer", "canonical_name_zh": "存储晶圆", "canonical_name_en": "Memory Wafer", "node_type": "component", "description": "DRAM和NAND Flash存储晶圆"},
    {"node_id": "packaging_material", "canonical_name_zh": "封装材料", "canonical_name_en": "Packaging Material", "node_type": "raw_material", "description": "封装基板、粘接膜、塑封料、镀钯铜线等半导体封装材料"},
    {"node_id": "memory_module", "canonical_name_zh": "存储模组", "canonical_name_en": "Memory Module", "node_type": "product", "description": "内存条、SSD固态硬盘、U盘等存储产品"},
    {"node_id": "smart_meter", "canonical_name_zh": "智能电表", "canonical_name_en": "Smart Meter", "node_type": "product", "description": "智能电表、水表、气表及AMI系统"},

    # 国药一致 (000028) - pharmaceutical distribution
    {"node_id": "pharmaceutical_product", "canonical_name_zh": "药品", "canonical_name_en": "Pharmaceutical Product", "node_type": "product", "description": "化学药、中成药、生物制品、疫苗等药品"},
    {"node_id": "medical_device", "canonical_name_zh": "医疗器械", "canonical_name_en": "Medical Device", "node_type": "product", "description": "医用耗材、诊断试剂、医疗设备等"},
    {"node_id": "pharmaceutical_distribution", "canonical_name_zh": "医药分销服务", "canonical_name_en": "Pharmaceutical Distribution", "node_type": "service", "description": "药品及医疗器械批发配送、SPD院内物流等分销服务"},
    {"node_id": "pharmaceutical_retail", "canonical_name_zh": "医药零售服务", "canonical_name_en": "Pharmaceutical Retail", "node_type": "service", "description": "连锁药店零售、DTP专业药房、慢病管理等服务"},

    # 富奥股份 (000030) - auto parts
    {"node_id": "automotive_steel", "canonical_name_zh": "汽车钢材", "canonical_name_en": "Automotive Steel", "node_type": "raw_material", "description": "用于汽车零部件的钢材、特种钢"},
    {"node_id": "automotive_aluminum", "canonical_name_zh": "汽车铝材", "canonical_name_en": "Automotive Aluminum", "node_type": "raw_material", "description": "用于轻量化底盘及零部件的铝合金材料"},
    {"node_id": "automotive_chip", "canonical_name_zh": "汽车芯片", "canonical_name_en": "Automotive Chip", "node_type": "component", "description": "用于域控制器、电控产品的汽车级芯片"},
    {"node_id": "chassis_system", "canonical_name_zh": "底盘系统", "canonical_name_en": "Chassis System", "node_type": "component", "description": "汽车底盘结构件、控制臂、副车架、底盘域控制器"},
    {"node_id": "thermal_management_system", "canonical_name_zh": "热管理系统", "canonical_name_en": "Thermal Management System", "node_type": "component", "description": "汽车热管理集成模块、空调箱总成、电池冷却器"},
    {"node_id": "suspension_system", "canonical_name_zh": "悬架系统", "canonical_name_en": "Suspension System", "node_type": "component", "description": "电控减振器、空气悬架、空气弹簧等悬架部件"},

    # 神州数码 (000034) - IT distribution
    {"node_id": "it_hardware", "canonical_name_zh": "IT硬件", "canonical_name_en": "IT Hardware", "node_type": "product", "description": "服务器、PC、网络设备、存储设备等信息技术硬件"},
    {"node_id": "software_license", "canonical_name_zh": "软件授权", "canonical_name_en": "Software License", "node_type": "service", "description": "操作系统、应用软件、数据库等软件授权"},
    {"node_id": "cloud_service_resource", "canonical_name_zh": "云服务资源", "canonical_name_en": "Cloud Service Resource", "node_type": "service", "description": "公有云、私有云计算及存储资源"},
    {"node_id": "it_distribution_service", "canonical_name_zh": "IT分销服务", "canonical_name_en": "IT Distribution Service", "node_type": "service", "description": "IT产品渠道分销、供应链管理及增值服务"},
    {"node_id": "cloud_solution", "canonical_name_zh": "云解决方案", "canonical_name_en": "Cloud Solution", "node_type": "service", "description": "企业数字化转型、云管理、行业解决方案"},

    # 深纺织A (000045) - polarizer
    {"node_id": "pva_film", "canonical_name_zh": "PVA膜", "canonical_name_en": "PVA Film", "node_type": "raw_material", "description": "聚乙烯醇膜，偏光片核心偏振层材料"},
    {"node_id": "tac_film", "canonical_name_zh": "TAC膜", "canonical_name_en": "TAC Film", "node_type": "raw_material", "description": "三醋酸纤维素膜，PVA保护膜材料"},
    {"node_id": "lcd_polarizer", "canonical_name_zh": "LCD偏光片", "canonical_name_en": "LCD Polarizer", "node_type": "component", "description": "TFT-LCD用偏光片，液晶显示面板核心材料"},
    {"node_id": "oled_polarizer", "canonical_name_zh": "OLED偏光片", "canonical_name_en": "OLED Polarizer", "node_type": "component", "description": "OLED用偏光片，有机发光显示面板核心材料"},

    # 德赛电池 (000049) - battery BMS/PACK
    {"node_id": "lithium_ion_cell", "canonical_name_zh": "锂离子电芯", "canonical_name_en": "Lithium Ion Cell", "node_type": "component", "description": "聚合物锂电芯、圆柱电芯、方形电芯等锂电池单体"},
    {"node_id": "bms_component", "canonical_name_zh": "BMS组件", "canonical_name_en": "BMS Component", "node_type": "component", "description": "电池管理系统PCB板、IC芯片、MOS管等电子元器件"},
    {"node_id": "consumer_battery_pack", "canonical_name_zh": "消费电子电池包", "canonical_name_en": "Consumer Battery Pack", "node_type": "product", "description": "智能手机、笔记本、穿戴设备用锂电池模组"},
    {"node_id": "energy_storage_battery", "canonical_name_zh": "储能电池", "canonical_name_en": "Energy Storage Battery", "node_type": "product", "description": "基站储能、家庭储能、便携式储能电池系统"},
]

# Deduplicate nodes by node_id
seen_ids = set()
UNIQUE_NODES = []
for n in NODES:
    if n['node_id'] not in seen_ids:
        seen_ids.add(n['node_id'])
        UNIQUE_NODES.append(n)

print(f"Total unique nodes: {len(UNIQUE_NODES)}")

# Define edges (INDUSTRIAL_FLOW) for each company
# Format: source_id -> target_id with relation_type

EDGES = [
    # ST国华
    {"edge_id": "flow_server_to_appsec", "source_id": "server_hardware", "target_id": "mobile_app_security_service", "relation_type": "enables", "weight": 0.8, "description": "服务器硬件支撑移动应用安全服务运行"},
    {"edge_id": "flow_os_to_appsec", "source_id": "operating_system", "target_id": "mobile_app_security_service", "relation_type": "enables", "weight": 0.7, "description": "操作系统支撑安全服务软件运行"},
    {"edge_id": "flow_db_to_appsec", "source_id": "security_database", "target_id": "mobile_app_security_service", "relation_type": "enables", "weight": 0.9, "description": "安全数据库是移动应用安全服务的核心数据输入"},
    {"edge_id": "flow_server_to_emersec", "source_id": "server_hardware", "target_id": "emergency_security_service", "relation_type": "enables", "weight": 0.8, "description": "服务器硬件支撑应急安全技术服务"},

    # 中国宝安
    {"edge_id": "flow_graphite_to_anode", "source_id": "natural_graphite", "target_id": "lithium_battery_anode", "relation_type": "raw_material_for", "weight": 0.9, "description": "天然石墨加工为锂电池负极材料"},
    {"edge_id": "flow_needlecoke_to_anode", "source_id": "needle_coke", "target_id": "lithium_battery_anode", "relation_type": "raw_material_for", "weight": 0.9, "description": "针状焦石墨化后制成人造石墨负极材料"},
    {"edge_id": "flow_lisalt_to_cathode", "source_id": "lithium_salt", "target_id": "lithium_battery_cathode", "relation_type": "raw_material_for", "weight": 0.9, "description": "锂盐用于制备锂电池正极材料"},

    # 南玻A
    {"edge_id": "flow_quartz_to_float", "source_id": "quartz_sand", "target_id": "float_glass", "relation_type": "raw_material_for", "weight": 0.85, "description": "石英砂是浮法玻璃的核心原料"},
    {"edge_id": "flow_soda_to_float", "source_id": "soda_ash", "target_id": "float_glass", "relation_type": "raw_material_for", "weight": 0.85, "description": "纯碱用于玻璃熔制"},
    {"edge_id": "flow_gas_to_float", "source_id": "natural_gas", "target_id": "float_glass", "relation_type": "energy_for", "weight": 0.9, "description": "天然气为玻璃熔炉提供热能"},
    {"edge_id": "flow_quartz_to_pv", "source_id": "quartz_sand", "target_id": "pv_glass", "relation_type": "raw_material_for", "weight": 0.85, "description": "低铁石英砂用于光伏玻璃生产"},
    {"edge_id": "flow_quartz_to_elec", "source_id": "quartz_sand", "target_id": "electronic_glass", "relation_type": "raw_material_for", "weight": 0.8, "description": "高纯石英砂用于电子玻璃生产"},

    # 深华发A
    {"edge_id": "flow_panel_to_monitor", "source_id": "lcd_panel", "target_id": "lcd_monitor", "relation_type": "component_for", "weight": 0.9, "description": "液晶面板组装为液晶显示器整机"},
    {"edge_id": "flow_plastic_to_inject", "source_id": "plastic_resin", "target_id": "injection_molding_part", "relation_type": "raw_material_for", "weight": 0.85, "description": "塑胶原料注塑成型为结构件"},

    # 深科技
    {"edge_id": "flow_wafer_to_module", "source_id": "memory_wafer", "target_id": "memory_module", "relation_type": "component_for", "weight": 0.9, "description": "存储晶圆封测后制成内存条和SSD"},
    {"edge_id": "flow_pkgmat_to_module", "source_id": "packaging_material", "target_id": "memory_module", "relation_type": "raw_material_for", "weight": 0.7, "description": "封装材料用于存储芯片封装"},
    {"edge_id": "flow_pkgmat_to_meter", "source_id": "packaging_material", "target_id": "smart_meter", "relation_type": "raw_material_for", "weight": 0.5, "description": "封装材料用于智能电表芯片封装"},

    # 国药一致
    {"edge_id": "flow_pharma_to_dist", "source_id": "pharmaceutical_product", "target_id": "pharmaceutical_distribution", "relation_type": "product_for", "weight": 0.95, "description": "药品通过分销渠道配送至医疗机构和药店"},
    {"edge_id": "flow_device_to_dist", "source_id": "medical_device", "target_id": "pharmaceutical_distribution", "relation_type": "product_for", "weight": 0.8, "description": "医疗器械通过分销渠道配送"},
    {"edge_id": "flow_pharma_to_retail", "source_id": "pharmaceutical_product", "target_id": "pharmaceutical_retail", "relation_type": "product_for", "weight": 0.9, "description": "药品通过零售药店销售给终端消费者"},

    # 富奥股份
    {"edge_id": "flow_steel_to_chassis", "source_id": "automotive_steel", "target_id": "chassis_system", "relation_type": "raw_material_for", "weight": 0.9, "description": "钢材用于底盘结构件制造"},
    {"edge_id": "flow_alum_to_chassis", "source_id": "automotive_aluminum", "target_id": "chassis_system", "relation_type": "raw_material_for", "weight": 0.85, "description": "铝合金用于轻量化底盘部件"},
    {"edge_id": "flow_steel_to_susp", "source_id": "automotive_steel", "target_id": "suspension_system", "relation_type": "raw_material_for", "weight": 0.85, "description": "钢材用于悬架弹簧和减振器"},
    {"edge_id": "flow_chip_to_thermal", "source_id": "automotive_chip", "target_id": "thermal_management_system", "relation_type": "component_for", "weight": 0.7, "description": "芯片用于热管理系统电控单元"},

    # 神州数码
    {"edge_id": "flow_hw_to_dist", "source_id": "it_hardware", "target_id": "it_distribution_service", "relation_type": "product_for", "weight": 0.95, "description": "IT硬件通过分销渠道交付至终端客户"},
    {"edge_id": "flow_sw_to_dist", "source_id": "software_license", "target_id": "it_distribution_service", "relation_type": "service_for", "weight": 0.85, "description": "软件授权通过分销渠道交付"},
    {"edge_id": "flow_cloud_to_solution", "source_id": "cloud_service_resource", "target_id": "cloud_solution", "relation_type": "service_for", "weight": 0.9, "description": "云资源聚合为云解决方案"},

    # 深纺织A
    {"edge_id": "flow_pva_to_lcdpol", "source_id": "pva_film", "target_id": "lcd_polarizer", "relation_type": "raw_material_for", "weight": 0.95, "description": "PVA膜是LCD偏光片核心偏振层"},
    {"edge_id": "flow_tac_to_lcdpol", "source_id": "tac_film", "target_id": "lcd_polarizer", "relation_type": "raw_material_for", "weight": 0.9, "description": "TAC膜用于保护PVA偏振层"},
    {"edge_id": "flow_pva_to_oledpol", "source_id": "pva_film", "target_id": "oled_polarizer", "relation_type": "raw_material_for", "weight": 0.9, "description": "PVA膜用于OLED偏光片"},

    # 德赛电池
    {"edge_id": "flow_cell_to_consumer", "source_id": "lithium_ion_cell", "target_id": "consumer_battery_pack", "relation_type": "component_for", "weight": 0.95, "description": "锂离子电芯封装集成为消费电子电池包"},
    {"edge_id": "flow_bms_to_consumer", "source_id": "bms_component", "target_id": "consumer_battery_pack", "relation_type": "component_for", "weight": 0.9, "description": "BMS组件管理消费电子电池包"},
    {"edge_id": "flow_cell_to_storage", "source_id": "lithium_ion_cell", "target_id": "energy_storage_battery", "relation_type": "component_for", "weight": 0.9, "description": "锂离子电芯封装为储能电池系统"},
]

print(f"Total edges: {len(EDGES)}")

# Submit via GraphRegistrationBatch
batch_payload = {
    "batch_id": f"batch_industrial_graph_001_{uuid.uuid4().hex[:8]}",
    "task_description": "Industrial graph for batch_001 A-share companies",
    "nodes": [
        {
            "node_id": n["node_id"],
            "canonical_name_zh": n["canonical_name_zh"],
            "canonical_name_en": n["canonical_name_en"],
            "node_type": n["node_type"],
            "aliases": [],
            "description": n["description"],
            "status": "ACTIVE"
        }
        for n in UNIQUE_NODES
    ],
    "edges": [
        {
            "edge_id": e["edge_id"],
            "source_id": e["source_id"],
            "target_id": e["target_id"],
            "relation_type": e["relation_type"],
            "weight": e["weight"],
            "confidence": "HIGH",
            "evidence": [
                {
                    "source": "tushare_stock_analysis",
                    "description": e["description"],
                    "url": "",
                    "timestamp": "2026-05-23T00:00:00Z"
                }
            ],
            "status": "ACTIVE"
        }
        for e in EDGES
    ]
}

print("\nSubmitting batch to API...")
try:
    result = api_post("/batches", batch_payload)
    print(f"Batch submitted successfully!")
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as ex:
    print(f"Error: {ex}")
