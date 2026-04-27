# 01. Project Overview

## 1. 프로젝트 배경

제조업 고객사는 일반적으로 **ERP / PLM / MES**라는 3개의 핵심 시스템을 운영한다.

- **ERP** (Enterprise Resource Planning): 경영·구매·재고·원가·수주
- **PLM** (Product Lifecycle Management): 제품 설계·BOM·도면·설계변경(ECR/ECO)
- **MES** (Manufacturing Execution System): 생산실적·공정·설비·LOT·품질

세 시스템은 **벤더가 다르고**, **DB가 분리되어 있고**, **기준정보가 미세하게 다르다**.
현업은 “A제품의 BOM·재고·생산실적·불량률을 한 화면에서 보고 싶다”는 단순한 요구를 가지지만,
실제로는 시스템 3개를 열어가며 직접 연결지어야 한다.

## 2. 문제 정의

단순 LLM 챗봇으로는 다음 한계가 있다.

1. ERP/PLM/MES의 **관계**를 모른다. (예: BOM의 부품 → 어떤 LOT에 투입되었나?)
2. LLM이 **임의로 SQL을 만들어 실행**하는 것은 운영 시스템에 위험하다.
3. 답변에 **근거(evidence)**가 없으면 현업이 신뢰하지 않는다.
4. 설계변경 / 공급사 변경 같은 **시간축 인과관계**가 자연어만으로는 표현되지 않는다.

## 3. 왜 GraphRAG + Agentic AI 인가

- **GraphRAG**: 제품-부품-공정-설비-LOT-불량-설계변경의 관계를 Neo4j 지식 그래프로 표현하여, 관계 기반 질의를 자연스럽게 처리.
- **Agentic AI (LangGraph)**: 질문 의도에 따라 ERP / PLM / MES / Graph / SPARQL Tool을 선택 호출하는 Supervisor Agent.
- **Tool 분리**: LLM은 SQL을 직접 실행하지 않고, 안전성 검증(safety check)을 거친 read-only Tool을 통해 데이터 접근.
- **Evidence-based answer**: 모든 답변은 source, record_id, description을 포함.

## 4. 목표 기능 (MVP 범위)

- ERP/PLM/MES synthetic 데이터셋 구축 및 key 정합성 유지
- LangGraph Supervisor Agent + 5개 도메인 Agent Node + Tool
- Neo4j 지식 그래프 + 샘플 Cypher 질의
- RDF/OWL ontology + 샘플 SPARQL
- Gemini API 연동 LLM Provider + OpenAI-compatible 추상화
- React Chat UI, Evidence Panel, Trace Timeline
- 5개 대표 Use Case 처리

## 5. Non-Goals

- 실제 ERP/PLM/MES 벤더 연동
- 운영 수준 권한 시스템
- 자체 LLM 학습/파인튜닝
- 복잡한 대시보드 / 실시간 스트리밍 처리

## 6. 성공 기준

- README만 보고도 “제조업 ERP/PLM/MES AI Agent PL 역할이 가능한 사람”임을 전달할 수 있다.
- 5개 데모 질문 중 최소 3개가 evidence-based answer로 동작한다.
- LLM 호출부가 Agent와 분리되어 있어 Phase 2의 자체 오픈소스 LLM 교체가 “provider 1개 추가”로 가능하다.
