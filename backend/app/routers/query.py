from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import GraphStats, SubgraphResult
from app.services import graph_service

router = APIRouter()


@router.get("/subgraph/{node_id}", response_model=SubgraphResult)
async def get_subgraph(
    node_id: str,
    depth: int = Query(2, ge=1, le=5),
):
    nodes, edges = await graph_service.get_subgraph(node_id, depth)
    return SubgraphResult(
        center_node_id=node_id,
        depth=depth,
        nodes=nodes,
        edges=edges,
    )


@router.get("/neighbors/{node_id}")
async def get_neighbors(node_id: str):
    nodes, edges = await graph_service.get_neighbors(node_id)
    return {"nodes": nodes, "edges": edges}


@router.get("/path")
async def get_path(
    from_node: str = Query(...),
    to_node: str = Query(...),
    max_depth: int = Query(5, ge=1, le=10),
):
    paths = await graph_service.get_paths(from_node, to_node, max_depth)
    return {"from_node": from_node, "to_node": to_node, "paths": paths}


@router.get("/stats", response_model=GraphStats)
async def get_stats():
    return await graph_service.get_stats()


@router.get("/incomplete-items")
async def get_incomplete_items(
    limit: int = Query(100, ge=1, le=1000),
):
    """Return a summary and lists of nodes/edges that need curation."""
    return await graph_service.get_incomplete_items(limit)


@router.get("/health")
async def health_check():
    """Check connectivity to Neo4j and PostgreSQL."""
    from app.services import neo4j_storage
    from app.database_postgres import get_postgres_pool

    result = {
        "status": "ok",
        "neo4j": "ok",
        "postgres": "unknown",
    }

    # Neo4j check
    try:
        driver = neo4j_storage.get_async_driver()
        async with driver.session() as session:
            await session.run("RETURN 1 AS one")
    except Exception as e:
        result["neo4j"] = f"error: {str(e)}"
        result["status"] = "degraded"

    # PostgreSQL check
    try:
        pool = await get_postgres_pool()
        if pool is None:
            result["postgres"] = "not_configured"
        else:
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            result["postgres"] = "ok"
    except Exception as e:
        result["postgres"] = f"error: {str(e)}"
        result["status"] = "degraded"

    return result


@router.get("/conflicts")
async def get_conflicts():
    return await graph_service.detect_conflicts()
