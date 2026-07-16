from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.models.company_schema import BusinessRegistrationBatch
from app.services import graph_service
from app.services.computation_jobs import create_job

router = APIRouter()


@router.post("", status_code=201)
async def submit_business_batch(
    batch: BusinessRegistrationBatch,
    engine: Optional[str] = Query(None, description="图引擎名称，默认 legacy"),
):
    try:
        result = await graph_service.process_business_batch(batch, engine=engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
