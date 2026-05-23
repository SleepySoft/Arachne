from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.industry_schema import Industry, IndustryNodeMapping
from app.models.schemas import EDGE_TYPE_LABELS, IndustrialNode, GraphEdge
from app.services import industry_storage
from app.services.neo4j_storage import _to_datetime, _evidence_from_db
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


@router.post("/{industry_id}/mappings", response_model=IndustryNodeMapping, status_code=201)
async def create_industry_mapping(industry_id: str, data: IndustryNodeMapping):
    industry = await industry_storage.get_industry(industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    if data.industry_id != industry_id:
        raise HTTPException(status_code=400, detail="industry_id mismatch")

    try:
        return await industry_storage.create_mapping(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{industry_id}/mappings/{mapping_id}", status_code=204)
async def delete_industry_mapping(industry_id: str, mapping_id: str):
    mapping = await industry_storage.get_mapping(mapping_id)
    if not mapping or mapping.industry_id != industry_id:
        raise HTTPException(status_code=404, detail="Mapping not found")

    deleted = await industry_storage.delete_mapping(mapping_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return None


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
            props["created_at"] = _to_datetime(props.get("created_at"))
            props["updated_at"] = _to_datetime(props.get("updated_at"))
            props["evidence"] = _evidence_from_db(props.get("evidence"))
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
            props["created_at"] = _to_datetime(props.get("created_at"))
            props["updated_at"] = _to_datetime(props.get("updated_at"))
            props["evidence"] = _evidence_from_db(props.get("evidence"))
            nodes.append(IndustrialNode(**props))

        # Fetch edges between mapped nodes
        edge_result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
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
async def get_industries_by_node(node_id: str):
    """返回映射了该产业节点的所有行业及其映射关系。"""
    mappings, _ = await industry_storage.list_mappings_by_node(node_id, limit=1000)
    if not mappings:
        return {"node_id": node_id, "industries": [], "mappings": []}

    industries = []
    for m in mappings:
        ind = await industry_storage.get_industry(m.industry_id)
        if ind:
            industries.append(ind)

    return {"node_id": node_id, "industries": industries, "mappings": mappings}
