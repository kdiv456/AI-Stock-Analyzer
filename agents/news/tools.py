"""News-retrieval tools for the News and Sentiment Agent."""

import json
import re
from datetime import UTC, datetime

import yfinance as yf


def _plain_text(text: str | None) -> str | None:
    """Remove simple HTML markup from Yahoo Finance descriptions."""
    if text is None:
        return None
    return re.sub(r"<[^>]+>", "", text).strip()



def _format_articles(articles: list[dict]) -> list[dict]:
    """Convert Yahoo Finance article objects into a small, consistent format."""
    formatted_articles = []

    for article in articles:
        is_ticker_news = "content" in article
        content = article.get("content", article)
        provider = content.get("provider") or {}
        canonical_url = content.get("canonicalUrl") or {}
        click_through_url = content.get("clickThroughUrl") or {}
        published_at = content.get("pubDate")

        if not is_ticker_news and article.get("providerPublishTime"):
            published_at = datetime.fromtimestamp(
                article["providerPublishTime"], tz=UTC
            ).isoformat()

        formatted_articles.append(
            {
                "title": content.get("title"),
                "summary": _plain_text(
                    content.get("summary") or content.get("description")
                ),
                "published_at": published_at,
                "publisher": provider.get("displayName") or article.get("publisher"),
                "url": (
                    canonical_url.get("url")
                    or click_through_url.get("url")
                    or article.get("link")
                ),
                "content_type": content.get("contentType") or article.get("type"),
            }
        )

    return formatted_articles


def _search_yahoo_news(query: str, limit: int) -> list[dict]:
    """Search Yahoo Finance news and return normalized article records."""
    if limit < 1 or limit > 20:
        raise ValueError("limit must be between 1 and 20.")

    search = yf.Search(query, news_count=limit, max_results=1)
    return _format_articles(search.news)


def search_news(ticker: str, limit: int = 10) -> str:
    """Search recent Yahoo Finance news related to a stock ticker.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        limit: Maximum number of articles to return, from 1 to 20.
    """
    try:
        articles = _search_yahoo_news(ticker, limit)
        return json.dumps(
            {
                "ticker": ticker.upper(),
                "query": ticker,
                "source": "Yahoo Finance News",
                "articles": articles,
            },
            indent=2,
        )
    except Exception as error:
        return json.dumps({"error": f"Unable to search news for {ticker}: {error}"})


def get_company_announcements(ticker: str, limit: int = 10) -> str:
    """Search recent company-announcement news related to a stock ticker.

    Results are third-party news search results. Check each listed publisher and
    URL before treating an item as an official company announcement.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        limit: Maximum number of articles to return, from 1 to 20.
    """
    try:
        query = f"{ticker} company announcement"
        articles = _search_yahoo_news(query, limit)
        return json.dumps(
            {
                "ticker": ticker.upper(),
                "query": query,
                "source": "Yahoo Finance News",
                "source_note": (
                    "These are company-announcement search results, not verified "
                    "official company filings."
                ),
                "articles": articles,
            },
            indent=2,
        )
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to retrieve announcements for {ticker}: {error}"}
        )


def get_earnings_news(ticker: str, limit: int = 10) -> str:
    """Search recent earnings-related Yahoo Finance news for a stock ticker.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        limit: Maximum number of articles to return, from 1 to 20.
    """
    try:
        query = f"{ticker} earnings"
        articles = _search_yahoo_news(query, limit)
        return json.dumps(
            {
                "ticker": ticker.upper(),
                "query": query,
                "source": "Yahoo Finance News",
                "articles": articles,
            },
            indent=2,
        )
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to retrieve earnings news for {ticker}: {error}"}
        )
