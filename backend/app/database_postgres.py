"""
PostgreSQL async connection pool for Industry and Company data.

Uses asyncpg for lightweight async PostgreSQL access.
Falls back to a no-op state if PostgreSQL is not available,
allowing the rest of the app to continue using Neo4j.
"""

from __future__ import annotations

import asyncpg
from asyncpg import Pool

from app.config import get_settings

_settings = get_settings()
_pool: Pool | None = None


async def get_postgres_pool() -> Pool | None:
    """Return the shared connection pool, creating it on first call."""
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                _settings.POSTGRES_URL,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
        except Exception:
            # PostgreSQL not available; callers should handle None gracefully
            _pool = None
    return _pool


async def close_postgres_pool() -> None:
    """Close the shared connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def init_postgres_tables() -> None:
    """Create tables if they do not exist."""
    pool = await get_postgres_pool()
    if pool is None:
        return

    async with pool.acquire() as conn:
        # Industries
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS industries (
                industry_id    VARCHAR(64) PRIMARY KEY,
                industry_uuid  UUID NOT NULL DEFAULT gen_random_uuid(),
                name_zh        VARCHAR(256) NOT NULL,
                name_en        VARCHAR(256),
                aliases        TEXT[],
                industry_type  VARCHAR(32) NOT NULL DEFAULT 'curated_view',
                description    TEXT,
                status         VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                notes          TEXT,
                created_at     TIMESTAMPTZ DEFAULT NOW(),
                updated_at     TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_industries_type
            ON industries(industry_type)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_industries_status
            ON industries(status)
            """
        )

        # Industry-Node Mappings
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS industry_node_mappings (
                mapping_id     VARCHAR(128) PRIMARY KEY,
                mapping_uuid   UUID NOT NULL DEFAULT gen_random_uuid(),
                industry_id    VARCHAR(64) NOT NULL REFERENCES industries(industry_id) ON DELETE CASCADE,
                node_id        VARCHAR(64) NOT NULL,
                role           VARCHAR(128),
                weight         REAL NOT NULL DEFAULT 1.0 CHECK (weight >= 0 AND weight <= 1),
                confidence     VARCHAR(16) NOT NULL DEFAULT 'LOW',
                evidence       JSONB DEFAULT '[]',
                status         VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                notes          TEXT,
                created_at     TIMESTAMPTZ DEFAULT NOW(),
                updated_at     TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_inm_industry_id
            ON industry_node_mappings(industry_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_inm_node_id
            ON industry_node_mappings(node_id)
            """
        )

        # Companies
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id     VARCHAR(64) PRIMARY KEY,
                company_uuid   UUID NOT NULL DEFAULT gen_random_uuid(),
                name_zh        VARCHAR(256) NOT NULL,
                name_en        VARCHAR(256),
                aliases        TEXT[],
                stock_codes    TEXT[],
                description    TEXT,
                country        VARCHAR(8) NOT NULL DEFAULT 'CN',
                province       VARCHAR(64),
                city           VARCHAR(64),
                founded_year   INTEGER,
                employee_count INTEGER,
                revenue_cny    BIGINT,
                market_cap_cny BIGINT,
                net_profit_cny BIGINT,
                company_type   VARCHAR(32) NOT NULL DEFAULT 'private',
                status         VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                notes          TEXT,
                created_at     TIMESTAMPTZ DEFAULT NOW(),
                updated_at     TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_companies_country
            ON companies(country)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_companies_type
            ON companies(company_type)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_companies_status
            ON companies(status)
            """
        )

        # Company-Node Exposures
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS company_node_exposures (
                exposure_id    VARCHAR(128) PRIMARY KEY,
                exposure_uuid  UUID NOT NULL DEFAULT gen_random_uuid(),
                company_id     VARCHAR(64) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
                node_id        VARCHAR(64) NOT NULL,
                activity_type  VARCHAR(32) NOT NULL DEFAULT 'unknown',
                role           VARCHAR(256),
                weight         REAL NOT NULL DEFAULT 1.0 CHECK (weight >= 0 AND weight <= 1),
                confidence     VARCHAR(16) NOT NULL DEFAULT 'LOW',
                evidence       JSONB DEFAULT '[]',
                status         VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                as_of_date     DATE,
                notes          TEXT,
                created_at     TIMESTAMPTZ DEFAULT NOW(),
                updated_at     TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cne_company_id
            ON company_node_exposures(company_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cne_node_id
            ON company_node_exposures(node_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cne_activity
            ON company_node_exposures(activity_type)
            """
        )

        # Computation Jobs
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS computation_jobs (
                job_id          VARCHAR(128) PRIMARY KEY,
                job_uuid        UUID NOT NULL DEFAULT gen_random_uuid(),
                job_type        VARCHAR(64) NOT NULL,
                target_id       VARCHAR(128),
                status          VARCHAR(16) NOT NULL DEFAULT 'pending',
                total_items     INTEGER,
                processed_items INTEGER DEFAULT 0,
                result_summary  JSONB,
                error_message   TEXT,
                created_at      TIMESTAMPTZ DEFAULT NOW(),
                started_at      TIMESTAMPTZ,
                completed_at    TIMESTAMPTZ
            )
            """
        )


