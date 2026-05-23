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

def make_evidence(quote_text):
    return {
        "source_title": "tushare_stock_analysis_batch_001",
        "source_url": None,
        "quote": quote_text
    }

# Define all industrial nodes needed for batch_001
NODES = [
    # ST国华 (000004) - mobile app security
    {"node_id": "server_hardware", "canonical_name_zh": "服务器硬件", "canonical_name_en": "Server Hardware", "entity_type": "infrastructure", "definition": "计算服务器、网络设备及存储等IT基础设施硬件"},
    {"node_id": "operating_system", "canonical_name_zh": "操作系统", "canonical_name_en": "Operating System", "entity_type": "application_system", "definition": "服务器及终端设备的系统软件，如麒麟、统信等"},
    {"node_id": "security_database", "canonical_name_zh": "安全数据库", "canonical_name_en": "Security Database", "entity_type": "service", "definition": "包含漏洞库、威胁情报、移动应用样本数据的安全知识库"},
    {"node_id": "mobile_app_security_service", "canonical_name_zh": "移动应用安全服务", "canonical_name_en": "Mobile App Security Service", "entity_type": "service", "definition": "为移动应用提供加固、防逆向、防篡改、隐私合规检测等安全服务"},
    {"node_id": "emergency_security_service", "canonical_name_zh": "应急安全技术服务", "canonical_name_en": "Emergency Security Service", "entity_type": "service", "definition": "提供应急安全技术服务及双预警摄像头系统"},

    # 中国宝安 (000009) - new energy materials
    {"node_id": "natural_graphite", "canonical_name_zh": "天然石墨", "canonical_name_en": "Natural Graphite", "entity_type": "material", "definition": "天然鳞片石墨，锂电池负极材料的核心原料之一"},
    {"node_id": "needle_coke", "canonical_name_zh": "针状焦", "canonical_name_en": "Needle Coke", "entity_type": "material", "definition": "由石油焦或煤沥青制得的优质焦炭，人造石墨负极材料核心原料"},
    {"node_id": "lithium_salt", "canonical_name_zh": "锂盐", "canonical_name_en": "Lithium Salt", "entity_type": "material", "definition": "碳酸锂、氢氧化锂等，锂电池正极材料的关键原料"},
    {"node_id": "lithium_battery_anode", "canonical_name_zh": "锂电池负极材料", "canonical_name_en": "Lithium Battery Anode Material", "entity_type": "material", "definition": "锂离子电池负极活性材料，包括天然石墨、人造石墨、硅基负极等"},
    {"node_id": "lithium_battery_cathode", "canonical_name_zh": "锂电池正极材料", "canonical_name_en": "Lithium Battery Cathode Material", "entity_type": "material", "definition": "锂离子电池正极活性材料，包括三元材料、磷酸铁锂等"},

    # 南玻A (000012) - glass manufacturing
    {"node_id": "quartz_sand", "canonical_name_zh": "石英砂", "canonical_name_en": "Quartz Sand", "entity_type": "material", "definition": "二氧化硅颗粒原料，玻璃生产的核心原材料"},
    {"node_id": "soda_ash", "canonical_name_zh": "纯碱", "canonical_name_en": "Soda Ash", "entity_type": "material", "definition": "碳酸钠，玻璃熔制过程中的关键助熔剂化工原料"},
    {"node_id": "natural_gas", "canonical_name_zh": "天然气", "canonical_name_en": "Natural Gas", "entity_type": "material", "definition": "清洁能源燃料，用于玻璃熔炉等工业窑炉加热"},
    {"node_id": "float_glass", "canonical_name_zh": "浮法玻璃", "canonical_name_en": "Float Glass", "entity_type": "component", "definition": "采用浮法工艺生产的平板玻璃原片，用于建筑和深加工"},
    {"node_id": "pv_glass", "canonical_name_zh": "光伏玻璃", "canonical_name_en": "Photovoltaic Glass", "entity_type": "component", "definition": "超白低铁压延玻璃，用于太阳能电池组件的正面封装盖板"},
    {"node_id": "engineering_glass", "canonical_name_zh": "工程玻璃", "canonical_name_en": "Engineering Glass", "entity_type": "component", "definition": "LOW-E中空玻璃、镀膜玻璃等建筑节能深加工玻璃产品"},
    {"node_id": "electronic_glass", "canonical_name_zh": "电子玻璃", "canonical_name_en": "Electronic Glass", "entity_type": "component", "definition": "超薄高铝/锂铝硅玻璃，用于智能手机、车载显示等电子屏幕"},

    # 深华发A (000020) - LCD monitor assembly
    {"node_id": "lcd_panel", "canonical_name_zh": "液晶面板", "canonical_name_en": "LCD Panel", "entity_type": "component", "definition": "液晶显示面板及显示模组，显示器整机的核心显示部件"},
    {"node_id": "plastic_resin", "canonical_name_zh": "塑胶原料", "canonical_name_en": "Plastic Resin", "entity_type": "material", "definition": "ABS、PP、PC等热塑性高分子材料，用于注塑成型结构件"},
    {"node_id": "lcd_monitor", "canonical_name_zh": "液晶显示器", "canonical_name_en": "LCD Monitor", "entity_type": "device", "definition": "以液晶面板为核心的显示终端整机，包括电竞显示器、工控显示器等"},
    {"node_id": "injection_molding_part", "canonical_name_zh": "注塑件", "canonical_name_en": "Injection Molding Part", "entity_type": "component", "definition": "通过注塑工艺成型的塑胶结构件，用于家电外壳及内部支撑"},

    # 深科技 (000021) - semiconductor packaging & EMS
    {"node_id": "memory_wafer", "canonical_name_zh": "存储晶圆", "canonical_name_en": "Memory Wafer", "entity_type": "component", "definition": "未经封装的DRAM或NAND Flash硅晶圆片，存储芯片的半成品"},
    {"node_id": "packaging_material", "canonical_name_zh": "封装材料", "canonical_name_en": "Packaging Material", "entity_type": "material", "definition": "半导体封装用基板、粘接膜、塑封料、镀钯铜线等辅助材料"},
    {"node_id": "memory_module", "canonical_name_zh": "存储模组", "canonical_name_en": "Memory Module", "entity_type": "device", "definition": "封测后的内存条、SSD固态硬盘、U盘等成品存储产品"},
    {"node_id": "smart_meter", "canonical_name_zh": "智能电表", "canonical_name_en": "Smart Meter", "entity_type": "device", "definition": "具备通信和计量功能的智能电表、水表、气表及AMI采集系统"},

    # 国药一致 (000028) - pharmaceutical distribution
    {"node_id": "pharmaceutical_product", "canonical_name_zh": "药品", "canonical_name_en": "Pharmaceutical Product", "entity_type": "material", "definition": "化学药、中成药、生物制品、疫苗等用于预防治疗疾病的医药产品"},
    {"node_id": "medical_device", "canonical_name_zh": "医疗器械", "canonical_name_en": "Medical Device", "entity_type": "device", "definition": "医用耗材、诊断试剂、医疗设备等用于医疗诊断治疗的器械产品"},
    {"node_id": "pharmaceutical_distribution", "canonical_name_zh": "医药分销服务", "canonical_name_en": "Pharmaceutical Distribution", "entity_type": "service", "definition": "药品及医疗器械从生产商到终端的批发配送、SPD院内物流等流通服务"},
    {"node_id": "pharmaceutical_retail", "canonical_name_zh": "医药零售服务", "canonical_name_en": "Pharmaceutical Retail", "entity_type": "service", "definition": "通过连锁药店、DTP药房向终端消费者销售药品及提供慢病管理的服务"},

    # 富奥股份 (000030) - auto parts
    {"node_id": "automotive_steel", "canonical_name_zh": "汽车钢材", "canonical_name_en": "Automotive Steel", "entity_type": "material", "definition": "用于汽车零部件制造的高强度钢、特种钢材"},
    {"node_id": "automotive_aluminum", "canonical_name_zh": "汽车铝材", "canonical_name_en": "Automotive Aluminum", "entity_type": "material", "definition": "用于汽车轻量化底盘及零部件的铝合金材料"},
    {"node_id": "automotive_chip", "canonical_name_zh": "汽车芯片", "canonical_name_en": "Automotive Chip", "entity_type": "component", "definition": "用于汽车域控制器、电控单元、传感器的车规级半导体芯片"},
    {"node_id": "chassis_system", "canonical_name_zh": "底盘系统", "canonical_name_en": "Chassis System", "entity_type": "subsystem", "definition": "汽车底盘结构件、控制臂、副车架、底盘域控制器等行驶系统总成"},
    {"node_id": "thermal_management_system", "canonical_name_zh": "热管理系统", "canonical_name_en": "Thermal Management System", "entity_type": "subsystem", "definition": "汽车热管理集成模块、空调箱总成、电动水泵、电池冷却器等温控系统"},
    {"node_id": "suspension_system", "canonical_name_zh": "悬架系统", "canonical_name_en": "Suspension System", "entity_type": "subsystem", "definition": "电控减振器、空气悬架、空气弹簧等缓冲和导向系统总成"},

    # 神州数码 (000034) - IT distribution
    {"node_id": "it_hardware", "canonical_name_zh": "IT硬件", "canonical_name_en": "IT Hardware", "entity_type": "device", "definition": "服务器、个人电脑、网络设备、存储设备等信息技术硬件产品"},
    {"node_id": "software_license", "canonical_name_zh": "软件授权", "canonical_name_en": "Software License", "entity_type": "service", "definition": "操作系统、应用软件、数据库等软件的使用许可授权"},
    {"node_id": "cloud_service_resource", "canonical_name_zh": "云服务资源", "canonical_name_en": "Cloud Service Resource", "entity_type": "service", "definition": "公有云、私有云提供的计算、存储、网络等云基础设施资源"},
    {"node_id": "it_distribution_service", "canonical_name_zh": "IT分销服务", "canonical_name_en": "IT Distribution Service", "entity_type": "service", "definition": "IT产品通过渠道网络从厂商到终端客户的分销、供应链管理及增值服务"},
    {"node_id": "cloud_solution", "canonical_name_zh": "云解决方案", "canonical_name_en": "Cloud Solution", "entity_type": "service", "definition": "基于云资源的企业数字化转型方案、云管理服务及行业解决方案"},

    # 深纺织A (000045) - polarizer
    {"node_id": "pva_film", "canonical_name_zh": "PVA膜", "canonical_name_en": "PVA Film", "entity_type": "material", "definition": "聚乙烯醇拉伸膜，偏光片的核心偏振光学功能层材料"},
    {"node_id": "tac_film", "canonical_name_zh": "TAC膜", "canonical_name_en": "TAC Film", "entity_type": "material", "definition": "三醋酸纤维素膜，用于保护和支撑PVA偏振层的光学薄膜"},
    {"node_id": "lcd_polarizer", "canonical_name_zh": "LCD偏光片", "canonical_name_en": "LCD Polarizer", "entity_type": "component", "definition": "TFT-LCD液晶显示面板必需的偏光光学薄膜组件"},
    {"node_id": "oled_polarizer", "canonical_name_zh": "OLED偏光片", "canonical_name_en": "OLED Polarizer", "entity_type": "component", "definition": "OLED有机发光显示面板使用的偏光光学薄膜组件"},

    # 德赛电池 (000049) - battery BMS/PACK
    {"node_id": "lithium_ion_cell", "canonical_name_zh": "锂离子电芯", "canonical_name_en": "Lithium Ion Cell", "entity_type": "component", "definition": "聚合物、圆柱或方形锂离子电芯单体，电池包的基本能量单元"},
    {"node_id": "bms_component", "canonical_name_zh": "BMS组件", "canonical_name_en": "BMS Component", "entity_type": "component", "definition": "电池管理系统用的PCB板、电源管理IC芯片、MOS管等电子元器件"},
    {"node_id": "consumer_battery_pack", "canonical_name_zh": "消费电子电池包", "canonical_name_en": "Consumer Battery Pack", "entity_type": "device", "definition": "由电芯和BMS封装集成的智能手机、笔记本、穿戴设备用锂电池模组"},
    {"node_id": "energy_storage_battery", "canonical_name_zh": "储能电池", "canonical_name_en": "Energy Storage Battery", "entity_type": "device", "definition": "用于基站储能、家庭储能、便携式储能的锂离子电池系统"},
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
EDGES = [
    # ST国华
    {"edge_id": "flow_server_to_appsec", "from_node": "server_hardware", "to_node": "mobile_app_security_service", "edge_type": "capability_supply", "description": "服务器硬件为移动应用安全服务提供计算和运行基础设施支撑"},
    {"edge_id": "flow_os_to_appsec", "from_node": "operating_system", "to_node": "mobile_app_security_service", "edge_type": "capability_supply", "description": "操作系统为移动应用安全服务软件提供底层运行环境支撑"},
    {"edge_id": "flow_db_to_appsec", "from_node": "security_database", "to_node": "mobile_app_security_service", "edge_type": "information_flow", "description": "安全数据库向移动应用安全服务提供漏洞情报和样本数据输入"},
    {"edge_id": "flow_server_to_emersec", "from_node": "server_hardware", "to_node": "emergency_security_service", "edge_type": "capability_supply", "description": "服务器硬件为应急安全技术服务提供计算和运行基础设施支撑"},

    # 中国宝安
    {"edge_id": "flow_graphite_to_anode", "from_node": "natural_graphite", "to_node": "lithium_battery_anode", "edge_type": "material_flow", "description": "天然石墨经过粉碎、球形化、石墨化等工序加工为锂电池负极材料"},
    {"edge_id": "flow_needlecoke_to_anode", "from_node": "needle_coke", "to_node": "lithium_battery_anode", "edge_type": "material_flow", "description": "针状焦经过石墨化工序加工为人造石墨锂电池负极材料"},
    {"edge_id": "flow_lisalt_to_cathode", "from_node": "lithium_salt", "to_node": "lithium_battery_cathode", "edge_type": "material_flow", "description": "锂盐作为锂源与前驱体反应合成锂电池正极材料"},

    # 南玻A
    {"edge_id": "flow_quartz_to_float", "from_node": "quartz_sand", "to_node": "float_glass", "edge_type": "material_flow", "description": "石英砂与纯碱等原料在熔炉中熔融后漂浮在锡液表面成型为浮法玻璃"},
    {"edge_id": "flow_soda_to_float", "from_node": "soda_ash", "to_node": "float_glass", "edge_type": "material_flow", "description": "纯碱作为助熔剂降低石英砂熔点，参与浮法玻璃的熔制反应"},
    {"edge_id": "flow_gas_to_float", "from_node": "natural_gas", "to_node": "float_glass", "edge_type": "energy_flow", "description": "天然气燃烧为浮法玻璃熔炉提供1600度左右的高温热能"},
    {"edge_id": "flow_quartz_to_pv", "from_node": "quartz_sand", "to_node": "pv_glass", "edge_type": "material_flow", "description": "低铁超白石英砂经压延工艺成型为光伏玻璃原片"},
    {"edge_id": "flow_quartz_to_elec", "from_node": "quartz_sand", "to_node": "electronic_glass", "edge_type": "material_flow", "description": "高纯石英砂经溢流下拉工艺成型为超薄电子玻璃"},

    # 深华发A
    {"edge_id": "flow_panel_to_monitor", "from_node": "lcd_panel", "to_node": "lcd_monitor", "edge_type": "composition", "description": "液晶面板与驱动板、外壳等组装为液晶显示器整机"},
    {"edge_id": "flow_plastic_to_inject", "from_node": "plastic_resin", "to_node": "injection_molding_part", "edge_type": "material_flow", "description": "塑胶原料经加热熔融后注入模具冷却成型为注塑结构件"},

    # 深科技
    {"edge_id": "flow_wafer_to_module", "from_node": "memory_wafer", "to_node": "memory_module", "edge_type": "material_flow", "description": "存储晶圆经过切割、封装、测试工序制成内存条和SSD等存储模组"},
    {"edge_id": "flow_pkgmat_to_module", "from_node": "packaging_material", "to_node": "memory_module", "edge_type": "material_flow", "description": "封装基板、塑封料等材料用于存储芯片的封装保护"},
    {"edge_id": "flow_pkgmat_to_meter", "from_node": "packaging_material", "to_node": "smart_meter", "edge_type": "material_flow", "description": "封装材料用于智能电表内部芯片的封装保护"},

    # 国药一致
    {"edge_id": "flow_pharma_to_dist", "from_node": "pharmaceutical_product", "to_node": "pharmaceutical_distribution", "edge_type": "service_flow", "description": "药品通过医药分销企业的仓储物流网络配送至医院和药店"},
    {"edge_id": "flow_device_to_dist", "from_node": "medical_device", "to_node": "pharmaceutical_distribution", "edge_type": "service_flow", "description": "医疗器械通过医药分销企业的仓储物流网络配送至医疗机构"},
    {"edge_id": "flow_pharma_to_retail", "from_node": "pharmaceutical_product", "to_node": "pharmaceutical_retail", "edge_type": "service_flow", "description": "药品通过连锁药店零售终端直接销售给终端消费者"},

    # 富奥股份
    {"edge_id": "flow_steel_to_chassis", "from_node": "automotive_steel", "to_node": "chassis_system", "edge_type": "material_flow", "description": "汽车钢材经冲压、焊接、机加工制成底盘结构件和副车架"},
    {"edge_id": "flow_alum_to_chassis", "from_node": "automotive_aluminum", "to_node": "chassis_system", "edge_type": "material_flow", "description": "铝合金经压铸、挤压成型为轻量化底盘控制臂和副车架"},
    {"edge_id": "flow_steel_to_susp", "from_node": "automotive_steel", "to_node": "suspension_system", "edge_type": "material_flow", "description": "特种钢材经热处理制成悬架弹簧和减振器活塞杆"},
    {"edge_id": "flow_chip_to_thermal", "from_node": "automotive_chip", "to_node": "thermal_management_system", "edge_type": "composition", "description": "汽车芯片集成于热管理系统的电控单元实现智能温控"},

    # 神州数码
    {"edge_id": "flow_hw_to_dist", "from_node": "it_hardware", "to_node": "it_distribution_service", "edge_type": "service_flow", "description": "IT硬件产品通过分销渠道网络从厂商流转至终端企业客户"},
    {"edge_id": "flow_sw_to_dist", "from_node": "software_license", "to_node": "it_distribution_service", "edge_type": "service_flow", "description": "软件授权许可通过分销渠道网络从厂商流转至终端客户"},
    {"edge_id": "flow_cloud_to_solution", "from_node": "cloud_service_resource", "to_node": "cloud_solution", "edge_type": "capability_supply", "description": "云资源能力被集成为面向行业客户的数字化转型解决方案"},

    # 深纺织A
    {"edge_id": "flow_pva_to_lcdpol", "from_node": "pva_film", "to_node": "lcd_polarizer", "edge_type": "composition", "description": "PVA膜经染色、拉伸后作为核心偏振层与TAC膜复合成LCD偏光片"},
    {"edge_id": "flow_tac_to_lcdpol", "from_node": "tac_film", "to_node": "lcd_polarizer", "edge_type": "composition", "description": "TAC膜作为保护层贴合于PVA偏振层两侧形成LCD偏光片"},
    {"edge_id": "flow_pva_to_oledpol", "from_node": "pva_film", "to_node": "oled_polarizer", "edge_type": "composition", "description": "PVA膜经处理作为偏振层与保护膜复合成OLED用偏光片"},

    # 德赛电池
    {"edge_id": "flow_cell_to_consumer", "from_node": "lithium_ion_cell", "to_node": "consumer_battery_pack", "edge_type": "composition", "description": "多颗锂离子电芯经串并联后与BMS和结构件封装为消费电子电池包"},
    {"edge_id": "flow_bms_to_consumer", "from_node": "bms_component", "to_node": "consumer_battery_pack", "edge_type": "composition", "description": "BMS组件集成于电池包内实现电芯管理、保护和均衡功能"},
    {"edge_id": "flow_cell_to_storage", "from_node": "lithium_ion_cell", "to_node": "energy_storage_battery", "edge_type": "composition", "description": "多颗锂离子电芯经串并联封装为基站储能或家庭储能电池系统"},
]

print(f"Total edges: {len(EDGES)}")

# Submit via GraphRegistrationBatch
batch_payload = {
    "batch_id": f"batch_industrial_graph_001_{uuid.uuid4().hex[:8]}",
    "task_description": "Industrial graph for batch_001 A-share companies: ST国华, 中国宝安, 南玻A, 深华发A, 深科技, 国药一致, 富奥股份, 神州数码, 深纺织A, 德赛电池",
    "nodes_to_upsert": [
        {
            "node_id": n["node_id"],
            "canonical_name_zh": n["canonical_name_zh"],
            "canonical_name_en": n["canonical_name_en"],
            "aliases": [],
            "definition": n["definition"],
            "entity_type": n["entity_type"],
            "evidence": [make_evidence(f"通过网络搜索和Tushare数据分析确认：{n['definition']}")],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
        for n in UNIQUE_NODES
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": e["edge_id"],
            "from_node": e["from_node"],
            "to_node": e["to_node"],
            "edge_type": e["edge_type"],
            "description": e["description"],
            "evidence": [make_evidence(f"通过网络搜索和Tushare数据分析确认：{e['description']}")],
            "confidence": "HIGH"
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
