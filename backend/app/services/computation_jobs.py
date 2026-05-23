"""
Computation job status tracking service.
Minimal CRUD for async job lifecycle management.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from app.database_postgres import get_postgres_pool


async def create_job(job_type: str, target_id: Optional[str] = None, total_items: Optional[int] = None) -> dict:
    """Create a new computation job and return its record."""
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    job_id = f"{job_type}_{target_id or 'all'}_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO computation_jobs (job_id, job_type, target_id, status, total_items)
            VALUES ($1, $2, $3, 'pending', $4)
            """,
            job_id, job_type, target_id, total_items,
        )

    return await get_job(job_id)


async def get_job(job_id: str) -> Optional[dict]:
    """Fetch a computation job by ID."""
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT job_id, job_type, target_id, status, total_items, processed_items,
                   result_summary, error_message,
                   created_at, started_at, completed_at
            FROM computation_jobs
            WHERE job_id = $1
            """,
            job_id,
        )

    if row is None:
        return None

    return {
        "job_id": row["job_id"],
        "job_type": row["job_type"],
        "target_id": row["target_id"],
        "status": row["status"],
        "total_items": row["total_items"],
        "processed_items": row["processed_items"],
        "result_summary": json.loads(row["result_summary"]) if isinstance(row["result_summary"], str) else row["result_summary"],
        "error_message": row["error_message"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "started_at": row["started_at"].isoformat() if row["started_at"] else None,
        "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
    }


async def mark_job_running(job_id: str) -> None:
    """Update job status to running and set started_at."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE computation_jobs
            SET status = 'running', started_at = NOW()
            WHERE job_id = $1
            """,
            job_id,
        )


async def update_job_progress(job_id: str, processed_items: int) -> None:
    """Update processed_items counter."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE computation_jobs
            SET processed_items = $2
            WHERE job_id = $1
            """,
            job_id, processed_items,
        )


async def complete_job(job_id: str, result_summary: Optional[dict] = None) -> None:
    """Mark job as completed."""
    import json
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE computation_jobs
            SET status = 'completed', completed_at = NOW(), result_summary = $2
            WHERE job_id = $1
            """,
            job_id, json.dumps(result_summary) if result_summary else None,
        )


async def fail_job(job_id: str, error_message: str) -> None:
    """Mark job as failed."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE computation_jobs
            SET status = 'failed', completed_at = NOW(), error_message = $2
            WHERE job_id = $1
            """,
            job_id, error_message,
        )
