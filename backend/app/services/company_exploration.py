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
from app.services import node_storage


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

    # 3. Fetch material node metadata from PostgreSQL
    nodes_map = await node_storage.get_nodes_by_ids(exposed_node_ids)
    material_nodes = [
        {
            "id": node.node_id,
            "type": "material",
            "label": node.canonical_name_zh or node.node_id,
            "node_type": node.entity_type.value if hasattr(node.entity_type, "value") else node.entity_type,
        }
        for node in nodes_map.values()
    ]
    material_nodes.sort(key=lambda x: x["label"])

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

    nodes = [anchor] + material_nodes

    return {
        "nodes": nodes,
        "edges": exposure_edges,
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

    # Upstream/downstream node IDs from Neo4j; names from PostgreSQL
    driver = get_async_driver()
    upstream_node_ids: List[str] = []
    downstream_node_ids: List[str] = []
    async with driver.session() as session:
        up_result = await session.run(
            """
            MATCH (up:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(n:IndustrialNode {node_id: $node_id})
            WHERE r.edge_type <> 'derived_from'
            RETURN up.node_id AS node_id
            """,
            node_id=node_id,
        )
        upstream_node_ids = [r["node_id"] async for r in up_result]

        down_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})-[r:INDUSTRIAL_FLOW]->(down:IndustrialNode)
            WHERE r.edge_type <> 'derived_from'
            RETURN down.node_id AS node_id
            """,
            node_id=node_id,
        )
        downstream_node_ids = [r["node_id"] async for r in down_result]

    upstream_nodes = [
        {"node_id": nid, "name": node.canonical_name_zh or nid}
        for nid, node in (await node_storage.get_nodes_by_ids(upstream_node_ids)).items()
    ]
    downstream_nodes = [
        {"node_id": nid, "name": node.canonical_name_zh or nid}
        for nid, node in (await node_storage.get_nodes_by_ids(downstream_node_ids)).items()
    ]

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
        "node_name": await _get_node_name(node_id),
        "peers": peers,
        "upstream": upstream_companies,
        "downstream": downstream_companies,
    }


async def _get_node_name(node_id: str) -> str:
    node = await node_storage.get_node(node_id)
    return node.canonical_name_zh if node else node_id
