from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services import mes_service

router = APIRouter()


@router.get("/products/{product_id}/production")
def production(product_id: str, session: Session = Depends(get_session)) -> dict:
    rows = mes_service.get_production_results(session, product_id)
    return {
        "product_id": product_id,
        "production_results": rows,
        "source": "MES.production_results",
    }


@router.get("/products/{product_id}/defect-rate")
def defect_rate(product_id: str, session: Session = Depends(get_session)) -> dict:
    rows = mes_service.get_monthly_defect_rate(session, product_id)
    return {
        "product_id": product_id,
        "monthly_defect_rate": rows,
        "source": "MES.production_results+defects",
    }


@router.get("/lots/{lot_id}/trace")
def trace_lot(lot_id: str, session: Session = Depends(get_session)) -> dict:
    res = mes_service.trace_lot(session, lot_id)
    if res is None:
        raise HTTPException(status_code=404, detail=f"Lot {lot_id} not found")
    return {"trace": res, "source": "MES.lots+production_results+defects"}


@router.get("/quality/defects/top")
def top_defects(
    product_id: str | None = None, session: Session = Depends(get_session)
) -> dict:
    rows = mes_service.top_defect_types(session, product_id=product_id)
    return {
        "product_id": product_id,
        "top_defect_types": rows,
        "source": "MES.defects",
    }
