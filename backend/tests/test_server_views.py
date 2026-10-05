"""Tests for shared server-side canvas views."""

from __future__ import annotations

import os
from uuid import UUID

import pytest
import pytest_asyncio

from app.database_postgres import get_postgres_pool, init_postgres_tables
from app.services import server_view_storage


pytestmark = pytest.mark.asyncio


async def _postgres_available() -> bool:
    try:
        import asyncpg

        url = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5433/arachne")
        conn = await asyncpg.connect(url)
        await conn.close()
        return True
    except Exception:
        return False


@pytest_asyncio.fixture(autouse=True)
async def server_view_table():
    if not await _postgres_available():
        pytest.skip("PostgreSQL not available")
    await init_postgres_tables()
    yield
    pool = await get_postgres_pool()
    if pool:
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM server_views WHERE name LIKE 'test-server-view-%'")


async def test_server_view_crud_and_default_per_workspace():
    industrial = await server_view_storage.create_view(
        "test-server-view-industrial",
        "industrial",
        {"version": 2, "id": "local-industrial", "workspace": "industrial"},
    )
    company = await server_view_storage.create_view(
        "test-server-view-company",
        "company",
        {"version": 2, "id": "local-company", "workspace": "company"},
    )

    updated = await server_view_storage.update_view(
        UUID(industrial["view_id"]),
        "test-server-view-industrial-renamed",
        None,
    )
    assert updated is not None
    assert updated["name"] == "test-server-view-industrial-renamed"

    default_industrial = await server_view_storage.set_default_view(
        UUID(industrial["view_id"])
    )
    default_company = await server_view_storage.set_default_view(
        UUID(company["view_id"])
    )
    assert default_industrial and default_industrial["is_default"]
    assert default_company and default_company["is_default"]
    assert (await server_view_storage.get_default_view("industrial"))["view_id"] == industrial["view_id"]
    assert (await server_view_storage.get_default_view("company"))["view_id"] == company["view_id"]

    industrial_views = await server_view_storage.list_views("industrial")
    assert any(view["view_id"] == industrial["view_id"] for view in industrial_views)

    assert await server_view_storage.delete_view(UUID(industrial["view_id"]))
    assert await server_view_storage.get_default_view("industrial") is None
