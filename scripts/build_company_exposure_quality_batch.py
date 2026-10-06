#!/usr/bin/env python3
"""Build a reviewable BusinessRegistrationBatch for exposure quality gaps.

The input is the JSON report emitted by ``audit_company_flow_coverage.py``.
Existing exposure records are read through the API, preserving business fields
while filling the review date and activating evidence-backed records.  A small
override table replaces legacy placeholder evidence with named source excerpts.
The script only writes JSON; submission remains an explicit API step.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

import httpx


DEFAULT_BASE = "http://localhost:16060/api/v1"
DELETE_UNSUPPORTED = {
    "fenghua_manufacture_battery_cell",
    "cxmt_procure_hydrofluoric_acid",
}

EVIDENCE_OVERRIDES: dict[str, tuple[str, str]] = {
    "pingan_uses_deposit": (
        "平安银行2025年年度报告（提炼数据）",
        "2025年，吸收存款平均付息率1.65%，同比2024年下降42个基点",
    ),
    "pingan_provides_loan": (
        "平安银行2025年年度报告（提炼数据）",
        "个人贷款 1,727,294 50.9%；企业贷款 1,663,546 49.1%",
    ),
    "pingan_provides_interbank": (
        "Tushare公司资料：000001.SZ 平安银行",
        "经营范围包括从事同业拆借。",
    ),
    "pingan_provides_bond_inv": (
        "Tushare公司资料：000001.SZ 平安银行",
        "经营范围包括买卖政府债券、金融债券。",
    ),
    "xueda_education_provide_education_service": (
        "学大教育2025年年度报告（提炼数据）",
        "教育培训服务费收入 3,119,716,159.11，占营业收入96.67%。",
    ),
    "yuedianli_produce_electricity": (
        "粤电力A 2025年年度报告（提炼数据）",
        "售电收入 50,555,016,115，占营业收入98.09%。",
    ),
    "yuedianli_operate_coal_power": (
        "粤电力A 2025年年度报告（提炼数据）",
        "公司电力业务包含火力发电；煤炭为火力发电燃料。",
    ),
    "yuedianli_operate_gas_power": (
        "粤电力A 2025年年度报告（提炼数据）",
        "燃料成本在营业成本中占较大比重，煤炭、天然气价格波动对公司经营业绩影响较大。",
    ),
    "fenghua_manufacture_chip_resistor": (
        "风华高科2025年年度报告（提炼数据）",
        "主营产品包括片式电阻器。",
    ),
    "fenghua_manufacture_ceramic_cap": (
        "风华高科2025年年度报告（提炼数据）",
        "片式多层陶瓷电容器（MLCC）等电子元器件及电子材料占营业收入98.19%。",
    ),
    "gree_manufacture_air_conditioner": (
        "格力电器2025年年度报告（提炼数据）",
        "公司坚守家用空调核心优势，多措并举稳定市场份额。",
    ),
    "gree_manufacture_small_home": (
        "格力电器2025年年度报告（提炼数据）",
        "消费领域覆盖家用空调、暖通设备、冰箱、洗衣机、热水器、厨房电器、环境电器等产品。",
    ),
    "gree_manufacture_refrigerator": (
        "格力电器2025年年度报告（提炼数据）",
        "消费领域覆盖家用空调、暖通设备、冰箱、洗衣机、热水器、厨房电器、环境电器等产品。",
    ),
    "gree_manufacture_kitchen": (
        "格力电器2025年年度报告（提炼数据）",
        "消费领域覆盖家用空调、暖通设备、冰箱、洗衣机、热水器、厨房电器、环境电器等产品。",
    ),
    "st_rongkong_operate_real_estate": (
        "ST荣控2025年年度报告（提炼数据）",
        "房地产销售收入 322,287,922.85，占营业收入79.34%。",
    ),
}


def fetch_exposures(client: httpx.Client, company_id: str) -> list[dict[str, Any]]:
    response = client.get(
        f"/companies/{company_id}/exposures", params={"page": 1, "page_size": 1000}
    )
    response.raise_for_status()
    return response.json().get("items", [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--as-of-date", default=date.today().isoformat())
    args = parser.parse_args()

    audit = json.loads(args.audit_json.read_text(encoding="utf-8"))
    gaps = audit.get("exposure_quality_gaps", [])
    company_ids = sorted({item["company_id"] for item in gaps})
    exposure_by_id: dict[str, dict[str, Any]] = {}
    with httpx.Client(base_url=args.base, timeout=120) as client:
        for company_id in company_ids:
            for exposure in fetch_exposures(client, company_id):
                exposure_by_id[exposure["exposure_id"]] = exposure

    records: list[dict[str, Any]] = []
    for gap in gaps:
        exposure_id = gap["exposure_id"]
        if exposure_id in DELETE_UNSUPPORTED:
            continue
        exposure = dict(exposure_by_id[exposure_id])
        exposure.pop("created_at", None)
        exposure.pop("updated_at", None)
        exposure["as_of_date"] = args.as_of_date
        exposure["status"] = "ACTIVE"
        override = EVIDENCE_OVERRIDES.get(exposure_id)
        if override:
            exposure["evidence"] = [{"source_title": override[0], "quote": override[1]}]
        records.append(exposure)

    batch = {
        "batch_id": f"finance_exposure_quality_{args.as_of_date.replace('-', '')}",
        "task_description": "复核 FinanceDashboard 公司产业暴露的证据、状态与观察日期；移除无公司证据支持的推断性暴露",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": [],
        "company_node_exposures_to_upsert": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "upserts": len(records),
                "delete_unsupported": sorted(DELETE_UNSUPPORTED),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
