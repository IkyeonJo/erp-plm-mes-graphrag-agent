# 04. Agent Workflow

LangGraph 기반 Supervisor Agent의 State, Node, Routing, 실패 처리, HITL 정책.

---

## 1. AgentState

`backend/app/agents/state.py`

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

`evidence`는 누적되는 list로, 각 Tool이 자신의 결과를 `{source, record_id, description}` 형태로 push.

---

## 2. Node 구성

| Node | 책임 |
|---|---|
| `classify_intent` | 질문 → intent 분류 (`quality_root_cause_analysis`, `bom_mismatch`, `supplier_impact`, `eco_impact`, `product_summary`, `general`) |
| `route_sources` | intent → required_sources 결정 (예: ERP+PLM+MES+Neo4j) |
| `call_erp_agent` | SQL Tool로 ERP 조회 |
| `call_plm_agent` | SQL Tool로 PLM 조회 |
| `call_mes_agent` | SQL Tool로 MES 조회 |
| `call_graph_agent` | Neo4j Tool로 관계 탐색 |
| `call_sparql_agent` | SPARQL Tool로 ontology 조회 |
| `analyze_results` | 결과 통합, 가설/후보 도출 |
| `generate_response` | LLM Provider로 evidence 기반 답변 생성 |

## 3. Workflow Graph

```text
classify_intent
   ↓
route_sources
   ↓ (병렬 가능)
call_erp_agent ──┐
call_plm_agent ──┤
call_mes_agent ──┼──→ analyze_results ──→ generate_response
call_graph_agent─┤
call_sparql_agent┘
```

각 도메인 node는 `required_sources`에 자기 source가 없으면 즉시 pass-through.

## 4. Routing Logic

질문 키워드 또는 LLM 기반 분류. MVP는 키워드 우선 + fallback LLM.

| 키워드 | source |
|---|---|
| 재고, 구매, 원가, 공급사, 수주, 납기 | ERP |
| BOM, 도면, 설계변경, ECO, ECR, revision | PLM |
| 생산, LOT, 불량, 공정, 설비, 검사, 불량률 | MES |
| 관계, 영향, 연결, 추적, 원인, 경로 | Neo4j |
| 온톨로지, RDF, SPARQL | SPARQL |

복합 질문(예: "공급사 변경이 불량률에 미친 영향")은 ERP + MES + Neo4j 모두 호출.

## 5. Intent Definition

| intent | 설명 | required_sources 예시 |
|---|---|---|
| `quality_root_cause_analysis` | 품질 원인 분석 | MES, PLM, ERP, Neo4j |
| `bom_mismatch` | BOM 불일치 탐지 | PLM, MES, Neo4j |
| `supplier_impact` | 공급사 영향도 | ERP, PLM, MES, Neo4j |
| `eco_impact` | 설계변경 영향도 | PLM, MES, Neo4j |
| `product_summary` | 제품 통합 요약 | ERP, PLM, MES, Neo4j |
| `general` | 도메인 외 일반 질문 | (LLM only) |

## 6. 실패 처리

```text
- Tool 호출 실패 시 errors[]에 기록, 다른 Tool 결과는 살린다.
- LLM 실패 시 raw evidence는 반환, final_answer는 "응답 생성 중 오류" 메시지.
- intent 분류 실패 시 general 처리하되 limitations에 표시.
- SQL safety check 실패 시 즉시 차단, errors에 사유 기록.
- timeout: Tool당 5초 (MVP).
```

## 7. Human-in-the-loop (HITL) 정책

자동 실행하지 않는 작업:

```text
- ERP 데이터 수정 / PLM BOM 변경 / MES 작업지시 변경
- 승인 상태 변경 / 외부 메시지 발송 / 파일 삭제 / 운영 DB write
```

쓰기 요청 발생 시 응답:

```text
이 작업은 운영 시스템에 변경을 발생시킬 수 있으므로 Human-in-the-loop 승인이 필요합니다.
현재 PoC에서는 실행하지 않고, 제안된 작업 계획만 생성합니다.
```

응답에는 다음을 포함한다.

- `proposed_action`: 어떤 시스템에 어떤 변경이 필요한지
- `affected_records`: 영향받는 record_id 목록
- `approver_role`: 승인 가능한 역할 (예: 품질팀장, 생산팀장)
- `rollback_plan`: 변경 후 롤백 시 필요한 정보

## 8. Trace

각 응답은 다음 trace 정보를 포함할 수 있다.

```json
{
  "trace": [
    {"node": "classify_intent", "intent": "quality_root_cause_analysis", "ms": 320},
    {"node": "call_mes_agent", "tool": "sql", "rows": 12, "ms": 180},
    {"node": "call_graph_agent", "tool": "neo4j", "paths": 3, "ms": 240},
    {"node": "generate_response", "provider": "gemini", "ms": 1850}
  ]
}
```

이 trace는 Frontend의 `TraceTimeline` 컴포넌트가 시각화한다.
