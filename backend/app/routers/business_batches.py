from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.models.company_schema import BusinessRegistrationBatch
from app.services import graph_service
from app.services import company_view as view_service
from app.services.computation_jobs import create_job

router = APIRouter()


@router.post("", status_code=201)
async def submit_business_batch(batch: BusinessRegistrationBatch, background_tasks: BackgroundTasks):
    try:
        result = await graph_service.process_business_batch(batch)

        # Trigger async recomputation of the global company view
        # so that newly registered companies appear in the relationship network.
        job = await create_job(
            job_type="company_view_compute",
            target_id=batch.batch_id,
            total_items=0,
        )
        background_tasks.add_task(
            view_service.compute_company_view,
            job["job_id"],
        )
        result["company_view_job_id"] = job["job_id"]

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
