from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import (
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeUpdate,
    PaginatedNodes,
)
from app.services import graph_service

router = APIRouter()


@router.post("", response_model=IndustrialNode, status_code=201)
async def create_node(data: IndustrialNodeCreate):
    try:
        return await graph_service.create_node(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=PaginatedNodes)
async def list_nodes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = await graph_service.list_nodes(skip, page_size, entity_type, status, search)
    return PaginatedNodes(total=total, page=page, page_size=page_size, items=items)


@router.get("/{node_id}", response_model=IndustrialNode)
async def get_node(node_id: str):
    node = await graph_service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.put("/{node_id}", response_model=IndustrialNode)
async def update_node(node_id: str, data: IndustrialNodeUpdate):
    node = await graph_service.update_node(node_id, data)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.delete("/{node_id}", status_code=204)
async def delete_node(node_id: str):
    deleted = await graph_service.delete_node(node_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Node not found")
    return None
