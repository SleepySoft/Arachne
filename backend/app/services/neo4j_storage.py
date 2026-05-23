import json
from datetime import datetime
from typing import List, Optional

from app.database import get_async_driver
from app.models.schemas import (
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


def _node_from_record(record) -> IndustrialNode:
    props = dict(record["n"])
    return IndustrialNode(
        node_uuid=props.get("node_uuid"),
        node_id=props["node_id"],
        canonical_name_zh=props["canonical_name_zh"],
        canonical_name_en=props.get("canonical_name_en"),
        aliases=props.get("aliases", []),
        definition=props["definition"],
        entity_type=props["entity_type"],
        evidence=_evidence_from_db(props.get("evidence", [])),
        confidence=props.get("confidence", "LOW"),
        status=props.get("status", "PENDING"),
        notes=props.get("notes"),
        created_at=_to_datetime(props.get("created_at")),
        updated_at=_to_datetime(props.get("updated_at")),
    )


def _edge_from_record(record) -> GraphEdge:
    rel = dict(record["r"])
    start = record["start_node"]
    end = record["end_node"]
    ns = rel.get("edge_namespace", "industrial_flow")
    common = {
        "edge_uuid": rel.get("edge_uuid"),
        "edge_id": rel["edge_id"],
        "from_node": start["node_id"],
        "to_node": end["node_id"],
        "description": rel["description"],
        "evidence": _evidence_from_db(rel.get("evidence", [])),
        "confidence": rel.get("confidence", "LOW"),
        "notes": rel.get("notes"),
        "created_at": _to_datetime(rel.get("created_at")),
        "updated_at": _to_datetime(rel.get("updated_at")),
    }
    if ns == "industrial_flow":
        return IndustrialFlowEdge(
            edge_namespace="industrial_flow",
            edge_type=rel["edge_type"],
            **common,
        )
    else:
        return OntologyEdge(
            edge_namespace="ontology",
            edge_type=rel["edge_type"],
            **common,
        )


# ---------------------------------------------------------------------------
# Node Storage
# ---------------------------------------------------------------------------

async def create_node(node: IndustrialNode) -> IndustrialNode:
    driver = get_async_driver()
    now = datetime.utcnow()
    async with driver.session() as session:
        result = await session.run(
            """
            CREATE (n:IndustrialNode {
                node_uuid: $node_uuid,
                node_id: $node_id,
                canonical_name_zh: $canonical_name_zh,
                canonical_name_en: $canonical_name_en,
                aliases: $aliases,
                definition: $definition,
                entity_type: $entity_type,
                evidence: $evidence,
                confidence: $confidence,
                status: $status,
                notes: $notes,
                created_at: $now,
                updated_at: $now
            })
            RETURN n
            """,
            node_uuid=str(node.node_uuid),
            node_id=node.node_id,
            canonical_name_zh=node.canonical_name_zh,
            canonical_name_en=node.canonical_name_en,
            aliases=node.aliases,
            definition=node.definition,
            entity_type=node.entity_type.value,
            evidence=_evidence_to_db(node.evidence),
            confidence=node.confidence.value,
            status=node.status.value,
            notes=node.notes,
            now=now,
        )
        record = await result.single()
        return _node_from_record(record)


async def get_node(node_id: str) -> Optional[IndustrialNode]:
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            "MATCH (n:IndustrialNode {node_id: $node_id}) RETURN n",
            node_id=node_id,
        )
        record = await result.single()
        if record is None:
            return None
        return _node_from_record(record)


async def update_node(node_id: str, data: dict) -> Optional[IndustrialNode]:
    driver = get_async_driver()
    now = datetime.utcnow()
    # Build dynamic SET clauses
    set_clauses = ["n.updated_at = $now"]
    params = {"node_id": node_id, "now": now}
    for key, value in data.items():
        if value is None:
            continue
        if key == "evidence":
            params[key] = _evidence_to_db(value)
        elif key in ("confidence", "status", "entity_type"):
            params[key] = value.value if hasattr(value, "value") else value
        else:
            params[key] = value
        set_clauses.append(f"n.{key} = ${key}")

    cypher = f"""
        MATCH (n:IndustrialNode {{node_id: $node_id}})
        SET {', '.join(set_clauses)}
        RETURN n
    """
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        record = await result.single()
        if record is None:
            return None
        return _node_from_record(record)


async def delete_node(node_id: str) -> bool:
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})
            OPTIONAL MATCH (n)-[r]-()
            DELETE r, n
            RETURN count(n) AS deleted
            """,
            node_id=node_id,
        )
        record = await result.single()
        return record["deleted"] > 0


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> tuple[List[IndustrialNode], int]:
    driver = get_async_driver()
    where_parts = ["1=1"]
    params: dict = {"skip": skip, "limit": limit}

    if entity_type:
        where_parts.append("n.entity_type = $entity_type")
        params["entity_type"] = entity_type
    if status:
        where_parts.append("n.status = $status")
        params["status"] = status
    if search:
        where_parts.append(
            "(n.canonical_name_zh CONTAINS $search OR n.node_id CONTAINS $search OR ANY(a IN n.aliases WHERE a CONTAINS $search))"
        )
        params["search"] = search

    where_clause = " AND ".join(where_parts)

    async with driver.session() as session:
        count_result = await session.run(
            f"MATCH (n:IndustrialNode) WHERE {where_clause} RETURN count(n) AS total",
            **{k: v for k, v in params.items() if k not in ("skip", "limit")},
        )
        count_record = await count_result.single()
        total = count_record["total"]

        result = await session.run(
            f"""
            MATCH (n:IndustrialNode) WHERE {where_clause}
            RETURN n ORDER BY n.canonical_name_zh
            SKIP $skip LIMIT $limit
            """,
            **params,
        )
        items = [_node_from_record(r) async for r in result]
        return items, total


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
            now=now,
        )
        record = await result.single()
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
            now=now,
        )
        record = await result.single()
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

    set_clauses = ["r.updated_at = $now"]
    params = {"edge_id": edge_id, "now": now}
    for key, value in data.items():
        if value is None:
            continue
        if key == "evidence":
            params[key] = _evidence_to_db(value)
        elif key in ("confidence",):
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
    async with driver.session() as session:
        node_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})
            OPTIONAL MATCH (n)-[*1..$depth]-(m:IndustrialNode)
            WITH collect(DISTINCT n) + collect(DISTINCT m) AS nodes
            UNWIND nodes AS node
            RETURN DISTINCT node
            """,
            node_id=node_id,
            depth=depth,
        )
        nodes = [_node_from_record(r) async for r in node_result]

        edge_result = await session.run(
            """
            MATCH (n:IndustrialNode {node_id: $node_id})
            OPTIONAL MATCH (n)-[r*1..$depth]-(m:IndustrialNode)
            WITH [rel IN r | rel] AS rels
            UNWIND rels AS edge
            RETURN DISTINCT edge AS r, startNode(edge) AS start_node, endNode(edge) AS end_node
            """,
            node_id=node_id,
            depth=depth,
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
            RETURN DISTINCT m AS n
            """,
            node_id=node_id,
        )
        nodes = [_node_from_record(r) async for r in node_result]

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

        # distributions
        node_type_dist = {}
        r3 = await session.run(
            "MATCH (n:IndustrialNode) RETURN n.entity_type AS t, count(n) AS c"
        )
        async for rec in r3:
            node_type_dist[rec["t"]] = rec["c"]

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

        status_dist = {}
        r7 = await session.run(
            "MATCH (n:IndustrialNode) RETURN n.status AS t, count(n) AS c"
        )
        async for rec in r7:
            status_dist[rec["t"]] = rec["c"]

        confidence_dist = {}
        r8 = await session.run(
            "MATCH (n:IndustrialNode) RETURN n.confidence AS t, count(n) AS c"
        )
        async for rec in r8:
            confidence_dist[rec["t"]] = rec["c"]

        return GraphStats(
            total_nodes=total_nodes,
            total_edges=total_edges,
            node_type_distribution=node_type_dist,
            edge_namespace_distribution=edge_ns_dist,
            edge_type_distribution=edge_type_dist,
            status_distribution=status_dist,
            confidence_distribution=confidence_dist,
        )
