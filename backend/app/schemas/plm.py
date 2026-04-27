from __future__ import annotations

from pydantic import BaseModel


class BomLine(BaseModel):
    bom_id: str
    product_id: str
    parent_part_id: str | None = None
    child_part_id: str
    quantity: int
    revision: str
    approval_status: str | None = None


class EngineeringChange(BaseModel):
    eco_id: str
    product_id: str
    changed_part_id: str
    change_type: str
    reason: str | None = None
    approved_date: str | None = None
    effective_date: str | None = None
    status: str | None = None
