"""Structured output models for the Risk Analysis Agent."""

from typing import Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["Low", "Moderate", "High", "Very High", "Insufficient Data"]

RiskCategoryName = Literal[
    "Valuation",
    "Financial",
    "Market",
    "Technical",
    "Regulatory",
    "Competition",
    "Industry/Sector",
    
    
    "Macroeconomic",
    "Recent News",
]
SourceAgentName = Literal[
    "Fundamental Analysis Agent",
    "Technical Analysis Agent",
    "News & Sentiment Agent",
]


class RiskCategory(BaseModel):
    """A single identified risk category and the evidence supporting it."""

    category: RiskCategoryName = Field(description="Type of investment risk assessed.")
    severity: RiskLevel = Field(description="Severity of this individual risk.")
    explanation: str = Field(description="Evidence-based explanation of the risk.")
    supporting_agents: list[SourceAgentName] = Field(
        description="Agents whose returned evidence supports this risk."
    )
    supporting_evidence: list[str] = Field(
        description="Relevant facts from the source-agent outputs."
    )


class SourceAgentEvidence(BaseModel):
    """Evidence taken from one upstream analysis agent."""

    source_agent: SourceAgentName = Field(description="Agent that supplied the evidence.")
    evidence: list[str] = Field(description="Facts used in the risk assessment.")


class RiskAnalysisReport(BaseModel):
    """The required structured report returned by the Risk Analysis Agent."""

    overall_risk_level: RiskLevel = Field(
        description="Overall evidence-based investment risk level."
    )
    risk_score: int = Field(
        ge=0,
        le=100,
        description="Evidence-based risk score: 0 is lowest risk and 100 is highest.",
    )
    risk_categories: list[RiskCategory] = Field(
        description="Risk categories that could be assessed from the source outputs."
    )
    risk_severity: str = Field(
        description="Concise explanation of the most material risk severity."
    )
    risk_explanation: str = Field(
        description="Overall explanation that balances the identified risks."
    )
    evidence_and_source_agents: list[SourceAgentEvidence] = Field(
        description="Traceable evidence supplied by the upstream agents."
    )
