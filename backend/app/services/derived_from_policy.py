"""
Backward-compatibility re-export for the legacy-engine derived_from policy.

The canonical implementation now lives in:
    app.engines.legacy.policies.derived_from_policy
"""

from __future__ import annotations

from app.engines.legacy.policies.derived_from_policy import (
    GENERIC_CONSUMABLE_IDS,
    is_generic_consumable,
    validate_derived_from_edge,
)

__all__ = [
    "GENERIC_CONSUMABLE_IDS",
    "is_generic_consumable",
    "validate_derived_from_edge",
]
