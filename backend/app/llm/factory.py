from __future__ import annotations

import logging

from app.core.config import settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


def get_llm_provider() -> BaseLLMProvider:
    provider_name = (settings.LLM_PROVIDER or "gemini").lower()

    if provider_name == "gemini":
        from app.llm.gemini_provider import GeminiProvider

        return GeminiProvider()

    if provider_name in {"openai_compatible", "vllm", "ollama", "tgi", "lmstudio"}:
        from app.llm.openai_compatible_provider import OpenAICompatibleProvider

        return OpenAICompatibleProvider()

    raise ValueError(f"Unsupported LLM provider: {provider_name}")


class StubProvider(BaseLLMProvider):
    """LLM_PROVIDER 미설정 / API Key 부재 시 사용하는 fallback.

    실제 모델 호출 없이 evidence를 그대로 정리하여 반환한다.
    PoC 실행성과 데모 가능성을 보장하기 위한 안전망.
    """

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs,  # type: ignore[no-untyped-def]
    ) -> str:
        return (
            "⚠️ LLM provider 미설정 또는 호출 실패로 stub 응답을 반환합니다.\n"
            "수집된 evidence는 응답 객체의 evidence 필드를 참고하세요.\n\n"
            f"[user prompt 요약]\n{user_prompt[:600]}"
        )


def get_llm_provider_safe() -> BaseLLMProvider:
    """예외 없이 항상 provider 반환 (stub fallback)."""
    try:
        return get_llm_provider()
    except Exception as e:
        logger.warning("LLM provider init failed (%s); falling back to StubProvider", e)
        return StubProvider()
