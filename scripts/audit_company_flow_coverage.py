#!/usr/bin/env python3
r"""Audit FinanceDashboard stocks against Arachne company exposures and flow coverage.

The audit is read-only.  It checks four independent layers:
1. stock code -> company resolution;
2. company -> exposure coverage;
3. exposure -> registered legacy industrial node integrity;
4. exposure -> native arachne_flow resource/method coverage.

Example (from the Arachne repository root):
    backend\venv\Scripts\python.exe scripts\audit_company_flow_coverage.py ^
      --finance-data-dir C:\D\code\FinanceDashboard\data ^
      --json-out temp\company_flow_coverage.json ^
      --markdown-out temp\company_flow_coverage.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import httpx

DEFAULT_BASE = "http://localhost:16060/api/v1"


def fetch_all(client: httpx.Client, path: str, **params: Any) -> list[dict[str, Any]]:
    page = 1
    items: list[dict[str, Any]] = []
    while True:
        response = client.get(path, params={"page": page, "page_size": 1000, **params})
        response.raise_for_status()
        payload = response.json()
        batch = payload if isinstance(payload, list) else payload.get("items", [])
        items.extend(batch)
        total = len(batch) if isinstance(payload, list) else int(payload.get("total", len(items)))
        if not batch or len(items) >= total:
            return items
        page += 1


def load_stocks(data_dir: Path) -> list[dict[str, str]]:
    stocks: list[dict[str, str]] = []
    for directory in sorted(data_dir.iterdir()):
        meta_path = directory / "meta.json"
        if not directory.is_dir() or directory.name.startswith("_") or not meta_path.exists():
            continue
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
        stocks.append(
            {
                "code": str(payload.get("code") or directory.name).upper(),
                "name": str(payload.get("name") or "").strip(),
                "sector": str(payload.get("sector") or "").strip(),
            }
        )
    return stocks


def index_companies(companies: Iterable[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    by_code: dict[str, dict[str, Any]] = {}
    by_name: dict[str, list[dict[str, Any]]] = {}
    for company in companies:
        for code in company.get("stock_codes") or []:
            by_code[str(code).upper()] = company
        for name in [company.get("name_zh"), *(company.get("aliases") or [])]:
            normalized = str(name or "").strip()
            if normalized:
                matches = by_name.setdefault(normalized, [])
                if all(item.get("company_id") != company.get("company_id") for item in matches):
                    matches.append(company)
    return by_code, by_name


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Company exposure and arachne_flow coverage audit",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| FinanceDashboard instruments | {summary['instrument_count']} |",
        f"| Company instruments | {summary['company_instrument_count']} |",
        f"| Resolved companies | {summary['resolved_company_count']} |",
        f"| Companies without exposures | {summary['zero_exposure_company_count']} |",
        f"| Exposure records | {summary['exposure_record_count']} |",
        f"| Invalid exposure node references | {summary['invalid_exposure_node_count']} |",
        f"| Companies fully covered by arachne_flow | {summary['flow_full_company_count']} |",
        f"| Companies partly covered by arachne_flow | {summary['flow_partial_company_count']} |",
        f"| Companies with zero native arachne_flow coverage | {summary['flow_zero_company_count']} |",
        f"| Unique exposure nodes absent from arachne_flow | {summary['flow_missing_unique_node_count']} |",
        "",
    ]
    sections = [
        ("Unresolved company instruments", report["unresolved"]),
        ("Companies without exposures", report["zero_exposure"]),
        ("Invalid exposure node references", report["invalid_exposure_nodes"]),
        ("Partial arachne_flow coverage", report["flow_partial"]),
        ("Zero native arachne_flow coverage", report["flow_zero"]),
        ("Missing arachne_flow nodes", report["flow_missing_nodes"]),
        ("Excluded non-company instruments", report["excluded_non_company"]),
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", ""])
        if not rows:
            lines.extend(["None.", ""])
            continue
        for row in rows:
            detail = ", ".join(f"{key}={value}" for key, value in row.items())
            lines.append(f"- {detail}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finance-data-dir", type=Path, required=True)
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--fail-on-gaps", action="store_true")
    args = parser.parse_args()

    stocks = load_stocks(args.finance_data_dir)
    excluded = [stock for stock in stocks if stock["sector"].upper() in {"ETF", "FUND"}]
    company_stocks = [stock for stock in stocks if stock not in excluded]

    with httpx.Client(base_url=args.base, timeout=120) as client:
        companies = fetch_all(client, "/companies")
        by_code, by_name = index_companies(companies)
        legacy_nodes = {
            item["node_id"]: item for item in fetch_all(client, "/nodes", engine="legacy")
        }
        flow_payload = client.get("/flows/graph", params={"merge": "method"})
        flow_payload.raise_for_status()
        flow_nodes = flow_payload.json().get("nodes", [])
        flow_ids = {item["node_id"] for item in flow_nodes}
        flow_method_refs = {
            item.get("properties", {}).get("method_ref")
            for item in flow_nodes
            if isinstance(item.get("properties"), dict)
        }
        native_flow_ids = flow_ids | {item for item in flow_method_refs if item}

        unresolved: list[dict[str, Any]] = []
        zero_exposure: list[dict[str, Any]] = []
        invalid_nodes: list[dict[str, Any]] = []
        company_rows: list[dict[str, Any]] = []
        missing_node_companies: dict[str, set[str]] = {}
        exposure_count = 0

        for stock in company_stocks:
            company = by_code.get(stock["code"])
            resolution = "stock_code"
            if company is None:
                exact_names = by_name.get(stock["name"], [])
                if len(exact_names) == 1:
                    company = exact_names[0]
                    resolution = "exact_name"
            if company is None:
                unresolved.append(stock)
                continue

            exposures = fetch_all(client, f"/companies/{company['company_id']}/exposures")
            exposure_count += len(exposures)
            if not exposures:
                zero_exposure.append(
                    {"code": stock["code"], "name": stock["name"], "company_id": company["company_id"]}
                )
            native_count = 0
            for exposure in exposures:
                node_id = exposure["node_id"]
                if node_id not in legacy_nodes:
                    invalid_nodes.append(
                        {
                            "code": stock["code"],
                            "company_id": company["company_id"],
                            "node_id": node_id,
                        }
                    )
                if node_id in native_flow_ids:
                    native_count += 1
                else:
                    missing_node_companies.setdefault(node_id, set()).add(stock["name"])
            company_rows.append(
                {
                    "code": stock["code"],
                    "name": stock["name"],
                    "company_id": company["company_id"],
                    "resolution": resolution,
                    "exposure_count": len(exposures),
                    "native_flow_count": native_count,
                }
            )

    flow_partial = [
        row for row in company_rows if 0 < row["native_flow_count"] < row["exposure_count"]
    ]
    flow_zero = [row for row in company_rows if row["exposure_count"] and not row["native_flow_count"]]
    flow_full = [
        row for row in company_rows if row["exposure_count"] and row["native_flow_count"] == row["exposure_count"]
    ]
    missing_nodes = [
        {
            "node_id": node_id,
            "name": legacy_nodes.get(node_id, {}).get("canonical_name_zh", ""),
            "company_count": len(names),
            "companies": "、".join(sorted(names)),
        }
        for node_id, names in sorted(
            missing_node_companies.items(), key=lambda item: (-len(item[1]), item[0])
        )
    ]
    report = {
        "summary": {
            "instrument_count": len(stocks),
            "company_instrument_count": len(company_stocks),
            "resolved_company_count": len(company_rows),
            "zero_exposure_company_count": len(zero_exposure),
            "exposure_record_count": exposure_count,
            "invalid_exposure_node_count": len(invalid_nodes),
            "flow_full_company_count": len(flow_full),
            "flow_partial_company_count": len(flow_partial),
            "flow_zero_company_count": len(flow_zero),
            "flow_missing_unique_node_count": len(missing_nodes),
            "exposure_count_distribution": dict(
                sorted(Counter(row["exposure_count"] for row in company_rows).items())
            ),
        },
        "unresolved": unresolved,
        "zero_exposure": zero_exposure,
        "invalid_exposure_nodes": invalid_nodes,
        "flow_partial": flow_partial,
        "flow_zero": flow_zero,
        "flow_full": flow_full,
        "flow_missing_nodes": missing_nodes,
        "excluded_non_company": excluded,
        "companies": company_rows,
    }

    json_text = json.dumps(report, ensure_ascii=False, indent=2)
    markdown_text = render_markdown(report)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json_text + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(markdown_text + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))

    has_gaps = bool(unresolved or zero_exposure or invalid_nodes or flow_partial or flow_zero)
    return 1 if args.fail_on_gaps and has_gaps else 0


if __name__ == "__main__":
    sys.exit(main())
