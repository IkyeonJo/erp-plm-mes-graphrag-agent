# 03. System Architecture

## 1. 전체 아키텍처

```text
┌──────────────────────────────────────────────────────────┐
│                          User                            │
└────────────────────────────┬─────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────┐
│  Frontend (React + Vite + TypeScript + Tailwind)         │
│   ChatPage                                               │
│    ├─ ChatWindow                                         │
│    ├─ EvidencePanel                                      │
│    ├─ SQLResultTable                                     │
│    ├─ GraphResultPanel                                   │
│    └─ TraceTimeline                                      │
└────────────────────────────┬─────────────────────────────┘
                             ↓ POST /chat
┌──────────────────────────────────────────────────────────┐
│  FastAPI Backend (Python 3.11+)                          │
│   /chat, /products, /lots, /quality, /graph, /health     │
└────────────────────────────┬─────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────┐
│  LangGraph Supervisor Agent                              │
│   classify_intent → route_sources                        │
│   ├─ call_erp_agent     →  SQL Tool (ERP)                │
│   ├─ call_plm_agent     →  SQL Tool (PLM)                │
│   ├─ call_mes_agent     →  SQL Tool (MES)                │
│   ├─ call_graph_agent   →  Neo4j Tool                    │
│   ├─ call_sparql_agent  →  SPARQL Tool                   │
│   ↓                                                      │
│   analyze_results → generate_response                    │
└────────────────────────────┬─────────────────────────────┘
                             ↓
┌──────────────────────────────────────────────────────────┐
│  LLM Provider Layer (vendor-agnostic interface)          │
│   factory.get_llm_provider()                             │
│    ├─ GeminiProvider (Phase 1)                           │
│    └─ OpenAICompatibleProvider                           │
│         (Phase 2: vLLM / Ollama / TGI / LM Studio)       │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  Data Sources                                            │
│   ├─ SQLite (synthetic ERP / PLM / MES)                  │
│   ├─ Neo4j Knowledge Graph                               │
│   └─ RDF/OWL ontology (manufacturing.ttl)                │
└──────────────────────────────────────────────────────────┘
```

## 2. 데이터 흐름

1. 사용자가 React Chat UI에서 질문 입력
2. Frontend → `POST /chat` 호출
3. FastAPI가 LangGraph workflow 실행
4. `classify_intent`가 5개 intent 중 하나로 분류
5. `route_sources`가 호출할 source를 결정 (ERP/PLM/MES/Graph/SPARQL)
6. 각 도메인 Agent Node가 Tool을 통해 read-only 조회
7. `analyze_results`가 Tool 결과를 통합, 후보 가설 정리
8. `generate_response`가 LLM Provider를 통해 evidence 포함 자연어 답변 생성
9. Frontend가 answer / evidence / used_sources / trace를 UI에 렌더링

## 3. 시스템 경계

| 경계 | 본 PoC | 실제 운영 시 |
|---|---|---|
| 데이터 | synthetic CSV → SQLite | 고객 ERP/PLM/MES DB / API |
| Graph | 로컬 Neo4j (Docker) | 사내 Neo4j 클러스터 |
| LLM | Gemini API (외부) | 자체 vLLM / Ollama / 사내 gateway |
| 권한 | 단일 사용자 가정 | RBAC + 마스킹 + audit |
| Write | 모두 차단 | HITL 승인 후만 허용 |

## 4. 비기능 요구사항 (PoC 기준)

- **응답 시간**: 단일 질문 기준 5초 이하 (LLM 응답 포함)
- **재현성**: synthetic data는 시드 고정으로 재생성 가능해야 함
- **로그**: Agent trace, tool call log를 응답에 포함하거나 `/logs` endpoint 제공 가능
- **에러 처리**: LLM 실패 시 raw Tool 결과는 반환 가능, evidence는 손실되지 않음

## 5. 디렉터리별 책임

| 경로 | 책임 |
|---|---|
| `backend/app/api/` | FastAPI router (얇은 엔드포인트) |
| `backend/app/agents/` | LangGraph node, supervisor, state |
| `backend/app/tools/` | SQL/Neo4j/SPARQL/RAG/Report — vendor 호출 |
| `backend/app/llm/` | LLM provider 추상화 (벤더 격리) |
| `backend/app/services/` | 도메인 서비스 (ERP/PLM/MES) |
| `backend/app/db/` | SQLAlchemy session, models, seed |
| `data/` | synthetic data + generator |
| `graph/cypher/` | Neo4j schema/constraints/load/queries |
| `ontology/` | OWL/RDF + SPARQL |
| `docs/` | PL 관점 산출물 |

## 6. 확장 포인트

- **OpenClaw Runtime** (Phase 2): LangGraph workflow를 24시간 상주 Agent Runtime에 연결
- **알림 채널**: Slack / Teams 알림용 Notification Tool
- **배치 파이프라인**: Airflow / Prefect로 야간 배치 분석
- **이상 감지**: 스케줄 기반 Agent (불량률 임계 초과 자동 알림 + HITL)
