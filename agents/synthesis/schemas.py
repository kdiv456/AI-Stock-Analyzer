"""Structured output models for the Synthesis Agent."""

from pydantic import BaseModel, Field


class SynthesisEvidence(BaseModel):
    """One piece of upstream evidence used in the final report."""

    source_agent: str = Field(
        description="Specialist agent that supplied the evidence."
    )
    evidence: str = Field(
        description="Specific fact or conclusion supplied by that agent."
    )
    source_url: str | None = Field(
        default=None,
        description="Article URL when the source evidence is news-based; otherwise null.",
    )


class SynthesisReport(BaseModel):
    """The required final investment research report."""

    company_overview: str = Field(description="Brief overview of the company.")
    fundamental_analysis: str = Field(
        description="Evidence-based summary of the Fundamental Agent output."
    )
    technical_analysis: str = Field(
        description="Evidence-based summary of the Technical Agent output."
    )
    news_and_sentiment: str = Field(
        description="Evidence-based summary of the News and Sentiment Agent output."
    )
    risk_analysis: str = Field(
        description="Evidence-based summary of the Risk Agent output."
    )
    bull_case: list[str] = Field(
        description="Positive factors supported by the specialist outputs."
    )
    bear_case: list[str] = Field(
        description="Negative factors and risks supported by the specialist outputs."
    )
    key_factors_to_monitor: list[str] = Field(
        description="Important developments or metrics to monitor."
    )
    overall_assessment: str = Field(
        description="Balanced overall assessment without Buy/Sell/Hold advice."
    )
    confidence_level: str = Field(
        description="Confidence level based on the completeness and agreement of evidence."
    )
    evidence_and_sources: list[SynthesisEvidence] = Field(
        description="Traceable evidence and sources used in the report."
    )
