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

        # ===================================================================
        # COMPANY SUBGRAPH TABLES (公司子图域)
        # ===================================================================
        # 注意：以下表属于 Company Subgraph Domain，与核心产业图域隔离。
        # company_subgraph_nodes / company_subgraph_edges 中的 node_id / edge_id
        # 是对 IndustrialNode / GraphEdge 的引用，不设外键约束以保持域隔离。
        # ===================================================================

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS company_subgraphs (
                subgraph_id     VARCHAR(128) PRIMARY KEY,
                subgraph_uuid   UUID NOT NULL DEFAULT gen_random_uuid(),
                company_id      VARCHAR(64) NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
                version_name    VARCHAR(128),
                description     TEXT,
                status          VARCHAR(16) NOT NULL DEFAULT 'ACTIVE',
                nodes_summary   JSONB,
                edges_summary   JSONB,
                relations_summary JSONB,
                created_at      TIMESTAMPTZ DEFAULT NOW(),
                updated_at      TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cs_company_id
            ON company_subgraphs(company_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cs_status
            ON company_subgraphs(status)
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS company_subgraph_nodes (
                id              SERIAL PRIMARY KEY,
                subgraph_id     VARCHAR(128) NOT NULL REFERENCES company_subgraphs(subgraph_id) ON DELETE CASCADE,
                node_id         VARCHAR(64) NOT NULL,
                canonical_name_zh VARCHAR(256),
                entity_type     VARCHAR(32),
                activity_type   VARCHAR(32) NOT NULL DEFAULT 'unknown',
                weight          REAL NOT NULL DEFAULT 1.0 CHECK (weight >= 0 AND weight <= 1),
                role            TEXT,
                exposure_confidence VARCHAR(16)
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csn_subgraph
            ON company_subgraph_nodes(subgraph_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csn_node
            ON company_subgraph_nodes(node_id)
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS company_subgraph_edges (
                id              SERIAL PRIMARY KEY,
                subgraph_id     VARCHAR(128) NOT NULL REFERENCES company_subgraphs(subgraph_id) ON DELETE CASCADE,
                edge_id         VARCHAR(128) NOT NULL,
                from_node       VARCHAR(64) NOT NULL,
                to_node         VARCHAR(64) NOT NULL,
                edge_namespace  VARCHAR(32) NOT NULL,
                edge_type       VARCHAR(32) NOT NULL,
                edge_type_label VARCHAR(64),
                description     TEXT,
                confidence      VARCHAR(16)
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_cse_subgraph
            ON company_subgraph_edges(subgraph_id)
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS company_subgraph_relations (
                id              SERIAL PRIMARY KEY,
                subgraph_id     VARCHAR(128) NOT NULL REFERENCES company_subgraphs(subgraph_id) ON DELETE CASCADE,
                from_company_id VARCHAR(64) NOT NULL,
                to_company_id   VARCHAR(64) NOT NULL,
                relation_type   VARCHAR(32) NOT NULL,
                relation_subtype VARCHAR(32),
                strength        REAL NOT NULL DEFAULT 1.0 CHECK (strength >= 0 AND strength <= 1),
                confidence      VARCHAR(16) NOT NULL,
                evidence        JSONB DEFAULT '[]',
                notes           TEXT,
                UNIQUE(subgraph_id, from_company_id, to_company_id, relation_type, relation_subtype)
            )
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csr_subgraph
            ON company_subgraph_relations(subgraph_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csr_type
            ON company_subgraph_relations(relation_type)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csr_from
            ON company_subgraph_relations(from_company_id)
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_csr_to
            ON company_subgraph_relations(to_company_id)
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
