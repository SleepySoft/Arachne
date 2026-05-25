"""Tests for PostgreSQL infrastructure layer."""

from __future__ import annotations

import os

import pytest

# Skip all tests in this module if POSTGRES_URL is not configured or PostgreSQL is unreachable
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


@pytest.fixture(scope="module")
async def pg_pool():
    from app.database_postgres import get_postgres_pool, close_postgres_pool

    if not await _postgres_available():
        pytest.skip("PostgreSQL not available")

    pool = await get_postgres_pool()
    assert pool is not None
    yield pool
    await close_postgres_pool()


async def test_init_tables_creates_schema(pg_pool):
    from app.database_postgres import init_postgres_tables

    await init_postgres_tables()

    async with pg_pool.acquire() as conn:
        tables = await conn.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN (
                'industries',
                'industry_node_mappings',
                'companies',
                'company_node_exposures'
            )
            ORDER BY table_name
            """
        )
        names = [t["table_name"] for t in tables]
        assert "industries" in names
        assert "industry_node_mappings" in names
        assert "companies" in names
        assert "company_node_exposures" in names


async def test_pool_acquisition_and_close():
    from app.database_postgres import get_postgres_pool, close_postgres_pool

    if not await _postgres_available():
        pytest.skip("PostgreSQL not available")

    pool = await get_postgres_pool()
    assert pool is not None

    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT 1")
        assert result == 1

    await close_postgres_pool()
