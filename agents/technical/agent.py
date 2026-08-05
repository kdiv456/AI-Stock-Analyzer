"""Google ADK Technical Analysis Agent."""

from google.adk.agents import Agent

from .schemas import TechnicalAnalysisReport
from .tools import (
    calculate_bollinger_bands,
    calculate_ema,
    calculate_macd,
    calculate_rsi,
    calculate_sma,
    calculate_volatility,
    detect_support_resistance,
    get_current_price,
    get_historical_prices,
)


root_agent = Agent(
    name="technical_analysis_agent",
    model="gemini-3.1-flash-lite",
    description="Analyzes a stock's price action and technical indicators.",
    output_schema=TechnicalAnalysisReport,
    instruction="""
You are the Technical Analysis Agent for an investment research system.

Your responsibility is only technical analysis. For each company analysis:
1. Call get_current_price and get_historical_prices.
2. Call calculate_sma, calculate_ema, calculate_rsi, calculate_macd,
   calculate_bollinger_bands, calculate_volatility, and
   detect_support_resistance.
3. Use the calculated values returned by the tools. Do not perform or invent
   indicator calculations yourself.
4. If a tool reports unavailable data, state that clearly.
5. Do not give Buy, Sell, or Hold recommendations.

Return JSON that exactly matches the required output schema.

In the evidence section, identify the indicator, its value, calculation date,
and data source for every important conclusion. Treat technical analysis as
research information, not investment advice.
""",
    tools=[
        get_current_price,
        get_historical_prices,
        calculate_sma,
        calculate_ema,
        calculate_rsi,
        calculate_macd,
        calculate_bollinger_bands,
        calculate_volatility,
        detect_support_resistance,
    ],
)
