#!/usr/bin/env python3
"""
Batch 110 Submission Script
Stock codes: 600885, 600886, 600887, 600888, 600889, 600892, 600893, 600894, 600895, 600897
"""

import httpx
import json

BASE_URL = "http://localhost:8005/api/v1"

def submit_graph_batch(data):
    r = httpx.post(f"{BASE_URL}/batches", json=data, timeout=60)
    return r.status_code, r.json()

def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.status_code, r.json()

# ============================================================
# STEP 1: Create missing industrial nodes
# ============================================================

graph_batch = {
    "batch_id": "batch_110_nodes",
    "task_description": "Batch 110:补充缺失的产业节点——继电器、低压电器、接触器、自动化设备、冰淇淋、奶粉、电子铝箔、高纯铝、铝杆、化成箔、腐蚀箔、航空发动机、机场地面服务",
    "nodes_to_upsert": [
        {
            "node_id": "relay",
            "canonical_name_zh": "继电器",
            "canonical_name_en": "relay",
            "aliases": ["电磁继电器", "固态继电器"],
            "definition": "一种当输入量（电、磁、声、光、热）达到一定值时，输出量将发生跳跃式变化的自动控制器件，广泛应用于电力系统保护、工业控制、通信设备、汽车电子、家用电器等领域，起到信号切换、电路保护和功率控制的作用。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "宏发股份主营业务",
                    "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "low_voltage_electrical",
            "canonical_name_zh": "低压电器",
            "canonical_name_en": "low voltage electrical apparatus",
            "aliases": ["低压开关", "低压配电电器"],
            "definition": "工作在交流电压1200V或直流电压1500V及以下的电路中起通断、保护、控制或调节作用的电器设备和器件，包括断路器、熔断器、接触器、继电器、开关等，是电力配电和工业控制的基础元器件。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "宏发股份主营业务",
                    "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "contactor",
            "canonical_name_zh": "接触器",
            "canonical_name_en": "contactor",
            "aliases": ["电磁接触器", "交流接触器"],
            "definition": "一种利用电磁原理自动控制的开关电器，用于频繁接通和分断交直流主电路及大容量控制电路，广泛应用于电动机启动控制、电焊机、电热设备、电容器组等电力负载的远程操控。",
            "entity_type": "component",
            "evidence": [
                {
                    "source_title": "宏发股份主营业务",
                    "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "automation_equipment",
            "canonical_name_zh": "自动化设备",
            "canonical_name_en": "automation equipment",
            "aliases": ["自动化装置", "自动控制系统设备"],
            "definition": "用于实现生产过程或作业流程自动化的机电一体化设备系统，包括PLC控制器、变频器、伺服系统、工业机器人、传感器、自动检测设备等，可替代人工完成重复性、高精度或危险性作业。",
            "entity_type": "device",
            "evidence": [
                {
                    "source_title": "宏发股份主营业务",
                    "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "ice_cream",
            "canonical_name_zh": "冰淇淋",
            "canonical_name_en": "ice cream",
            "aliases": ["冰激凌", "雪糕"],
            "definition": "以饮用水、牛奶、奶粉、奶油（或植物油脂）、食糖等为主要原料，加入适量食品添加剂，经混合、灭菌、均质、老化、凝冻、硬化等工艺制成的体积膨胀的冷冻饮品，是乳制品行业的重要品类。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "伊利股份主营业务",
                    "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "milk_powder",
            "canonical_name_zh": "奶粉",
            "canonical_name_en": "milk powder",
            "aliases": ["乳粉", "婴幼儿配方奶粉"],
            "definition": "以生鲜牛（羊）乳为主要原料，经浓缩、干燥等工艺去除大部分水分后制成的粉状乳制品，包括全脂奶粉、脱脂奶粉、婴幼儿配方奶粉、中老年奶粉等，具有保质期长、便于运输和储存的特点。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "伊利股份主营业务",
                    "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "electronic_aluminum_foil",
            "canonical_name_zh": "电子铝箔",
            "canonical_name_en": "electronic aluminum foil",
            "aliases": ["电极箔", "光箔"],
            "definition": "用于制造铝电解电容器电极的高纯度铝箔，通过腐蚀和化成（阳极氧化）工艺在表面形成致密氧化膜，是铝电解电容器的核心原材料，广泛应用于消费电子、工业控制、新能源和通信设备等领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新疆众和主营业务",
                    "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "high_purity_aluminum",
            "canonical_name_zh": "高纯铝",
            "canonical_name_en": "high purity aluminum",
            "aliases": ["精铝", "超高纯铝"],
            "definition": "纯度达到99.9%以上的高纯度金属铝，通过电解精炼或偏析法提纯获得，具有优异的导电性、耐腐蚀性和可加工性，主要用于制造电子铝箔、半导体靶材、航空航天合金和光学镀膜材料等高端领域。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新疆众和主营业务",
                    "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "aluminum_rod",
            "canonical_name_zh": "铝杆",
            "canonical_name_en": "aluminum rod",
            "aliases": ["铝线杆", "电工圆铝杆"],
            "definition": "通过连铸连轧工艺生产的圆形截面的铝及铝合金长条材料，是制造电线电缆、架空导线、电磁线等电工产品的原材料，具有良好的导电性和轻量化特点。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新疆众和主营业务",
                    "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "formed_foil",
            "canonical_name_zh": "化成箔",
            "canonical_name_en": "formed foil",
            "aliases": ["阳极氧化箔", "电极化成箔"],
            "definition": "以电子铝箔为基材，经过电化学阳极氧化处理在表面形成致密氧化铝电介质的铝箔材料，是铝电解电容器制造中的关键中间材料，直接决定电容器的耐压等级和电容量。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新疆众和主营业务",
                    "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "etched_foil",
            "canonical_name_zh": "腐蚀箔",
            "canonical_name_en": "etched foil",
            "aliases": ["蚀刻箔", "腐蚀铝箔"],
            "definition": "以电子铝箔为基材，通过电化学腐蚀工艺在表面形成微米级孔洞结构以大幅增加比表面积的铝箔材料，是制造化成箔和铝电解电容器的原材料，比表面积的扩大可显著提高电容器的电容量。",
            "entity_type": "material",
            "evidence": [
                {
                    "source_title": "新疆众和主营业务",
                    "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "aero_engine",
            "canonical_name_zh": "航空发动机",
            "canonical_name_en": "aero engine",
            "aliases": ["航空动力装置", "飞机发动机", "航发"],
            "definition": "为航空器提供推进动力的热力机械装置，是飞机的'心脏'，主要包括涡轮风扇发动机、涡轮喷气发动机、涡轮螺旋桨发动机和活塞式发动机等类型，集气动热力学、结构力学、材料科学、控制技术于一体，是航空工业中技术最密集、难度最高的产品之一。",
            "entity_type": "system",
            "evidence": [
                {
                    "source_title": "航发动力主营业务",
                    "quote": "航空发动机批量制造及修理等"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        },
        {
            "node_id": "air_ground_service",
            "canonical_name_zh": "机场地面服务",
            "canonical_name_en": "air ground service",
            "aliases": ["地勤服务", "航空地面保障服务"],
            "definition": "为航空器在地面停靠期间及旅客在机场候机楼内提供的各类保障服务，包括飞机引导、客舱清洁、行李装卸、配餐供应、加油加水、机务维修、旅客值机、登机服务、贵宾接待、货运装卸等。",
            "entity_type": "service",
            "evidence": [
                {
                    "source_title": "厦门空港主营业务",
                    "quote": "主要业务:国内外航空运输企业及旅客提供地面保障服务"
                }
            ],
            "confidence": "HIGH",
            "status": "ACTIVE"
        }
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "aluminum_ingot_to_electronic_aluminum_foil",
            "from_node": "aluminum_ingot",
            "to_node": "electronic_aluminum_foil",
            "edge_type": "material_flow",
            "description": "高纯度铝锭经过轧制加工成电子铝箔",
            "evidence": [
                {
                    "source_title": "铝加工产业链",
                    "quote": "精铝/高纯铝经轧制加工后制成电子铝箔，用于铝电解电容器制造"
                }
            ],
            "confidence": "HIGH"
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "electronic_aluminum_foil_to_etched_foil",
            "from_node": "electronic_aluminum_foil",
            "to_node": "etched_foil",
            "edge_type": "material_flow",
            "description": "电子铝箔经电化学腐蚀工艺加工成腐蚀箔",
            "evidence": [
                {
                    "source_title": "电容器材料工艺流程",
                    "quote": "电子铝箔先经腐蚀扩大比表面积，再经化成形成氧化膜"
                }
            ],
            "confidence": "HIGH"
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "etched_foil_to_formed_foil",
            "from_node": "etched_foil",
            "to_node": "formed_foil",
            "edge_type": "material_flow",
            "description": "腐蚀箔经阳极氧化化成工艺加工成化成箔",
            "evidence": [
                {
                    "source_title": "电容器材料工艺流程",
                    "quote": "腐蚀箔经化成处理形成氧化铝电介质，成为化成箔"
                }
            ],
            "confidence": "HIGH"
        }
    ]
}

print("=" * 60)
print("STEP 1: Submitting missing nodes for Batch 110")
print("=" * 60)
code, result = submit_graph_batch(graph_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

# ============================================================
# STEP 2: Create companies and exposures
# ============================================================

business_batch = {
    "batch_id": "batch_110_business",
    "task_description": "Batch 110:注册10家公司及其产业节点暴露",
    "companies_to_upsert": [
        {
            "company_id": "sh_600885",
            "name_zh": "宏发股份",
            "aliases": ["宏发科技股份有限公司"],
            "stock_codes": ["600885.SH"],
            "description": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备",
            "country": "CN",
            "province": "湖北",
            "city": "武汉市",
            "employee_count": 18190,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600886",
            "name_zh": "国投电力",
            "aliases": ["国投电力控股股份有限公司"],
            "stock_codes": ["600886.SH"],
            "description": "电力的生产和供应",
            "country": "CN",
            "province": "北京",
            "city": "北京市",
            "employee_count": 10740,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600887",
            "name_zh": "伊利股份",
            "aliases": ["内蒙古伊利实业集团股份有限公司"],
            "stock_codes": ["600887.SH"],
            "description": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品",
            "country": "CN",
            "province": "内蒙古",
            "city": "呼和浩特市",
            "employee_count": 63414,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600888",
            "name_zh": "新疆众和",
            "aliases": ["新疆众和股份有限公司"],
            "stock_codes": ["600888.SH"],
            "description": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔",
            "country": "CN",
            "province": "新疆",
            "city": "乌鲁木齐市",
            "employee_count": 3135,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600889",
            "name_zh": "ST京化",
            "aliases": ["南京化纤股份有限公司"],
            "stock_codes": ["600889.SH"],
            "description": "粘胶纤维和自来水的生产与经营",
            "country": "CN",
            "province": "江苏",
            "city": "南京市",
            "employee_count": 1120,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600892",
            "name_zh": "ST大晟",
            "aliases": ["大晟时代文化投资股份有限公司"],
            "stock_codes": ["600892.SH"],
            "description": "主要经营贸易业务",
            "country": "CN",
            "province": "广东",
            "city": "深圳市",
            "employee_count": 366,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600893",
            "name_zh": "航发动力",
            "aliases": ["中国航发动力股份有限公司"],
            "stock_codes": ["600893.SH"],
            "description": "航空发动机批量制造及修理等",
            "country": "CN",
            "province": "陕西",
            "city": "西安市",
            "employee_count": 30428,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600894",
            "name_zh": "广日股份",
            "aliases": ["广州广日股份有限公司"],
            "stock_codes": ["600894.SH"],
            "description": "以电梯整机制造,电梯零部件生产及物流服务为主业",
            "country": "CN",
            "province": "广东",
            "city": "广州市",
            "employee_count": 4874,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600895",
            "name_zh": "张江高科",
            "aliases": ["上海张江高科技园区开发股份有限公司"],
            "stock_codes": ["600895.SH"],
            "description": "主要业务:园区内房地产租赁,园区内房地产销售",
            "country": "CN",
            "province": "上海",
            "city": "上海市",
            "employee_count": 190,
            "company_type": "public",
            "status": "ACTIVE"
        },
        {
            "company_id": "sh_600897",
            "name_zh": "厦门空港",
            "aliases": ["元翔(厦门)国际航空港股份有限公司"],
            "stock_codes": ["600897.SH"],
            "description": "主要业务:国内外航空运输企业及旅客提供地面保障服务;出租和管理候机楼内航空营业场所,商业场所和办公场所;商务信息咨询;旅客票务代理;其他航空运输辅助活动;装卸搬运;国内货运代理;其他未列明运输代理业务;其他仓储业;物业管理;停车场管理",
            "country": "CN",
            "province": "福建",
            "city": "厦门市",
            "employee_count": 3828,
            "company_type": "public",
            "status": "ACTIVE"
        }
    ],
    "company_node_exposures_to_upsert": [
        # sh_600885 宏发股份
        {
            "exposure_id": "sh_600885_produce_relay",
            "company_id": "sh_600885",
            "node_id": "relay",
            "activity_type": "produce",
            "role": "继电器生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宏发股份主营业务", "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"}]
        },
        {
            "exposure_id": "sh_600885_produce_low_voltage_electrical",
            "company_id": "sh_600885",
            "node_id": "low_voltage_electrical",
            "activity_type": "produce",
            "role": "低压电器生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宏发股份主营业务", "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"}]
        },
        {
            "exposure_id": "sh_600885_produce_contactor",
            "company_id": "sh_600885",
            "node_id": "contactor",
            "activity_type": "produce",
            "role": "接触器生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宏发股份主营业务", "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"}]
        },
        {
            "exposure_id": "sh_600885_produce_automation_equipment",
            "company_id": "sh_600885",
            "node_id": "automation_equipment",
            "activity_type": "produce",
            "role": "自动化设备生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "宏发股份主营业务", "quote": "主要业务:研制,生产和销售继电器,低压电器,接触器,自动化设备及相关的电子元器件和组件,机电产品,机械设备"}]
        },
        # sh_600886 国投电力
        {
            "exposure_id": "sh_600886_operate_hydro_power_generation",
            "company_id": "sh_600886",
            "node_id": "hydro_power_generation",
            "activity_type": "operate",
            "role": "水电运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "国投电力主营业务", "quote": "电力的生产和供应.投资建设,经营管理以电力生产为主的能源项目;开发及经营新能源项目"}]
        },
        {
            "exposure_id": "sh_600886_produce_electricity_power",
            "company_id": "sh_600886",
            "node_id": "electricity_power",
            "activity_type": "produce",
            "role": "电力生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "国投电力主营业务", "quote": "电力的生产和供应"}]
        },
        # sh_600887 伊利股份
        {
            "exposure_id": "sh_600887_produce_liquid_milk",
            "company_id": "sh_600887",
            "node_id": "liquid_milk",
            "activity_type": "produce",
            "role": "液态奶生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "伊利股份主营业务", "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"}]
        },
        {
            "exposure_id": "sh_600887_produce_ice_cream",
            "company_id": "sh_600887",
            "node_id": "ice_cream",
            "activity_type": "produce",
            "role": "冷饮产品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "伊利股份主营业务", "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"}]
        },
        {
            "exposure_id": "sh_600887_produce_milk_powder",
            "company_id": "sh_600887",
            "node_id": "milk_powder",
            "activity_type": "produce",
            "role": "奶粉生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "伊利股份主营业务", "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"}]
        },
        {
            "exposure_id": "sh_600887_produce_dairy_product",
            "company_id": "sh_600887",
            "node_id": "dairy_product",
            "activity_type": "produce",
            "role": "乳制品生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "伊利股份主营业务", "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"}]
        },
        {
            "exposure_id": "sh_600887_produce_feed",
            "company_id": "sh_600887",
            "node_id": "feed",
            "activity_type": "produce",
            "role": "饲料生产商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "伊利股份主营业务", "quote": "液体乳系列,冷饮产品系列,奶粉及奶食品,混和饲料,方便食品"}]
        },
        # sh_600888 新疆众和
        {
            "exposure_id": "sh_600888_produce_electronic_aluminum_foil",
            "company_id": "sh_600888",
            "node_id": "electronic_aluminum_foil",
            "activity_type": "produce",
            "role": "电子铝箔生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        {
            "exposure_id": "sh_600888_produce_high_purity_aluminum",
            "company_id": "sh_600888",
            "node_id": "high_purity_aluminum",
            "activity_type": "produce",
            "role": "高纯铝生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        {
            "exposure_id": "sh_600888_produce_aluminum_ingot",
            "company_id": "sh_600888",
            "node_id": "aluminum_ingot",
            "activity_type": "produce",
            "role": "铝锭生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        {
            "exposure_id": "sh_600888_produce_aluminum_rod",
            "company_id": "sh_600888",
            "node_id": "aluminum_rod",
            "activity_type": "produce",
            "role": "铝杆生产商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        {
            "exposure_id": "sh_600888_produce_formed_foil",
            "company_id": "sh_600888",
            "node_id": "formed_foil",
            "activity_type": "produce",
            "role": "化成箔生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        {
            "exposure_id": "sh_600888_produce_etched_foil",
            "company_id": "sh_600888",
            "node_id": "etched_foil",
            "activity_type": "produce",
            "role": "腐蚀箔生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "新疆众和主营业务", "quote": "主要产品:电子铝箔,精铝,普铝锭,铝杆,化成,腐蚀箔"}]
        },
        # sh_600889 ST京化
        {
            "exposure_id": "sh_600889_produce_viscose_fiber",
            "company_id": "sh_600889",
            "node_id": "viscose_fiber",
            "activity_type": "produce",
            "role": "粘胶纤维生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST京化主营业务", "quote": "粘胶纤维和自来水的生产与经营"}]
        },
        {
            "exposure_id": "sh_600889_produce_tap_water",
            "company_id": "sh_600889",
            "node_id": "tap_water",
            "activity_type": "produce",
            "role": "自来水生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST京化主营业务", "quote": "粘胶纤维和自来水的生产与经营"}]
        },
        # sh_600892 ST大晟
        {
            "exposure_id": "sh_600892_provide_commodity_trade",
            "company_id": "sh_600892",
            "node_id": "commodity_trade",
            "activity_type": "provide_service",
            "role": "贸易商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "ST大晟主营业务", "quote": "主要经营贸易业务"}]
        },
        # sh_600893 航发动力
        {
            "exposure_id": "sh_600893_produce_aero_engine",
            "company_id": "sh_600893",
            "node_id": "aero_engine",
            "activity_type": "produce",
            "role": "航空发动机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航发动力主营业务", "quote": "航空发动机批量制造及修理等"}]
        },
        {
            "exposure_id": "sh_600893_provide_aero_engine_maintenance",
            "company_id": "sh_600893",
            "node_id": "aero_engine",
            "activity_type": "provide_service",
            "role": "航空发动机修理服务商",
            "weight": 0.8,
            "confidence": "HIGH",
            "evidence": [{"source_title": "航发动力主营业务", "quote": "航空发动机批量制造及修理等"}]
        },
        # sh_600894 广日股份
        {
            "exposure_id": "sh_600894_produce_elevator",
            "company_id": "sh_600894",
            "node_id": "elevator",
            "activity_type": "produce",
            "role": "电梯整机生产商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广日股份主营业务", "quote": "以电梯整机制造,电梯零部件生产及物流服务为主业"}]
        },
        {
            "exposure_id": "sh_600894_produce_elevator_parts",
            "company_id": "sh_600894",
            "node_id": "elevator_parts",
            "activity_type": "produce",
            "role": "电梯零部件生产商",
            "weight": 0.9,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广日股份主营业务", "quote": "以电梯整机制造,电梯零部件生产及物流服务为主业"}]
        },
        {
            "exposure_id": "sh_600894_provide_logistics_service",
            "company_id": "sh_600894",
            "node_id": "logistics_service",
            "activity_type": "provide_service",
            "role": "物流服务商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "广日股份主营业务", "quote": "以电梯整机制造,电梯零部件生产及物流服务为主业"}]
        },
        # sh_600895 张江高科
        {
            "exposure_id": "sh_600895_operate_tech_park_operation_service",
            "company_id": "sh_600895",
            "node_id": "tech_park_operation_service",
            "activity_type": "operate",
            "role": "科技产业园区运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "张江高科主营业务", "quote": "主要业务:园区内房地产租赁,园区内房地产销售"}]
        },
        {
            "exposure_id": "sh_600895_operate_property_rental",
            "company_id": "sh_600895",
            "node_id": "property_rental",
            "activity_type": "operate",
            "role": "房地产租赁运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "张江高科主营业务", "quote": "主要业务:园区内房地产租赁,园区内房地产销售"}]
        },
        # sh_600897 厦门空港
        {
            "exposure_id": "sh_600897_operate_airport_operation_service",
            "company_id": "sh_600897",
            "node_id": "airport_operation_service",
            "activity_type": "operate",
            "role": "机场运营商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦门空港主营业务", "quote": "主要业务:国内外航空运输企业及旅客提供地面保障服务"}]
        },
        {
            "exposure_id": "sh_600897_provide_air_ground_service",
            "company_id": "sh_600897",
            "node_id": "air_ground_service",
            "activity_type": "provide_service",
            "role": "机场地面服务商",
            "weight": 1.0,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦门空港主营业务", "quote": "主要业务:国内外航空运输企业及旅客提供地面保障服务"}]
        },
        {
            "exposure_id": "sh_600897_provide_cargo_handling",
            "company_id": "sh_600897",
            "node_id": "cargo_handling",
            "activity_type": "provide_service",
            "role": "货运装卸服务商",
            "weight": 0.7,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦门空港主营业务", "quote": "装卸搬运;国内货运代理;其他未列明运输代理业务"}]
        },
        {
            "exposure_id": "sh_600897_operate_warehouse_service",
            "company_id": "sh_600897",
            "node_id": "warehouse_service",
            "activity_type": "operate",
            "role": "仓储服务商",
            "weight": 0.6,
            "confidence": "HIGH",
            "evidence": [{"source_title": "厦门空港主营业务", "quote": "其他仓储业"}]
        }
    ]
}

print("\n" + "=" * 60)
print("STEP 2: Submitting companies and exposures for Batch 110")
print("=" * 60)
code, result = submit_business_batch(business_batch)
print(f"Status: {code}")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\nBatch 110 submission completed.")
