"""Google ADK Synthesis Agent for the final investment research report."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .guardrails import block_investment_recommendations
from .schemas import SynthesisReport

try:
    # Used by `adk web`, which loads this module as `agents.synthesis.agent`.
    from agents.fundamental.agent import root_agent as fundamental_agent
    from agents.news.agent import root_agent as news_sentiment_agent
    from agents.risk.agent import root_agent as risk_agent
    from agents.technical.agent import root_agent as technical_agent
except ModuleNotFoundError:
    # Used by `adk run agents/synthesis`, which loads this module as `synthesis.agent`.
    from fundamental.agent import root_agent as fundamental_agent
    from news.agent import root_agent as news_sentiment_agent
    from risk.agent import root_agent as risk_agent
    from technical.agent import root_agent as technical_agent


fundamental_analysis_tool = AgentTool(agent=fundamental_agent)
technical_analysis_tool = AgentTool(agent=technical_agent)
news_sentiment_analysis_tool = AgentTool(agent=news_sentiment_agent)
risk_analysis_tool = AgentTool(agent=risk_agent)


root_agent = Agent(
    name="synthesis_agent",
    model="gemini-3.1-flash-lite",
    description="Combines specialist evidence into an explainable investment research report.",
    output_schema=SynthesisReport,
    before_tool_callback=block_investment_recommendations,
    instruction="""
You are the Synthesis Agent for an investment research system.

Your responsibility is to combine specialist analysis into one explainable
investment research report. For every company analysis:
1. If the request contains "SPECIALIST REPORTS FROM MANAGER", use only the
   reports included in that request. Do not call additional specialist agents.
2. Otherwise, call fundamental_analysis_agent, technical_analysis_agent,
   news_sentiment_agent, and risk_analysis_agent with the user's request.
3. Synthesize only evidence returned by those agents. Do not collect new data,
   independently calculate metrics, or invent facts.
4. Clearly identify conflicts or uncertainty in the source-agent outputs.
5. Build the bull case and bear case only from the supported evidence.
6. Give an overall assessment, not a Buy, Sell, or Hold recommendation.

If a report was not supplied by the Manager, state that it was not requested
or not available; do not infer its conclusions.

Return JSON that exactly matches the required output schema.

For every material conclusion, cite the source agent and the evidence it
provided. Treat the report as research information, not investment advice.
""",
    tools=[
        fundamental_analysis_tool,
        technical_analysis_tool,
        news_sentiment_analysis_tool,
        risk_analysis_tool,
    ],
)
