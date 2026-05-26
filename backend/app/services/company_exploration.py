"""
================================================================================
 DOMAIN: COMPANY EXPLORATION (公司探索视图)
================================================================================
为异构画布提供数据：公司节点 + 物料节点 + 暴露边 + 产业流边。

Phase 1: 锚点公司 + 其暴露物料 + 物料间产业流
================================================================================
"""

from __future__ import annotations

from typing import List

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool


async def get_exploration_graph(company_id: str) -> dict:
    """
    Return the heterogeneous exploration graph centered on a company.

    Nodes:
      - company: the anchor company
      - material: IndustrialNodes exposed by the anchor company
      - material_extra: upstream/downstream IndustrialNodes connected to exposed nodes

    Edges:
      - exposure: company -> material (anchor exposes this node)
      - industrial_flow: material -> material (INDUSTRIAL_FLOW in Neo4j)
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    # 1. Fetch anchor company info
    async with pool.acquire() as conn:
        company_row = await conn.fetchrow(
            "SELECT company_id, name_zh, company_type, status FROM companies WHERE company_id = $1",
            company_id,
        )
    if not company_row:
        return {"nodes": [], "edges": []}

    anchor = {
        "id": company_row["company_id"],
        "type": "company",
        "label": company_row["name_zh"] or company_row["company_id"],
        "company_type": company_row["company_type"] or "unknown",
        "status": company_row["status"] or "ACTIVE",
    }

    # 2. Fetch exposures (material nodes) for this company
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
        return {"nodes": [anchor], "edges": []}

    exposed_node_ids = [r["node_id"] for r in exposure_rows]

    driver = get_async_driver()

    # 3. Fetch material nodes details from Neo4j
    material_nodes: List[dict] = []
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n.node_id AS id, n.canonical_name_zh AS label, n.node_type AS node_type
            ORDER BY n.canonical_name_zh
            """,
            node_ids=exposed_node_ids,
        )
        records = await result.data()
        material_nodes = [
            {
                "id": r["id"],
                "type": "material",
                "label": r["label"] or r["id"],
                "node_type": r["node_type"] or "unknown",
            }
            for r in records
        ]

    # Build activity_type map for exposure edges
    activity_map = {r["node_id"]: r["activity_type"] for r in exposure_rows}
    weight_map = {r["node_id"]: float(r["weight"]) if r["weight"] is not None else 1.0 for r in exposure_rows}
    role_map = {r["node_id"]: r["role"] for r in exposure_rows}

    # 4. Build exposure edges (company -> material)
    exposure_edges: List[dict] = []
    for m in material_nodes:
        exposure_edges.append({
            "source": company_id,
            "target": m["id"],
            "type": "exposure",
            "activity_type": activity_map.get(m["id"], "unknown"),
            "weight": weight_map.get(m["id"], 1.0),
            "role": role_map.get(m["id"]),
        })

    # 5. Fetch industrial_flow edges among exposed nodes + 1-hop neighbors
    industrial_edges: List[dict] = []
    async with driver.session() as session:
        # Edges where both ends are in exposed nodes
        result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
            WHERE a.node_id IN $node_ids AND b.node_id IN $node_ids
            RETURN a.node_id AS source, b.node_id AS target, r.edge_type AS edge_type
            """,
            node_ids=exposed_node_ids,
        )
        records = await result.data()
        seen_pairs = set()
        for r in records:
            pair = (r["source"], r["target"])
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                industrial_edges.append({
                    "source": r["source"],
                    "target": r["target"],
                    "type": "industrial_flow",
                    "edge_type": r["edge_type"] or "material_flow",
                })

    nodes = [anchor] + material_nodes

    return {
        "nodes": nodes,
        "edges": exposure_edges + industrial_edges,
    }


async def get_material_companies(node_id: str, exclude_company_id: str | None = None) -> dict:
    """
    Return companies connected to a material node.

    Returns peer companies (same node exposure), upstream companies
    (exposing upstream nodes), and downstream companies (exposing downstream nodes).
    """
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    driver = get_async_driver()

    # Peer companies
    async with pool.acquire() as conn:
        peer_rows = await conn.fetch(
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
            exclude_company_id or "",
        )
    peers = [
        {
            "id": r["company_id"],
            "type": "company",
            "label": r["name_zh"] or r["company_id"],
            "activity_type": r["activity_type"],
            "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
        }
        for r in peer_rows
    ]

    # Upstream nodes from Neo4j
    upstream_nodes: List[dict] = []
    downstream_nodes: List[dict] = []
    async with driver.session() as session:
        up_result = await session.run(
            """
            MATCH (up:IndustrialNode)-[:INDUSTRIAL_FLOW]->(n:IndustrialNode {node_id: $node_id})
            RETURN up.node_id AS node_id, up.canonical_name_zh AS name
            ORDER BY up.canonical_name_zh
            """,
            node_id=node_id,
        )
        upstream_nodes = await up_result.data()

        down_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})-[:INDUSTRIAL_FLOW]->(down:IndustrialNode)
            RETURN down.node_id AS node_id, down.canonical_name_zh AS name
            ORDER BY down.canonical_name_zh
            """,
            node_id=node_id,
        )
        downstream_nodes = await down_result.data()

    # Upstream companies (companies exposing upstream nodes)
    upstream_companies: List[dict] = []
    if upstream_nodes:
        up_node_ids = [n["node_id"] for n in upstream_nodes]
        node_name_map = {n["node_id"]: n["name"] or n["node_id"] for n in upstream_nodes}
        async with pool.acquire() as conn:
            up_rows = await conn.fetch(
                """
                SELECT DISTINCT e.company_id, c.name_zh, e.node_id, e.activity_type, e.weight
                FROM company_node_exposures e
                JOIN companies c ON e.company_id = c.company_id
                WHERE e.node_id = ANY($1)
                  AND e.company_id != $2
                  AND e.status IN ('ACTIVE', 'PENDING')
                ORDER BY e.weight DESC, c.name_zh
                """,
                up_node_ids,
                exclude_company_id or "",
            )
        upstream_companies = [
            {
                "id": r["company_id"],
                "type": "company",
                "label": r["name_zh"] or r["company_id"],
                "via_node_id": r["node_id"],
                "via_node_name": node_name_map.get(r["node_id"], r["node_id"]),
                "activity_type": r["activity_type"],
                "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
            }
            for r in up_rows
        ]

    # Downstream companies
    downstream_companies: List[dict] = []
    if downstream_nodes:
        down_node_ids = [n["node_id"] for n in downstream_nodes]
        node_name_map = {n["node_id"]: n["name"] or n["node_id"] for n in downstream_nodes}
        async with pool.acquire() as conn:
            down_rows = await conn.fetch(
                """
                SELECT DISTINCT e.company_id, c.name_zh, e.node_id, e.activity_type, e.weight
                FROM company_node_exposures e
                JOIN companies c ON e.company_id = c.company_id
                WHERE e.node_id = ANY($1)
                  AND e.company_id != $2
                  AND e.status IN ('ACTIVE', 'PENDING')
                ORDER BY e.weight DESC, c.name_zh
                """,
                down_node_ids,
                exclude_company_id or "",
            )
        downstream_companies = [
            {
                "id": r["company_id"],
                "type": "company",
                "label": r["name_zh"] or r["company_id"],
                "via_node_id": r["node_id"],
                "via_node_name": node_name_map.get(r["node_id"], r["node_id"]),
                "activity_type": r["activity_type"],
                "weight": float(r["weight"]) if r["weight"] is not None else 1.0,
            }
            for r in down_rows
        ]

    return {
        "node_id": node_id,
        "node_name": await _get_node_name(driver, node_id),
        "peers": peers,
        "upstream": upstream_companies,
        "downstream": downstream_companies,
    }


async def _get_node_name(driver, node_id: str) -> str:
    async with driver.session() as session:
        result = await session.run(
            "MATCH (n:IndustrialNode {node_id: $node_id}) RETURN n.canonical_name_zh AS name",
            node_id=node_id,
        )
        record = await result.single()
        return record["name"] if record else node_id
