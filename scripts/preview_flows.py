#!/usr/bin/env python3
"""批量校验 arachne-flow YAML 文件（调用后端 /flows/preview，不写库不编译）。

用法（在仓库根目录）：
    # 校验全部流程文件
    backend\\venv\\Scripts\\python.exe scripts/preview_flows.py

    # 只校验某个类别目录（data/flows/<category>/）
    backend\\venv\\Scripts\\python.exe scripts/preview_flows.py --category biopharma

退出码：有文件解析失败时为 1（适合作为保存后/CI 检查）。
依赖：后端 API 在线（默认 http://localhost:16060，可用 --base 覆盖）。
注意：新增 flow 文件后，后端需重启才能解析新的 include 依赖（include 图有进程内缓存）。
"""
import argparse
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
FLOW_DIR = ROOT / "data" / "flows"
DEFAULT_BASE = "http://localhost:16060/api/v1"


def main():
    ap = argparse.ArgumentParser(description="批量 preview 校验 flow YAML")
    ap.add_argument("--category", help="只校验 data/flows/<category>/ 下的文件")
    ap.add_argument("--base", default=DEFAULT_BASE, help="后端 API 基础地址")
    args = ap.parse_args()

    scan_dir = FLOW_DIR / args.category if args.category else FLOW_DIR
    files = sorted(f for f in scan_dir.rglob("*.yaml") if f.name != "manifest.yaml")
    if not files:
        print(f"未找到 flow 文件: {scan_dir}")
        sys.exit(1)

    failed = False
    for f in files:
        content = f.read_text(encoding="utf-8")
        r = httpx.post(f"{args.base}/flows/preview",
                       json={"flow_id": f.stem, "content": content}, timeout=60)
        rel = f.relative_to(FLOW_DIR)
        if r.status_code != 200:
            print(f"{rel}: HTTP {r.status_code} {r.text[:300]}")
            failed = True
            continue
        d = r.json()
        errs, warns = d.get("errors", []), d.get("warnings", [])
        print(f"{rel}: nodes={len(d.get('nodes', []))} edges={len(d.get('edges', []))} "
              f"errors={len(errs)} warnings={len(warns)}")
        for e in errs:
            print(f"  ERR: {e}")
            failed = True
        for w in warns[:6]:
            print(f"  WARN: {w}")

    sys.exit(1 if failed else 0)


main()
