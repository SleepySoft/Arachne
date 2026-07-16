import json
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool
from app.services import node_storage
from app.engines.legacy.schemas import (
    Evidence,
    GraphEdge,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialNode,
    OntologyEdge,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _evidence_to_db(evidence_list: List[Evidence]) -> str:
    items = []
    for e in evidence_list:
        if isinstance(e, dict):
            items.append(
                {
                    "source_title": e.get("source_title", ""),
                    "source_url": str(e.get("source_url")) if e.get("source_url") else None,
                    "quote": e.get("quote", ""),
                }
            )
        else:
            items.append(
                {
                    "source_title": e.source_title,
                    "source_url": str(e.source_url) if e.source_url else None,
                    "quote": e.quote,
                }
            )
    return json.dumps(items, ensure_ascii=False)


def _evidence_from_db(raw) -> List[Evidence]:
    if not raw:
        return []
    try:
        items = json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if not item:
            continue
        url = item.get("source_url")
        out.append(
            Evidence(
                source_title=item.get("source_title", ""),
                source_url=url if url else None,
                quote=item.get("quote", ""),
            )
        )
    return out


def _to_datetime(value):
    if value is None:
        return None
    if hasattr(value, "to_native"):
        return value.to_native()
    return value


def _edge_from_record(record) -> GraphEdge:
    rel = dict(record["r"])
    start = record["start_node"]
    end = record["end_node"]
    # Use the canonical Neo4j relationship type as the source of truth for the
    # namespace. The `edge_namespace` property is kept for compatibility and
    # query convenience, but a missing or mismatched property must not cause
    # the parser to misclassify an ontology edge as an industrial-flow edge.
    rel_type = record["r"].type
    ns = "industrial_flow" if rel_type == "INDUSTRIAL_FLOW" else "ontology"
    prop_ns = rel.get("edge_namespace")
    if prop_ns and prop_ns != ns:
        # Mismatched property: trust the relationship type and surface the
        # inconsistency via the description so it can be detected/cleaned.
        rel["description"] = f"[ns-mismatch: edge_namespace={prop_ns} vs type={rel_type}] {rel.get('description') or ''}".strip()
    evidence = _evidence_from_db(rel.get("evidence", []))
    confidence = rel.get("confidence", "LOW")
    # Downgrade HIGH confidence if no evidence for backward compatibility with old data
    if confidence == "HIGH" and not evidence:
        confidence = "MEDIUM"
    common = {
        "edge_id": rel["edge_id"],
        "from_node": start["node_id"],
        "to_node": end["node_id"],
        "description": rel.get("description") or "无描述",
        "evidence": evidence,
        "confidence": confidence,
        "notes": rel.get("notes"),
        "is_test": rel.get("is_test", False),
        "created_at": _to_datetime(rel.get("created_at")),
        "updated_at": _to_datetime(rel.get("updated_at")),
    }
    if rel.get("edge_uuid"):
        common["edge_uuid"] = rel["edge_uuid"]
    if ns == "industrial_flow":
        return IndustrialFlowEdge(
            edge_namespace="industrial_flow",
            edge_type=rel.get("edge_type", ""),
            **common,
        )
    else:
        return OntologyEdge(
            edge_namespace="ontology",
            edge_type=rel.get("edge_type", ""),
            **common,
        )


# ---------------------------------------------------------------------------
# Node Storage
# ---------------------------------------------------------------------------

async def create_node(node: IndustrialNode) -> IndustrialNode:
    """Create a skeleton node in Neo4j and persist metadata in PostgreSQL."""
    driver = get_async_driver()
    async with driver.session() as session:
        await session.run(
            "CREATE (n:IndustrialNode {node_id: $node_id})",
            node_id=node.node_id,
        )
    try:
        return await node_storage.create_node(node)
    except Exception:
        # Rollback Neo4j skeleton if PG write fails
        async with driver.session() as session:
            await session.run(
                "MATCH (n:IndustrialNode {node_id: $node_id}) DELETE n",
                node_id=node.node_id,
            )
        raise


async def get_node(node_id: str) -> Optional[IndustrialNode]:
    """Node metadata now lives in PostgreSQL."""
    return await node_storage.get_node(node_id)


async def update_node(node_id: str, data: dict) -> Optional[IndustrialNode]:
    """Update node metadata in PostgreSQL. Neo4j skeleton only holds node_id."""
    return await node_storage.update_node(node_id, data)


async def delete_node(node_id: str) -> bool:
    """Delete metadata from PostgreSQL and skeleton from Neo4j."""
    pg_deleted = await node_storage.delete_node(node_id)
    driver = get_async_driver()
    async with driver.session() as session:
        await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})
            OPTIONAL MATCH (n)-[r]-()
            DELETE r, n
            """,
            node_id=node_id,
        )
    return pg_deleted


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    draft_only: Optional[bool] = None,
) -> tuple[List[IndustrialNode], int]:
    """Node metadata now lives in PostgreSQL."""
    return await node_storage.list_nodes(
        skip=skip,
        limit=limit,
        entity_type=entity_type,
        status=status,
        search=search,
        draft_only=draft_only,
    )


# ---------------------------------------------------------------------------
# Edge Storage
# ---------------------------------------------------------------------------

async def create_industrial_flow_edge(edge: IndustrialFlowEdge) -> IndustrialFlowEdge:
    driver = get_async_driver()
    now = datetime.utcnow()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:IndustrialNode {node_id: $from_node})
            MATCH (b:IndustrialNode {node_id: $to_node})
            CREATE (a)-[r:INDUSTRIAL_FLOW {
                edge_uuid: $edge_uuid,
                edge_id: $edge_id,
                edge_namespace: $edge_namespace,
                edge_type: $edge_type,
                description: $description,
                evidence: $evidence,
                confidence: $confidence,
                notes: $notes,
                is_test: $is_test,
                created_at: $now,
                updated_at: $now
            }]->(b)
            RETURN r, a AS start_node, b AS end_node
            """,
            edge_uuid=str(edge.edge_uuid),
            edge_id=edge.edge_id,
            edge_namespace=edge.edge_namespace,
            edge_type=edge.edge_type.value,
            from_node=edge.from_node,
            to_node=edge.to_node,
            description=edge.description,
            evidence=_evidence_to_db(edge.evidence),
            confidence=edge.confidence.value,
            notes=edge.notes,
            is_test=edge.is_test,
            now=now,
        )
        record = await result.single()
        if record is None:
            raise ValueError(f"Cannot create edge: from_node '{edge.from_node}' or to_node '{edge.to_node}' does not exist")
        return _edge_from_record(record)


async def create_ontology_edge(edge: OntologyEdge) -> OntologyEdge:
    driver = get_async_driver()
    now = datetime.utcnow()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:IndustrialNode {node_id: $from_node})
            MATCH (b:IndustrialNode {node_id: $to_node})
            CREATE (a)-[r:ONTOLOGY {
                edge_uuid: $edge_uuid,
                edge_id: $edge_id,
                edge_namespace: $edge_namespace,
                edge_type: $edge_type,
                description: $description,
                evidence: $evidence,
                confidence: $confidence,
                notes: $notes,
                is_test: $is_test,
                created_at: $now,
                updated_at: $now
            }]->(b)
            RETURN r, a AS start_node, b AS end_node
            """,
            edge_uuid=str(edge.edge_uuid),
            edge_id=edge.edge_id,
            edge_namespace=edge.edge_namespace,
            edge_type=edge.edge_type.value,
            from_node=edge.from_node,
            to_node=edge.to_node,
            description=edge.description,
            evidence=_evidence_to_db(edge.evidence),
            confidence=edge.confidence.value,
            notes=edge.notes,
            is_test=edge.is_test,
            now=now,
        )
        record = await result.single()
        if record is None:
            raise ValueError(f"Cannot create edge: from_node '{edge.from_node}' or to_node '{edge.to_node}' does not exist")
        return _edge_from_record(record)


async def get_edge(edge_id: str) -> Optional[GraphEdge]:
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r {edge_id: $edge_id}]->(b:IndustrialNode)
            RETURN r, a AS start_node, b AS end_node
            """,
            edge_id=edge_id,
        )
        record = await result.single()
        if record is None:
            return None
        return _edge_from_record(record)


async def update_edge(edge_id: str, data: dict, namespace: str) -> Optional[GraphEdge]:
    driver = get_async_driver()
    now = datetime.utcnow()
    rel_type = "INDUSTRIAL_FLOW" if namespace == "industrial_flow" else "ONTOLOGY"

    existing = await get_edge(edge_id)
    if not existing:
        return None

    new_from = data.get("from_node", existing.from_node)
    new_to = data.get("to_node", existing.to_node)

    # Build the merged property set, preserving fields that are not being updated.
    merged_props = {
        "edge_id": existing.edge_id,
        "edge_namespace": existing.edge_namespace,
        "edge_type": existing.edge_type,
        "description": existing.description,
        "evidence": _evidence_to_db(existing.evidence),
        "confidence": existing.confidence.value if hasattr(existing.confidence, "value") else existing.confidence,
        "notes": existing.notes,
        "is_test": existing.is_test,
        "created_at": existing.created_at,
    }
    if getattr(existing, "edge_uuid", None):
        merged_props["edge_uuid"] = str(existing.edge_uuid)

    for key, value in data.items():
        if value is None or key in ("from_node", "to_node"):
            continue
        if key == "evidence":
            merged_props[key] = _evidence_to_db(value)
        elif key == "confidence":
            merged_props[key] = value.value if hasattr(value, "value") else value
        else:
            merged_props[key] = value
    merged_props["updated_at"] = now

    # If the endpoints change, recreate the relationship so it connects to the new nodes.
    if new_from != existing.from_node or new_to != existing.to_node:
        # Avoid creating a duplicate edge (same namespace/type between the same pair).
        async with driver.session() as session:
            dup = await session.run(
                f"""
                MATCH (a:IndustrialNode {{node_id: $from_node}})-[r:{rel_type} {{edge_namespace: $ns, edge_type: $et}}]->(b:IndustrialNode {{node_id: $to_node}})
                WHERE r.edge_id <> $edge_id
                RETURN count(r) AS cnt
                """,
                from_node=new_from,
                to_node=new_to,
                ns=existing.edge_namespace,
                et=existing.edge_type,
                edge_id=edge_id,
            )
            dup_record = await dup.single()
            if dup_record and dup_record["cnt"] > 0:
                et = existing.edge_type.value if hasattr(existing.edge_type, "value") else existing.edge_type
                raise ValueError(
                    f"已存在同类型关系：{new_from} -> {new_to} ({existing.edge_namespace}/{et})"
                )

            # Build Cypher property map using explicit identifiers.
            prop_items = []
            params: dict = {
                "old_from": existing.from_node,
                "old_to": existing.to_node,
                "new_from": new_from,
                "new_to": new_to,
            }
            for k, v in merged_props.items():
                param_key = f"p_{k}"
                params[param_key] = v
                prop_items.append(f"{k}: ${param_key}")
            props_clause = "{" + ", ".join(prop_items) + "}"

            cypher = f"""
                MATCH (old_a:IndustrialNode {{node_id: $old_from}})-[old_r:{rel_type} {{edge_id: $p_edge_id}}]->(old_b:IndustrialNode {{node_id: $old_to}})
                WITH old_r
                MATCH (new_a:IndustrialNode {{node_id: $new_from}}), (new_b:IndustrialNode {{node_id: $new_to}})
                DELETE old_r
                CREATE (new_a)-[r:{rel_type} {props_clause}]->(new_b)
                RETURN r, new_a AS start_node, new_b AS end_node
            """
            result = await session.run(cypher, **params)
            record = await result.single()
            if record is None:
                return None
            return _edge_from_record(record)

    # Endpoints unchanged: just update properties on the existing relationship.
    set_clauses = ["r.updated_at = $now"]
    params = {"edge_id": edge_id, "now": now}
    for key, value in data.items():
        if value is None or key in ("from_node", "to_node"):
            continue
        if key == "evidence":
            params[key] = _evidence_to_db(value)
        elif key == "confidence":
            params[key] = value.value if hasattr(value, "value") else value
        else:
            params[key] = value
        set_clauses.append(f"r.{key} = ${key}")

    cypher = f"""
        MATCH (a:IndustrialNode)-[r:{rel_type} {{edge_id: $edge_id}}]->(b:IndustrialNode)
        SET {', '.join(set_clauses)}
        RETURN r, a AS start_node, b AS end_node
    """
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        record = await result.single()
        if record is None:
            return None
        return _edge_from_record(record)


async def delete_edge(edge_id: str, namespace: str) -> bool:
    driver = get_async_driver()
    rel_type = "INDUSTRIAL_FLOW" if namespace == "industrial_flow" else "ONTOLOGY"
    async with driver.session() as session:
        result = await session.run(
            f"""
            MATCH ()-[r:{rel_type} {{edge_id: $edge_id}}]->()
            DELETE r
            RETURN count(r) AS deleted
            """,
            edge_id=edge_id,
        )
        record = await result.single()
        return record["deleted"] > 0


async def list_edges(
    skip: int = 0,
    limit: int = 20,
    edge_namespace: Optional[str] = None,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
) -> tuple[List[GraphEdge], int]:
    driver = get_async_driver()
    params: dict = {"skip": skip, "limit": limit}

    if edge_namespace:
        rel_clause = f"-[r:{edge_namespace.upper()}]->"
        if edge_type:
            where_clause = "r.edge_type = $edge_type"
            params["edge_type"] = edge_type
        else:
            where_clause = "1=1"
    else:
        rel_clause = "-[r]->"
        if edge_type:
            where_clause = "r.edge_type = $edge_type"
            params["edge_type"] = edge_type
        else:
            where_clause = "1=1"

    if from_node:
        where_clause += " AND a.node_id = $from_node"
        params["from_node"] = from_node
    if to_node:
        where_clause += " AND b.node_id = $to_node"
        params["to_node"] = to_node

    async with driver.session() as session:
        count_result = await session.run(
            f"""
            MATCH (a:IndustrialNode){rel_clause}(b:IndustrialNode)
            WHERE {where_clause}
            RETURN count(r) AS total
            """,
            **{k: v for k, v in params.items() if k not in ("skip", "limit")},
        )
        count_record = await count_result.single()
        total = count_record["total"]

        result = await session.run(
            f"""
            MATCH (a:IndustrialNode){rel_clause}(b:IndustrialNode)
            WHERE {where_clause}
            RETURN r, a AS start_node, b AS end_node
            ORDER BY r.edge_id
            SKIP $skip LIMIT $limit
            """,
            **params,
        )
        items = [_edge_from_record(r) async for r in result]
        return items, total


# ---------------------------------------------------------------------------
# Query Storage
# ---------------------------------------------------------------------------

async def get_subgraph(node_id: str, depth: int = 2) -> tuple[List[IndustrialNode], List[GraphEdge]]:
    driver = get_async_driver()
    # Neo4j does not allow parameters in path length patterns like [*1..$depth],
    # so we safely interpolate the validated integer depth into the Cypher string.
    async with driver.session() as session:
        node_result = await session.run(
            f"""
            MATCH (n:IndustrialNode {{node_id: $node_id}})
            OPTIONAL MATCH (n)-[*1..{depth}]-(m:IndustrialNode)
            WITH collect(DISTINCT n) + collect(DISTINCT m) AS nodes
            UNWIND nodes AS node
            RETURN DISTINCT node.node_id AS node_id
            """,
            node_id=node_id,
        )
        node_ids = [r["node_id"] async for r in node_result]
        node_map = await node_storage.get_nodes_by_ids(node_ids)
        nodes = [node_map[nid] for nid in node_ids if nid in node_map]

        edge_result = await session.run(
            f"""
            MATCH (n:IndustrialNode {{node_id: $node_id}})
            OPTIONAL MATCH (n)-[r*1..{depth}]-(m:IndustrialNode)
            WITH [rel IN r | rel] AS rels
            UNWIND rels AS edge
            RETURN DISTINCT edge AS r, startNode(edge) AS start_node, endNode(edge) AS end_node
            """,
            node_id=node_id,
        )
        edges = []
        async for r in edge_result:
            try:
                edges.append(_edge_from_record(r))
            except Exception:
                continue
        return nodes, edges


async def get_neighbors(node_id: str) -> tuple[List[IndustrialNode], List[GraphEdge]]:
    driver = get_async_driver()
    async with driver.session() as session:
        node_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})-[r]-(m:IndustrialNode)
            RETURN DISTINCT m.node_id AS node_id
            """,
            node_id=node_id,
        )
        neighbor_ids = [r["node_id"] async for r in node_result]
        node_map = await node_storage.get_nodes_by_ids(neighbor_ids)
        nodes = [node_map[nid] for nid in neighbor_ids if nid in node_map]

        edge_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})-[r]-(m:IndustrialNode)
            RETURN r, startNode(r) AS start_node, endNode(r) AS end_node
            """,
            node_id=node_id,
        )
        edges = [_edge_from_record(r) async for r in edge_result]
        return nodes, edges


async def get_paths(from_node: str, to_node: str, max_depth: int = 5) -> List[List[dict]]:
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH path = (a:IndustrialNode {node_id: $from_node})-[*1..$max_depth]->(b:IndustrialNode {node_id: $to_node})
            RETURN [node IN nodes(path) | node.node_id] AS node_ids,
                   [rel IN relationships(path) | {
                        edge_id: rel.edge_id,
                        edge_namespace: rel.edge_namespace,
                        edge_type: rel.edge_type,
                        from_node: startNode(rel).node_id,
                        to_node: endNode(rel).node_id
                   }] AS rels
            LIMIT 10
            """,
            from_node=from_node,
            to_node=to_node,
            max_depth=max_depth,
        )
        paths = []
        async for record in result:
            path = []
            node_ids = record["node_ids"]
            rels = record["rels"]
            for i, nid in enumerate(node_ids):
                path.append({"type": "node", "node_id": nid})
                if i < len(rels):
                    path.append({"type": "edge", **rels[i]})
            paths.append(path)
        return paths


async def get_stats() -> GraphStats:
    driver = get_async_driver()
    async with driver.session() as session:
        total_nodes = 0
        total_edges = 0

        r1 = await session.run("MATCH (n:IndustrialNode) RETURN count(n) AS c")
        rec1 = await r1.single()
        if rec1:
            total_nodes = rec1["c"]

        r2 = await session.run("MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->() RETURN count(r) AS c")
        rec2 = await r2.single()
        if rec2:
            total_edges = rec2["c"]

        edge_ns_dist = {}
        r4 = await session.run(
            "MATCH ()-[r:INDUSTRIAL_FLOW]->() RETURN 'industrial_flow' AS t, count(r) AS c"
        )
        rec4 = await r4.single()
        if rec4:
            edge_ns_dist["industrial_flow"] = rec4["c"]
        r5 = await session.run(
            "MATCH ()-[r:ONTOLOGY]->() RETURN 'ontology' AS t, count(r) AS c"
        )
        rec5 = await r5.single()
        if rec5:
            edge_ns_dist["ontology"] = rec5["c"]

        edge_type_dist = {}
        r6 = await session.run(
            "MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->() RETURN r.edge_type AS t, count(r) AS c"
        )
        async for rec in r6:
            edge_type_dist[rec["t"]] = rec["c"]

    # Node metadata distributions now come from PostgreSQL
    node_type_dist = {}
    status_dist = {}
    confidence_dist = {}

    pool = await get_postgres_pool()
    if pool is not None:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT entity_type, COUNT(*) AS c FROM industrial_nodes GROUP BY entity_type"
            )
            for row in rows:
                node_type_dist[row["entity_type"]] = row["c"]

            rows = await conn.fetch(
                "SELECT status, COUNT(*) AS c FROM industrial_nodes GROUP BY status"
            )
            for row in rows:
                status_dist[row["status"]] = row["c"]

            rows = await conn.fetch(
                "SELECT confidence, COUNT(*) AS c FROM industrial_nodes GROUP BY confidence"
            )
            for row in rows:
                confidence_dist[row["confidence"]] = row["c"]

    return GraphStats(
        total_nodes=total_nodes,
        total_edges=total_edges,
        node_type_distribution=node_type_dist,
        edge_namespace_distribution=edge_ns_dist,
        edge_type_distribution=edge_type_dist,
        status_distribution=status_dist,
        confidence_distribution=confidence_dist,
    )
