// =============================================================
// 04_sample_queries.cypher — 5개 Use Case에 매핑되는 대표 GraphRAG 질의
// =============================================================

// 1. 제품의 부품 트리
MATCH (p:Product {product_id: $product_id})-[:HAS_PART]->(part:Part)
RETURN p, part;

// 2. 공급사 → 부품 → 제품 영향도
MATCH (s:Supplier {supplier_id: $supplier_id})<-[:SUPPLIED_BY]-(part:Part)<-[:HAS_PART]-(p:Product)
RETURN s.supplier_id AS supplier_id,
       collect(DISTINCT part.part_id) AS parts,
       collect(DISTINCT p.product_id) AS products;

// 3. 제품의 LOT/불량 추적 (최근 N개)
MATCH (p:Product {product_id: $product_id})<-[:PRODUCED_PRODUCT]-(lot:Lot)-[:HAS_DEFECT]->(d:Defect)
RETURN lot.lot_id AS lot_id,
       d.defect_type AS defect_type,
       d.defect_qty  AS defect_qty
ORDER BY d.defect_qty DESC
LIMIT 20;

// 4. 제품 → 공정 → 설비 경로
MATCH (p:Product {product_id: $product_id})-[:PRODUCED_IN]->(proc:Process)-[:USES]->(eq:Equipment)
RETURN p.product_id, proc.process_id, eq.equipment_id;

// 5. 설계변경의 영향 부품/제품
MATCH (p:Product)-[:CHANGED_BY]->(eco:EngineeringChange)-[:CHANGES]->(part:Part)
WHERE eco.effective_date >= date($from)
RETURN p.product_id, eco.eco_id, eco.change_type, part.part_id, eco.effective_date
ORDER BY eco.effective_date DESC;

// 6. 공급사 → 부품 → 제품 → LOT → 불량 (Use Case 3)
MATCH (s:Supplier {supplier_id: $supplier_id})<-[:SUPPLIED_BY]-(part:Part)<-[:HAS_PART]-(p:Product)<-[:PRODUCED_PRODUCT]-(lot:Lot)-[:HAS_DEFECT]->(d:Defect)
RETURN s.supplier_id AS supplier_id,
       part.part_id  AS part_id,
       p.product_id  AS product_id,
       lot.lot_id    AS lot_id,
       d.defect_type AS defect_type,
       d.defect_qty  AS qty
ORDER BY qty DESC
LIMIT 50;
