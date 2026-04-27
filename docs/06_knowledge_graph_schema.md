# 06. Knowledge Graph Schema (Neo4j)

ERP/PLM/MES synthetic data를 GraphRAG에 활용하기 위한 Neo4j 스키마와 활용 방식.

---

## 1. Nodes

| Label | 주요 속성 |
|---|---|
| `Product` | product_id, product_name, model_name, revision, lifecycle_status |
| `Part` | part_id, part_name, part_type |
| `BOM` | bom_id, revision, effective_from, effective_to, approval_status |
| `Supplier` | supplier_id, supplier_name, country, rating |
| `WorkOrder` | work_order_id, planned_qty, start_date, end_date, status |
| `Lot` | lot_id, start_time, end_time, status |
| `Process` | process_id, process_name, sequence |
| `Equipment` | equipment_id, equipment_name, equipment_type, line_id |
| `Defect` | defect_id, defect_type, defect_qty, detected_at |
| `EngineeringChange` | eco_id, change_type, reason, approved_date, effective_date |
| `Document` | document_id, doc_type, revision, approved_by, approved_date |

## 2. Relationships

```text
(:Product)-[:HAS_PART]->(:Part)
(:Part)-[:SUPPLIED_BY]->(:Supplier)
(:Product)-[:HAS_BOM]->(:BOM)
(:BOM)-[:CONTAINS]->(:Part)
(:Product)-[:PRODUCED_IN]->(:Process)
(:Process)-[:USES]->(:Equipment)
(:WorkOrder)-[:PRODUCES]->(:Product)
(:WorkOrder)-[:CREATES]->(:Lot)
(:Lot)-[:PRODUCED_PRODUCT]->(:Product)
(:Lot)-[:USED_PART]->(:Part)
(:Lot)-[:HAS_DEFECT]->(:Defect)
(:Defect)-[:OCCURRED_IN]->(:Process)
(:Defect)-[:OCCURRED_AT]->(:Equipment)
(:Product)-[:CHANGED_BY]->(:EngineeringChange)
(:EngineeringChange)-[:CHANGES]->(:Part)
(:Document)-[:DESCRIBES]->(:Product)
```

## 3. Constraints (대표)

```cypher
CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.product_id IS UNIQUE;

CREATE CONSTRAINT part_id_unique IF NOT EXISTS
FOR (p:Part) REQUIRE p.part_id IS UNIQUE;

CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
FOR (s:Supplier) REQUIRE s.supplier_id IS UNIQUE;

CREATE CONSTRAINT lot_id_unique IF NOT EXISTS
FOR (l:Lot) REQUIRE l.lot_id IS UNIQUE;

CREATE CONSTRAINT eco_id_unique IF NOT EXISTS
FOR (e:EngineeringChange) REQUIRE e.eco_id IS UNIQUE;
```

## 4. 대표 GraphRAG 질의

### 4.1 제품 부품 트리

```cypher
MATCH (p:Product {product_id: $product_id})-[:HAS_PART]->(part:Part)
RETURN p, part;
```

### 4.2 공급사 영향도

```cypher
MATCH (s:Supplier {supplier_id: $supplier_id})<-[:SUPPLIED_BY]-(part:Part)<-[:HAS_PART]-(p:Product)
RETURN s, part, p;
```

### 4.3 제품의 LOT/불량 추적

```cypher
MATCH (p:Product {product_id: $product_id})<-[:PRODUCED_PRODUCT]-(lot:Lot)-[:HAS_DEFECT]->(d:Defect)
RETURN p, lot, d;
```

### 4.4 제품 → 공정 → 설비 경로

```cypher
MATCH (p:Product {product_id: $product_id})-[:PRODUCED_IN]->(proc:Process)-[:USES]->(eq:Equipment)
RETURN p, proc, eq;
```

### 4.5 설계변경의 영향 부품·제품

```cypher
MATCH (p:Product)-[:CHANGED_BY]->(eco:EngineeringChange)-[:CHANGES]->(part:Part)
WHERE eco.effective_date >= date($from)
RETURN p, eco, part;
```

## 5. GraphRAG 활용 방식

LangGraph의 `call_graph_agent` Node에서 다음 패턴 사용:

1. 사용자가 "공급사 S-03이 들어간 제품과 최근 품질 이슈"를 묻는다.
2. `call_graph_agent`가 4.2 / 4.3 쿼리를 조합하여 `Supplier → Part → Product → Lot → Defect` 경로를 한 번에 가져온다.
3. 결과는 `graph_path` 형태로 evidence에 누적:
   ```json
   {
     "source": "Neo4j",
     "graph_path": "Supplier(S-03) → Part(P-203) → Product(PROD-A) → Lot(LOT-L24041) → Defect(Solder Crack)",
     "record_id": "neo4j-path-001"
   }
   ```
4. Response Agent가 이 경로를 자연어로 풀어내어 답변에 포함.

## 6. 데이터 적재 전략

- 초기 MVP: synthetic CSV → SQLite seed 후 Python loader로 Neo4j에 MERGE
- 또는 Cypher `LOAD CSV WITH HEADERS` 직접 사용
- `graph/cypher/03_load_data.cypher` 가 이 절차의 SQL/Cypher 정의 위치
