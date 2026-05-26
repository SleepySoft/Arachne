"""Router for company material-based connection exploration."""

from fastapi import APIRouter, HTTPException

from app.services.company_material import get_material_connections

router = APIRouter()


@router.get("/{company_id}/material-connections")
async def list_material_connections(company_id: str):
    """
    Return all material-based connections for a company.

    Includes peer companies (same node exposure), upstream suppliers
    (companies exposing upstream nodes), and downstream customers
    (companies exposing downstream nodes).
    """
    try:
        data = await get_material_connections(company_id)
        return data
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get material connections: {exc}")
