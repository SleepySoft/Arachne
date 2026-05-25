"""Tests for Industry PostgreSQL storage layer."""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from app.database_postgres import get_postgres_pool
from app.models.industry_schema import (
    Industry,
    IndustryCreate,
    IndustryNodeMapping,
    IndustryType,
    RecordStatus,
)
from app.services import industry_storage

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


@pytest.fixture(autouse=True)
async def cleanup():
    """Auto-cleanup after each test."""
    yield
    if not await _postgres_available():
        return
    # Clean up test data
    pool = await get_postgres_pool()
    if pool:
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM industry_node_mappings WHERE industry_id LIKE 'test_%'")
            await conn.execute("DELETE FROM industries WHERE industry_id LIKE 'test_%'")


@pytest.fixture
async def sample_industry() -> Industry:
    return Industry(
        industry_id=f"test_solar_{uuid4().hex[:6]}",
        industry_uuid=uuid4(),
        name_zh="测试光伏行业",
        name_en="Test Solar Industry",
        aliases=["光伏", "太阳能"],
        industry_type=IndustryType.CURATED_VIEW,
        description="用于测试的光伏行业",
        status=RecordStatus.ACTIVE,
    )


class TestIndustryCRUD:
    async def test_create_and_get(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        created = await industry_storage.create_industry(sample_industry)
        assert created.industry_id == sample_industry.industry_id
        assert created.name_zh == sample_industry.name_zh

        fetched = await industry_storage.get_industry(sample_industry.industry_id)
        assert fetched is not None
        assert fetched.name_zh == "测试光伏行业"
        assert fetched.aliases == ["光伏", "太阳能"]

    async def test_update(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        updated = await industry_storage.update_industry(
            sample_industry.industry_id,
            {"name_zh": "更新后的名称", "description": "新描述"},
        )
        assert updated is not None
        assert updated.name_zh == "更新后的名称"
        assert updated.description == "新描述"

    async def test_delete(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        ok = await industry_storage.delete_industry(sample_industry.industry_id)
        assert ok is True

        fetched = await industry_storage.get_industry(sample_industry.industry_id)
        assert fetched is None

    async def test_list_with_filter(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        items, total = await industry_storage.list_industries(
            search="测试光伏",
            limit=10,
        )
        assert total >= 1
        assert any(i.industry_id == sample_industry.industry_id for i in items)


class TestMappingCRUD:
    async def test_create_and_list_by_industry(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        mapping = IndustryNodeMapping(
            mapping_id=f"test_map_{uuid4().hex[:6]}",
            industry_id=sample_industry.industry_id,
            node_id="silicon_wafer",
            role="核心产品",
            weight=0.9,
        )
        created = await industry_storage.create_mapping(mapping)
        assert created.mapping_id == mapping.mapping_id
        assert created.node_id == "silicon_wafer"

        items, total = await industry_storage.list_mappings_by_industry(
            sample_industry.industry_id
        )
        assert total == 1
        assert items[0].node_id == "silicon_wafer"

    async def test_list_by_node(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        mapping = IndustryNodeMapping(
            mapping_id=f"test_map_{uuid4().hex[:6]}",
            industry_id=sample_industry.industry_id,
            node_id="polysilicon",
            role="上游材料",
            weight=0.8,
        )
        await industry_storage.create_mapping(mapping)

        items, total = await industry_storage.list_mappings_by_node("polysilicon")
        assert total >= 1
        assert any(m.mapping_id == mapping.mapping_id for m in items)

    async def test_delete_mapping(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        mapping = IndustryNodeMapping(
            mapping_id=f"test_map_{uuid4().hex[:6]}",
            industry_id=sample_industry.industry_id,
            node_id="solar_cell",
        )
        await industry_storage.create_mapping(mapping)

        ok = await industry_storage.delete_mapping(mapping.mapping_id)
        assert ok is True

        fetched = await industry_storage.get_mapping(mapping.mapping_id)
        assert fetched is None

    async def test_cascade_delete_industry_deletes_mappings(self, sample_industry):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await industry_storage.create_industry(sample_industry)
        mapping = IndustryNodeMapping(
            mapping_id=f"test_map_{uuid4().hex[:6]}",
            industry_id=sample_industry.industry_id,
            node_id="solar_module",
        )
        await industry_storage.create_mapping(mapping)

        await industry_storage.delete_industry(sample_industry.industry_id)

        fetched = await industry_storage.get_mapping(mapping.mapping_id)
        assert fetched is None
