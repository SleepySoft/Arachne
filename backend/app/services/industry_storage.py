"""
PostgreSQL storage layer for Industry and IndustryNodeMapping.

Uses asyncpg for async PostgreSQL access.
All functions return Pydantic models from industry_schema.
"""

from __future__ import annotations

import json
from typing import List, Optional, Tuple
from uuid import UUID

from app.database_postgres import get_postgres_pool
from app.models.industry_schema import Industry, IndustryNodeMapping


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_to_industry(row: dict) -> Industry:
    return Industry(
        industry_id=row["industry_id"],
        industry_uuid=row["industry_uuid"],
        name_zh=row["name_zh"],
        name_en=row.get("name_en"),
        aliases=row.get("aliases") or [],
        industry_type=row["industry_type"],
        description=row.get("description"),
        status=row["status"],
        notes=row.get("notes"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def _row_to_mapping(row: dict) -> IndustryNodeMapping:
    evidence_raw = row.get("evidence") or []
    while isinstance(evidence_raw, str):
        evidence_raw = json.loads(evidence_raw)
    return IndustryNodeMapping(
        mapping_id=row["mapping_id"],
        mapping_uuid=row["mapping_uuid"],
        industry_id=row["industry_id"],
        node_id=row["node_id"],
        role=row.get("role"),
        weight=row["weight"],
        confidence=row["confidence"],
        evidence=evidence_raw,
        status=row["status"],
        notes=row.get("notes"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# Industry CRUD
# ---------------------------------------------------------------------------

async def create_industry(data: Industry) -> Industry:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO industries (
                industry_id, industry_uuid, name_zh, name_en,
                aliases, industry_type, description, status, notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
            """,
            data.industry_id,
            data.industry_uuid or str(UUID(int=0)),
            data.name_zh,
            data.name_en,
            data.aliases,
            data.industry_type.value,
            data.description,
            data.status.value,
            data.notes,
        )
        return _row_to_industry(row)


async def get_industry(industry_id: str) -> Optional[Industry]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM industries WHERE industry_id = $1",
            industry_id,
        )
        if row is None:
            return None
        return _row_to_industry(row)


async def update_industry(industry_id: str, data: dict) -> Optional[Industry]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {"name_zh", "name_en", "aliases", "industry_type", "description", "status", "notes"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_industry(industry_id)

    # Build dynamic SET
    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE industries
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE industry_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, industry_id, *fields.values())
        if row is None:
            return None
        return _row_to_industry(row)


async def delete_industry(industry_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM industries WHERE industry_id = $1",
            industry_id,
        )
        # asyncpg execute returns 'DELETE <count>'
        return result.split()[-1] != "0"


async def list_industries(
    skip: int = 0,
    limit: int = 20,
    industry_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[List[Industry], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    conditions = ["1=1"]
    params: list = []
    param_idx = 1

    if industry_type:
        conditions.append(f"industry_type = ${param_idx}")
        params.append(industry_type)
        param_idx += 1

    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1

    if search:
        conditions.append(f"(name_zh ILIKE ${param_idx} OR name_en ILIKE ${param_idx} OR industry_id ILIKE ${param_idx})")
        params.append(f"%{search}%")
        param_idx += 1

    where_clause = " AND ".join(conditions)

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM industries WHERE {where_clause}",
            *params,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM industries
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            limit,
            skip,
        )
        items = [_row_to_industry(r) for r in rows]
        return items, total


# ---------------------------------------------------------------------------
# IndustryNodeMapping CRUD
# ---------------------------------------------------------------------------

async def create_mapping(data: IndustryNodeMapping) -> IndustryNodeMapping:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO industry_node_mappings (
                mapping_id, mapping_uuid, industry_id, node_id,
                role, weight, confidence, evidence, status, notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING *
            """,
            data.mapping_id,
            data.mapping_uuid or str(UUID(int=0)),
            data.industry_id,
            data.node_id,
            data.role,
            data.weight,
            data.confidence.value,
            json.dumps([e.model_dump(mode='json') for e in data.evidence]) if data.evidence else "[]",
            data.status.value,
            data.notes,
        )
        return _row_to_mapping(row)


async def get_mapping(mapping_id: str) -> Optional[IndustryNodeMapping]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM industry_node_mappings WHERE mapping_id = $1",
            mapping_id,
        )
        if row is None:
            return None
        return _row_to_mapping(row)


async def get_mapping_by_industry_and_node(
    industry_id: str, node_id: str
) -> Optional[IndustryNodeMapping]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM industry_node_mappings WHERE industry_id = $1 AND node_id = $2",
            industry_id,
            node_id,
        )
        if row is None:
            return None
        return _row_to_mapping(row)


async def update_mapping(mapping_id: str, data: dict) -> Optional[IndustryNodeMapping]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {"role", "weight", "confidence", "evidence", "status", "notes"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_mapping(mapping_id)

    # Convert evidence list to JSON string if present
    if "evidence" in fields and fields["evidence"] is not None:
        fields["evidence"] = json.dumps([e.model_dump(mode='json') for e in fields["evidence"]])

    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE industry_node_mappings
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE mapping_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, mapping_id, *fields.values())
        if row is None:
            return None
        return _row_to_mapping(row)


async def delete_mapping(mapping_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM industry_node_mappings WHERE mapping_id = $1",
            mapping_id,
        )
        return result.split()[-1] != "0"


async def list_mappings_by_industry(
    industry_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[IndustryNodeMapping], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            "SELECT COUNT(*) FROM industry_node_mappings WHERE industry_id = $1",
            industry_id,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            """
            SELECT * FROM industry_node_mappings
            WHERE industry_id = $1
            ORDER BY weight DESC, created_at DESC
            LIMIT $2 OFFSET $3
            """,
            industry_id,
            limit,
            skip,
        )
        items = [_row_to_mapping(r) for r in rows]
        return items, total


async def list_mappings_by_node(
    node_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[IndustryNodeMapping], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            "SELECT COUNT(*) FROM industry_node_mappings WHERE node_id = $1",
            node_id,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            """
            SELECT * FROM industry_node_mappings
            WHERE node_id = $1
            ORDER BY weight DESC, created_at DESC
            LIMIT $2 OFFSET $3
            """,
            node_id,
            limit,
            skip,
        )
        items = [_row_to_mapping(r) for r in rows]
        return items, total


async def delete_mappings_by_industry(industry_id: str) -> int:
    """Delete all mappings for an industry. Returns count deleted."""
    pool = await get_postgres_pool()
    if pool is None:
        return 0

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM industry_node_mappings WHERE industry_id = $1",
            industry_id,
        )
        # result is like 'DELETE 5'
        parts = result.split()
        return int(parts[-1]) if len(parts) >= 2 else 0
