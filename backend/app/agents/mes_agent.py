from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.services import mes_service


def _extract_product_id(text: str) -> str | None:
    m = re.search(r"PROD-[A-Z0-9]+", text)
    if m:
        return m.group(0)
    if "A제품" in text or "제품 A" in text:
        return "PROD-A"
    return None


def _extract_lot_id(text: str) -> str | None:
    m = re.search(r"LOT-[A-Z0-9]+", text)
    return m.group(0) if m else None


def call_mes_agent(state: AgentState, session: Session) -> AgentState:
    if "MES" not in state.get("required_sources", []):
        return state

    q = state["user_query"]
    product_id = _extract_product_id(q)
    lot_id = _extract_lot_id(q)

    result: dict = {}

    if product_id:
        result["monthly_defect_rate"] = mes_service.get_monthly_defect_rate(session, product_id)
        result["top_defect_types"] = mes_service.top_defect_types(session, product_id)
        for row in result["monthly_defect_rate"][-3:]:
            state["evidence"].append(
                {
                    "source": "MES.production_results",
                    "record_id": f"{product_id}-{row['period']}",
                    "description": f"{row['period']} 불량률 {row['defect_rate']*100:.2f}%",
                }
            )

    if lot_id:
        result["lot_trace"] = mes_service.trace_lot(session, lot_id)
        if result["lot_trace"]:
            state["evidence"].append(
                {
                    "source": "MES.lots",
                    "record_id": lot_id,
                    "description": f"LOT {lot_id} 생산 이력 추적",
                }
            )

    state["mes_result"] = result or None
    state["trace"].append({"node": "call_mes_agent", "product_id": product_id, "lot_id": lot_id})
    return state
