"""Runtime safety checks for the user-facing Manager Agent."""

from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types


PERSONALIZED_ADVICE_TERMS = (
    "for my portfolio",
    "for my retirement",
    "for my pension",
    "based on my salary",
    "based on my income",
    "based on my savings",
    "how much should i invest",
    "how much money should i invest",
    "what should i buy with",
)

TRADE_EXECUTION_TERMS = (
    "place a trade",
    "execute a trade",
    "buy shares for me",
    "sell shares for me",
    "place an order",
)


def _request_text(llm_request: LlmRequest) -> str:
    """Extract user-visible text from the model request."""
    return " ".join(
        part.text or ""
        for content in llm_request.contents
        for part in content.parts or []
    ).lower()


def block_personalized_financial_advice(
    callback_context, llm_request: LlmRequest
) -> LlmResponse | None:
    """Block personalized financial advice and trade-execution requests."""
    request_text = _request_text(llm_request)

    if any(term in request_text for term in PERSONALIZED_ADVICE_TERMS):
        message = (
            "I can provide general, evidence-based investment research, but I "
            "cannot provide personalized financial advice or tell you how much "
            "to invest. You can ask for a research report on a company instead."
        )
    elif any(term in request_text for term in TRADE_EXECUTION_TERMS):
        message = (
            "I cannot place, execute, or instruct a trade. I can provide a "
            "research report with fundamental, technical, news, and risk "
            "analysis for a ticker."
        )
    else:
        return None

    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=message)])
    )
