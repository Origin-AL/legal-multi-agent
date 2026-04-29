from __future__ import annotations

import json
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError

from app.llm.base import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):
    name = "openai-compatible"

    def __init__(self, *, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = self._sanitize_api_key(api_key)
        self.model = model

    def generate_json(self, *, task: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
            "enable_thinking": False,
        }
        http_request = request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=60) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM provider returned HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            raise RuntimeError(f"LLM provider request failed: {exc.reason}") from exc

        content = raw["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        if not isinstance(content, str):
            content = str(content)
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            parsed = self._extract_json_object(content)
            if parsed is not None:
                return parsed
            raise RuntimeError(f"LLM provider did not return valid JSON content: {content}") from exc

    def _sanitize_api_key(self, api_key: str) -> str:
        cleaned = api_key.strip().replace("\ufeff", "").replace("\u200b", "")
        try:
            cleaned.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError(
                "LEGAL_LLM_API_KEY contains non-ASCII characters. Re-enter the API key manually and avoid Chinese punctuation or quotes."
            ) from exc
        return cleaned

    def _extract_json_object(self, content: str) -> dict[str, Any] | None:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        candidate = content[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None
