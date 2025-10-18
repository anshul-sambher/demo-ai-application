"""Utilities for retrieving market data from trusted sources.

This module focuses on fetching information from sources like the Wall Street
Journal (WSJ) and other credible publishers. To remain lightweight, the module
uses publicly available RSS feeds. When the network is unavailable, a curated
fallback dataset ensures the application continues to function for demo
purposes.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

import feedparser
import requests

logger = logging.getLogger(__name__)


@dataclass
class Article:
    """Represents a market news article."""

    title: str
    link: str
    published: datetime | None
    source: str
    summary: str | None = None

    @classmethod
    def from_feed_entry(cls, entry: feedparser.FeedParserDict, *, source: str) -> "Article":
        published = None
        if "published_parsed" in entry and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        summary = None
        if "summary" in entry:
            summary = entry.summary
        return cls(
            title=entry.get("title", "Untitled"),
            link=entry.get("link", ""),
            published=published,
            source=source,
            summary=summary,
        )


RSS_SOURCES = {
    "WSJ Markets": "https://feeds.a.dj.com/rss/RSSMarketsMain",
    "WSJ Investing": "https://feeds.a.dj.com/rss/WSJcomUSBusiness",
    "Reuters Markets": "https://feeds.reuters.com/reuters/USMarkets",
    "CNBC Investing": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
}


def _parse_feed(url: str, *, source: str) -> List[Article]:
    """Parse an RSS feed into :class:`Article` instances."""

    logger.debug("Fetching RSS feed for %s", source)
    parsed = feedparser.parse(url)
    articles = [Article.from_feed_entry(entry, source=source) for entry in parsed.entries]
    logger.info("Fetched %d articles for %s", len(articles), source)
    return articles


def get_market_articles(limit_per_source: int = 5) -> List[Article]:
    """Fetch the most recent market articles from curated RSS sources."""

    collected: List[Article] = []
    for source, url in RSS_SOURCES.items():
        try:
            articles = _parse_feed(url, source=source)[:limit_per_source]
            collected.extend(articles)
        except Exception as exc:  # pragma: no cover - resilience for demo
            logger.warning("Failed to fetch %s: %s", source, exc)
    if not collected:
        collected = _load_fallback_articles()
    return collected


FALLBACK_JSON = """
[
    {
        "title": "Understanding ETFs: Building Blocks for Gen Z Portfolios",
        "link": "https://example.com/etf-guide",
        "published": "2024-01-10T14:00:00",
        "source": "Demo Dataset",
        "summary": "Exchange-traded funds (ETFs) can help Gen Z investors build diversified portfolios with low fees."
    },
    {
        "title": "How Dollar-Cost Averaging Can Reduce Stress Investing",
        "link": "https://example.com/dca",
        "published": "2024-02-05T09:30:00",
        "source": "Demo Dataset",
        "summary": "Dollar-cost averaging turns investing into a steady habit and fits nicely with gamified streak systems."
    }
]
"""


def _load_fallback_articles() -> List[Article]:
    """Return articles from a baked-in dataset when RSS feeds are unreachable."""

    data = json.loads(FALLBACK_JSON)
    fallback = []
    for raw in data:
        published = None
        if raw.get("published"):
            published = datetime.fromisoformat(raw["published"])
        fallback.append(
            Article(
                title=raw["title"],
                link=raw["link"],
                published=published,
                source=raw["source"],
                summary=raw.get("summary"),
            )
        )
    return fallback


def fetch_trending_assets(limit: int = 5) -> List[str]:
    """Fetch trending assets using a simple public API."""

    url = "https://query1.finance.yahoo.com/v1/finance/trending/US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        payload = response.json()
        quotes = payload.get("finance", {}).get("result", [{}])[0].get("quotes", [])
        symbols = [quote.get("symbol") for quote in quotes if quote.get("symbol")]
        return symbols[:limit]
    except Exception as exc:  # pragma: no cover - relies on external network
        logger.warning("Unable to fetch trending assets: %s", exc)
        return ["AAPL", "MSFT", "NVDA", "TSLA", "VOO"]
