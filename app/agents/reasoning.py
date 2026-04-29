from __future__ import annotations

from typing import Any

from app.agents.base import BaseAgent
from app.models import Citation, IssueItem
from app.prompts import REASONING_SYSTEM_PROMPT
from app.utils.normalizers import normalize_risk_level


class LegalReasoningAgent(BaseAgent):
    name = "legal_reasoning_agent"

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        facts = context["state"].get("facts", [])
        legal_basis = context["state"].get("legal_basis", [])
        matter_type = context["state"].get("matter_type", "general_legal_consultation")
        user_prompt = "\n".join(
            [
                f"matter_type={matter_type}",
                f"facts={facts}",
                f"authorities={[citation.model_dump() for citation in legal_basis]}",
            ]
        )
        llm_result = self.llm_provider.generate_json(
            task="reasoning",
            system_prompt=REASONING_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        issues = [
            IssueItem(
                title=str(item.get("title", "Issue")),
                analysis=str(item.get("analysis", "")),
                risk_level=normalize_risk_level(str(item.get("risk_level", "medium"))),
                citations=self._match_citations(legal_basis, str(item.get("title", ""))),
            )
            for item in llm_result.get("issues", [])
        ]
        risk_level = normalize_risk_level(str(llm_result.get("risk_level", "medium")))
        suggested_actions = [str(item) for item in llm_result.get("suggested_actions", [])]
        draft_opinion = str(llm_result.get("draft_opinion", ""))
        return {
            "issues": issues,
            "risk_level": risk_level,
            "suggested_actions": suggested_actions,
            "draft_opinion": draft_opinion,
            "messages": [
                self.message("review_agent", f"Produced {len(issues)} issue entries. Check overreach and citation sufficiency.")
            ],
            "llm_debug": [self.debug_entry(task="reasoning", output=llm_result)],
            "summary": str(llm_result.get("summary", f"Generated {len(issues)} issue analyses.")),
        }

    def _match_citations(self, legal_basis: list[Citation], issue_title: str) -> list[Citation]:
        if "liquidated" in issue_title.lower() or "\u8fdd\u7ea6" in issue_title:
            return legal_basis[1:3] if len(legal_basis) > 2 else legal_basis
        return legal_basis[:2]
