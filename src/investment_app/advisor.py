"""Core logic for the Gen Z investment advisory experience."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .data_sources import Article

RISK_PROFILES = {
    "Starter": {
        "description": "Perfect for new investors building habits with ETFs and robo-advisors.",
        "focus": ["Low-cost index ETFs", "Automated recurring contributions", "Emergency fund"],
    },
    "Confident": {
        "description": "For investors comfortable with moderate risk and thematic bets.",
        "focus": ["Thematic ETFs", "Blue-chip dividend stocks", "Sustainable investing"],
    },
    "Adventurer": {
        "description": "High energy investors willing to explore crypto and high-growth tech.",
        "focus": ["Crypto dollar-cost averaging", "Options for hedging", "Growth tech equities"],
    },
}


@dataclass
class AdvisoryInsight:
    """Structured insight combining market news and gamified advice."""

    title: str
    body: str


def summarize_articles(articles: Iterable[Article], limit: int = 5) -> List[str]:
    """Condense a list of articles into quick-hit summaries."""

    lines: List[str] = []
    for idx, article in enumerate(articles):
        if idx >= limit:
            break
        headline = article.title.strip()
        source = article.source
        lines.append(f"• {headline} ({source})")
    return lines


def generate_advisory_playbook(
    *,
    risk_profile: str,
    trending_assets: Iterable[str],
    quests_completed: List[str] | None = None,
) -> List[AdvisoryInsight]:
    """Create actionable guidance tailored to the user's style."""

    quests_completed = quests_completed or []
    profile = RISK_PROFILES.get(risk_profile, RISK_PROFILES["Starter"])
    insights = [
        AdvisoryInsight(
            title=f"{risk_profile} Investor Playbook",
            body="\n".join(
                [profile["description"], "", "Focus areas:"]
                + [f"  - {focus}" for focus in profile["focus"]]
            ),
        )
    ]

    if trending_assets:
        ideas = [f"  - Research how {symbol} fits your strategy." for symbol in trending_assets]
        insights.append(
            AdvisoryInsight(
                title="Trending Asset Radar",
                body="Keep tabs on the buzz, but align it with your plan:\n" + "\n".join(ideas),
            )
        )

    if quests_completed:
        streak_body = "You completed: " + ", ".join(quests_completed)
        streak_body += "\nMaintain your streak to unlock exclusive badges and higher-tier insights."
        insights.append(
            AdvisoryInsight(title="XP Streak Bonus", body=streak_body)
        )

    return insights
