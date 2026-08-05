"""Google ADK Fundamental Analysis Agent."""

from google.adk.agents import Agent

from .schemas import FundamentalAnalysisReport
from .tools import (
    get_balance_sheet,
    get_company_info,
    get_financial_ratios,
    get_income_statement,
)


root_agent = Agent(
    name="fundamental_analysis_agent",
    model="gemini-3.1-flash-lite",
    description="Analyzes a company's financial fundamentals using financial data tools.",
    output_schema=FundamentalAnalysisReport,
    instruction="""
You are the Fundamental Analysis Agent for an investment research system.

Your responsibility is only fundamental analysis. For every company analysis:
1. Call get_company_info, get_income_statement, get_balance_sheet, and
   get_financial_ratios with the user's ticker.
2. Base every conclusion only on the data returned by those tools.
3. Do not invent data. If a metric is unavailable, state that it is unavailable.
4. Do not give a Buy, Sell, or Hold recommendation.

Return JSON that exactly matches the required output schema. The fundamental
score must be an integer from 0 to 100 and must include a score rationale.

In "Evidence and Data Sources", name the metric and reporting date used for
each important conclusion. Treat Yahoo Finance data as a data source, not as
investment advice.
""",
    tools=[
        get_company_info,
        get_income_statement,
        get_balance_sheet,
        get_financial_ratios,
    ],
)
