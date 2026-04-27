from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Bom, Eco, Product


def get_product_bom(session: Session, product_id: str) -> list[dict[str, Any]]:
    rows = session.scalars(select(Bom).where(Bom.product_id == product_id)).all()
    return [
        {
            "bom_id": r.bom_id,
            "product_id": r.product_id,
            "parent_part_id": r.parent_part_id,
            "child_part_id": r.child_part_id,
            "quantity": r.quantity,
            "revision": r.revision,
            "approval_status": r.approval_status,
        }
        for r in rows
    ]


def list_recent_eco(session: Session, limit: int = 30) -> list[dict[str, Any]]:
    rows = session.scalars(
        select(Eco).order_by(Eco.approved_date.desc().nullslast()).limit(limit)
    ).all()
    return [
        {
            "eco_id": r.eco_id,
            "product_id": r.product_id,
            "changed_part_id": r.changed_part_id,
            "change_type": r.change_type,
            "reason": r.reason,
            "approved_date": str(r.approved_date) if r.approved_date else None,
            "effective_date": str(r.effective_date) if r.effective_date else None,
            "status": r.status,
        }
        for r in rows
    ]


def get_product(session: Session, product_id: str) -> dict[str, Any] | None:
    r = session.get(Product, product_id)
    if not r:
        return None
    return {
        "product_id": r.product_id,
        "product_name": r.product_name,
        "model_name": r.model_name,
        "revision": r.revision,
        "lifecycle_status": r.lifecycle_status,
    }
