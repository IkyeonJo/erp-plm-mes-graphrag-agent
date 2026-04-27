from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.supervisor import run_supervisor
from app.db.session import get_session
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, session: Session = Depends(get_session)) -> ChatResponse:
    logger.info("[/chat] user_id=%s, message=%r", req.user_id, req.message)
    result = await run_supervisor(req.message, session=session)
    return ChatResponse(**result)
