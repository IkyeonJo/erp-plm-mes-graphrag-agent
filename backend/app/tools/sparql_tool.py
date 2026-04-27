"""
SPARQL Tool — RDF/OWL ontology 기반 SELECT 쿼리.

Rules:
- SELECT 만 허용 (CONSTRUCT / DESCRIBE / ASK 는 PoC 범위 외)
- ontology/manufacturing.ttl 을 로드
- 결과는 JSON serializable 구조로 반환
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_TTL = Path(__file__).resolve().parents[3] / "ontology" / "manufacturing.ttl"


class SparqlSafetyError(Exception):
    pass


def _safety_check(query: str) -> str:
    stripped = query.strip()
    lowered = stripped.lower()
    if not lowered.startswith("select") and not lowered.startswith("prefix"):
        raise SparqlSafetyError("only SELECT (with optional PREFIX) is allowed")
    if re.search(r"\b(insert|delete|drop|clear|create)\b", lowered):
        raise SparqlSafetyError("forbidden SPARQL update keyword detected")
    return stripped


def sparql_query(
    query: str, ttl_path: str | Path | None = None
) -> list[dict[str, Any]]:
    safe = _safety_check(query)

    try:
        from rdflib import Graph
    except ImportError:
        logger.warning("rdflib not installed; returning empty result")
        return []

    path = Path(ttl_path) if ttl_path else DEFAULT_TTL
    if not path.exists():
        logger.warning("ontology TTL not found: %s; returning empty result", path)
        return []

    g = Graph()
    g.parse(path.as_posix(), format="turtle")

    try:
        results = g.query(safe)
    except Exception as e:
        logger.warning("SPARQL query failed: %s", e)
        return []

    out: list[dict[str, Any]] = []
    for row in results:
        try:
            labels = list(results.vars or [])
            out.append({str(k): str(v) for k, v in zip(labels, row, strict=False)})
        except Exception:  # pragma: no cover
            out.append({"value": str(row)})
    return out
