"""Tests for engine discovery and metadata endpoints."""

from __future__ import annotations

import httpx
import pytest
from httpx import ASGITransport

pytestmark = pytest.mark.asyncio


async def test_list_engines_returns_registered_engines():
    # Register engines explicitly; AsyncClient with ASGITransport does not run
    # the application's lifespan startup handlers in this test setup.
    from app.engines.arachne_flow.engine import ArachneFlowEngine
    from app.engines.legacy.engine import LegacyEngine
    from app.main import app
    from app.services.engine_registry import register_engine

    register_engine(LegacyEngine())
    register_engine(ArachneFlowEngine())

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/v1/engines")
    assert response.status_code == 200
    data = response.json()
    assert "engines" in data
    assert "default" in data

    names = [e["name"] for e in data["engines"]]
    assert "legacy" in names
    assert "arachne_flow" in names
    assert data["default"] == "legacy"

    legacy = next(e for e in data["engines"] if e["name"] == "legacy")
    assert legacy["is_read_only"] is False
    assert legacy["supports_flows"] is False
    assert legacy["default_view"] == "industrial_graph"

    flow = next(e for e in data["engines"] if e["name"] == "arachne_flow")
    assert flow["is_read_only"] is True
    assert flow["supports_flows"] is True
    assert flow["default_view"] == "flow_graph"
