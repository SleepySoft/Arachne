#!/usr/bin/env python3
"""
Arachne System Manager

跨平台进程管理器，用于启动、停止和监控 Arachne 系统的三个组件：
- Neo4j 图数据库
- FastAPI 后端
- Vite React 前端

Usage:
    python arachne_manager.py status
    python arachne_manager.py start [all|neo4j|backend|frontend]
    python arachne_manager.py stop [all|neo4j|backend|frontend]
    python arachne_manager.py stats
    python arachne_manager.py logs [neo4j|backend|frontend]
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

import httpx
import psutil

# ── Configuration ──────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.resolve()

NEO4J_DIR = PROJECT_ROOT / "neo4j-community-5.26.0"
NEO4J_HTTP_PORT = 7474
NEO4J_BOLT_PORT = 7687

BACKEND_DIR = PROJECT_ROOT / "backend"
BACKEND_PORT = 8000

FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_PORT = 3000

SEED_DATA_PATH = PROJECT_ROOT / "data" / "seed_industry_graph.json"

# ── Helpers ────────────────────────────────────────────────


def _is_windows() -> bool:
    return platform.system() == "Windows"


def _find_python() -> Path:
    """Locate the Python executable in backend venv."""
    if _is_windows():
        return BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    return BACKEND_DIR / "venv" / "bin" / "python"


def _port_in_use(port: int) -> bool:
    """Check if a local TCP port is listening."""
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            return True
    return False


def _find_process_by_port(port: int) -> Optional[psutil.Process]:
    """Return the process listening on the given port."""
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            try:
                return psutil.Process(conn.pid)
            except psutil.NoSuchProcess:
                pass
    return None


def _wait_for_port(port: int, timeout: float = 30.0, label: str = "") -> bool:
    """Poll until a port is open or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _port_in_use(port):
            return True
        time.sleep(0.3)
    return False


# ── Component base ─────────────────────────────────────────


@dataclass
class ComponentStatus:
    name: str
    running: bool
    pid: Optional[int] = None
    port: Optional[int] = None
    extra: Dict[str, str] = field(default_factory=dict)

    def display(self) -> str:
        state = "RUNNING" if self.running else "STOPPED"
        color = "\033[32m" if self.running else "\033[31m"
        reset = "\033[0m"
        parts = [f"  {color}{state:<8}{reset}  {self.name:<12}"]
        if self.pid:
            parts.append(f"PID={self.pid}")
        if self.port:
            parts.append(f"port={self.port}")
        for k, v in self.extra.items():
            parts.append(f"{k}={v}")
        return "  ".join(parts)


class Component:
    name: str
    port: int

    def status(self) -> ComponentStatus:
        proc = _find_process_by_port(self.port)
        return ComponentStatus(
            name=self.name,
            running=proc is not None,
            pid=proc.pid if proc else None,
            port=self.port,
        )

    def start(self) -> bool:
        raise NotImplementedError

    def stop(self) -> bool:
        proc = _find_process_by_port(self.port)
        if proc is None:
            return True
        try:
            proc.terminate()
            gone, alive = psutil.wait_procs([proc], timeout=5)
            for p in alive:
                p.kill()
            return True
        except Exception as e:
            print(f"  Error stopping {self.name}: {e}")
            return False


# ── Neo4j ──────────────────────────────────────────────────


class Neo4jComponent(Component):
    name = "neo4j"
    port = NEO4J_BOLT_PORT

    def start(self) -> bool:
        if _port_in_use(NEO4J_BOLT_PORT):
            print(f"  Neo4j already running on port {NEO4J_BOLT_PORT}")
            return True

        if not NEO4J_DIR.exists():
            print(f"  ERROR: Neo4j not found at {NEO4J_DIR}")
            return False

        cmd: List[str]
        if _is_windows():
            cmd = [str(NEO4J_DIR / "bin" / "neo4j.bat"), "console"]
        else:
            cmd = [str(NEO4J_DIR / "bin" / "neo4j"), "console"]

        creationflags = 0
        preexec_fn: Optional[Callable] = None
        if _is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        subprocess.Popen(
            cmd,
            cwd=str(NEO4J_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
        )

        if _wait_for_port(NEO4J_BOLT_PORT, timeout=30, label="Neo4j"):
            print(f"  Neo4j started on port {NEO4J_BOLT_PORT}")
            return True
        print("  ERROR: Neo4j failed to start within 30s")
        return False

    def status(self) -> ComponentStatus:
        s = super().status()
        s.extra["browser"] = f"http://localhost:{NEO4J_HTTP_PORT}"
        return s


# ── Backend ────────────────────────────────────────────────


class BackendComponent(Component):
    name = "backend"
    port = BACKEND_PORT

    def start(self) -> bool:
        if _port_in_use(BACKEND_PORT):
            print(f"  Backend already running on port {BACKEND_PORT}")
            return True

        python = _find_python()
        if not python.exists():
            print(f"  ERROR: Python venv not found at {python}")
            return False

        cmd = [
            str(python),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(BACKEND_PORT),
        ]

        creationflags = 0
        preexec_fn: Optional[Callable] = None
        if _is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        subprocess.Popen(
            cmd,
            cwd=str(BACKEND_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
        )

        if _wait_for_port(BACKEND_PORT, timeout=30, label="Backend"):
            print(f"  Backend started on port {BACKEND_PORT}")
            self._maybe_seed()
            return True
        print("  ERROR: Backend failed to start within 30s")
        return False

    def _maybe_seed(self) -> None:
        """Seed data if the graph is empty."""
        try:
            resp = httpx.get(f"http://localhost:{BACKEND_PORT}/api/v1/query/stats", timeout=5)
            data = resp.json()
            if data.get("total_nodes", 0) == 0 and SEED_DATA_PATH.exists():
                print("  Graph is empty, seeding data...")
                payload = json.loads(SEED_DATA_PATH.read_text(encoding="utf-8"))
                r = httpx.post(
                    f"http://localhost:{BACKEND_PORT}/api/v1/batches",
                    json=payload,
                    timeout=30,
                )
                result = r.json()
                print(
                    f"  Seeded: {result.get('nodes_created', 0)} nodes, "
                    f"{result.get('edges_created', 0)} edges"
                )
        except Exception as e:
            print(f"  Warning: could not seed data: {e}")

    def status(self) -> ComponentStatus:
        s = super().status()
        s.extra["docs"] = f"http://localhost:{BACKEND_PORT}/docs"
        # Try to fetch live stats
        try:
            resp = httpx.get(f"http://localhost:{BACKEND_PORT}/api/v1/query/stats", timeout=3)
            data = resp.json()
            s.extra["nodes"] = str(data.get("total_nodes", "?"))
            s.extra["edges"] = str(data.get("total_edges", "?"))
        except Exception:
            pass
        return s


# ── Frontend ───────────────────────────────────────────────


class FrontendComponent(Component):
    name = "frontend"
    port = FRONTEND_PORT

    def _find_npx(self) -> str:
        """Locate npx executable (cross-platform)."""
        if _is_windows():
            candidates = ["npx.cmd", "npx.exe", "npx"]
            extra_paths = [r"C:\Program Files\nodejs", r"C:\Program Files (x86)\nodejs"]
        else:
            candidates = ["npx"]
            extra_paths = []

        search_paths = list(dict.fromkeys(
            os.environ.get("PATH", "").split(os.pathsep) + extra_paths
        ))

        for c in candidates:
            for path_dir in search_paths:
                full = Path(path_dir) / c
                if full.exists():
                    return str(full)
            # Absolute candidate
            if Path(c).exists():
                return str(Path(c).resolve())
        return "npx"  # fallback

    def start(self) -> bool:
        if _port_in_use(FRONTEND_PORT):
            print(f"  Frontend already running on port {FRONTEND_PORT}")
            return True

        npx = self._find_npx()
        cmd = [npx, "vite", "--host"]

        creationflags = 0
        preexec_fn: Optional[Callable] = None
        if _is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        subprocess.Popen(
            cmd,
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
        )

        if _wait_for_port(FRONTEND_PORT, timeout=30, label="Frontend"):
            print(f"  Frontend started on port {FRONTEND_PORT}")
            return True
        print("  ERROR: Frontend failed to start within 30s")
        return False

    def status(self) -> ComponentStatus:
        s = super().status()
        s.extra["url"] = f"http://localhost:{FRONTEND_PORT}"
        return s


# ── Manager ────────────────────────────────────────────────


class SystemManager:
    components: Dict[str, Component] = {
        "neo4j": Neo4jComponent(),
        "backend": BackendComponent(),
        "frontend": FrontendComponent(),
    }

    def show_status(self) -> None:
        print("\n" + "─" * 60)
        print("Arachne System Status")
        print("─" * 60)
        for comp in self.components.values():
            print(comp.status().display())
        print("─" * 60 + "\n")

    def start(self, target: str) -> None:
        order = ["neo4j", "backend", "frontend"]
        targets = order if target == "all" else [target]

        for name in targets:
            if name not in self.components:
                print(f"Unknown component: {name}")
                continue
            print(f"Starting {name}...")
            self.components[name].start()

        self.show_status()

    def stop(self, target: str) -> None:
        order = ["frontend", "backend", "neo4j"]
        targets = order if target == "all" else [target]

        for name in targets:
            if name not in self.components:
                print(f"Unknown component: {name}")
                continue
            print(f"Stopping {name}...")
            ok = self.components[name].stop()
            if ok:
                print(f"  {name} stopped")

        self.show_status()

    def show_stats(self) -> None:
        backend = self.components["backend"]
        st = backend.status()
        if not st.running:
            print("Backend is not running. Start it first: python arachne_manager.py start backend")
            return

        try:
            resp = httpx.get(f"http://localhost:{BACKEND_PORT}/api/v1/query/stats", timeout=5)
            data = resp.json()
        except Exception as e:
            print(f"Could not fetch stats: {e}")
            return

        print("\n" + "─" * 60)
        print("Graph Statistics")
        print("─" * 60)
        print(f"  Total Nodes:  {data.get('total_nodes', 0)}")
        print(f"  Total Edges:  {data.get('total_edges', 0)}")

        print(f"\n  Node Types:")
        for t, c in (data.get("node_type_distribution") or {}).items():
            print(f"    {t:<20} {c}")

        print(f"\n  Edge Types:")
        for t, c in (data.get("edge_type_distribution") or {}).items():
            print(f"    {t:<20} {c}")

        print(f"\n  Status:")
        for s, c in (data.get("status_distribution") or {}).items():
            print(f"    {s:<20} {c}")

        print(f"\n  Confidence:")
        for c, n in (data.get("confidence_distribution") or {}).items():
            print(f"    {c:<20} {n}")

        print("─" * 60 + "\n")

    def show_logs(self, target: str) -> None:
        log_paths: Dict[str, Optional[Path]] = {
            "neo4j": NEO4J_DIR / "logs" / "neo4j.log",
            "backend": None,  # stdout/stderr suppressed; no log file yet
            "frontend": None,
        }

        if target not in log_paths:
            print(f"Unknown component: {target}")
            return

        path = log_paths[target]
        if path and path.exists():
            print(f"\n--- {target} logs ({path}) ---\n")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                print("".join(lines[-50:]))
        else:
            print(f"No log file available for {target} (runs with suppressed output).")


# ── CLI ────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Arachne System Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python arachne_manager.py status
  python arachne_manager.py start
  python arachne_manager.py start neo4j
  python arachne_manager.py stop
  python arachne_manager.py stats
  python arachne_manager.py logs neo4j
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # status
    sub.add_parser("status", help="Show status of all components")

    # start
    p_start = sub.add_parser("start", help="Start one or all components")
    p_start.add_argument("target", nargs="?", default="all", choices=["all", "neo4j", "backend", "frontend"])

    # stop
    p_stop = sub.add_parser("stop", help="Stop one or all components")
    p_stop.add_argument("target", nargs="?", default="all", choices=["all", "neo4j", "backend", "frontend"])

    # stats
    sub.add_parser("stats", help="Show graph statistics from backend")

    # logs
    p_logs = sub.add_parser("logs", help="Show recent logs for a component")
    p_logs.add_argument("target", choices=["neo4j", "backend", "frontend"])

    args = parser.parse_args()
    mgr = SystemManager()

    if args.command == "status":
        mgr.show_status()
    elif args.command == "start":
        mgr.start(args.target)
    elif args.command == "stop":
        mgr.stop(args.target)
    elif args.command == "stats":
        mgr.show_stats()
    elif args.command == "logs":
        mgr.show_logs(args.target)


if __name__ == "__main__":
    main()
