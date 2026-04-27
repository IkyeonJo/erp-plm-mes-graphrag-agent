from __future__ import annotations

import json
import logging

from app.agents.state import AgentState
from app.llm.factory import get_llm_provider_safe

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a manufacturing AI assistant specialized in ERP/PLM/MES integrated analysis.

Rules:
- Answer ONLY based on the provided ERP/PLM/MES/Neo4j/SPARQL evidence.
- If evidence is insufficient, clearly say so. Do not invent.
- Express root cause analysis as candidates (가능성/후보/추정), not confirmed facts.
- Always include data source labels in your answer when citing facts.
- Mention that the dataset is synthetic when relevant.
- Respond in Korean by default; numbers and IDs stay as-is.
- Keep the answer concise but structured: 요약 → 핵심 발견 → 후보 원인 → 한계 → 다음 점검 권장사항.
""".strip()


def _build_user_prompt(state: AgentState) -> str:
    parts = [
        f"User question:\n{state['user_query']}",
        f"Intent: {state.get('intent', 'general')}",
        f"Used sources: {state.get('required_sources', [])}",
    ]

    for key in ("erp_result", "plm_result", "mes_result", "graph_result", "sparql_result"):
        value = state.get(key)
        if value:
            parts.append(f"{key}:\n{json.dumps(value, ensure_ascii=False, default=str)[:3500]}")

    parts.append(
        "Evidence:\n"
        + json.dumps(state.get("evidence", []), ensure_ascii=False, default=str)[:3500]
    )

    parts.append(
        "Response format:\n"
        "- 한국어로 답변\n"
        "- '데이터는 synthetic dataset 기반' 한계를 한 줄 포함\n"
        "- 원인 분석은 후보로 표현"
    )
    return "\n\n".join(parts)


async def generate_response_node(state: AgentState) -> AgentState:
    llm = get_llm_provider_safe()
    user_prompt = _build_user_prompt(state)

    try:
        answer = await llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=1024,
        )
    except Exception as e:
        logger.exception("response generation failed: %s", e)
        answer = ""
        state["errors"].append(f"response_generation_failed: {e}")

    if not answer:
        answer = (
            "LLM 응답을 받지 못했습니다. evidence 기반 raw 결과는 응답 객체의 evidence 필드를 참고하세요. "
            "(데이터는 synthetic dataset 기반)"
        )

    state["final_answer"] = answer
    state["trace"].append({"node": "generate_response", "provider": type(llm).__name__})
    return state
