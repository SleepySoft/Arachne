"""
Computation job status polling API.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.computation_jobs import get_job

router = APIRouter()


@router.get("/{job_id}", response_model=dict)
async def get_job_status(job_id: str):
    """Get the status of a computation job."""
    job = await get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
