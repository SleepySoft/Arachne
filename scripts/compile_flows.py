#!/usr/bin/env python3
"""批量编译 arachne-flow 文件到 Neo4j flow 图（写库！调用 /flows/{id}/compile）。

⚠️ 本脚本会写入 Neo4j（ArachneFlow* 节点与边）。编译前请确保：
  1. 已用 scripts/preview_flows.py 校验通过；
  2. 新增/删除过 flow 文件后已重启后端（include 图有进程内缓存，
     可用 scripts\\restart-backend.ps1）。

用法（在仓库根目录）：
    # 编译某个类别目录下的全部文件
    backend\\venv\\Scripts\\python.exe scripts/compile_flows.py --category biopharma

    # 编译单个文件（flow_id 即文件 stem）
    backend\\venv\\Scripts\\python.exe scripts/compile_flows.py --flow-id vaccine

编译后建议运行 backend\\venv\\Scripts\\python.exe backend/scripts/flow_context.py --dangling
检查断链变化。
依赖：后端 API 在线（默认 http://localhost:16060，可用 --base 覆盖）。
"""
import argparse
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
FLOW_DIR = ROOT / "data" / "flows"
DEFAULT_BASE = "http://localhost:16060/api/v1"


def main():
    ap = argparse.ArgumentParser(description="批量编译 flow 文件到 Neo4j")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--category", help="编译 data/flows/<category>/ 下全部文件")
    group.add_argument("--flow-id", help="编译单个 flow（文件 stem）")
    ap.add_argument("--base", default=DEFAULT_BASE, help="后端 API 基础地址")
    args = ap.parse_args()

    if args.flow_id:
        flow_ids = [args.flow_id]
    else:
        files = sorted((FLOW_DIR / args.category).glob("*.yaml"))
        flow_ids = [f.stem for f in files if f.name != "manifest.yaml"]
        if not flow_ids:
            print(f"未找到 flow 文件: {FLOW_DIR / args.category}")
            sys.exit(1)

    failed = False
    for fid in flow_ids:
        r = httpx.post(f"{args.base}/flows/{fid}/compile", timeout=120)
        if r.status_code != 200:
            print(f"{fid}: HTTP {r.status_code} {r.text[:300]}")
            failed = True
            continue
        print(f"{fid}: {r.json()}")

    sys.exit(1 if failed else 0)


main()
