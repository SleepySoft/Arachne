"""
Neo4j storage layer for the arachne-flow engine.

The flow graph uses its own relationship type (:ARACHNE_FLOW) and node labels
(:ArachneFlowNode, :ArachneFlowResource, :ArachneFlowAction,
:ArachneFlowMethod). Node metadata for RESOURCE nodes is resolved from the
shared PostgreSQL `industrial_nodes` table; ACTION/METHOD metadata is stored
on the Neo4j nodes themselves.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from app.database_flow import get_flow_async_driver
from app.engines.arachne_flow.schemas import (
    ActionType,
    FlowAction,
    FlowMethod,
    FlowResource,
    FlowTriple,
    InputRole,
    OutputRole,
    ParsedFlow,
    ResourceType,
    SpecialRole,
)
from app.models.core import GraphEdge, GraphNode, GraphStats, PaginatedEdges, PaginatedNodes
from app.services import node_storage


# ---------------------------------------------------------------------------
# Node ID helpers
# ---------------------------------------------------------------------------


def namespaced_action_id(flow_id: str, action_id: str) -> str:
    """Return the globally unique node ID for an ACTION occurrence."""
    return f"{flow_id}:{action_id}"


def parse_namespaced_action_id(node_id: str) -> Tuple[Optional[str], str]:
    """Split a namespaced ACTION id into (flow_id, action_id)."""
    if ":" in node_id:
        flow_id, action_id = node_id.split(":", 1)
        return flow_id, action_id
    return None, node_id


# ---------------------------------------------------------------------------
# Compile / write
# ---------------------------------------------------------------------------


async def compile_parsed_flow(parsed: ParsedFlow, clear_existing: bool = False) -> Dict[str, int]:
    """Write a parsed flow into the flow Neo4j instance.

    Args:
        parsed: normalized flow graph.
        clear_existing: if True, remove any previously compiled graph for the
            same flow_id before writing.

    Returns:
        Counts of created nodes and edges.
    """
    driver = get_flow_async_driver()
    flow_id = parsed.flow_id

    if clear_existing:
        await clear_flow(flow_id)

    async with driver.session() as session:
        resource_ids = set(parsed.resources.keys())
        action_ids = set(parsed.actions.keys())
        dual_ids = resource_ids & action_ids
        resource_only_ids = resource_ids - dual_ids
        action_only_ids = action_ids - dual_ids

        # Create dual-role nodes (both resource and action)
        for node_id in dual_ids:
            resource = parsed.resources[node_id]
            action = parsed.actions[node_id]
            await session.run(
                """
                MERGE (n:ArachneFlowNode:ArachneFlowResource:ArachneFlowAction {node_id: $node_id})
                SET n.flow_id = $flow_id,
                    n.node_kind = 'dual',
                    n.also_resource = true,
                    n.resource_type = $resource_type,
                    n.action_type = $action_type,
                    n.local_name = $local_name,
                    n.original_action_id = $original_action_id,
                    n.method_ref = $method_ref,
                    n.updated_at = datetime()
                """,
                {
                    "node_id": node_id,
                    "flow_id": flow_id,
                    "resource_type": resource.resource_type.value,
                    "action_type": action.action_type.value,
                    "local_name": resource.local_name,
                    "original_action_id": action.action_id,
                    "method_ref": action.method_ref,
                },
            )

        # Create resource-only nodes (shared by resource_id, not namespaced)
        for node_id in resource_only_ids:
            resource = parsed.resources[node_id]
            await session.run(
                """
                MERGE (n:ArachneFlowNode:ArachneFlowResource {node_id: $node_id})
                SET n.flow_id = $flow_id,
                    n.node_kind = 'resource',
                    n.resource_type = $resource_type,
                    n.local_name = $local_name,
                    n.updated_at = datetime()
                """,
                {
                    "node_id": resource.resource_id,
                    "flow_id": flow_id,
                    "resource_type": resource.resource_type.value,
                    "local_name": resource.local_name,
                },
            )

        # Create action-only nodes (namespaced per flow occurrence)
        for node_id in action_only_ids:
            action = parsed.actions[node_id]
            ns_id = namespaced_action_id(flow_id, action.action_id)
            await session.run(
                """
                CREATE (n:ArachneFlowNode:ArachneFlowAction {node_id: $node_id})
                SET n.flow_id = $flow_id,
                    n.node_kind = 'action',
                    n.action_type = $action_type,
                    n.original_action_id = $original_action_id,
                    n.method_ref = $method_ref,
                    n.updated_at = datetime()
                """,
                {
                    "node_id": ns_id,
                    "flow_id": flow_id,
                    "action_type": action.action_type.value,
                    "original_action_id": action.action_id,
                    "method_ref": action.method_ref,
                },
            )

        # Create method nodes (shared by method_id)
        for method in parsed.methods.values():
            await session.run(
                """
                MERGE (n:ArachneFlowNode:ArachneFlowMethod {node_id: $node_id})
                SET n.flow_id = $flow_id,
                    n.node_kind = 'method',
                    n.method_name = $method_name,
                    n.updated_at = datetime()
                """,
                {
                    "node_id": method.method_id,
                    "flow_id": flow_id,
                    "method_name": method.method_name or method.method_id,
                },
            )

        # Create edges
        input_roles = {r.value for r in InputRole}
        output_roles = {r.value for r in OutputRole}
        edge_count = 0
        dual_ids = set(parsed.resources.keys()) & set(parsed.actions.keys())
        for triple in parsed.triples:
            pred = triple.predicate
            src, tgt = _resolve_node_ids(flow_id, triple, dual_ids)
            edge_id = _make_edge_id(flow_id, src, pred, tgt, edge_count)

            if pred in input_roles or pred in output_roles or pred == SpecialRole.NEXT.value:
                await session.run(
                    """
                    MATCH (a:ArachneFlowNode {node_id: $src})
                    MATCH (b:ArachneFlowNode {node_id: $tgt})
                    CREATE (a)-[r:ARACHNE_FLOW {edge_id: $edge_id, flow_id: $flow_id,
                                                edge_namespace: 'arachne_flow',
                                                edge_type: $edge_type,
                                                created_at: datetime()}]->(b)
                    """,
                    {
                        "src": src,
                        "tgt": tgt,
                        "edge_id": edge_id,
                        "flow_id": flow_id,
                        "edge_type": pred,
                    },
                )
            elif pred == SpecialRole.REF.value:
                await session.run(
                    """
                    MATCH (a:ArachneFlowNode {node_id: $src})
                    MATCH (b:ArachneFlowNode {node_id: $tgt})
                    CREATE (a)-[r:ARACHNE_FLOW {edge_id: $edge_id, flow_id: $flow_id,
                                                edge_namespace: 'arachne_flow',
                                                edge_type: 'ref',
                                                created_at: datetime()}]->(b)
                    """,
                    {
                        "src": src,
                        "tgt": tgt,
                        "edge_id": edge_id,
                        "flow_id": flow_id,
                    },
                )
            edge_count += 1

    # Post-pass: stamp Chinese canonical names from the shared PG metadata layer
    # onto resource/dual/method nodes so search and display work in Chinese
    # without per-read PG lookups.
    await _stamp_canonical_names(driver, parsed)

    dual_count = len(set(parsed.resources.keys()) & set(parsed.actions.keys()))
    return {
        "resources": len(parsed.resources),
        "actions": len(parsed.actions),
        "methods": len(parsed.methods),
        "dual": dual_count,
        "edges": len(parsed.triples),
    }


async def _stamp_canonical_names(driver, parsed: ParsedFlow) -> None:
    """Write canonical_name_zh/en from PG industrial_nodes onto flow nodes."""
    candidate_ids = list(
        (set(parsed.resources.keys()) | set(parsed.methods.keys()))
    )
    if not candidate_ids:
        return
    try:
        meta_map = await node_storage.get_nodes_by_ids(candidate_ids)
    except Exception:
        return  # PG unavailable; names stay raw, read-time enrichment still applies
    rows = [
        {"node_id": nid, "zh": meta.canonical_name_zh, "en": meta.canonical_name_en}
        for nid, meta in meta_map.items()
        if meta.canonical_name_zh or meta.canonical_name_en
    ]
    if not rows:
        return
    async with driver.session() as session:
        await session.run(
            """
            UNWIND $rows AS row
            MATCH (n:ArachneFlowNode {node_id: row.node_id})
            SET n.canonical_name_zh = row.zh, n.canonical_name_en = row.en
            """,
            {"rows": rows},
        )


def _resolve_node_ids(
    flow_id: str,
    triple: FlowTriple,
    dual_ids: set,
) -> Tuple[str, str]:
    """Map logical triple source/target to actual Neo4j node IDs."""
    input_roles = {r.value for r in InputRole}
    output_roles = {r.value for r in OutputRole}
    pred = triple.predicate

    def action_node_id(action_id: str) -> str:
        return action_id if action_id in dual_ids else namespaced_action_id(flow_id, action_id)

    if pred in input_roles:
        # [RESOURCE, input_role, ACTION]
        return triple.source, action_node_id(triple.target)
    elif pred in output_roles:
        # [ACTION, output_role, RESOURCE]
        return action_node_id(triple.source), triple.target
    elif pred == SpecialRole.NEXT.value:
        return action_node_id(triple.source), action_node_id(triple.target)
    elif pred == SpecialRole.REF.value:
        return action_node_id(triple.source), triple.target
    return triple.source, triple.target


def _make_edge_id(flow_id: str, src: str, pred: str, tgt: str, idx: int) -> str:
    base = f"{flow_id}:{src}->{tgt}:{pred}"
    if len(base) > 200:
        base = f"{flow_id}:{idx}:{uuid4().hex[:8]}"
    return base


async def clear_flow(flow_id: str) -> None:
    """Remove all edges and orphan nodes belonging to a given flow_id.

    Resource/method nodes are shared across flows, so nodes that still have
    relationships after their flow's edges are removed are kept.
    """
    driver = get_flow_async_driver()
    async with driver.session() as session:
        await session.run(
            """
            MATCH ()-[r:ARACHNE_FLOW {flow_id: $flow_id}]->()
            DELETE r
            """,
            {"flow_id": flow_id},
        )
        await session.run(
            """
            MATCH (n:ArachneFlowNode {flow_id: $flow_id})
            WHERE NOT (n)-[:ARACHNE_FLOW]-()
            DELETE n
            """,
            {"flow_id": flow_id},
        )


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------


async def _enrich_resource(node: GraphNode) -> GraphNode:
    """Merge PostgreSQL metadata into a RESOURCE (or dual) GraphNode if available."""
    if node.entity_type not in {"arachne_flow:resource", "arachne_flow:dual"}:
        return node
    meta = await node_storage.get_node(node.node_id)
    if meta is None:
        return node
    node.label = meta.canonical_name_zh or meta.canonical_name_en or node.label or node.node_id
    node.properties["canonical_name_zh"] = meta.canonical_name_zh
    node.properties["canonical_name_en"] = meta.canonical_name_en
    node.properties["definition"] = meta.definition
    node.properties["aliases"] = meta.aliases
    node.properties["confidence"] = meta.confidence.value if meta.confidence else None
    node.properties["status"] = meta.status.value if meta.status else None
    return node


async def _enrich_method(node: GraphNode) -> GraphNode:
    """Merge PostgreSQL metadata into a METHOD node (method_id == industrial node id)."""
    if node.entity_type != "arachne_flow:method":
        return node
    meta = await node_storage.get_node(node.node_id)
    if meta is None:
        return node
    node.label = meta.canonical_name_zh or meta.canonical_name_en or node.label or node.node_id
    node.properties["canonical_name_zh"] = meta.canonical_name_zh
    node.properties["canonical_name_en"] = meta.canonical_name_en
    node.properties["definition"] = meta.definition
    node.properties["aliases"] = meta.aliases
    return node


async def _enrich_action(node: GraphNode) -> GraphNode:
    """Merge method metadata into an ACTION node via its method_ref.

    Actions are per-flow occurrences with synthetic English ids (act_xxx).
    When they reference a METHOD that maps to an industrial node, borrow its
    Chinese name and definition so details panels read like legacy nodes.
    """
    if node.entity_type != "arachne_flow:action":
        return node
    method_ref = node.properties.get("method_ref")
    if not method_ref:
        return node
    meta = await node_storage.get_node(str(method_ref))
    if meta is None:
        return node
    node.label = meta.canonical_name_zh or meta.canonical_name_en or node.label or node.node_id
    node.properties["method_name_zh"] = meta.canonical_name_zh
    node.properties["method_name_en"] = meta.canonical_name_en
    if not node.properties.get("definition"):
        node.properties["definition"] = meta.definition
    return node


async def _enrich_node(node: GraphNode) -> GraphNode:
    """Dispatch metadata enrichment by node kind (resource/dual/method/action)."""
    node = await _enrich_resource(node)
    node = await _enrich_method(node)
    node = await _enrich_action(node)
    return node


def _to_datetime(value):
    if value is None:
        return None
    if hasattr(value, "to_native"):
        return value.to_native()
    return value


def _serialize_property_value(value):
    if value is None:
        return None
    if hasattr(value, "to_native"):
        return value.to_native()
    if isinstance(value, list):
        return [_serialize_property_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_property_value(v) for k, v in value.items()}
    return value


def _neo4j_node_to_graph_node(record: Dict[str, Any]) -> GraphNode:
    n = record["n"]
    node_id = n["node_id"]
    kind = n.get("node_kind", "resource")
    if kind == "dual":
        entity_type = "arachne_flow:dual"
        label = n.get("canonical_name_zh") or n.get("local_name") or n.get("original_action_id") or node_id
    elif kind == "resource":
        entity_type = "arachne_flow:resource"
        label = n.get("canonical_name_zh") or n.get("local_name") or node_id
    elif kind == "action":
        entity_type = "arachne_flow:action"
        label = n.get("original_action_id") or node_id
    elif kind == "method":
        entity_type = "arachne_flow:method"
        label = n.get("canonical_name_zh") or n.get("method_name") or node_id
    else:
        entity_type = "arachne_flow:unknown"
        label = node_id

    properties = {
        k: _serialize_property_value(v)
        for k, v in dict(n).items()
        if v is not None
    }
    return GraphNode(
        node_id=node_id,
        label=label,
        entity_type=entity_type,
        properties=properties,
    )


def _neo4j_edge_to_graph_edge(record: Dict[str, Any]) -> GraphEdge:
    r = record["r"]
    return GraphEdge(
        edge_id=r.get("edge_id") or str(record.get("rel_id")),
        from_node=record["from_id"],
        to_node=record["to_id"],
        edge_namespace="arachne_flow",
        edge_type=r.get("edge_type", "unknown"),
        properties={
            k: _serialize_property_value(v)
            for k, v in dict(r).items()
            if v is not None
        },
    )


async def get_flow_node(node_id: str) -> Optional[GraphNode]:
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            "MATCH (n:ArachneFlowNode {node_id: $node_id}) RETURN n",
            {"node_id": node_id},
        )
        record = await result.single()
        if record is None:
            return None
        node = _neo4j_node_to_graph_node(record)
        return await _enrich_node(node)


async def list_flow_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[GraphNode], int]:
    driver = get_flow_async_driver()
    where_clauses = []
    params: Dict[str, Any] = {"skip": skip, "limit": limit}

    if entity_type:
        # entity_type is something like "arachne_flow:action"
        kind = entity_type.replace("arachne_flow:", "")
        if kind in {"resource", "action", "method"}:
            where_clauses.append("n.node_kind = $kind")
            params["kind"] = kind

    if search:
        where_clauses.append(
            "(n.node_id CONTAINS $search OR n.local_name CONTAINS $search OR n.method_name CONTAINS $search OR n.original_action_id CONTAINS $search OR n.canonical_name_zh CONTAINS $search OR n.canonical_name_en CONTAINS $search)"
        )
        params["search"] = search

    where = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    async with driver.session() as session:
        count_result = await session.run(
            f"MATCH (n:ArachneFlowNode) {where} RETURN count(n) AS total", params
        )
        count_rec = await count_result.single()
        total = count_rec["total"] if count_rec else 0

        items_result = await session.run(
            f"""
            MATCH (n:ArachneFlowNode) {where}
            RETURN n ORDER BY n.node_id SKIP $skip LIMIT $limit
            """,
            params,
        )
        nodes = [_neo4j_node_to_graph_node(record) async for record in items_result]

    # Enrich nodes (resources/methods/actions) with PG metadata
    enriched = []
    for node in nodes:
        enriched.append(await _enrich_node(node))
    return enriched, total


async def get_flow_edge(edge_id: str) -> Optional[GraphEdge]:
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:ArachneFlowNode)-[r:ARACHNE_FLOW {edge_id: $edge_id}]->(b:ArachneFlowNode)
            RETURN r, a.node_id AS from_id, b.node_id AS to_id
            """,
            {"edge_id": edge_id},
        )
        record = await result.single()
        if record is None:
            return None
        return _neo4j_edge_to_graph_edge(record)


async def list_flow_edges(
    skip: int = 0,
    limit: int = 20,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
) -> Tuple[List[GraphEdge], int]:
    driver = get_flow_async_driver()
    where_clauses = []
    params: Dict[str, Any] = {"skip": skip, "limit": limit}

    if edge_type:
        where_clauses.append("r.edge_type = $edge_type")
        params["edge_type"] = edge_type
    if from_node:
        where_clauses.append("a.node_id = $from_node")
        params["from_node"] = from_node
    if to_node:
        where_clauses.append("b.node_id = $to_node")
        params["to_node"] = to_node

    where = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    async with driver.session() as session:
        count_result = await session.run(
            f"""
            MATCH (a:ArachneFlowNode)-[r:ARACHNE_FLOW]->(b:ArachneFlowNode) {where}
            RETURN count(r) AS total
            """,
            params,
        )
        count_rec = await count_result.single()
        total = count_rec["total"] if count_rec else 0

        items_result = await session.run(
            f"""
            MATCH (a:ArachneFlowNode)-[r:ARACHNE_FLOW]->(b:ArachneFlowNode) {where}
            RETURN r, a.node_id AS from_id, b.node_id AS to_id
            ORDER BY r.edge_id SKIP $skip LIMIT $limit
            """,
            params,
        )
        edges = [_neo4j_edge_to_graph_edge(record) async for record in items_result]
    return edges, total


# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------


async def get_flow_subgraph(
    node_id: str,
    depth: int = 2,
    flow_id: Optional[str] = None,
) -> Tuple[List[GraphNode], List[GraphEdge]]:
    """Return the subgraph around a node.

    When ``flow_id`` is given, traversal only follows edges belonging to that
    flow, so per-flow views do not pull in other flows' occurrences via shared
    resource nodes (e.g. every product flow's packaging/testing actions into
    ``chip``). When omitted, the whole cross-flow ecosystem is traversed.
    """
    driver = get_flow_async_driver()
    flow_filter = (
        "WHERE ALL(rel IN relationships(path) WHERE rel.flow_id = $flow_id)"
        if flow_id
        else ""
    )
    async with driver.session() as session:
        result = await session.run(
            f"""
            MATCH path = (center:ArachneFlowNode {{node_id: $node_id}})-[r:ARACHNE_FLOW*1..{depth}]-(n:ArachneFlowNode)
            {flow_filter}
            RETURN center, nodes(path) AS nodes, relationships(path) AS rels
            LIMIT 1000
            """,
            {"node_id": node_id, "flow_id": flow_id},
        )
        node_map: Dict[str, GraphNode] = {}
        edge_map: Dict[str, GraphEdge] = {}
        async for record in result:
            for n in record["nodes"]:
                nid = n["node_id"]
                if nid not in node_map:
                    node_map[nid] = _neo4j_node_to_graph_node({"n": n})
            for r in record["rels"]:
                eid = r.get("edge_id")
                if eid and eid not in edge_map:
                    edge_map[eid] = GraphEdge(
                        edge_id=eid,
                        from_node=r.start_node["node_id"],
                        to_node=r.end_node["node_id"],
                        edge_namespace="arachne_flow",
                        edge_type=r.get("edge_type", "unknown"),
                        properties={
                            k: _serialize_property_value(v)
                            for k, v in dict(r).items()
                            if v is not None
                        },
                    )
        # Include the center itself even if it has no neighbors.
        if not node_map:
            center = await get_flow_node(node_id)
            if center:
                node_map[node_id] = center

    nodes = list(node_map.values())
    enriched = [await _enrich_node(n) for n in nodes]
    return enriched, list(edge_map.values())


async def get_flow_neighbors(node_id: str) -> Tuple[List[GraphNode], List[GraphEdge]]:
    return await get_flow_subgraph(node_id, depth=1)


async def get_flow_paths(
    from_node: str,
    to_node: str,
    max_depth: int = 5,
) -> List[List[Dict[str, Any]]]:
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH path = (start:ArachneFlowNode {{node_id: $from}})-[:ARACHNE_FLOW*1..{max_depth}]->(end:ArachneFlowNode {{node_id: $to}})
            RETURN [n IN nodes(path) | {{node_id: n.node_id, label: n.node_id}}] AS nodes,
                   [r IN relationships(path) | {{edge_id: r.edge_id, edge_type: r.edge_type}}] AS edges
            LIMIT 100
            """,
            {"from": from_node, "to": to_node},
        )
        paths = []
        async for record in result:
            path = []
            nodes = record["nodes"]
            edges = record["edges"]
            for i, n in enumerate(nodes):
                path.append({"node_id": n["node_id"], "label": n["node_id"]})
                if i < len(edges):
                    path.append({
                        "edge_id": edges[i].get("edge_id"),
                        "edge_type": edges[i].get("edge_type"),
                    })
            paths.append(path)
    return paths


async def get_flow_stats() -> GraphStats:
    driver = get_flow_async_driver()
    async with driver.session() as session:
        node_total_result = await session.run(
            "MATCH (n:ArachneFlowNode) RETURN count(n) AS total"
        )
        node_total_rec = await node_total_result.single()
        node_total = node_total_rec["total"] if node_total_rec else 0

        node_kind_result = await session.run(
            "MATCH (n:ArachneFlowNode) RETURN n.node_kind AS kind, count(*) AS cnt"
        )
        node_kind_counts: Dict[str, int] = {}
        async for rec in node_kind_result:
            node_kind_counts[rec["kind"] or "unknown"] = rec["cnt"]

        edge_total_result = await session.run(
            "MATCH ()-[r:ARACHNE_FLOW]->() RETURN count(r) AS total"
        )
        edge_total_rec = await edge_total_result.single()
        edge_total = edge_total_rec["total"] if edge_total_rec else 0

        edge_type_result = await session.run(
            "MATCH ()-[r:ARACHNE_FLOW]->() RETURN r.edge_type AS etype, count(*) AS cnt"
        )
        edge_type_counts: Dict[str, int] = {}
        async for rec in edge_type_result:
            edge_type_counts[rec["etype"] or "unknown"] = rec["cnt"]

    return GraphStats(
        total_nodes=node_total,
        total_edges=edge_total,
        node_type_distribution=node_kind_counts,
        edge_namespace_distribution={"arachne_flow": edge_total},
        edge_type_distribution=edge_type_counts,
        status_distribution={},
        confidence_distribution={},
    )
