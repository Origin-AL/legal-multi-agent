from __future__ import annotations

import logging
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from langfuse import observe

from app.agents.facts import FactExtractionAgent
from app.agents.intake import IntakeAgent
from app.agents.reasoning import LegalReasoningAgent
from app.agents.retrieval import LegalRetrievalAgent
from app.agents.review import ReviewAgent
from app.config import settings
from app.observability import langfuse
from app.llm.factory import build_llm_provider
from app.llm.base import BaseLLMProvider
from app.models import (
    AgentError,
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

logger = logging.getLogger(__name__)

_FALLBACK_RESULTS: dict[str, dict[str, Any]] = {
    "intake_agent": {
        "matter_type": "general_legal_consultation",
        "summary": "Intake failed; defaulted to general consultation.",
    },
    "fact_extraction_agent": {
        "facts": [],
        "summary": "Fact extraction failed; no facts extracted.",
    },
    "legal_retrieval_agent": {
        "legal_basis": [],
        "summary": "Legal retrieval failed; no authorities found.",
    },
    "legal_reasoning_agent": {
        "issues": [],
        "risk_level": RiskLevel.medium,
        "suggested_actions": [],
        "draft_opinion": "分析生成失败，请稍后重试。",
        "summary": "Reasoning failed; no opinion generated.",
    },
    "review_agent": {
        "confidence": ConfidenceLevel.low,
        "review_notes": [],
        "summary": "Review failed; skipped.",
    },
}


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
        self._langfuse = langfuse
        self._intake = IntakeAgent(llm_provider)
        self._facts = FactExtractionAgent(llm_provider)
        self._retrieval = LegalRetrievalAgent(llm_provider, retriever)
        self._reasoning = LegalReasoningAgent(llm_provider)
        self._review = ReviewAgent(llm_provider)
        # Pipeline stages: list of agent groups. Groups run sequentially;
        # agents within a group run in parallel.
        self._stages: list[list] = [
            [self._intake],               # Stage 1: intake (sequential)
            [self._facts, self._retrieval],  # Stage 2: facts ‖ retrieval (parallel)
            [self._reasoning],            # Stage 3: reasoning (sequential)
            [self._review],               # Stage 4: review (sequential)
        ]

    def _run_agent(
        self,
        agent,
        request: AnalysisRequest,
        state: dict[str, object],
    ) -> tuple[dict[str, Any], AgentError | None]:
        """Run a single agent, returning (result, error). On failure, returns fallback + error."""
        try:
            result = agent.run({"request": request, "state": state})
            return result, None
        except Exception as exc:
            logger.exception("Agent %s failed: %s", agent.name, exc)
            fallback = dict(_FALLBACK_RESULTS.get(agent.name, {"summary": "Agent failed."}))
            error = AgentError(
                agent_name=agent.name,
                error_type=type(exc).__name__,
                message=str(exc)[:200],
            )
            return fallback, error

    def _build_response(
        self,
        *,
        request: AnalysisRequest,
        state: dict[str, object],
        trace: list[AgentTrace],
        coordination_log: list[CoordinationMessage],
        llm_debug: list[LLMDebugEntry],
        agent_errors: list[AgentError],
    ) -> AnalysisResponse:
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
            agent_errors=agent_errors,
            created_at=self.repository.now(),
        )
        self.repository.save(request, response)
        return response

    @observe(name="analysis_request")
    def run(self, request: AnalysisRequest) -> AnalysisResponse:
        state: dict[str, object] = {}
        trace: list[AgentTrace] = []
        coordination_log: list[CoordinationMessage] = []
        llm_debug: list[LLMDebugEntry] = []
        agent_errors: list[AgentError] = []

        for stage in self._stages:
            if len(stage) == 1:
                results = [(stage[0], *self._run_agent(stage[0], request, state))]
            else:
                with ThreadPoolExecutor(max_workers=len(stage)) as pool:
                    futures = {pool.submit(self._run_agent, agent, request, state): agent for agent in stage}
                    results = []
                    for future in as_completed(futures):
                        agent = futures[future]
                        result, error = future.result()
                        results.append((agent, result, error))

            for agent, result, error in results:
                if error:
                    agent_errors.append(error)
                summary = str(result.pop("summary", ""))
                raw_messages = result.pop("messages", [])
                raw_debug = result.pop("llm_debug", [])
                state.update(result)
                trace.append(AgentTrace(agent_name=agent.name, summary=summary))
                coordination_log.extend(CoordinationMessage(**message) for message in raw_messages)
                llm_debug.extend(LLMDebugEntry(**entry) for entry in raw_debug)

        response = self._build_response(
            request=request,
            state=state,
            trace=trace,
            coordination_log=coordination_log,
            llm_debug=llm_debug,
            agent_errors=agent_errors,
        )
        self._record_scores(response)
        langfuse.flush()
        return response

    @observe(name="analysis_request_stream")
    def run_streaming(self, request: AnalysisRequest) -> Generator[dict[str, Any], None, None]:
        """Yield one event per agent completion for SSE streaming."""
        state: dict[str, object] = {}
        trace: list[AgentTrace] = []
        coordination_log: list[CoordinationMessage] = []
        llm_debug: list[LLMDebugEntry] = []
        agent_errors: list[AgentError] = []

        _stage_keys: dict[str, list[str]] = {
            "intake_agent": ["matter_type"],
            "fact_extraction_agent": ["facts"],
            "legal_retrieval_agent": ["legal_basis"],
            "legal_reasoning_agent": ["issues", "risk_level", "suggested_actions", "draft_opinion"],
            "review_agent": ["confidence", "review_notes"],
        }

        def _process_result(agent, result, error):
            """Process an agent result, update state, yield SSE event."""
            if error:
                agent_errors.append(error)
            summary = str(result.pop("summary", ""))
            raw_messages = result.pop("messages", [])
            raw_debug = result.pop("llm_debug", [])
            state.update(result)
            trace.append(AgentTrace(agent_name=agent.name, summary=summary))
            coordination_log.extend(CoordinationMessage(**message) for message in raw_messages)
            llm_debug.extend(LLMDebugEntry(**entry) for entry in raw_debug)

            snapshot: dict[str, Any] = {"summary": summary}
            if error:
                snapshot["error"] = error.model_dump()
            for key in _stage_keys.get(agent.name, []):
                val = state.get(key)
                if isinstance(val, list):
                    snapshot[key] = [item.model_dump() if hasattr(item, "model_dump") else item for item in val]
                elif hasattr(val, "model_dump"):
                    snapshot[key] = val.model_dump()
                elif hasattr(val, "value"):
                    snapshot[key] = val.value
                else:
                    snapshot[key] = val

            return {"event": "stage", "agent": agent.name, "data": snapshot}

        for stage in self._stages:
            if len(stage) == 1:
                agent = stage[0]
                result, error = self._run_agent(agent, request, state)
                yield _process_result(agent, result, error)
            else:
                # Parallel stage: run agents concurrently, yield as each completes
                with ThreadPoolExecutor(max_workers=len(stage)) as pool:
                    futures = {pool.submit(self._run_agent, agent, request, state): agent for agent in stage}
                    for future in as_completed(futures):
                        agent = futures[future]
                        result, error = future.result()
                        yield _process_result(agent, result, error)

        response = self._build_response(
            request=request,
            state=state,
            trace=trace,
            coordination_log=coordination_log,
            llm_debug=llm_debug,
            agent_errors=agent_errors,
        )
        self._record_scores(response)
        yield {"event": "done", "data": response.model_dump()}
        langfuse.flush()

    def _record_scores(self, response: AnalysisResponse) -> None:
        """Attach evaluation scores to the current Langfuse trace."""
        _CONFIDENCE_MAP = {"high": 1.0, "medium": 0.5, "low": 0.0}
        _RISK_MAP = {"high": 1.0, "medium": 0.5, "low": 0.0}

        confidence = getattr(response.confidence, "value", str(response.confidence))
        langfuse.score_current_trace(
            name="confidence",
            value=_CONFIDENCE_MAP.get(confidence, 0.5),
            data_type="NUMERIC",
            comment=f"Review confidence: {confidence}",
        )

        risk = getattr(response.risk_level, "value", str(response.risk_level))
        langfuse.score_current_trace(
            name="risk_level",
            value=_RISK_MAP.get(risk, 0.5),
            data_type="NUMERIC",
            comment=f"Risk level: {risk}",
        )

        langfuse.score_current_trace(
            name="has_agent_errors",
            value=len(response.agent_errors) == 0,
            data_type="BOOLEAN",
            comment=f"{len(response.agent_errors)} agent errors",
        )

    def get_analysis(self, analysis_id: str) -> AnalysisResponse | None:
        stored = self.repository.get_analysis(analysis_id)
        return None if stored is None else stored.response
