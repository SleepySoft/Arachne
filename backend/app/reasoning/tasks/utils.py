"""Shared utilities for reasoning tasks."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from app.engines.legacy.schemas import GraphEdge, IndustrialNode
from app.models.core import Confidence
from app.reasoning.schemas import (
    CompanyExposureInfo,
    CompanyExposuresOutput,
    ExposedNodeInfo,
    ReasoningConstraints,
)


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
    """Build a Cypher relationship type pattern from allowed namespaces.

    When the caller does not explicitly request namespaces, the default is
    ``INDUSTRIAL_FLOW`` only. Ontology/topology edges are opt-in because they
    represent taxonomic/structural relationships and should not be mixed into
    supply-chain traversal by default.
    """
    namespaces = constraints.allowed_edge_namespaces
    if not namespaces:
        return "INDUSTRIAL_FLOW"
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
    """Fetch IndustrialNode objects by IDs from PostgreSQL."""
    if not node_ids:
        return {}
    from app.services import node_storage

    return await node_storage.get_nodes_by_ids(node_ids)


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


async def build_company_exposures(
    node_ids: List[str],
    max_exposures: int = 50,
) -> Optional[CompanyExposuresOutput]:
    """Build a company exposure summary for a set of industrial nodes.

    Returns companies grouped by company_id, each listing the nodes they expose.
    The total number of exposure records is capped by max_exposures.
    """
    if not node_ids:
        return None
    try:
        from app.services import company_storage
    except Exception:
        return None

    exposures = await company_storage.list_exposures_by_nodes(node_ids, limit=max_exposures)
    if not exposures:
        return None

    company_ids = list({e.company_id for e in exposures})
    companies = await company_storage.get_companies_by_ids(company_ids)
    company_map = {c.company_id: c for c in companies}

    grouped: Dict[str, CompanyExposureInfo] = {}
    for e in exposures:
        company = company_map.get(e.company_id)
        if company is None:
            continue
        if company.company_id not in grouped:
            grouped[company.company_id] = CompanyExposureInfo(
                company_id=company.company_id,
                name_zh=company.name_zh,
                name_en=company.name_en,
                stock_codes=company.stock_codes or [],
                company_type=company.company_type.value if company.company_type else None,
                exposed_nodes=[],
            )
        grouped[company.company_id].exposed_nodes.append(
            ExposedNodeInfo(
                node_id=e.node_id,
                activity_type=e.activity_type.value if e.activity_type else None,
                role=e.role,
                weight=e.weight,
                confidence=e.confidence.value if e.confidence else None,
            )
        )

    # Enrich exposed nodes with names/entity_type from the industrial graph
    nodes_map = await fetch_nodes_by_ids(node_ids)
    for info in grouped.values():
        for exposed in info.exposed_nodes:
            node = nodes_map.get(exposed.node_id)
            if node:
                exposed.canonical_name_zh = node.canonical_name_zh
                exposed.canonical_name_en = node.canonical_name_en
                exposed.entity_type = node.entity_type

    company_list = list(grouped.values())
    return CompanyExposuresOutput(
        total_companies=len(company_list),
        total_exposures=sum(len(c.exposed_nodes) for c in company_list),
        companies=company_list,
    )
