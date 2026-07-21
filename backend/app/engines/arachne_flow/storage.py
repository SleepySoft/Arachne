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
from app.engines.arachne_flow.builder import FlowGraph
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
                ON CREATE SET n.flow_id = $flow_id,
                    n.node_kind = 'dual',
                    n.also_resource = true,
                    n.resource_type = $resource_type,
                    n.action_type = $action_type,
                    n.local_name = $local_name,
                    n.original_action_id = $original_action_id,
                    n.method_ref = $method_ref
                SET n.updated_at = datetime()
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
                ON CREATE SET n.flow_id = $flow_id,
                    n.node_kind = 'resource',
                    n.resource_type = $resource_type,
                    n.local_name = $local_name
                SET n.updated_at = datetime()
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
                ON CREATE SET n.flow_id = $flow_id,
                    n.node_kind = 'method',
                    n.method_name = $method_name
                SET n.updated_at = datetime()
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


async def compile_flow_graph(
    graph: FlowGraph,
    clear_existing: bool = True,
) -> Dict[str, int]:
    """Persist a unified in-memory flow graph to Neo4j.

    This is the batch counterpart to ``compile_parsed_flow``: all files have
    already been merged/deduplicated in memory, so we just write the final
    node/edge set in one pass.
    """
    driver = get_flow_async_driver()

    if clear_existing:
        await _clear_all_flow_data(driver)

    dual_ids = graph.dual_node_ids()

    async with driver.session() as session:
        # 1. Resource nodes (and dual-role nodes).
        for node_id, resource in graph.resources.items():
            if node_id in dual_ids:
                action = graph.actions[node_id]
                await session.run(
                    """
                    MERGE (n:ArachneFlowNode:ArachneFlowResource:ArachneFlowAction {node_id: $node_id})
                    ON CREATE SET n.flow_id = $flow_id,
                        n.node_kind = 'dual',
                        n.also_resource = true,
                        n.resource_type = $resource_type,
                        n.action_type = $action_type,
                        n.local_name = $local_name,
                        n.original_action_id = $original_action_id,
                        n.method_ref = $method_ref
                    SET n.updated_at = datetime()
                    """,
                    {
                        "node_id": node_id,
                        "flow_id": action.flow_id,
                        "resource_type": resource.resource_type.value,
                        "action_type": action.action_type.value,
                        "local_name": resource.local_name,
                        "original_action_id": action.action_id,
                        "method_ref": action.method_ref,
                    },
                )
            else:
                await session.run(
                    """
                    MERGE (n:ArachneFlowNode:ArachneFlowResource {node_id: $node_id})
                    ON CREATE SET n.flow_id = $flow_id,
                        n.node_kind = 'resource',
                        n.resource_type = $resource_type,
                        n.local_name = $local_name
                    SET n.updated_at = datetime()
                    """,
                    {
                        "node_id": node_id,
                        "flow_id": "arachne_flow",
                        "resource_type": resource.resource_type.value,
                        "local_name": resource.local_name,
                    },
                )

        # 2. Method nodes (global singletons).
        for method in graph.methods.values():
            await session.run(
                """
                MERGE (n:ArachneFlowNode:ArachneFlowMethod {node_id: $node_id})
                ON CREATE SET n.flow_id = $flow_id,
                    n.node_kind = 'method',
                    n.method_name = $method_name
                SET n.updated_at = datetime()
                """,
                {
                    "node_id": method.method_id,
                    "flow_id": "arachne_flow",
                    "method_name": method.method_name or method.method_id,
                },
            )

        # 3. Action-only nodes (namespaced per flow occurrence).
        for node_id, action in graph.actions.items():
            if node_id in dual_ids:
                continue
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
                    "node_id": node_id,
                    "flow_id": action.flow_id,
                    "action_type": action.action_type.value,
                    "original_action_id": action.action_id,
                    "method_ref": action.method_ref,
                },
            )

        # 4. Edges.
        for idx, (triple, flow_id) in enumerate(graph.triples):
            edge_id = _make_edge_id(
                flow_id, triple.source, triple.predicate, triple.target, idx
            )
            if triple.predicate == SpecialRole.REF.value:
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
                        "src": triple.source,
                        "tgt": triple.target,
                        "edge_id": edge_id,
                        "flow_id": flow_id,
                    },
                )
            else:
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
                        "src": triple.source,
                        "tgt": triple.target,
                        "edge_id": edge_id,
                        "flow_id": flow_id,
                        "edge_type": triple.predicate,
                    },
                )

    await _stamp_canonical_names_for_graph(driver, graph)

    return {
        "resources": len(graph.resources),
        "methods": len(graph.methods),
        "actions": len(graph.actions),
        "dual": len(dual_ids),
        "edges": len(graph.triples),
    }


async def _clear_all_flow_data(driver) -> None:
    """Remove every arachne-flow node and edge. Used by batch (re)loads."""
    async with driver.session() as session:
        await session.run("MATCH ()-[r:ARACHNE_FLOW]->() DELETE r")
        await session.run("MATCH (n:ArachneFlowNode) DELETE n")


async def _stamp_canonical_names_for_graph(driver, graph: FlowGraph) -> None:
    """Write canonical_name_zh/en from PG industrial_nodes onto flow nodes."""
    candidate_ids = list(set(graph.resources.keys()) | set(graph.methods.keys()))
    if not candidate_ids:
        return
    try:
        meta_map = await node_storage.get_nodes_by_ids(candidate_ids)
    except Exception:
        return
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
            MATCH (n:ArachneFlowNode)
            WHERE NOT (n)-[:ARACHNE_FLOW]-()
            DELETE n
            """,
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


async def get_flow_file_graph(flow_ids: List[str]) -> Tuple[List[GraphNode], List[GraphEdge]]:
    """Return exactly the triples declared by the given flows.

    Unlike a depth-limited traversal from the root product, this returns ALL
    edges whose ``flow_id`` belongs to the selected files plus their endpoint
    nodes — "what you see is what the file declares".
    """
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (a:ArachneFlowNode)-[r:ARACHNE_FLOW]->(b:ArachneFlowNode)
            WHERE r.flow_id IN $flow_ids
            RETURN r, a, b
            LIMIT 5000
            """,
            {"flow_ids": flow_ids},
        )
        node_map: Dict[str, GraphNode] = {}
        edge_map: Dict[str, GraphEdge] = {}
        async for record in result:
            for key in ("a", "b"):
                n = record[key]
                nid = n["node_id"]
                if nid not in node_map:
                    node_map[nid] = _neo4j_node_to_graph_node({"n": n})
            r = record["r"]
            eid = r.get("edge_id")
            if eid:
                edge_map[eid] = GraphEdge(
                    edge_id=eid,
                    from_node=record["a"]["node_id"],
                    to_node=record["b"]["node_id"],
                    edge_namespace="arachne_flow",
                    edge_type=r.get("edge_type", "unknown"),
                    properties={
                        k: _serialize_property_value(v)
                        for k, v in dict(r).items()
                        if v is not None
                    },
                )
    nodes = [await _enrich_node(n) for n in node_map.values()]
    return nodes, list(edge_map.values())


def merged_action_id(merge_key: str) -> str:
    """Node id for a view-layer action node merged across flows."""
    return f"merged_action:{merge_key}"


async def get_merged_flow_graph() -> Tuple[List[GraphNode], List[GraphEdge]]:
    """Full flow graph with cross-flow occurrences merged for readability.

    Merge rules:
    - ACTION occurrences with the same ``method_ref`` (fallback:
      ``original_action_id``) collapse into one action node; per-flow
      provenance is kept in ``flow_ids`` / ``merged_from`` properties.
    - Parallel edges between the same node pair with the same predicate
      aggregate into one edge carrying ``flow_ids`` and ``count``.
    - RESOURCE / METHOD nodes are already shared and pass through unchanged.
    """
    nodes, _ = await list_flow_nodes(skip=0, limit=10000)
    all_edges, _ = await list_flow_edges(skip=0, limit=10000)

    # 1) Determine merge keys for action nodes, but only actually merge when
    # the same method/action is used by actions from more than one distinct flow.
    # Singleton actions and intra-flow repeated methods keep their original
    # namespaced id so product-specific stubs and per-stage processes don't
    # create confusing merged_action:xxx nodes.
    method_labels: Dict[str, str] = {
        n.node_id: n.label for n in nodes if n.entity_type == "arachne_flow:method"
    }
    action_merge_key: Dict[str, str] = {}
    key_flows: Dict[str, Set[str]] = {}
    for n in nodes:
        if n.entity_type != "arachne_flow:action":
            continue
        props = n.properties or {}
        key = str(props.get("method_ref") or props.get("original_action_id") or n.node_id)
        action_merge_key[n.node_id] = key
        flow_id = str(props.get("flow_id") or "")
        key_flows.setdefault(key, set()).add(flow_id)

    merged_actions: Dict[str, GraphNode] = {}
    singleton_action_ids: Set[str] = set()
    for n in nodes:
        if n.entity_type != "arachne_flow:action":
            continue
        props = n.properties or {}
        key = action_merge_key[n.node_id]
        if len(key_flows.get(key, set())) <= 1:
            singleton_action_ids.add(n.node_id)
            continue
        merged_id = merged_action_id(key)
        existing = merged_actions.get(merged_id)
        if existing is None:
            merged_actions[merged_id] = GraphNode(
                node_id=merged_id,
                label=method_labels.get(key) or props.get("method_name_zh") or key,
                entity_type="arachne_flow:action",
                properties={
                    "node_kind": "action",
                    "method_ref": props.get("method_ref"),
                    "original_action_id": props.get("original_action_id") or key,
                    "action_type": props.get("action_type"),
                    "canonical_name_zh": method_labels.get(key),
                    "flow_ids": sorted({props.get("flow_id")} - {None}),
                    "merged_from": [n.node_id],
                },
            )
        else:
            eprops = existing.properties
            flow_ids = set(eprops.get("flow_ids") or [])
            flow_id = props.get("flow_id")
            if flow_id:
                flow_ids.add(flow_id)
            eprops["flow_ids"] = sorted(flow_ids)
            eprops.setdefault("merged_from", []).append(n.node_id)

    def map_node(nid: str) -> str:
        key = action_merge_key.get(nid)
        if key and len(key_flows.get(key, set())) > 1:
            return merged_action_id(key)
        return nid

    # 2) Remap edges and aggregate parallels
    agg: Dict[Tuple[str, str, str], GraphEdge] = {}
    for e in all_edges:
        src = map_node(e.from_node)
        tgt = map_node(e.to_node)
        etype = e.edge_type
        key = (src, tgt, etype)
        flow_id = (e.properties or {}).get("flow_id")
        existing = agg.get(key)
        if existing is None:
            edge_id = f"{src}->{tgt}:{etype}"
            if len(edge_id) > 200:
                edge_id = f"merged:{uuid4().hex[:16]}"
            agg[key] = GraphEdge(
                edge_id=edge_id,
                from_node=src,
                to_node=tgt,
                edge_namespace="arachne_flow",
                edge_type=etype,
                properties={
                    "flow_ids": sorted({flow_id} - {None}),
                    "count": 1,
                    "edge_type": etype,
                },
            )
        else:
            eprops = existing.properties
            flow_ids = set(eprops.get("flow_ids") or [])
            if flow_id:
                flow_ids.add(flow_id)
            eprops["flow_ids"] = sorted(flow_ids)
            eprops["count"] = int(eprops.get("count") or 1) + 1

    out_nodes: List[GraphNode] = [
        n for n in nodes if n.entity_type != "arachne_flow:action"
    ] + list(merged_actions.values())
    # Singleton actions are not merged; keep them as-is.
    out_nodes.extend(
        n for n in nodes
        if n.entity_type == "arachne_flow:action" and n.node_id in singleton_action_ids
    )
    return out_nodes, list(agg.values())


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
