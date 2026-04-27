from __future__ import annotations

from app.agents.intent_classifier import classify_intent_node, route_sources_node
from app.agents.state import empty_state


def test_quality_root_cause():
    state = empty_state("A제품의 최근 3개월 불량률이 상승한 원인을 분석해줘.")
    state = classify_intent_node(state)
    state = route_sources_node(state)

    assert state["intent"] == "quality_root_cause_analysis"
    assert "MES" in state["required_sources"]
    assert "Neo4j" in state["required_sources"]


def test_supplier_impact():
    state = empty_state("공급사 S-03의 부품이 들어간 제품과 최근 품질 이슈를 알려줘.")
    state = classify_intent_node(state)
    state = route_sources_node(state)

    assert state["intent"] == "supplier_impact"
    assert "ERP" in state["required_sources"]


def test_general_question():
    state = empty_state("오늘 날씨 어때?")
    state = classify_intent_node(state)
    state = route_sources_node(state)

    assert state["intent"] == "general"
    assert state["required_sources"] == []
