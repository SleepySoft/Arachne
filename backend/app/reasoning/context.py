"""Task context parsing and filtering helpers."""

from __future__ import annotations

from typing import Any, Dict

from app.reasoning.schemas import TaskContext


def apply_context_metadata_filter(
    rows: list[Dict[str, Any]],
    context: TaskContext | None,
) -> list[Dict[str, Any]]:
    """Apply metadata_filters from TaskContext to a list of dict rows.

    V0.2 performs simple equality filtering on top-level keys.
    """
    if not context or not context.metadata_filters:
        return rows

    filters = context.metadata_filters
    filtered = []
    for row in rows:
        match = True
        for key, value in filters.items():
            if key in row and row[key] != value:
                match = False
                break
        if match:
            filtered.append(row)
    return filtered
