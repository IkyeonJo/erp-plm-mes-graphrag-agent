// =============================================================
// 01_schema.cypher — 노드/관계 스키마 가이드
//   Neo4j는 schema-on-write가 부분 적용되므로 본 파일은 "사용되는 라벨/관계의 정의"를 코드로 명시한다.
//   실제 데이터는 03_load_data.cypher 에서 적재한다.
// =============================================================

// 라벨: Product, Part, BOM, Supplier, WorkOrder, Lot, Process, Equipment, Defect, EngineeringChange, Document

// 관계 (일관성 유지)
//   (:Product)-[:HAS_PART]->(:Part)
//   (:Part)-[:SUPPLIED_BY]->(:Supplier)
//   (:Product)-[:HAS_BOM]->(:BOM)
//   (:BOM)-[:CONTAINS]->(:Part)
//   (:Product)-[:PRODUCED_IN]->(:Process)
//   (:Process)-[:USES]->(:Equipment)
//   (:WorkOrder)-[:PRODUCES]->(:Product)
//   (:WorkOrder)-[:CREATES]->(:Lot)
//   (:Lot)-[:PRODUCED_PRODUCT]->(:Product)
//   (:Lot)-[:USED_PART]->(:Part)
//   (:Lot)-[:HAS_DEFECT]->(:Defect)
//   (:Defect)-[:OCCURRED_IN]->(:Process)
//   (:Defect)-[:OCCURRED_AT]->(:Equipment)
//   (:Product)-[:CHANGED_BY]->(:EngineeringChange)
//   (:EngineeringChange)-[:CHANGES]->(:Part)
//   (:Document)-[:DESCRIBES]->(:Product)

// 인덱스 (대표)
CREATE INDEX product_id_idx IF NOT EXISTS FOR (p:Product) ON (p.product_id);
CREATE INDEX part_id_idx    IF NOT EXISTS FOR (p:Part)    ON (p.part_id);
CREATE INDEX supplier_id_idx IF NOT EXISTS FOR (s:Supplier) ON (s.supplier_id);
CREATE INDEX lot_id_idx     IF NOT EXISTS FOR (l:Lot)     ON (l.lot_id);
CREATE INDEX eco_id_idx     IF NOT EXISTS FOR (e:EngineeringChange) ON (e.eco_id);
