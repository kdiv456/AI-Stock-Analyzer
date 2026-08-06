"""Google ADK Manager Agent for dynamic investment-research orchestration."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

try:
    # Used by `adk web`, which loads this module as `agents.manager.agent`.
    from agents.fundamental.agent import root_agent as fundamental_agent
    from agents.news.agent import root_agent as news_sentiment_agent
    from agents.risk.agent import root_agent as risk_agent
    from agents.synthesis.agent import root_agent as synthesis_agent
    from agents.technical.agent import root_agent as technical_agent
except ModuleNotFoundError:
    # Used by `adk run agents/manager`, which loads this module as `manager.agent`.
    from fundamental.agent import root_agent as fundamental_agent
    from news.agent import root_agent as news_sentiment_agent
    from risk.agent import root_agent as risk_agent
    from synthesis.agent import root_agent as synthesis_agent
    from technical.agent import root_agent as technical_agent


fundamental_analysis_tool = AgentTool(agent=fundamental_agent)
technical_analysis_tool = AgentTool(agent=technical_agent)
news_sentiment_analysis_tool = AgentTool(agent=news_sentiment_agent)
risk_analysis_tool = AgentTool(agent=risk_agent)
synthesis_tool = AgentTool(agent=synthesis_agent)


root_agent = Agent(
    name="manager_orchestrator_agent",
    model="gemini-3.1-flash-lite",
    description="Selects specialist agents and returns a final synthesized research report.",
    instruction="""
You are the Manager / Orchestrator Agent for an investment research system.

Understand the user's request, select only the necessary specialist agents,
and always use synthesis_agent for the final response.

Routing rules:
- Complete company or investment research request: call Fundamental, Technical,
  News & Sentiment, and Risk.
- Price fall/rise, chart, trend, RSI, MACD, volatility, or support/resistance:
  call Technical and News & Sentiment.
- Financial health, revenue, earnings, debt, cash flow, margin, ROE, or
  valuation: call Fundamental.
- News, sentiment, announcements, events, catalysts, or earnings headlines:
  call News & Sentiment.
- Investment risks: call Risk.
- If the request is ambiguous or spans multiple areas, use all four specialist
  agents.

After calling the selected specialist agents, call synthesis_agent. In its
`request` argument, include:
1. The exact heading `SPECIALIST REPORTS FROM MANAGER`.
2. The user's original request.
3. The complete outputs from every specialist agent you selected.

The Synthesis Agent will produce the final report. Return that final report to
the user without adding new analysis, facts, or Buy/Sell/Hold recommendations.
""",
    tools=[
        fundamental_analysis_tool,
        technical_analysis_tool,
        news_sentiment_analysis_tool,
        risk_analysis_tool,
        synthesis_tool,
    ],
)
