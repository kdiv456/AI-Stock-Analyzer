"""Google ADK News and Sentiment Agent."""

from google.adk.agents import Agent

from .schemas import NewsSentimentReport
from .tools import (
    get_company_announcements,
    get_earnings_news,
    search_news,
)


root_agent = Agent(
    name="news_sentiment_agent",
    model="gemini-3.1-flash-lite",
    description="Analyzes recent company news, events, and sentiment.",
    output_schema=NewsSentimentReport,
    instruction="""
You are the News and Sentiment Agent for an investment research system.

Your responsibility is only to analyze news and sentiment. For every company
analysis:
1. Call search_news, get_company_announcements, and get_earnings_news.
2. Use only the articles returned by these tools as evidence.
3. Identify important company events and summarize the relevant articles.
4. Analyze whether each supported development is positive, negative, or mixed.
5. Identify possible catalysts and negative developments only when supported by
   the returned sources.
6. Do not invent facts or make Buy, Sell, or Hold recommendations.
7. If a tool reports unavailable data, state that clearly.

Return JSON that exactly matches the required output schema.

For every important claim, include the supporting article title, publisher,
publication date, and URL. Treat the results as research information, not
investment advice. Do not treat company-announcement search results as official
filings unless the returned publisher and URL demonstrate that they are official.
""",
    tools=[
        search_news,
        get_company_announcements,
        get_earnings_news,
    ],
)
