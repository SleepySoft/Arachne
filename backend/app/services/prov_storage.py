"""
PostgreSQL storage layer for PROV statements.

PROV statements are type-level provenance assertions attached to industrial nodes.
They are stored independently of the Neo4j graph topology.
"""

from __future__ import annotations

import json
from typing import List, Optional, Tuple
from uuid import UUID

from app.database_postgres import get_postgres_pool
from app.models.prov_schema import ProvStatement, ProvRelation, ProvRole


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _evidence_to_db(evidence: List) -> str:
    if not evidence:
        return "[]"
    return json.dumps([e.model_dump(mode="json") for e in evidence])


def _evidence_from_db(raw):
    if raw is None:
        return []
    while isinstance(raw, str):
        raw = json.loads(raw)
    if not isinstance(raw, list):
        return []
    return raw


def _row_to_statement(row) -> ProvStatement:
    return ProvStatement(
        statement_uuid=row["statement_uuid"],
        statement_id=row["statement_id"],
        node_id=row["node_id"],
        node_role=ProvRole(row["node_role"]),
        prov_relation=ProvRelation(row["prov_relation"]),
        target_node_id=row["target_node_id"],
        target_role=ProvRole(row["target_role"]),
        is_inferred=row["is_inferred"],
        evidence=_evidence_from_db(row.get("evidence")),
        confidence=row["confidence"],
        status=row["status"],
        notes=row.get("notes"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

async def create_statement(data: ProvStatement) -> ProvStatement:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    # Ensure statement_id is generated before insert
    data = data.model_copy(update={"statement_id": data.statement_id or f"{data.node_id}__{data.prov_relation.value}__{data.target_node_id}"})

    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                """
                INSERT INTO prov_statements (
                    statement_id, statement_uuid, node_id, node_role,
                    prov_relation, target_node_id, target_role,
                    is_inferred, evidence, confidence, status, notes
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING *
                """,
                data.statement_id,
                data.statement_uuid or str(UUID(int=0)),
                data.node_id,
                data.node_role.value,
                data.prov_relation.value,
                data.target_node_id,
                data.target_role.value,
                data.is_inferred,
                _evidence_to_db(data.evidence),
                data.confidence.value,
                data.status.value,
                data.notes,
            )
        except Exception as exc:
            if "unique" in str(exc).lower():
                raise ValueError(
                    f"PROV statement already exists: {data.node_id} {data.prov_relation.value} {data.target_node_id}"
                ) from exc
            raise
        return _row_to_statement(row)


async def get_statement(statement_id: str) -> Optional[ProvStatement]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM prov_statements WHERE statement_id = $1",
            statement_id,
        )
        if row is None:
            return None
        return _row_to_statement(row)


async def update_statement(statement_id: str, data: dict) -> Optional[ProvStatement]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {
        "node_role",
        "target_role",
        "is_inferred",
        "evidence",
        "confidence",
        "status",
        "notes",
    }
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_statement(statement_id)

    if "evidence" in fields and fields["evidence"] is not None:
        fields["evidence"] = _evidence_to_db(fields["evidence"])

    if "node_role" in fields:
        fields["node_role"] = fields["node_role"].value if hasattr(fields["node_role"], "value") else fields["node_role"]
    if "target_role" in fields:
        fields["target_role"] = fields["target_role"].value if hasattr(fields["target_role"], "value") else fields["target_role"]
    if "confidence" in fields:
        fields["confidence"] = fields["confidence"].value if hasattr(fields["confidence"], "value") else fields["confidence"]
    if "status" in fields:
        fields["status"] = fields["status"].value if hasattr(fields["status"], "value") else fields["status"]

    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE prov_statements
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE statement_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, statement_id, *fields.values())
        if row is None:
            return None
        return _row_to_statement(row)


async def delete_statement(statement_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM prov_statements WHERE statement_id = $1",
            statement_id,
        )
        return result.split()[-1] != "0"


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------

async def list_statements(
    skip: int = 0,
    limit: int = 100,
    node_id: Optional[str] = None,
    target_node_id: Optional[str] = None,
    prov_relation: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[ProvStatement], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    conditions = ["1=1"]
    params: list = []
    param_idx = 1

    if node_id:
        conditions.append(f"node_id = ${param_idx}")
        params.append(node_id)
        param_idx += 1

    if target_node_id:
        conditions.append(f"target_node_id = ${param_idx}")
        params.append(target_node_id)
        param_idx += 1

    if prov_relation:
        conditions.append(f"prov_relation = ${param_idx}")
        params.append(prov_relation)
        param_idx += 1

    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1

    where_clause = " AND ".join(conditions)

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM prov_statements WHERE {where_clause}",
            *params,
        )
        total = total_row["count"] if total_row else 0

        rows = await conn.fetch(
            f"""
            SELECT * FROM prov_statements
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
            """,
            *params,
            limit,
            skip,
        )
        items = [_row_to_statement(r) for r in rows]
        return items, total


async def list_statements_by_node(
    node_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[ProvStatement], int]:
    return await list_statements(skip=skip, limit=limit, node_id=node_id)


async def list_statements_by_target(
    target_node_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[ProvStatement], int]:
    return await list_statements(skip=skip, limit=limit, target_node_id=target_node_id)
