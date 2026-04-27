from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class GraphNode(BaseModel):
    label: str
    properties: dict[str, Any]


class GraphPath(BaseModel):
    summary: str
    nodes: list[GraphNode]
    record_id: str | None = None
