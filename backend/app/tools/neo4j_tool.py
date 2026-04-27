"""
Neo4j Tool — read-only Cypher 실행.

Rules:
- MATCH / RETURN / OPTIONAL MATCH / WITH 만 기본 허용
- DELETE / DETACH / SET / MERGE / CREATE / REMOVE 는 차단
- Neo4j 미연결 시 빈 결과 반환 (PoC 실행성 보장)
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

_FORBIDDEN_CYPHER = [
    r"\bdelete\b",
    r"\bdetach\b",
    r"\bset\b",
    r"\bmerge\b",
    r"\bcreate\b",
    r"\bremove\b",
    r"\bdrop\b",
]


class CypherSafetyError(Exception):
    pass


def cypher_safety_check(cypher: str) -> str:
    cleaned = re.sub(r"//.*?$", "", cypher, flags=re.MULTILINE).strip()
    lowered = cleaned.lower()

    for pat in _FORBIDDEN_CYPHER:
        if re.search(pat, lowered):
            raise CypherSafetyError(f"forbidden Cypher token: {pat}")

    if "match" not in lowered and "with" not in lowered:
        raise CypherSafetyError("read-only Cypher must contain MATCH/WITH")

    return cleaned


def neo4j_query(cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Neo4j 미연결 환경에서는 빈 결과를 반환하여 PoC 실행성을 유지."""
    safe = cypher_safety_check(cypher)

    try:
        from neo4j import GraphDatabase
    except ImportError:
        logger.warning("neo4j driver not installed; returning empty result")
        return []

    try:
        driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    except Exception as e:  # pragma: no cover
        logger.warning("Neo4j connection failed: %s; returning empty result", e)
        return []

    try:
        with driver.session(database=settings.NEO4J_DATABASE) as session:
            result = session.run(safe, params or {})
            return [dict(r) for r in result]
    except Exception as e:
        logger.warning("Neo4j query failed: %s", e)
        return []
    finally:
        driver.close()
