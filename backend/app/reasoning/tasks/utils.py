"""Shared utilities for reasoning tasks."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from app.database import get_async_driver
from app.models.schemas import Confidence, GraphEdge, IndustrialNode
from app.reasoning.schemas import ReasoningConstraints


CONFIDENCE_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}


def _confidence_rank(conf: Optional[str]) -> int:
    return CONFIDENCE_ORDER.get((conf or "LOW").upper(), 1)


def allowed_confidence_values(
    min_confidence: Confidence,
    include_low_confidence: bool,
) -> List[str]:
    """Return the list of confidence string values that satisfy the constraint."""
    min_rank = _confidence_rank(min_confidence.value)
    values = []
    for name, rank in CONFIDENCE_ORDER.items():
        if rank < min_rank:
            continue
        if name == "LOW" and not include_low_confidence:
            continue
        values.append(name)
    return values


def passes_node_filters(
    node: IndustrialNode,
    constraints: ReasoningConstraints,
) -> bool:
    """Check whether a node passes node-level constraints."""
    if constraints.allowed_node_types and node.entity_type not in constraints.allowed_node_types:
        return False

    if not constraints.include_pending_nodes and node.status != "ACTIVE":
        return False

    if _confidence_rank(node.confidence) < _confidence_rank(constraints.min_node_confidence.value):
        return False

    if constraints.stop_node_types and node.entity_type in constraints.stop_node_types:
        return False

    return True


def passes_edge_filters(
    edge: GraphEdge,
    constraints: ReasoningConstraints,
) -> bool:
    """Check whether an edge passes edge-level constraints."""
    ns = edge.edge_namespace
    if constraints.allowed_edge_namespaces and ns not in constraints.allowed_edge_namespaces:
        return False

    edge_type = getattr(edge, "edge_type", None)
    if constraints.allowed_edge_types and edge_type not in constraints.allowed_edge_types:
        return False

    allowed_confidences = allowed_confidence_values(
        constraints.min_edge_confidence,
        constraints.include_low_confidence_edges,
    )
    if edge.confidence not in allowed_confidences:
        return False

    return True


def build_allowed_rel_types(constraints: ReasoningConstraints) -> str:
    """Build a Cypher relationship type pattern from allowed namespaces."""
    namespaces = constraints.allowed_edge_namespaces
    if not namespaces:
        return "INDUSTRIAL_FLOW|ONTOLOGY"
    parts = []
    for ns in namespaces:
        parts.append(ns.upper())
    return "|".join(parts)


def node_to_dict(node: IndustrialNode) -> Dict[str, Any]:
    """Serialize an IndustrialNode to a plain dict for output."""
    return {
        "node_id": node.node_id,
        "canonical_name_zh": node.canonical_name_zh,
        "canonical_name_en": node.canonical_name_en,
        "entity_type": node.entity_type,
        "confidence": node.confidence,
        "status": node.status,
        "aliases": node.aliases,
        "definition": node.definition,
    }


def edge_to_dict(edge: GraphEdge) -> Dict[str, Any]:
    """Serialize a GraphEdge to a plain dict for output."""
    return {
        "edge_id": edge.edge_id,
        "from_node": edge.from_node,
        "to_node": edge.to_node,
        "edge_namespace": edge.edge_namespace,
        "edge_type": getattr(edge, "edge_type", None),
        "description": edge.description,
        "confidence": edge.confidence,
    }


async def fetch_nodes_by_ids(node_ids: List[str]) -> Dict[str, IndustrialNode]:
    """Fetch IndustrialNode objects by IDs from Neo4j."""
    if not node_ids:
        return {}
    from app.services import neo4j_storage

    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n
            """,
            node_ids=node_ids,
        )
        nodes = {}
        async for record in result:
            node = neo4j_storage._node_from_record(record)
            nodes[node.node_id] = node
        return nodes


async def validate_source_nodes(node_ids: List[str]) -> Tuple[List[str], List[str]]:
    """Return (existing_ids, missing_ids)."""
    nodes = await fetch_nodes_by_ids(node_ids)
    existing = [nid for nid in node_ids if nid in nodes]
    missing = [nid for nid in node_ids if nid not in nodes]
    return existing, missing


def collect_unique_edges(path_records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Collect unique edges from Cypher path records."""
    edges: Dict[str, Dict[str, Any]] = {}
    for record in path_records:
        for rel in record.get("rels", []):
            eid = rel.get("edge_id")
            if eid and eid not in edges:
                edges[eid] = rel
    return edges


def collect_unique_node_ids(path_records: List[Dict[str, Any]]) -> Set[str]:
    """Collect unique node IDs from Cypher path records."""
    node_ids: Set[str] = set()
    for record in path_records:
        node_ids.update(record.get("node_ids", []))
    return node_ids
