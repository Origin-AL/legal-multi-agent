from __future__ import annotations

from typing import Any

from app.agents.base import BaseAgent
from app.models import MatterType
from app.prompts import INTAKE_SYSTEM_PROMPT
from app.utils.normalizers import normalize_matter_type


class IntakeAgent(BaseAgent):
    name = "intake_agent"

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        request = context["request"]
        user_prompt = (
            f"QUERY: {request.user_query}\n"
            f"CASE_TYPE_HINT: {request.case_type_hint or ''}\n"
            "Return the most likely legal matter type."
        )
        llm_result = self.llm_provider.generate_json(
            task="intake",
            system_prompt=INTAKE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        matter_type = normalize_matter_type(str(llm_result.get("matter_type", MatterType.general_legal_consultation.value)))
        return {
            "matter_type": matter_type,
            "required_materials": list(llm_result.get("required_materials", ["background_facts"])),
            "messages": [
                self.message("fact_extraction_agent", f"Extract material facts for {matter_type.value}."),
                self.message("legal_retrieval_agent", f"Retrieve authorities for matter type: {matter_type.value}."),
            ],
            "llm_debug": [self.debug_entry(task="intake", output=llm_result)],
            "summary": str(llm_result.get("summary", f"Classified request as {matter_type}.")),
        }
