"""
Backward-compatibility re-export for legacy-engine database checkers.

The canonical implementation now lives in:
    app.engines.legacy.policies.db_checkers
"""

from __future__ import annotations

from app.engines.legacy.policies.db_checkers import (
    CHECKERS,
    Checker,
    CheckIssue,
    CheckResult,
    FixResult,
    Severity,
    get_checker,
    list_checkers,
    register_checker,
)

__all__ = [
    "CHECKERS",
    "Checker",
    "CheckIssue",
    "CheckResult",
    "FixResult",
    "Severity",
    "get_checker",
    "list_checkers",
    "register_checker",
]
