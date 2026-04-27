from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, erp, graph, mes, plm
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="ERP/PLM/MES GraphRAG Agent",
    description=(
        "A manufacturing GraphRAG + LangGraph Agent PoC for integrated "
        "ERP/PLM/MES data search, analysis, and evidence-based response generation."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.APP_ENV}


app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(erp.router, prefix="/erp", tags=["erp"])
app.include_router(plm.router, prefix="/plm", tags=["plm"])
app.include_router(mes.router, prefix="/mes", tags=["mes"])
app.include_router(graph.router, prefix="/graph", tags=["graph"])
