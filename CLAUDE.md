# CLAUDE.md

이 문서는 Claude Code가 `erp-plm-mes-graphrag-agent` GitHub 포트폴리오 레포지토리에서 일관된 방식으로 작업하도록 하기 위한 프로젝트 지침서입니다.

본 프로젝트는 제조업 고객사의 ERP/PLM/MES 데이터를 통합 조회·분석하는 **GraphRAG + Agentic AI 챗봇 PoC**입니다. 실제 고객 데이터 없이 synthetic manufacturing dataset을 사용하되, 실무 제조업 AI 통합 프로젝트에 가까운 구조를 보여주는 것을 목표로 합니다.

---

## 1. Project Goal

이 레포지토리의 목적은 다음 포지션에 지원하기 위한 GitHub 포트폴리오를 만드는 것이다.

- 제조업 고객사의 AI 업무 통합 시스템 구축 프로젝트
- ERP/PLM/MES 데이터 통합 조회·분석 챗봇
- 지식 그래프 위에 Agentic AI 결합
- Phase 1: 챗봇 구축
- Phase 2: 자체 오픈소스 LLM 기반 Supervisor Agent 및 업무 자동화 확장
- 기술 스택: FastAPI, LangGraph, Neo4j, OWL/RDF, SPARQL, SQL, ERP/PLM/MES 연동

이 포트폴리오는 단순 LLM 챗봇이 아니라 다음 역량을 보여줘야 한다.

1. 제조업 ERP/PLM/MES 도메인 이해
2. BOM, LOT, 공정, 설비, 품질, 설계변경 데이터 모델링
3. FastAPI 기반 백엔드 설계
4. LangGraph 기반 Supervisor Agent 설계
5. Neo4j 기반 Knowledge Graph 구축
6. RDF/OWL/SPARQL 온톨로지 최소 구현
7. SQL Tool, Graph Tool, SPARQL Tool, RAG Tool의 독립 모듈화
8. Evidence-based answer 생성
9. PL 관점의 요구사항 → 기술 태스크 변환 문서화
10. 보안, 권한, 감사로그, Human-in-the-loop 설계

---

## 2. Repository Name

권장 레포지토리 이름:

```text
erp-plm-mes-graphrag-agent
```

프로젝트 한 줄 설명:

```text
A manufacturing GraphRAG + LangGraph Agent PoC for integrated ERP/PLM/MES data search, analysis, and evidence-based response generation.
```

한국어 설명:

```text
제조업 ERP/PLM/MES 데이터를 통합 조회·분석하기 위한 FastAPI + LangGraph + Neo4j 기반 GraphRAG Agent PoC
```

---

## 3. High-level Architecture

전체 구조는 다음과 같다.

```text
User
 ↓
React Chat UI
 ↓
FastAPI Backend
 ↓
LangGraph Supervisor Agent
 ├─ ERP SQL Tool
 ├─ PLM BOM Tool
 ├─ MES Production Tool
 ├─ Neo4j Graph Tool
 ├─ RDF/SPARQL Tool
 └─ Report Generator
 ↓
Evidence-based Answer
```

조금 더 상세한 구조:

```text
[User]
   ↓
[Frontend: React]
   ↓
[FastAPI Backend]
   ↓
[LangGraph Supervisor Agent]
   ├─ Intent Classifier Node
   ├─ Data Source Router Node
   ├─ ERP Agent Node
   ├─ PLM Agent Node
   ├─ MES Agent Node
   ├─ Knowledge Graph Agent Node
   ├─ SPARQL Agent Node
   ├─ Analysis Node
   └─ Response Generator Node
   ↓
[Tools]
   ├─ SQL Tool
   ├─ Neo4j Tool
   ├─ SPARQL Tool
   ├─ Document RAG Tool
   └─ Report Tool
   ↓
[Data Sources]
   ├─ ERP synthetic DB
   ├─ PLM synthetic DB
   ├─ MES synthetic DB
   ├─ Neo4j Knowledge Graph
   └─ RDF/OWL ontology
```

---

## 4. Recommended Repository Structure

기본 레포 구조는 다음을 따른다.

```text
erp-plm-mes-graphrag-agent/
 ├─ backend/
 │   ├─ app/
 │   │   ├─ main.py
 │   │   ├─ core/
 │   │   │   ├─ config.py
 │   │   │   └─ logging.py
 │   │   ├─ api/
 │   │   │   ├─ chat.py
 │   │   │   ├─ erp.py
 │   │   │   ├─ plm.py
 │   │   │   ├─ mes.py
 │   │   │   └─ graph.py
 │   │   ├─ agents/
 │   │   │   ├─ supervisor.py
 │   │   │   ├─ state.py
 │   │   │   ├─ intent_classifier.py
 │   │   │   ├─ erp_agent.py
 │   │   │   ├─ plm_agent.py
 │   │   │   ├─ mes_agent.py
 │   │   │   ├─ graph_agent.py
 │   │   │   ├─ sparql_agent.py
 │   │   │   └─ response_agent.py
 │   │   ├─ tools/
 │   │   │   ├─ sql_tool.py
 │   │   │   ├─ neo4j_tool.py
 │   │   │   ├─ sparql_tool.py
 │   │   │   ├─ rag_tool.py
 │   │   │   └─ report_tool.py
 │   │   ├─ llm/
 │   │   │   ├─ __init__.py
 │   │   │   ├─ base.py
 │   │   │   ├─ gemini_provider.py
 │   │   │   ├─ openai_compatible_provider.py
 │   │   │   └─ factory.py
 │   │   ├─ schemas/
 │   │   │   ├─ chat.py
 │   │   │   ├─ erp.py
 │   │   │   ├─ plm.py
 │   │   │   ├─ mes.py
 │   │   │   └─ graph.py
 │   │   ├─ services/
 │   │   │   ├─ erp_service.py
 │   │   │   ├─ plm_service.py
 │   │   │   ├─ mes_service.py
 │   │   │   └─ graph_service.py
 │   │   └─ db/
 │   │       ├─ session.py
 │   │       ├─ models.py
 │   │       └─ seed.py
 │   ├─ tests/
 │   ├─ pyproject.toml
 │   └─ Dockerfile
 │
 ├─ frontend/
 │   ├─ src/
 │   │   ├─ App.tsx
 │   │   ├─ pages/
 │   │   │   └─ ChatPage.tsx
 │   │   ├─ components/
 │   │   │   ├─ ChatWindow.tsx
 │   │   │   ├─ EvidencePanel.tsx
 │   │   │   ├─ GraphResultPanel.tsx
 │   │   │   ├─ SQLResultTable.tsx
 │   │   │   └─ TraceTimeline.tsx
 │   │   └─ lib/
 │   │       └─ api.ts
 │   ├─ package.json
 │   └─ Dockerfile
 │
 ├─ data/
 │   ├─ synthetic/
 │   │   ├─ erp/
 │   │   │   ├─ customers.csv
 │   │   │   ├─ suppliers.csv
 │   │   │   ├─ items.csv
 │   │   │   ├─ purchase_orders.csv
 │   │   │   ├─ sales_orders.csv
 │   │   │   ├─ inventory.csv
 │   │   │   └─ costs.csv
 │   │   ├─ plm/
 │   │   │   ├─ products.csv
 │   │   │   ├─ parts.csv
 │   │   │   ├─ bom.csv
 │   │   │   ├─ design_documents.csv
 │   │   │   ├─ ecr.csv
 │   │   │   └─ eco.csv
 │   │   └─ mes/
 │   │       ├─ work_orders.csv
 │   │       ├─ production_results.csv
 │   │       ├─ equipment.csv
 │   │       ├─ processes.csv
 │   │       ├─ quality_inspections.csv
 │   │       ├─ defects.csv
 │   │       └─ lots.csv
 │   └─ generate_synthetic_data.py
 │
 ├─ graph/
 │   ├─ cypher/
 │   │   ├─ 01_schema.cypher
 │   │   ├─ 02_constraints.cypher
 │   │   ├─ 03_load_data.cypher
 │   │   └─ 04_sample_queries.cypher
 │   └─ graph_schema.md
 │
 ├─ ontology/
 │   ├─ manufacturing.ttl
 │   ├─ sample_queries.sparql
 │   └─ ontology_notes.md
 │
 ├─ docs/
 │   ├─ 01_project_overview.md
 │   ├─ 02_requirements_to_tasks.md
 │   ├─ 03_system_architecture.md
 │   ├─ 04_agent_workflow.md
 │   ├─ 05_data_model_erp_plm_mes.md
 │   ├─ 06_knowledge_graph_schema.md
 │   ├─ 07_security_and_permission.md
 │   ├─ 08_phase_plan.md
 │   └─ 09_customer_meeting_checklist.md
 │
 ├─ docker-compose.yml
 ├─ .env.example
 ├─ README.md
 └─ CLAUDE.md
```

---

## 5. Domain Concepts

Claude Code는 구현 시 아래 제조업 도메인 개념을 기준으로 삼아야 한다.

### 5.1 ERP

ERP는 Enterprise Resource Planning의 약자이며, 제조기업의 경영·구매·재고·원가·수주·생산계획 데이터를 관리한다.

ERP synthetic data에는 다음 개념을 포함한다.

```text
Customer
Supplier
Item
PurchaseOrder
SalesOrder
Inventory
Cost
Warehouse
DeliveryDueDate
```

대표 질문:

```text
A제품의 현재 재고와 원가를 알려줘.
공급사 S-03이 납품한 부품 목록을 보여줘.
최근 3개월간 P-203 부품의 구매단가 추이를 알려줘.
납기 지연 위험이 있는 수주 건을 찾아줘.
```

### 5.2 PLM

PLM은 Product Lifecycle Management의 약자이며, 제품 설계·BOM·도면·사양서·설계변경 이력을 관리한다.

PLM synthetic data에는 다음 개념을 포함한다.

```text
Product
Part
BOM
DesignDocument
ECR
ECO
Revision
ApprovalStatus
```

대표 질문:

```text
A제품의 최신 BOM을 보여줘.
부품 P-203이 들어간 제품을 찾아줘.
최근 설계변경이 있었던 제품을 알려줘.
ECO-2026-014의 변경 내용과 영향 제품을 요약해줘.
```

### 5.3 MES

MES는 Manufacturing Execution System의 약자이며, 실제 공장 생산·공정·설비·품질·LOT 추적 데이터를 관리한다.

MES synthetic data에는 다음 개념을 포함한다.

```text
WorkOrder
ProductionResult
Process
Equipment
QualityInspection
Defect
Lot
Operator
Shift
```

대표 질문:

```text
A제품의 최근 3개월 불량률 추이를 알려줘.
LOT-L24041의 생산 이력을 추적해줘.
EQ-11 설비에서 발생한 주요 불량 유형을 알려줘.
PR-03 공정의 생산성과 불량률을 비교해줘.
```

---

## 6. Core Use Cases

이 프로젝트는 최소한 다음 질의를 처리해야 한다.

### Use Case 1: Product Quality Root Cause Analysis

질문:

```text
A제품의 최근 3개월 불량률이 상승한 원인을 분석해줘.
```

Agent 흐름:

```text
1. Supervisor Agent가 원인분석 질문으로 분류
2. MES Tool이 A제품의 월별 생산량, 불량 수량, 불량률 조회
3. Neo4j Tool이 A제품의 부품, 공정, 설비 관계 탐색
4. PLM Tool이 최근 설계변경 이력 조회
5. ERP Tool이 관련 부품의 공급사 및 입고 이력 조회
6. Analysis Agent가 원인 후보 생성
7. Response Agent가 evidence와 함께 답변 생성
```

예상 답변 스타일:

```text
A제품의 불량률은 2026년 2월 1.8%에서 2026년 4월 4.9%로 증가했습니다.
증가 구간은 LOT-L24041 이후이며, 해당 LOT부터 부품 P-203의 공급사가 S-02에서 S-07로 변경되었습니다.
PLM상 ECO-2026-014도 같은 기간 승인되었으나, 변경 대상은 외장 케이스로 품질 이슈와 직접 관련성은 낮아 보입니다.
MES 기준 불량은 Solder Crack 유형이 62%를 차지하며, PR-03 공정과 EQ-11 설비에서 집중 발생했습니다.
따라서 1차 원인 후보는 P-203 공급사 변경 또는 PR-03 공정 조건 변화입니다.
```

### Use Case 2: BOM Mismatch Detection

질문:

```text
PLM BOM과 MES 실제 투입 부품이 다른 LOT를 찾아줘.
```

Agent 흐름:

```text
1. PLM Tool이 설계 BOM 조회
2. ERP Tool이 기준 BOM 또는 품목 기준정보 조회
3. MES Tool이 실제 LOT 투입 부품 조회
4. Graph Tool이 제품-부품-LOT 관계 탐색
5. Analysis Agent가 불일치 항목 식별
6. Response Agent가 영향받는 제품, LOT, 리스크 요약
```

### Use Case 3: Supplier Impact Analysis

질문:

```text
공급사 S-03의 부품이 들어간 제품과 최근 품질 이슈를 요약해줘.
```

Agent 흐름:

```text
1. ERP Tool이 공급사 S-03의 납품 부품 조회
2. PLM Tool이 해당 부품이 포함된 제품/BOM 조회
3. MES Tool이 해당 제품의 최근 품질 이슈 조회
4. Neo4j Tool이 Supplier-Part-Product-Defect 경로 탐색
5. Response Agent가 제품별 리스크 요약
```

### Use Case 4: Engineering Change Impact Analysis

질문:

```text
최근 설계변경이 있었던 제품 중 불량률이 증가한 제품을 찾아줘.
```

Agent 흐름:

```text
1. PLM Tool이 최근 ECR/ECO 조회
2. MES Tool이 변경 전후 불량률 비교
3. Graph Tool이 변경 부품과 제품 관계 탐색
4. Analysis Agent가 설계변경과 품질 이슈의 상관 후보 생성
5. Response Agent가 evidence와 함께 답변
```

### Use Case 5: Integrated Product Summary

질문:

```text
A제품의 BOM, 재고, 생산실적, 불량률을 통합 요약해줘.
```

Agent 흐름:

```text
1. PLM Tool이 BOM 조회
2. ERP Tool이 재고/원가/수주 조회
3. MES Tool이 생산실적/불량률 조회
4. Graph Tool이 관계 요약
5. Response Agent가 통합 리포트 생성
```

---

## 7. Data Modeling Guidelines

### 7.1 ERP Tables

최소 테이블:

```text
customers
suppliers
items
purchase_orders
sales_orders
inventory
costs
```

권장 컬럼 예시:

```text
items:
- item_id
- item_name
- item_type
- unit
- standard_cost
- supplier_id

purchase_orders:
- po_id
- supplier_id
- item_id
- order_date
- delivery_date
- quantity
- unit_price
- status

inventory:
- inventory_id
- item_id
- warehouse_id
- quantity_on_hand
- safety_stock
- last_updated
```

### 7.2 PLM Tables

최소 테이블:

```text
products
parts
bom
design_documents
ecr
eco
```

권장 컬럼 예시:

```text
products:
- product_id
- product_name
- model_name
- revision
- lifecycle_status

bom:
- bom_id
- product_id
- parent_part_id
- child_part_id
- quantity
- revision
- effective_from
- effective_to
- approval_status

eco:
- eco_id
- product_id
- changed_part_id
- change_type
- reason
- approved_date
- effective_date
- status
```

### 7.3 MES Tables

최소 테이블:

```text
work_orders
production_results
equipment
processes
quality_inspections
defects
lots
```

권장 컬럼 예시:

```text
production_results:
- result_id
- work_order_id
- product_id
- lot_id
- process_id
- equipment_id
- production_date
- shift
- produced_qty
- defect_qty

defects:
- defect_id
- lot_id
- product_id
- process_id
- equipment_id
- defect_type
- defect_qty
- detected_at

lots:
- lot_id
- product_id
- work_order_id
- start_time
- end_time
- status
```

---

## 8. Knowledge Graph Guidelines

Neo4j에는 다음 노드와 관계를 구성한다.

### 8.1 Nodes

```text
Product
Part
BOM
Supplier
WorkOrder
Lot
Process
Equipment
Defect
EngineeringChange
Document
```

### 8.2 Relationships

```text
(:Product)-[:HAS_PART]->(:Part)
(:Part)-[:SUPPLIED_BY]->(:Supplier)
(:Product)-[:HAS_BOM]->(:BOM)
(:Product)-[:PRODUCED_IN]->(:Process)
(:Process)-[:USES]->(:Equipment)
(:Lot)-[:PRODUCED_PRODUCT]->(:Product)
(:Lot)-[:HAS_DEFECT]->(:Defect)
(:Product)-[:CHANGED_BY]->(:EngineeringChange)
(:Document)-[:DESCRIBES]->(:Product)
(:WorkOrder)-[:PRODUCES]->(:Product)
(:WorkOrder)-[:CREATES]->(:Lot)
```

### 8.3 Sample Cypher Queries

Claude Code는 `graph/cypher/04_sample_queries.cypher`에 다음 질의를 포함한다.

```cypher
// Find parts of a product
MATCH (p:Product {product_id: $product_id})-[:HAS_PART]->(part:Part)
RETURN p, part;

// Find products affected by a supplier
MATCH (s:Supplier {supplier_id: $supplier_id})<-[:SUPPLIED_BY]-(part:Part)<-[:HAS_PART]-(p:Product)
RETURN s, part, p;

// Find defects related to a product
MATCH (p:Product {product_id: $product_id})<-[:PRODUCED_PRODUCT]-(lot:Lot)-[:HAS_DEFECT]->(d:Defect)
RETURN p, lot, d;

// Find process and equipment path for a product
MATCH (p:Product {product_id: $product_id})-[:PRODUCED_IN]->(proc:Process)-[:USES]->(eq:Equipment)
RETURN p, proc, eq;
```

---

## 9. RDF / OWL / SPARQL Guidelines

공고에 OWL/RDF/SPARQL이 포함되어 있으므로 최소 온톨로지 샘플을 구현한다.

### 9.1 Ontology File

파일:

```text
ontology/manufacturing.ttl
```

포함 클래스:

```text
ManufacturingEntity
Product
Part
Supplier
Process
Equipment
Defect
EngineeringChange
Lot
```

포함 관계:

```text
hasPart
suppliedBy
producedIn
usesEquipment
hasDefect
changedBy
```

### 9.2 Sample SPARQL Queries

파일:

```text
ontology/sample_queries.sparql
```

포함 질의:

```sparql
# Find parts of a product
SELECT ?part WHERE {
  ?product a :Product .
  ?product :hasPart ?part .
}

# Find products using a specific part
SELECT ?product WHERE {
  ?product a :Product .
  ?product :hasPart ?part .
  ?part :partId "P-203" .
}

# Find defects related to a product
SELECT ?defect WHERE {
  ?lot :producedProduct ?product .
  ?lot :hasDefect ?defect .
}
```

---

## 10. LangGraph Agent Design

LangGraph는 다음 설계를 따른다.

### 10.1 Agent State

파일:

```text
backend/app/agents/state.py
```

상태에는 다음 필드를 포함한다.

```python
class AgentState(TypedDict):
    user_query: str
    intent: str
    required_sources: list[str]
    erp_result: dict | None
    plm_result: dict | None
    mes_result: dict | None
    graph_result: dict | None
    sparql_result: dict | None
    analysis_result: dict | None
    evidence: list[dict]
    final_answer: str | None
    errors: list[str]
```

### 10.2 Nodes

최소 노드:

```text
classify_intent
route_sources
call_erp_agent
call_plm_agent
call_mes_agent
call_graph_agent
call_sparql_agent
analyze_results
generate_response
```

### 10.3 Routing Logic

질문 키워드 기반 또는 LLM 기반 라우팅을 구현한다.

예시:

```text
재고, 구매, 원가, 공급사, 수주 → ERP
BOM, 도면, 설계변경, ECO, ECR, revision → PLM
생산, LOT, 불량, 공정, 설비, 검사 → MES
관계, 영향, 연결, 추적, 원인 → Neo4j Graph
온톨로지, RDF, SPARQL → SPARQL
```

### 10.4 Human-in-the-loop Policy

초기 PoC에서는 모든 작업을 읽기 전용으로 제한한다.

다음 작업은 자동 실행하지 않는다.

```text
ERP 데이터 수정
PLM BOM 변경
MES 작업지시 변경
승인 상태 변경
외부 메시지 발송
파일 삭제
운영 DB write
```

쓰기 작업이 필요한 경우에는 다음 응답을 생성한다.

```text
이 작업은 운영 시스템에 변경을 발생시킬 수 있으므로 Human-in-the-loop 승인이 필요합니다.
현재 PoC에서는 실행하지 않고, 제안된 작업 계획만 생성합니다.
```


---

## 11. LLM Provider Design

본 프로젝트는 Phase 1에서 Gemini API를 기본 LLM provider로 사용하고, Phase 2에서는 자체 오픈소스 LLM으로 교체 가능한 구조를 목표로 한다.

중요 원칙:

```text
LLM 호출 로직은 Agent 코드에 직접 작성하지 않는다.
반드시 backend/app/llm/ 하위 provider 모듈로 분리한다.
```

이 구조를 통해 초기에는 Gemini API를 사용하고, 이후에는 vLLM, Ollama, TGI, LM Studio, OpenAI-compatible endpoint 등으로 쉽게 교체할 수 있게 한다.

### 11.1 Recommended LLM Module Structure

권장 구조:

```text
backend/app/llm/
 ├─ __init__.py
 ├─ base.py
 ├─ gemini_provider.py
 ├─ openai_compatible_provider.py
 └─ factory.py
```

각 파일의 역할:

```text
base.py
- 모든 LLM provider가 따라야 하는 공통 interface 정의

gemini_provider.py
- Gemini API 호출 담당

openai_compatible_provider.py
- OpenAI-compatible API 형식의 로컬/오픈소스 LLM 호출 담당
- 예: vLLM, Ollama OpenAI-compatible endpoint, TGI, LM Studio 등

factory.py
- 환경변수 LLM_PROVIDER 값에 따라 provider 선택
```

### 11.2 Environment Variables

`.env.example`에는 다음 값을 반드시 포함한다.

```env
# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-pro

# Optional OpenAI-compatible provider
OPENAI_API_KEY=optional
OPENAI_MODEL=gpt-4o-mini

# Local / Open-source LLM serving
LOCAL_LLM_BASE_URL=http://localhost:8001/v1
LOCAL_LLM_API_KEY=not-needed-for-local
LOCAL_LLM_MODEL=qwen2.5-7b-instruct
```

`backend/app/core/config.py`에는 위 환경변수를 읽는 settings를 정의한다.

예시:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    LOCAL_LLM_BASE_URL: str = "http://localhost:8001/v1"
    LOCAL_LLM_API_KEY: str = "not-needed-for-local"
    LOCAL_LLM_MODEL: str = "qwen2.5-7b-instruct"

    class Config:
        env_file = ".env"


settings = Settings()
```

### 11.3 Base LLM Provider Interface

`backend/app/llm/base.py`에는 공통 인터페이스를 둔다.

```python
from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        pass
```

모든 Agent node는 특정 벤더 API를 직접 호출하지 않고, 반드시 이 interface를 통해 LLM을 호출한다.

### 11.4 Gemini Provider

`backend/app/llm/gemini_provider.py`에서 Gemini API 호출을 담당한다.

권장 패키지:

```bash
uv add google-generativeai
```

예시 구현:

```python
from typing import Any

import google.generativeai as genai

from app.core.config import settings
from app.llm.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        prompt = f'''
{system_prompt}

User:
{user_prompt}
'''.strip()

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

        return response.text or ""
```

주의:

```text
- Gemini API Key는 코드에 직접 쓰지 않는다.
- GEMINI_API_KEY는 .env에서만 읽는다.
- .env 파일은 절대 GitHub에 커밋하지 않는다.
```

### 11.5 OpenAI-compatible Provider

Phase 2에서 자체 오픈소스 LLM을 도입할 가능성을 보여주기 위해 OpenAI-compatible provider를 함께 준비한다.

`backend/app/llm/openai_compatible_provider.py` 예시:

```python
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.llm.base import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.LOCAL_LLM_API_KEY,
            base_url=settings.LOCAL_LLM_BASE_URL,
        )
        self.model = settings.LOCAL_LLM_MODEL

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""
```

권장 패키지:

```bash
uv add openai
```

이 provider는 다음과 같은 자체 LLM 서빙 구조와 연결할 수 있다.

```text
vLLM OpenAI-compatible server
Ollama OpenAI-compatible API
Text Generation Inference
LM Studio local server
사내 자체 LLM gateway
```

### 11.6 LLM Factory

`backend/app/llm/factory.py`에서 provider를 선택한다.

```python
from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_compatible_provider import OpenAICompatibleProvider


def get_llm_provider() -> BaseLLMProvider:
    if settings.LLM_PROVIDER == "gemini":
        return GeminiProvider()

    if settings.LLM_PROVIDER == "openai_compatible":
        return OpenAICompatibleProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
```

향후 확장 예시:

```text
LLM_PROVIDER=gemini
LLM_PROVIDER=openai_compatible
LLM_PROVIDER=local_vllm
LLM_PROVIDER=ollama
```

초기 구현에서는 `gemini`와 `openai_compatible`만 지원해도 충분하다.

### 11.7 LangGraph에서 LLM 사용 방식

LangGraph node는 Gemini API를 직접 호출하지 않는다. 반드시 `get_llm_provider()`를 통해 호출한다.

예시:

```python
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider


async def generate_response_node(state: AgentState) -> AgentState:
    llm = get_llm_provider()

    system_prompt = '''
You are a manufacturing AI assistant.

Rules:
- Answer only based on provided ERP, PLM, MES, Neo4j, and SPARQL evidence.
- Do not invent facts.
- If evidence is insufficient, clearly say so.
- Root cause analysis must be expressed as candidates, not confirmed facts.
- Include limitations and recommended next checks.
'''.strip()

    user_prompt = f'''
User question:
{state["user_query"]}

Intent:
{state["intent"]}

Evidence:
{state["evidence"]}

Analysis:
{state["analysis_result"]}
'''.strip()

    answer = await llm.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.2,
        max_tokens=2048,
    )

    state["final_answer"] = answer
    return state
```

### 11.8 LLM Usage Rules

Claude Code는 LLM 사용 시 아래 규칙을 반드시 지킨다.

```text
1. LLM API Key는 코드에 직접 쓰지 않는다.
2. Gemini API 호출은 llm provider 모듈에만 위치시킨다.
3. Agent node 내부에서 특정 벤더 API를 직접 호출하지 않는다.
4. Phase 2의 오픈소스 LLM 교체를 고려해 OpenAI-compatible provider도 준비한다.
5. 모든 LLM 응답은 evidence 기반이어야 한다.
6. LLM은 SQL을 직접 실행하지 않는다. SQL Tool이 safety check 후 실행한다.
7. LLM이 생성한 원인 분석은 확정이 아니라 후보로 표현한다.
8. timeout, retry, fallback provider 구조를 추후 확장 가능하게 둔다.
9. 운영 DB write 작업을 LLM에게 직접 맡기지 않는다.
10. LLM output은 사용자에게 보여주기 전 source/evidence/limitation 구조를 갖춰야 한다.
```

### 11.9 Prompt Template Guidelines

LLM prompt는 다음 구조를 따른다.

```text
System Prompt:
- 역할
- 답변 규칙
- 금지사항
- evidence 기반 답변 원칙

User Prompt:
- 사용자 질문
- 분류된 intent
- 사용된 source
- ERP/PLM/MES/Graph/SPARQL evidence
- analysis result
- 원하는 output format
```

Response Agent의 출력은 가능하면 다음 JSON-like 구조를 따른다.

```json
{
  "summary": "핵심 답변",
  "findings": [],
  "root_cause_candidates": [],
  "evidence": [],
  "limitations": [],
  "recommended_next_checks": []
}
```

### 11.10 Error Handling and Fallback

초기 MVP에서는 단순 예외 처리를 구현한다.

권장 정책:

```text
- LLM API 호출 실패 시 명확한 에러 메시지 반환
- API Key 누락 시 서버 시작 또는 첫 호출 시 알기 쉬운 메시지 출력
- timeout/retry는 TODO로 표시하거나 간단 구현
- LLM 실패 시 raw ERP/PLM/MES 조회 결과는 반환 가능
```

예시 사용자 응답:

```text
LLM 응답 생성 중 오류가 발생했습니다. 다만 ERP/PLM/MES 조회 결과는 아래와 같습니다.
```

### 11.11 Dependency Update

`backend/pyproject.toml`에는 다음 의존성을 포함한다.

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
langgraph
langchain
neo4j
rdflib
python-dotenv
google-generativeai
openai
```

개발 의존성:

```text
pytest
ruff
mypy
```

### 11.12 Portfolio Message

README와 docs에는 다음 메시지를 포함한다.

```text
LLM 호출부를 LangGraph Agent와 분리하여,
초기에는 Gemini API를 사용하고,
향후에는 vLLM/Ollama/TGI 기반 오픈소스 LLM으로 쉽게 교체할 수 있게 설계했습니다.
```

이는 공고의 “Gemini API 1차 → 자체 오픈소스 LLM 2차” 로드맵과 직접 연결되는 포트폴리오 포인트다.


---

## 12. Tool Design Rules

모든 Tool은 독립적인 모듈로 설계한다.

### 11.1 SQL Tool

파일:

```text
backend/app/tools/sql_tool.py
```

역할:

```text
ERP/PLM/MES synthetic SQL DB에 대해 read-only query 실행
```

규칙:

```text
- SELECT만 허용
- INSERT/UPDATE/DELETE/DROP/ALTER 금지
- 쿼리 실행 전 SQL safety check
- 결과는 dict/list 형태로 반환
- 모든 결과에는 source metadata 포함
```

### 11.2 Neo4j Tool

파일:

```text
backend/app/tools/neo4j_tool.py
```

역할:

```text
제품-부품-공정-설비-불량 관계 탐색
```

규칙:

```text
- MATCH/RETURN 중심
- DELETE/SET/MERGE/CREATE는 seed/load 단계 외 금지
- 반환 결과에 graph_path 포함
```

### 11.3 SPARQL Tool

파일:

```text
backend/app/tools/sparql_tool.py
```

역할:

```text
RDF 온톨로지 기반 조회
```

규칙:

```text
- SELECT 쿼리 중심
- ontology/manufacturing.ttl 로드
- 결과는 JSON serializable 구조로 반환
```

### 11.4 RAG Tool

파일:

```text
backend/app/tools/rag_tool.py
```

역할:

```text
사양서, 설계문서, 품질문서 등 비정형 문서 검색
```

초기 MVP에서는 간단한 keyword search 또는 local vector search로 구현해도 된다.

### 11.5 Report Tool

파일:

```text
backend/app/tools/report_tool.py
```

역할:

```text
Agent 결과를 structured report로 변환
```

출력 구조:

```json
{
  "summary": "...",
  "findings": [],
  "root_cause_candidates": [],
  "evidence": [],
  "recommended_actions": [],
  "limitations": []
}
```

---

## 13. Evidence-based Answer Rules

모든 Agent 응답은 반드시 evidence를 포함해야 한다.

응답 구조:

```json
{
  "answer": "최종 자연어 답변",
  "evidence": [
    {
      "source": "MES.production_results",
      "record_id": "RESULT-001",
      "description": "2026-04 A제품 불량률 4.9%"
    },
    {
      "source": "PLM.eco",
      "record_id": "ECO-2026-014",
      "description": "외장 케이스 변경 승인"
    }
  ],
  "limitations": [
    "Synthetic dataset 기반 분석이므로 실제 운영 데이터와 다를 수 있음"
  ]
}
```

응답 원칙:

```text
- 근거 없는 단정 금지
- 원인 분석은 “후보”로 표현
- 데이터 출처 명시
- 불확실성 명시
- Synthetic data임을 명확히 표시
```

---

## 14. FastAPI API Design

최소 API:

```text
POST /chat
GET /products/{product_id}/summary
GET /products/{product_id}/bom
GET /lots/{lot_id}/trace
GET /quality/defects/top
GET /graph/product/{product_id}
GET /health
```

### 14.1 POST /chat

Request:

```json
{
  "message": "A제품의 최근 3개월 불량률이 상승한 원인을 분석해줘."
}
```

Response:

```json
{
  "answer": "...",
  "intent": "quality_root_cause_analysis",
  "used_sources": ["MES", "PLM", "ERP", "Neo4j"],
  "evidence": [],
  "trace": []
}
```

### 14.2 GET /products/{product_id}/summary

제품 통합 요약:

```json
{
  "product_id": "PROD-A",
  "bom_summary": {},
  "inventory_summary": {},
  "production_summary": {},
  "quality_summary": {}
}
```

---

## 15. Frontend Guidelines

프론트엔드는 과하게 만들지 않는다. 이 프로젝트의 핵심은 백엔드, Agent, GraphRAG, 문서화이다.

최소 화면:

```text
ChatPage
 ├─ ChatWindow
 ├─ EvidencePanel
 ├─ SQLResultTable
 ├─ GraphResultPanel
 └─ TraceTimeline
```

UI 요구사항:

```text
- 사용자가 질문 입력
- AI 답변 표시
- 사용된 데이터 소스 표시
- Evidence 표시
- Agent trace 표시
- Graph 결과는 간단한 텍스트 또는 네트워크 시각화
```

프론트엔드 스택:

```text
React
TypeScript
Vite
Tailwind CSS
```

---

## 16. Documentation Requirements

이 프로젝트는 PL 포트폴리오이므로 코드만큼 문서가 중요하다.

### 16.1 docs/01_project_overview.md

포함 내용:

```text
- 프로젝트 배경
- 제조업 ERP/PLM/MES 데이터 통합 문제
- 왜 GraphRAG와 Agentic AI가 필요한지
- 목표 기능
- MVP 범위
```

### 16.2 docs/02_requirements_to_tasks.md

고객 요구를 기술 태스크로 변환하는 예시를 포함한다.

예시:

```text
현업 요구:
“A제품 불량 원인을 한 번에 보고 싶다.”

기술 태스크:
1. MES production_results, defects 테이블 조회 API 구현
2. PLM engineering_change_orders 조회 API 구현
3. ERP purchase_orders, suppliers 조회 API 구현
4. Product-Part-Process-Equipment 그래프 스키마 정의
5. LangGraph 원인분석 workflow 구현
6. Evidence 기반 응답 포맷 설계
7. 사용자 권한별 데이터 마스킹 정책 정의
```

### 16.3 docs/03_system_architecture.md

포함 내용:

```text
- 전체 아키텍처
- 데이터 흐름
- Agent 호출 흐름
- Tool 구조
- 시스템 경계
```

### 16.4 docs/04_agent_workflow.md

포함 내용:

```text
- LangGraph State 정의
- Node 정의
- Routing 기준
- 실패 처리
- Human-in-the-loop 정책
```

### 16.5 docs/05_data_model_erp_plm_mes.md

포함 내용:

```text
- ERP 테이블
- PLM 테이블
- MES 테이블
- 주요 키 매핑
- Product ID, Part ID, Lot ID, Equipment ID 등 기준정보
```

### 16.6 docs/06_knowledge_graph_schema.md

포함 내용:

```text
- Neo4j 노드
- 관계
- Cypher 예시
- GraphRAG 활용 방식
```

### 16.7 docs/07_security_and_permission.md

포함 내용:

```text
- 읽기 전용 원칙
- DB 권한
- 민감 데이터 마스킹
- Agent 실행 로그
- 승인 기반 자동화
- 운영망/개발망 분리 가정
```

### 16.8 docs/08_phase_plan.md

포함 내용:

```text
Phase 1: 0~6개월 챗봇 구축
Phase 2: 7~12개월 Agent 기능 확장 및 자체 LLM 통합
Phase 3: 업무 자동화 및 운영 고도화
```

이 포트폴리오에서는 실제 구현 범위를 MVP로 제한하되, Phase Plan은 실무 프로젝트 관점으로 작성한다.

### 16.9 docs/09_customer_meeting_checklist.md

참여 전 고객에게 확인해야 할 질문을 정리한다.

필수 질문:

```text
1. ERP/PLM/MES는 각각 어떤 벤더 또는 자체 시스템인가?
2. DB 직접 접근인가, API 연동인가, 파일/배치 연동인가?
3. 데이터 사전, ERD, API 명세서가 있는가?
4. 품목코드, BOM, LOT, 설비코드의 기준정보가 일치하는가?
5. Phase 1의 성공 기준은 무엇인가?
6. OpenClaw의 정확한 역할은 무엇인가?
7. Agent가 운영 시스템에 write 작업을 수행하는가?
8. 사용자 권한과 데이터 마스킹 정책은 어떻게 되는가?
9. 자체 오픈소스 LLM은 어떤 서빙 구조로 운영할 예정인가?
10. PL의 책임 범위는 일정/요구사항 관리인지, 아키텍처 의사결정까지인지?
```

---

## 17. Security and Governance Rules

제조업 내부 시스템에 AI Agent를 연결하는 프로젝트이므로 보안 설계를 강조한다.

초기 MVP 보안 원칙:

```text
1. 모든 데이터는 synthetic data 사용
2. 모든 Tool은 read-only 기본값
3. SQL safety check 필수
4. 운영 시스템 write 작업 금지
5. 민감 데이터는 마스킹
6. Agent trace와 tool call log 저장
7. Human-in-the-loop 승인 정책 문서화
8. .env 파일 커밋 금지
9. API Key는 .env.example에만 placeholder로 제공
10. Docker compose는 로컬 개발용으로 제한
```

Agent 자동화 단계에서의 위험:

```text
- 잘못된 SQL 실행
- 권한 없는 데이터 조회
- 오래된 BOM 또는 승인 전 도면 기준 답변
- 생산 현장 데이터 오해석
- 원인 분석의 과도한 단정
- 운영 시스템에 잘못된 write
```

응답 정책:

```text
- 불확실한 분석은 “가능성”, “후보”, “추정”으로 표현
- 운영 의사결정 전 사람 검토 필요 문구 포함
- 데이터 기준일과 출처 표시
```

---

## 18. Coding Style

### 18.1 Python

기본 원칙:

```text
- Python 3.11+
- 타입 힌트 사용
- Pydantic 모델 사용
- FastAPI dependency injection 사용
- 함수는 작게 유지
- Tool은 독립 모듈로 유지
- Agent 로직과 Tool 로직 분리
- 테스트 가능한 구조
```

선호 패키지 관리:

```text
uv 사용 권장
```

예시 명령:

```bash
uv init
uv add fastapi uvicorn pydantic sqlalchemy langgraph langchain neo4j rdflib python-dotenv
uv add --dev pytest ruff mypy
```

### 18.2 TypeScript / React

기본 원칙:

```text
- React + TypeScript + Vite
- 컴포넌트는 작게 유지
- API 호출은 src/lib/api.ts에 분리
- UI는 Tailwind CSS
- 포트폴리오이므로 과도한 디자인보다 명확한 정보 표시 우선
```

### 18.3 Formatting

Python:

```bash
ruff check .
ruff format .
```

TypeScript:

```bash
npm run lint
npm run format
```

---

## 19. Docker Compose

`docker-compose.yml`에는 최소 다음 서비스를 포함한다.

```text
backend
frontend
neo4j
```

선택:

```text
postgres
redis
```

초기 MVP에서는 SQLite를 사용할 수 있다. 다만 포트폴리오 완성도를 위해 Docker Compose에는 Neo4j를 포함한다.

예상 실행 명령:

```bash
cp .env.example .env
docker compose up --build
```

예상 접속 URL:

```text
Frontend: http://localhost:5173
Backend API Docs: http://localhost:8000/docs
Neo4j Browser: http://localhost:7474
```

---

## 20. README Requirements

README는 채용 담당자 또는 실무진이 1분 안에 프로젝트를 이해할 수 있어야 한다.

필수 섹션:

```text
1. Project Summary
2. Why This Project
3. Architecture
4. Features
5. Demo Questions
6. Tech Stack
7. Repository Structure
8. How to Run
9. Example Responses
10. PL Documentation
11. Security Design
12. Roadmap
```

README 첫 문단 예시:

```markdown
# ERP/PLM/MES GraphRAG Agent

This project is a manufacturing AI Agent PoC that integrates synthetic ERP, PLM, and MES data using FastAPI, LangGraph, Neo4j, and RDF/SPARQL. It demonstrates how a Supervisor Agent can route user questions to SQL tools, graph tools, and ontology tools to generate evidence-based answers for manufacturing operations.
```

한국어 설명도 같이 포함한다.

```markdown
본 프로젝트는 제조업 ERP/PLM/MES 데이터를 통합 조회·분석하기 위한 GraphRAG + Agentic AI 챗봇 PoC입니다. 제품, 부품, BOM, 공정, 설비, LOT, 불량, 설계변경 간 관계를 지식 그래프로 모델링하고, LangGraph Supervisor Agent가 사용자 질문에 따라 ERP/PLM/MES/Neo4j/SPARQL Tool을 선택 호출합니다.
```

---

## 21. Implementation Priority

Claude Code는 아래 순서로 작업한다.

### Phase A: Skeleton

```text
1. 레포 기본 폴더 생성
2. README.md 초안 작성
3. docs/ 문서 초안 생성
4. backend FastAPI skeleton 생성
5. frontend React skeleton 생성
6. docker-compose.yml 생성
```

### Phase B: Synthetic Data

```text
1. data/generate_synthetic_data.py 작성
2. ERP CSV 생성
3. PLM CSV 생성
4. MES CSV 생성
5. 데이터 간 key 정합성 유지
```

중요한 key:

```text
product_id
part_id
supplier_id
lot_id
process_id
equipment_id
work_order_id
eco_id
```

### Phase C: Backend APIs

```text
1. ERP 조회 API
2. PLM BOM 조회 API
3. MES 생산/품질 조회 API
4. Product summary API
5. Lot trace API
```

### Phase D: Knowledge Graph

```text
1. Neo4j schema 작성
2. constraints 작성
3. CSV load 또는 Python loader 작성
4. sample Cypher query 작성
5. Graph Tool 구현
```

### Phase E: Ontology

```text
1. manufacturing.ttl 작성
2. sample SPARQL 작성
3. RDFLib 기반 SPARQL Tool 구현
```

### Phase F: LLM Provider and LangGraph Agent

```text
1. LLM provider interface 정의
2. GeminiProvider 구현
3. OpenAI-compatible Provider 구현
4. LLM Factory 구현
5. AgentState 정의
6. Intent classifier 구현
7. Source router 구현
8. ERP/PLM/MES/Graph/SPARQL agent node 구현
9. Analysis node 구현
10. Response generator에서 LLM provider 호출
11. /chat API와 연결
```

### Phase G: Frontend

```text
1. Chat UI
2. Evidence Panel
3. Trace Timeline
4. Graph Result Panel
```

### Phase H: Polish

```text
1. README 보강
2. 데모 질문 추가
3. Example response 추가
4. 보안 문서 보강
5. 테스트 추가
6. 실행 스크린샷 또는 GIF 추가
```

---

## 22. Non-goals

이 포트폴리오에서 하지 않아도 되는 것:

```text
- 실제 ERP/PLM/MES 벤더 연동
- 실제 제조기업 데이터 사용
- 완전한 PLM/MES 구현
- 운영 수준의 권한 시스템
- 자체 LLM 학습/파인튜닝
- OpenClaw 실제 통합
- 복잡한 프론트엔드 대시보드
- 실시간 스트리밍 생산 데이터 처리
```

다만 문서에서는 향후 확장 방향으로 다음을 언급할 수 있다.

```text
- OpenClaw 기반 상주형 Agent Runtime
- vLLM/Ollama 기반 오픈소스 LLM 서빙
- 스케줄 기반 이상 감지
- Slack/Teams 알림
- Human approval workflow
- Airflow/Prefect 기반 배치 파이프라인
```

---

## 23. OpenClaw Positioning

공고에 OpenClaw가 있으므로 README나 docs에서 다음처럼 설명한다.

```text
본 MVP에서는 OpenClaw를 직접 통합하지 않지만, 향후 Phase 2에서 LangGraph workflow를 장기 실행 Agent Runtime에 연결하는 구조를 가정한다.
OpenClaw는 Supervisor Agent가 24시간 상주하며 ERP/PLM/MES/Knowledge Graph/문서/메신저 도구를 호출하는 실행 계층으로 활용될 수 있다.
```

예상 구조:

```text
FastAPI
 ↓
LangGraph Workflow
 ↓
OpenClaw Runtime / Supervisor Agent
 ├─ ERP Tool
 ├─ PLM Tool
 ├─ MES Tool
 ├─ Neo4j Tool
 ├─ SPARQL Tool
 ├─ Report Tool
 └─ Notification Tool
```

보안 강조:

```text
- OpenClaw류 runtime은 강력하지만 위험할 수 있으므로 read-only, least privilege, audit log, HITL 승인이 필요하다.
```

---

## 24. Interview Positioning

이 포트폴리오는 면접에서 다음 메시지를 전달하기 위한 것이다.

```text
저는 단순히 LLM API를 호출하는 개발자가 아니라,
제조업 ERP/PLM/MES 데이터가 어떻게 나뉘어 있고,
BOM, LOT, 공정, 설비, 불량, 설계변경이 어떻게 연결되는지 이해하며,
이를 FastAPI, LangGraph, Neo4j, RDF/SPARQL 기반으로 통합하는 Agentic AI 구조를 설계할 수 있습니다.

또한 PL 포지션에 맞게 고객 요구사항을 기술 태스크로 변환하고,
일정, 범위, 보안, Human-in-the-loop 정책까지 문서화할 수 있습니다.
```

지원서에 사용할 수 있는 소개 문구:

```text
제조업 ERP/PLM/MES 데이터를 가상으로 구성하고, FastAPI + LangGraph + Neo4j 기반으로 통합 조회·분석하는 GraphRAG Agent PoC를 구현했습니다.
제품-BOM-부품-공정-설비-불량 간 관계를 지식 그래프로 모델링하고, Supervisor Agent가 사용자 질문에 따라 SQL Tool, Graph Tool, SPARQL Tool을 선택 호출하도록 설계했습니다.
또한 고객 요구사항을 기술 태스크로 변환하는 PL 관점의 문서, Phase Plan, 권한/보안/Human-in-the-loop 설계 문서를 함께 포함했습니다.
```

---

## 25. Quality Checklist

작업 완료 전 아래를 확인한다.

### Code

```text
- FastAPI 서버가 실행되는가?
- /docs Swagger가 열리는가?
- /chat API가 동작하는가?
- synthetic data가 생성되는가?
- ERP/PLM/MES API가 최소 1개 이상씩 동작하는가?
- Neo4j graph load가 가능한가?
- SPARQL sample query가 실행되는가?
- LangGraph Agent가 최소 3개 이상의 demo question을 처리하는가?
```

### Documentation

```text
- README가 1분 안에 프로젝트 목적을 설명하는가?
- 아키텍처 다이어그램이 있는가?
- ERP/PLM/MES 데이터 모델이 설명되어 있는가?
- Agent workflow가 설명되어 있는가?
- 보안/권한/HITL 정책이 있는가?
- 고객 미팅 체크리스트가 있는가?
```

### Portfolio Appeal

```text
- 제조업 도메인 이해가 드러나는가?
- PL 역할 수행 가능성이 드러나는가?
- Agentic AI 구조가 드러나는가?
- GraphRAG와 지식 그래프 역량이 드러나는가?
- 실행 가능한 데모가 있는가?
```

---

## 26. Claude Code Working Rules

Claude Code는 작업 시 다음 규칙을 따른다.

```text
1. 먼저 전체 파일 구조를 만든다.
2. 작은 단위로 구현하고 실행 가능성을 확인한다.
3. 임의로 범위를 키우지 않는다.
4. 복잡한 기능보다 포트폴리오 메시지 전달을 우선한다.
5. 모든 주요 기능은 README와 docs에 설명한다.
6. Agent 응답에는 evidence를 포함한다.
7. 운영 시스템 write 작업은 구현하지 않는다.
8. 실제 기업 데이터처럼 보이는 민감 데이터는 만들지 않는다.
9. synthetic data임을 명확히 표시한다.
10. PL 관점의 문서화를 코드와 동등하게 중요하게 취급한다.
```

---

## 27. Suggested First Prompt for Claude Code

Claude Code에서 처음 실행할 프롬프트 예시:

```text
이 CLAUDE.md를 기준으로 `erp-plm-mes-graphrag-agent` 레포지토리의 초기 스캐폴딩을 생성해줘.

우선 다음을 만들어줘:
1. README.md 초안
2. docs/ 하위 9개 문서 초안
3. backend FastAPI skeleton
4. frontend React + Vite skeleton
5. backend/app/llm/ provider 구조
6. data/generate_synthetic_data.py 초안
7. graph/cypher/ 기본 cypher 파일
8. ontology/manufacturing.ttl 및 sample_queries.sparql
9. docker-compose.yml
10. .env.example

아직 복잡한 기능 구현보다, 실행 가능한 최소 구조와 포트폴리오 메시지가 잘 드러나는 문서화를 우선해줘.
```

---

## 28. Final Success Definition

이 프로젝트가 성공적으로 완성되었다는 기준은 다음과 같다.

```text
GitHub 방문자가 README만 보고도
“이 사람은 제조업 ERP/PLM/MES 통합 AI Agent 프로젝트의 PL 역할을 맡을 수 있겠다”
라고 느낄 수 있어야 한다.

실무진이 코드를 보면
“FastAPI, LangGraph, Neo4j, RDF/SPARQL, SQL Tool 구조를 최소한으로 구현해봤다”
라고 판단할 수 있어야 한다.

면접관이 docs를 보면
“고객 요구사항을 기술 태스크로 분해하고, 보안과 운영 리스크를 고려할 줄 안다”
라고 느낄 수 있어야 한다.
```
