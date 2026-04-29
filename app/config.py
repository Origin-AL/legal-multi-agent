from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "Legal Multi-Agent MVP"
    knowledge_base_path: Path = Path("data/legal_knowledge.json")
    database_path: Path = Path("data/legal_agent.db")
    llm_provider: str = os.getenv("LEGAL_LLM_PROVIDER", "mock")
    llm_model: str = os.getenv("LEGAL_LLM_MODEL", "mock-legal-model")
    llm_api_key: str | None = os.getenv("LEGAL_LLM_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    llm_base_url: str = os.getenv("LEGAL_LLM_BASE_URL", "https://api.openai.com/v1")


settings = Settings()
