"""Langfuse Prompt Management integration with local fallback.

Prompts are fetched from Langfuse and cached by the SDK (5 min TTL).
If Langfuse is unavailable, hardcoded prompts from app.prompts are used as fallback.
"""
from __future__ import annotations

import logging
from typing import Any

from langfuse import Langfuse

from app.prompts import (
    FACT_SYSTEM_PROMPT,
    INTAKE_SYSTEM_PROMPT,
    REASONING_SYSTEM_PROMPT,
    REVIEW_SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)

_PROMPT_MAP: dict[str, str] = {
    "intake": INTAKE_SYSTEM_PROMPT,
    "facts": FACT_SYSTEM_PROMPT,
    "reasoning": REASONING_SYSTEM_PROMPT,
    "review": REVIEW_SYSTEM_PROMPT,
}


class PromptManager:
    """Fetches prompts from Langfuse Prompt Management with local fallback."""

    def __init__(self, langfuse_client: Langfuse) -> None:
        self._client = langfuse_client

    def get_prompt(self, task: str, *, version: int | str | None = None, label: str = "production") -> str:
        """Return the system prompt for a given task.

        Tries Langfuse Prompt Management first, falls back to local prompts.
        """
        if task not in _PROMPT_MAP:
            raise ValueError(f"Unknown prompt task: {task}. Valid tasks: {list(_PROMPT_MAP)}")

        try:
            if version is not None:
                prompt = self._client.get_prompt(task, version=version)
            else:
                prompt = self._client.get_prompt(task, label=label)
            result = prompt.compile()
            return result[0] if isinstance(result, list) else result
        except Exception:
            logger.debug("Langfuse prompt fetch failed for task=%s, using local fallback", task)
            return _PROMPT_MAP[task]
