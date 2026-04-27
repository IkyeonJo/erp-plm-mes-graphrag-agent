from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    """모든 LLM provider가 따라야 하는 공통 인터페이스.

    Agent 코드는 provider 객체에 의존하지 않고, 이 인터페이스만 사용한다.
    Phase 1: GeminiProvider
    Phase 2: OpenAICompatibleProvider (vLLM/Ollama/TGI/LM Studio/사내 gateway)
    """

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        ...
