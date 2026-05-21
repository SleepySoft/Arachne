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


@router.get("/conflicts")
async def get_conflicts():
    return await graph_service.detect_conflicts()
