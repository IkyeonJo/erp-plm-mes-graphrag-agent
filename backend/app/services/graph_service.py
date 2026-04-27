"""
Graph service — Neo4j Tool 호출을 service 레벨로 wrapping.

PoC에서는 Neo4j가 없을 수도 있으므로, 연결 실패 시 빈 결과를 반환한다.
실제 운영에서는 모든 graph 호출은 read-only Cypher 만 허용된다.
"""

from __future__ import annotations

import logging
from typing import Any

from app.tools.neo4j_tool import neo4j_query

logger = logging.getLogger(__name__)


def get_product_graph(product_id: str) -> dict[str, Any]:
    cypher = """
    MATCH (p:Product {product_id: $product_id})-[:HAS_PART]->(part:Part)
    OPTIONAL MATCH (part)-[:SUPPLIED_BY]->(s:Supplier)
    RETURN p.product_id AS product_id,
           collect(DISTINCT {part_id: part.part_id, supplier_id: s.supplier_id}) AS parts
    """
    rows = neo4j_query(cypher, {"product_id": product_id})
    return {"rows": rows, "graph_path": f"Product({product_id}) → Part → Supplier"}


def get_supplier_impact(supplier_id: str) -> dict[str, Any]:
    cypher = """
    MATCH (s:Supplier {supplier_id: $supplier_id})<-[:SUPPLIED_BY]-(part:Part)<-[:HAS_PART]-(p:Product)
    RETURN s.supplier_id AS supplier_id, part.part_id AS part_id, p.product_id AS product_id
    """
    rows = neo4j_query(cypher, {"supplier_id": supplier_id})
    return {
        "rows": rows,
        "graph_path": f"Supplier({supplier_id}) → Part → Product",
    }
