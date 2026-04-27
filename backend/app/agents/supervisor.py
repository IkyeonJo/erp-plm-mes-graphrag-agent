"""
LangGraph Supervisor — 단일 호출 진입점.

PoC에서는 LangGraph StateGraph 대신 명시적 파이프라인 함수로 구현.
이 구조를 그대로 LangGraph로 매핑할 수 있도록 node 단위로 분해되어 있다.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.agents.analysis_agent import analyze_results_node
from app.agents.erp_agent import call_erp_agent
from app.agents.graph_agent import call_graph_agent
from app.agents.intent_classifier import classify_intent_node, route_sources_node
from app.agents.mes_agent import call_mes_agent
from app.agents.plm_agent import call_plm_agent
from app.agents.response_agent import generate_response_node
from app.agents.sparql_agent import call_sparql_agent
from app.agents.state import empty_state

logger = logging.getLogger(__name__)


async def run_supervisor(user_query: str, session: Session) -> dict[str, Any]:
    state = empty_state(user_query)

    state = classify_intent_node(state)
    state = route_sources_node(state)

    state = call_erp_agent(state, session)
    state = call_plm_agent(state, session)
    state = call_mes_agent(state, session)
    state = call_graph_agent(state)
    state = call_sparql_agent(state)

    state = analyze_results_node(state)
    state = await generate_response_node(state)

    return {
        "answer": state.get("final_answer") or "응답을 생성하지 못했습니다.",
        "intent": state.get("intent", "general"),
        "used_sources": state.get("required_sources", []),
        "evidence": state.get("evidence", []),
        "trace": state.get("trace", []),
        "limitations": [
            "본 응답은 synthetic dataset 기반으로 생성되었습니다.",
            "원인 분석 항목은 확정된 결론이 아닌 후보(가설)입니다.",
        ],
    }
