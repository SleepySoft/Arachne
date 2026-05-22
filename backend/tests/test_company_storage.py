"""Tests for Company PostgreSQL storage layer."""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from app.database_postgres import get_postgres_pool
from app.models.company_schema import (
    Company,
    CompanyNodeExposure,
    CompanyActivityType,
    CompanyType,
    RecordStatus,
)
from app.services import company_storage

pytestmark = pytest.mark.asyncio


async def _postgres_available() -> bool:
    try:
        import asyncpg
        url = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/arachne")
        conn = await asyncpg.connect(url)
        await conn.close()
        return True
    except Exception:
        return False


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    if not await _postgres_available():
        return
    pool = await get_postgres_pool()
    if pool:
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM company_node_exposures WHERE company_id LIKE 'test_%'")
            await conn.execute("DELETE FROM companies WHERE company_id LIKE 'test_%'")


@pytest.fixture
def sample_company() -> Company:
    uid = uuid4().hex[:6]
    return Company(
        company_id=f"test_longi_{uid}",
        company_uuid=uuid4(),
        name_zh="隆基绿能",
        name_en="LONGi Green Energy",
        aliases=["隆基", "隆基股份"],
        stock_codes=["601012.SH"],
        description="全球最大单晶硅片生产商",
        country="CN",
        province="陕西",
        city="西安",
        founded_year=2000,
        employee_count=60000,
        revenue_cny=128998000000,
        market_cap_cny=150000000000,
        company_type=CompanyType.PUBLIC,
        status=RecordStatus.ACTIVE,
    )


class TestCompanyCRUD:
    async def test_create_and_get(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        created = await company_storage.create_company(sample_company)
        assert created.company_id == sample_company.company_id
        assert created.name_zh == "隆基绿能"
        assert created.stock_codes == ["601012.SH"]
        assert created.revenue_cny == 128998000000

        fetched = await company_storage.get_company(sample_company.company_id)
        assert fetched is not None
        assert fetched.province == "陕西"
        assert founded := fetched.founded_year == 2000

    async def test_update(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        updated = await company_storage.update_company(
            sample_company.company_id,
            {"name_zh": "隆基绿能科技", "employee_count": 65000},
        )
        assert updated is not None
        assert updated.name_zh == "隆基绿能科技"
        assert updated.employee_count == 65000

    async def test_delete(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        ok = await company_storage.delete_company(sample_company.company_id)
        assert ok is True
        assert await company_storage.get_company(sample_company.company_id) is None

    async def test_list_with_filters(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        items, total = await company_storage.list_companies(
            country="CN",
            company_type="public",
            search="隆基",
        )
        assert total >= 1
        assert any(c.company_id == sample_company.company_id for c in items)


class TestExposureCRUD:
    async def test_create_and_list_by_company(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        exp = CompanyNodeExposure(
            exposure_id=f"test_exp_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="silicon_wafer",
            activity_type=CompanyActivityType.PRODUCE,
            role="核心产品",
            weight=0.95,
        )
        created = await company_storage.create_exposure(exp)
        assert created.node_id == "silicon_wafer"
        assert created.activity_type == "produce"

        items, total = await company_storage.list_exposures_by_company(
            sample_company.company_id
        )
        assert total == 1
        assert items[0].weight == 0.95

    async def test_list_by_company_with_activity_filter(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        exp1 = CompanyNodeExposure(
            exposure_id=f"test_exp1_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="silicon_wafer",
            activity_type=CompanyActivityType.PRODUCE,
        )
        exp2 = CompanyNodeExposure(
            exposure_id=f"test_exp2_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="solar_cell",
            activity_type=CompanyActivityType.PRODUCE,
        )
        exp3 = CompanyNodeExposure(
            exposure_id=f"test_exp3_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="rnd_center",
            activity_type=CompanyActivityType.RND,
        )
        await company_storage.create_exposure(exp1)
        await company_storage.create_exposure(exp2)
        await company_storage.create_exposure(exp3)

        items, total = await company_storage.list_exposures_by_company(
            sample_company.company_id,
            activity_type="produce",
        )
        assert total == 2
        assert all(e.activity_type == "produce" for e in items)

    async def test_list_by_node(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        exp = CompanyNodeExposure(
            exposure_id=f"test_exp_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="polysilicon",
            activity_type=CompanyActivityType.PROCURE,
        )
        await company_storage.create_exposure(exp)

        items, total = await company_storage.list_exposures_by_node("polysilicon")
        assert total >= 1
        assert any(e.exposure_id == exp.exposure_id for e in items)

    async def test_cascade_delete_company_deletes_exposures(self, sample_company):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        await company_storage.create_company(sample_company)
        exp = CompanyNodeExposure(
            exposure_id=f"test_exp_{uuid4().hex[:6]}",
            company_id=sample_company.company_id,
            node_id="solar_module",
        )
        await company_storage.create_exposure(exp)

        await company_storage.delete_company(sample_company.company_id)
        assert await company_storage.get_exposure(exp.exposure_id) is None
