from __future__ import annotations

from app.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.mock_provider import MockLLMProvider
from app.llm.openai_compatible import OpenAICompatibleProvider


def build_llm_provider() -> BaseLLMProvider:
    if settings.llm_provider == "openai-compatible" and settings.llm_api_key:
        return OpenAICompatibleProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    return MockLLMProvider()
