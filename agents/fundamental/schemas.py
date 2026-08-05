"""Structured output models for the Fundamental Analysis Agent."""

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """One factual item supporting a conclusion in the report."""

    metric: str = Field(description="The financial metric used as evidence.")
    value: str = Field(description="The metric value exactly as reported by the tool.")
    reporting_period: str = Field(
        description="The reporting date or period associated with the metric."
    )
    source: str = Field(description="The source that provided the metric.")



class FundamentalAnalysisReport(BaseModel):
    """The required structured report returned by the Fundamental Agent."""

    company_overview: str = Field(description="Brief description of the company.")
    growth: str = Field(description="Analysis of revenue and earnings growth.")
    profitability: str = Field(description="Analysis of margins, earnings, and ROE.")
    financial_health: str = Field(description="Analysis of assets, liabilities, debt, and cash.")
    valuation: str = Field(description="Analysis of P/E, P/S, and P/B when available.")
    fundamental_score: int = Field(
        ge=0,
        le=100,
        description="Evidence-based fundamental score from 0 to 100.",
    )
    score_rationale: str = Field(
        description="Explanation for the fundamental score based on returned data."
    )
    summary: str = Field(description="Concise overall fundamental assessment.")
    evidence_and_data_sources: list[EvidenceItem] = Field(
        description="Metrics and sources supporting the report's conclusions."
    )
