from __future__ import annotations

from pydantic import BaseModel


class ProductionResult(BaseModel):
    result_id: str
    work_order_id: str
    product_id: str
    lot_id: str
    process_id: str
    equipment_id: str
    production_date: str
    shift: str
    produced_qty: int
    defect_qty: int


class DefectSummary(BaseModel):
    defect_type: str
    count: int
    last_detected_at: str | None = None
