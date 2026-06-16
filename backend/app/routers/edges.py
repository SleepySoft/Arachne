from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import (
    GraphEdge,
    GraphEdgeCreate,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialFlowEdgeQuickCreate,
    IndustrialFlowEdgeUpdate,
    OntologyEdgeCreate,
    OntologyEdgeUpdate,
    PaginatedEdges,
)
from app.services import graph_service

router = APIRouter()


@router.post("", response_model=GraphEdge, status_code=201)
async def create_edge(data: GraphEdgeCreate):
    try:
        return await graph_service.create_edge(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quick-create", response_model=IndustrialFlowEdge, status_code=201)
async def quick_create_edge(data: IndustrialFlowEdgeQuickCreate):
    """快速创建产业流关系。只需提供 from_node 和 to_node，系统自动生成 edge_id 和描述。"""
    try:
        return await graph_service.quick_create_edge(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=PaginatedEdges)
async def list_edges(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    edge_namespace: Optional[str] = None,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = await graph_service.list_edges(
        skip, page_size, edge_namespace, edge_type, from_node, to_node
    )
    return PaginatedEdges(total=total, page=page, page_size=page_size, items=items)


@router.get("/{edge_id}", response_model=GraphEdge)
async def get_edge(edge_id: str):
    edge = await graph_service.get_edge(edge_id)
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    return edge


@router.put("/{edge_id}", response_model=GraphEdge)
async def update_edge(edge_id: str, data):
    existing = await graph_service.get_edge(edge_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Edge not found")

    ns = existing.edge_namespace
    if ns == "industrial_flow":
        update_data = IndustrialFlowEdgeUpdate(**data.model_dump(exclude_unset=True))
    else:
        update_data = OntologyEdgeUpdate(**data.model_dump(exclude_unset=True))

    edge = await graph_service.update_edge(edge_id, update_data, ns)
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    return edge


@router.delete("/{edge_id}", status_code=204)
async def delete_edge(edge_id: str):
    existing = await graph_service.get_edge(edge_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Edge not found")

    deleted = await graph_service.delete_edge(edge_id, existing.edge_namespace)
    if not deleted:
        raise HTTPException(status_code=404, detail="Edge not found")
    return None
