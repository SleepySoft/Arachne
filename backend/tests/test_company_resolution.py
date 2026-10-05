from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.models.company_schema import Company
from app.routers.companies import resolve_company_by_stock_code


pytestmark = pytest.mark.asyncio


def _company(company_id: str, name: str) -> Company:
    return Company(company_id=company_id, name_zh=name)


async def test_resolver_prefers_stock_code_match():
    match = _company("by_code", "代码命中")
    with (
        patch(
            "app.routers.companies.company_storage.find_companies_by_stock_code",
            AsyncMock(return_value=[match]),
        ),
        patch(
            "app.routers.companies.company_storage.find_companies_by_exact_name",
            AsyncMock(),
        ) as by_name,
    ):
        result = await resolve_company_by_stock_code("300001.SZ", "名称命中")

    assert result.company_id == "by_code"
    by_name.assert_not_awaited()


async def test_resolver_falls_back_to_exact_name():
    match = _company("by_name", "南大光电")
    with (
        patch(
            "app.routers.companies.company_storage.find_companies_by_stock_code",
            AsyncMock(return_value=[]),
        ),
        patch(
            "app.routers.companies.company_storage.find_companies_by_exact_name",
            AsyncMock(return_value=[match]),
        ) as by_name,
    ):
        result = await resolve_company_by_stock_code("300346.SZ", "南大光电")

    assert result.company_id == "by_name"
    by_name.assert_awaited_once_with("南大光电")


async def test_resolver_does_not_fuzzy_match_unknown_company():
    with (
        patch(
            "app.routers.companies.company_storage.find_companies_by_stock_code",
            AsyncMock(return_value=[]),
        ),
        patch(
            "app.routers.companies.company_storage.find_companies_by_exact_name",
            AsyncMock(return_value=[]),
        ),
        pytest.raises(HTTPException) as exc,
    ):
        await resolve_company_by_stock_code("002430.SZ", "杭氧股份")

    assert exc.value.status_code == 404
