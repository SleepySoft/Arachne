from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.engines.legacy.schemas import (
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeQuickCreate,
    IndustrialNodeUpdate,
    PaginatedNodes,
)
from app.services import fuzzy_search, graph_service

router = APIRouter()


@router.post("", response_model=IndustrialNode, status_code=201)
async def create_node(
    data: IndustrialNodeCreate,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    try:
        return await graph_service.create_node(data, engine=engine)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quick-create", response_model=IndustrialNode, status_code=201)
async def quick_create_node(
    data: IndustrialNodeQuickCreate,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    """快速创建草稿节点。只需提供中文名或英文名，系统自动生成 draft_ 占位 ID 并填充默认值。"""
    try:
        return await graph_service.quick_create_node(data, engine=engine)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fuzzy-search")
async def fuzzy_search_nodes(
    query: str = Query(..., min_length=2, description="Search query for similar node names"),
    limit: int = Query(10, ge=1, le=50),
    score_threshold: float = Query(0.35, ge=0.0, le=1.0),
):
    """Fuzzy search nodes by name similarity without vector DB.

    Returns a list of candidate nodes sorted by similarity score.
    """
    results = await fuzzy_search.fuzzy_search_nodes(query, limit, score_threshold)
    return {
        "query": query,
        "count": len(results),
        "items": [
            {
                "score": round(r["score"], 3),
                "node": r["node"],
            }
            for r in results
        ],
    }


@router.get("", response_model=PaginatedNodes)
async def list_nodes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    draft_only: Optional[bool] = Query(None, description="仅返回草稿/待完善节点"),
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    skip = (page - 1) * page_size
    items, total = await graph_service.list_nodes(
        skip, page_size, entity_type, status, search, draft_only, engine=engine
    )
    return PaginatedNodes(total=total, page=page, page_size=page_size, items=items)


@router.get("/{node_id}", response_model=IndustrialNode)
async def get_node(
    node_id: str,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    node = await graph_service.get_node(node_id, engine=engine)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.put("/{node_id}", response_model=IndustrialNode)
async def update_node(
    node_id: str,
    data: IndustrialNodeUpdate,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    node = await graph_service.update_node(node_id, data, engine=engine)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.delete("/{node_id}", status_code=204)
async def delete_node(
    node_id: str,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    deleted = await graph_service.delete_node(node_id, engine=engine)
    if not deleted:
        raise HTTPException(status_code=404, detail="Node not found")
    return None
