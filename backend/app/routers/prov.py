from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.prov_schema import ProvStatement
from app.services import prov_storage

router = APIRouter()


@router.post("/statements", response_model=ProvStatement, status_code=201)
async def create_statement(data: ProvStatement):
    try:
        return await prov_storage.create_statement(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/statements", response_model=dict)
async def list_statements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    node_id: Optional[str] = None,
    target_node_id: Optional[str] = None,
    prov_relation: Optional[str] = None,
    status: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = await prov_storage.list_statements(
        skip=skip,
        limit=page_size,
        node_id=node_id,
        target_node_id=target_node_id,
        prov_relation=prov_relation,
        status=status,
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/statements/{statement_id}", response_model=ProvStatement)
async def get_statement(statement_id: str):
    statement = await prov_storage.get_statement(statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="PROV statement not found")
    return statement


@router.put("/statements/{statement_id}", response_model=ProvStatement)
async def update_statement(statement_id: str, data: dict):
    existing = await prov_storage.get_statement(statement_id)
    if not existing:
        raise HTTPException(status_code=404, detail="PROV statement not found")

    updated = await prov_storage.update_statement(statement_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="PROV statement not found")
    return updated


@router.delete("/statements/{statement_id}", status_code=204)
async def delete_statement(statement_id: str):
    existing = await prov_storage.get_statement(statement_id)
    if not existing:
        raise HTTPException(status_code=404, detail="PROV statement not found")

    deleted = await prov_storage.delete_statement(statement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="PROV statement not found")
    return None


@router.get("/nodes/{node_id}/statements", response_model=dict)
async def list_statements_for_node(
    node_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
):
    skip = (page - 1) * page_size
    items, total = await prov_storage.list_statements_by_node(
        node_id, skip=skip, limit=page_size
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}
