"""
RAG Tool — 비정형 문서 검색.

PoC에서는 단순 keyword search 위주.
실제 운영에서는 vector store(예: Chroma/PGVector) 도입.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def keyword_search(query: str, base_dir: str | Path, top_k: int = 5) -> list[dict[str, Any]]:
    base = Path(base_dir)
    if not base.exists():
        return []

    hits: list[dict[str, Any]] = []
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if query.lower() in text.lower():
            snippet_idx = text.lower().find(query.lower())
            snippet = text[max(0, snippet_idx - 60) : snippet_idx + 140]
            hits.append(
                {
                    "path": str(path),
                    "snippet": snippet,
                    "score": text.lower().count(query.lower()),
                }
            )

    hits.sort(key=lambda h: h["score"], reverse=True)
    return hits[:top_k]
