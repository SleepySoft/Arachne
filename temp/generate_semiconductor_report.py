# -*- coding: utf-8 -*-
import asyncio
import os
from collections import defaultdict
from datetime import datetime, timezone

import asyncpg
from neo4j import AsyncGraphDatabase

PG_URL = "postgresql://postgres:postgres@localhost:5433/arachne"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")

# Only include companies imported in the semiconductor business batches
# (covers the two batches on 2026-06-18 plus subsequent WF6-related updates)
BATCH_AFTER = datetime(2026, 6, 16, 0, 0, 0, tzinfo=timezone.utc)


SEGMENTS = [
    {
        "title": "上游材料",
        "description": "半导体制造所需的基础原材料、晶圆材料、特种气体与湿化学品。",
        "node_ids": [
            "silicon",
            "silicon_wafer",
            "photoresist",
            "euv_photoresist",
            "duv_photoresist",
            "cmp_slurry",
            "sputtering_target",
            "electronic_special_gases",
            "wet_chemicals",
            "tungsten_hexafluoride",
            "tungsten_pentachloride",
            "tungsten_hexachloride",
            "tungsten_hexacarbonyl",
            "molybdenum_precursor",
            "tungsten_film",
            "molybdenum_film",
        ],
    },
    {
        "title": "上游设备",
        "description": "晶圆制造、检测、涂胶显影、薄膜沉积、刻蚀、清洗、量测等设备。",
        "node_ids": [
            "lithography_machine",
            "etching_machine",
            "cvd_equipment",
            "pvd_equipment",
            "ald_equipment",
            "cleaning_equipment",
            "cmp_equipment",
            "track_coater_developer",
            "metrology_equipment",
            "semiconductor_manufacturing_equipment",
        ],
    },
    {
        "title": "EDA/IP 与技术服务",
        "description": "为芯片设计提供电子设计自动化工具与 IP 核。",
        "node_ids": [
            "eda_software",
            "ip_core",
        ],
    },
    {
        "title": "芯片设计（Fabless/IDM 设计）",
        "description": "处理器、存储、模拟、射频、功率、SoC、FPGA 等芯片设计公司。",
        "node_ids": [
            "cpu",
            "gpu",
            "ai_accelerator",
            "soc",
            "memory_chip",
            "nand_flash_chip",
            "mcu",
            "power_semiconductor",
            "cis",
            "rf_chip",
            "pmic",
            "fpga",
            "analog_chip",
        ],
    },
    {
        "title": "晶圆制造",
        "description": "拥有晶圆代工或 IDM 制造能力的企业，涵盖先进与成熟制程。",
        "node_ids": [
            "foundry",
            "idm",
            "advanced_process_node",
            "mature_process_node",
        ],
    },
    {
        "title": "封装测试（OSAT）",
        "description": "为芯片提供封装、测试等后段服务。",
        "node_ids": [
            "osat",
        ],
    },
]


async def fetch_companies():
    conn = await asyncpg.connect(PG_URL)
    rows = await conn.fetch(
        """
        SELECT
            c.company_id,
            c.name_zh,
            c.name_en,
            c.country,
            c.stock_codes,
            c.description,
            c.company_type,
            e.node_id,
            e.activity_type,
            e.role,
            e.weight,
            e.confidence
        FROM companies c
        JOIN company_node_exposures e ON c.company_id = e.company_id
        WHERE e.created_at >= $1
        ORDER BY c.country, c.name_zh
        """,
        BATCH_AFTER,
    )
    await conn.close()
    return rows


async def fetch_nodes():
    driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    node_map = {}
    async with driver.session() as s:
        result = await s.run(
            """
            MATCH (n:IndustrialNode)
            RETURN n.node_id AS node_id, n.canonical_name_zh AS name_zh,
                   n.canonical_name_en AS name_en, n.node_type AS node_type
            """
        )
        async for rec in result:
            node_map[rec["node_id"]] = {
                "name_zh": rec["name_zh"] or rec["node_id"],
                "name_en": rec["name_en"] or "",
                "node_type": rec["node_type"] or "unknown",
            }
    await driver.close()
    return node_map


def build_report(rows, node_map):
    companies = {}
    for r in rows:
        cid = r["company_id"]
        if cid not in companies:
            companies[cid] = {
                "company_id": cid,
                "name_zh": r["name_zh"],
                "name_en": r["name_en"] or "",
                "country": r["country"],
                "stock_codes": r["stock_codes"] or [],
                "description": r["description"] or "",
                "company_type": r["company_type"],
                "exposures": [],
            }
        node = node_map.get(r["node_id"], {"name_zh": r["node_id"], "name_en": ""})
        companies[cid]["exposures"].append({
            "node_id": r["node_id"],
            "node_name": node["name_zh"],
            "activity_type": r["activity_type"],
            "role": r["role"] or "",
            "weight": float(r["weight"]),
            "confidence": r["confidence"],
        })

    total_exposures = len(rows)

    lines = []
    lines.append("# 半导体产业链公司分类研报")
    lines.append("")
    lines.append("> 生成时间：自动生成于 Arachne 产业本体图系统")
    lines.append(f"> 数据来源：已录入 **{len(companies)}** 家国内外半导体公司及其 **{total_exposures}** 条节点暴露关系")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append(
        "本报告基于 Arachne 产业本体图系统，将已录入的国内外半导体公司按照产业链上中下游进行分类整理。"
        "报告覆盖 **上游材料、上游设备、EDA/IP、芯片设计、晶圆制造、封装测试** 六大关键环节，"
        "旨在快速呈现各环节的代表性企业及其核心产业位置。"
    )
    lines.append("")

    # Overview table
    lines.append("## 一、产业链全景")
    lines.append("")
    lines.append("| 环节 | 覆盖公司数 | 代表性节点 |")
    lines.append("|---|---|---|")
    for seg in SEGMENTS:
        seg_node_ids = set(seg["node_ids"])
        seg_companies = {
            cid for cid, c in companies.items()
            if any(exp["node_id"] in seg_node_ids for exp in c["exposures"])
        }
        rep_nodes = ", ".join(node_map.get(n, {"name_zh": n})["name_zh"] for n in seg["node_ids"][:5])
        lines.append(f"| {seg['title']} | {len(seg_companies)} | {rep_nodes} |")
    lines.append("")

    # Per segment details
    for seg in SEGMENTS:
        seg_node_ids = set(seg["node_ids"])
        seg_companies = []
        for cid, c in companies.items():
            seg_exposures = [e for e in c["exposures"] if e["node_id"] in seg_node_ids]
            if seg_exposures:
                seg_companies.append((c, seg_exposures))
        if not seg_companies:
            continue
        lines.append(f"## {seg['title']}")
        lines.append("")
        lines.append(seg["description"])
        lines.append("")
        lines.append(f"本环节共覆盖 **{len(seg_companies)}** 家公司。")
        lines.append("")
        for c, seg_exposures in sorted(seg_companies, key=lambda x: (x[0]["country"], x[0]["name_zh"])):
            en_suffix = f" / {c['name_en']}" if c["name_en"] else ""
            stocks = ", ".join(c["stock_codes"]) if c["stock_codes"] else "-"
            lines.append(f"### {c['name_zh']}{en_suffix}")
            lines.append("")
            lines.append(f"- **国家/地区**：{c['country']}")
            lines.append(f"- **证券代码**：{stocks}")
            lines.append(f"- **公司类型**：{c['company_type']}")
            exp_str = "； ".join(
                f"{e['node_name']}（{e['activity_type']}{', ' + e['role'] if e['role'] else ''}）"
                for e in seg_exposures
            )
            lines.append(f"- **产业链位置**：{exp_str}")
            if c["description"]:
                lines.append(f"- **简介**：{c['description']}")
            lines.append("")

    # Cross-segment companies
    lines.append("## 附录：跨环节布局公司")
    lines.append("")
    lines.append("以下公司在多个产业链环节存在暴露关系，具有纵向整合或平台化特征。")
    lines.append("")
    cross = []
    for cid, c in companies.items():
        segments_hit = set()
        for seg in SEGMENTS:
            seg_node_ids = set(seg["node_ids"])
            if any(e["node_id"] in seg_node_ids for e in c["exposures"]):
                segments_hit.add(seg["title"])
        if len(segments_hit) > 1:
            cross.append((c, sorted(segments_hit)))
    for c, segments_hit in sorted(cross, key=lambda x: (x[0]["country"], x[0]["name_zh"])):
        en_suffix = f" / {c['name_en']}" if c["name_en"] else ""
        lines.append(f"- **{c['name_zh']}{en_suffix}**（{c['country']}）：{', '.join(segments_hit)}")
    lines.append("")

    # Summary stats
    lines.append("## 统计汇总")
    lines.append("")
    lines.append(f"- **公司总数**：{len(companies)}")
    lines.append(f"- **暴露关系总数**：{total_exposures}")
    by_country = defaultdict(int)
    for c in companies.values():
        by_country[c["country"]] += 1
    lines.append(f"- **按国家/地区分布**：" + "， ".join(f"{k}: {v}" for k, v in sorted(by_country.items(), key=lambda x: -x[1])))
    lines.append("")

    return "\n".join(lines)


async def main():
    rows = await fetch_companies()
    node_map = await fetch_nodes()
    report = build_report(rows, node_map)
    out_path = os.path.join(os.path.dirname(__file__), "..", "docs", "semiconductor_company_research_report.md")
    out_path = os.path.abspath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report written to {out_path}")
    print(f"Companies included: {len(set(r['company_id'] for r in rows))}")
    print(f"Exposures included: {len(rows)}")


if __name__ == "__main__":
    asyncio.run(main())
