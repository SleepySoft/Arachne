import asyncio
import httpx

EDGES = [
    ("silicon_material_flow_silicon_wafer", "silicon", "silicon_wafer", "material_flow", "高纯硅材料作为硅片制造的原材料"),
    ("photoresist_material_flow_wafer", "photoresist", "wafer", "material_flow", "光刻胶涂覆在晶圆表面用于光刻图形转移"),
    ("euv_photoresist_material_flow_wafer", "euv_photoresist", "wafer", "material_flow", "EUV 光刻胶用于先进制程晶圆光刻"),
    ("duv_photoresist_material_flow_wafer", "duv_photoresist", "wafer", "material_flow", "DUV 光刻胶用于成熟制程晶圆光刻"),
    ("cmp_slurry_material_flow_wafer", "cmp_slurry", "wafer", "material_flow", "CMP 抛光液用于晶圆表面平坦化"),
    ("sputtering_target_material_flow_wafer", "sputtering_target", "wafer", "material_flow", "溅射靶材通过 PVD 沉积到晶圆表面形成金属层"),
    ("wafer_material_flow_foundry", "wafer", "foundry", "material_flow", "晶圆作为输入进入晶圆代工厂进行加工"),
    ("wafer_material_flow_idm", "wafer", "idm", "material_flow", "晶圆作为输入进入 IDM 制造环节"),
    ("memory_wafer_material_flow_foundry", "memory_wafer", "foundry", "material_flow", "存储晶圆进入代工厂/存储厂加工"),
    ("advanced_process_node_capability_foundry", "advanced_process_node", "foundry", "capability_supply", "先进制程能力是晶圆代工的核心能力支撑"),
    ("mature_process_node_capability_foundry", "mature_process_node", "foundry", "capability_supply", "成熟制程能力是晶圆代工的核心能力支撑"),
    ("advanced_process_node_capability_idm", "advanced_process_node", "idm", "capability_supply", "先进制程能力支撑 IDM 制造"),
    ("mature_process_node_capability_idm", "mature_process_node", "idm", "capability_supply", "成熟制程能力支撑 IDM 制造"),
    ("eda_software_capability_fabless", "eda_software", "fabless", "capability_supply", "EDA 工具为无晶圆设计公司提供设计能力"),
    ("eda_software_capability_idm_design", "eda_software", "idm", "capability_supply", "EDA 工具支撑 IDM 的设计环节"),
    ("ip_core_composition_soc", "ip_core", "soc", "composition", "IP 核是 SoC 芯片的组成模块"),
    ("ip_core_composition_cpu", "ip_core", "cpu", "composition", "CPU IP 核是 CPU 芯片的核心组成"),
    ("foundry_capability_chip", "foundry", "chip", "capability_supply", "晶圆代工厂通过制造能力产出芯片"),
    ("idm_capability_chip", "idm", "chip", "capability_supply", "IDM 通过制造能力产出芯片"),
    ("chip_material_flow_osat", "chip", "osat", "material_flow", "未封装芯片流入 OSAT 进行封装测试"),
    ("packaging_substrate_material_flow_osat", "packaging_substrate", "osat", "material_flow", "封装基板流入 OSAT 用于芯片封装"),
    ("dram_chip_material_flow_memory_chip", "dram_chip", "memory_chip", "material_flow", "DRAM 芯片是存储芯片的重要组成"),
    ("nand_flash_chip_material_flow_memory_chip", "nand_flash_chip", "memory_chip", "material_flow", "NAND Flash 芯片是存储芯片的重要组成"),
    ("memory_chip_material_flow_server", "memory_chip", "server", "material_flow", "存储芯片是服务器的核心部件"),
    ("memory_chip_material_flow_personal_computer", "memory_chip", "personal_computer", "material_flow", "存储芯片是 PC 的核心部件"),
    ("cpu_material_flow_server", "cpu", "server", "material_flow", "CPU 是服务器的核心计算部件"),
    ("cpu_material_flow_personal_computer", "cpu", "personal_computer", "material_flow", "CPU 是 PC 的核心计算部件"),
    ("gpu_material_flow_server", "gpu", "server", "material_flow", "GPU/AI 加速器是服务器算力扩展部件"),
    ("gpu_material_flow_data_center", "gpu", "data_center", "material_flow", "GPU/AI 加速器是数据中心核心算力"),
    ("ai_accelerator_material_flow_data_center", "ai_accelerator", "data_center", "material_flow", "AI 加速器是数据中心 AI 算力核心"),
    ("power_semiconductor_material_flow_new_energy_vehicle", "power_semiconductor", "new_energy_vehicle", "material_flow", "功率半导体是新能源汽车电驱电控核心"),
    ("mcu_material_flow_automotive_electronics", "mcu", "automotive_electronics", "material_flow", "MCU 是汽车电子控制单元核心"),
    ("cis_material_flow_smartphone", "cis", "smartphone", "material_flow", "CIS 是智能手机摄像头核心部件"),
    ("rf_chip_material_flow_smartphone", "rf_chip", "smartphone", "material_flow", "射频芯片是智能手机通信核心"),
    ("soc_material_flow_smartphone", "soc", "smartphone", "material_flow", "SoC 是智能手机主控芯片"),
    ("pmic_material_flow_smartphone", "pmic", "smartphone", "material_flow", "PMIC 是智能手机电源管理核心"),
]

BATCH = {
    "batch_id": "semiconductor_relations_upstream_downstream_001",
    "task_description": "补充半导体产业图中缺失的上下游关系（材料/设备/制造/封测之间的 material_flow 与 capability_supply）",
    "nodes_to_upsert": [],
    "edges_to_upsert": [
        {
            "edge_namespace": "industrial_flow",
            "edge_id": eid,
            "from_node": src,
            "to_node": tgt,
            "edge_type": etype,
            "description": desc,
            "confidence": "HIGH",
            "evidence": [{"source_title": "半导体产业链公司研报", "quote": desc}],
        }
        for eid, src, tgt, etype, desc in EDGES
    ],
    "rejected_or_pending": []
}


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.post("http://localhost:16060/api/v1/batches", json=BATCH)
        print(r.status_code)
        print(r.json())


asyncio.run(main())
