# Ontology Notes

## 목적

공고에 OWL/RDF/SPARQL이 포함되어 있어, 본 포트폴리오는 **최소 ontology 샘플**을 포함한다.
실제 제조업 도입 시에는 다음 표준 매핑을 권장한다.

| 표준 | 용도 |
|---|---|
| ISA-95 | Enterprise–Control 통합, 작업/생산 모델 |
| OAGIS | ERP/PLM/MES 메시지 통합 |
| ISO 10303 (STEP) | CAD/PLM 데이터 표현 |
| MIMOSA / OSA-EAI | 설비 / 자산 관리 |

## 본 PoC ontology 구성

- 클래스: `ManufacturingEntity`, `Product`, `Part`, `Supplier`, `Process`, `Equipment`, `Defect`, `EngineeringChange`, `Lot`
- 관계: `hasPart`, `suppliedBy`, `producedIn`, `usesEquipment`, `hasDefect`, `producedProduct`, `changedBy`, `changesPart`
- 시나리오 데이터: ECO-2026-009 (P-203 → P-204 공급사 변경) 등

## SPARQL Tool

`backend/app/tools/sparql_tool.py`

- `manufacturing.ttl` 을 rdflib로 로드하고 SELECT 쿼리만 허용
- INSERT / DELETE / DROP / CLEAR / CREATE 차단
- LangGraph `call_sparql_agent` 노드가 호출

## Phase 2 확장

- ontology를 ISA-95 라벨 매핑으로 확장
- Neo4j에 `n10s` (neosemantics) 플러그인을 통해 RDF 적재
- LLM이 ontology를 활용해 **schema-aware question rewriting** 수행
