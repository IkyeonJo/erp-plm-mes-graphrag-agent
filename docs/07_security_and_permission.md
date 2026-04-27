# 07. Security and Permission

제조업 내부 시스템에 AI Agent를 연결하는 프로젝트이므로, 보안 설계를 운영 수준 기준으로 사전 정리한다.

본 PoC는 synthetic data 기반이지만, **실제 고객사 도입 시 어떤 통제가 필요한가**를 PL 관점에서 제시한다.

---

## 1. 기본 원칙

1. 모든 데이터는 synthetic data 사용 (실 데이터 절대 금지)
2. 모든 Tool은 read-only 기본값
3. SQL safety check (SELECT 외 차단)
4. 운영 시스템 write 작업 자동 실행 금지
5. 민감 데이터 마스킹 정책 사전 정의
6. Agent trace, tool call log 저장
7. Human-in-the-loop 승인 정책 문서화
8. `.env` 파일 커밋 금지, API Key는 `.env.example`에만 placeholder
9. Docker Compose는 로컬 개발용으로 제한
10. 운영망 / 개발망 분리 가정

## 2. SQL Safety Check

`backend/app/tools/sql_tool.py` 에서 다음 단계로 검증.

```text
1. 입력 SQL에서 주석 제거 후 정규화
2. 첫 statement만 허용 (멀티 쿼리 차단)
3. SELECT 또는 WITH ... SELECT 만 허용
4. INSERT / UPDATE / DELETE / DROP / ALTER / TRUNCATE / GRANT / REVOKE 차단
5. PRAGMA / ATTACH 차단
6. 파라미터 바인딩 강제 (string concat 금지)
7. row 수 LIMIT 권장 (default 1000)
```

차단 시 `errors[]`에 사유 기록하고 사용자에게는 “안전상 차단되었습니다” 안내.

## 3. Neo4j Tool 제한

```text
- MATCH / RETURN / OPTIONAL MATCH / WITH 만 기본 허용
- DELETE / DETACH DELETE / SET / MERGE / CREATE 는 seed/load 단계 외 차단
- Tool 호출 시 read-only Cypher 검사 통과해야 실행
- 결과 row LIMIT 기본값 100
```

## 4. 민감 데이터 마스킹

| 데이터 | 마스킹 정책 |
|---|---|
| 공급사 단가 | role=guest 사용자에게는 단가 컬럼 제외 |
| 고객사 연락처 | 항상 마스킹 (`010-****-1234`) |
| 임직원 이름 | `홍O동` 형태 마스킹 (PoC에서는 generic name 사용) |
| 원가 상세 | role∈{cost, finance} 만 |

PoC에서는 정책만 문서화하고 실제 마스킹 함수는 `services/` 레이어에서 추후 구현 위치를 명시한다.

## 5. Audit Log

각 `/chat` 요청은 다음을 audit log에 기록:

```json
{
  "request_id": "uuid",
  "user_id": "anon",
  "intent": "quality_root_cause_analysis",
  "used_sources": ["MES", "PLM", "Neo4j"],
  "tool_calls": [
    {"tool": "sql", "target": "MES", "ok": true, "rows": 12, "ms": 180},
    {"tool": "neo4j", "ok": true, "paths": 3, "ms": 240}
  ],
  "evidence_count": 5,
  "llm_provider": "gemini",
  "elapsed_ms": 2700,
  "ts": "2026-04-27T13:30:00+09:00"
}
```

운영 환경에서는 JSON Lines로 별도 audit storage (S3/CloudWatch/ELK)에 저장.

## 6. Human-in-the-loop (HITL)

자동 실행 금지 작업:

```text
- ERP 데이터 수정 / PLM BOM 변경 / MES 작업지시 변경
- 승인 상태 변경 / 외부 메시지 발송 / 파일 삭제 / 운영 DB write
```

쓰기 의도가 감지되면 Agent는 다음을 응답한다:

- `proposed_action`: 어떤 시스템에 어떤 변경이 필요한가
- `affected_records`: 영향받는 record_id 목록
- `approver_role`: 승인 가능한 역할
- `rollback_plan`: 롤백 절차

## 7. API Key / Secret 관리

- 모든 secret은 `.env`에서만 읽고, 절대 코드에 하드코딩하지 않는다.
- `.env`는 `.gitignore`에 포함되어 있다.
- 운영 환경에서는 `.env` 대신 secret manager (AWS Secrets Manager / Vault) 사용 가정.
- 클라이언트(Frontend)에는 LLM API Key를 절대 노출하지 않는다 (모든 LLM 호출은 backend 경유).

## 8. 운영망 / 개발망 분리 가정

```text
- 운영망: ERP/PLM/MES 실 시스템, 사내 LLM gateway
- 개발망: synthetic DB, 외부 Gemini API
- 본 PoC는 개발망 가정. 운영망 도입 시 Gemini → 사내 vLLM/Ollama로 교체.
```

## 9. 데이터 보관 / 폐기

- synthetic data는 무기한 보관 가능
- Agent trace/audit log: 운영 시 90일 보관 후 cold storage 권장 (조직 정책에 따름)
- LLM에 전달된 데이터는 외부 LLM(Gemini)일 경우 추가 평가 필요. Phase 2의 자체 LLM 도입 동기 중 하나.

## 10. 위험 시나리오 (예방 대상)

| 위험 | 대응 |
|---|---|
| LLM이 임의 SQL 생성 후 실행 | Tool에서 safety check, 최종적으로 SQL 직접 실행 권한 없음 |
| 권한 없는 데이터 조회 | 향후 RBAC + service layer에서 row-level filter |
| 오래된 BOM / 미승인 도면 기준 답변 | revision/approval_status 필터 권장 사용, 응답에 “기준일” 명시 |
| 원인 분석의 과도한 단정 | 응답 정책 — “후보/추정/가능성”으로 표현 강제 |
| 운영 시스템에 잘못된 write | HITL 정책으로 자동 차단, audit log 필수 |
