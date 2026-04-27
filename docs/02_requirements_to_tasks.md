# 02. Requirements → Technical Tasks

PL 역할의 핵심 역량 중 하나는 **현업의 자연어 요구사항을 기술 태스크로 분해**하는 것이다.
본 문서는 이 프로젝트가 처리하는 5개 Use Case에 대해 변환 예시를 제공한다.

---

## Use Case 1. "A제품 불량 원인을 한 번에 보고 싶다"

### 현업 요구

```text
요즘 A제품 불량률이 높다. 왜 그런지 시스템 3개를 열어보지 않고 한 화면에서 보고 싶다.
```

### 기술 태스크 분해

| # | 태스크 | 담당 영역 |
|---|---|---|
| 1 | MES `production_results`, `defects` 테이블 조회 API 구현 | Backend |
| 2 | PLM `eco`, `ecr` 조회 API 구현 (변경 시점·대상부품) | Backend |
| 3 | ERP `purchase_orders`, `suppliers` 조회 API 구현 (공급사 이력) | Backend |
| 4 | Product–Part–Process–Equipment–Defect 그래프 스키마 정의 | Knowledge Graph |
| 5 | LangGraph 원인분석 workflow 구현 (`quality_root_cause_analysis`) | Agent |
| 6 | Evidence 기반 응답 포맷 설계 (`source / record_id / description`) | API/UX |
| 7 | 사용자 권한별 데이터 마스킹 정책 정의 | Security |
| 8 | 응답 limitations 영역에 “synthetic data” 명시 정책 | Governance |

### 산출물

- `/chat` API: intent=`quality_root_cause_analysis`, used_sources, evidence
- Frontend: Evidence Panel, Trace Timeline

---

## Use Case 2. "PLM BOM과 실제 투입 부품이 다른 LOT를 찾아줘"

### 기술 태스크

1. PLM `bom` (revision, effective_from/to, approval_status) 조회 API
2. MES `lots`, `production_results`의 실제 투입 부품 조회 API
3. BOM 비교 알고리즘 (set diff + revision 일자 기준)
4. Graph Tool: Product → BOM ↔ Lot → Part 경로 비교
5. Response Agent: 영향받는 제품·LOT·리스크 요약
6. **HITL**: 결과를 기반으로 BOM 정정은 자동 실행하지 않고 “승인 요청” 메시지

---

## Use Case 3. "공급사 S-03이 들어간 제품과 최근 품질 이슈"

### 기술 태스크

1. ERP `suppliers`, `purchase_orders` 조회 API
2. PLM `parts ↔ products` 매핑 조회 API
3. MES `defects` 최근 N개월 조회 API
4. Neo4j: `(:Supplier)<-[:SUPPLIED_BY]-(:Part)<-[:HAS_PART]-(:Product)<-[:PRODUCED_PRODUCT]-(:Lot)-[:HAS_DEFECT]->(:Defect)` 경로 탐색
5. Response Agent: 제품별 리스크 요약 (불량률 변화 % 포함)

---

## Use Case 4. "최근 설계변경된 제품 중 불량률 증가한 제품"

### 기술 태스크

1. PLM `ecr` / `eco` 최근 N개월 조회 API
2. MES 변경 전후 불량률 비교 API (window 기반)
3. Neo4j: `(:Product)-[:CHANGED_BY]->(:EngineeringChange)` 그래프
4. Analysis: 변경일 ± window 불량률 비교, 후보 도출
5. Response: 결과는 “상관 후보”로 표현 (확정 아님)

---

## Use Case 5. "A제품의 BOM/재고/생산실적/불량률 통합 요약"

### 기술 태스크

1. PLM BOM 조회 API
2. ERP 재고/원가/수주 조회 API
3. MES 생산실적/불량률 조회 API
4. Graph Tool로 관계 요약
5. Report Tool로 structured summary 생성 (`bom_summary`, `inventory_summary`, `production_summary`, `quality_summary`)

---

## 변환 시 PL 체크포인트

- [ ] 어떤 시스템(ERP/PLM/MES)에 어떤 테이블/컬럼이 필요한가?
- [ ] DB 직접 접근인가, API 연동인가, 파일 배치인가?
- [ ] 기준정보(품목코드, BOM, LOT, 설비코드)가 시스템 간 일치하는가?
- [ ] 응답에 어떤 evidence를 포함해야 하는가?
- [ ] write 작업이 포함되는가? → HITL 처리 필요 여부
- [ ] 응답에 마스킹이 필요한 민감 데이터가 있는가?
- [ ] 성공 기준은 무엇인가? (정확도? 응답 시간? 사용자 만족?)
