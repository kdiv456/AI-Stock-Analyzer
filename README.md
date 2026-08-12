# AI Stock Analyzer

## Project Overview

AI Stock Analyzer is an investment research framework built with Google ADK and `yfinance`. It orchestrates specialist agents for fundamental analysis, technical analysis, news and sentiment review, risk assessment, and final report synthesis. The system is designed to generate evidence-based JSON research reports while enforcing research-only guardrails that block personalized advice, trade execution requests, and explicit buy/sell/hold recommendations.

## Key Features

- Fundamental company analysis using financial statements and ratios
- Technical indicator analysis using price history, moving averages, RSI, MACD, Bollinger Bands, volatility, and support/resistance
- News and sentiment analysis from Yahoo Finance news search results
- Risk analysis combining evidence from fundamental, technical, and news agents
- Manager orchestrator that routes requests to the appropriate specialist agents
- Final synthesis agent that combines specialist outputs into a cohesive research report
- Guardrails to prevent personalized financial advice and explicit trade recommendations

## Architecture

The repository is organized around ADK agents. Each agent is responsible for one research domain, with tools that fetch or calculate structured data.

### Agents

- `agents/manager`: Orchestrator agent that selects specialist agents and returns the final synthesized report
- `agents/fundamental`: Fundamental analysis agent and supporting financial data tools
- `agents/technical`: Technical analysis agent and indicator calculation tools
- `agents/news`: News and sentiment analysis agent and news search tools
- `agents/risk`: Risk analysis agent that synthesizes risk categories from other agents
- `agents/synthesis`: Final synthesis agent that produces the combined report

### Guardrails

- `agents/manager/guardrails.py`: blocks requests asking for personalized advice or trade execution
- `agents/synthesis/guardrails.py`: blocks final responses containing explicit Buy/Sell/Hold recommendation language

### Output Schemas

Each specialist agent returns structured JSON data validated by Pydantic models in `agents/*/schemas.py`.

- Fundamental agent: `agents/fundamental/schemas.py`
- Technical agent: `agents/technical/schemas.py`
- News agent: `agents/news/schemas.py`
- Risk agent: `agents/risk/schemas.py`
- Synthesis agent: `agents/synthesis/schemas.py`

## Data Sources

This project relies primarily on Yahoo Finance data via the `yfinance` library:

- Company profile, business summary, sector, industry
- Income statements and balance sheets
- Financial ratios
- Current price and historical daily prices
- News articles, company announcements, and earnings news

## Requirements

- Python 3.13 (the repository includes a local virtual environment under `myenv/`)
- `yfinance`
- `pydantic`
- `google-adk`
- `google-genai`

> Note: There is no `requirements.txt` file in this repository, so install the dependencies manually or create your own requirements file from the imports listed above.

## Setup

1. Activate the project Python environment:

```bash
source myenv/bin/activate
```

2. Install dependencies if they are not already available in `myenv`:

```bash
pip install yfinance pydantic google-adk google-genai
```

3. Create or update `.env` with your Google API key:

```bash
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

4. Avoid committing secrets. Keep `.env` local and excluded from version control.

## Usage

### Run the manager agent

The manager agent is the entrypoint for user-facing research requests. It routes the request to the appropriate specialist agents and then calls the synthesis agent.

```bash
adk run agents/manager
```

### Run a web interface

This repository is also compatible with ADK web serving, as indicated by the last command in the repository state.

```bash
adk web --port 8000
```

### Example request

Ask the manager agent for a company research report, for example:

- "Provide a research summary of Apple Inc. that includes fundamentals, technicals, news sentiment, and risks."
- "Analyze Microsoft stock from a fundamental and technical perspective."

### Using specialist agents directly

If you want to run a specific agent instead of the manager orchestration, use the agent module path directly:

```bash
adk run agents/fundamental
adk run agents/technical
adk run agents/news
adk run agents/risk
adk run agents/synthesis
```

> Note: The exact CLI arguments depend on your installed ADK version and runtime environment.

## Project Structure

```
README.md
agents/
  fundamental/
    agent.py
    schemas.py
    tools.py
  technical/
    agent.py
    schemas.py
    tools.py
  news/
    agent.py
    schemas.py
    tools.py
  risk/
    agent.py
    schemas.py
  synthesis/
    agent.py
    guardrails.py
    schemas.py
  manager/
    agent.py
    guardrails.py
myenv/
.env
.gitignore
```

### What each folder contains

- `agent.py`: the ADK agent definition, including model, instructions, tools, and output schema
- `schemas.py`: Pydantic models defining the agent's structured output
- `tools.py`: fetchers and calculators used by the agent
- `guardrails.py`: runtime safety checks to enforce research-only behavior

## How It Works

1. The manager agent receives a user request.
2. It chooses the specialist agents required by the request using routing rules.
3. Each specialist agent calls its supporting tools and returns structured JSON evidence.
4. The risk agent analyzes the specialist outputs to identify risk categories.
5. The synthesis agent combines the specialist reports into the final research report.
6. Guardrails validate the content and block explicit investment recommendations.

## Extending the Project

To add new capabilities:

1. Add or extend a tool in the relevant `agents/*/tools.py` file.
2. Update the corresponding `schemas.py` model to include new output fields.
3. Update the agent's `agent.py` instruction and tool list to use the new tool.
4. If the new capability spans multiple domains, update `agents/manager/agent.py` routing rules.

## Notes and Considerations

- This project is research-oriented and intentionally avoids personalized financial advice.
- The classification and explanation are only as accurate as the underlying data returned by Yahoo Finance and the ADK model.
- The system uses structured JSON outputs, which makes it easier to validate and integrate with downstream automation.
- If a tool cannot fetch data, the agent should explicitly report unavailable data rather than guessing.

## Troubleshooting

- If `adk` is not found, make sure the environment is activated and the ADK CLI is installed.
- If data fetching fails, confirm that `yfinance` can access Yahoo Finance from your network.
- If the manager returns guardrail responses, reframe the request as general research rather than asking for trades, portfolio guidance, or investment amounts.

## Security

- Do not commit `.env` or any API keys to source control.
- Use your own `GOOGLE_API_KEY` and keep it private.

---

If you want, I can also help create a `requirements.txt` file and add a sample startup script to make the project easier to run.
