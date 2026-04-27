"""
synthetic CSV → SQLite seed.

사용법:
    uv run python -m app.db.seed

CSV 파일은 SYNTHETIC_DATA_DIR 하위에서 읽는다.
파일이 없으면 안내 메시지 출력 후 종료.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Base
from app.db.session import SessionLocal, engine

logger = logging.getLogger(__name__)


CSV_TO_TABLE: dict[str, tuple[str, str]] = {
    # csv path (relative to SYNTHETIC_DATA_DIR) → (sub-folder, table name)
    "erp/customers.csv": ("erp", "erp_customers"),
    "erp/suppliers.csv": ("erp", "erp_suppliers"),
    "erp/items.csv": ("erp", "erp_items"),
    "erp/purchase_orders.csv": ("erp", "erp_purchase_orders"),
    "erp/sales_orders.csv": ("erp", "erp_sales_orders"),
    "erp/inventory.csv": ("erp", "erp_inventory"),
    "erp/costs.csv": ("erp", "erp_costs"),
    "plm/products.csv": ("plm", "plm_products"),
    "plm/parts.csv": ("plm", "plm_parts"),
    "plm/bom.csv": ("plm", "plm_bom"),
    "plm/design_documents.csv": ("plm", "plm_design_documents"),
    "plm/ecr.csv": ("plm", "plm_ecr"),
    "plm/eco.csv": ("plm", "plm_eco"),
    "mes/work_orders.csv": ("mes", "mes_work_orders"),
    "mes/equipment.csv": ("mes", "mes_equipment"),
    "mes/processes.csv": ("mes", "mes_processes"),
    "mes/lots.csv": ("mes", "mes_lots"),
    "mes/production_results.csv": ("mes", "mes_production_results"),
    "mes/quality_inspections.csv": ("mes", "mes_quality_inspections"),
    "mes/defects.csv": ("mes", "mes_defects"),
}


def init_schema() -> None:
    Base.metadata.create_all(engine)


def load_csv_to_table(session: Session, csv_path: Path, table_name: str) -> int:
    if not csv_path.exists():
        logger.warning("CSV not found, skip: %s", csv_path)
        return 0

    df = pd.read_csv(csv_path)
    if df.empty:
        return 0

    df.to_sql(table_name, engine, if_exists="append", index=False)
    return len(df)


def run() -> None:
    init_schema()
    base = Path(settings.SYNTHETIC_DATA_DIR).resolve()

    if not base.exists():
        logger.error(
            "synthetic data directory not found: %s\n"
            "→ data/generate_synthetic_data.py 를 먼저 실행하세요.",
            base,
        )
        return

    with SessionLocal() as session:
        total = 0
        for rel_csv, (_subdir, table_name) in CSV_TO_TABLE.items():
            csv_path = base / rel_csv
            inserted = load_csv_to_table(session, csv_path, table_name)
            if inserted:
                logger.info("loaded %s rows → %s", inserted, table_name)
                total += inserted
        session.commit()
        logger.info("seed done. total rows = %s", total)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
