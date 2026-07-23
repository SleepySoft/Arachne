"""Arachne-flow reasoning adapter: translate arachne-flow graph queries to the reasoning framework.

The reasoning tasks were designed for the legacy graph (:IndustrialNode + industrial_flow/ontology).
This adapter provides the same graph-access patterns for the arachne-flow graph
(:ArachneFlowNode + :ARACHNE_FLOW) so reasoning tasks can run on the arachne_flow engine.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from app.database_flow import get_flow_async_driver
from app.engines.arachne_flow import storage as flow_storage
from app.models.core import GraphEdge, GraphNode


# Arachne-flow input/output roles that participate in material/process flow traversal.
INPUT_ROLES = {
    "feedstock",
    "component",
    "additive",
    "process_material",
    "catalyst",
    "energy",
    "carrier",
    "tool",
    "packaging",
    "subject",
    "basis",
    "requirement",
}
OUTPUT_ROLES = {
    "primary_result",
    "co_result",
    "intermediate",
    "byproduct",
    "scrap",
    "waste",
    "emission",
    "recovered_resource",
}
FLOW_ROLES = INPUT_ROLES | OUTPUT_ROLES | {"next"}
# ref edges are used for method-based expansion, not flow traversal.
SPECIAL_ROLES = {"ref", "next"}


async def fetch_arachne_flow_node(node_id: str) -> Optional[GraphNode]:
    """Fetch an arachne-flow node by id."""
    return await flow_storage.get_flow_node(node_id)


async def fetch_arachne_flow_nodes(node_ids: List[str]) -> Dict[str, GraphNode]:
    """Fetch multiple arachne-flow nodes by ids."""
    result: Dict[str, GraphNode] = {}
    for nid in node_ids:
        node = await flow_storage.get_flow_node(nid)
        if node:
            result[nid] = node
    return result


async def validate_arachne_flow_sources(node_ids: List[str]) -> Tuple[List[str], List[str]]:
    """Validate which node ids exist in the arachne-flow graph.

    Returns:
        (existing_ids, missing_ids)
    """
    if not node_ids:
        return [], []
    driver = get_flow_async_driver()
    async with driver.session() as session:
        result = await session.run(
            "MATCH (n:ArachneFlowNode) WHERE n.node_id IN $ids RETURN n.node_id AS id",
            {"ids": node_ids},
        )
        existing = {record["id"] async for record in result}
    existing_list = [nid for nid in node_ids if nid in existing]
    missing_list = [nid for nid in node_ids if nid not in existing]
    return existing_list, missing_list


async def fetch_arachne_flow_paths(
    source_id: str,
    max_depth: int,
    direction: str,
    limit: int,
) -> List[Dict[str, Any]]:
    """Fetch paths from an arachne-flow source node using :ARACHNE_FLOW edges.

    Traversal follows input/output roles (material/process flow) and next edges.
    """
    driver = get_flow_async_driver()
    rel_pattern = "|".join(FLOW_ROLES)

    if direction == "forward":
        rel_clause = f"-[r:ARACHNE_FLOW*1..{max_depth}]->"
    else:
        rel_clause = f"<-[r:ARACHNE_FLOW*1..{max_depth}]-"

    cypher = f"""
    MATCH path = (src:ArachneFlowNode {{node_id: $source_id}}){rel_clause}(dst:ArachneFlowNode)
    WHERE all(rel IN relationships(path) WHERE rel.edge_type IN $roles)
    RETURN [n IN nodes(path) | n.node_id] AS node_ids,
           [rel IN relationships(path) | {{
                edge_id: rel.edge_id,
                edge_namespace: rel.edge_namespace,
                edge_type: rel.edge_type,
                from_node: startNode(rel).node_id,
                to_node: endNode(rel).node_id,
                flow_id: rel.flow_id,
                created_at: rel.created_at
           }}] AS rels
    LIMIT $limit
    """

    paths: List[Dict[str, Any]] = []
    async with driver.session() as session:
        result = await session.run(
            cypher,
            {"source_id": source_id, "roles": list(FLOW_ROLES), "limit": limit},
        )
        async for record in result:
            paths.append({"node_ids": record["node_ids"], "rels": record["rels"]})
    return paths


async def expand_by_method_ref(node_ids: List[str], direction: str = "both") -> Set[str]:
    """Expand arachne-flow nodes via method_ref relationships.

    - For ACTION nodes, add their referenced METHOD node.
    - For METHOD nodes, add all ACTION nodes that reference them.
    """
    if not node_ids:
        return set()
    expanded: Set[str] = set(node_ids)
    driver = get_flow_async_driver()

    async with driver.session() as session:
        # Actions -> their methods
        result = await session.run(
            """
            MATCH (a:ArachneFlowAction)-[r:ARACHNE_FLOW {edge_type: 'ref'}]->(m:ArachneFlowMethod)
            WHERE a.node_id IN $ids
            RETURN m.node_id AS method_id
            """,
            {"ids": node_ids},
        )
        async for record in result:
            expanded.add(record["method_id"])

        # Methods -> their actions
        result = await session.run(
            """
            MATCH (a:ArachneFlowAction)-[r:ARACHNE_FLOW {edge_type: 'ref'}]->(m:ArachneFlowMethod)
            WHERE m.node_id IN $ids
            RETURN a.node_id AS action_id
            """,
            {"ids": node_ids},
        )
        async for record in result:
            expanded.add(record["action_id"])

    return expanded


def map_arachne_flow_node_to_reasoning(node: GraphNode) -> Dict[str, Any]:
    """Convert an arachne-flow GraphNode to a reasoning node dict."""
    props = node.properties or {}
    return {
        "node_id": node.node_id,
        "label": node.label,
        "entity_type": node.entity_type,
        "node_kind": props.get("node_kind"),
        "flow_id": props.get("flow_id"),
        "flow_ids": props.get("flow_ids"),
        "method_ref": props.get("method_ref"),
        "original_action_id": props.get("original_action_id"),
        "resource_type": props.get("resource_type"),
        "action_type": props.get("action_type"),
        "canonical_name_zh": props.get("canonical_name_zh"),
        "canonical_name_en": props.get("canonical_name_en"),
    }


def map_arachne_flow_edge_to_reasoning(edge: GraphEdge) -> Dict[str, Any]:
    """Convert an arachne-flow GraphEdge to a reasoning edge dict."""
    props = edge.properties or {}
    return {
        "edge_id": edge.edge_id,
        "from_node": edge.from_node,
        "to_node": edge.to_node,
        "edge_namespace": edge.edge_namespace,
        "edge_type": edge.edge_type,
        "flow_id": props.get("flow_id"),
        "flow_ids": props.get("flow_ids"),
        "count": props.get("count"),
    }
