from __future__ import annotations

from fastapi import APIRouter

from app.services import graph_service

router = APIRouter()


@router.get("/product/{product_id}")
def product_graph(product_id: str) -> dict:
    out = graph_service.get_product_graph(product_id)
    return {
        "product_id": product_id,
        "graph": out,
        "source": "Neo4j",
    }


@router.get("/supplier/{supplier_id}/impact")
def supplier_impact(supplier_id: str) -> dict:
    out = graph_service.get_supplier_impact(supplier_id)
    return {
        "supplier_id": supplier_id,
        "impact": out,
        "source": "Neo4j",
    }
