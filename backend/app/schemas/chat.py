from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="사용자 자연어 질문")
    user_id: str | None = Field(default=None, description="요청 사용자 (PoC에서는 anon 가능)")


class EvidenceItem(BaseModel):
    source: str
    record_id: str | None = None
    description: str | None = None
    extra: dict[str, Any] | None = None


class TraceItem(BaseModel):
    node: str
    detail: str | None = None
    elapsed_ms: int | None = None


class ChatResponse(BaseModel):
    answer: str
    intent: str
    used_sources: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    trace: list[TraceItem] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
