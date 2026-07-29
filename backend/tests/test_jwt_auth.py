"""Tests for JWT-based authentication (AUTH_MODE=jwt)."""

import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.main import app
import app.auth as auth_mod


# ---------------------------------------------------------------------------
# Fixtures: generate an RSA key pair + mock JWKS cache
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_jwk = jwt.algorithms.RSAAlgorithm.to_jwk(public_key, as_dict=True)
    public_jwk["kid"] = "test-key-1"
    return private_key, public_jwk


class _MockSettings:
    AUTH_MODE = "jwt"
    AUTH_SCOPE_HEADER = "X-Arachne-Scope"
    JWT_ISSUER = "test-issuer"
    JWT_AUDIENCE = "arachne"
    JWT_JWKS_URL = "https://test-host/.well-known/jwks.json"
    JWT_JWKS_REFRESH_SECONDS = 3600
    JWT_LOCAL_BYPASS = False


class _MockCache:
    def __init__(self, public_jwk):
        self._key = jwt.algorithms.RSAAlgorithm.from_jwk(public_jwk)

    async def get_key(self, kid):
        if kid == "test-key-1":
            return self._key
        return None


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_auth():
    """Restore original functions after each test."""
    orig_settings = auth_mod.get_settings
    orig_cache = auth_mod._get_jwks_cache
    yield
    auth_mod.get_settings = orig_settings
    auth_mod._get_jwks_cache = orig_cache


def _setup_jwt(rsa_keys):
    private_key, public_jwk = rsa_keys
    auth_mod.get_settings = lambda: _MockSettings()
    auth_mod._get_jwks_cache = lambda: _MockCache(public_jwk)
    return private_key


def _make_token(private_key, scope="read_write", expired=False, bad_kid=False):
    payload = {
        "sub": "test-user",
        "scope": scope,
        "iss": "test-issuer",
        "aud": "arachne",
        "exp": int(time.time()) - 10 if expired else int(time.time()) + 3600,
    }
    headers = {"kid": "wrong-kid" if bad_kid else "test-key-1"}
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_no_token_defaults_read_only(client, rsa_keys):
    _setup_jwt(rsa_keys)
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_only"
    # Write POST should be blocked
    r = client.post("/api/v1/industries", json={})
    assert r.status_code == 403


def test_valid_read_write_token(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_write")
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["scope"] == "read_write"
    # Write POST should pass the permission layer (may 422 for validation, not 403)
    r = client.post("/api/v1/industries", json={}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code != 403


def test_valid_read_only_token(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_only")
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["scope"] == "read_only"
    r = client.post("/api/v1/industries", json={}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_expired_token_defaults_read_only(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_write", expired=True)
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["scope"] == "read_only"


def test_unknown_kid_defaults_read_only(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_write", bad_kid=True)
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["scope"] == "read_only"


def test_read_only_allows_reasoning_execute(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_only")
    r = client.post(
        "/api/v1/reasoning/execute",
        json={
            "task_id": "jwt-test",
            "task_type": "association",
            "source_nodes": ["chip"],
            "requested_outputs": ["temporary_graph"],
            "engine": "arachne_flow",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code != 403


def test_response_scope_header(client, rsa_keys):
    private_key = _setup_jwt(rsa_keys)
    token = _make_token(private_key, scope="read_write")
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.headers.get("X-Arachne-Scope") == "read_write"
