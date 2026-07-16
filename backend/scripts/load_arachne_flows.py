r"""Load arachne-flow YAML files into Neo4j and track their compile status in PostgreSQL.

Usage (from repo root):
    backend\venv\Scripts\python.exe backend/scripts/load_arachne_flows.py
"""
from __future__ import annotations

import asyncio
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database_flow import close_flow_async_driver, init_flow_db
from app.database_postgres import close_postgres_pool, get_postgres_pool, init_postgres_tables
from app.engines.arachne_flow.parser import FlowParseError, parse_flow_file
from app.engines.arachne_flow import storage


ROOT = Path(__file__).resolve().parents[2]
FLOW_DIR = ROOT / "data" / "flows" / "semiconductor"


async def _upsert_status(
    pool,
    flow_id: str,
    file_path: str,
    md5: str,
    status: str,
    error_message: str | None = None,
):
    await pool.execute(
        """
        INSERT INTO arachne_flow_files (flow_id, file_path, md5, status, error_message, compiled_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        ON CONFLICT (flow_id) DO UPDATE
        SET file_path = EXCLUDED.file_path,
            md5 = EXCLUDED.md5,
            status = EXCLUDED.status,
            error_message = EXCLUDED.error_message,
            compiled_at = EXCLUDED.compiled_at,
            updated_at = NOW()
        """,
        flow_id,
        file_path,
        md5,
        status,
        error_message,
    )


async def load_all():
    await init_flow_db()
    await init_postgres_tables()
    pool = await get_postgres_pool()

    if not FLOW_DIR.exists():
        print(f"[error] flow directory not found: {FLOW_DIR}")
        return

    files = sorted(p for p in FLOW_DIR.glob("*.yaml") if p.name != "manifest.yaml")
    print(f"[info] found {len(files)} flow files in {FLOW_DIR}\n")

    for path in files:
        content = path.read_bytes()
        md5 = hashlib.md5(content).hexdigest()
        try:
            parsed = parse_flow_file(path)
            counts = await storage.compile_parsed_flow(parsed, clear_existing=True)
            await _upsert_status(pool, parsed.flow_id, str(path.relative_to(ROOT)), md5, "COMPILED")
            print(
                f"[ok] {parsed.flow_id}: "
                f"resources={counts['resources']} actions={counts['actions']} "
                f"methods={counts['methods']} edges={counts['edges']}"
            )
        except FlowParseError as exc:
            await _upsert_status(pool, path.stem, str(path.relative_to(ROOT)), md5, "PARSE_ERROR", str(exc))
            print(f"[parse error] {path.name}: {exc}")
        except Exception as exc:
            await _upsert_status(pool, path.stem, str(path.relative_to(ROOT)), md5, "COMPILE_ERROR", str(exc))
            print(f"[compile error] {path.name}: {exc}")

    await close_flow_async_driver()
    await close_postgres_pool()


if __name__ == "__main__":
    asyncio.run(load_all())
