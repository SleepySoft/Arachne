"""Reasoning engine dispatcher."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

from app.reasoning.schemas import (
    GraphType,
    ObjectCandidate,
    ObjectKind,
    ReasoningDiagnostics,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TaskType,
)
from app.reasoning.tasks.association import run_association
from app.reasoning.tasks.bottleneck_detection import run_bottleneck_detection
from app.reasoning.tasks.candidate_discovery import run_candidate_discovery
from app.reasoning.tasks.cross_graph_context import run_cross_graph_context
from app.reasoning.tasks.impact_propagation import run_impact_propagation
from app.reasoning.tasks.substitution_search import run_substitution_search
from app.reasoning.tasks.utils import validate_source_nodes
from app.services import fuzzy_search


_TASK_DISPATCH: Dict[TaskType, Any] = {
    TaskType.ASSOCIATION: run_association,
    TaskType.IMPACT_PROPAGATION: run_impact_propagation,
    TaskType.BOTTLENECK_DETECTION: run_bottleneck_detection,
    TaskType.SUBSTITUTION_SEARCH: run_substitution_search,
    TaskType.CANDIDATE_DISCOVERY: run_candidate_discovery,
    TaskType.CROSS_GRAPH_CONTEXT: run_cross_graph_context,
}


def _compute_input_fingerprint(task: ReasoningTask) -> str:
    """Deterministic short fingerprint of task inputs."""
    parts = [
        task.task_type.value,
        ",".join(sorted(task.source_nodes)),
        ",".join(sorted(task.source_edges)),
        ",".join(sorted(task.source_claims)),
        ",".join(sorted(task.source_metadata)),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


async def _suggest_similar_nodes(
    missing_ids: list[str],
    limit: int = 3,
) -> dict[str, list[ObjectCandidate]]:
    """Suggest similar existing nodes for missing source IDs."""
    suggestions: dict[str, list[ObjectCandidate]] = {}
    for mid in missing_ids:
        try:
            items = await fuzzy_search.fuzzy_search_nodes(query=mid, limit=limit)
        except Exception:
            continue
        candidates: list[ObjectCandidate] = []
        for item in items:
            node = item["node"]
            candidates.append(
                ObjectCandidate(
                    object_id=node.node_id,
                    object_kind=ObjectKind.NODE,
                    graph=GraphType.INDUSTRIAL,
                    canonical_name=node.canonical_name_zh or node.canonical_name_en,
                    aliases=node.aliases or [],
                    entity_type=node.entity_type,
                    status=node.status,
                    confidence=node.confidence,
                    match_type="keyword",
                    match_score=item["score"],
                )
            )
        if candidates:
            suggestions[mid] = candidates
    return suggestions


async def execute_reasoning_task(task: ReasoningTask) -> ReasoningResultEnvelope:
    """Execute a reasoning task and return a uniform envelope."""
    reasoning_id = f"reasoning_{str(uuid4())[:8]}"
    started_at = datetime.utcnow()

    # Pre-validate sources so we can suggest alternatives for missing IDs
    existing, missing = await validate_source_nodes(task.source_nodes)
    suggestions: dict[str, list[ObjectCandidate]] = {}
    if missing and task.parameters.get("suggest_similar_on_missing", True):
        suggestions = await _suggest_similar_nodes(missing)

    handler = _TASK_DISPATCH.get(task.task_type)
    if handler is None:
        diagnostics = ReasoningDiagnostics(
            warnings=[f"Task type '{task.task_type.value}' is not implemented in V0.2"],
            execution_time_ms=int((datetime.utcnow() - started_at).total_seconds() * 1000),
        )
        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.FAILED,
            generated_at=datetime.utcnow(),
            input_fingerprint=_compute_input_fingerprint(task),
            output_types=[o.value for o in task.requested_outputs],
            result_payload={},
            diagnostics=diagnostics,
        )

    try:
        result = await handler(task, reasoning_id)
        result.input_fingerprint = _compute_input_fingerprint(task)
        if suggestions:
            result.result_payload["missing_source_suggestions"] = {
                mid: [c.model_dump() for c in lst] for mid, lst in suggestions.items()
            }
        return result
    except Exception as exc:
        diagnostics = ReasoningDiagnostics(
            warnings=[f"Execution failed: {type(exc).__name__}: {str(exc)}"],
            execution_time_ms=int((datetime.utcnow() - started_at).total_seconds() * 1000),
        )
        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.FAILED,
            generated_at=datetime.utcnow(),
            input_fingerprint=_compute_input_fingerprint(task),
            output_types=[o.value for o in task.requested_outputs],
            result_payload={},
            diagnostics=diagnostics,
        )
