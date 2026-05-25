"""Integration tests for Business Batch router."""

from __future__ import annotations

import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

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


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


class TestBusinessBatchRouter:
    async def test_submit_business_batch(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        batch_id = f"test_batch_{uid}"

        payload = {
            "batch_id": batch_id,
            "task_description": "测试批量注册业务数据",
            "industries_to_upsert": [
                {
                    "industry_id": f"test_ind_{uid}",
                    "name_zh": "测试批量行业",
                    "industry_type": "curated_view",
                    "status": "ACTIVE",
                }
            ],
            "companies_to_upsert": [
                {
                    "company_id": f"test_co_{uid}",
                    "name_zh": "测试批量公司",
                    "country": "CN",
                    "company_type": "public",
                    "status": "ACTIVE",
                }
            ],
            "industry_node_mappings_to_upsert": [
                {
                    "mapping_id": f"test_map_{uid}",
                    "industry_id": f"test_ind_{uid}",
                    "node_id": "silicon_wafer",
                    "weight": 0.9,
                    "status": "ACTIVE",
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
                }
            ],
        }

        resp = client.post("/api/v1/business-batches", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["batch_id"] == batch_id
        assert data["industries_created"] >= 1
        assert data["companies_created"] >= 1
        assert data["mappings_created"] >= 1
        assert data["exposures_created"] >= 1

    async def test_business_batch_upsert_existing(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        batch_id = f"test_batch_up_{uid}"
        industry_id = f"test_ind_up_{uid}"

        # First submission
        payload1 = {
            "batch_id": batch_id,
            "task_description": "第一次提交",
            "industries_to_upsert": [
                {
                    "industry_id": industry_id,
                    "name_zh": "原始名称",
                    "industry_type": "curated_view",
                    "status": "ACTIVE",
                }
            ],
        }
        resp1 = client.post("/api/v1/business-batches", json=payload1)
        assert resp1.status_code == 201
        assert resp1.json()["industries_created"] == 1

        # Second submission with same industry_id (should update)
        payload2 = {
            "batch_id": batch_id + "_2",
            "task_description": "第二次提交",
            "industries_to_upsert": [
                {
                    "industry_id": industry_id,
                    "name_zh": "更新后的名称",
                    "industry_type": "curated_view",
                    "status": "ACTIVE",
                }
            ],
        }
        resp2 = client.post("/api/v1/business-batches", json=payload2)
        assert resp2.status_code == 201
        data2 = resp2.json()
        assert data2["industries_updated"] == 1
        assert data2["industries_created"] == 0

        # Verify the name was updated
        resp3 = client.get(f"/api/v1/industries/{industry_id}")
        assert resp3.status_code == 200
        assert resp3.json()["name_zh"] == "更新后的名称"

    async def test_business_batch_mapping_dedup(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        batch_id = f"test_batch_map_{uid}"
        industry_id = f"test_ind_map_{uid}"

        payload = {
            "batch_id": batch_id,
            "task_description": "测试映射去重",
            "industries_to_upsert": [
                {
                    "industry_id": industry_id,
                    "name_zh": "映射去重测试行业",
                    "status": "ACTIVE",
                }
            ],
            "industry_node_mappings_to_upsert": [
                {
                    "mapping_id": f"map1_{uid}",
                    "industry_id": industry_id,
                    "node_id": "lithium_battery_cell",
                    "weight": 0.5,
                    "status": "ACTIVE",
                },
                {
                    "mapping_id": f"map2_{uid}",
                    "industry_id": industry_id,
                    "node_id": "lithium_battery_cell",
                    "weight": 0.8,
                    "status": "ACTIVE",
                },
            ],
        }

        resp = client.post("/api/v1/business-batches", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        # First mapping created, second should update the same mapping (dedup by industry_id + node_id)
        assert data["mappings_created"] == 1
        assert data["mappings_updated"] == 1

    async def test_business_batch_empty(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        payload = {
            "batch_id": f"empty_batch_{uid}",
            "task_description": "空批次测试",
        }

        resp = client.post("/api/v1/business-batches", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["industries_created"] == 0
        assert data["industries_updated"] == 0
        assert data["companies_created"] == 0
        assert data["companies_updated"] == 0
