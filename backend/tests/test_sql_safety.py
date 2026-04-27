from __future__ import annotations

import pytest

from app.tools.sql_tool import SqlSafetyError, safety_check


def test_select_allowed():
    assert safety_check("SELECT * FROM erp_items").lower().startswith("select")


def test_with_select_allowed():
    assert safety_check("WITH a AS (SELECT 1) SELECT * FROM a").lower().startswith("with")


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE erp_items",
        "DELETE FROM erp_items",
        "UPDATE erp_items SET item_name='x'",
        "INSERT INTO erp_items VALUES (1)",
        "ALTER TABLE erp_items ADD COLUMN x TEXT",
        "ATTACH DATABASE 'x.db' AS x",
        "PRAGMA writable_schema = 1",
    ],
)
def test_forbidden_blocked(sql: str):
    with pytest.raises(SqlSafetyError):
        safety_check(sql)


def test_multi_statement_blocked():
    with pytest.raises(SqlSafetyError):
        safety_check("SELECT 1; SELECT 2")
