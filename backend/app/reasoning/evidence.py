"""Evidence chain assembly for reasoning outputs."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.engines.legacy.schemas import IndustrialNode
from app.models.core import Evidence
from app.reasoning.schemas import EvidenceChain, EvidenceCompleteness, EvidenceRef, EvidenceSupports, ReasoningPath


def _evidence_to_ref(
    evidence: Evidence,
    source_system: str,
    target_id: str,
    idx: int,
) -> EvidenceRef:
    return EvidenceRef(
        evidence_id=f"{source_system}:{target_id}:{idx}",
        source_system=source_system,  # type: ignore[arg-type]
        source_title=evidence.source_title,
        source_url=str(evidence.source_url) if evidence.source_url else None,
        quote=evidence.quote,
        reliability="MEDIUM",
    )


def _extract_evidence(
    obj: Any,
    source_system: str = "industrial_graph",
) -> List[Evidence]:
    """Extract Evidence list from IndustrialNode, edge model, or dict."""
    if hasattr(obj, "evidence") and not isinstance(obj, dict):
        return list(getattr(obj, "evidence", []) or [])
    if isinstance(obj, dict):
        raw = obj.get("evidence") or []
        if isinstance(raw, str):
            import json
            try:
                raw = json.loads(raw)
            except Exception:
                raw = []
        out = []
        for item in raw:
            if isinstance(item, dict):
                out.append(
                    Evidence(
                        source_title=item.get("source_title", ""),
                        source_url=item.get("source_url"),
                        quote=item.get("quote", ""),
                    )
                )
            elif isinstance(item, Evidence):
                out.append(item)
        return out
    return []


def _target_id_for_node(node: Any) -> str:
    if isinstance(node, IndustrialNode):
        return node.node_id
    if isinstance(node, dict):
        return node.get("node_id", "")
    return str(node)


def _target_id_for_edge(edge: Any) -> str:
    if isinstance(edge, dict):
        return edge.get("edge_id", "")
    if hasattr(edge, "edge_id"):
        return edge.edge_id
    return str(edge)


def _build_chain(
    target_id: str,
    supports: EvidenceSupports,
    evidence_list: List[Evidence],
    source_system: str = "industrial_graph",
) -> EvidenceChain:
    items = [
        _evidence_to_ref(ev, source_system, target_id, idx)
        for idx, ev in enumerate(evidence_list)
    ]
    if not items:
        completeness = EvidenceCompleteness.MISSING
    elif len(items) >= 2:
        completeness = EvidenceCompleteness.COMPLETE
    else:
        completeness = EvidenceCompleteness.PARTIAL

    return EvidenceChain(
        evidence_chain_id=f"ec_{supports.value}_{target_id}_{str(uuid4())[:8]}",
        supports=supports,
        target_id=target_id,
        evidence_items=items,
        completeness=completeness,
    )


def build_evidence_chains(
    nodes: Optional[List[Any]] = None,
    edges: Optional[List[Any]] = None,
    paths: Optional[List[ReasoningPath]] = None,
    source_system: str = "industrial_graph",
) -> List[EvidenceChain]:
    """Build EvidenceChain objects for nodes, edges, and paths."""
    chains: List[EvidenceChain] = []

    for node in nodes or []:
        target_id = _target_id_for_node(node)
        evidence_list = _extract_evidence(node, source_system)
        chains.append(
            _build_chain(target_id, EvidenceSupports.NODE, evidence_list, source_system)
        )

    for edge in edges or []:
        target_id = _target_id_for_edge(edge)
        evidence_list = _extract_evidence(edge, source_system)
        chains.append(
            _build_chain(target_id, EvidenceSupports.EDGE, evidence_list, source_system)
        )

    for path in paths or []:
        # Path evidence chain aggregates edge evidence along the path
        path_evidence: List[Evidence] = []
        for edge in edges or []:
            eid = _target_id_for_edge(edge)
            if eid in path.edge_sequence:
                path_evidence.extend(_extract_evidence(edge, source_system))
        if path_evidence:
            chains.append(
                _build_chain(
                    path.path_id,
                    EvidenceSupports.PATH,
                    path_evidence,
                    source_system,
                )
            )

    return chains
