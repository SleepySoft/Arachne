"""
================================================================================
 DOMAIN: COMPANY SUBGRAPH (公司子图)
================================================================================
公司子图版本管理与关系 API 路由。

本文件属于 Company Subgraph Domain，与核心产业图域隔离。
================================================================================
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.models.company_subgraph_schema import (
    CompanySubgraph,
    CompanySubgraphRelation,
    PaginatedCompanySubgraphs,
)
from app.services import company_subgraph as subgraph_service
from app.services.computation_jobs import create_job, get_job
from app.database_postgres import get_postgres_pool

router = APIRouter()


# ---------------------------------------------------------------------------
# Subgraph Version Management
# ---------------------------------------------------------------------------

@router.post("/{company_id}/subgraphs/compute", response_model=dict)
async def compute_subgraph(
    company_id: str,
    background_tasks: BackgroundTasks,
    version_name: Optional[str] = None,
    description: Optional[str] = None,
):
    """
    Trigger async computation of a new company subgraph version.
    Returns immediately with a job_id for polling.
    """
    job = await create_job(
        job_type="company_subgraph_compute",
        target_id=company_id,
        total_items=3,  # phases: nodes, edges, relations
    )

    background_tasks.add_task(
        subgraph_service.compute_company_subgraph,
        company_id,
        job["job_id"],
        version_name,
        description,
    )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "company_id": company_id,
        "created_at": job["created_at"],
    }


@router.get("/{company_id}/subgraphs", response_model=PaginatedCompanySubgraphs)
async def list_subgraphs(
    company_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all subgraph versions for a company (newest first)."""
    skip = (page - 1) * page_size
    items, total = await subgraph_service.list_subgraphs(company_id, skip, page_size)
    return PaginatedCompanySubgraphs(total=total, page=page, page_size=page_size, items=items)


@router.get("/{company_id}/subgraphs/{subgraph_id}", response_model=CompanySubgraph)
async def get_subgraph(company_id: str, subgraph_id: str):
    """Get a subgraph version with full details (nodes + edges + relations)."""
    subgraph = await subgraph_service.get_subgraph(subgraph_id, include_details=True)
    if subgraph is None or subgraph.company_id != company_id:
        raise HTTPException(status_code=404, detail="Subgraph not found")
    return subgraph


@router.delete("/{company_id}/subgraphs/{subgraph_id}", status_code=204)
async def delete_subgraph(company_id: str, subgraph_id: str):
    """Delete a subgraph version."""
    subgraph = await subgraph_service.get_subgraph(subgraph_id, include_details=False)
    if subgraph is None or subgraph.company_id != company_id:
        raise HTTPException(status_code=404, detail="Subgraph not found")

    success = await subgraph_service.delete_subgraph(subgraph_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete subgraph")

    return None


# ---------------------------------------------------------------------------
# Subgraph Relations
# ---------------------------------------------------------------------------

@router.post("/{company_id}/subgraphs/{subgraph_id}/relations", response_model=CompanySubgraphRelation)
async def add_relation(
    company_id: str,
    subgraph_id: str,
    data: CompanySubgraphRelation,
):
    """Add a relation to a subgraph (typically evidenced_business)."""
    subgraph = await subgraph_service.get_subgraph(subgraph_id, include_details=False)
    if subgraph is None or subgraph.company_id != company_id:
        raise HTTPException(status_code=404, detail="Subgraph not found")

    return await subgraph_service.add_subgraph_relation(subgraph_id, data)


@router.delete("/{company_id}/subgraphs/{subgraph_id}/relations/{relation_id}", status_code=204)
async def delete_relation(
    company_id: str,
    subgraph_id: str,
    relation_id: int,
):
    """Delete a relation from a subgraph."""
    subgraph = await subgraph_service.get_subgraph(subgraph_id, include_details=False)
    if subgraph is None or subgraph.company_id != company_id:
        raise HTTPException(status_code=404, detail="Subgraph not found")

    success = await subgraph_service.delete_subgraph_relation(subgraph_id, relation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Relation not found")

    return None


# ---------------------------------------------------------------------------
# Full-Graph Relation Inference
# ---------------------------------------------------------------------------

@router.post("/compute-relations", response_model=dict)
async def compute_all_relations(background_tasks: BackgroundTasks):
    """
    Trigger async computation of inferred_industrial relations across ALL companies.
    Results are written into each company's most recent ACTIVE subgraph.
    Returns immediately with a job_id for polling.
    """
    job = await create_job(
        job_type="company_relation_inference",
        total_items=0,  # Will be updated when computation starts
    )

    background_tasks.add_task(
        subgraph_service.compute_all_company_relations,
        job["job_id"],
    )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "created_at": job["created_at"],
    }


# ---------------------------------------------------------------------------
# Global Company Network
# ---------------------------------------------------------------------------

@router.get("/network", response_model=dict)
async def get_company_network():
    """
    Return the global company relationship network.
    Nodes = all active companies, Edges = relations from latest ACTIVE subgraphs.
    """
    pool = await get_postgres_pool()
    if pool is None:
        return {"nodes": [], "edges": []}

    async with pool.acquire() as conn:
        company_rows = await conn.fetch(
            """
            SELECT company_id, name_zh, company_type, status
            FROM companies
            WHERE status = 'ACTIVE'
            ORDER BY name_zh
            """
        )

        relation_rows = await conn.fetch(
            """
            WITH latest_subgraphs AS (
                SELECT DISTINCT ON (company_id) subgraph_id
                FROM company_subgraphs
                WHERE status = 'ACTIVE'
                ORDER BY company_id, created_at DESC
            )
            SELECT DISTINCT ON (csr.from_company_id, csr.to_company_id, csr.relation_type, csr.relation_subtype)
                csr.from_company_id,
                csr.to_company_id,
                csr.relation_type,
                csr.relation_subtype,
                csr.strength,
                csr.confidence
            FROM company_subgraph_relations csr
            WHERE csr.subgraph_id IN (SELECT subgraph_id FROM latest_subgraphs)
            ORDER BY csr.from_company_id, csr.to_company_id, csr.relation_type, csr.relation_subtype
            """
        )

    nodes = [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"],
            "company_type": r["company_type"],
            "status": r["status"],
        }
        for r in company_rows
    ]

    edges = [
        {
            "from_company_id": r["from_company_id"],
            "to_company_id": r["to_company_id"],
            "relation_type": r["relation_type"],
            "relation_subtype": r["relation_subtype"],
            "strength": float(r["strength"] or 1.0),
            "confidence": r["confidence"],
        }
        for r in relation_rows
    ]

    return {"nodes": nodes, "edges": edges}
