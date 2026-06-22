# -*- coding: utf-8 -*-
"""
Refactor the wafer hub to reduce mixed semantics.
- Create process nodes for wafer manufacturing and individual process steps.
- Redirect equipment nodes to process nodes (capability_supply).
- Redirect material nodes to process nodes (material_flow).
- Separate chip design from wafer manufacturing.
- Remove direct equipment/material -> wafer edges.
"""
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

EVIDENCE = {
    "process": {"source_title": "半导体制造工艺通用分类", "quote": "半导体制造主要包括光刻、刻蚀、薄膜沉积、离子注入、CMP、清洗、量测检测等工艺环节。"},
}

NEW_NODES = [
    {
        "node_id": "wafer_manufacturing",
        "canonical_name_zh": "晶圆制造",
        "canonical_name_en": "Wafer Manufacturing",
        "definition": "将硅片等半导体衬底通过光刻、刻蚀、薄膜沉积、离子注入、CMP、清洗等工艺加工为晶圆或芯片的制造过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "chip_design",
        "canonical_name_zh": "芯片设计",
        "canonical_name_en": "Chip Design",
        "definition": "根据功能需求进行电路设计、逻辑综合、物理实现、验证并输出掩膜版数据的过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "lithography_process",
        "canonical_name_zh": "光刻工艺",
        "canonical_name_en": "Lithography Process",
        "definition": "利用光刻胶和光刻设备将掩膜版图形转移到晶圆表面的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "etching_process",
        "canonical_name_zh": "刻蚀工艺",
        "canonical_name_en": "Etching Process",
        "definition": "按光刻图形选择性去除晶圆表面材料的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "thin_film_deposition_process",
        "canonical_name_zh": "薄膜沉积工艺",
        "canonical_name_en": "Thin Film Deposition Process",
        "definition": "在晶圆表面沉积介质、金属等薄膜材料的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "ion_implantation_process",
        "canonical_name_zh": "离子注入工艺",
        "canonical_name_en": "Ion Implantation Process",
        "definition": "将掺杂离子注入晶圆以改变其电学性能的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "cleaning_process",
        "canonical_name_zh": "清洗工艺",
        "canonical_name_en": "Cleaning Process",
        "definition": "去除晶圆表面颗粒、有机物、金属离子等污染物的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "cmp_process",
        "canonical_name_zh": "CMP工艺",
        "canonical_name_en": "CMP Process",
        "definition": "化学机械抛光，用于平坦化晶圆表面介质或金属薄膜的工艺过程。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
    {
        "node_id": "metrology_inspection",
        "canonical_name_zh": "量测检测",
        "canonical_name_en": "Metrology and Inspection",
        "definition": "对晶圆/芯片关键尺寸、缺陷、电学参数等进行测量和检测的环节。",
        "entity_type": "process",
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [EVIDENCE["process"]],
    },
]

EDGES_TO_DELETE = [
    # equipment -> wafer
    "cleaning_equipment_to_wafer",
    "cmp_equipment_to_wafer",
    "deposition_equipment_processes_wafer",
    "etching_machine_processes_wafer",
    "ion_implanter_processes_wafer",
    "lithography_machine_processes_wafer",
    "metrology_equipment_to_wafer",
    "track_to_wafer",
    # materials -> wafer
    "cmp_slurry_material_flow_wafer",
    "duv_photoresist_material_flow_wafer",
    "electronic_special_gases_to_wafer",
    "euv_photoresist_material_flow_wafer",
    "photoresist_material_flow_wafer",
    "silicon_wafer_composes_wafer",
    "sputtering_target_material_flow_wafer",
    "wet_chemicals_to_wafer",
    # wafer -> service modes
    "wafer_material_flow_foundry",
    "wafer_material_flow_idm",
]

NEW_EDGES = [
    # silicon_wafer -> wafer as material_flow
    {"edge_id": "silicon_wafer_to_wafer", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "silicon_wafer", "to_node": "wafer",
     "description": "硅片作为晶圆制造的基础原材料，经过加工成为晶圆。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体制造流程", "quote": "硅片经过光刻、刻蚀、薄膜沉积等工艺加工为晶圆。"}]},

    # equipment -> process (capability_supply)
    {"edge_id": "lithography_machine_to_lithography_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "lithography_machine", "to_node": "lithography_process",
     "description": "光刻机为光刻工艺提供曝光图形转移能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "光刻机是执行光刻工艺的核心设备。"}]},
    {"edge_id": "track_coater_developer_to_lithography_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "track_coater_developer", "to_node": "lithography_process",
     "description": "涂胶显影设备为光刻工艺提供涂胶、显影能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "涂胶显影设备是光刻工艺的重要配套设备。"}]},
    {"edge_id": "etching_machine_to_etching_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "etching_machine", "to_node": "etching_process",
     "description": "刻蚀机为刻蚀工艺提供材料去除能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "刻蚀机是执行刻蚀工艺的核心设备。"}]},
    {"edge_id": "deposition_equipment_to_thin_film_deposition_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "deposition_equipment", "to_node": "thin_film_deposition_process",
     "description": "薄膜沉积设备为薄膜沉积工艺提供薄膜生长能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "薄膜沉积设备用于在晶圆表面沉积薄膜。"}]},
    {"edge_id": "ion_implanter_to_ion_implantation_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "ion_implanter", "to_node": "ion_implantation_process",
     "description": "离子注入机为离子注入工艺提供掺杂能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "离子注入机用于将掺杂离子注入晶圆。"}]},
    {"edge_id": "cmp_equipment_to_cmp_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "cmp_equipment", "to_node": "cmp_process",
     "description": "CMP设备为CMP工艺提供化学机械抛光能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "CMP设备用于晶圆表面平坦化。"}]},
    {"edge_id": "cleaning_equipment_to_cleaning_process", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "cleaning_equipment", "to_node": "cleaning_process",
     "description": "清洗设备为清洗工艺提供污染物去除能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "清洗设备用于去除晶圆表面污染物。"}]},
    {"edge_id": "metrology_equipment_to_metrology_inspection", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "metrology_equipment", "to_node": "metrology_inspection",
     "description": "量测设备为量测检测环节提供尺寸、缺陷等检测能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体设备与工艺对应关系", "quote": "量测设备用于晶圆关键尺寸和缺陷检测。"}]},

    # materials -> process (material_flow)
    {"edge_id": "photoresist_to_lithography_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "photoresist", "to_node": "lithography_process",
     "description": "光刻胶作为光刻工艺的核心感光材料。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "光刻胶用于光刻工艺中的图形转移。"}]},
    {"edge_id": "duv_photoresist_to_lithography_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "duv_photoresist", "to_node": "lithography_process",
     "description": "DUV光刻胶用于DUV光刻工艺。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "DUV光刻胶用于深紫外光刻工艺。"}]},
    {"edge_id": "euv_photoresist_to_lithography_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "euv_photoresist", "to_node": "lithography_process",
     "description": "EUV光刻胶用于EUV光刻工艺。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "EUV光刻胶用于极紫外光刻工艺。"}]},
    {"edge_id": "electronic_special_gases_to_thin_film_deposition_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronic_special_gases", "to_node": "thin_film_deposition_process",
     "description": "电子特气作为反应气体或载气用于薄膜沉积工艺。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "电子特气广泛用于薄膜沉积等工艺。"}]},
    {"edge_id": "electronic_special_gases_to_etching_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "electronic_special_gases", "to_node": "etching_process",
     "description": "电子特气作为刻蚀气体用于刻蚀工艺。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "部分电子特气用于刻蚀工艺中的反应气体。"}]},
    {"edge_id": "sputtering_target_to_thin_film_deposition_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "sputtering_target", "to_node": "thin_film_deposition_process",
     "description": "溅射靶材作为薄膜沉积工艺中的源材料。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "溅射靶材通过PVD等工艺在晶圆表面形成薄膜。"}]},
    {"edge_id": "wet_chemicals_to_cleaning_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "wet_chemicals", "to_node": "cleaning_process",
     "description": "湿电子化学品用于清洗工艺去除晶圆表面污染物。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "湿电子化学品用于晶圆清洗环节。"}]},
    {"edge_id": "wet_chemicals_to_etching_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "wet_chemicals", "to_node": "etching_process",
     "description": "部分湿电子化学品用于湿法刻蚀工艺。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "湿电子化学品也用于湿法刻蚀工艺。"}]},
    {"edge_id": "cmp_slurry_to_cmp_process", "edge_namespace": "industrial_flow", "edge_type": "material_flow",
     "from_node": "cmp_slurry", "to_node": "cmp_process",
     "description": "抛光液作为CMP工艺中的关键耗材。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体材料与工艺对应关系", "quote": "CMP抛光液用于化学机械抛光工艺。"}]},

    # chip design flow
    {"edge_id": "eda_software_to_chip_design", "edge_namespace": "industrial_flow", "edge_type": "capability_supply",
     "from_node": "eda_software", "to_node": "chip_design",
     "description": "EDA软件为芯片设计提供设计、仿真、验证能力。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "芯片设计工具链", "quote": "EDA软件是芯片设计不可或缺的工具。"}]},
    {"edge_id": "ip_core_to_chip_design", "edge_namespace": "industrial_flow", "edge_type": "information_flow",
     "from_node": "ip_core", "to_node": "chip_design",
     "description": "IP核作为可复用的设计模块输入芯片设计过程。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "芯片设计工具链", "quote": "IP核是芯片设计中的可复用功能模块。"}]},
    {"edge_id": "chip_design_to_wafer_manufacturing", "edge_namespace": "industrial_flow", "edge_type": "information_flow",
     "from_node": "chip_design", "to_node": "wafer_manufacturing",
     "description": "芯片设计输出的掩膜版数据和信息流向晶圆制造。", "confidence": "MEDIUM",
     "evidence": [{"source_title": "半导体制造流程", "quote": "芯片设计完成后，设计数据进入晶圆制造环节。"}]},
]


async def main():
    async with httpx.AsyncClient() as c:
        # 1. Create process nodes
        for node in NEW_NODES:
            r = await c.post(f"{BASE}/nodes", json=node)
            print(f"create {node['node_id']}: {r.status_code} {r.text[:120]}")

        # 2. Delete old edges
        for eid in EDGES_TO_DELETE:
            r = await c.delete(f"{BASE}/edges/{eid}")
            print(f"delete {eid}: {r.status_code}")

        # 3. Create new edges
        for e in NEW_EDGES:
            r = await c.post(f"{BASE}/edges", json=e)
            print(f"create {e['edge_id']}: {r.status_code} {r.text[:120]}")


asyncio.run(main())
