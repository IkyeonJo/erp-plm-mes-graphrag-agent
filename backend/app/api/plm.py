from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services import plm_service

router = APIRouter()


@router.get("/products/{product_id}")
def get_product(product_id: str, session: Session = Depends(get_session)) -> dict:
    p = plm_service.get_product(session, product_id)
    if p is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return {"product": p, "source": "PLM.products"}


@router.get("/products/{product_id}/bom")
def get_bom(product_id: str, session: Session = Depends(get_session)) -> dict:
    rows = plm_service.get_product_bom(session, product_id)
    return {"product_id": product_id, "bom": rows, "source": "PLM.bom"}


@router.get("/eco/recent")
def list_recent_eco(session: Session = Depends(get_session)) -> dict:
    rows = plm_service.list_recent_eco(session)
    return {"eco": rows, "source": "PLM.eco"}
