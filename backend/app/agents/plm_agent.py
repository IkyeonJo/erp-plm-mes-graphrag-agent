from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.services import plm_service


def _extract_product_id(text: str) -> str | None:
    m = re.search(r"PROD-[A-Z0-9]+", text) or re.search(r"제품\s*([A-Z0-9-]+)", text)
    if m:
        token = m.group(0)
        if token.startswith("PROD-"):
            return token
    if "A제품" in text or "제품 A" in text:
        return "PROD-A"
    return None


def call_plm_agent(state: AgentState, session: Session) -> AgentState:
    if "PLM" not in state.get("required_sources", []):
        return state

    q = state["user_query"]
    product_id = _extract_product_id(q)

    result: dict = {}

    if product_id:
        product = plm_service.get_product(session, product_id)
        bom = plm_service.get_product_bom(session, product_id)
        result["product"] = product
        result["bom"] = bom
        if product:
            state["evidence"].append(
                {
                    "source": "PLM.products",
                    "record_id": product["product_id"],
                    "description": f"제품 {product['product_name']}",
                }
            )

    eco = plm_service.list_recent_eco(session, limit=10)
    result["recent_eco"] = eco
    for e in eco[:3]:
        state["evidence"].append(
            {
                "source": "PLM.eco",
                "record_id": e["eco_id"],
                "description": f"{e['change_type']} — {e['reason']}",
            }
        )

    state["plm_result"] = result or None
    state["trace"].append({"node": "call_plm_agent", "product_id": product_id})
    return state
