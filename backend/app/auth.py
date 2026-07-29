"""
Permission framework for the Arachne API.

Pluggable read-only / read-write scope model designed for embedded use:
- The integrating (host) system performs authentication and conveys the
  resulting permission scope to Arachne via an HTTP header.
- Arachne enforces the scope: read-only blocks all mutating endpoints.
- A small allowlist of POST endpoints that are semantically read-only
  (reasoning, flow preview, queries) is always permitted.

AUTH_MODE settings (see config.py):
  - "disabled" (default): all operations allowed (standalone mode)
  - "header": read the configured header ("read_only" | "read_write");
              defaults to read_only when the header is absent
  - "custom": reserved hook for future token/session-based integration
"""

from __future__ import annotations

from enum import Enum
from typing import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import get_settings


class PermissionScope(str, Enum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"


# POST endpoints that are semantically read-only (no data mutation).
# These remain available even when the scope is read_only.
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


def resolve_scope(request: Request) -> PermissionScope:
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

    # mode == "custom": reserved for future integration.
    # Implement custom logic here (e.g. decode JWT, call an auth service).
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
    scope = resolve_scope(request)
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
