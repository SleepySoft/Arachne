"""Tests for JWT local bypass (standalone access in jwt mode)."""

import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.main import app
import app.auth as auth_mod


class _JwtSettingsBypass:
    AUTH_MODE = "jwt"
    AUTH_SCOPE_HEADER = "X-Arachne-Scope"
    JWT_ISSUER = "test-issuer"
    JWT_AUDIENCE = "arachne"
    JWT_JWKS_URL = "https://test-host/.well-known/jwks.json"
    JWT_JWKS_REFRESH_SECONDS = 3600
    JWT_LOCAL_BYPASS = True


class _JwtSettingsNoBypass:
    AUTH_MODE = "jwt"
    AUTH_SCOPE_HEADER = "X-Arachne-Scope"
    JWT_ISSUER = "test-issuer"
    JWT_AUDIENCE = "arachne"
    JWT_JWKS_URL = "https://test-host/.well-known/jwks.json"
    JWT_JWKS_REFRESH_SECONDS = 3600
    JWT_LOCAL_BYPASS = False


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore():
    orig_settings = auth_mod.get_settings
    orig_cache = auth_mod._get_jwks_cache
    orig_local = auth_mod._is_local_ip
    yield
    auth_mod.get_settings = orig_settings
    auth_mod._get_jwks_cache = orig_cache
    auth_mod._is_local_ip = orig_local


def test_local_bypass_gives_read_write(client):
    """When bypass is on and request is local, no token needed for write."""
    auth_mod.get_settings = lambda: _JwtSettingsBypass()
    auth_mod._is_local_ip = lambda host: True  # simulate local access
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_write"
    r = client.post("/api/v1/industries", json={})
    assert r.status_code != 403


def test_local_bypass_off_requires_jwt(client):
    """When bypass is off, local access without token = read_only."""
    auth_mod.get_settings = lambda: _JwtSettingsNoBypass()
    auth_mod._is_local_ip = lambda host: True
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_only"
    r = client.post("/api/v1/industries", json={})
    assert r.status_code == 403


def test_local_bypass_off_with_valid_token(client, tmp_path):
    """When bypass is off but valid JWT present, get read_write."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_jwk = jwt.algorithms.RSAAlgorithm.to_jwk(private_key.public_key(), as_dict=True)
    public_jwk["kid"] = "k1"

    class MockCache:
        async def get_key(self, kid):
            return jwt.algorithms.RSAAlgorithm.from_jwk(public_jwk) if kid == "k1" else None

    auth_mod.get_settings = lambda: _JwtSettingsNoBypass()
    auth_mod._get_jwks_cache = lambda: MockCache()

    token = jwt.encode(
        {"sub": "u", "scope": "read_write", "iss": "test-issuer", "aud": "arachne",
         "exp": int(time.time()) + 3600},
        private_key, algorithm="RS256", headers={"kid": "k1"},
    )
    r = client.get("/api/v1/auth/scope", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["scope"] == "read_write"


def test_non_local_with_bypass_still_needs_jwt(client):
    """Bypass only applies to local IPs; non-local without token = read_only."""
    auth_mod.get_settings = lambda: _JwtSettingsBypass()
    auth_mod._is_local_ip = lambda host: False  # simulate external access
    r = client.get("/api/v1/auth/scope")
    assert r.json()["scope"] == "read_only"
