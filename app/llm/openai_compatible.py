from __future__ import annotations

import json
import logging
import time
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError

from langfuse import get_client, observe

from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RETRY_BACKOFF_BASE = 1.5
_RETRYABLE_HTTP_CODES = {408, 429, 500, 502, 503, 504}


class OpenAICompatibleProvider(BaseLLMProvider):
    name = "openai-compatible"

    def __init__(self, *, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = self._sanitize_api_key(api_key)
        self.model = model

    @observe(as_type="generation")
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
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}/chat/completions"

        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            http_request = request.Request(url=url, data=body, headers=headers, method="POST")
            try:
                with request.urlopen(http_request, timeout=60) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                break
            except HTTPError as exc:
                last_exc = exc
                if exc.code not in _RETRYABLE_HTTP_CODES:
                    raise RuntimeError(
                        f"LLM provider returned HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}"
                    ) from exc
                logger.warning("LLM HTTP %d on attempt %d/%d", exc.code, attempt + 1, _MAX_RETRIES)
            except URLError as exc:
                last_exc = exc
                logger.warning("LLM network error on attempt %d/%d: %s", attempt + 1, _MAX_RETRIES, exc.reason)
            except TimeoutError:
                last_exc = TimeoutError("request timed out")
                logger.warning("LLM timeout on attempt %d/%d", attempt + 1, _MAX_RETRIES)

            if attempt < _MAX_RETRIES - 1:
                delay = _RETRY_BACKOFF_BASE * (2 ** attempt) + attempt * 0.3
                time.sleep(delay)
        else:
            raise RuntimeError(f"LLM provider failed after {_MAX_RETRIES} attempts: {last_exc}") from last_exc

        content = raw["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        if not isinstance(content, str):
            content = str(content)

        client = get_client()
        usage = raw.get("usage")
        if usage:
            client.update_current_generation(
                model=self.model,
                usage_details={
                    "input": usage.get("prompt_tokens", 0),
                    "output": usage.get("completion_tokens", 0),
                    "total": usage.get("total_tokens", 0),
                },
                metadata={"task": task},
            )
        else:
            client.update_current_generation(
                model=self.model,
                metadata={"task": task},
            )

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
