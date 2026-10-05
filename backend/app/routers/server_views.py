"""Shared canvas views stored on the Arachne server."""

from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator, model_validator

from app.services import server_view_storage


router = APIRouter()
Workspace = Literal["industrial", "company"]


class ServerViewCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=256)
    workspace: Workspace
    view: dict

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value

    @model_validator(mode="after")
    def validate_view_workspace(self):
        if self.view.get("workspace") != self.workspace:
            raise ValueError("view.workspace must match workspace")
        return self


class ServerViewUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=256)
    view: dict | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value


class ServerViewOut(BaseModel):
    view_id: str
    name: str
    workspace: Workspace
    view: dict
    is_default: bool
    created_at: str | None = None
    updated_at: str | None = None


def _parse_view_id(view_id: str) -> UUID:
    try:
        return UUID(view_id)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid view_id") from exc


@router.get("", response_model=list[ServerViewOut])
async def list_server_views(workspace: Workspace | None = Query(default=None)):
    return await server_view_storage.list_views(workspace)


@router.get("/default", response_model=ServerViewOut | None)
async def get_default_server_view(workspace: Workspace = Query(...)):
    return await server_view_storage.get_default_view(workspace)


@router.get("/{view_id}", response_model=ServerViewOut)
async def get_server_view(view_id: str):
    view = await server_view_storage.get_view(_parse_view_id(view_id))
    if view is None:
        raise HTTPException(status_code=404, detail="Server view not found")
    return view


@router.post("", response_model=ServerViewOut, status_code=201)
async def create_server_view(body: ServerViewCreate):
    try:
        return await server_view_storage.create_view(body.name, body.workspace, body.view)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.put("/{view_id}", response_model=ServerViewOut)
async def update_server_view(view_id: str, body: ServerViewUpdate):
    parsed_id = _parse_view_id(view_id)
    existing = await server_view_storage.get_view(parsed_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Server view not found")
    if body.view is not None and body.view.get("workspace") != existing["workspace"]:
        raise HTTPException(status_code=422, detail="view.workspace must match workspace")
    view = await server_view_storage.update_view(
        parsed_id,
        body.name,
        body.view,
    )
    if view is None:
        raise HTTPException(status_code=404, detail="Server view not found")
    return view


@router.delete("/{view_id}", status_code=204)
async def delete_server_view(view_id: str):
    if not await server_view_storage.delete_view(_parse_view_id(view_id)):
        raise HTTPException(status_code=404, detail="Server view not found")


@router.put("/{view_id}/default", response_model=ServerViewOut)
async def set_default_server_view(view_id: str):
    view = await server_view_storage.set_default_view(_parse_view_id(view_id))
    if view is None:
        raise HTTPException(status_code=404, detail="Server view not found")
    return view
