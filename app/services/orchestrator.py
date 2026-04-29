from __future__ import annotations

from app.agents.facts import FactExtractionAgent
from app.agents.intake import IntakeAgent
from app.agents.reasoning import LegalReasoningAgent
from app.agents.retrieval import LegalRetrievalAgent
from app.agents.review import ReviewAgent
from app.config import settings
from app.llm.factory import build_llm_provider
from app.llm.base import BaseLLMProvider
from app.models import (
    AgentTrace,
    AnalysisRequest,
    AnalysisResponse,
    ConfidenceLevel,
    CoordinationMessage,
    LLMDebugEntry,
    RiskLevel,
)
from app.rag.knowledge_loader import load_knowledge_documents
from app.rag.retriever import LegalKnowledgeRetriever
from app.repositories.analysis_repository import AnalysisRepository


class LegalOrchestrator:
    def __init__(
        self,
        *,
        llm_provider: BaseLLMProvider | None = None,
        retriever: LegalKnowledgeRetriever | None = None,
        repository: AnalysisRepository | None = None,
    ) -> None:
        llm_provider = llm_provider or build_llm_provider()
        retriever = retriever or LegalKnowledgeRetriever(load_knowledge_documents(settings.knowledge_base_path))
        repository = repository or AnalysisRepository(settings.database_path)

        self.repository = repository
        self.pipeline = [
            IntakeAgent(llm_provider),
            FactExtractionAgent(llm_provider),
            LegalRetrievalAgent(llm_provider, retriever),
            LegalReasoningAgent(llm_provider),
            ReviewAgent(llm_provider),
        ]

    def run(self, request: AnalysisRequest) -> AnalysisResponse:
        state: dict[str, object] = {}
        trace: list[AgentTrace] = []
        coordination_log: list[CoordinationMessage] = []
        llm_debug: list[LLMDebugEntry] = []

        for agent in self.pipeline:
            result = agent.run({"request": request, "state": state})
            summary = str(result.pop("summary", ""))
            raw_messages = result.pop("messages", [])
            raw_debug = result.pop("llm_debug", [])
            state.update(result)
            trace.append(AgentTrace(agent_name=agent.name, summary=summary))
            coordination_log.extend(CoordinationMessage(**message) for message in raw_messages)
            llm_debug.extend(LLMDebugEntry(**entry) for entry in raw_debug)

        response = AnalysisResponse(
            analysis_id=self.repository.create_analysis_id(),
            case_id=self.repository.create_case_id(),
            matter_type=state.get("matter_type"),
            risk_level=state.get("risk_level", RiskLevel.medium),
            confidence=state.get("confidence", ConfidenceLevel.low),
            facts=list(state.get("facts", [])),
            legal_basis=list(state.get("legal_basis", [])),
            issues=list(state.get("issues", [])),
            suggested_actions=list(state.get("suggested_actions", [])),
            draft_opinion=str(state.get("draft_opinion", "")),
            review_notes=list(state.get("review_notes", [])),
            coordination_log=coordination_log,
            trace=trace,
            llm_debug=llm_debug,
            created_at=self.repository.now(),
        )
        self.repository.save(request, response)
        return response

    def get_analysis(self, analysis_id: str) -> AnalysisResponse | None:
        stored = self.repository.get_analysis(analysis_id)
        return None if stored is None else stored.response
