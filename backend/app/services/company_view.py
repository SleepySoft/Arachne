"""
================================================================================
 DOMAIN: COMPANY VIEW (公司视图)
================================================================================
全局公司关系网络的计算与协调服务。

核心职责：
  1. 从 PostgreSQL 读取公司暴露节点
  2. 通过产业图（Neo4j INDUSTRIAL_FLOW）推导公司间上下游关系
  3. 将结果写入 Neo4j 全局公司视图（Company 节点 + INFERRED_UPSTREAM 关系）
  4. 维护版本历史（company_view_versions）

本域与产业图域、公司 CRUD 域隔离。
================================================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool
from app.services import company_view_neo4j as neo4j_view
from app.services.computation_jobs import (
    mark_job_running,
    update_job_progress,
    complete_job,
    fail_job,
)


# ---------------------------------------------------------------------------
# Global Company View Computation
# ---------------------------------------------------------------------------

async def compute_company_view(job_id: str) -> dict:
    """
    Compute the global company relationship network.

    Workflow:
      1. Sync all ACTIVE companies as :Company nodes in Neo4j
      2. Clear old INFERRED_UPSTREAM relationships
      3. For every pair of companies, query industrial flow paths
      4. Batch-write INFERRED_UPSTREAM relationships

    Designed to run inside FastAPI BackgroundTasks.
    """
    try:
        await mark_job_running(job_id)

        pool = await get_postgres_pool()
        if pool is None:
            raise RuntimeError("PostgreSQL not available")

        # 1. Fetch all ACTIVE companies and their exposures
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT company_id, node_id
                FROM company_node_exposures
                WHERE status IN ('ACTIVE', 'PENDING')
                ORDER BY company_id
                """
            )

        company_nodes: Dict[str, List[str]] = {}
        for r in rows:
            cid = r["company_id"]
            if cid not in company_nodes:
                company_nodes[cid] = []
            company_nodes[cid].append(r["node_id"])

        companies = list(company_nodes.keys())
        total_pairs = len(companies) * (len(companies) - 1) // 2

        # Update job total
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE computation_jobs SET total_items = $2 WHERE job_id = $1",
                job_id, total_pairs,
            )

        # 2. Sync Company nodes to Neo4j
        synced_count = await neo4j_view.sync_companies_to_neo4j()

        # 3. Clear old inferred relations
        cleared_count = await neo4j_view.clear_inferred_relations()

        # 4. Compute pairwise industrial flows
        driver = get_async_driver()
        relations_to_create: List[Tuple[str, str, int]] = []
        processed = 0

        for i, company_a in enumerate(companies):
            for company_b in companies[i + 1 :]:
                node_ids_a = company_nodes[company_a]
                node_ids_b = company_nodes[company_b]

                # Single query for both directions
                async with driver.session() as session:
                    result = await session.run(
                        """
                        MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
                        WHERE (a.node_id IN $a_nodes AND b.node_id IN $b_nodes)
                           OR (a.node_id IN $b_nodes AND b.node_id IN $a_nodes)
                        RETURN
                          count(CASE WHEN a.node_id IN $a_nodes AND b.node_id IN $b_nodes THEN 1 END) AS ab_count,
                          count(CASE WHEN a.node_id IN $b_nodes AND b.node_id IN $a_nodes THEN 1 END) AS ba_count
                        """,
                        a_nodes=node_ids_a,
                        b_nodes=node_ids_b,
                    )
                    record = await result.single()
                    ab_count = record["ab_count"] if record else 0
                    ba_count = record["ba_count"] if record else 0

                if ab_count > 0:
                    relations_to_create.append((company_a, company_b, ab_count))
                if ba_count > 0:
                    relations_to_create.append((company_b, company_a, ba_count))

                processed += 1
                if processed % 10 == 0:
                    await update_job_progress(job_id, processed)

        # 5. Batch-write to Neo4j
        created_count = await neo4j_view.batch_create_inferred_relations(relations_to_create)

        await complete_job(job_id, {
            "total_companies": len(companies),
            "total_pairs": total_pairs,
            "processed_pairs": processed,
            "synced_companies": synced_count,
            "cleared_relations": cleared_count,
            "created_relations": created_count,
        })

        # 6. Record version snapshot
        await _record_version(
            job_id=job_id,
            status="completed",
            total_companies=len(companies),
            total_relations=created_count,
            total_pairs=total_pairs,
            processed_pairs=processed,
            synced_companies=synced_count,
            cleared_relations=cleared_count,
            created_relations=created_count,
        )

        return {
            "total_companies": len(companies),
            "created_relations": created_count,
        }

    except Exception as exc:
        await fail_job(job_id, str(exc))
        await _record_version(
            job_id=job_id,
            status="failed",
            error_message=str(exc),
        )
        raise


# ---------------------------------------------------------------------------
# Version Management
# ---------------------------------------------------------------------------

async def _record_version(
    job_id: str,
    status: str,
    total_companies: Optional[int] = None,
    total_relations: Optional[int] = None,
    total_pairs: Optional[int] = None,
    processed_pairs: Optional[int] = None,
    synced_companies: Optional[int] = None,
    cleared_relations: Optional[int] = None,
    created_relations: Optional[int] = None,
    error_message: Optional[str] = None,
) -> None:
    """Insert a version record into company_view_versions."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    completed_at = None
    if status == "completed":
        from datetime import datetime, timezone
        completed_at = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO company_view_versions (
                job_id, status, total_companies, total_relations,
                total_pairs, processed_pairs, synced_companies,
                cleared_relations, created_relations, error_message,
                completed_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
            job_id, status, total_companies, total_relations,
            total_pairs, processed_pairs, synced_companies,
            cleared_relations, created_relations, error_message,
            completed_at,
        )


async def list_company_view_versions(
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """Return paginated list of company view versions."""
    pool = await get_postgres_pool()
    if pool is None:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}

    offset = (page - 1) * page_size

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            "SELECT COUNT(*) FROM company_view_versions"
        )
        total = total_row[0] if total_row else 0

        rows = await conn.fetch(
            """
            SELECT version_id, version_uuid, job_id, status,
                   total_companies, total_relations, total_pairs,
                   processed_pairs, synced_companies, cleared_relations,
                   created_relations, error_message,
                   created_at, completed_at
            FROM company_view_versions
            ORDER BY version_id DESC
            LIMIT $1 OFFSET $2
            """,
            page_size, offset,
        )

    items = [
        {
            "version_id": r["version_id"],
            "version_uuid": str(r["version_uuid"]),
            "job_id": r["job_id"],
            "status": r["status"],
            "total_companies": r["total_companies"],
            "total_relations": r["total_relations"],
            "total_pairs": r["total_pairs"],
            "processed_pairs": r["processed_pairs"],
            "synced_companies": r["synced_companies"],
            "cleared_relations": r["cleared_relations"],
            "created_relations": r["created_relations"],
            "error_message": r["error_message"],
            "created_at": r["created_at"].isoformat() if r["created_at"] else None,
            "completed_at": r["completed_at"].isoformat() if r["completed_at"] else None,
        }
        for r in rows
    ]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
