#!/usr/bin/env python3
"""arachne-flow 推理冒烟测试（只读推理，不写库）。

验证 flow 编译结果能否支撑两类推理任务，并演示**正确的请求格式**
（这是最容易踩坑的地方）：
  - 引擎字段：  "engine": "arachne_flow"
  - 种子字段：  "source_nodes": ["node_id", ...]   # 纯字符串数组，不是 source_object_ids
  - 方向枚举：  "traversal_direction": "both"      # 不是 bidirectional

用法（在仓库根目录）：
    # 默认跑一组生物医药样例
    backend\\venv\\Scripts\\python.exe scripts/smoke_flow_reasoning.py

    # 指定产业节点做关联推理（association）
    backend\\venv\\Scripts\\python.exe scripts/smoke_flow_reasoning.py --seed monoclonal_antibody --seed vaccine

    # 指定公司做公司产业上下文推理（cross_graph_context）
    backend\\venv\\Scripts\\python.exe scripts/smoke_flow_reasoning.py --company wuxi_biologics --company tiantan_bio

依赖：后端 API 在线（默认 http://localhost:16060，可用 --base 覆盖）；
flow 图已编译（scripts/compile_flows.py）。
"""
import argparse
import sys

import httpx

DEFAULT_BASE = "http://localhost:16060/api/v1"

DEFAULT_SEEDS = ["monoclonal_antibody", "vaccine", "chemical_drug", "viral_vector"]
DEFAULT_COMPANIES = ["wuxi_biologics", "tiantan_bio"]


def run(base: str, task_type: str, seeds: list[str]) -> dict:
    r = httpx.post(
        f"{base}/reasoning/execute",
        json={
            "task_id": f"smoke_{task_type}",
            "engine": "arachne_flow",
            "task_type": task_type,
            "source_nodes": seeds,
            "requested_outputs": ["temporary_graph", "paths", "node_scores"],
            "constraints": {"max_depth": 2, "traversal_direction": "both"},
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser(description="arachne-flow 推理冒烟测试")
    ap.add_argument("--seed", action="append", default=[],
                    help="产业节点 id（可多次），走 association 任务")
    ap.add_argument("--company", action="append", default=[],
                    help="公司 id（可多次），走 cross_graph_context 任务")
    ap.add_argument("--base", default=DEFAULT_BASE, help="后端 API 基础地址")
    args = ap.parse_args()

    seeds = args.seed or DEFAULT_SEEDS
    companies = args.company or DEFAULT_COMPANIES

    failed = False
    for nid in seeds:
        d = run(args.base, "association", [nid])
        rp = d.get("result_payload") or {}
        tg = rp.get("temporary_graph") or {}
        status = d.get("status")
        print(f"association [{nid}] -> {status} | graph {len(tg.get('nodes', []))}n/"
              f"{len(tg.get('edges', []))}e | paths {len(rp.get('paths') or [])} "
              f"| scores {len(rp.get('node_scores') or [])}")
        if status != "success":
            failed = True

    for cid in companies:
        d = run(args.base, "cross_graph_context", [cid])
        rp = d.get("result_payload") or {}
        cc = rp.get("company_context") or {}
        cats = cc.get("categories") or {}
        status = d.get("status")
        print(f"cross_graph_context [{cid}] -> {status} | seeds={rp.get('seed_nodes') or cats.get('seed_nodes')} "
              f"| peers={len(cc.get('peers', []))} up={len(cc.get('upstream_companies', []))} "
              f"down={len(cc.get('downstream_companies', []))} related={len(cc.get('related_companies', []))}")
        if status != "success":
            failed = True

    sys.exit(1 if failed else 0)


main()
