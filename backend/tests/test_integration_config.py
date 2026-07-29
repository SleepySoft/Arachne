"""Tests for the /integration/config endpoint (local-IP restricted)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.routers.integration as integration_mod


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_ip_check():
    original = integration_mod._is_local_ip
    yield
    integration_mod._is_local_ip = original


def test_config_blocked_for_non_local(client):
    """TestClient host is 'testclient' which is not a valid IP -> blocked."""
    r = client.get("/integration/config")
    assert r.status_code == 403


def test_config_returns_manifest_for_local(client):
    integration_mod._is_local_ip = lambda host: True
    r = client.get("/integration/config")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "Arachne Industrial Ontology Graph"
    assert "auth" in data
    assert "accepted_scopes" in data["auth"]
    assert "read_only" in data["auth"]["accepted_scopes"]
    assert "read_write" in data["auth"]["accepted_scopes"]
    assert "api" in data
    assert "embed" in data
    assert "published_views" in data


def test_config_includes_read_only_post_paths(client):
    integration_mod._is_local_ip = lambda host: True
    r = client.get("/integration/config")
    data = r.json()
    paths = data["api"]["read_only_post_paths"]
    assert "/api/v1/reasoning/execute" in paths
    assert "/api/v1/reasoning/query" in paths


def test_config_embed_templates(client):
    integration_mod._is_local_ip = lambda host: True
    r = client.get("/integration/config")
    data = r.json()
    assert "seed={seed}" in data["embed"]["reasoning_url_template"]
    assert "view={view_id}" in data["embed"]["published_view_url_template"]


def test_config_not_in_openapi(client):
    """The endpoint should be hidden from the OpenAPI schema."""
    r = client.get("/api/v1/openapi.json")
    schema = r.json()
    paths = schema.get("paths", {})
    assert "/integration/config" not in paths
