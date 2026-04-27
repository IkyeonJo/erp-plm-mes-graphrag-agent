from __future__ import annotations

import re

from app.agents.state import AgentState
from app.services import graph_service


def call_graph_agent(state: AgentState) -> AgentState:
    if "Neo4j" not in state.get("required_sources", []):
        return state

    q = state["user_query"]
    result: dict = {}

    m = re.search(r"S-\d{2,3}", q)
    if m:
        sup = m.group(0)
        result["supplier_impact"] = graph_service.get_supplier_impact(sup)
        state["evidence"].append(
            {
                "source": "Neo4j",
                "record_id": f"graph-supplier-{sup}",
                "description": result["supplier_impact"]["graph_path"],
            }
        )

    m2 = re.search(r"PROD-[A-Z0-9]+", q)
    product_id = m2.group(0) if m2 else ("PROD-A" if "A제품" in q else None)
    if product_id:
        result["product_graph"] = graph_service.get_product_graph(product_id)
        state["evidence"].append(
            {
                "source": "Neo4j",
                "record_id": f"graph-product-{product_id}",
                "description": result["product_graph"]["graph_path"],
            }
        )

    state["graph_result"] = result or None
    state["trace"].append({"node": "call_graph_agent"})
    return state
