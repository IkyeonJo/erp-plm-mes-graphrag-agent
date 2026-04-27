# 05. Data Model — ERP / PLM / MES

본 PoC의 synthetic data 모델. Key 정합성을 유지해야 5개 Use Case가 동작한다.

---

## 1. ERP Tables

### 1.1 customers

| 컬럼 | 타입 | 설명 |
|---|---|---|
| customer_id | TEXT (PK) | C-001 |
| customer_name | TEXT | |
| region | TEXT | |
| contact | TEXT | |

### 1.2 suppliers

| 컬럼 | 타입 | 설명 |
|---|---|---|
| supplier_id | TEXT (PK) | S-01 |
| supplier_name | TEXT | |
| country | TEXT | |
| rating | TEXT | A/B/C |

### 1.3 items

| 컬럼 | 타입 | 설명 |
|---|---|---|
| item_id | TEXT (PK) | I-001 (=part_id 또는 product_id 매핑) |
| item_name | TEXT | |
| item_type | TEXT | RAW / PART / PRODUCT |
| unit | TEXT | EA, kg |
| standard_cost | REAL | |
| supplier_id | TEXT (FK) | RAW/PART에 한해 |

### 1.4 purchase_orders

| 컬럼 | 타입 |
|---|---|
| po_id | TEXT (PK) |
| supplier_id | TEXT (FK) |
| item_id | TEXT (FK) |
| order_date | DATE |
| delivery_date | DATE |
| quantity | INT |
| unit_price | REAL |
| status | TEXT |

### 1.5 sales_orders

| 컬럼 | 타입 |
|---|---|
| so_id | TEXT (PK) |
| customer_id | TEXT (FK) |
| product_id | TEXT (FK) |
| order_date | DATE |
| due_date | DATE |
| quantity | INT |
| status | TEXT |

### 1.6 inventory

| 컬럼 | 타입 |
|---|---|
| inventory_id | TEXT (PK) |
| item_id | TEXT (FK) |
| warehouse_id | TEXT |
| quantity_on_hand | INT |
| safety_stock | INT |
| last_updated | DATETIME |

### 1.7 costs

| 컬럼 | 타입 |
|---|---|
| cost_id | TEXT (PK) |
| item_id | TEXT (FK) |
| period | TEXT (YYYY-MM) |
| material_cost | REAL |
| labor_cost | REAL |
| overhead_cost | REAL |

---

## 2. PLM Tables

### 2.1 products

| 컬럼 | 타입 |
|---|---|
| product_id | TEXT (PK) |
| product_name | TEXT |
| model_name | TEXT |
| revision | TEXT |
| lifecycle_status | TEXT (DEV / PROD / EOL) |

### 2.2 parts

| 컬럼 | 타입 |
|---|---|
| part_id | TEXT (PK) |
| part_name | TEXT |
| part_type | TEXT |
| supplier_id | TEXT (FK) |

### 2.3 bom

| 컬럼 | 타입 |
|---|---|
| bom_id | TEXT (PK) |
| product_id | TEXT (FK) |
| parent_part_id | TEXT (FK, nullable) |
| child_part_id | TEXT (FK) |
| quantity | INT |
| revision | TEXT |
| effective_from | DATE |
| effective_to | DATE |
| approval_status | TEXT |

### 2.4 design_documents

| 컬럼 | 타입 |
|---|---|
| document_id | TEXT (PK) |
| product_id | TEXT (FK) |
| doc_type | TEXT (DRAWING / SPEC / TEST) |
| revision | TEXT |
| approved_by | TEXT |
| approved_date | DATE |

### 2.5 ecr (Engineering Change Request)

| 컬럼 | 타입 |
|---|---|
| ecr_id | TEXT (PK) |
| product_id | TEXT (FK) |
| requested_by | TEXT |
| request_date | DATE |
| reason | TEXT |
| status | TEXT |

### 2.6 eco (Engineering Change Order)

| 컬럼 | 타입 |
|---|---|
| eco_id | TEXT (PK) |
| product_id | TEXT (FK) |
| changed_part_id | TEXT (FK) |
| change_type | TEXT |
| reason | TEXT |
| approved_date | DATE |
| effective_date | DATE |
| status | TEXT |

---

## 3. MES Tables

### 3.1 work_orders

| 컬럼 | 타입 |
|---|---|
| work_order_id | TEXT (PK) |
| product_id | TEXT (FK) |
| planned_qty | INT |
| start_date | DATE |
| end_date | DATE |
| status | TEXT |

### 3.2 production_results

| 컬럼 | 타입 |
|---|---|
| result_id | TEXT (PK) |
| work_order_id | TEXT (FK) |
| product_id | TEXT (FK) |
| lot_id | TEXT (FK) |
| process_id | TEXT (FK) |
| equipment_id | TEXT (FK) |
| production_date | DATE |
| shift | TEXT (DAY/NIGHT) |
| produced_qty | INT |
| defect_qty | INT |

### 3.3 equipment

| 컬럼 | 타입 |
|---|---|
| equipment_id | TEXT (PK) |
| equipment_name | TEXT |
| equipment_type | TEXT |
| line_id | TEXT |

### 3.4 processes

| 컬럼 | 타입 |
|---|---|
| process_id | TEXT (PK) |
| process_name | TEXT |
| sequence | INT |

### 3.5 quality_inspections

| 컬럼 | 타입 |
|---|---|
| inspection_id | TEXT (PK) |
| lot_id | TEXT (FK) |
| product_id | TEXT (FK) |
| inspector | TEXT |
| inspected_at | DATETIME |
| pass_qty | INT |
| fail_qty | INT |

### 3.6 defects

| 컬럼 | 타입 |
|---|---|
| defect_id | TEXT (PK) |
| lot_id | TEXT (FK) |
| product_id | TEXT (FK) |
| process_id | TEXT (FK) |
| equipment_id | TEXT (FK) |
| defect_type | TEXT |
| defect_qty | INT |
| detected_at | DATETIME |

### 3.7 lots

| 컬럼 | 타입 |
|---|---|
| lot_id | TEXT (PK) |
| product_id | TEXT (FK) |
| work_order_id | TEXT (FK) |
| start_time | DATETIME |
| end_time | DATETIME |
| status | TEXT |

---

## 4. 시스템 간 Key 매핑

| 개념 | ERP | PLM | MES |
|---|---|---|---|
| 제품 | items.item_id (item_type=PRODUCT) | products.product_id | work_orders.product_id |
| 부품 | items.item_id (item_type=PART/RAW) | parts.part_id, bom.child_part_id | (실투입은 별도 lot_components 가능) |
| 공급사 | suppliers.supplier_id, items.supplier_id | parts.supplier_id | — |
| LOT | — | — | lots.lot_id |
| 공정 | — | — | processes.process_id |
| 설비 | — | — | equipment.equipment_id |
| ECO | — | eco.eco_id | (적용 시점은 lots/production_results의 production_date로 판단) |

> PoC에서는 `item_id` 와 `product_id` / `part_id` 가 동일 ID 체계를 공유한다고 가정한다.
> 실제 고객사는 시스템마다 다른 코드체계를 갖는 경우가 많아, **기준정보 매핑 테이블**이 별도로 필요하다.

---

## 5. 정합성 규칙 (synthetic data generator)

- 모든 `product_id`는 PLM `products`에 먼저 존재해야 한다.
- 모든 `part_id`는 PLM `parts`에 존재해야 한다.
- `bom.child_part_id` 는 `parts.part_id` FK.
- `production_results.product_id` ⊆ `work_orders.product_id` ⊆ `products.product_id`.
- `defects.lot_id` ⊆ `lots.lot_id`, `defects.product_id` ⊆ `products.product_id`.
- ECO는 최소 1건 이상 “P-203 부품 공급사 변경(S-02 → S-07)” 시나리오를 포함하여, Use Case 1이 의미 있는 답을 만들 수 있게 한다.
