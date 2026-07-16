from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.engines.legacy.schemas import GraphRegistrationBatch
from app.services import graph_service

router = APIRouter()


@router.post("", status_code=201)
async def submit_batch(
    batch: GraphRegistrationBatch,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    try:
        result = await graph_service.process_batch(batch, engine=engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
