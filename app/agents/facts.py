from __future__ import annotations

from typing import Any

from app.agents.base import BaseAgent
from app.prompts import FACT_SYSTEM_PROMPT


class FactExtractionAgent(BaseAgent):
    name = "fact_extraction_agent"

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        request = context["request"]
        lines = [f"QUERY: {request.user_query}"]
        for material in request.materials:
            lines.append(f"MATERIAL: {material.title}")
            for chunk in material.content.replace("\n", " ").split("。"):
                chunk = chunk.strip()
                if chunk:
                    lines.append(f"MATERIAL: {chunk}")
        llm_result = self.llm_provider.generate_json(
            task="facts",
            system_prompt=FACT_SYSTEM_PROMPT,
            user_prompt="\n".join(lines),
        )
        facts = [str(item) for item in llm_result.get("facts", [])]
        return {
            "facts": facts,
            "messages": [
                self.message(
                    "legal_reasoning_agent",
                    f"Prepared {len(facts)} fact items. Separate proven facts from assumptions.",
                )
            ],
            "llm_debug": [self.debug_entry(task="facts", output=llm_result)],
            "summary": str(llm_result.get("summary", f"Extracted {len(facts)} fact items.")),
        }
