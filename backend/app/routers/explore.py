"""
================================================================================
 DOMAIN: CROSS-DOMAIN EXPLORATION (跨域探索)
================================================================================

This is the ONLY router allowed to touch both the Industrial Graph and the
Factual Graph in a single request. All other routers are strictly single-domain.

Bridge layer: PostgreSQL company_node_exposures (node_id ↔ company_id)

Every response explicitly labels which domain each piece of data comes from.
================================================================================
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool
from app.services import factual_graph_storage as factual_storage

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _get_company_name(pool, company_id: str) -> str:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT name_zh FROM companies WHERE company_id = $1",
            company_id,
        )
    return row["name_zh"] if row else company_id


async def _get_node_names(node_ids: List[str]) -> dict:
    if not node_ids:
        return {}
    from app.services import node_storage

    nodes_map = await node_storage.get_nodes_by_ids(node_ids)
    return {
        node_id: node.canonical_name_zh or node_id
        for node_id, node in nodes_map.items()
    }


# ---------------------------------------------------------------------------
# 1. Company → Industrial Context
# ---------------------------------------------------------------------------

@router.get("/companies/{company_id}/industrial-context")
async def explore_company_industrial_context(company_id: str):
    """
    Starting from a Company (Factual Graph), explore its position in the
    Industrial Graph via company_node_exposures bridge.

    Returns:
      - Exposed industrial nodes
      - Upstream/downstream industrial nodes for each exposure
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")

    company_name = await _get_company_name(pool, company_id)

    # 1. Fetch exposures from PG
    async with pool.acquire() as conn:
        exposure_rows = await conn.fetch(
            """
            SELECT node_id, activity_type, weight, role
            FROM company_node_exposures
            WHERE company_id = $1 AND status IN ('ACTIVE', 'PENDING')
            ORDER BY weight DESC
            """,
            company_id,
        )

    if not exposure_rows:
        return {
            "company_id": company_id,
            "company_name": company_name,
            "domain": "cross",
            "exposures": [],
        }

    exposed_node_ids = [r["node_id"] for r in exposure_rows]
    node_name_map = await _get_node_names(exposed_node_ids)

    # 2. Query upstream/downstream for each node from Neo4j
    driver = get_async_driver()
    exposures = []

    for exp in exposure_rows:
        node_id = exp["node_id"]

        async with driver.session() as session:
            up_result = await session.run(
                """
                MATCH (up:IndustrialNode)-[:INDUSTRIAL_FLOW]->(n:IndustrialNode {node_id: $node_id})
                RETURN up.node_id AS node_id
                """,
                node_id=node_id,
            )
            upstream_ids = [r["node_id"] async for r in up_result]

            down_result = await session.run(
                """
                MATCH (n:IndustrialNode {node_id: $node_id})-[:INDUSTRIAL_FLOW]->(down:IndustrialNode)
                RETURN down.node_id AS node_id
                """,
                node_id=node_id,
            )
            downstream_ids = [r["node_id"] async for r in down_result]

        up_name_map = await _get_node_names(upstream_ids)
        down_name_map = await _get_node_names(downstream_ids)

        exposures.append({
            "node_id": node_id,
            "node_name": node_name_map.get(node_id, node_id),
            "activity_type": exp["activity_type"],
            "weight": float(exp["weight"]) if exp["weight"] is not None else 1.0,
            "role": exp["role"],
            "domain": "industrial",
            "upstream": [
                {"node_id": nid, "node_name": up_name_map.get(nid, nid), "domain": "industrial"}
                for nid in upstream_ids
            ],
            "downstream": [
                {"node_id": nid, "node_name": down_name_map.get(nid, nid), "domain": "industrial"}
                for nid in downstream_ids
            ],
        })

    return {
        "company_id": company_id,
        "company_name": company_name,
        "domain": "cross",
        "exposures": exposures,
    }


# ---------------------------------------------------------------------------
# 2. Industrial Node → Ecosystem (companies + factual relations)
# ---------------------------------------------------------------------------

@router.get("/nodes/{node_id}/ecosystem")
async def explore_node_ecosystem(
    node_id: str,
    include_factual: bool = Query(True, description="Include factual graph relations"),
):
    """
    Starting from an IndustrialNode, find:
      - Companies exposing this node
      - Their related persons and companies in the Factual Graph
      - Upstream/downstream companies (companies exposing adjacent nodes)
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")

    driver = get_async_driver()

    # Node name
    node_name_map = await _get_node_names([node_id])
    node_name = node_name_map.get(node_id, node_id)

    # 1. Directly exposing companies
    async with pool.acquire() as conn:
        exposure_rows = await conn.fetch(
            """
            SELECT e.company_id, c.name_zh, e.activity_type, e.weight, e.role
            FROM company_node_exposures e
            JOIN companies c ON e.company_id = c.company_id
            WHERE e.node_id = $1 AND e.status IN ('ACTIVE', 'PENDING')
            ORDER BY e.weight DESC, c.name_zh
            """,
            node_id,
        )

    exposing_companies = []
    company_ids = [r["company_id"] for r in exposure_rows]

    for row in exposure_rows:
        cid = row["company_id"]
        company_data = {
            "company_id": cid,
            "company_name": row["name_zh"] or cid,
            "activity_type": row["activity_type"],
            "weight": float(row["weight"]) if row["weight"] is not None else 1.0,
            "role": row["role"],
            "domain": "factual",
            "related_persons": [],
            "related_companies": [],
        }

        if include_factual:
            # Related persons
            persons, _ = await factual_storage.list_relations(
                relation_domain="person_company",
                to_entity_id=cid,
                page=1,
                page_size=50,
            )
            company_data["related_persons"] = [
                {
                    "person_id": p.person_id if hasattr(p, "person_id") else p.from_entity_id,
                    "name": "",  # Will be populated below if needed
                    "relation_type": p.relation_type.value if hasattr(p.relation_type, "value") else p.relation_type,
                    "subtype": p.subtype if hasattr(p, "subtype") else None,
                    "domain": "factual",
                }
                for p in persons
            ]

            # Related companies (company_company relations)
            c_rels, _ = await factual_storage.list_relations(
                relation_domain="company_company",
                from_entity_id=cid,
                page=1,
                page_size=50,
            )
            c_rels += (await factual_storage.list_relations(
                relation_domain="company_company",
                to_entity_id=cid,
                page=1,
                page_size=50,
            ))[0]

            company_data["related_companies"] = [
                {
                    "company_id": r.from_company_id if hasattr(r, "from_company_id") else r.to_company_id,
                    "relation_type": r.relation_type.value if hasattr(r.relation_type, "value") else r.relation_type,
                    "domain": "factual",
                }
                for r in c_rels
            ]

        exposing_companies.append(company_data)

    # 2. Upstream/downstream companies via Industrial Graph
    upstream_companies = []
    downstream_companies = []

    async with driver.session() as session:
        up_result = await session.run(
            """
            MATCH (up:IndustrialNode)-[:INDUSTRIAL_FLOW]->(n:IndustrialNode {node_id: $node_id})
            RETURN up.node_id AS node_id
            """,
            node_id=node_id,
        )
        up_nodes = [r["node_id"] async for r in up_result]

        down_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})-[:INDUSTRIAL_FLOW]->(down:IndustrialNode)
            RETURN down.node_id AS node_id
            """,
            node_id=node_id,
        )
        down_nodes = [r["node_id"] async for r in down_result]

    if up_nodes:
        async with pool.acquire() as conn:
            up_company_rows = await conn.fetch(
                """
                SELECT DISTINCT e.company_id, c.name_zh, e.node_id, e.activity_type, e.weight
                FROM company_node_exposures e
                JOIN companies c ON e.company_id = c.company_id
                WHERE e.node_id = ANY($1) AND e.status IN ('ACTIVE', 'PENDING')
                ORDER BY e.weight DESC, c.name_zh
                """,
                up_nodes,
            )
        upstream_companies = [
            {
                "company_id": r["company_id"],
                "company_name": r["name_zh"] or r["company_id"],
                "via_node_id": r["node_id"],
                "activity_type": r["activity_type"],
                "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
                "domain": "factual",
            }
            for r in up_company_rows
        ]

    if down_nodes:
        async with pool.acquire() as conn:
            down_company_rows = await conn.fetch(
                """
                SELECT DISTINCT e.company_id, c.name_zh, e.node_id, e.activity_type, e.weight
                FROM company_node_exposures e
                JOIN companies c ON e.company_id = c.company_id
                WHERE e.node_id = ANY($1) AND e.status IN ('ACTIVE', 'PENDING')
                ORDER BY e.weight DESC, c.name_zh
                """,
                down_nodes,
            )
        downstream_companies = [
            {
                "company_id": r["company_id"],
                "company_name": r["name_zh"] or r["company_id"],
                "via_node_id": r["node_id"],
                "activity_type": r["activity_type"],
                "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
                "domain": "factual",
            }
            for r in down_company_rows
        ]

    return {
        "node_id": node_id,
        "node_name": node_name,
        "domain": "cross",
        "exposing_companies": exposing_companies,
        "upstream_companies": upstream_companies,
        "downstream_companies": downstream_companies,
    }


# ---------------------------------------------------------------------------
# 3. Person → Industrial Footprint
# ---------------------------------------------------------------------------

@router.get("/persons/{person_id}/industrial-footprint")
async def explore_person_industrial_footprint(person_id: str):
    """
    Starting from a Person (Factual Graph), find:
      - Related companies (via factual relations)
      - Each company's exposed industrial nodes
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")

    # 1. Get person info
    person = await factual_storage.get_person(person_id)
    person_name = person.name_zh if person else person_id

    # 2. Get related companies from PG (via factual_relations)
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT fr.from_entity_id AS company_id, fr.relation_type, fr.subtype,
                   fr.equity_ratio, fr.start_date, fr.end_date, fr.is_history
            FROM factual_relations fr
            WHERE fr.relation_domain = 'person_company'
              AND fr.from_entity_id = $1
              AND fr.status IN ('ACTIVE', 'PENDING')
            ORDER BY fr.created_at DESC
            """,
            person_id,
        )

    if not rows:
        return {
            "person_id": person_id,
            "person_name": person_name,
            "domain": "cross",
            "companies": [],
        }

    company_ids = [r["company_id"] for r in rows]
    company_relation_map = {r["company_id"]: r for r in rows}

    # 3. Fetch company names
    async with pool.acquire() as conn:
        name_rows = await conn.fetch(
            "SELECT company_id, name_zh FROM companies WHERE company_id = ANY($1)",
            company_ids,
        )
    name_map = {r["company_id"]: r["name_zh"] or r["company_id"] for r in name_rows}

    # 4. Fetch exposures for all related companies
    async with pool.acquire() as conn:
        exp_rows = await conn.fetch(
            """
            SELECT company_id, node_id, activity_type, weight, role
            FROM company_node_exposures
            WHERE company_id = ANY($1) AND status IN ('ACTIVE', 'PENDING')
            ORDER BY weight DESC
            """,
            company_ids,
        )

    # Group exposures by company
    exposure_map = {}
    for r in exp_rows:
        cid = r["company_id"]
        if cid not in exposure_map:
            exposure_map[cid] = []
        exposure_map[cid].append(r)

    # Node names
    all_node_ids = list({r["node_id"] for r in exp_rows})
    node_name_map = await _get_node_names(all_node_ids)

    companies = []
    for cid in company_ids:
        rel = company_relation_map[cid]
        exposures = []
        for exp in exposure_map.get(cid, []):
            exposures.append({
                "node_id": exp["node_id"],
                "node_name": node_name_map.get(exp["node_id"], exp["node_id"]),
                "activity_type": exp["activity_type"],
                "weight": float(exp["weight"]) if exp["weight"] is not None else 1.0,
                "role": exp["role"],
                "domain": "industrial",
            })

        companies.append({
            "company_id": cid,
            "company_name": name_map.get(cid, cid),
            "relation_type": rel["relation_type"],
            "subtype": rel["subtype"],
            "equity_ratio": rel["equity_ratio"],
            "is_history": rel["is_history"],
            "domain": "factual",
            "exposures": exposures,
        })

    return {
        "person_id": person_id,
        "person_name": person_name,
        "domain": "cross",
        "companies": companies,
    }


# ---------------------------------------------------------------------------
# 4. Company → Full Cross-Domain Context
# ---------------------------------------------------------------------------

@router.get("/companies/{company_id}/full-context")
async def explore_company_full_context(company_id: str):
    """
    Return the complete cross-domain context for a company:
      - Factual Graph: related persons and companies
      - Industrial Graph: exposed nodes + upstream/downstream
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")

    company_name = await _get_company_name(pool, company_id)

    # Factual relations
    related_persons = []
    p_rels, _ = await factual_storage.list_relations(
        relation_domain="person_company",
        to_entity_id=company_id,
        page=1,
        page_size=100,
    )
    for pr in p_rels:
        pid = pr.person_id if hasattr(pr, "person_id") else pr.from_entity_id
        person = await factual_storage.get_person(pid)
        related_persons.append({
            "person_id": pid,
            "person_name": person.name_zh if person else pid,
            "relation_type": pr.relation_type.value if hasattr(pr.relation_type, "value") else pr.relation_type,
            "subtype": pr.subtype if hasattr(pr, "subtype") else None,
            "equity_ratio": pr.equity_ratio if hasattr(pr, "equity_ratio") else None,
            "domain": "factual",
        })

    related_companies = []
    cc_from, _ = await factual_storage.list_relations(
        relation_domain="company_company",
        from_entity_id=company_id,
        page=1,
        page_size=100,
    )
    cc_to, _ = await factual_storage.list_relations(
        relation_domain="company_company",
        to_entity_id=company_id,
        page=1,
        page_size=100,
    )
    for cr in cc_from + cc_to:
        cid = cr.to_company_id if hasattr(cr, "to_company_id") else cr.from_company_id
        related_companies.append({
            "company_id": cid,
            "company_name": await _get_company_name(pool, cid),
            "relation_type": cr.relation_type.value if hasattr(cr.relation_type, "value") else cr.relation_type,
            "direction": "outgoing" if (hasattr(cr, "from_company_id") and cr.from_company_id == company_id) else "incoming",
            "domain": "factual",
        })

    # Industrial context
    industrial = await explore_company_industrial_context(company_id)

    return {
        "company_id": company_id,
        "company_name": company_name,
        "domain": "cross",
        "factual_graph": {
            "related_persons": related_persons,
            "related_companies": related_companies,
        },
        "industrial_graph": {
            "exposures": industrial.get("exposures", []),
        },
    }
