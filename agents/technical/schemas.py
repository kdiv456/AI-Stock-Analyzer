"""Structured output models for the Technical Analysis Agent."""

from pydantic import BaseModel, Field


class TechnicalEvidenceItem(BaseModel):
    """One indicator value supporting a technical conclusion."""

    indicator: str = Field(description="Indicator or market-data metric used as evidence.")
    value: str = Field(description="Value exactly as returned by a tool.")
    calculation_date: str = Field(
        description="Date associated with the price or calculated indicator."
    )
    source: str = Field(description="Data source that provided the evidence.")



class TechnicalAnalysisReport(BaseModel):
    """The required structured report returned by the Technical Agent."""

    price_trend: str = Field(description="Analysis of recent price movement.")
    moving_averages: str = Field(description="Interpretation of SMA and EMA results.")
    rsi: str = Field(description="Interpretation of the RSI result.")
    macd: str = Field(description="Interpretation of MACD, signal line, and histogram.")
    bollinger_bands: str = Field(
        description="Interpretation of price relative to Bollinger Bands."
    )
    volume: str = Field(description="Analysis of the available trading-volume data.")
    volatility: str = Field(description="Interpretation of historical volatility.")
    support_and_resistance: str = Field(
        description="Interpretation of the calculated support and resistance levels."
    )
    technical_summary: str = Field(description="Concise overall technical assessment.")
    evidence_and_data_sources: list[TechnicalEvidenceItem] = Field(
        description="Indicator values and sources supporting the report."
    )
    