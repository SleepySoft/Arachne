"""
Tests for the pluggable permission framework (read-only / read-write scope).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.auth as auth_mod


class _DisabledSettings:
    AUTH_MODE = "disabled"
    AUTH_SCOPE_HEADER = "X-Arachne-Scope"


class _HeaderSettings:
    AUTH_MODE = "header"
    AUTH_SCOPE_HEADER = "X-Arachne-Scope"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_settings():
    """Ensure get_settings is restored after each test."""
    original = auth_mod.get_settings
    yield
    auth_mod.get_settings = original


def test_disabled_mode_allows_writes(client):
    auth_mod.get_settings = lambda: _DisabledSettings()
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_write"
    # A write POST should not be blocked by the permission layer.
    r = client.post("/api/v1/industries", json={})
    assert r.status_code != 403


def test_header_mode_defaults_read_only(client):
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_only"
    assert r.headers.get("X-Arachne-Scope") == "read_only"


def test_read_only_blocks_write_post(client):
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.post("/api/v1/industries", json={})
    assert r.status_code == 403
    assert "read_only" in r.json()["detail"].lower() or "write" in r.json()["detail"].lower()


def test_read_only_allows_reasoning_execute(client):
    """Reasoning execute is a POST but semantically read-only."""
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.post(
        "/api/v1/reasoning/execute",
        json={
            "task_id": "perm-test",
            "task_type": "association",
            "source_nodes": ["chip"],
            "requested_outputs": ["temporary_graph"],
            "engine": "arachne_flow",
        },
    )
    assert r.status_code != 403


def test_read_only_allows_get(client):
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.get("/api/v1/query/health")
    assert r.status_code != 403


def test_read_write_header_allows_writes(client):
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.post(
        "/api/v1/industries",
        json={},
        headers={"X-Arachne-Scope": "read_write"},
    )
    assert r.status_code != 403


def test_read_only_blocks_delete(client):
    auth_mod.get_settings = lambda: _HeaderSettings()
    r = client.delete("/api/v1/industries/fake-id")
    assert r.status_code == 403
