"""
PostgreSQL storage layer for IndustrialNode metadata.

Since v2, node metadata lives in PostgreSQL while Neo4j only keeps the
skeleton node (node_id + label) for relationship storage.
"""

from __future__ import annotations

import asyncpg
import json
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from app.database_postgres import get_postgres_pool
from app.engines.legacy.schemas import IndustrialNode
from app.models.core import Evidence


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _evidence_to_db(evidence: List[Evidence]) -> str:
    if not evidence:
        return "[]"
    out = []
    for e in evidence:
        if isinstance(e, dict):
            out.append(
                {
                    "source_title": e.get("source_title", ""),
                    "source_url": str(e.get("source_url")) if e.get("source_url") else None,
                    "quote": e.get("quote", ""),
                }
            )
        else:
            out.append(
                {
                    "source_title": e.source_title,
                    "source_url": str(e.source_url) if e.source_url else None,
                    "quote": e.quote,
                }
            )
    return json.dumps(out, ensure_ascii=False)


def _evidence_from_db(raw) -> List[Evidence]:
    if not raw:
        return []
    if isinstance(raw, str):
        try:
            import json
            items = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return []
    else:
        items = raw
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if not item:
            continue
        url = item.get("source_url")
        out.append(
            Evidence(
                source_title=item.get("source_title", ""),
                source_url=url if url else None,
                quote=item.get("quote", ""),
            )
        )
    return out


def _row_to_node(row: asyncpg.Record) -> IndustrialNode:
    evidence = _evidence_from_db(row.get("evidence"))
    confidence = row.get("confidence", "LOW")
    status = row.get("status", "PENDING")

    # Tolerate old or inconsistent data
    if not evidence:
        if confidence == "HIGH":
            confidence = "MEDIUM"
        if status == "ACTIVE":
            status = "PENDING"

    node_uuid = row.get("node_uuid")
    if node_uuid is None:
        node_uuid = UUID(int=0)

    return IndustrialNode(
        node_uuid=node_uuid,
        node_id=row["node_id"],
        canonical_name_zh=row.get("canonical_name_zh") or row["node_id"],
        canonical_name_en=row.get("canonical_name_en"),
        aliases=row.get("aliases") or [],
        definition=row.get("definition") or "（定义待补充）",
        entity_type=row.get("entity_type", "unknown"),
        evidence=evidence,
        confidence=confidence,
        status=status,
        notes=row.get("notes"),
        is_test=row.get("is_test", False),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

async def create_node(node: IndustrialNode) -> IndustrialNode:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO industrial_nodes (
                node_id, node_uuid, canonical_name_zh, canonical_name_en,
                aliases, definition, entity_type, evidence, confidence,
                status, notes, is_test
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING *
            """,
            node.node_id,
            node.node_uuid or UUID(int=0),
            node.canonical_name_zh,
            node.canonical_name_en,
            node.aliases,
            node.definition,
            node.entity_type.value if hasattr(node.entity_type, "value") else node.entity_type,
            _evidence_to_db(node.evidence),
            node.confidence.value if hasattr(node.confidence, "value") else node.confidence,
            node.status.value if hasattr(node.status, "value") else node.status,
            node.notes,
            node.is_test,
        )
        return _row_to_node(row)


async def get_node(node_id: str) -> Optional[IndustrialNode]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM industrial_nodes WHERE node_id = $1",
            node_id,
        )
        if row is None:
            return None
        return _row_to_node(row)


async def node_exists(node_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT 1 FROM industrial_nodes WHERE node_id = $1",
            node_id,
        )
        return row is not None


async def update_node(node_id: str, data: dict) -> Optional[IndustrialNode]:
    pool = await get_postgres_pool()
    if pool is None:
        return None

    allowed = {
        "canonical_name_zh",
        "canonical_name_en",
        "aliases",
        "definition",
        "entity_type",
        "evidence",
        "confidence",
        "status",
        "notes",
        "is_test",
    }
    fields: Dict[str, Any] = {}
    for k, v in data.items():
        if k not in allowed or v is None:
            continue
        if k == "evidence":
            fields[k] = _evidence_to_db(v)
        elif k in ("entity_type", "confidence", "status"):
            fields[k] = v.value if hasattr(v, "value") else v
        else:
            fields[k] = v

    if not fields:
        return await get_node(node_id)

    set_clauses = [f"{k} = ${i + 2}" for i, k in enumerate(fields.keys())]
    sql = f"""
        UPDATE industrial_nodes
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE node_id = $1
        RETURNING *
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql, node_id, *fields.values())
        if row is None:
            return None
        return _row_to_node(row)


async def delete_node(node_id: str) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False

    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM industrial_nodes WHERE node_id = $1",
            node_id,
        )
        return result.split()[-1] != "0"


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    draft_only: Optional[bool] = None,
) -> Tuple[List[IndustrialNode], int]:
    pool = await get_postgres_pool()
    if pool is None:
        return [], 0

    conditions = ["1=1"]
    params: list = []
    param_idx = 1

    if entity_type:
        conditions.append(f"entity_type = ${param_idx}")
        params.append(entity_type)
        param_idx += 1

    if status:
        conditions.append(f"status = ${param_idx}")
        params.append(status)
        param_idx += 1

    if search:
        conditions.append(
            f"(canonical_name_zh ILIKE ${param_idx} OR canonical_name_en ILIKE ${param_idx} "
            f"OR node_id ILIKE ${param_idx} OR EXISTS (SELECT 1 FROM unnest(aliases) a WHERE a ILIKE ${param_idx}))"
        )
        params.append(f"%{search}%")
        param_idx += 1

    if draft_only:
        conditions.append(
            f"(node_id LIKE 'draft_%' OR status = 'PENDING' OR entity_type = 'unknown' OR definition = '' OR definition IS NULL)"
        )

    where_clause = " AND ".join(conditions)

    async with pool.acquire() as conn:
        total_row = await conn.fetchrow(
            f"SELECT COUNT(*) FROM industrial_nodes WHERE {where_clause}",
            *params,
        )
        total = total_row["count"] if total_row else 0

        if search:
            # Boost exact matches, then prefix matches, then substring matches.
            rows = await conn.fetch(
                f"""
                SELECT *,
                  CASE
                    WHEN canonical_name_zh = ${param_idx} OR canonical_name_en = ${param_idx}
                      OR node_id = ${param_idx} OR EXISTS (SELECT 1 FROM unnest(aliases) a WHERE a = ${param_idx}) THEN 3
                    WHEN canonical_name_zh ILIKE ${param_idx + 1} OR canonical_name_en ILIKE ${param_idx + 1}
                      OR node_id ILIKE ${param_idx + 1} OR EXISTS (SELECT 1 FROM unnest(aliases) a WHERE a ILIKE ${param_idx + 1}) THEN 2
                    ELSE 1
                  END AS score
                FROM industrial_nodes
                WHERE {where_clause}
                ORDER BY score DESC, canonical_name_zh
                LIMIT ${param_idx + 2} OFFSET ${param_idx + 3}
                """,
                *params,
                search,
                f"{search}%",
                limit,
                skip,
            )
        else:
            rows = await conn.fetch(
                f"""
                SELECT * FROM industrial_nodes
                WHERE {where_clause}
                ORDER BY canonical_name_zh
                LIMIT ${param_idx} OFFSET ${param_idx + 1}
                """,
                *params,
                limit,
                skip,
            )

        items = [_row_to_node(r) for r in rows]
        return items, total


async def get_nodes_by_ids(node_ids: List[str]) -> Dict[str, IndustrialNode]:
    pool = await get_postgres_pool()
    if pool is None:
        return {}

    if not node_ids:
        return {}

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM industrial_nodes WHERE node_id = ANY($1)",
            node_ids,
        )
        return {row["node_id"]: _row_to_node(row) for row in rows}
