# -*- coding: utf-8 -*-
"""
Construct company view and industry view for batch_001 companies.
Submit to PostgreSQL via BusinessRegistrationBatch API.
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

# Define companies for batch_001
COMPANIES = [
    {
        "company_id": "st_guohua",
        "name_zh": "ST国华",
        "name_en": "ST Guohua",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "private",
        "description": "深圳国华网安科技股份有限公司，主营移动应用安全服务（爱加密品牌）、应急安全技术服务",
        "exposures": [
            {"node_id": "server_hardware", "activity_type": "consumer", "weight": 0.8, "role": "采购服务器硬件支撑安全服务"},
            {"node_id": "operating_system", "activity_type": "consumer", "weight": 0.7, "role": "采购操作系统支撑安全服务运行"},
            {"node_id": "security_database", "activity_type": "consumer", "weight": 0.9, "role": "使用安全数据库提供威胁情报"},
            {"node_id": "mobile_app_security_service", "activity_type": "producer", "weight": 1.0, "role": "核心产出：移动应用安全服务"},
            {"node_id": "emergency_security_service", "activity_type": "producer", "weight": 0.6, "role": "产出：应急安全技术服务"},
        ]
    },
    {
        "company_id": "china_baoan",
        "name_zh": "中国宝安",
        "name_en": "China Baoan Group",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "private",
        "description": "中国宝安集团股份有限公司，通过贝特瑞为全球锂电池负极材料龙头，兼营生物医药（马应龙）、精密制造",
        "exposures": [
            {"node_id": "natural_graphite", "activity_type": "consumer", "weight": 0.9, "role": "自有鸡西石墨矿，采购天然石墨原料"},
            {"node_id": "needle_coke", "activity_type": "consumer", "weight": 0.9, "role": "采购针状焦用于人造石墨负极"},
            {"node_id": "lithium_salt", "activity_type": "consumer", "weight": 0.8, "role": "采购锂盐用于正极材料"},
            {"node_id": "lithium_battery_anode", "activity_type": "producer", "weight": 1.0, "role": "核心产出：全球第一锂电池负极材料"},
            {"node_id": "lithium_battery_cathode", "activity_type": "producer", "weight": 0.7, "role": "产出：高镍三元正极材料"},
        ]
    },
    {
        "company_id": "csg_holding",
        "name_zh": "南玻A",
        "name_en": "CSG Holding",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "private",
        "description": "中国南玻集团股份有限公司，主营浮法玻璃、光伏玻璃、工程玻璃、电子玻璃及太阳能产业链",
        "exposures": [
            {"node_id": "quartz_sand", "activity_type": "consumer", "weight": 0.9, "role": "自有石英砂矿，采购硅砂原料"},
            {"node_id": "soda_ash", "activity_type": "consumer", "weight": 0.85, "role": "采购纯碱用于玻璃熔制"},
            {"node_id": "natural_gas", "activity_type": "consumer", "weight": 0.9, "role": "采购天然气为熔炉提供燃料"},
            {"node_id": "float_glass", "activity_type": "producer", "weight": 0.9, "role": "产出：浮法玻璃原片"},
            {"node_id": "pv_glass", "activity_type": "producer", "weight": 0.85, "role": "产出：光伏玻璃"},
            {"node_id": "engineering_glass", "activity_type": "producer", "weight": 0.8, "role": "产出：工程玻璃"},
            {"node_id": "electronic_glass", "activity_type": "producer", "weight": 0.7, "role": "产出：电子玻璃"},
        ]
    },
    {
        "company_id": "shen_huafa",
        "name_zh": "深华发A",
        "name_en": "Shenzhen Zhongheng Huafa",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "private",
        "description": "深圳中恒华发股份有限公司，主营液晶显示器整机代工、注塑件及物业租赁",
        "exposures": [
            {"node_id": "lcd_panel", "activity_type": "consumer", "weight": 0.95, "role": "采购液晶面板组装显示器"},
            {"node_id": "plastic_resin", "activity_type": "consumer", "weight": 0.8, "role": "采购塑胶原料注塑结构件"},
            {"node_id": "lcd_monitor", "activity_type": "producer", "weight": 1.0, "role": "核心产出：液晶显示器整机"},
            {"node_id": "injection_molding_part", "activity_type": "producer", "weight": 0.6, "role": "产出：注塑结构件"},
        ]
    },
    {
        "company_id": "kaifa_technology",
        "name_zh": "深科技",
        "name_en": "Shenzhen Kaifa Technology",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "state_owned",
        "description": "深圳长城开发科技股份有限公司，主营存储半导体封测（沛顿科技）、高端EMS制造、计量智能终端",
        "exposures": [
            {"node_id": "memory_wafer", "activity_type": "consumer", "weight": 0.95, "role": "采购存储晶圆进行封测"},
            {"node_id": "packaging_material", "activity_type": "consumer", "weight": 0.8, "role": "采购封装材料用于芯片封装"},
            {"node_id": "memory_module", "activity_type": "producer", "weight": 1.0, "role": "核心产出：内存条、SSD等存储模组"},
            {"node_id": "smart_meter", "activity_type": "producer", "weight": 0.7, "role": "产出：智能电表及AMI系统"},
        ]
    },
    {
        "company_id": "sinopharm_consistent",
        "name_zh": "国药一致",
        "name_en": "Sinopharm Consistent",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "state_owned",
        "description": "国药集团一致药业股份有限公司，医药分销（~70%）与医药零售国大药房（~30%）双主业",
        "exposures": [
            {"node_id": "pharmaceutical_product", "activity_type": "consumer", "weight": 0.95, "role": "采购药品进行分销和零售"},
            {"node_id": "medical_device", "activity_type": "consumer", "weight": 0.8, "role": "采购医疗器械进行分销"},
            {"node_id": "pharmaceutical_distribution", "activity_type": "producer", "weight": 1.0, "role": "核心产出：医药分销服务"},
            {"node_id": "pharmaceutical_retail", "activity_type": "producer", "weight": 0.9, "role": "产出：医药零售服务"},
        ]
    },
    {
        "company_id": "faw_aito",
        "name_zh": "富奥股份",
        "name_en": "FAW Aito Auto Parts",
        "country": "CN",
        "province": "吉林",
        "city": "长春",
        "company_type": "state_owned",
        "description": "富奥汽车零部件股份有限公司，一汽系背景，主营底盘系统、热管理系统、智能网联、悬架系统等汽车零部件",
        "exposures": [
            {"node_id": "automotive_steel", "activity_type": "consumer", "weight": 0.9, "role": "采购钢材制造底盘结构件"},
            {"node_id": "automotive_aluminum", "activity_type": "consumer", "weight": 0.85, "role": "采购铝材制造轻量化底盘"},
            {"node_id": "automotive_chip", "activity_type": "consumer", "weight": 0.8, "role": "采购汽车芯片用于域控制器"},
            {"node_id": "chassis_system", "activity_type": "producer", "weight": 1.0, "role": "核心产出：底盘系统"},
            {"node_id": "thermal_management_system", "activity_type": "producer", "weight": 0.9, "role": "产出：热管理系统"},
            {"node_id": "suspension_system", "activity_type": "producer", "weight": 0.85, "role": "产出：悬架系统"},
        ]
    },
    {
        "company_id": "digital_china",
        "name_zh": "神州数码",
        "name_en": "Digital China",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "private",
        "description": "神州数码集团股份有限公司，中国最大IT分销及增值服务商，兼营自有品牌信创（神州鲲泰）和云服务",
        "exposures": [
            {"node_id": "it_hardware", "activity_type": "consumer", "weight": 0.95, "role": "采购IT硬件进行分销"},
            {"node_id": "software_license", "activity_type": "consumer", "weight": 0.85, "role": "采购软件授权进行分销"},
            {"node_id": "cloud_service_resource", "activity_type": "consumer", "weight": 0.8, "role": "采购云资源集成解决方案"},
            {"node_id": "it_distribution_service", "activity_type": "producer", "weight": 1.0, "role": "核心产出：IT分销服务"},
            {"node_id": "cloud_solution", "activity_type": "producer", "weight": 0.7, "role": "产出：云解决方案"},
        ]
    },
    {
        "company_id": "shenzhen_textile",
        "name_zh": "深纺织A",
        "name_en": "Shenzhen Textile Holdings",
        "country": "CN",
        "province": "广东",
        "city": "深圳",
        "company_type": "state_owned",
        "description": "深圳纺织集团股份有限公司，通过控股子公司盛波光电主营LCD/OLED偏光片，国内偏光片行业领先企业",
        "exposures": [
            {"node_id": "pva_film", "activity_type": "consumer", "weight": 0.95, "role": "采购PVA膜作为偏光片核心材料"},
            {"node_id": "tac_film", "activity_type": "consumer", "weight": 0.9, "role": "采购TAC膜保护偏振层"},
            {"node_id": "lcd_polarizer", "activity_type": "producer", "weight": 1.0, "role": "核心产出：LCD偏光片"},
            {"node_id": "oled_polarizer", "activity_type": "producer", "weight": 0.8, "role": "产出：OLED偏光片"},
        ]
    },
    {
        "company_id": "desay_battery",
        "name_zh": "德赛电池",
        "name_en": "Desay Battery",
        "country": "CN",
        "province": "广东",
        "city": "惠州",
        "company_type": "private",
        "description": "深圳市德赛电池科技股份有限公司，主营锂电池BMS及PACK封装集成，客户包括苹果、华为等，近年布局储能电芯",
        "exposures": [
            {"node_id": "lithium_ion_cell", "activity_type": "consumer", "weight": 0.95, "role": "采购锂离子电芯进行封装集成"},
            {"node_id": "bms_component", "activity_type": "consumer", "weight": 0.9, "role": "采购BMS组件管理电池包"},
            {"node_id": "consumer_battery_pack", "activity_type": "producer", "weight": 1.0, "role": "核心产出：消费电子电池包"},
            {"node_id": "energy_storage_battery", "activity_type": "producer", "weight": 0.7, "role": "产出：储能电池系统"},
        ]
    },
]

# Define industries
INDUSTRIES = [
    {
        "industry_id": "new_energy_ev",
        "name_zh": "新能源与电动车",
        "name_en": "New Energy and Electric Vehicles",
        "industry_type": "curated_view",
        "description": "涵盖锂电池材料、动力电池、储能、新能源汽车零部件、充电设施等产业链",
        "mappings": [
            {"node_id": "natural_graphite", "role": "上游原材料", "weight": 1.0},
            {"node_id": "needle_coke", "role": "上游原材料", "weight": 1.0},
            {"node_id": "lithium_salt", "role": "上游原材料", "weight": 1.0},
            {"node_id": "lithium_battery_anode", "role": "中游材料", "weight": 1.0},
            {"node_id": "lithium_battery_cathode", "role": "中游材料", "weight": 1.0},
            {"node_id": "lithium_ion_cell", "role": "中游电芯", "weight": 1.0},
            {"node_id": "bms_component", "role": "中游组件", "weight": 0.8},
            {"node_id": "consumer_battery_pack", "role": "下游电池包", "weight": 0.9},
            {"node_id": "energy_storage_battery", "role": "下游储能", "weight": 0.9},
            {"node_id": "automotive_steel", "role": "上游原材料", "weight": 0.8},
            {"node_id": "automotive_aluminum", "role": "上游原材料", "weight": 0.8},
            {"node_id": "automotive_chip", "role": "上游芯片", "weight": 0.8},
            {"node_id": "chassis_system", "role": "中游零部件", "weight": 0.9},
            {"node_id": "thermal_management_system", "role": "中游零部件", "weight": 0.9},
            {"node_id": "suspension_system", "role": "中游零部件", "weight": 0.9},
        ]
    },
    {
        "industry_id": "semiconductor_electronics",
        "name_zh": "半导体与电子制造",
        "name_en": "Semiconductor and Electronics Manufacturing",
        "industry_type": "curated_view",
        "description": "涵盖半导体材料、芯片设计制造封测、电子元器件、IT设备、显示面板等产业链",
        "mappings": [
            {"node_id": "memory_wafer", "role": "上游晶圆", "weight": 1.0},
            {"node_id": "packaging_material", "role": "上游材料", "weight": 0.8},
            {"node_id": "memory_module", "role": "中游模组", "weight": 1.0},
            {"node_id": "smart_meter", "role": "下游终端", "weight": 0.7},
            {"node_id": "server_hardware", "role": "上游设备", "weight": 0.9},
            {"node_id": "operating_system", "role": "上游软件", "weight": 0.8},
            {"node_id": "it_hardware", "role": "中游硬件", "weight": 1.0},
            {"node_id": "software_license", "role": "中游软件", "weight": 0.8},
            {"node_id": "cloud_service_resource", "role": "中游资源", "weight": 0.8},
            {"node_id": "lcd_panel", "role": "上游面板", "weight": 0.9},
            {"node_id": "pva_film", "role": "上游材料", "weight": 0.9},
            {"node_id": "tac_film", "role": "上游材料", "weight": 0.9},
            {"node_id": "lcd_polarizer", "role": "中游组件", "weight": 1.0},
            {"node_id": "oled_polarizer", "role": "中游组件", "weight": 0.9},
            {"node_id": "lcd_monitor", "role": "下游终端", "weight": 0.8},
            {"node_id": "plastic_resin", "role": "上游原料", "weight": 0.6},
            {"node_id": "injection_molding_part", "role": "中游结构件", "weight": 0.6},
        ]
    },
    {
        "industry_id": "consumer_medicine",
        "name_zh": "大消费与医药",
        "name_en": "Consumer and Medicine",
        "industry_type": "curated_view",
        "description": "涵盖食品饮料、医药制造、医药分销零售、医疗器械等产业链",
        "mappings": [
            {"node_id": "pharmaceutical_product", "role": "上游药品", "weight": 1.0},
            {"node_id": "medical_device", "role": "上游器械", "weight": 0.9},
            {"node_id": "pharmaceutical_distribution", "role": "中游分销", "weight": 1.0},
            {"node_id": "pharmaceutical_retail", "role": "下游零售", "weight": 0.9},
        ]
    },
    {
        "industry_id": "traditional_manufacturing_resources",
        "name_zh": "传统制造与资源",
        "name_en": "Traditional Manufacturing and Resources",
        "industry_type": "curated_view",
        "description": "涵盖钢铁、有色、化工、建材、玻璃、造纸等基础工业产业链",
        "mappings": [
            {"node_id": "quartz_sand", "role": "上游原料", "weight": 1.0},
            {"node_id": "soda_ash", "role": "上游化工", "weight": 1.0},
            {"node_id": "natural_gas", "role": "上游能源", "weight": 0.9},
            {"node_id": "float_glass", "role": "中游产品", "weight": 1.0},
            {"node_id": "pv_glass", "role": "中游产品", "weight": 0.9},
            {"node_id": "engineering_glass", "role": "中游产品", "weight": 0.9},
            {"node_id": "electronic_glass", "role": "中游产品", "weight": 0.8},
        ]
    },
]

# Build batch payload
batch_payload = {
    "batch_id": f"business_batch_001_{uuid.uuid4().hex[:8]}",
    "task_description": "Company and industry view for batch_001 A-share companies",
    "industries": [
        {
            "industry_id": ind["industry_id"],
            "name_zh": ind["name_zh"],
            "name_en": ind["name_en"],
            "industry_type": ind["industry_type"],
            "description": ind["description"]
        }
        for ind in INDUSTRIES
    ],
    "industry_mappings": [
        {
            "industry_id": ind["industry_id"],
            "node_id": m["node_id"],
            "role": m["role"],
            "weight": m["weight"],
            "confidence": "HIGH"
        }
        for ind in INDUSTRIES
        for m in ind["mappings"]
    ],
    "companies": [
        {
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "name_en": c["name_en"],
            "country": c["country"],
            "province": c.get("province", ""),
            "city": c.get("city", ""),
            "company_type": c["company_type"],
            "description": c["description"]
        }
        for c in COMPANIES
    ],
    "company_exposures": [
        {
            "company_id": c["company_id"],
            "node_id": e["node_id"],
            "activity_type": e["activity_type"],
            "weight": e["weight"],
            "role": e["role"],
            "confidence": "HIGH"
        }
        for c in COMPANIES
        for e in c["exposures"]
    ]
}

print(f"Companies: {len(batch_payload['companies'])}")
print(f"Company exposures: {len(batch_payload['company_exposures'])}")
print(f"Industries: {len(batch_payload['industries'])}")
print(f"Industry mappings: {len(batch_payload['industry_mappings'])}")

print("\nSubmitting business batch to API...")
try:
    result = api_post("/business-batches", batch_payload)
    print(f"Batch submitted!")
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as ex:
    print(f"Error: {ex}")
