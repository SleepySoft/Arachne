"""
Engine registry for pluggable graph engines.

Engines are registered at application startup. The default engine is "legacy".
"""

from __future__ import annotations

from typing import Dict, Optional

from app.engines.base import GraphEngine


class UnknownEngineError(Exception):
    """Raised when a requested engine has not been registered."""


_engines: Dict[str, GraphEngine] = {}


def register_engine(engine: GraphEngine) -> None:
    """Register a graph engine instance."""
    _engines[engine.name] = engine


def get_engine(name: Optional[str] = None) -> GraphEngine:
    """Return a registered engine by name, defaulting to 'legacy'."""
    engine_name = name or "legacy"
    if engine_name not in _engines:
        raise UnknownEngineError(f"Unknown engine: {engine_name}")
    return _engines[engine_name]


def list_engines() -> list[str]:
    """Return a list of registered engine names."""
    return list(_engines.keys())
