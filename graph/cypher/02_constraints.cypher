// =============================================================
// 02_constraints.cypher — 핵심 ID Uniqueness 보장
// =============================================================

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.product_id IS UNIQUE;

CREATE CONSTRAINT part_id_unique IF NOT EXISTS
FOR (p:Part) REQUIRE p.part_id IS UNIQUE;

CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
FOR (s:Supplier) REQUIRE s.supplier_id IS UNIQUE;

CREATE CONSTRAINT bom_id_unique IF NOT EXISTS
FOR (b:BOM) REQUIRE b.bom_id IS UNIQUE;

CREATE CONSTRAINT work_order_id_unique IF NOT EXISTS
FOR (w:WorkOrder) REQUIRE w.work_order_id IS UNIQUE;

CREATE CONSTRAINT lot_id_unique IF NOT EXISTS
FOR (l:Lot) REQUIRE l.lot_id IS UNIQUE;

CREATE CONSTRAINT process_id_unique IF NOT EXISTS
FOR (p:Process) REQUIRE p.process_id IS UNIQUE;

CREATE CONSTRAINT equipment_id_unique IF NOT EXISTS
FOR (e:Equipment) REQUIRE e.equipment_id IS UNIQUE;

CREATE CONSTRAINT defect_id_unique IF NOT EXISTS
FOR (d:Defect) REQUIRE d.defect_id IS UNIQUE;

CREATE CONSTRAINT eco_id_unique IF NOT EXISTS
FOR (e:EngineeringChange) REQUIRE e.eco_id IS UNIQUE;

CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document) REQUIRE d.document_id IS UNIQUE;
