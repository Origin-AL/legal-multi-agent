from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    name: str

    @abstractmethod
    def generate_json(self, *, task: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        raise NotImplementedError
