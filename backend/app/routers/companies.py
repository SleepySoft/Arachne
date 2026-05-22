from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.company_schema import Company, CompanyNodeExposure
from app.models.schemas import IndustrialNode
from app.services import company_storage
from app.database import get_async_driver

router = APIRouter()


@router.post("", response_model=Company, status_code=201)
async def create_company(data: Company):
    try:
        existing = await company_storage.get_company(data.company_id)
        if existing:
            raise HTTPException(409, "Company already exists")
        return await company_storage.create_company(data)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get("", response_model=dict)
async def list_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    country: Optional[str] = None,
    company_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = await company_storage.list_companies(
        skip=skip,
        limit=page_size,
        country=country,
        company_type=company_type,
        status=status,
        search=search,
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{company_id}", response_model=Company)
async def get_company(company_id: str):
    company = await company_storage.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: str, data: dict):
    existing = await company_storage.get_company(company_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Company not found")
    updated = await company_storage.update_company(company_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated


@router.delete("/{company_id}", status_code=204)
async def delete_company(company_id: str):
    deleted = await company_storage.delete_company(company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return None


@router.get("/{company_id}/exposures", response_model=dict)
async def list_company_exposures(
    company_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    activity_type: Optional[str] = None,
):
    company = await company_storage.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    skip = (page - 1) * page_size
    items, total = await company_storage.list_exposures_by_company(
        company_id, skip=skip, limit=page_size, activity_type=activity_type
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{company_id}/nodes", response_model=List[IndustrialNode])
async def get_company_nodes(company_id: str):
    """Return the IndustrialNodes exposed by this company."""
    company = await company_storage.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    exposures, _ = await company_storage.list_exposures_by_company(company_id, limit=1000)
    node_ids = [e.node_id for e in exposures]
    if not node_ids:
        return []

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


@router.get("/{company_id}/subgraph", response_model=dict)
async def get_company_subgraph(company_id: str):
    """Return the company temporary subgraph: exposed nodes + edges between them from Neo4j."""
    company = await company_storage.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    exposures, _ = await company_storage.list_exposures_by_company(company_id, limit=1000)
    node_ids = [e.node_id for e in exposures]
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

        # Fetch edges between exposed nodes
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
