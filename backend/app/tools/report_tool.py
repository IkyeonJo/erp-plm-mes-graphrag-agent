"""
Report Tool — Agent 결과를 structured report로 변환.
"""

from __future__ import annotations

from typing import Any


def build_report(
    summary: str,
    findings: list[str] | None = None,
    root_cause_candidates: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    recommended_actions: list[str] | None = None,
    limitations: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "summary": summary,
        "findings": findings or [],
        "root_cause_candidates": root_cause_candidates or [],
        "evidence": evidence or [],
        "recommended_actions": recommended_actions or [],
        "limitations": limitations or [],
    }
