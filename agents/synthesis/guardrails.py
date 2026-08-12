"""Runtime safety checks for the final investment research report."""

import re
from typing import Any

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.set_model_response_tool import SetModelResponseTool


RECOMMENDATION_PATTERNS = (
    r"\b(?:strong\s+)?(?:buy|sell|hold)\s+(?:rating|recommendation)\b",
    r"\b(?:recommend|advise|suggest)\s+(?:buying|selling|holding|to\s+(?:buy|sell|hold))\b",
    r"\b(?:you|investors?)\s+should\s+(?:buy|sell|hold)\b",
    r"\b(?:buy|sell|hold)\s+(?:this|the)\s+(?:stock|share)\b",
)


def _flatten_text(value: Any) -> str:
    """Collect all text values from a structured model response."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)
    return ""


def block_investment_recommendations(
    tool: BaseTool, args: dict[str, Any], tool_context
) -> dict[str, str] | None:
    """Block unsafe structured final reports before ADK returns them to a user."""
    if not isinstance(tool, SetModelResponseTool):
        return None

    report_text = _flatten_text(args)
    if any(
        re.search(pattern, report_text, flags=re.IGNORECASE)
        for pattern in RECOMMENDATION_PATTERNS
    ):
        return {
            "error": (
                "Blocked by research-only guardrail: revise the report to give "
                "a balanced overall assessment without a Buy/Sell/Hold "
                "recommendation."
            )
        }

    return None
