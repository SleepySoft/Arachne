"""
================================================================================
 DOMAIN: FACTUAL GRAPH — Storage Layer
================================================================================
PostgreSQL + Neo4j dual storage for the Factual Graph.

PostgreSQL (authoritative source):
  - persons table
  - factual_relations table

Neo4j (graph traversal & exploration):
  - :Person nodes
  - :Company nodes (lightweight sync from PG companies)
  - Typed relationships: :SHAREHOLDER_OF, :SPOUSE, :SUPPLIER_OF, etc.

Neo4j constraints:
  - Does NOT support nested Map properties → evidence serialized as JSON string
================================================================================
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool
from app.models.factual_graph_schema import (
    CompanyCompanyRelation,
    FactualRelation,
    Person,
    PersonCompanyRelation,
    PersonPersonRelation,
    PersonCreate,
    PersonUpdate,
)
from app.models.schemas import Evidence


# ---------------------------------------------------------------------------
# JSON / datetime helpers (same pattern as neo4j_storage.py)
# ---------------------------------------------------------------------------

def _to_datetime(val: Any) -> Optional[datetime]:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    # neo4j.time.DateTime fallback
    if hasattr(val, "to_native"):
        return val.to_native()
    if hasattr(val, "isoformat"):
        return datetime.fromisoformat(val.isoformat())
    return None


def _evidence_to_db(evidence: List[Evidence]) -> str:
    return json.dumps([e.model_dump(mode="json") for e in evidence], ensure_ascii=False)


def _evidence_from_db(raw: Any) -> List[Evidence]:
    if raw is None:
        return []
    if isinstance(raw, str):
        data = json.loads(raw)
    elif isinstance(raw, list):
        data = raw
    else:
        return []
    return [Evidence(**item) for item in data]


# ---------------------------------------------------------------------------
# Person — PostgreSQL CRUD
# ---------------------------------------------------------------------------

async def create_person(person: Person) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """
                INSERT INTO persons (
                    person_id, name_zh, name_en, aliases, gender, birth_year,
                    nationality, id_card_hash, profile, status, notes, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW(), NOW())
                """,
                person.person_id,
                person.name_zh,
                person.name_en,
                person.aliases or [],
                person.gender,
                person.birth_year,
                person.nationality,
                person.id_card_hash,
                person.profile,
                person.status.value,
                person.notes,
            )
            return True
        except Exception:
            return False


async def get_person(person_id: str) -> Optional[Person]:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM persons WHERE person_id = $1",
            person_id,
        )
    if row is None:
        return None
    return _row_to_person(row)


async def list_persons(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[Person], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    offset = (page - 1) * page_size
    conditions = []
    params: List[Any] = []
    param_idx = 1

    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1
    if search:
        conditions.append(f"(name_zh ILIKE ${param_idx} OR name_en ILIKE ${param_idx} OR person_id ILIKE ${param_idx})")
        params.append(f"%{search}%")
        param_idx += 1

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM persons {where_clause}",
            *params,
        )
        total = total_row[0] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM persons
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            page_size,
            offset,
        )

    return [_row_to_person(r) for r in rows], total


async def update_person(person_id: str, update: PersonUpdate) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    fields = []
    values: List[Any] = []
    param_idx = 1

    for field, val in update.model_dump(exclude_unset=True).items():
        if val is not None:
            fields.append(f"{field} = ${param_idx}")
            values.append(val)
            param_idx += 1

    if not fields:
        return False

    fields.append(f"updated_at = ${param_idx}")
    values.append(datetime.now(timezone.utc))
    param_idx += 1
    values.append(person_id)

    async with pool.acquire() as conn:
        result = await conn.execute(
            f"UPDATE persons SET {', '.join(fields)} WHERE person_id = ${param_idx}",
            *values,
        )
    return "UPDATE 1" in result


async def delete_person(person_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM persons WHERE person_id = $1",
            person_id,
        )
    return "DELETE 1" in result


def _row_to_person(row: Any) -> Person:
    return Person(
        person_uuid=row["person_uuid"],
        person_id=row["person_id"],
        name_zh=row["name_zh"],
        name_en=row["name_en"],
        aliases=list(row["aliases"]) if row["aliases"] else [],
        gender=row["gender"],
        birth_year=row["birth_year"],
        nationality=row["nationality"],
        id_card_hash=row["id_card_hash"],
        profile=row["profile"],
        status=row["status"],
        notes=row["notes"],
        created_at=_to_datetime(row["created_at"]),
        updated_at=_to_datetime(row["updated_at"]),
    )


# ---------------------------------------------------------------------------
# Factual Relation — PostgreSQL CRUD
# ---------------------------------------------------------------------------

async def create_relation(relation: FactualRelation) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    data = _relation_to_db_dict(relation)
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """
                INSERT INTO factual_relations (
                    relation_id, relation_type, relation_domain,
                    from_entity_type, from_entity_id, to_entity_type, to_entity_id,
                    subtype, equity_ratio, amount_cny, contract_no, proportion,
                    start_date, end_date, is_history,
                    evidence, source, confidence, status, notes, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, NOW(), NOW())
                """,
                data["relation_id"],
                data["relation_type"],
                data["relation_domain"],
                data["from_entity_type"],
                data["from_entity_id"],
                data["to_entity_type"],
                data["to_entity_id"],
                data["subtype"],
                data["equity_ratio"],
                data["amount_cny"],
                data["contract_no"],
                data["proportion"],
                data["start_date"],
                data["end_date"],
                data["is_history"],
                data["evidence"],
                data["source"],
                data["confidence"],
                data["status"],
                data["notes"],
            )
            return True
        except Exception:
            return False


async def get_relation(relation_id: str) -> Optional[FactualRelation]:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM factual_relations WHERE relation_id = $1",
            relation_id,
        )
    if row is None:
        return None
    return _row_to_relation(row)


async def list_relations(
    page: int = 1,
    page_size: int = 20,
    relation_domain: Optional[str] = None,
    from_entity_id: Optional[str] = None,
    to_entity_id: Optional[str] = None,
    relation_type: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[FactualRelation], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    offset = (page - 1) * page_size
    conditions = []
    params: List[Any] = []
    param_idx = 1

    if relation_domain:
        conditions.append(f"relation_domain = ${param_idx}")
        params.append(relation_domain)
        param_idx += 1
    if from_entity_id:
        conditions.append(f"from_entity_id = ${param_idx}")
        params.append(from_entity_id)
        param_idx += 1
    if to_entity_id:
        conditions.append(f"to_entity_id = ${param_idx}")
        params.append(to_entity_id)
        param_idx += 1
    if relation_type:
        conditions.append(f"relation_type = ${param_idx}")
        params.append(relation_type)
        param_idx += 1
    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM factual_relations {where_clause}",
            *params,
        )
        total = total_row[0] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM factual_relations
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            page_size,
            offset,
        )

    return [_row_to_relation(r) for r in rows], total


async def update_relation(relation_id: str, updates: Dict[str, Any]) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    allowed = {
        "relation_type", "subtype", "equity_ratio", "amount_cny",
        "contract_no", "proportion", "start_date", "end_date",
        "is_history", "evidence", "source", "confidence", "status", "notes",
    }
    fields = []
    values: List[Any] = []
    param_idx = 1

    for k, v in updates.items():
        if k not in allowed or v is None:
            continue
        if k == "evidence" and isinstance(v, list):
            v = json.dumps(v, ensure_ascii=False)
        fields.append(f"{k} = ${param_idx}")
        values.append(v)
        param_idx += 1

    if not fields:
        return False

    fields.append(f"updated_at = ${param_idx}")
    values.append(datetime.now(timezone.utc))
    param_idx += 1
    values.append(relation_id)

    async with pool.acquire() as conn:
        result = await conn.execute(
            f"UPDATE factual_relations SET {', '.join(fields)} WHERE relation_id = ${param_idx}",
            *values,
        )
    return "UPDATE 1" in result


async def delete_relation(relation_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM factual_relations WHERE relation_id = $1",
            relation_id,
        )
    return "DELETE 1" in result


def _relation_to_db_dict(relation: FactualRelation) -> Dict[str, Any]:
    base = {
        "relation_id": relation.relation_id,
        "relation_type": relation.relation_type.value if hasattr(relation.relation_type, "value") else relation.relation_type,
        "relation_domain": relation.relation_domain,
        "evidence": _evidence_to_db(relation.evidence),
        "source": relation.source,
        "confidence": relation.confidence.value,
        "status": relation.status.value,
        "start_date": relation.start_date,
        "end_date": relation.end_date,
        "is_history": relation.is_history,
        "notes": relation.notes,
        "subtype": None,
        "equity_ratio": None,
        "amount_cny": None,
        "contract_no": None,
        "proportion": None,
    }

    if isinstance(relation, PersonCompanyRelation):
        base.update({
            "from_entity_type": "person",
            "from_entity_id": relation.person_id,
            "to_entity_type": "company",
            "to_entity_id": relation.company_id,
            "subtype": relation.subtype,
            "equity_ratio": relation.equity_ratio,
            "amount_cny": int(relation.amount_cny) if relation.amount_cny else None,
        })
    elif isinstance(relation, PersonPersonRelation):
        base.update({
            "from_entity_type": "person",
            "from_entity_id": relation.from_person_id,
            "to_entity_type": "person",
            "to_entity_id": relation.to_person_id,
            "subtype": relation.subtype,
        })
    elif isinstance(relation, CompanyCompanyRelation):
        base.update({
            "from_entity_type": "company",
            "from_entity_id": relation.from_company_id,
            "to_entity_type": "company",
            "to_entity_id": relation.to_company_id,
            "amount_cny": int(relation.amount_cny) if relation.amount_cny else None,
            "contract_no": relation.contract_no,
            "proportion": relation.proportion,
        })

    return base


def _row_to_relation(row: Any) -> FactualRelation:
    evidence = _evidence_from_db(row["evidence"])
    domain = row["relation_domain"]

    common = {
        "relation_id": row["relation_id"],
        "relation_type": row["relation_type"],
        "evidence": evidence,
        "source": row["source"],
        "confidence": row["confidence"],
        "status": row["status"],
        "start_date": row["start_date"],
        "end_date": row["end_date"],
        "is_history": row["is_history"],
        "notes": row["notes"],
        "created_at": _to_datetime(row["created_at"]),
        "updated_at": _to_datetime(row["updated_at"]),
    }

    if domain == "person_company":
        return PersonCompanyRelation(
            relation_domain="person_company",
            person_id=row["from_entity_id"],
            company_id=row["to_entity_id"],
            subtype=row["subtype"],
            equity_ratio=row["equity_ratio"],
            amount_cny=row["amount_cny"],
            **common,
        )
    elif domain == "person_person":
        return PersonPersonRelation(
            relation_domain="person_person",
            from_person_id=row["from_entity_id"],
            to_person_id=row["to_entity_id"],
            subtype=row["subtype"],
            **common,
        )
    elif domain == "company_company":
        return CompanyCompanyRelation(
            relation_domain="company_company",
            from_company_id=row["from_entity_id"],
            to_company_id=row["to_entity_id"],
            amount_cny=row["amount_cny"],
            contract_no=row["contract_no"],
            proportion=row["proportion"],
            **common,
        )
    else:
        raise ValueError(f"Unknown relation_domain: {domain}")


# ---------------------------------------------------------------------------
# Neo4j — Person / Company nodes + typed relationships
# ---------------------------------------------------------------------------

RELATION_TYPE_MAP = {
    # person_company
    "shareholder": "SHAREHOLDER_OF",
    "executive": "EXECUTIVE_OF",
    "legal_representative": "LEGAL_REP_OF",
    "actual_controller": "ACTUAL_CONTROLLER_OF",
    "supervisor": "SUPERVISOR_OF",
    "director": "DIRECTOR_OF",
    "board_chair": "BOARD_CHAIR_OF",
    "general_manager": "GENERAL_MANAGER_OF",
    "history_role": "HISTORY_ROLE_OF",
    # person_person
    "relative": "RELATIVE_OF",
    "spouse": "SPOUSE",
    "parent_child": "PARENT_CHILD_OF",
    "sibling": "SIBLING_OF",
    "partner": "PARTNER_WITH",
    "colleague": "COLLEAGUE_WITH",
    "trust": "TRUST",
    "associate": "ASSOCIATE_OF",
    # company_company
    "supplier": "SUPPLIER_OF",
    "customer": "CUSTOMER_OF",
    "partner": "PARTNER_WITH",
    "investor": "INVESTOR_OF",
    "investee": "INVESTEE_OF",
    "competitor": "COMPETITOR_WITH",
    "client": "CLIENT_OF",
    "contractor": "CONTRACTOR_OF",
    "guarantor": "GUARANTOR_OF",
    "creditor": "CREDITOR_OF",
    "debtor": "DEBTOR_OF",
    "lessee": "LESSEE_OF",
    "lessor": "LESSOR_OF",
}


async def sync_person_to_neo4j(person: Person) -> bool:
    """Upsert a :Person node in Neo4j."""
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MERGE (p:Person {person_id: $person_id})
            ON CREATE SET
                p.name_zh = $name_zh,
                p.name_en = $name_en,
                p.aliases = $aliases,
                p.gender = $gender,
                p.birth_year = $birth_year,
                p.nationality = $nationality,
                p.id_card_hash = $id_card_hash,
                p.profile = $profile,
                p.status = $status,
                p.created_at = datetime()
            ON MATCH SET
                p.name_zh = $name_zh,
                p.name_en = $name_en,
                p.aliases = $aliases,
                p.gender = $gender,
                p.birth_year = $birth_year,
                p.nationality = $nationality,
                p.id_card_hash = $id_card_hash,
                p.profile = $profile,
                p.status = $status,
                p.updated_at = datetime()
            RETURN p.person_id AS pid
            """,
            person_id=person.person_id,
            name_zh=person.name_zh or "",
            name_en=person.name_en or "",
            aliases=person.aliases or [],
            gender=person.gender or "",
            birth_year=person.birth_year,
            nationality=person.nationality or "",
            id_card_hash=person.id_card_hash or "",
            profile=person.profile or "",
            status=person.status.value if person.status else "PENDING",
        )
        record = await result.single()
        return record is not None


async def sync_company_to_neo4j(company_id: str, name_zh: str) -> bool:
    """Upsert a lightweight :Company node in Neo4j (from PG companies)."""
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MERGE (c:Company {company_id: $company_id})
            ON CREATE SET
                c.name_zh = $name_zh,
                c.created_at = datetime()
            ON MATCH SET
                c.name_zh = $name_zh,
                c.updated_at = datetime()
            RETURN c.company_id AS cid
            """,
            company_id=company_id,
            name_zh=name_zh or company_id,
        )
        record = await result.single()
        return record is not None


async def sync_companies_to_neo4j() -> int:
    """Batch sync all ACTIVE companies from PG into Neo4j as :Company nodes."""
    pool = await get_postgres_pool()
    if pool is None:
        return 0

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT company_id, name_zh
            FROM companies
            WHERE status = 'ACTIVE'
            ORDER BY company_id
            """
        )

    if not rows:
        return 0

    driver = get_async_driver()
    companies = [
        {"company_id": r["company_id"], "name_zh": r["name_zh"] or ""}
        for r in rows
    ]

    BATCH_SIZE = 500
    total = 0
    for i in range(0, len(companies), BATCH_SIZE):
        chunk = companies[i : i + BATCH_SIZE]
        async with driver.session() as session:
            result = await session.run(
                """
                UNWIND $companies AS c
                MERGE (co:Company {company_id: c.company_id})
                ON CREATE SET co.name_zh = c.name_zh, co.created_at = datetime()
                ON MATCH SET co.name_zh = c.name_zh, co.updated_at = datetime()
                RETURN count(co) AS cnt
                """,
                companies=chunk,
            )
            record = await result.single()
            total += record["cnt"] if record else 0

    return total


async def create_relation_in_neo4j(relation: FactualRelation) -> bool:
    """Create a typed relationship in Neo4j for the given factual relation."""
    rel_type = RELATION_TYPE_MAP.get(
        relation.relation_type.value if hasattr(relation.relation_type, "value") else relation.relation_type
    )
    if not rel_type:
        return False

    props = {
        "relation_id": relation.relation_id,
        "source": relation.source,
        "confidence": relation.confidence.value if hasattr(relation.confidence, "value") else relation.confidence,
        "status": relation.status.value if hasattr(relation.status, "value") else relation.status,
        "evidence": _evidence_to_db(relation.evidence),
    }
    if relation.start_date:
        props["start_date"] = relation.start_date.isoformat()
    if relation.end_date:
        props["end_date"] = relation.end_date.isoformat()
    if relation.is_history:
        props["is_history"] = True
    if relation.notes:
        props["notes"] = relation.notes

    # Subtype
    subtype = None
    if hasattr(relation, "subtype") and relation.subtype:
        subtype = relation.subtype
        props["subtype"] = subtype

    # Domain-specific numeric props
    if hasattr(relation, "equity_ratio") and relation.equity_ratio is not None:
        props["equity_ratio"] = relation.equity_ratio
    if hasattr(relation, "amount_cny") and relation.amount_cny is not None:
        props["amount_cny"] = relation.amount_cny
    if hasattr(relation, "contract_no") and relation.contract_no:
        props["contract_no"] = relation.contract_no
    if hasattr(relation, "proportion") and relation.proportion is not None:
        props["proportion"] = relation.proportion

    driver = get_async_driver()

    if isinstance(relation, PersonCompanyRelation):
        from_label, from_id = "Person", relation.person_id
        to_label, to_id = "Company", relation.company_id
    elif isinstance(relation, PersonPersonRelation):
        from_label, from_id = "Person", relation.from_person_id
        to_label, to_id = "Person", relation.to_person_id
    elif isinstance(relation, CompanyCompanyRelation):
        from_label, from_id = "Company", relation.from_company_id
        to_label, to_id = "Company", relation.to_company_id
    else:
        return False

    # Build dynamic property string
    prop_keys = list(props.keys())
    prop_str = ", ".join([f"{k}: ${k}" for k in prop_keys])

    async with driver.session() as session:
        result = await session.run(
            f"""
            MATCH (a:{from_label} {{{'person_id' if from_label == 'Person' else 'company_id'}: $from_id}}),
                  (b:{to_label} {{{'person_id' if to_label == 'Person' else 'company_id'}: $to_id}})
            CREATE (a)-[r:{rel_type} {{{prop_str}}}]->(b)
            RETURN r
            """,
            from_id=from_id,
            to_id=to_id,
            **props,
        )
        record = await result.single()
        return record is not None


async def delete_relation_from_neo4j(relation_id: str) -> bool:
    """Delete any Neo4j relationship that has the given relation_id property."""
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH ()-[r]->()
            WHERE r.relation_id = $relation_id
            DELETE r
            RETURN count(r) AS cnt
            """,
            relation_id=relation_id,
        )
        record = await result.single()
        return (record["cnt"] if record else 0) > 0


# ---------------------------------------------------------------------------
# Neo4j — Queries for the Factual Graph
# ---------------------------------------------------------------------------

async def get_person_neighborhood(person_id: str, max_depth: int = 2) -> dict:
    """Return the subgraph centered on a Person (within the Factual Graph only)."""
    driver = get_async_driver()
    relation_types = "|".join(RELATION_TYPE_MAP.values())

    async with driver.session() as session:
        node_result = await session.run(
            f"""
            MATCH (center:Person {{person_id: $person_id}})-[r:{relation_types}*1..{max_depth}]-(n)
            RETURN DISTINCT
                CASE WHEN n:Person THEN 'person' ELSE 'company' END AS node_type,
                COALESCE(n.person_id, n.company_id) AS id,
                COALESCE(n.name_zh, n.company_id) AS label
            """,
            person_id=person_id,
        )
        node_records = await node_result.data()

        edge_result = await session.run(
            f"""
            MATCH (center:Person {{person_id: $person_id}})-[r:{relation_types}*1..{max_depth}]-(n)
            WITH center, r, n
            UNWIND r AS rel
            RETURN DISTINCT
                COALESCE(startNode(rel).person_id, startNode(rel).company_id) AS from_id,
                COALESCE(endNode(rel).person_id, endNode(rel).company_id) AS to_id,
                type(rel) AS relation_type,
                rel.subtype AS subtype,
                rel.source AS source
            """,
            person_id=person_id,
        )
        edge_records = await edge_result.data()

    # Add center node if not already present
    center_present = any(r["id"] == person_id for r in node_records)
    if not center_present:
        node_records.insert(0, {"node_type": "person", "id": person_id, "label": person_id})

    return {
        "nodes": [
            {"id": r["id"], "type": r["node_type"], "label": r["label"] or r["id"]}
            for r in node_records
        ],
        "edges": [
            {
                "from_id": r["from_id"],
                "to_id": r["to_id"],
                "relation_type": r["relation_type"],
                "subtype": r.get("subtype"),
                "source": r.get("source"),
            }
            for r in edge_records
        ],
    }


async def get_company_neighborhood(company_id: str, max_depth: int = 2) -> dict:
    """Return the subgraph centered on a Company (within the Factual Graph only)."""
    driver = get_async_driver()
    relation_types = "|".join(RELATION_TYPE_MAP.values())

    async with driver.session() as session:
        node_result = await session.run(
            f"""
            MATCH (center:Company {{company_id: $company_id}})-[r:{relation_types}*1..{max_depth}]-(n)
            RETURN DISTINCT
                CASE WHEN n:Person THEN 'person' ELSE 'company' END AS node_type,
                COALESCE(n.person_id, n.company_id) AS id,
                COALESCE(n.name_zh, n.company_id) AS label
            """,
            company_id=company_id,
        )
        node_records = await node_result.data()

        edge_result = await session.run(
            f"""
            MATCH (center:Company {{company_id: $company_id}})-[r:{relation_types}*1..{max_depth}]-(n)
            WITH center, r, n
            UNWIND r AS rel
            RETURN DISTINCT
                COALESCE(startNode(rel).person_id, startNode(rel).company_id) AS from_id,
                COALESCE(endNode(rel).person_id, endNode(rel).company_id) AS to_id,
                type(rel) AS relation_type,
                rel.subtype AS subtype,
                rel.source AS source
            """,
            company_id=company_id,
        )
        edge_records = await edge_result.data()

    center_present = any(r["id"] == company_id for r in node_records)
    if not center_present:
        node_records.insert(0, {"node_type": "company", "id": company_id, "label": company_id})

    return {
        "nodes": [
            {"id": r["id"], "type": r["node_type"], "label": r["label"] or r["id"]}
            for r in node_records
        ],
        "edges": [
            {
                "from_id": r["from_id"],
                "to_id": r["to_id"],
                "relation_type": r["relation_type"],
                "subtype": r.get("subtype"),
                "source": r.get("source"),
            }
            for r in edge_records
        ],
    }
