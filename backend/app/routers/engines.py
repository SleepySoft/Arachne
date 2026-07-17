"""Engine discovery endpoint.

Returns the list of registered graph engines and their capabilities so the
frontend can render the engine switcher without hard-coding engine names.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.models.core import EngineList, EngineMetadata
from app.services.engine_registry import get_engine, list_engines

router = APIRouter()


@router.get("", response_model=EngineList)
async def list_engines_info():
    """List all registered graph engines with metadata and default engine."""
    engines = [get_engine(name).metadata for name in list_engines()]
    # Ensure legacy is advertised as the default when available.
    default = "legacy" if any(e.name == "legacy" for e in engines) else (engines[0].name if engines else "")
    return EngineList(engines=engines, default=default)
