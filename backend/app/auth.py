"""
Permission framework for the Arachne API.

Pluggable read-only / read-write scope model designed for embedded use:
- The integrating (host) system performs authentication and issues JWTs.
- Arachne verifies JWTs via JWKS (resource-server pattern) and enforces scope.
- Without a valid token, the scope defaults to **read_only** so anonymous
  callers can browse but not mutate.
- A small allowlist of POST endpoints that are semantically read-only
  (reasoning, flow preview, queries) is always permitted.

AUTH_MODE settings (see config.py):
  - "disabled": all operations allowed (standalone mode, read_write)
  - "header":   read X-Arachne-Scope header from integrating system
  - "jwt":      verify Bearer JWT via JWKS; no token = read_only
  - "custom":   reserved hook for future integration
"""

from __future__ import annotations

import asyncio
import time
from enum import Enum
from typing import Any, Awaitable, Callable

import httpx
import jwt
from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import get_settings


class PermissionScope(str, Enum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"


# POST endpoints that are semantically read-only (no data mutation).
READ_ONLY_POST_PATHS: set[str] = {
    "/api/v1/reasoning/query",
    "/api/v1/reasoning/execute",
    "/api/v1/flows/preview",
    "/api/v1/flows/format",
    "/api/v1/flows/subgraph",
    "/api/v1/companies/by-nodes",
    "/api/v1/edges/reified-usage",
}

WRITE_METHODS = {"POST", "PUT", "DELETE", "PATCH"}


# ---------------------------------------------------------------------------
# JWKS cache
# ---------------------------------------------------------------------------

class _JWKSCache:
    """In-memory JWKS cache with TTL-based refresh and key-rotation support."""

    def __init__(self, url: str, refresh_seconds: int):
        self.url = url
        self.refresh_seconds = refresh_seconds
        self._keys: dict[str, Any] = {}
        self._last_fetch: float = 0.0
        self._lock = asyncio.Lock()

    async def get_key(self, kid: str) -> Any | None:
        """Return the public key for *kid*, refreshing the cache if stale."""
        if self._is_stale():
            await self._refresh()
        key = self._keys.get(kid)
        if key is not None:
            return key
        # Key not in cache — maybe it was just rotated. Force one refresh.
        await self._refresh(force=True)
        return self._keys.get(kid)

    def _is_stale(self) -> bool:
        return not self._keys or (time.time() - self._last_fetch > self.refresh_seconds)

    async def _refresh(self, force: bool = False) -> None:
        async with self._lock:
            if not force and not self._is_stale():
                return
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(self.url)
                    resp.raise_for_status()
                    jwks = resp.json()
                new_keys: dict[str, Any] = {}
                for jwk in jwks.get("keys", []):
                    kid = jwk.get("kid")
                    if kid:
                        new_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                if new_keys:
                    self._keys = new_keys
                self._last_fetch = time.time()
            except Exception:
                # Keep stale keys on failure; will retry on next stale check.
                pass


_jwks_cache: _JWKSCache | None = None


def _get_jwks_cache():
    """Return (and lazily create) the singleton JWKS cache."""
    global _jwks_cache
    settings = get_settings()
    if not settings.JWT_JWKS_URL:
        return None
    if _jwks_cache is None or _jwks_cache.url != settings.JWT_JWKS_URL:
        _jwks_cache = _JWKSCache(
            settings.JWT_JWKS_URL, settings.JWT_JWKS_REFRESH_SECONDS
        )
    return _jwks_cache


# ---------------------------------------------------------------------------
# JWT verification
# ---------------------------------------------------------------------------

async def _verify_jwt(request: Request) -> PermissionScope:
    """Verify a Bearer JWT. Returns READ_ONLY if absent or invalid."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return PermissionScope.READ_ONLY

    token = auth_header[7:]
    settings = get_settings()
    cache = _get_jwks_cache()
    if cache is None:
        # JWKS not configured — cannot verify, default to read-only.
        return PermissionScope.READ_ONLY

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            return PermissionScope.READ_ONLY

        key = await cache.get_key(kid)
        if key is None:
            return PermissionScope.READ_ONLY

        decode_kwargs: dict[str, Any] = {"algorithms": ["RS256"]}
        if settings.JWT_ISSUER:
            decode_kwargs["issuer"] = settings.JWT_ISSUER
        if settings.JWT_AUDIENCE:
            decode_kwargs["audience"] = settings.JWT_AUDIENCE

        payload = jwt.decode(token, key=key, **decode_kwargs)
        scope_str = str(payload.get("scope", "read_only")).lower()
        if scope_str in ("read_write", "read-write", "write"):
            return PermissionScope.READ_WRITE
        return PermissionScope.READ_ONLY
    except Exception:
        # Invalid / expired / malformed token — degrade to read-only.
        return PermissionScope.READ_ONLY


# ---------------------------------------------------------------------------
# Scope resolution (pluggable)
# ---------------------------------------------------------------------------

async def resolve_scope(request: Request) -> PermissionScope:
    """Determine the permission scope for the current request.

    This is the pluggable hook: replace or extend to integrate with the
    host system authentication (JWT, session cookie, mTLS, etc.).
    """
    settings = get_settings()
    mode = settings.AUTH_MODE

    if mode == "disabled":
        return PermissionScope.READ_WRITE

    if mode == "header":
        raw = request.headers.get(settings.AUTH_SCOPE_HEADER, "")
        if raw.lower() in ("read_write", "read-write", "write"):
            return PermissionScope.READ_WRITE
        return PermissionScope.READ_ONLY

    if mode == "jwt":
        return await _verify_jwt(request)

    # mode == "custom": reserved for future integration.
    return PermissionScope.READ_WRITE


def is_write_request(request: Request) -> bool:
    """Return True if the request would mutate data and thus requires write scope."""
    if request.method not in WRITE_METHODS:
        return False
    if request.method == "POST":
        path = request.url.path.rstrip("/")
        if path in READ_ONLY_POST_PATHS:
            return False
    return True


async def permission_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable],
):
    """Block write requests when the scope is read-only; tag every response."""
    scope = await resolve_scope(request)
    if scope == PermissionScope.READ_ONLY and is_write_request(request):
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Read-only mode: this operation requires write access.",
                "scope": scope.value,
            },
        )
    response = await call_next(request)
    response.headers["X-Arachne-Scope"] = scope.value
    return response
