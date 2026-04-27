from __future__ import annotations

import logging
from typing import Any

from app.core.config import settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. .env 또는 환경변수에 설정하세요."
            )
        try:
            import google.generativeai as genai
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "google-generativeai 패키지가 설치되어 있지 않습니다. `uv add google-generativeai`"
            ) from e

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._genai = genai
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        prompt = f"{system_prompt}\n\nUser:\n{user_prompt}".strip()
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return getattr(response, "text", "") or ""
        except Exception as e:
            logger.exception("Gemini generate failed: %s", e)
            return ""
