from __future__ import annotations

import re

from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.services import erp_service


def _extract_supplier_id(text: str) -> str | None:
    m = re.search(r"S-\d{2,3}", text)
    return m.group(0) if m else None


def _extract_item_id(text: str) -> str | None:
    m = re.search(r"P-\d{3}", text) or re.search(r"I-\d{3}", text)
    return m.group(0) if m else None


def call_erp_agent(state: AgentState, session: Session) -> AgentState:
    if "ERP" not in state.get("required_sources", []):
        return state

    q = state["user_query"]
    supplier_id = _extract_supplier_id(q)
    item_id = _extract_item_id(q)

    result: dict = {}

    if supplier_id:
        items = erp_service.get_supplier_items(session, supplier_id)
        result["supplier_items"] = items
        for it in items:
            state["evidence"].append(
                {
                    "source": "ERP.items",
                    "record_id": it["item_id"],
                    "description": f"공급사 {supplier_id} 부품 {it['item_name']}",
                }
            )

    if item_id:
        history = erp_service.get_purchase_history(session, item_id)
        inventory = erp_service.get_item_inventory(session, item_id)
        result["purchase_history"] = history
        result["inventory"] = inventory
        if history:
            state["evidence"].append(
                {
                    "source": "ERP.purchase_orders",
                    "record_id": history[0]["po_id"],
                    "description": f"{item_id} 최근 구매 이력",
                }
            )

    state["erp_result"] = result or None
    state["trace"].append({"node": "call_erp_agent", "supplier_id": supplier_id, "item_id": item_id})
    return state
