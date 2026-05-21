from fastapi import APIRouter, HTTPException

from app.models.schemas import GraphRegistrationBatch
from app.services import graph_service

router = APIRouter()


@router.post("", status_code=201)
async def submit_batch(batch: GraphRegistrationBatch):
    try:
        result = await graph_service.process_batch(batch)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
