"""Structured output models for the News and Sentiment Agent."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class NewsSource(BaseModel):
    """A source article used to support the news analysis."""

    title: str = Field(description="Title of the source article.")
    publisher: str = Field(description="Publisher that provided the article.")
    published_at: str = Field(description="Publication time supplied by the source.")
    url: str = Field(description="Source article URL.")



class NewsSentimentReport(BaseModel):
    """The required structured report returned by the News and Sentiment Agent."""

    overall_sentiment: Literal[
        "Positive", "Negative", "Mixed", "Neutral", "Insufficient Data"
    ] = Field(description="Evidence-based overall sentiment from recent articles.")
    key_positive_events: list[str] = Field(
        description="Positive company events supported by the returned sources."
    )
    key_negative_events: list[str] = Field(
        description="Negative company events supported by the returned sources."
    )
    important_developments: list[str] = Field(
        description="Material company developments identified from the articles."
    )
    potential_catalysts: list[str] = Field(
        description="Possible future catalysts explicitly supported by the articles."
    )
    news_summary: str = Field(description="Concise evidence-based news summary.")
    sources_and_urls: list[NewsSource] = Field(
        description="Articles cited in the news analysis."
    )

    @field_validator("news_summary", mode="before")
    @classmethod
    def convert_summary_list_to_string(cls, value: str | list[str]) -> str:
        """Accept a model-produced list of summary sentences as one summary string."""
        if isinstance(value, list):
            return " ".join(str(item) for item in value)
        return value
    
