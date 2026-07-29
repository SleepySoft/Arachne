"""Auth scope endpoint - lets the frontend check current permissions."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.auth import resolve_scope
from app.config import get_settings

router = APIRouter()
_settings = get_settings()


@router.get("/scope")
async def get_auth_scope(request: Request):
    """Return the current permission scope and auth mode."""
    return {
        "scope": resolve_scope(request).value,
        "auth_mode": _settings.AUTH_MODE,
    }
