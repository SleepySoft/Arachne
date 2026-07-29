"""
Published views API - store and retrieve embeddable reasoning view configs.

A *published view* bundles reasoning parameters (and optionally a result
snapshot) behind a stable UUID so that external systems can embed a
reasoning result via a short URL:  embed.html?view=<view_id>
"""

from __future__ import annotations

import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.database_postgres import get_postgres_pool

router = APIRouter()


class PublishedViewCreate(BaseModel):
    title: str | None = None
    params: dict = Field(default_factory=dict)
    result_snapshot: dict | None = None
    created_by: str | None = None
    expires_at: str | None = None


class PublishedViewOut(BaseModel):
    view_id: str
    title: str | None = None
    params: dict
    result_snapshot: dict | None = None
    created_by: str | None = None
    created_at: str | None = None
    expires_at: str | None = None


def _row_to_dict(row) -> dict:
    return {
        "view_id": str(row["view_id"]),
        "title": row["title"],
        "params": json.loads(row["params"]) if isinstance(row["params"], str) else row["params"],
        "result_snapshot": (
            json.loads(row["result_snapshot"])
            if row["result_snapshot"] and isinstance(row["result_snapshot"], str)
            else row["result_snapshot"]
        ),
        "created_by": row["created_by"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "expires_at": row["expires_at"].isoformat() if row["expires_at"] else None,
    }


@router.post("", response_model=PublishedViewOut, status_code=201)
async def create_published_view(body: PublishedViewCreate):
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO published_views (title, params, result_snapshot, created_by, expires_at)
            VALUES ($1, $2::jsonb, $3::jsonb, $4, $5)
            RETURNING *
            """,
            body.title,
            json.dumps(body.params),
            json.dumps(body.result_snapshot) if body.result_snapshot else None,
            body.created_by,
            body.expires_at,
        )
    return _row_to_dict(row)


@router.get("/{view_id}", response_model=PublishedViewOut)
async def get_published_view(view_id: str):
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")
    try:
        uid = UUID(view_id)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid view_id")
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM published_views
            WHERE view_id = $1
              AND (expires_at IS NULL OR expires_at > NOW())
            """,
            uid,
        )
    if row is None:
        raise HTTPException(status_code=404, detail="View not found or expired")
    return _row_to_dict(row)


@router.get("", response_model=list[PublishedViewOut])
async def list_published_views(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
):
    pool = await get_postgres_pool()
    if pool is None:
        raise HTTPException(status_code=503, detail="PostgreSQL not available")
    offset = (page - 1) * page_size
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM published_views
            WHERE expires_at IS NULL OR expires_at > NOW()
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            """,
            page_size,
            offset,
        )
    return [_row_to_dict(r) for r in rows]
