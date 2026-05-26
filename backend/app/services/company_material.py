"""
================================================================================
 DOMAIN: COMPANY MATERIAL CONNECTIONS (公司物料关联探索)
================================================================================
以物料为透镜，查询某家公司的关联公司（同行、上游供应商、下游客户）。

数据来源混合：
  - 公司暴露：PostgreSQL company_node_exposures
  - 物料流向：Neo4j IndustrialNode / INDUSTRIAL_FLOW
================================================================================
"""

from __future__ import annotations

from typing import Dict, List

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool


async def get_material_connections(company_id: str) -> dict:
    """
    Return all material-based connections for a given company.

    Structure:
      {
        "company_id": str,
        "company_name": str,
        "exposures": [
          {
            "node_id": str,
            "node_name": str,
            "activity_type": str,
            "peers": [...],
            "upstream": [...],
            "downstream": [...],
          }
        ]
      }
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    # 1. Fetch company name
    async with pool.acquire() as conn:
        company_row = await conn.fetchrow(
            "SELECT name_zh FROM companies WHERE company_id = $1",
            company_id,
        )
    company_name = company_row["name_zh"] if company_row else company_id

    # 2. Fetch all exposures for this company
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
            "exposures": [],
        }

    driver = get_async_driver()
    exposures: List[dict] = []

    for exp in exposure_rows:
        node_id = exp["node_id"]

        # 2a. Peers: other companies exposing the same node
        peers = await _get_peer_companies(pool, company_id, node_id)

        # 2b. Upstream & downstream nodes from Neo4j
        upstream_nodes: List[dict] = []
        downstream_nodes: List[dict] = []
        async with driver.session() as session:
            # Upstream nodes: nodes that have INDUSTRIAL_FLOW TO this node
            up_result = await session.run(
                """
                MATCH (up:IndustrialNode)-[:INDUSTRIAL_FLOW]->(n:IndustrialNode {node_id: $node_id})
                RETURN up.node_id AS node_id, up.canonical_name_zh AS name
                ORDER BY up.canonical_name_zh
                """,
                node_id=node_id,
            )
            upstream_nodes = await up_result.data()

            # Downstream nodes: nodes that this node has INDUSTRIAL_FLOW TO
            down_result = await session.run(
                """
                MATCH (n:IndustrialNode {node_id: $node_id})-[:INDUSTRIAL_FLOW]->(down:IndustrialNode)
                RETURN down.node_id AS node_id, down.canonical_name_zh AS name
                ORDER BY down.canonical_name_zh
                """,
                node_id=node_id,
            )
            downstream_nodes = await down_result.data()

        # 2c. Companies exposing upstream nodes
        upstream_companies = await _get_companies_by_nodes(pool, company_id, upstream_nodes)

        # 2d. Companies exposing downstream nodes
        downstream_companies = await _get_companies_by_nodes(pool, company_id, downstream_nodes)

        exposures.append({
            "node_id": node_id,
            "node_name": await _get_node_name(driver, node_id),
            "activity_type": exp["activity_type"],
            "weight": float(exp["weight"]) if exp["weight"] is not None else 1.0,
            "role": exp["role"],
            "peers": peers,
            "upstream": upstream_companies,
            "downstream": downstream_companies,
        })

    return {
        "company_id": company_id,
        "company_name": company_name,
        "exposures": exposures,
    }


async def _get_peer_companies(pool, exclude_company_id: str, node_id: str) -> List[dict]:
    """Return other companies that expose the same node."""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT e.company_id, c.name_zh, e.activity_type, e.weight
            FROM company_node_exposures e
            JOIN companies c ON e.company_id = c.company_id
            WHERE e.node_id = $1
              AND e.company_id != $2
              AND e.status IN ('ACTIVE', 'PENDING')
            ORDER BY e.weight DESC, c.name_zh
            """,
            node_id,
            exclude_company_id,
        )
    return [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or r["company_id"],
            "activity_type": r["activity_type"],
            "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
        }
        for r in rows
    ]


async def _get_companies_by_nodes(
    pool, exclude_company_id: str, nodes: List[dict]
) -> List[dict]:
    """Return companies that expose any of the given nodes."""
    if not nodes:
        return []

    node_ids = [n["node_id"] for n in nodes]
    # Build a lookup for node names
    node_name_map: Dict[str, str] = {n["node_id"]: n["name"] or n["node_id"] for n in nodes}

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT DISTINCT e.company_id, c.name_zh, e.node_id, e.activity_type, e.weight
            FROM company_node_exposures e
            JOIN companies c ON e.company_id = c.company_id
            WHERE e.node_id = ANY($1)
              AND e.company_id != $2
              AND e.status IN ('ACTIVE', 'PENDING')
            ORDER BY e.weight DESC, c.name_zh
            """,
            node_ids,
            exclude_company_id,
        )

    return [
        {
            "company_id": r["company_id"],
            "name_zh": r["name_zh"] or r["company_id"],
            "node_id": r["node_id"],
            "node_name": node_name_map.get(r["node_id"], r["node_id"]),
            "activity_type": r["activity_type"],
            "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
        }
        for r in rows
    ]


async def _get_node_name(driver, node_id: str) -> str:
    """Fetch canonical_name_zh for a node from Neo4j."""
    async with driver.session() as session:
        result = await session.run(
            "MATCH (n:IndustrialNode {node_id: $node_id}) RETURN n.canonical_name_zh AS name",
            node_id=node_id,
        )
        record = await result.single()
        return record["name"] if record else node_id
