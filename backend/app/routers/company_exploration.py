"""Router for company exploration (heterogeneous graph)."""

from fastapi import APIRouter, HTTPException

from app.services.company_exploration import get_exploration_graph, get_material_companies

router = APIRouter()


@router.get("/{company_id}/exploration-graph")
async def exploration_graph(company_id: str):
    """Return the heterogeneous exploration graph centered on a company."""
    try:
        data = await get_exploration_graph(company_id)
        return data
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get exploration graph: {exc}")


@router.get("/nodes/{node_id}/connected-companies")
async def connected_companies(node_id: str, exclude_company_id: str | None = None):
    """Return peer/upstream/downstream companies for a material node."""
    try:
        data = await get_material_companies(node_id, exclude_company_id)
        return data
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get connected companies: {exc}")
