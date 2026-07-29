"""
Integration configuration endpoint.

Arachne is the authority: it prepares a complete integration manifest
that the integrating system fetches to align its JWT issuance, API calls,
and embed URLs. The endpoint lives under a separate prefix (not /api/v1),
is hidden from OpenAPI docs, and only accepts local/private-IP requests
to prevent external discovery.
"""

from __future__ import annotations

import ipaddress

from fastapi import APIRouter, HTTPException, Request

from app.auth import READ_ONLY_POST_PATHS, PermissionScope
from app.config import get_settings

router = APIRouter(include_in_schema=False)
_settings = get_settings()


def _is_local_ip(host: str | None) -> bool:
    """True for loopback or private-network addresses."""
    if not host:
        return False
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_loopback or ip.is_private
    except (ValueError, TypeError):
        return False


@router.get("/config")
async def get_integration_config(request: Request):
    """Complete integration manifest for embedding systems.

    Only accessible from local/private IPs. Excluded from OpenAPI schema.
    """
    client_host = request.client.host if request.client else None
    if not _is_local_ip(client_host):
        raise HTTPException(
            status_code=403,
            detail="Integration config is only available from local networks.",
        )

    auth_section: dict = {
        "mode": _settings.AUTH_MODE,
        "accepted_scopes": [s.value for s in PermissionScope],
        "token_header": "Authorization",
        "token_format": "Bearer <jwt>",
        "required_claims": ["sub", "scope", "exp"],
    }
    if _settings.AUTH_MODE == "jwt":
        auth_section.update(
            {
                "expected_issuer": _settings.JWT_ISSUER,
                "expected_audience": _settings.JWT_AUDIENCE,
                "jwks_url": _settings.JWT_JWKS_URL,
                "jwks_refresh_seconds": _settings.JWT_JWKS_REFRESH_SECONDS,
            }
        )

    return {
        "service": "Arachne Industrial Ontology Graph",
        "version": "1.0.0",
        "auth": auth_section,
        "scope_model": {
            "read_only": "GET requests + read-only POST endpoints only; all mutations blocked (403)",
            "read_write": "all endpoints including create/update/delete",
        },
        "api": {
            "base_url": _settings.API_V1_STR,
            "read_only_post_paths": sorted(READ_ONLY_POST_PATHS),
            "key_endpoints": {
                "reasoning_execute": {
                    "method": "POST",
                    "path": f"{_settings.API_V1_STR}/reasoning/execute",
                    "scope": "read_only",
                },
                "reasoning_query": {
                    "method": "POST",
                    "path": f"{_settings.API_V1_STR}/reasoning/query",
                    "scope": "read_only",
                },
                "node_fuzzy_search": {
                    "method": "GET",
                    "path": f"{_settings.API_V1_STR}/nodes/fuzzy-search",
                    "scope": "read_only",
                },
                "published_views": {
                    "method": "GET",
                    "path": f"{_settings.API_V1_STR}/published-views",
                    "scope": "read_only",
                },
                "create_node": {
                    "method": "POST",
                    "path": f"{_settings.API_V1_STR}/nodes",
                    "scope": "read_write",
                },
            },
        },
        "embed": {
            "reasoning_url_template": "/embed.html?seed={seed}&engine={engine}&task_type={task_type}",
            "published_view_url_template": "/embed.html?view={view_id}",
            "supported_params": {
                "seed": "node ID(s), comma-separated (required)",
                "engine": "arachne_flow | legacy (default: arachne_flow)",
                "task_type": "association | cross_graph_context | ... (default: association)",
                "max_depth": "traversal depth (default: 2)",
                "direction": "forward | backward | both (default: forward)",
                "outputs": "comma-separated OutputType values",
                "resolve": "1 = resolve seed as name via search (default: 0)",
                "view": "published view UUID (loads params from backend)",
                "title": "custom display title",
                "refresh": "1 = re-run even if view has cached snapshot",
            },
            "token_passing": "For authenticated embeds, pass token via postMessage from parent window or httpOnly cookie set by the proxy.",
        },
        "published_views": {
            "create": f"POST {_settings.API_V1_STR}/published-views",
            "get": f"GET {_settings.API_V1_STR}/published-views/{{view_id}}",
            "list": f"GET {_settings.API_V1_STR}/published-views",
            "note": "Store params + optional result_snapshot; embed page loads by view_id for stable short URLs.",
        },
    }
