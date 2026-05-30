"""
================================================================================
 DOMAIN: COMPANY VIEW — Neo4j Storage Layer
================================================================================
全局公司关系网络在 Neo4j 中的存储与查询。

节点标签: Company
关系类型: INFERRED_UPSTREAM

与产业图（IndustrialNode / INDUSTRIAL_FLOW）完全隔离。
================================================================================
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool


# ---------------------------------------------------------------------------
# Company Node Sync
# ---------------------------------------------------------------------------

async def sync_companies_to_neo4j() -> int:
    """
    Sync all ACTIVE companies from PostgreSQL into Neo4j as :Company nodes.
    Uses MERGE to avoid duplicates. Returns the number of companies synced.
    """
    pool = await get_postgres_pool()
    if pool is None:
        return 0

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT company_id, name_zh, name_en, company_type, status
            FROM companies
            WHERE status = 'ACTIVE'
            ORDER BY company_id
            """
        )

    if not rows:
        return 0

    driver = get_async_driver()
    companies = [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or "",
            "name_en": r["name_en"] or "",
            "company_type": r["company_type"] or "unknown",
            "status": r["status"] or "ACTIVE",
        }
        for r in rows
    ]

    async with driver.session() as session:
        result = await session.run(
            """
            UNWIND $companies AS c
            MERGE (co:Company {company_id: c.company_id})
            ON CREATE SET
                co.name_zh = c.name_zh,
                co.name_en = c.name_en,
                co.company_type = c.company_type,
                co.status = c.status,
                co.created_at = datetime()
            ON MATCH SET
                co.name_zh = c.name_zh,
                co.name_en = c.name_en,
                co.company_type = c.company_type,
                co.status = c.status,
                co.updated_at = datetime()
            RETURN count(co) AS cnt
            """,
            companies=companies,
        )
        record = await result.single()
        return record["cnt"] if record else 0


# ---------------------------------------------------------------------------
# Relation Management
# ---------------------------------------------------------------------------

async def clear_inferred_relations() -> int:
    """
    Delete all INFERRED_UPSTREAM relationships in the Company view.
    Returns the number of relationships deleted.
    """
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH ()-[r:INFERRED_UPSTREAM]->()
            WITH r LIMIT 10000
            DELETE r
            RETURN count(r) AS cnt
            """
        )
        record = await result.single()
        return record["cnt"] if record else 0


async def batch_create_inferred_relations(
    relations: List[Tuple[str, str, int, str, Optional[str]]],
) -> int:
    """
    Batch-create INFERRED_UPSTREAM relationships.

    Args:
        relations: List of (from_company_id, to_company_id, path_count, relation_type, relation_subtype)

    Returns:
        Number of relationships created.
    """
    if not relations:
        return 0

    driver = get_async_driver()

    # Chunk to avoid overly large UNWIND batches
    BATCH_SIZE = 500
    total_created = 0

    for i in range(0, len(relations), BATCH_SIZE):
        chunk = relations[i : i + BATCH_SIZE]
        batch = [
            {
                "from_id": f_id,
                "to_id": t_id,
                "path_count": p_count,
                "strength": min(1.0, max(0.1, min(1.0, p_count * 0.2))),
                "relation_type": r_type,
                "relation_subtype": r_subtype or "",
            }
            for f_id, t_id, p_count, r_type, r_subtype in chunk
        ]

        async with driver.session() as session:
            result = await session.run(
                """
                UNWIND $batch AS rel
                MATCH (a:Company {company_id: rel.from_id}), (b:Company {company_id: rel.to_id})
                CREATE (a)-[:INFERRED_UPSTREAM {
                    path_count: rel.path_count,
                    strength: rel.strength,
                    confidence: 'MEDIUM',
                    derived_at: datetime(),
                    relation_type: rel.relation_type,
                    relation_subtype: rel.relation_subtype
                }]->(b)
                RETURN count(*) AS cnt
                """,
                batch=batch,
            )
            record = await result.single()
            total_created += record["cnt"] if record else 0

    return total_created


# ---------------------------------------------------------------------------
# Network Queries
# ---------------------------------------------------------------------------

async def get_company_network() -> dict:
    """
    Return the global company relationship network from Neo4j.
    Nodes = all Company nodes, Edges = all INFERRED_UPSTREAM relationships.
    """
    driver = get_async_driver()

    async with driver.session() as session:
        node_result = await session.run(
            """
            MATCH (c:Company)
            RETURN c.company_id AS company_id,
                   c.name_zh AS name_zh,
                   c.company_type AS company_type,
                   c.status AS status
            ORDER BY c.company_id
            """
        )
        node_records = await node_result.data()

        edge_result = await session.run(
            """
            MATCH (a:Company)-[r:INFERRED_UPSTREAM]->(b:Company)
            RETURN a.company_id AS from_company_id,
                   b.company_id AS to_company_id,
                   r.path_count AS path_count,
                   r.strength AS strength,
                   r.confidence AS confidence,
                   r.relation_type AS relation_type,
                   r.relation_subtype AS relation_subtype
            ORDER BY a.company_id, b.company_id
            """
        )
        edge_records = await edge_result.data()

    nodes = [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or r["company_id"],
            "company_type": r["company_type"] or "unknown",
            "status": r["status"] or "ACTIVE",
        }
        for r in node_records
    ]

    edges = [
        {
            "from_company_id": r["from_company_id"],
            "to_company_id": r["to_company_id"],
            "path_count": r["path_count"] or 1,
            "strength": float(r["strength"] or 1.0),
            "confidence": r["confidence"] or "MEDIUM",
            "relation_type": r.get("relation_type") or "inferred_industrial",
            "relation_subtype": r.get("relation_subtype") or "upstream_of",
        }
        for r in edge_records
    ]

    return {"nodes": nodes, "edges": edges}


async def get_upstream_companies(company_id: str) -> List[dict]:
    """
    Return direct upstream companies of the given company.
    Upstream = companies that have INFERRED_UPSTREAM pointing TO this company.
    """
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (upstream:Company)-[r:INFERRED_UPSTREAM]->(target:Company {company_id: $company_id})
            RETURN upstream.company_id AS company_id,
                   upstream.name_zh AS name_zh,
                   upstream.company_type AS company_type,
                   r.path_count AS path_count,
                   r.strength AS strength,
                   r.relation_type AS relation_type,
                   r.relation_subtype AS relation_subtype
            ORDER BY r.strength DESC, upstream.name_zh
            """,
            company_id=company_id,
        )
        records = await result.data()

    return [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or r["company_id"],
            "company_type": r["company_type"] or "unknown",
            "path_count": r["path_count"] or 1,
            "strength": float(r["strength"] or 1.0),
            "relation_type": r.get("relation_type") or "inferred_industrial",
            "relation_subtype": r.get("relation_subtype") or "upstream_of",
        }
        for r in records
    ]


async def get_inferred_paths(
    from_company_id: str,
    to_company_id: str,
    from_node_ids: List[str],
    to_node_ids: List[str],
) -> dict:
    """
    Return the industrial graph paths that support an inferred relation
    between two companies.

    Queries Neo4j for direct INDUSTRIAL_FLOW edges from any node exposed
    by from_company to any node exposed by to_company.
    """
    driver = get_async_driver()

    async with driver.session() as session:
        # Get company names
        name_result = await session.run(
            """
            MATCH (a:Company {company_id: $from_id}), (b:Company {company_id: $to_id})
            RETURN a.name_zh AS from_name, b.name_zh AS to_name
            """,
            from_id=from_company_id,
            to_id=to_company_id,
        )
        name_record = await name_result.single()

        # Get industrial flow paths
        path_result = await session.run(
            """
            MATCH (src:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(tgt:IndustrialNode)
            WHERE src.node_id IN $from_nodes AND tgt.node_id IN $to_nodes
            RETURN src.node_id AS from_node_id,
                   src.canonical_name_zh AS from_node_name,
                   tgt.node_id AS to_node_id,
                   tgt.canonical_name_zh AS to_node_name,
                   r.edge_type AS edge_type
            ORDER BY src.canonical_name_zh, tgt.canonical_name_zh
            """,
            from_nodes=from_node_ids,
            to_nodes=to_node_ids,
        )
        path_records = await path_result.data()

    return {
        "from_company_id": from_company_id,
        "to_company_id": to_company_id,
        "from_company_name": name_record["from_name"] if name_record else from_company_id,
        "to_company_name": name_record["to_name"] if name_record else to_company_id,
        "relation_type": "inferred_industrial",
        "total_paths": len(path_records),
        "paths": [
            {
                "from_node": {
                    "node_id": r["from_node_id"],
                    "canonical_name_zh": r["from_node_name"] or r["from_node_id"],
                },
                "to_node": {
                    "node_id": r["to_node_id"],
                    "canonical_name_zh": r["to_node_name"] or r["to_node_id"],
                },
                "edge_type": r["edge_type"] or "industrial_flow",
            }
            for r in path_records
        ],
    }


async def get_downstream_companies(company_id: str) -> List[dict]:
    """
    Return direct downstream companies of the given company.
    Downstream = companies that this company has INFERRED_UPSTREAM pointing TO.
    """
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (source:Company {company_id: $company_id})-[r:INFERRED_UPSTREAM]->(downstream:Company)
            RETURN downstream.company_id AS company_id,
                   downstream.name_zh AS name_zh,
                   downstream.company_type AS company_type,
                   r.path_count AS path_count,
                   r.strength AS strength,
                   r.relation_type AS relation_type,
                   r.relation_subtype AS relation_subtype
            ORDER BY r.strength DESC, downstream.name_zh
            """,
            company_id=company_id,
        )
        records = await result.data()

    return [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or r["company_id"],
            "company_type": r["company_type"] or "unknown",
            "path_count": r["path_count"] or 1,
            "strength": float(r["strength"] or 1.0),
            "relation_type": r.get("relation_type") or "inferred_industrial",
            "relation_subtype": r.get("relation_subtype") or "upstream_of",
        }
        for r in records
    ]
