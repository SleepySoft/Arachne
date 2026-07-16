"""Diagnostics collection for reasoning tasks."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.engines.legacy.schemas import GraphEdge, IndustrialNode
from app.reasoning.schemas import ReasoningDiagnostics


def build_diagnostics(
    nodes: List[IndustrialNode],
    edges: List[Any],
    diagnostics: ReasoningDiagnostics,
    warnings: List[str],
    started_at: datetime,
) -> ReasoningDiagnostics:
    """Finalize diagnostics from collected nodes/edges and warnings."""
    missing_evidence = 0
    low_confidence_nodes = 0
    pending_nodes = 0

    for node in nodes:
        if node.status == "PENDING":
            pending_nodes += 1
        if not node.evidence:
            missing_evidence += 1
        if node.confidence == "LOW":
            low_confidence_nodes += 1

    low_confidence_edges = 0
    for edge in edges:
        conf = getattr(edge, "confidence", None) or edge.get("confidence") if isinstance(edge, dict) else None
        if conf == "LOW":
            low_confidence_edges += 1
        # dict edges don't carry evidence list in the temp record
        if not isinstance(edge, dict) and not getattr(edge, "evidence", None):
            missing_evidence += 1

    diagnostics.missing_evidence_count = missing_evidence
    diagnostics.low_confidence_node_count = low_confidence_nodes
    diagnostics.low_confidence_edge_count = low_confidence_edges
    diagnostics.pending_node_count = pending_nodes
    diagnostics.warnings = warnings
    diagnostics.execution_time_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)
    return diagnostics
