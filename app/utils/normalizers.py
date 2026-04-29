from __future__ import annotations

from app.models import ConfidenceLevel, MatterType, RiskLevel


MATTER_TYPE_ALIASES = {
    "general_legal_consultation": MatterType.general_legal_consultation,
    "general": MatterType.general_legal_consultation,
    "legal_consultation": MatterType.general_legal_consultation,
    "\u6cd5\u5f8b\u54a8\u8be2": MatterType.general_legal_consultation,
    "\u6cd5\u5f8b\u95ee\u7b54": MatterType.general_legal_consultation,
    "contract_review": MatterType.contract_review,
    "contract": MatterType.contract_review,
    "\u5408\u540c\u5ba1\u67e5": MatterType.contract_review,
    "\u5408\u540c\u5206\u6790": MatterType.contract_review,
    "labor_dispute": MatterType.labor_dispute,
    "labor": MatterType.labor_dispute,
    "\u52b3\u52a8\u4e89\u8bae": MatterType.labor_dispute,
    "compliance_review": MatterType.compliance_review,
    "compliance": MatterType.compliance_review,
    "\u5408\u89c4\u5ba1\u67e5": MatterType.compliance_review,
    "\u5408\u89c4": MatterType.compliance_review,
    "litigation_strategy": MatterType.litigation_strategy,
    "litigation": MatterType.litigation_strategy,
    "\u8bc9\u8bbc\u7b56\u7565": MatterType.litigation_strategy,
    "\u8bc9\u8bbc\u5206\u6790": MatterType.litigation_strategy,
}


RISK_ALIASES = {
    "low": RiskLevel.low,
    "medium": RiskLevel.medium,
    "high": RiskLevel.high,
    "\u4f4e": RiskLevel.low,
    "\u4f4e\u98ce\u9669": RiskLevel.low,
    "\u4e2d": RiskLevel.medium,
    "\u4e2d\u7b49": RiskLevel.medium,
    "\u4e2d\u98ce\u9669": RiskLevel.medium,
    "\u4e2d\u7b49\u98ce\u9669": RiskLevel.medium,
    "\u9ad8": RiskLevel.high,
    "\u9ad8\u98ce\u9669": RiskLevel.high,
}

CONFIDENCE_ALIASES = {
    "low": ConfidenceLevel.low,
    "medium": ConfidenceLevel.medium,
    "high": ConfidenceLevel.high,
    "\u4f4e": ConfidenceLevel.low,
    "\u4f4e\u7f6e\u4fe1": ConfidenceLevel.low,
    "\u4f4e\u7f6e\u4fe1\u5ea6": ConfidenceLevel.low,
    "\u4e2d": ConfidenceLevel.medium,
    "\u4e2d\u7b49": ConfidenceLevel.medium,
    "\u4e2d\u7b49\u7f6e\u4fe1": ConfidenceLevel.medium,
    "\u4e2d\u7b49\u7f6e\u4fe1\u5ea6": ConfidenceLevel.medium,
    "\u9ad8": ConfidenceLevel.high,
    "\u9ad8\u7f6e\u4fe1": ConfidenceLevel.high,
    "\u9ad8\u7f6e\u4fe1\u5ea6": ConfidenceLevel.high,
}


def normalize_risk_level(value: str | RiskLevel | None) -> RiskLevel:
    if isinstance(value, RiskLevel):
        return value
    key = (value or "medium").strip().lower()
    return RISK_ALIASES.get(key, RiskLevel.medium)


def normalize_confidence_level(value: str | ConfidenceLevel | None) -> ConfidenceLevel:
    if isinstance(value, ConfidenceLevel):
        return value
    key = (value or "medium").strip().lower()
    return CONFIDENCE_ALIASES.get(key, ConfidenceLevel.medium)


def normalize_matter_type(value: str | MatterType | None) -> MatterType:
    if isinstance(value, MatterType):
        return value
    raw = (value or "general_legal_consultation").strip()
    return MATTER_TYPE_ALIASES.get(raw, MATTER_TYPE_ALIASES.get(raw.lower(), MatterType.general_legal_consultation))
