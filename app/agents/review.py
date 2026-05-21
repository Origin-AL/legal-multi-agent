from __future__ import annotations

from typing import Any

from langfuse import observe

from app.agents.base import BaseAgent
from app.prompts import REVIEW_SYSTEM_PROMPT
from app.utils.normalizers import normalize_confidence_level


class ReviewAgent(BaseAgent):
    name = "review_agent"

    @observe(as_type="agent", name="review_agent")
    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        request = context["request"]
        facts = context["state"].get("facts", [])
        issues = context["state"].get("issues", [])
        legal_basis = context["state"].get("legal_basis", [])
        draft_opinion = context["state"].get("draft_opinion", "")
        matter_type = context["state"].get("matter_type", "general_legal_consultation")
        user_prompt = "\n".join(
            [
                f"matter_type={matter_type}",
                f"user_query={request.user_query}",
                f"materials={[material.model_dump() for material in request.materials]}",
                f"facts={facts}",
                f"issues={[issue.model_dump() for issue in issues]}",
                f"legal_basis={[citation.model_dump() for citation in legal_basis]}",
                f"draft_opinion={draft_opinion}",
            ]
        )
        llm_result = self.llm_provider.generate_json(
            task="review",
            system_prompt=REVIEW_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        confidence = normalize_confidence_level(str(llm_result.get("confidence", "medium")))
        review_notes = [str(item) for item in llm_result.get("review_notes", [])]
        return {
            "confidence": confidence,
            "review_notes": review_notes,
            "messages": [self.message("orchestrator", f"Review completed with confidence={confidence.value}.")],
            "llm_debug": [self.debug_entry(task="review", output=llm_result)],
            "summary": str(llm_result.get("summary", f"Assigned confidence level {confidence.value}.")),
        }
