from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.industry_schema import Industry, IndustryNodeMapping
from app.models.schemas import IndustrialNode, GraphEdge
from app.services import industry_storage
from app.database import get_async_driver

router = APIRouter()


@router.post("", response_model=Industry, status_code=201)
async def create_industry(data: Industry):
    try:
        existing = await industry_storage.get_industry(data.industry_id)
        if existing:
            raise HTTPException(409, "Industry already exists")
        return await industry_storage.create_industry(data)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get("", response_model=dict)
async def list_industries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    industry_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = await industry_storage.list_industries(
        skip=skip,
        limit=page_size,
        industry_type=industry_type,
        status=status,
        search=search,
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{industry_id}", response_model=Industry)
async def get_industry(industry_id: str):
    industry = await industry_storage.get_industry(industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    return industry


@router.put("/{industry_id}", response_model=Industry)
async def update_industry(industry_id: str, data: dict):
    existing = await industry_storage.get_industry(industry_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Industry not found")
    updated = await industry_storage.update_industry(industry_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Industry not found")
    return updated


@router.delete("/{industry_id}", status_code=204)
async def delete_industry(industry_id: str):
    deleted = await industry_storage.delete_industry(industry_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Industry not found")
    return None


@router.get("/{industry_id}/mappings", response_model=dict)
async def list_industry_mappings(
    industry_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
):
    industry = await industry_storage.get_industry(industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    skip = (page - 1) * page_size
    items, total = await industry_storage.list_mappings_by_industry(
        industry_id, skip=skip, limit=page_size
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{industry_id}/nodes", response_model=List[IndustrialNode])
async def get_industry_nodes(industry_id: str):
    """Return the IndustrialNodes mapped to this industry."""
    industry = await industry_storage.get_industry(industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    mappings, _ = await industry_storage.list_mappings_by_industry(industry_id, limit=1000)
    node_ids = [m.node_id for m in mappings]
    if not node_ids:
        return []

    # Query Neo4j for the actual nodes
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n
            """,
            node_ids=node_ids,
        )
        records = await result.data()
        nodes = []
        for record in records:
            props = dict(record["n"])
            nodes.append(IndustrialNode(**props))
        return nodes


@router.get("/{industry_id}/subgraph", response_model=dict)
async def get_industry_subgraph(industry_id: str):
    """Return the industry subgraph: mapped nodes + edges between them from Neo4j."""
    industry = await industry_storage.get_industry(industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    mappings, _ = await industry_storage.list_mappings_by_industry(industry_id, limit=1000)
    node_ids = [m.node_id for m in mappings]
    if not node_ids:
        return {"nodes": [], "edges": []}

    driver = get_async_driver()
    async with driver.session() as session:
        # Fetch nodes
        node_result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n
            """,
            node_ids=node_ids,
        )
        node_records = await node_result.data()
        nodes = []
        for record in node_records:
            props = dict(record["n"])
            nodes.append(IndustrialNode(**props))

        # Fetch edges between mapped nodes
        edge_result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE a.node_id IN $node_ids AND b.node_id IN $node_ids
            RETURN r, a.node_id AS from_node, b.node_id AS to_node
            """,
            node_ids=node_ids,
        )
        edge_records = await edge_result.data()
        edges = []
        for record in edge_records:
            rel = dict(record["r"])
            rel["from_node"] = record["from_node"]
            rel["to_node"] = record["to_node"]
            edges.append(rel)

        return {"nodes": nodes, "edges": edges}
