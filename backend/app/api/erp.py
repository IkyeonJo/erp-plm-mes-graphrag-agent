from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services import erp_service

router = APIRouter()


@router.get("/items/{item_id}/inventory")
def get_inventory(item_id: str, session: Session = Depends(get_session)) -> dict:
    rows = erp_service.get_item_inventory(session, item_id)
    return {"item_id": item_id, "inventory": rows, "source": "ERP.inventory"}


@router.get("/suppliers/{supplier_id}/items")
def get_supplier_items(supplier_id: str, session: Session = Depends(get_session)) -> dict:
    rows = erp_service.get_supplier_items(session, supplier_id)
    return {"supplier_id": supplier_id, "items": rows, "source": "ERP.items"}


@router.get("/items/{item_id}/purchase-history")
def purchase_history(item_id: str, session: Session = Depends(get_session)) -> dict:
    rows = erp_service.get_purchase_history(session, item_id)
    return {"item_id": item_id, "history": rows, "source": "ERP.purchase_orders"}


@router.get("/suppliers")
def list_suppliers(session: Session = Depends(get_session)) -> dict:
    rows = erp_service.list_suppliers(session)
    return {"suppliers": rows, "source": "ERP.suppliers"}
