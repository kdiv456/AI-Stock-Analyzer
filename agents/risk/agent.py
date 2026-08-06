"""Google ADK Risk Analysis Agent."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .schemas import RiskAnalysisReport

try:
    # Used by `adk web`, which loads this module as `agents.risk.agent`.
    from agents.fundamental.agent import root_agent as fundamental_agent
    from agents.news.agent import root_agent as news_sentiment_agent
    from agents.technical.agent import root_agent as technical_agent
except ModuleNotFoundError:
    # Used by `adk run agents/risk`, which loads this module as `risk.agent`.
    from fundamental.agent import root_agent as fundamental_agent
    from news.agent import root_agent as news_sentiment_agent
    from technical.agent import root_agent as technical_agent


fundamental_analysis_tool = AgentTool(agent=fundamental_agent)
technical_analysis_tool = AgentTool(agent=technical_agent)
news_sentiment_analysis_tool = AgentTool(agent=news_sentiment_agent)


root_agent = Agent(
    name="risk_analysis_agent",
    model="gemini-3.1-flash-lite",
    description="Identifies investment risks from fundamental, technical, and news evidence.",
    output_schema=RiskAnalysisReport,
    instruction="""
You are the Risk Analysis Agent for an investment research system.

Your responsibility is to identify and explain investment risks. For every
company analysis:
1. Call fundamental_analysis_agent, technical_analysis_agent, and
   news_sentiment_agent with the user's request.
2. Use only the evidence returned by those agents.
3. Challenge positive conclusions when the returned data also supports a risk.
4. Do not collect independent market data, invent facts, or make Buy, Sell, or
   Hold recommendations.
5. State when a risk category cannot be assessed because evidence is missing.

Assess these risk categories when evidence is available:
- Valuation risk
- Financial risk
- Market risk
- Technical risk, including price trend, volatility, and indicator risk
- Regulatory risk
- Competition risk
- Industry or sector risk
- Macroeconomic risk
- Risks identified by recent news

Return JSON that exactly matches the required output schema.

The risk score must be an integer from 0 to 100, where 0 is the lowest risk
and 100 is the highest risk. For every risk, state which source agent and
which returned evidence supports it. Treat this as research information, not
investment advice.
""",
    tools=[
        fundamental_analysis_tool,
        technical_analysis_tool,
        news_sentiment_analysis_tool,
    ],
)
