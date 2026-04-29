from __future__ import annotations

from typing import Any

from app.llm.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    name = "mock"

    def generate_json(self, *, task: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        prompt = user_prompt.lower()

        if task == "intake":
            matter_type = "general_legal_consultation"
            if any(token in prompt for token in ["\u5408\u540c", "\u89e3\u9664", "\u8fdd\u7ea6", "contract", "breach"]):
                matter_type = "contract_review"
            elif any(token in prompt for token in ["\u52b3\u52a8", "\u52a0\u73ed", "\u8d54\u507f", "labor", "employment"]):
                matter_type = "labor_dispute"
            return {
                "matter_type": matter_type,
                "required_materials": ["contract_text", "background_facts"],
                "summary": f"Classified request as {matter_type}.",
            }

        if task == "facts":
            facts = []
            for block in user_prompt.split("\n"):
                text = block.strip()
                if text.startswith("MATERIAL:"):
                    facts.append(text.removeprefix("MATERIAL:").strip())
                elif text.startswith("QUERY:"):
                    facts.append(text.removeprefix("QUERY:").strip())
            return {
                "facts": facts[:8] if facts else ["No extracted facts."],
                "summary": f"Extracted {min(len(facts), 8)} fact items.",
            }

        if task == "reasoning":
            if "contract_review" in user_prompt:
                return {
                    "issues": [
                        {
                            "title": "Termination clause enforceability",
                            "analysis": "Review whether termination triggers, notice duty, and cure period are clearly defined.",
                            "risk_level": "medium",
                        },
                        {
                            "title": "Liquidated damages reasonableness",
                            "analysis": "Review whether the agreed penalty is obviously disproportionate to expected losses.",
                            "risk_level": "high",
                        },
                    ],
                    "risk_level": "high",
                    "suggested_actions": [
                        "Check notice evidence and breach timeline.",
                        "Assess whether 30% liquidated damages can be justified by actual losses.",
                        "Clarify termination trigger and cure period wording.",
                    ],
                    "draft_opinion": "Preliminary contract review suggests material risk around termination and liquidated damages design.",
                    "summary": "Generated 2 issue analyses.",
                }
            return {
                "issues": [
                    {
                        "title": "Insufficient fact pattern",
                        "analysis": "The current record is insufficient for a conclusive opinion.",
                        "risk_level": "medium",
                    }
                ],
                "risk_level": "medium",
                "suggested_actions": ["Upload the core agreement, evidence, and timeline."],
                "draft_opinion": "Only a preliminary view is possible based on the current materials.",
                "summary": "Generated 1 issue analysis.",
            }

        if task == "review":
            confidence = "high" if "legal_basis=[]" not in user_prompt and "materials=[]" not in user_prompt else "low"
            notes = [
                "Confirm that the termination trigger is supported by the actual delivery timeline and any notice record, not only by the clause text.",
                "The liquidated damages discussion should expressly distinguish contractual drafting risk from likely judicial adjustment risk under the cited authority.",
                "Before relying on the opinion externally, verify whether there are cure rights, exceptions, or subsequent performance communications that could weaken termination grounds.",
            ]
            return {
                "confidence": confidence,
                "review_notes": notes,
                "summary": "The draft is directionally usable, but it still needs evidence-linked verification on breach facts, notice, and the proportionality of liquidated damages.",
            }

        return {"summary": "No-op response."}
