"""Command line entry point for the Gen Z investment advisory application."""

from __future__ import annotations

import argparse
import logging
from typing import List

from .advisor import AdvisoryInsight, generate_advisory_playbook, summarize_articles
from .data_sources import Article, fetch_trending_assets, get_market_articles
from .gamification import GamifiedProfile, default_daily_quests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gamified investment advisor with live market insights",
    )
    parser.add_argument(
        "--username",
        default="Player1",
        help="Name for the gamified profile.",
    )
    parser.add_argument(
        "--risk-profile",
        choices=["Starter", "Confident", "Adventurer"],
        default="Starter",
        help="Select the style of advice you want to receive.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of articles per source to display.",
    )
    return parser


def format_articles(articles: List[Article]) -> str:
    lines = ["Latest Headlines:"]
    for article in articles:
        published = article.published.isoformat() if article.published else "Unknown time"
        summary = f"    {article.summary}" if article.summary else ""
        lines.append(f"- {article.title} [{article.source}] ({published})")
        if summary:
            lines.append(summary)
        lines.append(f"    Link: {article.link}")
    return "\n".join(lines)


def format_insights(insights: List[AdvisoryInsight]) -> str:
    lines: List[str] = []
    for insight in insights:
        lines.append(f"\n=== {insight.title} ===")
        lines.append(insight.body)
    return "\n".join(lines)


def run(username: str, risk_profile: str, limit: int) -> str:
    profile = GamifiedProfile(username=username)
    for quest in default_daily_quests():
        profile.add_quest(quest)

    articles = get_market_articles(limit_per_source=limit)
    article_summary = summarize_articles(articles, limit=limit * 2)

    profile.complete_quest("Read the Headlines")

    trending_assets = fetch_trending_assets(limit=5)
    profile.complete_quest("Review Trending Assets")

    insights = generate_advisory_playbook(
        risk_profile=risk_profile,
        trending_assets=trending_assets,
        quests_completed=[name for name, quest in profile.quests.items() if quest.completed],
    )

    output_sections = [
        profile.get_status_summary(),
        "",
        format_articles(articles),
        "",
        "Quick Headlines:",
        *article_summary,
        format_insights(insights),
    ]

    return "\n".join(output_sections)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    report = run(args.username, args.risk_profile, args.limit)
    print(report)


if __name__ == "__main__":
    main()
