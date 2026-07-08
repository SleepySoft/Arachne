"""Admin / maintenance endpoints (local-dev only, no auth)."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Query

from app.services.test_data_cleanup import cleanup_test_data

router = APIRouter(tags=["admin"])


@router.post("/cleanup-test-data", response_model=Dict[str, Any])
async def cleanup_test_data_endpoint(
    dry_run: bool = Query(default=False, description="If true, return counts without deleting anything"),
):
    """Delete all entities marked as `is_test = true`.

    Set ``dry_run=true`` to preview how many rows/nodes would be removed.
    """
    result = await cleanup_test_data(dry_run=dry_run)
    return result
