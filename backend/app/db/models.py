"""
SQLAlchemy ORM models — synthetic ERP / PLM / MES.

Note:
- 본 PoC는 SQLite + synthetic CSV 기반.
- 실제 운영에서는 ERP/PLM/MES 별도 DB로 분리되어야 한다.
- ID 체계는 PoC 단순화를 위해 시스템 간 동일 코드를 가정한다.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# =====================
# ERP
# =====================
class Customer(Base):
    __tablename__ = "erp_customers"
    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_name: Mapped[str] = mapped_column(String)
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    contact: Mapped[str | None] = mapped_column(String, nullable=True)


class Supplier(Base):
    __tablename__ = "erp_suppliers"
    supplier_id: Mapped[str] = mapped_column(String, primary_key=True)
    supplier_name: Mapped[str] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[str | None] = mapped_column(String, nullable=True)


class Item(Base):
    __tablename__ = "erp_items"
    item_id: Mapped[str] = mapped_column(String, primary_key=True)
    item_name: Mapped[str] = mapped_column(String)
    item_type: Mapped[str] = mapped_column(String)  # RAW / PART / PRODUCT
    unit: Mapped[str | None] = mapped_column(String, nullable=True)
    standard_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    supplier_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("erp_suppliers.supplier_id"), nullable=True
    )


class PurchaseOrder(Base):
    __tablename__ = "erp_purchase_orders"
    po_id: Mapped[str] = mapped_column(String, primary_key=True)
    supplier_id: Mapped[str] = mapped_column(String, ForeignKey("erp_suppliers.supplier_id"))
    item_id: Mapped[str] = mapped_column(String, ForeignKey("erp_items.item_id"))
    order_date: Mapped[date] = mapped_column(Date)
    delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)


class SalesOrder(Base):
    __tablename__ = "erp_sales_orders"
    so_id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("erp_customers.customer_id"))
    product_id: Mapped[str] = mapped_column(String)
    order_date: Mapped[date] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)


class Inventory(Base):
    __tablename__ = "erp_inventory"
    inventory_id: Mapped[str] = mapped_column(String, primary_key=True)
    item_id: Mapped[str] = mapped_column(String, ForeignKey("erp_items.item_id"))
    warehouse_id: Mapped[str | None] = mapped_column(String, nullable=True)
    quantity_on_hand: Mapped[int] = mapped_column(Integer)
    safety_stock: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Cost(Base):
    __tablename__ = "erp_costs"
    cost_id: Mapped[str] = mapped_column(String, primary_key=True)
    item_id: Mapped[str] = mapped_column(String, ForeignKey("erp_items.item_id"))
    period: Mapped[str] = mapped_column(String)  # YYYY-MM
    material_cost: Mapped[float] = mapped_column(Float, default=0.0)
    labor_cost: Mapped[float] = mapped_column(Float, default=0.0)
    overhead_cost: Mapped[float] = mapped_column(Float, default=0.0)


# =====================
# PLM
# =====================
class Product(Base):
    __tablename__ = "plm_products"
    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_name: Mapped[str] = mapped_column(String)
    model_name: Mapped[str | None] = mapped_column(String, nullable=True)
    revision: Mapped[str | None] = mapped_column(String, nullable=True)
    lifecycle_status: Mapped[str | None] = mapped_column(String, nullable=True)


class Part(Base):
    __tablename__ = "plm_parts"
    part_id: Mapped[str] = mapped_column(String, primary_key=True)
    part_name: Mapped[str] = mapped_column(String)
    part_type: Mapped[str | None] = mapped_column(String, nullable=True)
    supplier_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("erp_suppliers.supplier_id"), nullable=True
    )


class Bom(Base):
    __tablename__ = "plm_bom"
    bom_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("plm_products.product_id"))
    parent_part_id: Mapped[str | None] = mapped_column(String, nullable=True)
    child_part_id: Mapped[str] = mapped_column(String, ForeignKey("plm_parts.part_id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    revision: Mapped[str | None] = mapped_column(String, nullable=True)
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    approval_status: Mapped[str | None] = mapped_column(String, nullable=True)


class DesignDocument(Base):
    __tablename__ = "plm_design_documents"
    document_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("plm_products.product_id"))
    doc_type: Mapped[str | None] = mapped_column(String, nullable=True)
    revision: Mapped[str | None] = mapped_column(String, nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String, nullable=True)
    approved_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class Ecr(Base):
    __tablename__ = "plm_ecr"
    ecr_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("plm_products.product_id"))
    requested_by: Mapped[str | None] = mapped_column(String, nullable=True)
    request_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)


class Eco(Base):
    __tablename__ = "plm_eco"
    eco_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("plm_products.product_id"))
    changed_part_id: Mapped[str] = mapped_column(String, ForeignKey("plm_parts.part_id"))
    change_type: Mapped[str | None] = mapped_column(String, nullable=True)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    approved_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)


# =====================
# MES
# =====================
class WorkOrder(Base):
    __tablename__ = "mes_work_orders"
    work_order_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String)
    planned_qty: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)


class Equipment(Base):
    __tablename__ = "mes_equipment"
    equipment_id: Mapped[str] = mapped_column(String, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(String)
    equipment_type: Mapped[str | None] = mapped_column(String, nullable=True)
    line_id: Mapped[str | None] = mapped_column(String, nullable=True)


class Process(Base):
    __tablename__ = "mes_processes"
    process_id: Mapped[str] = mapped_column(String, primary_key=True)
    process_name: Mapped[str] = mapped_column(String)
    sequence: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Lot(Base):
    __tablename__ = "mes_lots"
    lot_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String)
    work_order_id: Mapped[str] = mapped_column(String, ForeignKey("mes_work_orders.work_order_id"))
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)


class ProductionResult(Base):
    __tablename__ = "mes_production_results"
    result_id: Mapped[str] = mapped_column(String, primary_key=True)
    work_order_id: Mapped[str] = mapped_column(String, ForeignKey("mes_work_orders.work_order_id"))
    product_id: Mapped[str] = mapped_column(String)
    lot_id: Mapped[str] = mapped_column(String, ForeignKey("mes_lots.lot_id"))
    process_id: Mapped[str] = mapped_column(String, ForeignKey("mes_processes.process_id"))
    equipment_id: Mapped[str] = mapped_column(String, ForeignKey("mes_equipment.equipment_id"))
    production_date: Mapped[date] = mapped_column(Date)
    shift: Mapped[str | None] = mapped_column(String, nullable=True)
    produced_qty: Mapped[int] = mapped_column(Integer, default=0)
    defect_qty: Mapped[int] = mapped_column(Integer, default=0)


class QualityInspection(Base):
    __tablename__ = "mes_quality_inspections"
    inspection_id: Mapped[str] = mapped_column(String, primary_key=True)
    lot_id: Mapped[str] = mapped_column(String, ForeignKey("mes_lots.lot_id"))
    product_id: Mapped[str] = mapped_column(String)
    inspector: Mapped[str | None] = mapped_column(String, nullable=True)
    inspected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    pass_qty: Mapped[int] = mapped_column(Integer, default=0)
    fail_qty: Mapped[int] = mapped_column(Integer, default=0)


class Defect(Base):
    __tablename__ = "mes_defects"
    defect_id: Mapped[str] = mapped_column(String, primary_key=True)
    lot_id: Mapped[str] = mapped_column(String, ForeignKey("mes_lots.lot_id"))
    product_id: Mapped[str] = mapped_column(String)
    process_id: Mapped[str] = mapped_column(String, ForeignKey("mes_processes.process_id"))
    equipment_id: Mapped[str] = mapped_column(String, ForeignKey("mes_equipment.equipment_id"))
    defect_type: Mapped[str] = mapped_column(String)
    defect_qty: Mapped[int] = mapped_column(Integer, default=0)
    detected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
