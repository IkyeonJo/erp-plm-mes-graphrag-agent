"""
SQL Tool — read-only SQL execution against synthetic ERP/PLM/MES SQLite.

Rules:
- SELECT 또는 WITH ... SELECT 만 허용
- 멀티 statement 차단 (세미콜론 split 후 첫 번째만)
- INSERT / UPDATE / DELETE / DROP / ALTER / TRUNCATE / GRANT / REVOKE 차단
- PRAGMA / ATTACH 차단
- 결과 row 수 LIMIT 기본 1000
"""

from __future__ import annotations

import logging
import re
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

FORBIDDEN_PATTERNS = [
    r"\binsert\b",
    r"\bupdate\b",
    r"\bdelete\b",
    r"\bdrop\b",
    r"\balter\b",
    r"\btruncate\b",
    r"\bgrant\b",
    r"\brevoke\b",
    r"\bpragma\b",
    r"\battach\b",
    r"\bdetach\b",
    r"\breplace\b",
    r"\binto\b",
    r"\bvacuum\b",
]
DEFAULT_LIMIT = 1000


class SqlSafetyError(Exception):
    pass


def _strip_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql.strip()


def safety_check(sql: str) -> str:
    """검증 통과 시 정규화된 SQL 반환, 실패 시 SqlSafetyError."""
    cleaned = _strip_comments(sql)
    if not cleaned:
        raise SqlSafetyError("empty SQL")

    parts = [p.strip() for p in cleaned.split(";") if p.strip()]
    if len(parts) > 1:
        raise SqlSafetyError("multiple statements not allowed")

    stmt = parts[0]
    lowered = stmt.lower()

    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise SqlSafetyError("only SELECT/WITH ... SELECT is allowed")

    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, lowered):
            raise SqlSafetyError(f"forbidden token detected: {pat}")

    return stmt


def execute_sql(
    session: Session,
    sql: str,
    params: dict[str, Any] | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    safe_sql = safety_check(sql)

    if "limit" not in safe_sql.lower():
        safe_sql = f"{safe_sql} LIMIT {limit}"

    logger.debug("execute_sql: %s | params=%s", safe_sql, params)
    result = session.execute(text(safe_sql), params or {})
    rows = [dict(r._mapping) for r in result]
    return rows
