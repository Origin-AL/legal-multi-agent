from __future__ import annotations

from typing import Any

from langfuse import observe

from app.agents.base import BaseAgent
from app.models import Citation, IssueItem
from app.prompts import REASONING_SYSTEM_PROMPT as _REASONING_FALLBACK
from app.utils.normalizers import normalize_risk_level


class LegalReasoningAgent(BaseAgent):
    name = "legal_reasoning_agent"

    @observe(as_type="agent", name="legal_reasoning_agent")
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
        system_prompt = self.prompt_manager.get_prompt("reasoning") if self.prompt_manager else _REASONING_FALLBACK
        llm_result = self.llm_provider.generate_json(
            task="reasoning",
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        issues = [
            IssueItem(
                title=str(item.get("title", "Issue")),
                analysis=str(item.get("analysis", "")),
                risk_level=normalize_risk_level(str(item.get("risk_level", "medium"))),
                citations=self._match_citations(legal_basis, item),
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

    def _match_citations(self, legal_basis: list[Citation], issue: dict[str, Any]) -> list[Citation]:
        """Match the most relevant citations to an issue based on keyword overlap and score."""
        if not legal_basis:
            return []

        issue_text = " ".join([
            str(issue.get("title", "")),
            str(issue.get("analysis", "")),
        ]).lower()

        scored: list[tuple[float, Citation]] = []
        for citation in legal_basis:
            relevance = citation.score
            citation_text = (citation.title + " " + citation.excerpt).lower()
            issue_chars = set(issue_text)
            cite_chars = set(citation_text)
            overlap = len(issue_chars & cite_chars)
            relevance += overlap * 0.01
            scored.append((relevance, citation))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:min(3, len(scored))]]
