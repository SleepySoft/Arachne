"""Integration tests for Business Batch router."""

from __future__ import annotations

import os
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport

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


class TestBusinessBatchRouter:
    async def test_business_batch_lifecycle(self):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        from app.main import app
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # 1. Submit a full batch with industry, company, mapping and exposure
            uid = uuid4().hex[:6]
            batch_id = f"test_batch_{uid}"
            payload = {
                "batch_id": batch_id,
                "task_description": "测试批量注册业务数据",
                "industries_to_upsert": [
                    {
                        "industry_id": f"test_ind_{uid}",
                        "name_zh": f"测试批量行业-{uid}",
                        "industry_type": "curated_view",
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
                "companies_to_upsert": [
                    {
                        "company_id": f"test_co_{uid}",
                        "name_zh": f"测试批量公司-{uid}",
                        "country": "CN",
                        "company_type": "public",
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
                "industry_node_mappings_to_upsert": [
                    {
                        "mapping_id": f"test_map_{uid}",
                        "industry_id": f"test_ind_{uid}",
                        "node_id": "silicon_wafer",
                        "weight": 0.9,
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
                "company_node_exposures_to_upsert": [
                    {
                        "exposure_id": f"test_exp_{uid}",
                        "company_id": f"test_co_{uid}",
                        "node_id": "silicon_wafer",
                        "activity_type": "produce",
                        "weight": 0.8,
                        "status": "ACTIVE",
                        "is_test": True,
                        "evidence": [
                            {
                                "source_title": "测试来源",
                                "quote": "测试公司生产硅片",
                            }
                        ],
                    }
                ],
            }

            resp = await client.post("/api/v1/business-batches", json=payload)
            assert resp.status_code == 201
            data = resp.json()
            assert data["batch_id"] == batch_id
            assert data["industries_created"] == 1
            assert data["companies_created"] == 1
            assert data["mappings_created"] == 1
            assert data["exposures_created"] == 1

            # 2. Upsert an existing industry
            uid2 = uuid4().hex[:6]
            batch_id2 = f"test_batch_up_{uid2}"
            industry_id2 = f"test_ind_up_{uid2}"

            resp1 = await client.post("/api/v1/business-batches", json={
                "batch_id": batch_id2,
                "task_description": "第一次提交",
                "industries_to_upsert": [
                    {
                        "industry_id": industry_id2,
                        "name_zh": "原始名称",
                        "industry_type": "curated_view",
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
            })
            assert resp1.status_code == 201
            assert resp1.json()["industries_created"] == 1

            resp2 = await client.post("/api/v1/business-batches", json={
                "batch_id": batch_id2 + "_2",
                "task_description": "第二次提交",
                "industries_to_upsert": [
                    {
                        "industry_id": industry_id2,
                        "name_zh": "更新后的名称",
                        "industry_type": "curated_view",
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
            })
            assert resp2.status_code == 201
            data2 = resp2.json()
            assert data2["industries_updated"] == 1
            assert data2["industries_created"] == 0

            resp3 = await client.get(f"/api/v1/industries/{industry_id2}")
            assert resp3.status_code == 200
            assert resp3.json()["name_zh"] == "更新后的名称"

            # 3. Mapping deduplication by industry_id + node_id
            uid3 = uuid4().hex[:6]
            batch_id3 = f"test_batch_map_{uid3}"
            industry_id3 = f"test_ind_map_{uid3}"

            resp = await client.post("/api/v1/business-batches", json={
                "batch_id": batch_id3,
                "task_description": "测试映射去重",
                "industries_to_upsert": [
                    {
                        "industry_id": industry_id3,
                        "name_zh": "映射去重测试行业",
                        "status": "ACTIVE",
                        "is_test": True,
                    }
                ],
                "industry_node_mappings_to_upsert": [
                    {
                        "mapping_id": f"map1_{uid3}",
                        "industry_id": industry_id3,
                        "node_id": "lithium_battery_cell",
                        "weight": 0.5,
                        "status": "ACTIVE",
                        "is_test": True,
                    },
                    {
                        "mapping_id": f"map2_{uid3}",
                        "industry_id": industry_id3,
                        "node_id": "lithium_battery_cell",
                        "weight": 0.8,
                        "status": "ACTIVE",
                        "is_test": True,
                    },
                ],
            })
            assert resp.status_code == 201
            data3 = resp.json()
            assert data3["mappings_created"] == 1
            assert data3["mappings_updated"] == 1

            # 4. Empty batch
            uid4 = uuid4().hex[:6]
            resp = await client.post("/api/v1/business-batches", json={
                "batch_id": f"empty_batch_{uid4}",
                "task_description": "空批次测试",
            })
            assert resp.status_code == 201
            data4 = resp.json()
            assert data4["industries_created"] == 0
            assert data4["industries_updated"] == 0
            assert data4["companies_created"] == 0
            assert data4["companies_updated"] == 0
