"""
Synthetic ERP / PLM / MES dataset generator.

목적:
- 5개 Use Case가 의미 있는 답을 만들 수 있도록 시나리오 데이터 구성.
- 시드 고정으로 재현 가능.

대표 시나리오:
- PROD-A 제품의 P-203 부품 공급사가 2026-03-01부터 S-02 → S-07로 변경됨.
- 변경 후 Solder Crack 불량이 PR-03 공정 / EQ-11 설비에서 집중 발생하여 불량률 상승.
- ECO-2026-014는 외장 케이스(P-501) 변경 — 품질 이슈와 직접 관련 낮음.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 42
random.seed(SEED)

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "synthetic"


@dataclass
class Paths:
    erp: Path
    plm: Path
    mes: Path

    @classmethod
    def from_root(cls, root: Path) -> "Paths":
        erp = root / "erp"
        plm = root / "plm"
        mes = root / "mes"
        for d in (erp, plm, mes):
            d.mkdir(parents=True, exist_ok=True)
        return cls(erp=erp, plm=plm, mes=mes)


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print(f"  ✓ {path.relative_to(path.parents[2])}: {len(rows)} rows")


# =======================
# ERP
# =======================

def generate_erp(p: Path) -> dict:
    customers = [
        ["C-001", "ACME Industrial", "Seoul", "010-****-1010"],
        ["C-002", "Daedong Auto", "Busan", "010-****-2020"],
        ["C-003", "Hanmi Electronics", "Daegu", "010-****-3030"],
    ]
    write_csv(
        p / "customers.csv",
        ["customer_id", "customer_name", "region", "contact"],
        customers,
    )

    suppliers = [
        ["S-01", "Nova Components", "KR", "A"],
        ["S-02", "Korea Parts Co.", "KR", "A"],
        ["S-03", "Asia Materials", "VN", "B"],
        ["S-07", "Vietnam Precision", "VN", "B"],
        ["S-09", "Global Solder Inc", "US", "A"],
    ]
    write_csv(
        p / "suppliers.csv",
        ["supplier_id", "supplier_name", "country", "rating"],
        suppliers,
    )

    items = [
        ["PROD-A", "Smart Sensor A", "PRODUCT", "EA", 120000.0, ""],
        ["PROD-B", "Smart Sensor B", "PRODUCT", "EA", 95000.0, ""],
        ["P-101", "Main PCB", "PART", "EA", 18000.0, "S-01"],
        ["P-203", "Connector Module", "PART", "EA", 4200.0, "S-02"],
        ["P-204", "Connector Module v2", "PART", "EA", 4500.0, "S-07"],
        ["P-301", "Sensor Chip", "PART", "EA", 26000.0, "S-09"],
        ["P-501", "External Case", "PART", "EA", 8000.0, "S-03"],
        ["P-502", "External Case v2", "PART", "EA", 8500.0, "S-03"],
    ]
    write_csv(
        p / "items.csv",
        [
            "item_id",
            "item_name",
            "item_type",
            "unit",
            "standard_cost",
            "supplier_id",
        ],
        items,
    )

    purchase_orders: list[list] = []
    base = date(2026, 1, 1)
    for i in range(40):
        d = base + timedelta(days=random.randint(0, 110))
        if i < 20:
            sup, item = "S-02", "P-203"
        else:
            sup, item = "S-07", "P-204"
        if d >= date(2026, 3, 1) and item == "P-203":
            sup, item = "S-07", "P-204"
        purchase_orders.append(
            [
                f"PO-{1000 + i}",
                sup,
                item,
                d.isoformat(),
                (d + timedelta(days=random.randint(3, 14))).isoformat(),
                random.randint(50, 500),
                round(4000 + random.random() * 800, 2),
                random.choice(["RECEIVED", "OPEN", "CLOSED"]),
            ]
        )
    write_csv(
        p / "purchase_orders.csv",
        [
            "po_id",
            "supplier_id",
            "item_id",
            "order_date",
            "delivery_date",
            "quantity",
            "unit_price",
            "status",
        ],
        purchase_orders,
    )

    sales_orders: list[list] = []
    for i in range(30):
        cust = random.choice(["C-001", "C-002", "C-003"])
        prod = random.choice(["PROD-A", "PROD-B"])
        d = base + timedelta(days=random.randint(0, 110))
        sales_orders.append(
            [
                f"SO-{2000 + i}",
                cust,
                prod,
                d.isoformat(),
                (d + timedelta(days=random.randint(7, 30))).isoformat(),
                random.randint(20, 200),
                random.choice(["OPEN", "CLOSED", "DELAYED"]),
            ]
        )
    write_csv(
        p / "sales_orders.csv",
        [
            "so_id",
            "customer_id",
            "product_id",
            "order_date",
            "due_date",
            "quantity",
            "status",
        ],
        sales_orders,
    )

    inventory = [
        ["INV-001", "PROD-A", "WH-01", 320, 100, datetime(2026, 4, 25).isoformat()],
        ["INV-002", "PROD-B", "WH-01", 110, 50, datetime(2026, 4, 25).isoformat()],
        ["INV-003", "P-101", "WH-02", 800, 200, datetime(2026, 4, 24).isoformat()],
        ["INV-004", "P-203", "WH-02", 50, 200, datetime(2026, 4, 24).isoformat()],
        ["INV-005", "P-204", "WH-02", 540, 200, datetime(2026, 4, 24).isoformat()],
        ["INV-006", "P-301", "WH-02", 460, 100, datetime(2026, 4, 24).isoformat()],
        ["INV-007", "P-501", "WH-02", 230, 100, datetime(2026, 4, 24).isoformat()],
    ]
    write_csv(
        p / "inventory.csv",
        [
            "inventory_id",
            "item_id",
            "warehouse_id",
            "quantity_on_hand",
            "safety_stock",
            "last_updated",
        ],
        inventory,
    )

    costs: list[list] = []
    for i, item in enumerate(["PROD-A", "PROD-B", "P-203", "P-204", "P-301"]):
        for m in range(1, 5):
            costs.append(
                [
                    f"COST-{3000 + i * 12 + m}",
                    item,
                    f"2026-{m:02d}",
                    round(20000 + random.random() * 5000, 2),
                    round(8000 + random.random() * 2000, 2),
                    round(4000 + random.random() * 1500, 2),
                ]
            )
    write_csv(
        p / "costs.csv",
        ["cost_id", "item_id", "period", "material_cost", "labor_cost", "overhead_cost"],
        costs,
    )

    return {"customers": len(customers), "suppliers": len(suppliers), "items": len(items)}


# =======================
# PLM
# =======================

def generate_plm(p: Path) -> dict:
    products = [
        ["PROD-A", "Smart Sensor A", "SSA-2026", "rev.4", "PROD"],
        ["PROD-B", "Smart Sensor B", "SSB-2026", "rev.2", "PROD"],
    ]
    write_csv(
        p / "products.csv",
        ["product_id", "product_name", "model_name", "revision", "lifecycle_status"],
        products,
    )

    parts = [
        ["P-101", "Main PCB", "PART", "S-01"],
        ["P-203", "Connector Module", "PART", "S-02"],
        ["P-204", "Connector Module v2", "PART", "S-07"],
        ["P-301", "Sensor Chip", "PART", "S-09"],
        ["P-501", "External Case", "PART", "S-03"],
        ["P-502", "External Case v2", "PART", "S-03"],
    ]
    write_csv(
        p / "parts.csv",
        ["part_id", "part_name", "part_type", "supplier_id"],
        parts,
    )

    bom: list[list] = []
    bom_id = 4000
    bom_rows_a = [
        ("PROD-A", "P-101", 1, "rev.4", date(2025, 12, 1), None, "APPROVED"),
        ("PROD-A", "P-203", 1, "rev.3", date(2025, 12, 1), date(2026, 2, 28), "APPROVED"),
        ("PROD-A", "P-204", 1, "rev.4", date(2026, 3, 1), None, "APPROVED"),
        ("PROD-A", "P-301", 2, "rev.4", date(2025, 12, 1), None, "APPROVED"),
        ("PROD-A", "P-501", 1, "rev.4", date(2025, 12, 1), None, "APPROVED"),
    ]
    for product_id, child, qty, rev, eff_from, eff_to, status in bom_rows_a:
        bom.append(
            [
                f"BOM-{bom_id}",
                product_id,
                "",
                child,
                qty,
                rev,
                eff_from.isoformat(),
                eff_to.isoformat() if eff_to else "",
                status,
            ]
        )
        bom_id += 1

    bom_rows_b = [
        ("PROD-B", "P-101", 1, "rev.2", date(2025, 12, 1), None, "APPROVED"),
        ("PROD-B", "P-204", 1, "rev.2", date(2025, 12, 1), None, "APPROVED"),
        ("PROD-B", "P-301", 1, "rev.2", date(2025, 12, 1), None, "APPROVED"),
        ("PROD-B", "P-502", 1, "rev.2", date(2025, 12, 1), None, "APPROVED"),
    ]
    for product_id, child, qty, rev, eff_from, eff_to, status in bom_rows_b:
        bom.append(
            [
                f"BOM-{bom_id}",
                product_id,
                "",
                child,
                qty,
                rev,
                eff_from.isoformat(),
                eff_to.isoformat() if eff_to else "",
                status,
            ]
        )
        bom_id += 1

    write_csv(
        p / "bom.csv",
        [
            "bom_id",
            "product_id",
            "parent_part_id",
            "child_part_id",
            "quantity",
            "revision",
            "effective_from",
            "effective_to",
            "approval_status",
        ],
        bom,
    )

    documents = [
        ["DOC-001", "PROD-A", "DRAWING", "rev.4", "design.team", "2025-12-15"],
        ["DOC-002", "PROD-A", "SPEC", "rev.4", "design.team", "2025-12-20"],
        ["DOC-003", "PROD-B", "DRAWING", "rev.2", "design.team", "2025-11-10"],
    ]
    write_csv(
        p / "design_documents.csv",
        ["document_id", "product_id", "doc_type", "revision", "approved_by", "approved_date"],
        documents,
    )

    ecr = [
        [
            "ECR-2026-007",
            "PROD-A",
            "quality.team",
            "2026-02-10",
            "P-203 공급사 품질 이슈",
            "APPROVED",
        ],
        [
            "ECR-2026-011",
            "PROD-A",
            "design.team",
            "2026-03-15",
            "외장 케이스 마감 변경",
            "APPROVED",
        ],
    ]
    write_csv(
        p / "ecr.csv",
        ["ecr_id", "product_id", "requested_by", "request_date", "reason", "status"],
        ecr,
    )

    eco = [
        [
            "ECO-2026-009",
            "PROD-A",
            "P-203",
            "SUPPLIER_CHANGE",
            "공급사 S-02 → S-07 (P-203 → P-204)",
            "2026-02-25",
            "2026-03-01",
            "EFFECTIVE",
        ],
        [
            "ECO-2026-014",
            "PROD-A",
            "P-501",
            "DESIGN_CHANGE",
            "외장 케이스 마감 변경",
            "2026-03-20",
            "2026-04-01",
            "EFFECTIVE",
        ],
        [
            "ECO-2026-018",
            "PROD-B",
            "P-502",
            "DESIGN_CHANGE",
            "외장 케이스 v2 적용",
            "2026-03-22",
            "2026-04-05",
            "EFFECTIVE",
        ],
    ]
    write_csv(
        p / "eco.csv",
        [
            "eco_id",
            "product_id",
            "changed_part_id",
            "change_type",
            "reason",
            "approved_date",
            "effective_date",
            "status",
        ],
        eco,
    )

    return {"products": len(products), "parts": len(parts), "bom": len(bom)}


# =======================
# MES
# =======================

def generate_mes(p: Path) -> dict:
    processes = [
        ["PR-01", "SMT Mounting", 1],
        ["PR-02", "Wave Soldering", 2],
        ["PR-03", "Connector Assembly", 3],
        ["PR-04", "Final Inspection", 4],
    ]
    write_csv(p / "processes.csv", ["process_id", "process_name", "sequence"], processes)

    equipment = [
        ["EQ-01", "SMT Line A", "SMT", "L1"],
        ["EQ-02", "Solder Bath A", "SOLDER", "L1"],
        ["EQ-11", "Connector Press 11", "ASSY", "L2"],
        ["EQ-12", "Connector Press 12", "ASSY", "L2"],
        ["EQ-21", "AOI Tester", "INSPECT", "L3"],
    ]
    write_csv(
        p / "equipment.csv",
        ["equipment_id", "equipment_name", "equipment_type", "line_id"],
        equipment,
    )

    work_orders: list[list] = []
    for i in range(20):
        prod = "PROD-A" if i < 14 else "PROD-B"
        start = date(2026, 1, 1) + timedelta(days=i * 6)
        end = start + timedelta(days=4)
        work_orders.append(
            [
                f"WO-{5000 + i}",
                prod,
                random.randint(80, 200),
                start.isoformat(),
                end.isoformat(),
                "CLOSED",
            ]
        )
    write_csv(
        p / "work_orders.csv",
        ["work_order_id", "product_id", "planned_qty", "start_date", "end_date", "status"],
        work_orders,
    )

    lots: list[list] = []
    for i in range(40):
        prod = "PROD-A" if i < 28 else "PROD-B"
        start_dt = datetime(2026, 1, 1) + timedelta(days=i * 3, hours=8)
        end_dt = start_dt + timedelta(hours=10)
        lots.append(
            [
                f"LOT-L{24000 + i}",
                prod,
                f"WO-{5000 + (i // 2) % 20}",
                start_dt.isoformat(),
                end_dt.isoformat(),
                "CLOSED",
            ]
        )
    write_csv(
        p / "lots.csv",
        ["lot_id", "product_id", "work_order_id", "start_time", "end_time", "status"],
        lots,
    )

    production_results: list[list] = []
    defects: list[list] = []
    inspections: list[list] = []

    rid = 6000
    did = 7000
    iid = 9000

    for i in range(40):
        prod = "PROD-A" if i < 28 else "PROD-B"
        lot_id = f"LOT-L{24000 + i}"
        wo_id = f"WO-{5000 + (i // 2) % 20}"
        production_date = date(2026, 1, 1) + timedelta(days=i * 3)
        for proc in ["PR-01", "PR-02", "PR-03", "PR-04"]:
            equip = (
                "EQ-01"
                if proc == "PR-01"
                else "EQ-02"
                if proc == "PR-02"
                else random.choice(["EQ-11", "EQ-12"])
                if proc == "PR-03"
                else "EQ-21"
            )
            produced = random.randint(80, 200)
            base_rate = 0.018
            if prod == "PROD-A" and production_date >= date(2026, 3, 1):
                if proc == "PR-03" and equip == "EQ-11":
                    base_rate = 0.05
                else:
                    base_rate = 0.022
            defect_q = max(0, int(produced * (base_rate + random.uniform(-0.005, 0.008))))
            production_results.append(
                [
                    f"RESULT-{rid}",
                    wo_id,
                    prod,
                    lot_id,
                    proc,
                    equip,
                    production_date.isoformat(),
                    random.choice(["DAY", "NIGHT"]),
                    produced,
                    defect_q,
                ]
            )
            rid += 1

            if defect_q > 0:
                if (
                    prod == "PROD-A"
                    and production_date >= date(2026, 3, 1)
                    and proc == "PR-03"
                    and equip == "EQ-11"
                ):
                    defect_type = "Solder Crack"
                else:
                    defect_type = random.choice(
                        ["Cosmetic Scratch", "Misalignment", "Solder Crack", "Open Circuit"]
                    )
                defects.append(
                    [
                        f"DEF-{did}",
                        lot_id,
                        prod,
                        proc,
                        equip,
                        defect_type,
                        defect_q,
                        datetime.combine(
                            production_date,
                            datetime.min.time(),
                        ).isoformat(),
                    ]
                )
                did += 1

        inspections.append(
            [
                f"INS-{iid}",
                lot_id,
                prod,
                "qa.team",
                datetime.combine(production_date, datetime.min.time()).isoformat(),
                random.randint(150, 300),
                random.randint(0, 12),
            ]
        )
        iid += 1

    write_csv(
        p / "production_results.csv",
        [
            "result_id",
            "work_order_id",
            "product_id",
            "lot_id",
            "process_id",
            "equipment_id",
            "production_date",
            "shift",
            "produced_qty",
            "defect_qty",
        ],
        production_results,
    )
    write_csv(
        p / "defects.csv",
        [
            "defect_id",
            "lot_id",
            "product_id",
            "process_id",
            "equipment_id",
            "defect_type",
            "defect_qty",
            "detected_at",
        ],
        defects,
    )
    write_csv(
        p / "quality_inspections.csv",
        [
            "inspection_id",
            "lot_id",
            "product_id",
            "inspector",
            "inspected_at",
            "pass_qty",
            "fail_qty",
        ],
        inspections,
    )

    return {
        "lots": len(lots),
        "production_results": len(production_results),
        "defects": len(defects),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic ERP/PLM/MES dataset")
    parser.add_argument(
        "--out",
        default=os.environ.get("SYNTHETIC_DATA_DIR", str(DEFAULT_OUT_DIR)),
        help="Output directory (default: ./synthetic)",
    )
    args = parser.parse_args()

    root = Path(args.out).resolve()
    root.mkdir(parents=True, exist_ok=True)
    p = Paths.from_root(root)

    print(f"[generate_synthetic_data] writing to {root}")
    print("ERP")
    erp = generate_erp(p.erp)
    print("PLM")
    plm = generate_plm(p.plm)
    print("MES")
    mes = generate_mes(p.mes)

    print("\nDone.")
    print(f"  ERP: {erp}")
    print(f"  PLM: {plm}")
    print(f"  MES: {mes}")


if __name__ == "__main__":
    main()
