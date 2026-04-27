from __future__ import annotations

import logging
from typing import Any

from app.core.config import settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    """OpenAI-compatible API 형식의 LLM provider.

    예: vLLM OpenAI server, Ollama (`/v1`), TGI, LM Studio, 사내 LLM gateway.
    Phase 2의 자체 오픈소스 LLM 통합 시 그대로 재사용.
    """

    def __init__(self) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "openai 패키지가 설치되어 있지 않습니다. `uv add openai`"
            ) from e

        self.client = AsyncOpenAI(
            api_key=settings.LOCAL_LLM_API_KEY or settings.OPENAI_API_KEY or "no-key",
            base_url=settings.LOCAL_LLM_BASE_URL,
        )
        self.model = settings.LOCAL_LLM_MODEL

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.exception("OpenAI-compatible generate failed: %s", e)
            return ""
