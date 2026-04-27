from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_query: str
    intent: str
    required_sources: list[str]

    erp_result: dict[str, Any] | None
    plm_result: dict[str, Any] | None
    mes_result: dict[str, Any] | None
    graph_result: dict[str, Any] | None
    sparql_result: dict[str, Any] | None

    analysis_result: dict[str, Any] | None
    evidence: list[dict[str, Any]]
    trace: list[dict[str, Any]]

    final_answer: str | None
    errors: list[str]


def empty_state(user_query: str) -> AgentState:
    return AgentState(
        user_query=user_query,
        intent="general",
        required_sources=[],
        erp_result=None,
        plm_result=None,
        mes_result=None,
        graph_result=None,
        sparql_result=None,
        analysis_result=None,
        evidence=[],
        trace=[],
        final_answer=None,
        errors=[],
    )
