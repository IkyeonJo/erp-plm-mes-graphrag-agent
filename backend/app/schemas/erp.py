from __future__ import annotations

from pydantic import BaseModel


class InventorySummary(BaseModel):
    item_id: str
    quantity_on_hand: int
    safety_stock: int
    warehouse_id: str | None = None


class SupplierItem(BaseModel):
    supplier_id: str
    supplier_name: str
    rating: str | None = None
