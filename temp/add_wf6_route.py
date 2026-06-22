# -*- coding: utf-8 -*-
import asyncio
import httpx

BATCH = {
    "batch_id": "semiconductor_wf6_alternative_route_001",
    "task_description": "补充六氟化钨（WF6）及其替代前驱体/薄膜路线：节点、本体关系与产业流",
    "nodes_to_upsert": [
        {
            "node_id": "tungsten_hexafluoride",
            "canonical_name_zh": "六氟化钨",
            "canonical_name_en": "Tungsten Hexafluoride",
            "aliases": ["WF6"],
            "definition": "半导体 CVD/ALD 钨薄膜核心前驱体，常温下为无色有毒气体，与还原剂反应在晶圆表面沉积高纯金属钨膜，用于接触孔、通孔、互连线及 3D NAND/DRAM 字线填充。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "湖北日报：日本部分六氟化钨厂商拟断供，对半导体产业有何影响？",
                "source_url": "https://news.hubeidaily.net/mobile/c_5347295.html",
                "quote": "在半导体制造中，六氟化钨主要作为化学气相沉积（CVD）工艺的关键前驱体...用于构建芯片内部的互连线、接触孔、通孔等导电结构。"
            }],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "tungsten_pentachloride",
            "canonical_name_zh": "五氯化钨",
            "canonical_name_en": "Tungsten Pentachloride",
            "aliases": ["WCl5"],
            "definition": "氟-free 钨前驱体候选材料，可作为 WF6 的替代品用于钨薄膜初始成核层，减少氟对超薄阻挡层/电介质的侵蚀，但成本与供给系统复杂度高于 WF6。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "Entegris White Paper: 96 Layers and Beyond: Solving 3D NAND Material and Integration Challenges",
                "source_url": "https://www.entegris.com/content/dam/web/resources/white-papers/whitepaper-solving-3d-nand-material-integration-challenges-8551.pdf",
                "quote": "Tungsten pentachloride (WCl5) is a potential substitute for WF6 but it has not been adopted in high volume because of its relatively high cost."
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "node_id": "tungsten_hexachloride",
            "canonical_name_zh": "六氯化钨",
            "canonical_name_en": "Tungsten Hexachloride",
            "aliases": ["WCl6"],
            "definition": "钨的氯化物前驱体之一，可作为 CVD-W 的替代来源，但存在残留氯损害与固态供给系统难度，尚未大规模量产。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "几种含钨前驱体的比较",
                "source_url": "https://zia-bj.org.cn/uploads_file/20210828/20210828164658_626.pdf",
                "quote": "WCl6，使用过程中残留的Cl会造成损害，并且WCl6不是气体，所以这给供给系统带来了比较大的麻烦。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "node_id": "tungsten_hexacarbonyl",
            "canonical_name_zh": "六羰基钨",
            "canonical_name_en": "Tungsten Hexacarbonyl",
            "aliases": ["W(CO)6"],
            "definition": "非腐蚀性钨前驱体，可用于沉积对氟敏感的栅极/扩散阻挡层，但成膜速度较慢且为固态，需配合专用输送系统。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "几种含钨前驱体的比较",
                "source_url": "https://zia-bj.org.cn/uploads_file/20210828/20210828164658_626.pdf",
                "quote": "W(CO)6，这个前驱体的问题是成膜的速度比较慢。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "node_id": "molybdenum_precursor",
            "canonical_name_zh": "钼前驱体",
            "canonical_name_en": "Molybdenum Precursor",
            "aliases": [],
            "definition": "ALD/CVD 钼薄膜的前驱体，可作为钨填充的替代路线，用于先进节点中高纵横比结构的金属化，避免氟污染。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "Lam Research ALTUS Product Family",
                "source_url": "https://www.lamresearch.com/zh-hans/product/altus-product-family/",
                "quote": "可使用ALD沉积钼(Mo)，以便更好地填充器件特征。或者，可使用非氟化卤化物前体来沉积钼，以避免在某些钨应用中造成的电介质损坏。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "node_id": "tungsten_film",
            "canonical_name_zh": "钨薄膜",
            "canonical_name_en": "Tungsten Film",
            "aliases": ["钨膜", "金属钨薄膜"],
            "definition": "通过 CVD/ALD 沉积的低电阻、高抗电迁移金属薄膜，用作芯片内部接触塞、通孔填充、局部互连及存储器字线。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "化工新材料系列(一) 电子特气：半导体新周期将至，国产替代如火如荼",
                "source_url": "https://pdf.dfcfw.com/pdf/H3_AP202305241587131051_1.pdf",
                "quote": "六氟化钨可通过化学气相淀积法(CVD)形成金属钨，用该法制成的钨具有低电阻率、高抗电迁移性以及填充小通孔时具优异平整性等优点。"
            }],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "node_id": "molybdenum_film",
            "canonical_name_zh": "钼薄膜",
            "canonical_name_en": "Molybdenum Film",
            "aliases": ["钼膜"],
            "definition": "通过 ALD/CVD 沉积的金属薄膜，可在部分先进互连/填充应用中替代钨薄膜，避免氟污染并改善台阶覆盖。",
            "entity_type": "material",
            "evidence": [{
                "source_title": "Lam Research ALTUS Product Family",
                "source_url": "https://www.lamresearch.com/zh-hans/product/altus-product-family/",
                "quote": "可使用ALD沉积钼(Mo)，以便更好地填充器件特征。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
    ],
    "edges_to_upsert": [
        {
            "edge_namespace": "ontology",
            "edge_id": "tungsten_hexafluoride_is_a_electronic_special_gases",
            "from_node": "tungsten_hexafluoride",
            "to_node": "electronic_special_gases",
            "edge_type": "is_a",
            "description": "六氟化钨是电子特种气体的一种，用于 CVD/ALD 钨沉积。",
            "evidence": [{
                "source_title": "湖北日报：日本部分六氟化钨厂商拟断供，对半导体产业有何影响？",
                "source_url": "https://news.hubeidaily.net/mobile/c_5347295.html",
                "quote": "六氟化钨（化学式WF6）是一种无机化合物，属于钨的高价氟化物...在半导体制造中，六氟化钨主要作为化学气相沉积（CVD）工艺的关键前驱体。"
            }],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "wf6_to_tungsten_film",
            "from_node": "tungsten_hexafluoride",
            "to_node": "tungsten_film",
            "edge_type": "material_flow",
            "description": "WF6 在 CVD/ALD 反应室中被还原，沉积为金属钨薄膜。",
            "evidence": [{
                "source_title": "湖北日报：日本部分六氟化钨厂商拟断供，对半导体产业有何影响？",
                "source_url": "https://news.hubeidaily.net/mobile/c_5347295.html",
                "quote": "在高温条件下，六氟化钨与氢气等还原剂发生反应，在晶圆表面沉积出金属钨薄膜。"
            }],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "wcl5_to_tungsten_film",
            "from_node": "tungsten_pentachloride",
            "to_node": "tungsten_film",
            "edge_type": "material_flow",
            "description": "WCl5 可作为氟-free 钨前驱体，沉积金属钨薄膜。",
            "evidence": [{
                "source_title": "Entegris White Paper: 96 Layers and Beyond: Solving 3D NAND Material and Integration Challenges",
                "source_url": "https://www.entegris.com/content/dam/web/resources/white-papers/whitepaper-solving-3d-nand-material-integration-challenges-8551.pdf",
                "quote": "Tungsten pentachloride (WCl5) is a potential substitute for WF6..."
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "wcl6_to_tungsten_film",
            "from_node": "tungsten_hexachloride",
            "to_node": "tungsten_film",
            "edge_type": "material_flow",
            "description": "WCl6 可作为钨薄膜沉积的替代前驱体。",
            "evidence": [{
                "source_title": "几种含钨前驱体的比较",
                "source_url": "https://zia-bj.org.cn/uploads_file/20210828/20210828164658_626.pdf",
                "quote": "WCl6...使用CVD-W技术的前驱体"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "wco6_to_tungsten_film",
            "from_node": "tungsten_hexacarbonyl",
            "to_node": "tungsten_film",
            "edge_type": "material_flow",
            "description": "W(CO)6 可作为非腐蚀性钨前驱体，沉积金属钨薄膜。",
            "evidence": [{
                "source_title": "几种含钨前驱体的比较",
                "source_url": "https://zia-bj.org.cn/uploads_file/20210828/20210828164658_626.pdf",
                "quote": "W(CO)6...前驱体的问题是成膜的速度比较慢。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "mo_precursor_to_mo_film",
            "from_node": "molybdenum_precursor",
            "to_node": "molybdenum_film",
            "edge_type": "material_flow",
            "description": "钼前驱体通过 ALD/CVD 沉积为钼薄膜。",
            "evidence": [{
                "source_title": "Lam Research ALTUS Product Family",
                "source_url": "https://www.lamresearch.com/zh-hans/product/altus-product-family/",
                "quote": "可使用ALD沉积钼(Mo)，以便更好地填充器件特征。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "tungsten_film_to_chip",
            "from_node": "tungsten_film",
            "to_node": "chip",
            "edge_type": "material_flow",
            "description": "钨薄膜作为芯片内部导电材料，用于接触孔、通孔和互连线。",
            "evidence": [{
                "source_title": "湖北日报：日本部分六氟化钨厂商拟断供，对半导体产业有何影响？",
                "source_url": "https://news.hubeidaily.net/mobile/c_5347295.html",
                "quote": "这些薄膜被用于构建芯片内部的互连线、接触孔、通孔等导电结构。"
            }],
            "confidence": "HIGH",
            "status": "ACTIVE",
        },
        {
            "edge_namespace": "industrial_flow",
            "edge_id": "molybdenum_film_to_chip",
            "from_node": "molybdenum_film",
            "to_node": "chip",
            "edge_type": "material_flow",
            "description": "钼薄膜可作为芯片金属化填充材料，替代部分钨薄膜应用。",
            "evidence": [{
                "source_title": "Lam Research ALTUS Product Family",
                "source_url": "https://www.lamresearch.com/zh-hans/product/altus-product-family/",
                "quote": "可使用ALD沉积钼(Mo)，以便更好地填充器件特征。"
            }],
            "confidence": "MEDIUM",
            "status": "PENDING",
        },
    ],
    "rejected_or_pending": [],
}


async def main():
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post("http://localhost:16060/api/v1/batches", json=BATCH)
        print(r.status_code)
        print(r.json())


asyncio.run(main())
