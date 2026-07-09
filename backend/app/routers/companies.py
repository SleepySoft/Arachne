from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel

from app.models.company_schema import Company, CompanyNodeExposure
from app.models.schemas import EDGE_TYPE_LABELS, IndustrialNode
from app.database import get_async_driver
from app.services import company_storage, node_storage
from app.services.neo4j_storage import _to_datetime, _evidence_from_db

router = APIRouter()


@router.post("", response_model=Company, status_code=201)
async def create_company(data: Company):
    try:
        existing = await company_storage.get_company(data.company_id)
        if existing:
            raise HTTPException(409, "Company already exists")
        existing_name = await company_storage.get_company_by_name_zh(data.name_zh)
        if existing_name:
            raise HTTPException(409, "公司名称已存在")
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


@router.post("/{company_id}/exposures", response_model=CompanyNodeExposure, status_code=201)
async def create_company_exposure(company_id: str, data: CompanyNodeExposure):
    company = await company_storage.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if data.company_id != company_id:
        raise HTTPException(status_code=400, detail="company_id mismatch")

    try:
        return await company_storage.create_exposure(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{company_id}/exposures/{exposure_id}", status_code=204)
async def delete_company_exposure(company_id: str, exposure_id: str):
    exposure = await company_storage.get_exposure(exposure_id)
    if not exposure or exposure.company_id != company_id:
        raise HTTPException(status_code=404, detail="Exposure not found")

    deleted = await company_storage.delete_exposure(exposure_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Exposure not found")
    return None


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

    # Fetch node metadata from PostgreSQL
    nodes_map = await node_storage.get_nodes_by_ids(node_ids)
    return [nodes_map[nid] for nid in node_ids if nid in nodes_map]


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

    # Fetch node metadata from PostgreSQL
    nodes_map = await node_storage.get_nodes_by_ids(node_ids)
    nodes = [nodes_map[nid] for nid in node_ids if nid in nodes_map]

    driver = get_async_driver()
    async with driver.session() as session:
        # Fetch edges between exposed nodes (include both industrial flow and ontology relations)
        edge_result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b:IndustrialNode)
            WHERE a.node_id IN $node_ids AND b.node_id IN $node_ids
            RETURN a.node_id AS from_node, b.node_id AS to_node,
                   r.edge_id AS edge_id, r.edge_namespace AS edge_namespace,
                   r.edge_type AS edge_type,
                   r.description AS description, r.confidence AS confidence,
                   r.notes AS notes, r.evidence AS evidence,
                   r.created_at AS created_at, r.updated_at AS updated_at
            """,
            node_ids=node_ids,
        )
        edge_records = await edge_result.data()
        edges = []
        for record in edge_records:
            edges.append({
                "from_node": record["from_node"],
                "to_node": record["to_node"],
                "edge_id": record["edge_id"],
                "edge_namespace": record["edge_namespace"],
                "edge_type": record["edge_type"],
                "edge_type_label": EDGE_TYPE_LABELS.get(record["edge_type"], record["edge_type"]),
                "description": record["description"],
                "confidence": record["confidence"],
                "notes": record["notes"],
                "evidence": _evidence_from_db(record.get("evidence")),
                "created_at": _to_datetime(record.get("created_at")),
                "updated_at": _to_datetime(record.get("updated_at")),
            })

        return {"nodes": nodes, "edges": edges}


@router.get("/by-node/{node_id}", response_model=dict)
async def get_companies_by_node(node_id: str):
    """返回暴露到该产业节点的所有公司及其暴露关系。"""
    exposures, _ = await company_storage.list_exposures_by_node(node_id, limit=1000)
    if not exposures:
        return {"node_id": node_id, "companies": [], "exposures": []}

    companies = []
    for e in exposures:
        c = await company_storage.get_company(e.company_id)
        if c:
            companies.append(c)

    return {"node_id": node_id, "companies": companies, "exposures": exposures}


class NodeIdsRequest(BaseModel):
    node_ids: List[str]


@router.post("/by-nodes", response_model=dict)
async def get_companies_by_nodes(request: NodeIdsRequest):
    """返回暴露到一组产业节点的所有公司及其暴露关系（去重并集）。"""
    node_ids = request.node_ids
    if not node_ids:
        return {"node_ids": node_ids, "companies": [], "exposures": []}

    exposures = await company_storage.list_exposures_by_nodes(node_ids, limit=1000)
    if not exposures:
        return {"node_ids": node_ids, "companies": [], "exposures": []}

    company_ids = list({e.company_id for e in exposures})
    companies = await company_storage.get_companies_by_ids(company_ids)

    return {"node_ids": node_ids, "companies": companies, "exposures": exposures}
