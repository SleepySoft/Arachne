"""
================================================================================
 DOMAIN: FACTUAL GRAPH — REST API Router
================================================================================

All endpoints under /api/v1/factual-graph/* operate exclusively within the
Factual Graph domain (:Person, :Company, and factual relations).

No :IndustrialNode or :INDUSTRIAL_FLOW is ever touched by these endpoints.
================================================================================
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.factual_graph_schema import (
    CompanyCompanyRelation,
    FactualRelation,
    PaginatedPersons,
    PaginatedRelations,
    Person,
    PersonCompanyRelation,
    PersonCreate,
    PersonPersonRelation,
    PersonUpdate,
)
from app.services import factual_graph_storage as storage

router = APIRouter()


# ---------------------------------------------------------------------------
# Persons
# ---------------------------------------------------------------------------

@router.post("/persons", response_model=Person, status_code=201)
async def create_person(person: PersonCreate):
    """Create a new Person in the Factual Graph."""
    # Build full Person from create input
    full_person = Person(
        person_id=person.person_id,
        name_zh=person.name_zh,
        name_en=person.name_en,
        aliases=person.aliases,
        gender=person.gender,
        birth_year=person.birth_year,
        nationality=person.nationality,
        id_card_hash=person.id_card_hash,
        profile=person.profile,
        status=person.status,
        notes=person.notes,
    )

    ok = await storage.create_person(full_person)
    if not ok:
        raise HTTPException(status_code=409, detail="Person already exists or DB error")

    # Sync to Neo4j
    await storage.sync_person_to_neo4j(full_person)

    return full_person


@router.get("/persons", response_model=PaginatedPersons)
async def list_persons(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    """List persons with optional filtering."""
    items, total = await storage.list_persons(
        page=page, page_size=page_size, status=status, search=search
    )
    return PaginatedPersons(total=total, page=page, page_size=page_size, items=items)


@router.get("/persons/{person_id}", response_model=Person)
async def get_person(person_id: str):
    """Get a single person by ID."""
    person = await storage.get_person(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.put("/persons/{person_id}", response_model=Person)
async def update_person(person_id: str, update: PersonUpdate):
    """Update a person."""
    ok = await storage.update_person(person_id, update)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found or nothing to update")

    # Re-sync to Neo4j
    person = await storage.get_person(person_id)
    if person:
        await storage.sync_person_to_neo4j(person)
    return person


@router.delete("/persons/{person_id}", status_code=204)
async def delete_person(person_id: str):
    """Delete a person."""
    ok = await storage.delete_person(person_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found")
    return None


# ---------------------------------------------------------------------------
# Relations
# ---------------------------------------------------------------------------

@router.post("/relations/person-company", response_model=PersonCompanyRelation, status_code=201)
async def create_person_company_relation(relation: PersonCompanyRelation):
    """Create a Person → Company factual relation."""
    ok = await storage.create_relation(relation)
    if not ok:
        raise HTTPException(status_code=409, detail="Relation already exists or DB error")

    # Ensure both ends exist in Neo4j
    person = await storage.get_person(relation.person_id)
    if person:
        await storage.sync_person_to_neo4j(person)
    # Company node sync
    await storage.sync_company_to_neo4j(relation.company_id, "")

    await storage.create_relation_in_neo4j(relation)
    return relation


@router.post("/relations/person-person", response_model=PersonPersonRelation, status_code=201)
async def create_person_person_relation(relation: PersonPersonRelation):
    """Create a Person → Person factual relation."""
    ok = await storage.create_relation(relation)
    if not ok:
        raise HTTPException(status_code=409, detail="Relation already exists or DB error")

    for pid in (relation.from_person_id, relation.to_person_id):
        person = await storage.get_person(pid)
        if person:
            await storage.sync_person_to_neo4j(person)

    await storage.create_relation_in_neo4j(relation)
    return relation


@router.post("/relations/company-company", response_model=CompanyCompanyRelation, status_code=201)
async def create_company_company_relation(relation: CompanyCompanyRelation):
    """Create a Company → Company factual relation."""
    ok = await storage.create_relation(relation)
    if not ok:
        raise HTTPException(status_code=409, detail="Relation already exists or DB error")

    await storage.sync_company_to_neo4j(relation.from_company_id, "")
    await storage.sync_company_to_neo4j(relation.to_company_id, "")

    await storage.create_relation_in_neo4j(relation)
    return relation


@router.get("/relations", response_model=PaginatedRelations)
async def list_relations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    relation_domain: Optional[str] = None,
    from_entity_id: Optional[str] = None,
    to_entity_id: Optional[str] = None,
    relation_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """List factual relations with filtering."""
    items, total = await storage.list_relations(
        page=page,
        page_size=page_size,
        relation_domain=relation_domain,
        from_entity_id=from_entity_id,
        to_entity_id=to_entity_id,
        relation_type=relation_type,
        status=status,
    )
    return PaginatedRelations(total=total, page=page, page_size=page_size, items=items)


@router.get("/relations/{relation_id}", response_model=FactualRelation)
async def get_relation(relation_id: str):
    """Get a single relation by ID."""
    relation = await storage.get_relation(relation_id)
    if relation is None:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation


@router.put("/relations/{relation_id}", response_model=FactualRelation)
async def update_relation(relation_id: str, updates: Dict[str, Any]):
    """Update a factual relation (partial update)."""
    ok = await storage.update_relation(relation_id, updates)
    if not ok:
        raise HTTPException(status_code=404, detail="Relation not found or nothing to update")
    relation = await storage.get_relation(relation_id)
    return relation


@router.delete("/relations/{relation_id}", status_code=204)
async def delete_relation(relation_id: str):
    """Delete a factual relation."""
    await storage.delete_relation_from_neo4j(relation_id)
    ok = await storage.delete_relation(relation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Relation not found")
    return None


# ---------------------------------------------------------------------------
# Neighborhood (Factual Graph only)
# ---------------------------------------------------------------------------

@router.get("/persons/{person_id}/neighborhood")
async def get_person_neighborhood(
    person_id: str,
    max_depth: int = Query(2, ge=1, le=3),
):
    """Return the subgraph centered on a Person within the Factual Graph."""
    return await storage.get_person_neighborhood(person_id, max_depth)


@router.get("/companies/{company_id}/neighborhood")
async def get_company_neighborhood(
    company_id: str,
    max_depth: int = Query(2, ge=1, le=3),
):
    """Return the subgraph centered on a Company within the Factual Graph."""
    return await storage.get_company_neighborhood(company_id, max_depth)


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

@router.post("/sync-companies")
async def sync_companies_to_neo4j():
    """Batch sync all ACTIVE companies from PostgreSQL to Neo4j :Company nodes."""
    count = await storage.sync_companies_to_neo4j()
    return {"synced_count": count}
