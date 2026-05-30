"""
================================================================================
 DOMAIN: COMPANY VIEW (公司视图)
================================================================================
全局公司关系网络 API 路由。

公司视图 = 独立于产业图的全局公司供应链网络，存储在 Neo4j 中。
================================================================================
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.services import company_view as view_service
from app.services import company_view_neo4j as neo4j_view
from app.services.computation_jobs import create_job, get_job

router = APIRouter()


# ---------------------------------------------------------------------------
# Version Management
# ---------------------------------------------------------------------------

@router.get("/versions", response_model=dict)
async def get_company_view_versions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List historical company view computation versions."""
    return await view_service.list_company_view_versions(page=page, page_size=page_size)


@router.delete("/versions/{version_id}", status_code=204)
async def delete_company_view_version(version_id: int):
    """Delete a company view version."""
    deleted = await view_service.delete_company_view_version(version_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Version not found")
    return None


@router.post("/versions", response_model=dict)
async def create_company_view_version(background_tasks: BackgroundTasks):
    """
    Trigger a new company view computation and record it as a new version.
    Returns immediately with a job_id for polling.
    """
    job = await create_job(
        job_type="company_view_compute",
        total_items=0,
    )

    background_tasks.add_task(
        view_service.compute_company_view,
        job["job_id"],
    )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "created_at": job["created_at"],
    }


# ---------------------------------------------------------------------------
# Legacy Global Computation (kept for backward compat)
# ---------------------------------------------------------------------------

@router.post("/compute", response_model=dict)
async def compute_company_view(background_tasks: BackgroundTasks):
    """
    Trigger async computation of the global company relationship network.
    Syncs companies to Neo4j, clears old relations, infers upstream/downstream
    from industrial flow, and writes INFERRED_UPSTREAM edges.
    Returns immediately with a job_id for polling.
    """
    job = await create_job(
        job_type="company_view_compute",
        total_items=0,
    )

    background_tasks.add_task(
        view_service.compute_company_view,
        job["job_id"],
    )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "created_at": job["created_at"],
    }


# ---------------------------------------------------------------------------
# Global Network
# ---------------------------------------------------------------------------

@router.get("/network", response_model=dict)
async def get_company_network():
    """
    Return the global company relationship network from Neo4j.
    Nodes = all Company nodes, Edges = all INFERRED_UPSTREAM relationships.
    """
    return await neo4j_view.get_company_network()


# ---------------------------------------------------------------------------
# Per-Company Upstream / Downstream
# ---------------------------------------------------------------------------

@router.get("/{company_id}/upstream", response_model=List[dict])
async def get_company_upstream(company_id: str):
    """Return direct upstream companies (suppliers) of the given company."""
    upstream = await neo4j_view.get_upstream_companies(company_id)
    return upstream


@router.get("/{company_id}/downstream", response_model=List[dict])
async def get_company_downstream(company_id: str):
    """Return direct downstream companies (customers) of the given company."""
    downstream = await neo4j_view.get_downstream_companies(company_id)
    return downstream


@router.get("/relations/{from_company_id}/{to_company_id}/paths", response_model=dict)
async def get_company_relation_paths(from_company_id: str, to_company_id: str):
    """
    Return the industrial graph paths that support an inferred relation
    between two companies.
    """
    return await view_service.get_relation_paths(from_company_id, to_company_id)
