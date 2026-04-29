from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.llm.base import BaseLLMProvider


class BaseAgent(ABC):
    name: str

    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        self.llm_provider = llm_provider

    @abstractmethod
    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def message(self, recipient: str, content: str) -> dict[str, str]:
        return {
            "sender": self.name,
            "recipient": recipient,
            "content": content,
        }

    def debug_entry(self, *, task: str, output: dict[str, Any] | list[Any] | str) -> dict[str, Any]:
        return {
            "agent_name": self.name,
            "task": task,
            "output": output,
        }
