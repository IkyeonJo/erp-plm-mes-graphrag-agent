"""
키워드 기반 1차 분류기. 향후 LLM 기반으로 강화 가능.
"""

from __future__ import annotations

from app.agents.state import AgentState

INTENT_KEYWORDS: dict[str, list[str]] = {
    "quality_root_cause_analysis": ["불량률", "원인", "왜", "올랐", "상승", "increase"],
    "bom_mismatch": ["BOM", "투입 부품", "다른", "불일치", "차이"],
    "supplier_impact": ["공급사", "supplier", "납품"],
    "eco_impact": ["설계변경", "ECO", "ECR", "design change"],
    "product_summary": ["요약", "통합", "summary"],
}

SOURCE_KEYWORDS: dict[str, list[str]] = {
    "ERP": ["재고", "구매", "원가", "공급사", "수주", "납기", "단가"],
    "PLM": ["BOM", "도면", "설계변경", "ECO", "ECR", "revision", "사양"],
    "MES": ["생산", "LOT", "불량", "공정", "설비", "검사", "불량률"],
    "Neo4j": ["관계", "영향", "연결", "추적", "원인", "경로"],
    "SPARQL": ["온톨로지", "RDF", "SPARQL"],
}

INTENT_TO_SOURCES: dict[str, list[str]] = {
    "quality_root_cause_analysis": ["MES", "PLM", "ERP", "Neo4j"],
    "bom_mismatch": ["PLM", "MES", "Neo4j"],
    "supplier_impact": ["ERP", "PLM", "MES", "Neo4j"],
    "eco_impact": ["PLM", "MES", "Neo4j"],
    "product_summary": ["ERP", "PLM", "MES", "Neo4j"],
    "general": [],
}


def classify_intent_node(state: AgentState) -> AgentState:
    q = state["user_query"]

    intent = "general"
    for name, kws in INTENT_KEYWORDS.items():
        if any(kw.lower() in q.lower() for kw in kws):
            intent = name
            break

    state["intent"] = intent
    state["trace"].append({"node": "classify_intent", "intent": intent})
    return state


def route_sources_node(state: AgentState) -> AgentState:
    intent = state.get("intent", "general")
    base_sources = INTENT_TO_SOURCES.get(intent, [])

    keyword_sources: list[str] = []
    q = state["user_query"]
    for src, kws in SOURCE_KEYWORDS.items():
        if any(kw.lower() in q.lower() for kw in kws):
            keyword_sources.append(src)

    merged = list(dict.fromkeys(base_sources + keyword_sources))
    state["required_sources"] = merged
    state["trace"].append({"node": "route_sources", "required_sources": merged})
    return state
