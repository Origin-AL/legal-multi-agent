from __future__ import annotations

from typing import Any

from app.agents.base import BaseAgent
from app.rag.retriever import LegalKnowledgeRetriever


class LegalRetrievalAgent(BaseAgent):
    name = "legal_retrieval_agent"

    def __init__(self, llm_provider, retriever: LegalKnowledgeRetriever) -> None:
        super().__init__(llm_provider)
        self.retriever = retriever

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        matter_type = context["state"].get("matter_type", "")
        query = context["request"].user_query
        facts = context["state"].get("facts", [])
        retrieval_query = " ".join([query, str(matter_type), *[str(item) for item in facts[:5]]])
        matched = self.retriever.search(retrieval_query, top_k=4)
        return {
            "legal_basis": matched,
            "messages": [
                self.message("legal_reasoning_agent", f"Retrieved {len(matched)} authorities for issue analysis."),
                self.message("review_agent", "Check whether retrieved authorities sufficiently support the opinion."),
            ],
            "llm_debug": [
                self.debug_entry(
                    task="retrieval",
                    output={
                        "retrieval_query": retrieval_query,
                        "matches": [citation.model_dump() for citation in matched],
                    },
                )
            ],
            "summary": f"Retrieved {len(matched)} legal authorities.",
        }
