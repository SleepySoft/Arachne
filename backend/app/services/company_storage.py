"""
PostgreSQL storage layer for Company and CompanyNodeExposure.

Uses asyncpg for async PostgreSQL access.
All functions return Pydantic models from company_schema.
"""

from __future__ import annotations

import json
from typing import List, Optional, Tuple
from uuid import UUID

from app.database_postgres import get_postgres_pool
from app.models.company_schema import Company, CompanyNodeExposure


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_to_company(row: dict) -> Company:
    return Company(
        company_id=row["company_id"],
        company_uuid=row["company_uuid"],
        name_zh=row["name_zh"],
        name_en=row.get("name_en"),
        aliases=row.get("aliases") or [],
        stock_codes=row.get("stock_codes") or [],
        description=row.get("description"),
        country=row.get("country") or "CN",
        province=row.get("province"),
        city=row.get("city"),
        founded_year=row.get("founded_year"),
        employee_count=row.get("employee_count"),
        revenue_cny=row.get("revenue_cny"),
        market_cap_cny=row.get("market_cap_cny"),
        net_profit_cny=row.get("net_profit_cny"),
        company_type=row["company_type"],
        status=row["status"],
        notes=row.get("notes"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def _row_to_exposure(row: dict) -> CompanyNodeExposure:
    evidence_raw = row.get("evidence") or []
    while isinstance(evidence_raw, str):
        evidence_raw = json.loads(evidence_raw)
    return CompanyNodeExposure(
        exposure_id=row["exposure_id"],
        exposure_uuid=row["exposure_uuid"],
        company_id=row["company_id"],
        node_id=row["node_id"],
        activity_type=row["activity_type"],
        role=row.get("role"),
        weight=row["weight"],
        confidence=row["confidence"],
        evidence=evidence_raw,
        status=row["status"],
        as_of_date=row.get("as_of_date"),
        notes=row.get("notes"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# Company CRUD
# ---------------------------------------------------------------------------

async def create_company(data: Company) -> Company:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO companies (
                company_id, company_uuid, name_zh, name_en,
                aliases, stock_codes, description, country, province, city,
                founded_year, employee_count, revenue_cny, market_cap_cny,
                net_profit_cny, company_type, status, notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
            RETURNING *
            """,
            data.company_id,
            data.company_uuid or str(UUID(int=0)),
            data.name_zh,
            data.name_en,
            data.aliases,
            data.stock_codes,
            data.description,
            data.country,
            data.province,
            data.city,
            data.founded_year,
            data.employee_count,
            data.revenue_cny,
            data.market_cap_cny,
            data.net_profit_cny,
            data.company_type.value,
            data.status.value,
            data.notes,
        )
        return _row_to_company(row)


async def get_company(company_id: str) -> Optional[Company]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM companies WHERE company_id = $1",
            company_id,
        )
        if row is None:
            return None
        return _row_to_company(row)


async def update_company(company_id: str, data: dict) -> Optional[Company]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {
        "name_zh", "name_en", "aliases", "stock_codes", "description",
        "country", "province", "city", "founded_year", "employee_count",
        "revenue_cny", "market_cap_cny", "net_profit_cny",
        "company_type", "status", "notes",
    }
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_company(company_id)

    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE companies
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE company_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, company_id, *fields.values())
        if row is None:
            return None
        return _row_to_company(row)


async def delete_company(company_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM companies WHERE company_id = $1",
            company_id,
        )
        return result.split()[-1] != "0"


async def list_companies(
    skip: int = 0,
    limit: int = 20,
    country: Optional[str] = None,
    company_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[Company], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    conditions = ["1=1"]
    params: list = []
    param_idx = 1

    if country:
        conditions.append(f"country = ${param_idx}")
        params.append(country)
        param_idx += 1

    if company_type:
        conditions.append(f"company_type = ${param_idx}")
        params.append(company_type)
        param_idx += 1

    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1

    if search:
        conditions.append(
            f"(name_zh ILIKE ${param_idx} OR name_en ILIKE ${param_idx} OR company_id ILIKE ${param_idx})"
        )
        params.append(f"%{search}%")
        param_idx += 1

    where_clause = " AND ".join(conditions)

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM companies WHERE {where_clause}",
            *params,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM companies
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            limit,
            skip,
        )
        items = [_row_to_company(r) for r in rows]
        return items, total


# ---------------------------------------------------------------------------
# CompanyNodeExposure CRUD
# ---------------------------------------------------------------------------

async def create_exposure(data: CompanyNodeExposure) -> CompanyNodeExposure:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO company_node_exposures (
                exposure_id, exposure_uuid, company_id, node_id,
                activity_type, role, weight, confidence, evidence, status, as_of_date, notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING *
            """,
            data.exposure_id,
            data.exposure_uuid or str(UUID(int=0)),
            data.company_id,
            data.node_id,
            data.activity_type.value,
            data.role,
            data.weight,
            data.confidence.value,
            json.dumps([e.model_dump(mode='json') for e in data.evidence]) if data.evidence else "[]",
            data.status.value,
            data.as_of_date,
            data.notes,
        )
        return _row_to_exposure(row)


async def get_exposure(exposure_id: str) -> Optional[CompanyNodeExposure]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM company_node_exposures WHERE exposure_id = $1",
            exposure_id,
        )
        if row is None:
            return None
        return _row_to_exposure(row)


async def get_exposure_by_company_and_node(
    company_id: str, node_id: str
) -> Optional[CompanyNodeExposure]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM company_node_exposures WHERE company_id = $1 AND node_id = $2",
            company_id,
            node_id,
        )
        if row is None:
            return None
        return _row_to_exposure(row)


async def update_exposure(exposure_id: str, data: dict) -> Optional[CompanyNodeExposure]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {"activity_type", "role", "weight", "confidence", "evidence", "status", "as_of_date", "notes"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_exposure(exposure_id)

    # Convert evidence list to JSON string if present
    if "evidence" in fields and fields["evidence"] is not None:
        fields["evidence"] = json.dumps([e.model_dump(mode='json') for e in fields["evidence"]])

    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE company_node_exposures
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE exposure_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, exposure_id, *fields.values())
        if row is None:
            return None
        return _row_to_exposure(row)


async def delete_exposure(exposure_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM company_node_exposures WHERE exposure_id = $1",
            exposure_id,
        )
        return result.split()[-1] != "0"


async def list_exposures_by_company(
    company_id: str,
    skip: int = 0,
    limit: int = 100,
    activity_type: Optional[str] = None,
) -> Tuple[List[CompanyNodeExposure], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    conditions = ["company_id = $1"]
    params = [company_id]
    param_idx = 2

    if activity_type:
        conditions.append(f"activity_type = ${param_idx}")
        params.append(activity_type)
        param_idx += 1

    where_clause = " AND ".join(conditions)

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM company_node_exposures WHERE {where_clause}",
            *params,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM company_node_exposures
            WHERE {where_clause}
            ORDER BY weight DESC, created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            limit,
            skip,
        )
        items = [_row_to_exposure(r) for r in rows]
        return items, total


async def list_exposures_by_node(
    node_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[CompanyNodeExposure], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            "SELECT COUNT(*) FROM company_node_exposures WHERE node_id = $1",
            node_id,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            """
            SELECT * FROM company_node_exposures
            WHERE node_id = $1
            ORDER BY weight DESC, created_at DESC
            LIMIT $2 OFFSET $3
            """,
            node_id,
            limit,
            skip,
        )
        items = [_row_to_exposure(r) for r in rows]
        return items, total


async def list_exposures_by_nodes(
    node_ids: List[str],
    limit: int = 1000,
) -> List[CompanyNodeExposure]:
    """返回一组产业节点上的所有公司暴露关系（去重）。"""
    pool = await get_postgres_pool()
    if not pool or not node_ids:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT DISTINCT ON (company_id, node_id, activity_type, role)
                exposure_id,
                exposure_uuid,
                company_id,
                node_id,
                activity_type,
                role,
                weight,
                confidence,
                evidence,
                created_at,
                updated_at
            FROM company_node_exposures
            WHERE node_id = ANY($1::text[])
            ORDER BY company_id, node_id, activity_type, role, weight DESC, created_at DESC
            LIMIT $2
            """,
            node_ids,
            limit,
        )
        return [_row_to_exposure(r) for r in rows]


async def get_companies_by_ids(company_ids: List[str]) -> List[Company]:
    """根据公司 ID 列表批量查询公司。"""
    pool = await get_postgres_pool()
    if not pool or not company_ids:
        return []

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM companies
            WHERE company_id = ANY($1::text[])
            ORDER BY name_zh
            """,
            company_ids,
        )
        return [_row_to_company(r) for r in rows]


async def delete_exposures_by_company(company_id: str) -> int:
    """Delete all exposures for a company. Returns count deleted."""
    pool = await get_postgres_pool()
    if pool is None:
        return 0

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM company_node_exposures WHERE company_id = $1",
            company_id,
        )
        parts = result.split()
        return int(parts[-1]) if len(parts) >= 2 else 0
