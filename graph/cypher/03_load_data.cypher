// =============================================================
// 03_load_data.cypher — synthetic CSV → Neo4j 적재
// 사용 전:
//   1) docker compose 실행 시 /var/lib/neo4j/import/cypher 에 graph/cypher 가 마운트된다.
//   2) data/synthetic 도 별도 import 위치(또는 ./data 마운트)에서 접근 가능해야 한다.
//   3) 본 파일은 :params 와 함께 Neo4j Browser 또는 cypher-shell 에서 실행한다.
//
// 본 PoC에서는 CSV 직접 적재 대신, backend의 graph_loader (Python) 사용을 권장한다.
// 본 cypher 파일은 "이렇게 적재된다"는 참조 구조를 보여준다.
// =============================================================

// --- Products
LOAD CSV WITH HEADERS FROM 'file:///plm/products.csv' AS row
MERGE (p:Product {product_id: row.product_id})
SET p.product_name = row.product_name,
    p.model_name   = row.model_name,
    p.revision     = row.revision,
    p.lifecycle_status = row.lifecycle_status;

// --- Parts
LOAD CSV WITH HEADERS FROM 'file:///plm/parts.csv' AS row
MERGE (part:Part {part_id: row.part_id})
SET part.part_name = row.part_name,
    part.part_type = row.part_type;

// --- Suppliers
LOAD CSV WITH HEADERS FROM 'file:///erp/suppliers.csv' AS row
MERGE (s:Supplier {supplier_id: row.supplier_id})
SET s.supplier_name = row.supplier_name,
    s.country       = row.country,
    s.rating        = row.rating;

// --- Part SUPPLIED_BY Supplier
LOAD CSV WITH HEADERS FROM 'file:///plm/parts.csv' AS row
WITH row WHERE row.supplier_id IS NOT NULL AND row.supplier_id <> ''
MATCH (part:Part {part_id: row.part_id})
MATCH (s:Supplier {supplier_id: row.supplier_id})
MERGE (part)-[:SUPPLIED_BY]->(s);

// --- BOM (Product HAS_PART Part) — PoC 단순화: parent_part_id가 없으면 product가 직접 has_part
LOAD CSV WITH HEADERS FROM 'file:///plm/bom.csv' AS row
MATCH (p:Product {product_id: row.product_id})
MATCH (part:Part {part_id: row.child_part_id})
MERGE (p)-[r:HAS_PART]->(part)
SET r.bom_id = row.bom_id,
    r.quantity = toInteger(row.quantity),
    r.revision = row.revision,
    r.approval_status = row.approval_status;

// --- Processes
LOAD CSV WITH HEADERS FROM 'file:///mes/processes.csv' AS row
MERGE (proc:Process {process_id: row.process_id})
SET proc.process_name = row.process_name,
    proc.sequence     = toInteger(row.sequence);

// --- Equipment
LOAD CSV WITH HEADERS FROM 'file:///mes/equipment.csv' AS row
MERGE (eq:Equipment {equipment_id: row.equipment_id})
SET eq.equipment_name = row.equipment_name,
    eq.equipment_type = row.equipment_type,
    eq.line_id        = row.line_id;

// --- WorkOrders & Lots
LOAD CSV WITH HEADERS FROM 'file:///mes/work_orders.csv' AS row
MERGE (w:WorkOrder {work_order_id: row.work_order_id})
SET w.planned_qty = toInteger(row.planned_qty),
    w.status      = row.status,
    w.start_date  = date(row.start_date),
    w.end_date    = date(row.end_date)
WITH w, row
MATCH (p:Product {product_id: row.product_id})
MERGE (w)-[:PRODUCES]->(p);

LOAD CSV WITH HEADERS FROM 'file:///mes/lots.csv' AS row
MERGE (l:Lot {lot_id: row.lot_id})
SET l.status = row.status
WITH l, row
MATCH (p:Product {product_id: row.product_id})
MATCH (w:WorkOrder {work_order_id: row.work_order_id})
MERGE (l)-[:PRODUCED_PRODUCT]->(p)
MERGE (w)-[:CREATES]->(l);

// --- Production results: Process 와 Equipment 연결 (Product PRODUCED_IN Process, Process USES Equipment)
LOAD CSV WITH HEADERS FROM 'file:///mes/production_results.csv' AS row
MATCH (p:Product {product_id: row.product_id})
MATCH (proc:Process {process_id: row.process_id})
MATCH (eq:Equipment {equipment_id: row.equipment_id})
MERGE (p)-[:PRODUCED_IN]->(proc)
MERGE (proc)-[:USES]->(eq);

// --- Defects
LOAD CSV WITH HEADERS FROM 'file:///mes/defects.csv' AS row
MERGE (d:Defect {defect_id: row.defect_id})
SET d.defect_type = row.defect_type,
    d.defect_qty  = toInteger(row.defect_qty)
WITH d, row
MATCH (l:Lot {lot_id: row.lot_id})
MATCH (proc:Process {process_id: row.process_id})
MATCH (eq:Equipment {equipment_id: row.equipment_id})
MERGE (l)-[:HAS_DEFECT]->(d)
MERGE (d)-[:OCCURRED_IN]->(proc)
MERGE (d)-[:OCCURRED_AT]->(eq);

// --- ECO
LOAD CSV WITH HEADERS FROM 'file:///plm/eco.csv' AS row
MERGE (e:EngineeringChange {eco_id: row.eco_id})
SET e.change_type = row.change_type,
    e.reason      = row.reason,
    e.approved_date = date(row.approved_date),
    e.effective_date = date(row.effective_date),
    e.status      = row.status
WITH e, row
MATCH (p:Product {product_id: row.product_id})
MATCH (part:Part {part_id: row.changed_part_id})
MERGE (p)-[:CHANGED_BY]->(e)
MERGE (e)-[:CHANGES]->(part);

// --- Documents
LOAD CSV WITH HEADERS FROM 'file:///plm/design_documents.csv' AS row
MERGE (d:Document {document_id: row.document_id})
SET d.doc_type = row.doc_type,
    d.revision = row.revision,
    d.approved_by = row.approved_by,
    d.approved_date = date(row.approved_date)
WITH d, row
MATCH (p:Product {product_id: row.product_id})
MERGE (d)-[:DESCRIBES]->(p);
