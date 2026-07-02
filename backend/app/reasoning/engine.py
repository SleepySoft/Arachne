"""Reasoning engine dispatcher."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

from app.reasoning.schemas import (
    ReasoningDiagnostics,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TaskType,
)
from app.reasoning.tasks.association import run_association
from app.reasoning.tasks.impact_propagation import run_impact_propagation


_TASK_DISPATCH: Dict[TaskType, Any] = {
    TaskType.ASSOCIATION: run_association,
    TaskType.IMPACT_PROPAGATION: run_impact_propagation,
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


async def execute_reasoning_task(task: ReasoningTask) -> ReasoningResultEnvelope:
    """Execute a reasoning task and return a uniform envelope."""
    reasoning_id = f"reasoning_{str(uuid4())[:8]}"
    started_at = datetime.utcnow()

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
