"""
================================================================================
 DOMAIN: COMPANY SUBGRAPH (公司子图)
================================================================================
公司子图计算、版本管理、关系推导服务。

本文件属于 Company Subgraph Domain，与核心产业图域隔离。
================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import List, Optional, Tuple

from app.database_postgres import get_postgres_pool
from app.database import get_async_driver
from app.models.company_subgraph_schema import (
    CompanySubgraph,
    CompanySubgraphNode,
    CompanySubgraphEdge,
    CompanySubgraphRelation,
    SubgraphRelationType,
    SubgraphRelationSubtype,
)
from app.models.schemas import Evidence, Confidence, RecordStatus, EDGE_TYPE_LABELS
from app.services import company_storage
from app.services.computation_jobs import (
    mark_job_running,
    update_job_progress,
    complete_job,
    fail_job,
)
from app.services.neo4j_storage import _to_datetime, _evidence_from_db


# ---------------------------------------------------------------------------
# Subgraph CRUD
# ---------------------------------------------------------------------------

async def create_subgraph_shell(
    subgraph_id: str,
    company_id: str,
    version_name: Optional[str] = None,
    description: Optional[str] = None,
) -> CompanySubgraph:
    """Create an empty subgraph version shell."""
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO company_subgraphs
            (subgraph_id, company_id, version_name, description, status)
            VALUES ($1, $2, $3, $4, 'ACTIVE')
            """,
            subgraph_id, company_id, version_name, description,
        )

    return await get_subgraph(subgraph_id)


async def get_subgraph(subgraph_id: str, include_details: bool = True) -> Optional[CompanySubgraph]:
    """Fetch a subgraph version. Optionally include nodes/edges/relations."""
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT subgraph_id, subgraph_uuid, company_id, version_name, description,
                   status, nodes_summary, edges_summary, relations_summary,
                   created_at, updated_at
            FROM company_subgraphs
            WHERE subgraph_id = $1
            """,
            subgraph_id,
        )

    if row is None:
        return None

    def _parse_jsonb(val):
        if isinstance(val, str):
            return json.loads(val)
        return val

    subgraph = CompanySubgraph(
        subgraph_id=row["subgraph_id"],
        subgraph_uuid=row["subgraph_uuid"],
        company_id=row["company_id"],
        version_name=row["version_name"],
        description=row["description"],
        status=RecordStatus(row["status"]),
        nodes_summary=_parse_jsonb(row["nodes_summary"]),
        edges_summary=_parse_jsonb(row["edges_summary"]),
        relations_summary=_parse_jsonb(row["relations_summary"]),
        created_at=_to_datetime(row["created_at"]),
        updated_at=_to_datetime(row["updated_at"]),
    )

    if include_details:
        subgraph.nodes = await _get_subgraph_nodes(subgraph_id)
        subgraph.edges = await _get_subgraph_edges(subgraph_id)
        subgraph.relations = await _get_subgraph_relations(subgraph_id)

    return subgraph


async def _get_subgraph_nodes(subgraph_id: str) -> List[CompanySubgraphNode]:
    pool = await get_postgres_pool()
    if pool is None:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT node_id, canonical_name_zh, entity_type, activity_type,
                   weight, role, exposure_confidence
            FROM company_subgraph_nodes
            WHERE subgraph_id = $1
            ORDER BY id
            """,
            subgraph_id,
        )

    return [
        CompanySubgraphNode(
            node_id=r["node_id"],
            canonical_name_zh=r["canonical_name_zh"] or "",
            entity_type=r["entity_type"] or "unknown",
            activity_type=r["activity_type"] or "unknown",
            weight=float(r["weight"] or 1.0),
            role=r["role"],
            exposure_confidence=r["exposure_confidence"],
        )
        for r in rows
    ]


async def _get_subgraph_edges(subgraph_id: str) -> List[CompanySubgraphEdge]:
    pool = await get_postgres_pool()
    if pool is None:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT edge_id, from_node, to_node, edge_namespace, edge_type,
                   edge_type_label, description, confidence
            FROM company_subgraph_edges
            WHERE subgraph_id = $1
            ORDER BY id
            """,
            subgraph_id,
        )

    return [
        CompanySubgraphEdge(
            edge_id=r["edge_id"],
            from_node=r["from_node"],
            to_node=r["to_node"],
            edge_namespace=r["edge_namespace"] or "industrial_flow",
            edge_type=r["edge_type"] or "material_flow",
            edge_type_label=r["edge_type_label"],
            description=r["description"],
            confidence=r["confidence"],
        )
        for r in rows
    ]


async def _get_subgraph_relations(subgraph_id: str) -> List[CompanySubgraphRelation]:
    pool = await get_postgres_pool()
    if pool is None:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, from_company_id, to_company_id, relation_type, relation_subtype,
                   strength, confidence, evidence, notes
            FROM company_subgraph_relations
            WHERE subgraph_id = $1
            ORDER BY id
            """,
            subgraph_id,
        )

    return [
        CompanySubgraphRelation(
            relation_id=r["id"],
            from_company_id=r["from_company_id"],
            to_company_id=r["to_company_id"],
            relation_type=SubgraphRelationType(r["relation_type"]),
            relation_subtype=SubgraphRelationSubtype(r["relation_subtype"]) if r["relation_subtype"] else None,
            strength=float(r["strength"] or 1.0),
            confidence=Confidence(r["confidence"]),
            evidence=_evidence_from_db(r["evidence"]) if r["evidence"] else [],
            notes=r["notes"],
        )
        for r in rows
    ]


async def list_subgraphs(
    company_id: str,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[CompanySubgraph], int]:
    """List subgraph versions for a company (newest first)."""
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            "SELECT COUNT(*) AS total FROM company_subgraphs WHERE company_id = $1",
            company_id,
        )
        total = total_row["total"] if total_row else 0

        rows = await conn.fetch(
            """
            SELECT subgraph_id, subgraph_uuid, company_id, version_name, description,
                   status, nodes_summary, edges_summary, relations_summary,
                   created_at, updated_at
            FROM company_subgraphs
            WHERE company_id = $1
            ORDER BY created_at DESC
            OFFSET $2 LIMIT $3
            """,
            company_id, skip, limit,
        )

    def _parse_jsonb(val):
        if isinstance(val, str):
            return json.loads(val)
        return val

    items = [
        CompanySubgraph(
            subgraph_id=r["subgraph_id"],
            subgraph_uuid=r["subgraph_uuid"],
            company_id=r["company_id"],
            version_name=r["version_name"],
            description=r["description"],
            status=RecordStatus(r["status"]),
            nodes_summary=_parse_jsonb(r["nodes_summary"]),
            edges_summary=_parse_jsonb(r["edges_summary"]),
            relations_summary=_parse_jsonb(r["relations_summary"]),
            created_at=_to_datetime(r["created_at"]),
            updated_at=_to_datetime(r["updated_at"]),
        )
        for r in rows
    ]

    return items, total


async def delete_subgraph(subgraph_id: str) -> bool:
    """Delete a subgraph version and all its detail records."""
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM company_subgraphs WHERE subgraph_id = $1",
            subgraph_id,
        )
    # CASCADE will delete nodes/edges/relations automatically
    return "DELETE 1" in result


# ---------------------------------------------------------------------------
# Subgraph Computation (Async Background Task)
# ---------------------------------------------------------------------------

async def compute_company_subgraph(
    company_id: str,
    job_id: str,
    version_name: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """
    Compute and cache a company subgraph version.
    This function is designed to run inside FastAPI BackgroundTasks.
    Returns the new subgraph_id.
    """
    try:
        await mark_job_running(job_id)

        # Generate subgraph ID
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        subgraph_id = f"{company_id}_{timestamp}"

        # Create shell
        await create_subgraph_shell(subgraph_id, company_id, version_name, description)

        # --- Phase A: Project nodes ---
        exposures = await _get_company_exposures(company_id)
        node_ids = [e["node_id"] for e in exposures]

        if not node_ids:
            await _update_summary(subgraph_id, 0, 0, 0)
            await complete_job(job_id, {"subgraph_id": subgraph_id, "nodes": 0, "edges": 0, "relations": 0})
            return subgraph_id

        # Fetch node properties from Neo4j
        node_props = await _fetch_node_properties(node_ids)

        pool = await get_postgres_pool()
        async with pool.acquire() as conn:
            for exp in exposures:
                props = node_props.get(exp["node_id"], {})
                await conn.execute(
                    """
                    INSERT INTO company_subgraph_nodes
                    (subgraph_id, node_id, canonical_name_zh, entity_type, activity_type, weight, role, exposure_confidence)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    subgraph_id,
                    exp["node_id"],
                    props.get("canonical_name_zh", ""),
                    props.get("entity_type", "unknown"),
                    exp["activity_type"],
                    exp["weight"],
                    exp["role"],
                    exp["confidence"],
                )

        # --- Phase B: Project edges (industrial_flow between exposed nodes) ---
        edges = await _fetch_industrial_flow_edges(node_ids)
        async with pool.acquire() as conn:
            for edge in edges:
                await conn.execute(
                    """
                    INSERT INTO company_subgraph_edges
                    (subgraph_id, edge_id, from_node, to_node, edge_namespace, edge_type, edge_type_label, description, confidence)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """,
                    subgraph_id,
                    edge["edge_id"],
                    edge["from_node"],
                    edge["to_node"],
                    edge["edge_namespace"],
                    edge["edge_type"],
                    edge.get("edge_type_label"),
                    edge.get("description"),
                    edge.get("confidence"),
                )

        # --- Phase C: Derive similarity_peer relations ---
        peer_relations = await _derive_similarity_peer(company_id, node_ids)
        async with pool.acquire() as conn:
            for rel in peer_relations:
                await conn.execute(
                    """
                    INSERT INTO company_subgraph_relations
                    (subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype, strength, confidence, evidence, notes)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    ON CONFLICT (subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype) DO NOTHING
                    """,
                    subgraph_id,
                    rel.from_company_id,
                    rel.to_company_id,
                    rel.relation_type.value,
                    rel.relation_subtype.value if rel.relation_subtype else None,
                    rel.strength,
                    rel.confidence.value,
                    json.dumps([e.model_dump() for e in rel.evidence]) if rel.evidence else "[]",
                    rel.notes,
                )

        node_count = len(node_ids)
        edge_count = len(edges)
        relation_count = len(peer_relations)

        await _update_summary(subgraph_id, node_count, edge_count, relation_count)
        await complete_job(job_id, {
            "subgraph_id": subgraph_id,
            "nodes": node_count,
            "edges": edge_count,
            "relations": relation_count,
        })

        return subgraph_id

    except Exception as exc:
        await fail_job(job_id, str(exc))
        raise


async def _get_company_exposures(company_id: str) -> List[dict]:
    """Fetch exposures from PostgreSQL."""
    pool = await get_postgres_pool()
    if pool is None:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT node_id, activity_type, weight, role, confidence
            FROM company_node_exposures
            WHERE company_id = $1 AND status = 'ACTIVE'
            ORDER BY weight DESC
            """,
            company_id,
        )

    return [
        {
            "node_id": r["node_id"],
            "activity_type": r["activity_type"],
            "weight": float(r["weight"] or 1.0),
            "role": r["role"],
            "confidence": r["confidence"],
        }
        for r in rows
    ]


async def _fetch_node_properties(node_ids: List[str]) -> dict:
    """Fetch node canonical_name_zh and entity_type from Neo4j."""
    if not node_ids:
        return {}

    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n.node_id AS node_id, n.canonical_name_zh AS canonical_name_zh, n.entity_type AS entity_type
            """,
            node_ids=node_ids,
        )
        records = await result.data()

    return {
        r["node_id"]: {
            "canonical_name_zh": r.get("canonical_name_zh", ""),
            "entity_type": r.get("entity_type", "unknown"),
        }
        for r in records
    }


async def _fetch_industrial_flow_edges(node_ids: List[str]) -> List[dict]:
    """Fetch industrial_flow edges between the given nodes from Neo4j."""
    if not node_ids:
        return []

    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE a.node_id IN $node_ids AND b.node_id IN $node_ids
            RETURN r.edge_id AS edge_id, a.node_id AS from_node, b.node_id AS to_node,
                   r.edge_namespace AS edge_namespace, r.edge_type AS edge_type,
                   r.description AS description, r.confidence AS confidence
            """,
            node_ids=node_ids,
        )
        records = await result.data()

    return [
        {
            "edge_id": r["edge_id"],
            "from_node": r["from_node"],
            "to_node": r["to_node"],
            "edge_namespace": r.get("edge_namespace", "industrial_flow"),
            "edge_type": r["edge_type"],
            "edge_type_label": EDGE_TYPE_LABELS.get(r["edge_type"], r["edge_type"]),
            "description": r.get("description", ""),
            "confidence": r.get("confidence", "LOW"),
        }
        for r in records
    ]


async def _derive_similarity_peer(company_id: str, node_ids: List[str]) -> List[CompanySubgraphRelation]:
    """
    Derive similarity_peer relations:
    Other companies that expose the same node with the same activity_type.
    """
    if not node_ids:
        return []

    pool = await get_postgres_pool()
    if pool is None:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT DISTINCT a.company_id AS peer_company_id
            FROM company_node_exposures a
            JOIN company_node_exposures b
              ON a.node_id = b.node_id AND a.activity_type = b.activity_type
            WHERE b.company_id = $1
              AND a.company_id != $1
              AND a.status = 'ACTIVE' AND b.status = 'ACTIVE'
            """,
            company_id,
        )

    relations = []
    for r in rows:
        peer_id = r["peer_company_id"]
        relations.append(CompanySubgraphRelation(
            from_company_id=company_id,
            to_company_id=peer_id,
            relation_type=SubgraphRelationType.SIMILARITY_PEER,
            relation_subtype=SubgraphRelationSubtype.PEER,
            strength=1.0,
            confidence=Confidence.HIGH,
        ))

    return relations


async def _update_summary(subgraph_id: str, node_count: int, edge_count: int, relation_count: int) -> None:
    """Update summary JSONB fields on the subgraph record."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        # Count by entity_type
        node_type_rows = await conn.fetch(
            """
            SELECT entity_type, COUNT(*) AS cnt
            FROM company_subgraph_nodes
            WHERE subgraph_id = $1
            GROUP BY entity_type
            """,
            subgraph_id,
        )
        nodes_summary = {
            "total": node_count,
            "by_entity_type": {r["entity_type"]: r["cnt"] for r in node_type_rows},
        }

        # Count by edge_namespace
        edge_ns_rows = await conn.fetch(
            """
            SELECT edge_namespace, COUNT(*) AS cnt
            FROM company_subgraph_edges
            WHERE subgraph_id = $1
            GROUP BY edge_namespace
            """,
            subgraph_id,
        )
        edges_summary = {
            "total": edge_count,
            "by_edge_namespace": {r["edge_namespace"]: r["cnt"] for r in edge_ns_rows},
        }

        # Count by relation_type
        rel_type_rows = await conn.fetch(
            """
            SELECT relation_type, COUNT(*) AS cnt
            FROM company_subgraph_relations
            WHERE subgraph_id = $1
            GROUP BY relation_type
            """,
            subgraph_id,
        )
        relations_summary = {
            "total": relation_count,
            "by_relation_type": {r["relation_type"]: r["cnt"] for r in rel_type_rows},
        }

        await conn.execute(
            """
            UPDATE company_subgraphs
            SET nodes_summary = $2, edges_summary = $3, relations_summary = $4, updated_at = NOW()
            WHERE subgraph_id = $1
            """,
            subgraph_id,
            json.dumps(nodes_summary),
            json.dumps(edges_summary),
            json.dumps(relations_summary),
        )


# ---------------------------------------------------------------------------
# Subgraph Relation CRUD
# ---------------------------------------------------------------------------

async def add_subgraph_relation(
    subgraph_id: str,
    data: CompanySubgraphRelation,
) -> CompanySubgraphRelation:
    """Add a relation to a subgraph (typically evidenced_business)."""
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO company_subgraph_relations
            (subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype, strength, confidence, evidence, notes)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
            """,
            subgraph_id,
            data.from_company_id,
            data.to_company_id,
            data.relation_type.value,
            data.relation_subtype.value if data.relation_subtype else None,
            data.strength,
            data.confidence.value,
            json.dumps([e.model_dump() for e in data.evidence]) if data.evidence else "[]",
            data.notes,
        )

    data.relation_id = row["id"]
    return data


async def delete_subgraph_relation(subgraph_id: str, relation_id: int) -> bool:
    """Delete a relation from a subgraph."""
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM company_subgraph_relations
            WHERE subgraph_id = $1 AND id = $2
            """,
            subgraph_id, relation_id,
        )

    return "DELETE 1" in result


# ---------------------------------------------------------------------------
# Full-Graph Relation Inference (Async Background Task)
# ---------------------------------------------------------------------------

async def compute_all_company_relations(job_id: str) -> None:
    """
    Compute inferred_industrial relations across ALL companies.
    Writes results into the most recent ACTIVE subgraph of each involved company.
    This is designed to run inside FastAPI BackgroundTasks.
    """
    try:
        await mark_job_running(job_id)

        pool = await get_postgres_pool()
        if pool is None:
            raise RuntimeError("PostgreSQL not available")

        # 1. Fetch all companies and their exposures
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT company_id, node_id, activity_type
                FROM company_node_exposures
                WHERE status = 'ACTIVE'
                ORDER BY company_id
                """
            )

        # Group by company
        company_nodes: dict[str, List[str]] = {}
        for r in rows:
            cid = r["company_id"]
            if cid not in company_nodes:
                company_nodes[cid] = []
            company_nodes[cid].append(r["node_id"])

        companies = list(company_nodes.keys())
        total_pairs = len(companies) * (len(companies) - 1) // 2

        # Update total in job
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE computation_jobs SET total_items = $2 WHERE job_id = $1",
                job_id, total_pairs,
            )

        # 2. For each pair, query Neo4j for industrial flow paths
        driver = get_async_driver()
        processed = 0

        for i, company_a in enumerate(companies):
            for company_b in companies[i + 1:]:
                node_ids_a = company_nodes[company_a]
                node_ids_b = company_nodes[company_b]

                # A -> B
                async with driver.session() as session:
                    result = await session.run(
                        """
                        MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
                        WHERE a.node_id IN $node_ids_a AND b.node_id IN $node_ids_b
                        RETURN count(r) AS cnt
                        """,
                        node_ids_a=node_ids_a, node_ids_b=node_ids_b,
                    )
                    record = await result.single()
                    ab_count = record["cnt"] if record else 0

                # B -> A
                async with driver.session() as session:
                    result = await session.run(
                        """
                        MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
                        WHERE a.node_id IN $node_ids_b AND b.node_id IN $node_ids_a
                        RETURN count(r) AS cnt
                        """,
                        node_ids_b=node_ids_b, node_ids_a=node_ids_a,
                    )
                    record = await result.single()
                    ba_count = record["cnt"] if record else 0

                # Write relations into the latest ACTIVE subgraph of each company
                if ab_count > 0:
                    await _write_inferred_relation(company_a, company_b, "upstream_of")
                if ba_count > 0:
                    await _write_inferred_relation(company_b, company_a, "upstream_of")

                processed += 1
                if processed % 10 == 0:
                    await update_job_progress(job_id, processed)

        await complete_job(job_id, {
            "total_companies": len(companies),
            "total_pairs": total_pairs,
            "processed_pairs": processed,
        })

    except Exception as exc:
        await fail_job(job_id, str(exc))
        raise


async def _write_inferred_relation(
    from_company_id: str,
    to_company_id: str,
    subtype: str,
) -> None:
    """Write an inferred_industrial relation into the latest ACTIVE subgraph of from_company."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        # Find latest ACTIVE subgraph for from_company
        row = await conn.fetchrow(
            """
            SELECT subgraph_id FROM company_subgraphs
            WHERE company_id = $1 AND status = 'ACTIVE'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            from_company_id,
        )

        if row is None:
            return

        subgraph_id = row["subgraph_id"]

        await conn.execute(
            """
            INSERT INTO company_subgraph_relations
            (subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype, strength, confidence, evidence, notes)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype) DO NOTHING
            """,
            subgraph_id,
            from_company_id,
            to_company_id,
            SubgraphRelationType.INFERRED_INDUSTRIAL.value,
            subtype,
            1.0,
            Confidence.MEDIUM.value,
            "[]",
            f"Derived from industrial flow between exposed nodes",
        )
