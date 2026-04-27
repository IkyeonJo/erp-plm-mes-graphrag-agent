from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Defect, Lot, ProductionResult


def get_production_results(
    session: Session, product_id: str, limit: int = 100
) -> list[dict[str, Any]]:
    rows = session.scalars(
        select(ProductionResult).where(ProductionResult.product_id == product_id).limit(limit)
    ).all()
    return [
        {
            "result_id": r.result_id,
            "work_order_id": r.work_order_id,
            "product_id": r.product_id,
            "lot_id": r.lot_id,
            "process_id": r.process_id,
            "equipment_id": r.equipment_id,
            "production_date": str(r.production_date),
            "shift": r.shift,
            "produced_qty": r.produced_qty,
            "defect_qty": r.defect_qty,
        }
        for r in rows
    ]


def get_monthly_defect_rate(session: Session, product_id: str) -> list[dict[str, Any]]:
    """SQLite 기준 strftime 사용. 월별 (defect_qty / produced_qty)."""
    period = func.strftime("%Y-%m", ProductionResult.production_date).label("period")
    stmt = (
        select(
            period,
            func.sum(ProductionResult.produced_qty).label("produced_qty"),
            func.sum(ProductionResult.defect_qty).label("defect_qty"),
        )
        .where(ProductionResult.product_id == product_id)
        .group_by(period)
        .order_by(period)
    )
    out: list[dict[str, Any]] = []
    for p, prod, defect in session.execute(stmt).all():
        rate = (defect / prod) if prod else 0.0
        out.append(
            {
                "period": p,
                "produced_qty": int(prod or 0),
                "defect_qty": int(defect or 0),
                "defect_rate": round(rate, 4),
            }
        )
    return out


def trace_lot(session: Session, lot_id: str) -> dict[str, Any] | None:
    lot = session.get(Lot, lot_id)
    if not lot:
        return None
    results = session.scalars(
        select(ProductionResult).where(ProductionResult.lot_id == lot_id)
    ).all()
    defects = session.scalars(select(Defect).where(Defect.lot_id == lot_id)).all()
    return {
        "lot_id": lot.lot_id,
        "product_id": lot.product_id,
        "work_order_id": lot.work_order_id,
        "status": lot.status,
        "production_results": [
            {
                "result_id": r.result_id,
                "process_id": r.process_id,
                "equipment_id": r.equipment_id,
                "produced_qty": r.produced_qty,
                "defect_qty": r.defect_qty,
                "production_date": str(r.production_date),
            }
            for r in results
        ],
        "defects": [
            {
                "defect_id": d.defect_id,
                "defect_type": d.defect_type,
                "defect_qty": d.defect_qty,
                "process_id": d.process_id,
                "equipment_id": d.equipment_id,
            }
            for d in defects
        ],
    }


def top_defect_types(
    session: Session, product_id: str | None = None, limit: int = 5
) -> list[dict[str, Any]]:
    stmt = select(Defect.defect_type, func.sum(Defect.defect_qty).label("qty")).group_by(
        Defect.defect_type
    )
    if product_id:
        stmt = stmt.where(Defect.product_id == product_id)
    stmt = stmt.order_by(func.sum(Defect.defect_qty).desc()).limit(limit)
    return [{"defect_type": dt, "qty": int(qty or 0)} for dt, qty in session.execute(stmt).all()]
