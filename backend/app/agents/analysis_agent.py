from __future__ import annotations

from app.agents.state import AgentState


def analyze_results_node(state: AgentState) -> AgentState:
    findings: list[str] = []
    candidates: list[str] = []

    mes = state.get("mes_result") or {}
    plm = state.get("plm_result") or {}
    erp = state.get("erp_result") or {}
    graph = state.get("graph_result") or {}

    if mes.get("monthly_defect_rate"):
        rates = mes["monthly_defect_rate"]
        if len(rates) >= 2:
            first, last = rates[0], rates[-1]
            delta = last["defect_rate"] - first["defect_rate"]
            if delta > 0.005:
                findings.append(
                    f"불량률이 {first['period']} {first['defect_rate']*100:.2f}% → "
                    f"{last['period']} {last['defect_rate']*100:.2f}% 로 변동"
                )
                if delta > 0.01:
                    candidates.append("MES 공정/설비 변경 또는 부품 공급사 변경 후보")

    if plm.get("recent_eco"):
        eco_count = len(plm["recent_eco"])
        if eco_count > 0:
            candidates.append(f"최근 ECO {eco_count}건 발생 — 변경 영향 검토 필요")

    if erp.get("supplier_items"):
        findings.append(f"공급사 영향 부품 수: {len(erp['supplier_items'])}")

    if graph.get("supplier_impact") or graph.get("product_graph"):
        findings.append("Knowledge Graph 경로 탐색 결과 evidence에 포함")

    state["analysis_result"] = {
        "findings": findings,
        "root_cause_candidates": candidates,
    }
    state["trace"].append(
        {
            "node": "analyze_results",
            "findings": len(findings),
            "candidates": len(candidates),
        }
    )
    return state
