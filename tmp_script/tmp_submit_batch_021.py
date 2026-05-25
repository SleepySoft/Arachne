#!/usr/bin/env python3
"""
Batch 021 Submission Script
Companies: 000670.SZ – 000683.SZ (10 companies)

This script manually constructs industrial nodes, edges, companies, and exposures
based on analysis of each company's business, then submits via API.
"""
import json
import requests
import os
from datetime import date

BASE_URL = "http://localhost:8000/api/v1"

def submit_graph_batch(batch):
    r = requests.post(f"{BASE_URL}/batches", json=batch)
    return r.status_code, r.json()

def submit_business_batch(batch):
    r = requests.post(f"{BASE_URL}/business-batches", json=batch)
    return r.status_code, r.json()

# ---------------------------------------------------------------------------
# 1. INDUSTRIAL NODES (Neo4j)
# ---------------------------------------------------------------------------

nodes = [
    {
        "node_id": "smart_processor",
        "canonical_name_zh": "智能处理器",
        "canonical_name_en": "Smart Processor",
        "aliases": ["应用处理器", "AP芯片"],
        "definition": "面向移动互联终端、智能家居、可穿戴设备等应用的高集成度系统级芯片（SoC），集成CPU、GPU、ISP、基带等模块，提供计算与多媒体处理能力。",
        "entity_type": "component",
        "evidence": [{"source_title": "盈方微 主营业务及经营范围", "quote": "面向移动互联终端,智能家居,可穿戴设备等应用的智能处理器及相关软件研发,设计,生产,销售"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "mobile_terminal",
        "canonical_name_zh": "移动互联终端",
        "canonical_name_en": "Mobile Internet Terminal",
        "aliases": ["移动终端", "智能终端"],
        "definition": "具备移动互联网接入能力的终端设备，包括智能手机、平板电脑、手持智能终端等，是智能处理器的主要下游应用载体。",
        "entity_type": "device",
        "evidence": [{"source_title": "盈方微 主营业务及经营范围", "quote": "面向移动互联终端,智能家居,可穿戴设备等应用的智能处理器"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "smart_home_device",
        "canonical_name_zh": "智能家居设备",
        "canonical_name_en": "Smart Home Device",
        "aliases": ["智能家电", "智慧家居终端"],
        "definition": "具备网络连接与智能控制功能的家用设备，如智能音箱、智能门锁、智能照明、智能摄像头等，构成智能家居系统的终端节点。",
        "entity_type": "device",
        "evidence": [{"source_title": "盈方微 主营业务及经营范围", "quote": "面向移动互联终端,智能家居,可穿戴设备等应用"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "wearable_device",
        "canonical_name_zh": "可穿戴设备",
        "canonical_name_en": "Wearable Device",
        "aliases": ["可穿戴智能终端", "体感设备"],
        "definition": "可直接穿戴在身上的便携式智能电子设备，如智能手表、智能手环、AR/VR眼镜等，通常集成低功耗处理器、传感器和无线通信模块。",
        "entity_type": "device",
        "evidence": [{"source_title": "盈方微 主营业务及经营范围", "quote": "面向移动互联终端,智能家居,可穿戴设备等应用"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "cement_product",
        "canonical_name_zh": "水泥制品",
        "canonical_name_en": "Cement Product",
        "aliases": ["水泥构件", "混凝土制品"],
        "definition": "以水泥为主要胶凝材料，掺入骨料、水及外加剂后经成型、养护制成的建筑制品，包括水泥管、电杆、预制板、商品混凝土等。",
        "entity_type": "component",
        "evidence": [{"source_title": "上峰水泥 主营业务及经营范围", "quote": "水泥及水泥制品的生产和销售"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "digital_marketing_service",
        "canonical_name_zh": "数字营销服务",
        "canonical_name_en": "Digital Marketing Service",
        "aliases": ["互联网营销", "线上推广服务"],
        "definition": "基于互联网和数字技术，通过搜索引擎、社交媒体、程序化广告等渠道为广告主提供精准投放、效果监测与数据分析的营销服务。",
        "entity_type": "service",
        "evidence": [{"source_title": "智度股份 主营业务及经营范围", "quote": "数字营销业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "internet_media_service",
        "canonical_name_zh": "互联网媒体服务",
        "canonical_name_en": "Internet Media Service",
        "aliases": ["网络媒体运营", "在线内容分发"],
        "definition": "依托互联网平台提供内容聚合、分发与运营服务，包括门户网站、信息流、短视频、社交社区等形式的媒体业务。",
        "entity_type": "service",
        "evidence": [{"source_title": "智度股份 主营业务及经营范围", "quote": "互联网媒体业务"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "viscose_staple",
        "canonical_name_zh": "粘胶短丝",
        "canonical_name_en": "Viscose Staple Fiber",
        "aliases": ["粘胶短纤维", "人造棉"],
        "definition": "以天然纤维素（如棉短绒、木浆）为原料，经碱化、老化、黄化等工艺制成粘胶后纺丝切断而成的短纤维，长度通常在38-51mm，可纯纺或混纺。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST海龙 主营业务及经营范围", "quote": "主要产品:粘胶长丝,粘胶短丝,浆粕,帆布,帘子布"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "pulp_for_viscose",
        "canonical_name_zh": "粘胶浆粕",
        "canonical_name_en": "Pulp for Viscose",
        "aliases": ["棉浆粕", "木浆粕", "溶解浆"],
        "definition": "专用于生产粘胶纤维的高纯度纤维素浆粕，原料可为棉短绒或优质木材，要求α-纤维素含量高、灰分低，是粘胶纤维产业链的核心上游原料。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST海龙 主营业务及经营范围", "quote": "主要产品:棉浆粕,粘胶纤维,空心砖,纱,布,面料的生产"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "canvas_fabric",
        "canonical_name_zh": "帆布",
        "canonical_name_en": "Canvas Fabric",
        "aliases": ["篷布", "机织布"],
        "definition": "以棉、涤纶或混纺纱线为原料，采用平纹或斜纹组织织制的粗厚织物，具有高强度、耐磨特性，广泛用于运输遮盖、鞋材、箱包、工业用布等领域。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST海龙 主营业务及经营范围", "quote": "主要产品:粘胶长丝,粘胶短丝,浆粕,帆布,帘子布"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "tire_cord_fabric",
        "canonical_name_zh": "帘子布",
        "canonical_name_en": "Tire Cord Fabric",
        "aliases": ["轮胎帘子布", "浸胶帘布"],
        "definition": "以粘胶长丝、涤纶或锦纶工业丝为经纱，采用特殊织造与浸胶工艺制成的高强度骨架织物，用于轮胎胎体增强，是轮胎制造的关键骨架材料。",
        "entity_type": "material",
        "evidence": [{"source_title": "ST海龙 主营业务及经营范围", "quote": "主要产品:粘胶长丝,粘胶短丝,浆粕,帆布,帘子布"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "automotive_bearing",
        "canonical_name_zh": "汽车轴承",
        "canonical_name_en": "Automotive Bearing",
        "aliases": ["车用轴承", "轮毂轴承"],
        "definition": "专用于汽车底盘、传动系、转向系及发动机等部位的滚动轴承，需满足高转速、重载荷、长寿命及低噪音要求，是汽车关键基础零部件。",
        "entity_type": "component",
        "evidence": [{"source_title": "襄阳轴承 主营业务及经营范围", "quote": "制造销售轴承及零部件,汽车零部件,机电设备,轴承设备及备件,模具磨料,油石砂轮"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "bulldozer",
        "canonical_name_zh": "推土机",
        "canonical_name_en": "Bulldozer",
        "aliases": ["履带式推土机", "轮式推土机"],
        "definition": "以履带或轮胎为行走装置，装备前置推土铲刀的土方工程机械，主要用于场地平整、推运土方、开挖沟渠等作业，是土方施工的基础装备。",
        "entity_type": "device",
        "evidence": [{"source_title": "山推股份 主营业务及经营范围", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "excavator",
        "canonical_name_zh": "挖掘机",
        "canonical_name_en": "Excavator",
        "aliases": ["挖掘机械", "钩机"],
        "definition": "配备铲斗或破碎锤等工作装置的自行式挖掘机械，通过动臂、斗杆、铲斗的协调动作完成挖掘、装载、破碎等作业，广泛应用于建筑、矿山、水利等工程。",
        "entity_type": "device",
        "evidence": [{"source_title": "山推股份 主营业务及经营范围", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "road_roller",
        "canonical_name_zh": "压路机",
        "canonical_name_en": "Road Roller",
        "aliases": ["压实机械", "压路机械"],
        "definition": "利用自身重量和振动作用对土壤、沥青混合料或混凝土基层进行压实的工程机械，按行走方式分为静碾、轮胎碾和振动碾，是道路施工的关键设备。",
        "entity_type": "device",
        "evidence": [{"source_title": "山推股份 主营业务及经营范围", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "visual_content_service",
        "canonical_name_zh": "视觉内容服务",
        "canonical_name_en": "Visual Content Service",
        "aliases": ["图片版权服务", "视觉素材服务"],
        "definition": "以正版图片、视频、音乐、字体等视觉素材为核心，向媒体、广告、企业客户提供版权授权、内容定制与视觉解决方案的服务业态。",
        "entity_type": "service",
        "evidence": [{"source_title": "视觉中国 主营业务及经营范围", "quote": "主营业务:视觉内容与服务,视觉数字娱乐,视觉社交社区"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "stock_image",
        "canonical_name_zh": "正版图片素材",
        "canonical_name_en": "Stock Image",
        "aliases": ["图库素材", "版权图片"],
        "definition": "由专业摄影师、插画师创作并通过版权管理平台进行授权销售的数字化图片资产，包括新闻 Editorial 图片和商业 Creative 图片两类，是视觉内容产业的核心生产资料。",
        "entity_type": "material",
        "evidence": [{"source_title": "视觉中国 主营业务及经营范围", "quote": "摄像及视频制作服务;图文设计制作;摄影扩印服务;组织文化艺术交流活动"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "power_dispatching_system",
        "canonical_name_zh": "电力调度系统",
        "canonical_name_en": "Power Dispatching System",
        "aliases": ["电网调度自动化系统", "EMS能量管理系统"],
        "definition": "用于电力系统运行监视、分析与控制的计算机系统，实现对发电、输电、变电、配电环节的实时数据采集、状态估计、潮流计算、负荷预测与调度指令下发。",
        "entity_type": "subsystem",
        "evidence": [{"source_title": "东方电子 主营业务及经营范围", "quote": "主要产品:电力调度,保护及配电自动化系统,信息管理系统,电子设备与材料"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "power_protection_system",
        "canonical_name_zh": "电力保护系统",
        "canonical_name_en": "Power Protection System",
        "aliases": ["继电保护系统", "线路保护装置"],
        "definition": "当电力系统发生故障或异常工况时，能够自动、快速、有选择性地切除故障元件或发出告警信号的装置与系统，是保障电网安全稳定运行的第二道防线。",
        "entity_type": "subsystem",
        "evidence": [{"source_title": "东方电子 主营业务及经营范围", "quote": "主要产品:电力调度,保护及配电自动化系统"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "power_automation_system",
        "canonical_name_zh": "配电自动化系统",
        "canonical_name_en": "Distribution Automation System",
        "aliases": ["DA系统", "馈线自动化系统"],
        "definition": "对配电网设备进行远方监视、协调与控制的技术系统，实现故障定位、隔离与供电恢复（FLISR），提高配电网供电可靠性与运行效率。",
        "entity_type": "subsystem",
        "evidence": [{"source_title": "东方电子 主营业务及经营范围", "quote": "主要产品:电力调度,保护及配电自动化系统"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "natural_alkali",
        "canonical_name_zh": "天然碱",
        "canonical_name_en": "Natural Alkali",
        "aliases": ["天然纯碱", "碳酸钠矿"],
        "definition": "以天然碳酸钠（Trona）或碳酸氢钠-碳酸钠复盐形式存在于地下的矿物资源，可直接开采或经简单加工制成纯碱、小苏打等化工产品，是制碱工业的重要天然原料。",
        "entity_type": "material",
        "evidence": [{"source_title": "博源化工 主营业务及经营范围", "quote": "主要业务:天然碱和无机盐系列产品的生产和经营"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "baking_soda",
        "canonical_name_zh": "小苏打",
        "canonical_name_en": "Baking Soda",
        "aliases": ["碳酸氢钠", "食用碱", "重碳酸钠"],
        "definition": "化学式为NaHCO₃的白色结晶性粉末，由纯碱溶液吸收二氧化碳制得，广泛应用于食品膨松、医药制剂、畜禽饲料、消防灭火及工业清洗等领域。",
        "entity_type": "material",
        "evidence": [{"source_title": "博源化工 主营业务及经营范围", "quote": "主要产品:纯碱,小苏打"}],
        "confidence": "HIGH",
        "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 2. INDUSTRIAL EDGES (Neo4j)
# ---------------------------------------------------------------------------

edges = [
    {
        "edge_id": "flow_smart_processor_to_mobile_terminal",
        "from_node": "smart_processor",
        "to_node": "mobile_terminal",
        "description": "智能处理器作为核心计算组件嵌入移动互联终端设备，提供运算、图形处理与通信能力。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向移动互联终端...应用的智能处理器"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_smart_processor_to_smart_home",
        "from_node": "smart_processor",
        "to_node": "smart_home_device",
        "description": "智能处理器为智能家居设备提供本地AI推理、联网通信与人机交互能力。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向...智能家居...应用的智能处理器"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_smart_processor_to_wearable",
        "from_node": "smart_processor",
        "to_node": "wearable_device",
        "description": "低功耗智能处理器是可穿戴设备实现健康监测、运动追踪与无线连接的核心组件。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向...可穿戴设备...应用的智能处理器"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_cement_to_cement_product",
        "from_node": "cement",
        "to_node": "cement_product",
        "description": "水泥作为胶凝材料与骨料、水混合后成型养护，制成各类水泥制品和预制构件。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "上峰水泥 主营业务", "quote": "水泥及水泥制品的生产和销售"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pulp_to_viscose_fiber",
        "from_node": "pulp_for_viscose",
        "to_node": "viscose_fiber",
        "description": "粘胶浆粕经碱化、黄化、纺丝等化学工艺转化为粘胶纤维（统称）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:棉浆粕,粘胶纤维...的生产"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pulp_to_viscose_filament",
        "from_node": "pulp_for_viscose",
        "to_node": "viscose_filament",
        "description": "粘胶浆粕经纺丝工艺制成连续长丝，即粘胶长丝。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:棉浆粕,粘胶长丝"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_pulp_to_viscose_staple",
        "from_node": "pulp_for_viscose",
        "to_node": "viscose_staple",
        "description": "粘胶浆粕经纺丝后切断成特定长度的短纤维，即粘胶短丝（人造棉）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:棉浆粕,粘胶短丝"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_viscose_to_canvas",
        "from_node": "viscose_fiber",
        "to_node": "canvas_fabric",
        "description": "粘胶纤维经纺纱织造制成帆布织物，用于工业用布和运输遮盖。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:粘胶纤维...帆布"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_viscose_to_tire_cord",
        "from_node": "viscose_fiber",
        "to_node": "tire_cord_fabric",
        "description": "粘胶长丝经织造与浸胶处理制成轮胎帘子布，作为轮胎胎体增强骨架材料。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:粘胶长丝...帘子布"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_bearing_to_automotive_bearing",
        "from_node": "bearing",
        "to_node": "automotive_bearing",
        "description": "通用轴承技术经针对性设计与材料优化，适配汽车高转速、重载荷工况，形成汽车专用轴承产品。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "襄阳轴承 主营业务", "quote": "制造销售轴承及零部件,汽车零部件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_construction_machinery_to_bulldozer",
        "from_node": "construction_machinery",
        "to_node": "bulldozer",
        "description": "推土机是工程机械的重要门类，专用于土方推运与场地平整作业。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_construction_machinery_to_excavator",
        "from_node": "construction_machinery",
        "to_node": "excavator",
        "description": "挖掘机是工程机械的核心门类，用于土石方挖掘、装载与破碎作业。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_construction_machinery_to_road_roller",
        "from_node": "construction_machinery",
        "to_node": "road_roller",
        "description": "压路机是工程机械中专用于路基与路面压实的设备类别。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "edge_type_label": "组成",
        "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:推土机,挖掘机,压路机,配件"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_stock_image_to_visual_content",
        "from_node": "stock_image",
        "to_node": "visual_content_service",
        "description": "正版图片素材经版权管理平台授权分发，形成视觉内容服务，供媒体、广告及企业客户使用。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [{"source_title": "视觉中国 主营业务", "quote": "主营业务:视觉内容与服务"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_natural_alkali_to_soda_ash",
        "from_node": "natural_alkali",
        "to_node": "soda_ash",
        "description": "天然碱矿物经溶解、净化、蒸发结晶等工艺加工成工业纯碱（碳酸钠）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "博源化工 主营业务", "quote": "主要业务:天然碱和无机盐系列产品的生产和经营.主要产品:纯碱"}],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_soda_ash_to_baking_soda",
        "from_node": "soda_ash",
        "to_node": "baking_soda",
        "description": "纯碱溶液在碳化塔中吸收二氧化碳气体，反应结晶生成碳酸氢钠（小苏打）。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [{"source_title": "博源化工 主营业务", "quote": "主要产品:纯碱,小苏打"}],
        "confidence": "HIGH"
    }
]

# ---------------------------------------------------------------------------
# 3. COMPANIES (PostgreSQL)
# ---------------------------------------------------------------------------

companies = [
    {
        "company_id": "yingfang_micro",
        "name_zh": "盈方微电子股份有限公司",
        "name_en": "Infotm Microelectronics Co., Ltd.",
        "aliases": ["盈方微"],
        "stock_codes": ["000670.SZ"],
        "description": "面向移动互联终端、智能家居、可穿戴设备等应用的智能处理器及相关软件研发、设计、生产、销售，并提供硬件设计和软件应用的整体解决方案。",
        "country": "CN",
        "province": "湖北",
        "city": "荆州市",
        "founded_year": 1993,
        "employee_count": 133,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "shangfeng_cement",
        "name_zh": "甘肃上峰水泥股份有限公司",
        "name_en": "Ganshu Shangfeng Cement Co., Ltd.",
        "aliases": ["上峰水泥"],
        "stock_codes": ["000672.SZ"],
        "description": "主营业务变更为水泥及水泥制品的生产和销售。",
        "country": "CN",
        "province": "甘肃",
        "city": "白银市",
        "founded_year": 1997,
        "employee_count": 2581,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "zhidu_share",
        "name_zh": "智度科技股份有限公司",
        "name_en": "Zhidu Technology Co., Ltd.",
        "aliases": ["智度股份"],
        "stock_codes": ["000676.SZ"],
        "description": "主要业务包括互联网媒体业务、数字营销业务和新零售、自有品牌、区块链、互联网金融等其他业务。",
        "country": "CN",
        "province": "广东",
        "city": "广州市",
        "founded_year": 1996,
        "employee_count": 456,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "st_hailong",
        "name_zh": "恒天海龙股份有限公司",
        "name_en": "Hengtian Hailong Co., Ltd.",
        "aliases": ["ST海龙", "恒天海龙"],
        "stock_codes": ["000677.SZ"],
        "description": "主要业务为棉浆粕、粘胶纤维、帘帆布的生产与销售。主要产品包括粘胶长丝、粘胶短丝、浆粕、帆布、帘子布。",
        "country": "CN",
        "province": "山东",
        "city": "潍坊市",
        "founded_year": 1989,
        "employee_count": 984,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "xiangyang_bearing",
        "name_zh": "襄阳汽车轴承股份有限公司",
        "name_en": "Xiangyang Automotive Bearing Co., Ltd.",
        "aliases": ["襄阳轴承"],
        "stock_codes": ["000678.SZ"],
        "description": "主要产品为轴承及零部件、汽车零部件、机电设备、轴承设备及备件。",
        "country": "CN",
        "province": "湖北",
        "city": "襄阳市",
        "founded_year": 1993,
        "employee_count": 2486,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "dalian_friendship",
        "name_zh": "大连友谊(集团)股份有限公司",
        "name_en": "Dalian Friendship (Group) Co., Ltd.",
        "aliases": ["大连友谊"],
        "stock_codes": ["000679.SZ"],
        "description": "主要业务为百货零售、酒店服务、房地产开发及销售。",
        "country": "CN",
        "province": "辽宁",
        "city": "大连市",
        "founded_year": 1992,
        "employee_count": 332,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "shantui_share",
        "name_zh": "山推工程机械股份有限公司",
        "name_en": "Shantui Construction Machinery Co., Ltd.",
        "aliases": ["山推股份"],
        "stock_codes": ["000680.SZ"],
        "description": "主要产品包括推土机、挖掘机、压路机及工程机械配件，涵盖土方工程机械的研发、制造与销售。",
        "country": "CN",
        "province": "山东",
        "city": "济宁市",
        "founded_year": 1993,
        "employee_count": 7247,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "visual_china",
        "name_zh": "视觉(中国)文化发展股份有限公司",
        "name_en": "Visual China Group Co., Ltd.",
        "aliases": ["视觉中国"],
        "stock_codes": ["000681.SZ"],
        "description": "主营业务包括视觉内容与服务、视觉数字娱乐、视觉社交社区三大板块。",
        "country": "CN",
        "province": "江苏",
        "city": "常州市",
        "founded_year": 1994,
        "employee_count": 466,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "dongfang_electronics",
        "name_zh": "东方电子股份有限公司",
        "name_en": "Dongfang Electronics Co., Ltd.",
        "aliases": ["东方电子"],
        "stock_codes": ["000682.SZ"],
        "description": "主要产品包括电力调度、保护及配电自动化系统、信息管理系统、电子设备与材料。",
        "country": "CN",
        "province": "山东",
        "city": "烟台市",
        "founded_year": 1994,
        "employee_count": 8153,
        "company_type": "public",
        "status": "ACTIVE"
    },
    {
        "company_id": "boyuan_chemical",
        "name_zh": "内蒙古博源化工股份有限公司",
        "name_en": "Inner Mongolia Boyuan Chemical Co., Ltd.",
        "aliases": ["博源化工"],
        "stock_codes": ["000683.SZ"],
        "description": "主要业务为天然碱和无机盐系列产品的生产和经营。主要产品包括纯碱、小苏打。",
        "country": "CN",
        "province": "内蒙古",
        "city": "鄂尔多斯市",
        "founded_year": 1997,
        "employee_count": 4755,
        "company_type": "public",
        "status": "ACTIVE"
    }
]

# ---------------------------------------------------------------------------
# 4. COMPANY NODE EXPOSURES (PostgreSQL)
# ---------------------------------------------------------------------------

exposures = [
    # 盈方微
    {"exposure_id": "exp_yingfang_smart_processor", "company_id": "yingfang_micro", "node_id": "smart_processor", "activity_type": "manufacture", "role": "智能处理器设计制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "盈方微 主营业务", "quote": "智能处理器及相关软件研发,设计,生产,销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_yingfang_semiconductor", "company_id": "yingfang_micro", "node_id": "semiconductor_device", "activity_type": "manufacture", "role": "集成电路芯片研发商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "盈方微 经营范围", "quote": "集成电路芯片,电子产品及计算机软硬件的研发,设计和销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_yingfang_mobile_terminal", "company_id": "yingfang_micro", "node_id": "mobile_terminal", "activity_type": "design", "role": "移动终端解决方案提供商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向移动互联终端...应用的智能处理器...并提供硬件设计和软件应用的整体解决方案"}], "status": "ACTIVE"},
    {"exposure_id": "exp_yingfang_smart_home", "company_id": "yingfang_micro", "node_id": "smart_home_device", "activity_type": "design", "role": "智能家居解决方案提供商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向...智能家居...应用的智能处理器"}], "status": "ACTIVE"},
    {"exposure_id": "exp_yingfang_wearable", "company_id": "yingfang_micro", "node_id": "wearable_device", "activity_type": "design", "role": "可穿戴设备解决方案提供商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "盈方微 主营业务", "quote": "面向...可穿戴设备...应用的智能处理器"}], "status": "ACTIVE"},

    # 上峰水泥
    {"exposure_id": "exp_shangfeng_cement", "company_id": "shangfeng_cement", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "上峰水泥 主营业务", "quote": "水泥及水泥制品的生产和销售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_shangfeng_cement_product", "company_id": "shangfeng_cement", "node_id": "cement_product", "activity_type": "produce", "role": "水泥制品生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "上峰水泥 主营业务", "quote": "水泥及水泥制品的生产和销售"}], "status": "ACTIVE"},

    # 智度股份
    {"exposure_id": "exp_zhidu_internet_media", "company_id": "zhidu_share", "node_id": "internet_media_service", "activity_type": "operate", "role": "互联网媒体运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "智度股份 主营业务", "quote": "互联网媒体业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zhidu_digital_marketing", "company_id": "zhidu_share", "node_id": "digital_marketing_service", "activity_type": "operate", "role": "数字营销服务商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "智度股份 主营业务", "quote": "数字营销业务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_zhidu_advertising", "company_id": "zhidu_share", "node_id": "advertising_service", "activity_type": "operate", "role": "广告服务运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "智度股份 经营范围", "quote": "广告设计,代理,广告制作,广告发布"}], "status": "ACTIVE"},

    # ST海龙
    {"exposure_id": "exp_hailong_viscose_fiber", "company_id": "st_hailong", "node_id": "viscose_fiber", "activity_type": "produce", "role": "粘胶纤维生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:粘胶长丝,粘胶短丝,浆粕,帆布,帘子布"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hailong_viscose_filament", "company_id": "st_hailong", "node_id": "viscose_filament", "activity_type": "produce", "role": "粘胶长丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:粘胶长丝"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hailong_viscose_staple", "company_id": "st_hailong", "node_id": "viscose_staple", "activity_type": "produce", "role": "粘胶短丝生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:粘胶短丝"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hailong_pulp", "company_id": "st_hailong", "node_id": "pulp_for_viscose", "activity_type": "produce", "role": "粘胶浆粕生产商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:棉浆粕"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hailong_canvas", "company_id": "st_hailong", "node_id": "canvas_fabric", "activity_type": "produce", "role": "帆布生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:帆布"}], "status": "ACTIVE"},
    {"exposure_id": "exp_hailong_tire_cord", "company_id": "st_hailong", "node_id": "tire_cord_fabric", "activity_type": "produce", "role": "帘子布生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "ST海龙 主营业务", "quote": "主要产品:帘子布"}], "status": "ACTIVE"},

    # 襄阳轴承
    {"exposure_id": "exp_xy_bearing", "company_id": "xiangyang_bearing", "node_id": "bearing", "activity_type": "manufacture", "role": "轴承制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "襄阳轴承 主营业务", "quote": "主要产品:轴承"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xy_rolling_bearing", "company_id": "xiangyang_bearing", "node_id": "rolling_bearing", "activity_type": "manufacture", "role": "滚动轴承制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "襄阳轴承 经营范围", "quote": "制造销售轴承及零部件"}], "status": "ACTIVE"},
    {"exposure_id": "exp_xy_automotive_bearing", "company_id": "xiangyang_bearing", "node_id": "automotive_bearing", "activity_type": "manufacture", "role": "汽车轴承制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "襄阳轴承 经营范围", "quote": "制造销售轴承及零部件,汽车零部件"}], "status": "ACTIVE"},

    # 大连友谊
    {"exposure_id": "exp_dl_friendship_dept", "company_id": "dalian_friendship", "node_id": "department_store", "activity_type": "operate", "role": "百货零售商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "大连友谊 主营业务", "quote": "主要业务:百货零售"}], "status": "ACTIVE"},
    {"exposure_id": "exp_dl_friendship_hotel", "company_id": "dalian_friendship", "node_id": "hotel_operation_service", "activity_type": "operate", "role": "酒店运营商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "大连友谊 主营业务", "quote": "酒店服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_dl_friendship_realestate", "company_id": "dalian_friendship", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "大连友谊 主营业务", "quote": "房地产开发及销售"}], "status": "ACTIVE"},

    # 山推股份
    {"exposure_id": "exp_shantui_bulldozer", "company_id": "shantui_share", "node_id": "bulldozer", "activity_type": "manufacture", "role": "推土机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:推土机"}], "status": "ACTIVE"},
    {"exposure_id": "exp_shantui_excavator", "company_id": "shantui_share", "node_id": "excavator", "activity_type": "manufacture", "role": "挖掘机制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:挖掘机"}], "status": "ACTIVE"},
    {"exposure_id": "exp_shantui_road_roller", "company_id": "shantui_share", "node_id": "road_roller", "activity_type": "manufacture", "role": "压路机制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "山推股份 主营业务", "quote": "主要产品:压路机"}], "status": "ACTIVE"},
    {"exposure_id": "exp_shantui_construction_machinery", "company_id": "shantui_share", "node_id": "construction_machinery", "activity_type": "manufacture", "role": "工程机械综合制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "山推股份 经营范围", "quote": "建筑工程用机械制造;建筑工程用机械销售;矿山机械制造"}], "status": "ACTIVE"},

    # 视觉中国
    {"exposure_id": "exp_visualchina_content", "company_id": "visual_china", "node_id": "visual_content_service", "activity_type": "provide_service", "role": "视觉内容服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "视觉中国 主营业务", "quote": "主营业务:视觉内容与服务"}], "status": "ACTIVE"},
    {"exposure_id": "exp_visualchina_stock_image", "company_id": "visual_china", "node_id": "stock_image", "activity_type": "provide_service", "role": "正版图片素材提供商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "视觉中国 经营范围", "quote": "摄像及视频制作服务;图文设计制作;摄影扩印服务"}], "status": "ACTIVE"},

    # 东方电子
    {"exposure_id": "exp_dongfang_dispatch", "company_id": "dongfang_electronics", "node_id": "power_dispatching_system", "activity_type": "manufacture", "role": "电力调度系统制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东方电子 主营业务", "quote": "主要产品:电力调度,保护及配电自动化系统"}], "status": "ACTIVE"},
    {"exposure_id": "exp_dongfang_protection", "company_id": "dongfang_electronics", "node_id": "power_protection_system", "activity_type": "manufacture", "role": "电力保护系统制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东方电子 主营业务", "quote": "主要产品:电力调度,保护及配电自动化系统"}], "status": "ACTIVE"},
    {"exposure_id": "exp_dongfang_automation", "company_id": "dongfang_electronics", "node_id": "power_automation_system", "activity_type": "manufacture", "role": "配电自动化系统制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "东方电子 主营业务", "quote": "主要产品:电力调度,保护及配电自动化系统"}], "status": "ACTIVE"},
    {"exposure_id": "exp_dongfang_distribution_equip", "company_id": "dongfang_electronics", "node_id": "power_distribution_equipment", "activity_type": "manufacture", "role": "配电设备制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "东方电子 经营范围", "quote": "输配电及控制设备制造;配电开关控制设备制造"}], "status": "ACTIVE"},

    # 博源化工
    {"exposure_id": "exp_boyuan_natural_alkali", "company_id": "boyuan_chemical", "node_id": "natural_alkali", "activity_type": "produce", "role": "天然碱生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "博源化工 主营业务", "quote": "主要业务:天然碱和无机盐系列产品的生产和经营"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boyuan_soda_ash", "company_id": "boyuan_chemical", "node_id": "soda_ash", "activity_type": "produce", "role": "纯碱生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "博源化工 主营业务", "quote": "主要产品:纯碱"}], "status": "ACTIVE"},
    {"exposure_id": "exp_boyuan_baking_soda", "company_id": "boyuan_chemical", "node_id": "baking_soda", "activity_type": "produce", "role": "小苏打生产商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "博源化工 主营业务", "quote": "主要产品:小苏打"}], "status": "ACTIVE"}
]

# ---------------------------------------------------------------------------
# 5. SUBMIT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph_batch = {
        "batch_id": "batch_021_graph",
        "task_description": "Batch 021: Industrial nodes and edges for 10 companies (000670-000683). Focus on smart processors, cement, viscose fiber, bearings, construction machinery, visual content, power systems, and alkali chemicals.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }

    business_batch = {
        "batch_id": "batch_021_business",
        "task_description": "Batch 021: Company registrations and node exposures for 10 companies (000670-000683).",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies,
        "company_node_exposures_to_upsert": exposures
    }

    print("Submitting graph batch...")
    status, resp = submit_graph_batch(graph_batch)
    print(f"Graph batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    print("\nSubmitting business batch...")
    status, resp = submit_business_batch(business_batch)
    print(f"Business batch status: {status}")
    print(json.dumps(resp, ensure_ascii=False, indent=2))
