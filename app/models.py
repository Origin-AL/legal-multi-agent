from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MatterType(str, Enum):
    general_legal_consultation = "general_legal_consultation"
    contract_review = "contract_review"
    labor_dispute = "labor_dispute"
    compliance_review = "compliance_review"
    litigation_strategy = "litigation_strategy"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ConfidenceLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class CaseMaterial(BaseModel):
    title: str = Field(..., max_length=200, description="Material title, such as contract or complaint name.")
    content: str = Field(..., max_length=50_000, description="Full text or extracted text content.")


class AnalysisRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=10_000)
    case_type_hint: str | None = Field(None, max_length=200)
    materials: list[CaseMaterial] = Field(default_factory=list, max_length=20)
    session_id: str | None = Field(None, max_length=200, description="Frontend conversation session ID for Langfuse Sessions grouping.")


class AgentTrace(BaseModel):
    agent_name: str
    summary: str


class LLMDebugEntry(BaseModel):
    agent_name: str
    task: str
    output: dict | list | str


class CoordinationMessage(BaseModel):
    sender: str
    recipient: str
    content: str


class Citation(BaseModel):
    source_type: str
    title: str
    excerpt: str
    reference_id: str
    score: float | None = None


class IssueItem(BaseModel):
    title: str
    analysis: str
    risk_level: RiskLevel
    citations: list[Citation] = Field(default_factory=list)


class AgentError(BaseModel):
    agent_name: str
    error_type: str
    message: str


class AnalysisResponse(BaseModel):
    analysis_id: str
    case_id: str
    matter_type: MatterType = MatterType.general_legal_consultation
    risk_level: RiskLevel
    confidence: ConfidenceLevel
    facts: list[str]
    legal_basis: list[Citation]
    issues: list[IssueItem]
    suggested_actions: list[str]
    draft_opinion: str
    review_notes: list[str]
    coordination_log: list[CoordinationMessage]
    trace: list[AgentTrace]
    llm_debug: list[LLMDebugEntry] = Field(default_factory=list)
    agent_errors: list[AgentError] = Field(default_factory=list)
    created_at: datetime


class StoredAnalysis(BaseModel):
    analysis_id: str
    case_id: str
    request: AnalysisRequest
    response: AnalysisResponse
    created_at: datetime


class KnowledgeDocument(BaseModel):
    reference_id: str
    source_type: str
    title: str
    excerpt: str
    body: str
    tags: list[str] = Field(default_factory=list)
    law_category: str = ""
    layer_type: str = "statute"
