"""
PostgreSQL async connection pool for Industry and Company data.

Uses asyncpg for lightweight async PostgreSQL access.
Falls back to a no-op state if PostgreSQL is not available,
allowing the rest of the app to continue using Neo4j.
"""

from __future__ import annotations

import asyncio

import asyncpg
from asyncpg import Pool

from app.config import get_settings

_settings = get_settings()
_pool: Pool | None = None
_pool_loop: asyncio.AbstractEventLoop | None = None


async def get_postgres_pool() -> Pool | None:
    """Return the shared connection pool, creating it on first call.

    The pool is bound to the event loop that created it. If the running loop
    changes (e.g. across pytest-asyncio tests), the stale pool is closed and a
    new one is created automatically.
    """
    global _pool, _pool_loop
    current_loop = asyncio.get_running_loop()

    if _pool is not None:
        if _pool_loop is not current_loop or current_loop.is_closed():
            try:
                await _pool.close()
            except Exception:
                pass
            _pool = None
            _pool_loop = None

    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                _settings.POSTGRES_URL,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            _pool_loop = current_loop
        except Exception:
            # PostgreSQL not available; callers should handle None gracefully
            _pool = None
            _pool_loop = None
    return _pool


async def close_postgres_pool() -> None:
    """Close the shared connection pool."""
    global _pool, _pool_loop
    if _pool is not None:
        try:
            await _pool.close()
        except Exception:
            pass
        _pool = None
        _pool_loop = None


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
                updated_at     TIMESTAMPTZ DEFAULT NOW(),
                is_test        BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE industries ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_industries_is_test
            ON industries(is_test)
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
                updated_at     TIMESTAMPTZ DEFAULT NOW(),
                is_test        BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE industry_node_mappings ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_inm_is_test
            ON industry_node_mappings(is_test)
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
                updated_at     TIMESTAMPTZ DEFAULT NOW(),
                is_test        BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE companies ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_companies_is_test
            ON companies(is_test)
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
                updated_at     TIMESTAMPTZ DEFAULT NOW(),
                is_test        BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE company_node_exposures ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cne_is_test
            ON company_node_exposures(is_test)
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

        # Persons (Factual Graph)
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS persons (
                person_id      VARCHAR(64) PRIMARY KEY,
                person_uuid    UUID NOT NULL DEFAULT gen_random_uuid(),
                name_zh        VARCHAR(256) NOT NULL,
                name_en        VARCHAR(256),
                aliases        TEXT[],
                gender         VARCHAR(16),
                birth_year     INTEGER,
                nationality    VARCHAR(64),
                id_card_hash   VARCHAR(256),
                profile        TEXT,
                status         VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                notes          TEXT,
                created_at     TIMESTAMPTZ DEFAULT NOW(),
                updated_at     TIMESTAMPTZ DEFAULT NOW(),
                is_test        BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE persons ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_persons_is_test
            ON persons(is_test)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_persons_status
            ON persons(status)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_persons_name
            ON persons(name_zh)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_persons_id_card_hash
            ON persons(id_card_hash)
            WHERE id_card_hash IS NOT NULL
            """
        )

        # Factual Relations (Factual Graph)
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS factual_relations (
                relation_id      VARCHAR(128) PRIMARY KEY,
                relation_type    VARCHAR(64) NOT NULL,
                relation_domain  VARCHAR(32) NOT NULL,
                from_entity_type VARCHAR(16) NOT NULL,
                from_entity_id   VARCHAR(64) NOT NULL,
                to_entity_type   VARCHAR(16) NOT NULL,
                to_entity_id     VARCHAR(64) NOT NULL,
                subtype          VARCHAR(128),
                equity_ratio     REAL CHECK (equity_ratio >= 0 AND equity_ratio <= 1),
                amount_cny       BIGINT,
                contract_no      VARCHAR(256),
                proportion       REAL CHECK (proportion >= 0 AND proportion <= 1),
                start_date       DATE,
                end_date         DATE,
                is_history       BOOLEAN NOT NULL DEFAULT FALSE,
                evidence         JSONB DEFAULT '[]',
                source           VARCHAR(256) NOT NULL,
                confidence       VARCHAR(16) NOT NULL DEFAULT 'LOW',
                status           VARCHAR(16) NOT NULL DEFAULT 'PENDING',
                notes            TEXT,
                created_at       TIMESTAMPTZ DEFAULT NOW(),
                updated_at       TIMESTAMPTZ DEFAULT NOW(),
                is_test          BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            """
            ALTER TABLE factual_relations ADD COLUMN IF NOT EXISTS is_test BOOLEAN NOT NULL DEFAULT FALSE
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_is_test
            ON factual_relations(is_test)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_domain
            ON factual_relations(relation_domain)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_from_entity
            ON factual_relations(from_entity_type, from_entity_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_to_entity
            ON factual_relations(to_entity_type, to_entity_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_status
            ON factual_relations(status)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_fr_type
            ON factual_relations(relation_type)
            """
        )


