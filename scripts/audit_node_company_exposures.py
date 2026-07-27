#!/usr/bin/env python3
"""审计"产业节点 → 公司暴露"覆盖情况（只读，不写库）。

回答的问题：某组产业节点（默认：某行业的全部映射节点）分别有哪些公司暴露？
哪些节点还没有任何公司覆盖（补公司数据的切入点）？

用法（在仓库根目录）：
    # 审计某个行业的全部映射节点
    backend\\venv\\Scripts\\python.exe scripts/audit_node_company_exposures.py --industry biopharma

    # 审计指定节点
    backend\\venv\\Scripts\\python.exe scripts/audit_node_company_exposures.py --nodes vaccine blood_product monoclonal_antibody

依赖：后端 API 在线（默认 http://localhost:16060，可用 --base 覆盖）。
"""
import argparse
import sys

import httpx

DEFAULT_BASE = "http://localhost:16060/api/v1"


def resolve_nodes(base: str, industry: str | None, nodes: list[str]) -> list[str]:
    if nodes:
        return nodes
    r = httpx.get(f"{base}/industries/{industry}/nodes", params={"page_size": 1000}, timeout=60)
    r.raise_for_status()
    d = r.json()
    items = d.get("items") or d.get("nodes") or []
    ids = [(n.get("node_id") or n.get("id")) for n in items]
    return [i for i in ids if i]


def main():
    ap = argparse.ArgumentParser(description="审计产业节点的公司暴露覆盖")
    ap.add_argument("--industry", help="行业 id：审计其全部映射节点（与 --nodes 二选一）")
    ap.add_argument("--nodes", nargs="*", default=[], help="指定要审计的 node_id 列表")
    ap.add_argument("--base", default=DEFAULT_BASE, help="后端 API 基础地址")
    args = ap.parse_args()

    if not args.industry and not args.nodes:
        ap.error("必须指定 --industry 或 --nodes")

    nodes = resolve_nodes(args.base, args.industry, args.nodes)
    print(f"审计节点数: {len(nodes)}\n")

    all_companies = set()
    uncovered = []
    print(f"{'node':44s} #  公司")
    for n in nodes:
        r = httpx.get(f"{args.base}/companies/by-node/{n}", timeout=120)
        if r.status_code != 200:
            print(f"{n:44s} HTTP {r.status_code}")
            continue
        items = (r.json() or {}).get("companies") or []
        names = []
        for it in items:
            names.append(it.get("name_zh") or it.get("company_id") or "?")
            all_companies.add(it.get("company_id"))
        if not items:
            uncovered.append(n)
        print(f"{n:44s} {len(items):3d} {', '.join(names[:8])}")

    print(f"\n覆盖公司总数(并集): {len(all_companies)}")
    print(f"无公司暴露的节点 ({len(uncovered)}):")
    for n in uncovered:
        print(f"  {n}")
    sys.exit(0)


main()
