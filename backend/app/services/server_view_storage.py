"""PostgreSQL storage for shared canvas views."""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from app.database_postgres import get_postgres_pool


def _row_to_dict(row: Any) -> dict:
    view = row["view"]
    if isinstance(view, str):
        view = json.loads(view)
    return {
        "view_id": str(row["view_id"]),
        "name": row["name"],
        "workspace": row["workspace"],
        "view": view,
        "is_default": row["is_default"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
    }


async def create_view(name: str, workspace: str, view: dict) -> dict:
    pool = await get_postgres_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL not available")
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO server_views (name, workspace, view)
            VALUES ($1, $2, $3::jsonb)
            RETURNING *
            """,
            name,
            workspace,
            json.dumps(view),
        )
    return _row_to_dict(row)


async def get_view(view_id: UUID) -> dict | None:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM server_views WHERE view_id = $1", view_id)
    return _row_to_dict(row) if row else None


async def list_views(workspace: str | None = None) -> list[dict]:
    pool = await get_postgres_pool()
    if pool is None:
        return []
    async with pool.acquire() as conn:
        if workspace:
            rows = await conn.fetch(
                """
                SELECT * FROM server_views
                WHERE workspace = $1
                ORDER BY is_default DESC, updated_at DESC
                """,
                workspace,
            )
        else:
            rows = await conn.fetch(
                """
                SELECT * FROM server_views
                ORDER BY workspace, is_default DESC, updated_at DESC
                """
            )
    return [_row_to_dict(row) for row in rows]


async def update_view(view_id: UUID, name: str | None, view: dict | None) -> dict | None:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE server_views
            SET name = COALESCE($2, name),
                view = COALESCE($3::jsonb, view),
                updated_at = NOW()
            WHERE view_id = $1
            RETURNING *
            """,
            view_id,
            name,
            json.dumps(view) if view is not None else None,
        )
    return _row_to_dict(row) if row else None


async def delete_view(view_id: UUID) -> bool:
    pool = await get_postgres_pool()
    if pool is None:
        return False
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM server_views WHERE view_id = $1", view_id)
    return result.split()[-1] != "0"


async def set_default_view(view_id: UUID) -> dict | None:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        async with conn.transaction():
            target = await conn.fetchrow(
                "SELECT workspace FROM server_views WHERE view_id = $1 FOR UPDATE",
                view_id,
            )
            if target is None:
                return None
            await conn.execute(
                "UPDATE server_views SET is_default = FALSE WHERE workspace = $1 AND is_default",
                target["workspace"],
            )
            row = await conn.fetchrow(
                """
                UPDATE server_views
                SET is_default = TRUE, updated_at = NOW()
                WHERE view_id = $1
                RETURNING *
                """,
                view_id,
            )
    return _row_to_dict(row)


async def get_default_view(workspace: str) -> dict | None:
    pool = await get_postgres_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM server_views WHERE workspace = $1 AND is_default",
            workspace,
        )
    return _row_to_dict(row) if row else None

