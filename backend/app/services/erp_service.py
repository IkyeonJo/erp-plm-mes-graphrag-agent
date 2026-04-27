from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Inventory, Item, PurchaseOrder, Supplier


def get_item_inventory(session: Session, item_id: str) -> list[dict[str, Any]]:
    rows = session.scalars(select(Inventory).where(Inventory.item_id == item_id)).all()
    return [
        {
            "inventory_id": r.inventory_id,
            "item_id": r.item_id,
            "warehouse_id": r.warehouse_id,
            "quantity_on_hand": r.quantity_on_hand,
            "safety_stock": r.safety_stock,
        }
        for r in rows
    ]


def get_supplier_items(session: Session, supplier_id: str) -> list[dict[str, Any]]:
    rows = session.scalars(select(Item).where(Item.supplier_id == supplier_id)).all()
    return [
        {
            "item_id": r.item_id,
            "item_name": r.item_name,
            "item_type": r.item_type,
            "standard_cost": r.standard_cost,
        }
        for r in rows
    ]


def list_suppliers(session: Session, limit: int = 100) -> list[dict[str, Any]]:
    rows = session.scalars(select(Supplier).limit(limit)).all()
    return [
        {
            "supplier_id": r.supplier_id,
            "supplier_name": r.supplier_name,
            "country": r.country,
            "rating": r.rating,
        }
        for r in rows
    ]


def get_purchase_history(
    session: Session, item_id: str, limit: int = 50
) -> list[dict[str, Any]]:
    rows = session.scalars(
        select(PurchaseOrder).where(PurchaseOrder.item_id == item_id).limit(limit)
    ).all()
    return [
        {
            "po_id": r.po_id,
            "supplier_id": r.supplier_id,
            "order_date": str(r.order_date),
            "delivery_date": str(r.delivery_date) if r.delivery_date else None,
            "quantity": r.quantity,
            "unit_price": r.unit_price,
            "status": r.status,
        }
        for r in rows
    ]
