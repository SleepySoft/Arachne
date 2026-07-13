"""Integration tests for Industry and Company routers."""

from __future__ import annotations

import os
from uuid import uuid4

import httpx
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


class TestIndustryRouter:
    async def test_create_and_get_industry(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        payload = {
            "industry_id": f"test_robot_{uid}",
            "name_zh": "测试机器人行业",
            "industry_type": "curated_view",
            "description": "用于测试的行业",
            "status": "ACTIVE",
            "is_test": True,
        }
        resp = client.post("/api/v1/industries", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["industry_id"] == payload["industry_id"]

        resp2 = client.get(f"/api/v1/industries/{payload['industry_id']}")
        assert resp2.status_code == 200
        assert resp2.json()["name_zh"] == "测试机器人行业"

    async def test_list_industries(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        resp = client.get("/api/v1/industries?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data

    async def test_delete_industry(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        payload = {
            "industry_id": f"test_del_{uid}",
            "name_zh": "待删除行业",
            "status": "ACTIVE",
            "is_test": True,
        }
        client.post("/api/v1/industries", json=payload)
        resp = client.delete(f"/api/v1/industries/{payload['industry_id']}")
        assert resp.status_code == 204

        resp2 = client.get(f"/api/v1/industries/{payload['industry_id']}")
        assert resp2.status_code == 404

    async def test_industry_mappings(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        industry_id = f"test_map_{uid}"
        client.post("/api/v1/industries", json={
            "industry_id": industry_id,
            "name_zh": "映射测试行业",
            "status": "ACTIVE",
            "is_test": True,
        })

        # Create mapping
        from app.services import industry_storage
        from app.models.industry_schema import IndustryNodeMapping
        mapping = IndustryNodeMapping(
            mapping_id=f"test_mapping_{uid}",
            industry_id=industry_id,
            node_id="silicon_wafer",
            role="核心产品",
            weight=0.9,
            is_test=True,
        )
        await industry_storage.create_mapping(mapping)

        resp = client.get(f"/api/v1/industries/{industry_id}/mappings")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["node_id"] == "silicon_wafer"


class TestCompanyRouter:
    async def test_create_and_get_company(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        payload = {
            "company_id": f"test_byd_{uid}",
            "name_zh": f"比亚迪测试-{uid}",
            "country": "CN",
            "company_type": "public",
            "status": "ACTIVE",
            "is_test": True,
        }
        resp = client.post("/api/v1/companies", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["company_id"] == payload["company_id"]

        resp2 = client.get(f"/api/v1/companies/{payload['company_id']}")
        assert resp2.status_code == 200
        assert resp2.json()["name_zh"] == payload["name_zh"]

    async def test_list_companies_with_filter(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        resp = client.get("/api/v1/companies?country=CN&company_type=public")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data

    async def test_company_exposures(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        company_id = f"test_exp_{uid}"
        client.post("/api/v1/companies", json={
            "company_id": company_id,
            "name_zh": f"exposure测试公司-{uid}",
            "status": "ACTIVE",
            "is_test": True,
        })

        from app.services import company_storage
        from app.models.company_schema import CompanyNodeExposure, CompanyActivityType
        exp = CompanyNodeExposure(
            exposure_id=f"test_exp_item_{uid}",
            company_id=company_id,
            node_id="lithium_battery_cell",
            activity_type=CompanyActivityType.PRODUCE,
            weight=0.85,
            is_test=True,
        )
        await company_storage.create_exposure(exp)

        resp = client.get(f"/api/v1/companies/{company_id}/exposures")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["node_id"] == "lithium_battery_cell"

    async def test_delete_company(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        payload = {
            "company_id": f"test_del_co_{uid}",
            "name_zh": "待删除公司",
            "status": "ACTIVE",
            "is_test": True,
        }
        client.post("/api/v1/companies", json=payload)
        resp = client.delete(f"/api/v1/companies/{payload['company_id']}")
        assert resp.status_code == 204

        resp2 = client.get(f"/api/v1/companies/{payload['company_id']}")
        assert resp2.status_code == 404


class TestNodeWithIndustries:
    async def test_create_node_with_industries(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        industry_id = f"test_ind_for_node_{uid}"

        # 先创建目标行业
        resp_ind = client.post("/api/v1/industries", json={
            "industry_id": industry_id,
            "name_zh": "节点创建行业测试",
            "status": "ACTIVE",
            "is_test": True,
        })
        assert resp_ind.status_code == 201

        # 创建节点并同时关联行业
        node_id = f"test_node_{uid}"
        resp = client.post("/api/v1/nodes", json={
            "node_id": node_id,
            "canonical_name_zh": "测试节点",
            "definition": "用于测试创建时关联行业的节点",
            "entity_type": "material",
            "confidence": "LOW",
            "status": "PENDING",
            "industry_ids": [{"industry_id": industry_id}],
            "is_test": True,
        })
        assert resp.status_code == 201
        assert resp.json()["node_id"] == node_id

        # 验证映射已生成
        resp2 = client.get(f"/api/v1/industries/{industry_id}/mappings")
        assert resp2.status_code == 200
        items = resp2.json()["items"]


class TestReifiedUsageEdge:
    async def test_create_reified_usage(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        execution_id = f"test_exec_{uid}"
        technology_id = f"test_tech_{uid}"

        # Create execution node (process)
        resp = client.post("/api/v1/nodes", json={
            "node_id": execution_id,
            "canonical_name_zh": "测试光刻前清洗",
            "definition": "测试用具体工艺执行",
            "entity_type": "process",
            "is_test": True,
        })
        assert resp.status_code == 201

        # Create technology node (process technology)
        resp = client.post("/api/v1/nodes", json={
            "node_id": technology_id,
            "canonical_name_zh": "测试晶圆清洗工艺",
            "definition": "测试用通用工艺技术",
            "entity_type": "process",
            "is_test": True,
        })
        assert resp.status_code == 201

        # Create reified usage
        resp = client.post("/api/v1/edges/reified-usage", json={
            "execution_node_id": execution_id,
            "technology_node_id": technology_id,
            "scenario": "pre_lithography",
            "description": "测试物化边",
            "is_test": True,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["usage_node"]["entity_type"] == "usage"
        assert data["uses_edge"]["edge_type"] == "uses"
        assert data["uses_edge"]["from_node"] == execution_id
        assert data["adopts_edge"]["edge_type"] == "adopts"
        assert data["adopts_edge"]["to_node"] == technology_id

        # Verify usage node is queryable
        usage_id = data["usage_node"]["node_id"]
        resp2 = client.get(f"/api/v1/nodes/{usage_id}")
        assert resp2.status_code == 200
        assert resp2.json()["entity_type"] == "usage"

    async def test_create_reified_usage_missing_nodes(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        resp = client.post("/api/v1/edges/reified-usage", json={
            "execution_node_id": "nonexistent_exec",
            "technology_node_id": "nonexistent_tech",
            "is_test": True,
        })
        assert resp.status_code == 400

    async def test_quick_create_node_with_industries(self, client):
        if not await _postgres_available():
            pytest.skip("PostgreSQL not available")

        uid = uuid4().hex[:6]
        industry_id = f"test_ind_for_qnode_{uid}"

        client.post("/api/v1/industries", json={
            "industry_id": industry_id,
            "name_zh": "快速创建行业测试",
            "status": "ACTIVE",
            "is_test": True,
        })

        resp = client.post("/api/v1/nodes/quick-create", json={
            "canonical_name_zh": f"快速测试节点-{uid}",
            "industry_ids": [{"industry_id": industry_id}],
            "is_test": True,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["node_id"].startswith("draft_")

        resp2 = client.get(f"/api/v1/industries/{industry_id}/mappings")
        assert resp2.status_code == 200
        items = resp2.json()["items"]
        assert any(i["node_id"] == data["node_id"] for i in items)
