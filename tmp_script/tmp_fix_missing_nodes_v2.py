#!/usr/bin/env python3
"""Fix missing nodes (flat_glass, sugar_cane, oilfield_service, public_transportation, ship)
and re-submit failed edges from batches 031-033."""
import requests
BASE_URL = "http://localhost:8000/api/v1"
submit_graph = lambda b: requests.post(f"{BASE_URL}/batches", json=b)

nodes = [
    {
        "node_id": "flat_glass",
        "canonical_name_zh": "平板玻璃",
        "canonical_name_en": "Flat Glass",
        "aliases": ["浮法玻璃", "白片玻璃", "钠钙玻璃"],
        "definition": "以石英砂、纯碱、石灰石、长石等无机矿物为主要原料，经1600℃高温熔融、成型（主要为浮法工艺）、退火等工序制成的板状钠钙硅酸盐玻璃。具有透光、透明、隔声等性能，是建筑采光、汽车车窗、光伏面板和电子显示等领域不可替代的基础材料。",
        "entity_type": "material",
        "evidence": [
            {"source_title": "《平板玻璃术语》(GB/T15764-2008)", "quote": "平板玻璃为板状的硅酸盐玻璃"},
            {"source_title": "头豹研究院 平板玻璃行业报告", "quote": "平板玻璃一般由石英砂、石灰石、长石、纯碱等无机矿物为原料制作，化学成分归属于纳钙硅酸盐玻璃"}
        ],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "sugar_cane",
        "canonical_name_zh": "甘蔗",
        "canonical_name_en": "Sugar Cane",
        "aliases": ["糖料甘蔗", "蔗"],
        "definition": "禾本科甘蔗属热带及亚热带多年生草本植物，茎秆富含蔗糖（12%-18%），是全球最重要的糖料作物（占全球食糖产量86%以上）。主要种植于南北纬34°之间的热带亚热带地区，中国主产区为广西、云南、广东、海南。除制糖外，蔗渣可造纸和生产环保餐具，糖蜜可发酵生产酒精和酵母，是综合利用价值极高的经济作物。",
        "entity_type": "material",
        "evidence": [
            {"source_title": "经合组织-粮农组织2022-2031农业展望", "quote": "甘蔗是主要的(86%)糖料作物，主要用于制糖，同时也用于生产乙醇"},
            {"source_title": "甘蔗制糖 百度百科", "quote": "甘蔗是禾本科植物...中国种植甘蔗的省（区）有14个，以广东、广西、台湾、云南、福建等为主"}
        ],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "oilfield_service",
        "canonical_name_zh": "油气田服务",
        "canonical_name_en": "Oilfield Service",
        "aliases": ["油田技术服务", "油服", "OFS"],
        "definition": "以油气田为主要工作场所，为石油天然气勘探、钻井、完井、采油、增产、集输及后期维护提供工程技术支持和解决方案的生产性服务行业。涵盖地球物理勘探、钻井工程、测井录井、完井修井、油气生产处理、油田化学品供应和油田信息化建设等五大板块，是油气产业链上游的重要组成部分。",
        "entity_type": "service",
        "evidence": [
            {"source_title": "中国油田服务行业市场发展监测及投资方向研究报告", "quote": "中国油田服务行业是指为油气勘探、开发和生产提供各种技术支持和服务的行业...涵盖从油田地质勘探、钻井、完井、油气生产到后期维护等多个环节"},
            {"source_title": "新疆科力新技术发展股份有限公司公开转让说明书", "quote": "油田技术服务业，是伴随着油气资源勘探开发而形成的，是为石油天然气勘探与开发提供工程技术支持和解决方案的生产性服务行业"}
        ],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "public_transportation",
        "canonical_name_zh": "公共交通",
        "canonical_name_en": "Public Transportation",
        "aliases": ["公共运输", "大众运输", "公交系统"],
        "definition": "在城市或城际范围内向公众开放的、定线运营的客运交通服务系统，包括公共汽车、轨道交通（地铁、轻轨、有轨电车）、快速公交系统（BRT）、渡轮、索道等多种运输方式。公共交通系统由道路/轨道网络、交通工具、站点设施和运营管理系统构成，是城市客运的骨干和缓解交通拥堵的关键基础设施。",
        "entity_type": "service",
        "evidence": [
            {"source_title": "公共交通 百度百科", "quote": "公共交通(Mass transit)，泛指所有收费提供交通服务的运输方式...狭义的公共交通包括城市范围内定线运营的公共汽车及轨道交通、渡轮、索道等交通方式"},
            {"source_title": "《城市公共交通分类标准》(CJJ/T 114-2007)", "quote": "城市公共交通分类标准"}
        ],
        "confidence": "HIGH",
        "status": "ACTIVE"
    },
    {
        "node_id": "ship",
        "canonical_name_zh": "船舶",
        "canonical_name_en": "Ship",
        "aliases": ["船只", "舰船", "海船"],
        "definition": "能航行或停泊于水域进行运输或作业的交通工具，通常由船体、推进系统、导航设备和各类功能舱室组成。按用途可分为运输船（货船、客船、油轮、集装箱船等）、工程船（挖泥船、起重船等）、渔业船、军用舰艇等；按航区可分为海船和内河船。船舶是水上交通运输、海洋资源开发和国防建设的核心装备，现代船舶多为钢制结构，采用内燃机或电力推进。",
        "entity_type": "system",
        "evidence": [
            {"source_title": "《船舶与海洋结构物构造》华南理工大学", "quote": "船舶按航区分：海船和内河船。按推进动力分：风帆船，蒸汽机船，内燃机船和核动力船。按用途可分为运输船、工程船、渔业船、港务船、海洋调查船、战斗舰艇等"},
            {"source_title": "前瞻产业研究院 2024年中国船舶制造行业全景图谱", "quote": "船舶是能航行或停泊于水域进行运输或作业的交通工具...为海洋开发、水上交通运输、能源运输、国防建设等提供必要的技术装备"}
        ],
        "confidence": "HIGH",
        "status": "ACTIVE"
    }
]

edges = [
    {
        "edge_id": "flow_soda_ash_to_glass",
        "from_node": "soda_ash",
        "to_node": "flat_glass",
        "description": "纯碱作为助熔剂与石英砂、石灰石等原料经高温熔融制成平板玻璃。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [
            {"source_title": "平板玻璃行业头豹词条报告", "quote": "原材料成本占生产成本的43%，其中纯碱占比最大，为54%"},
            {"source_title": "《平板玻璃生产全流程解析》", "quote": "采用石英砂（二氧化硅含量＞99%）、纯碱及白云石作为基础原料"}
        ],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_sugar_cane_to_white_sugar",
        "from_node": "sugar_cane",
        "to_node": "white_sugar",
        "description": "甘蔗经压榨提汁、清净、蒸发、结晶、分蜜和干燥等工序制成白砂糖。",
        "edge_namespace": "industrial_flow",
        "edge_type": "material_flow",
        "evidence": [
            {"source_title": "甘蔗制糖 百度百科", "quote": "甘蔗制糖是以甘蔗为原料，通过提汁、清净、蒸发、结晶、分蜜和干燥等工序生产白砂糖、粗糖等产品的工艺过程"},
            {"source_title": "新华社 '甜蜜'的'秘密'", "quote": "甘蔗压榨后，除了可以生产白糖，还可以产出糖蜜、蔗渣、滤泥等副产物"}
        ],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_drilling_tool_to_oilfield",
        "from_node": "oil_drilling_tool",
        "to_node": "oilfield_service",
        "description": "石油钻具（钻头、钻杆、井下工具等）是油气田服务中钻井工程环节的核心装备。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [
            {"source_title": "石化机械 主营业务", "quote": "产品包含钻头钻具及井下工具、陆上钻采装备、固井压裂装备、海洋石油装备和油气储运设备等多个领域的产品组合"},
            {"source_title": "中国油田服务行业市场发展监测报告", "quote": "油田服务行业涵盖从油田地质勘探、钻井、完井、油气生产到后期维护等多个环节"}
        ],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_bus_to_transport",
        "from_node": "bus",
        "to_node": "public_transportation",
        "description": "客车（公共汽车）作为公共交通工具用于城市及城际旅客运输服务。",
        "edge_namespace": "industrial_flow",
        "edge_type": "service_flow",
        "evidence": [
            {"source_title": "公共交通 百度百科", "quote": "狭义的公共交通包括城市范围内定线运营的公共汽车及轨道交通、渡轮、索道等交通方式"},
            {"source_title": "《城市公共交通常用名词术语》", "quote": "公共汽车：有固定的线路和车站，供公众乘用的汽车"}
        ],
        "confidence": "HIGH"
    },
    {
        "edge_id": "flow_marine_engine_to_ship",
        "from_node": "marine_engine",
        "to_node": "ship",
        "description": "船用发动机（柴油机、汽轮机等）作为推进动力核心装配于船舶。",
        "edge_namespace": "industrial_flow",
        "edge_type": "composition",
        "evidence": [
            {"source_title": "《船舶与海洋结构物构造》华南理工大学", "quote": "按推进动力分：风帆船，蒸汽机船，内燃机船和核动力船"},
            {"source_title": "潍柴重机 经营范围", "quote": "船用配套设备制造；船舶自动化、检测、监控系统制造"}
        ],
        "confidence": "HIGH"
    }
]

if __name__ == "__main__":
    gb = {
        "batch_id": "batch_fix_missing_nodes_v2_graph",
        "task_description": "Fix: Create 5 missing nodes (flat_glass, sugar_cane, oilfield_service, public_transportation, ship) and re-submit 5 failed edges from batches 031-033.",
        "nodes_to_upsert": nodes,
        "edges_to_upsert": edges,
        "rejected_or_pending": []
    }
    r = submit_graph(gb)
    print(f"Graph fix v2: {r.status_code}", r.json())
