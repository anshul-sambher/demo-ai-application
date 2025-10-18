"""Gamification utilities for the Gen Z focused advisory application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Quest:
    """Represents a quest that rewards the user for completing investing tasks."""

    name: str
    description: str
    xp_reward: int
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True


@dataclass
class Badge:
    """Represents an achievement badge unlocked by the user."""

    name: str
    description: str


@dataclass
class GamifiedProfile:
    """Tracks progress, quests, and achievements for a user."""

    username: str
    level: int = 1
    experience: int = 0
    quests: Dict[str, Quest] = field(default_factory=dict)
    badges: List[Badge] = field(default_factory=list)

    LEVEL_XP = 100

    def add_quest(self, quest: Quest) -> None:
        self.quests[quest.name] = quest

    def complete_quest(self, quest_name: str) -> Quest | None:
        quest = self.quests.get(quest_name)
        if quest and not quest.completed:
            quest.mark_complete()
            self.experience += quest.xp_reward
            while self.experience >= self.LEVEL_XP:
                self.level += 1
                self.experience -= self.LEVEL_XP
            if quest_name == "Read the Headlines":
                self.badges.append(
                    Badge(
                        name="Market Scout",
                        description="Awarded for keeping up with market news streaks.",
                    )
                )
        return quest

    def get_status_summary(self) -> str:
        quest_lines = []
        for quest in self.quests.values():
            status = "✓" if quest.completed else "✗"
            quest_lines.append(f"  {status} {quest.name} (+{quest.xp_reward} XP)")
        badge_lines = [f"  • {badge.name}: {badge.description}" for badge in self.badges]
        summary = [
            f"Player: {self.username}",
            f"Level: {self.level}",
            f"XP: {self.experience}/{self.LEVEL_XP}",
            "Quests:",
            *quest_lines,
            "Badges:",
            *(badge_lines or ["  • None yet. Keep exploring!"]),
        ]
        return "\n".join(summary)


def default_daily_quests() -> List[Quest]:
    """Generate the default set of daily quests."""

    return [
        Quest(
            name="Read the Headlines",
            description="Review today's WSJ and Reuters headlines to stay informed.",
            xp_reward=60,
        ),
        Quest(
            name="Plan a Micro-Investment",
            description="Choose a $10 investment idea and log it in the app.",
            xp_reward=40,
        ),
        Quest(
            name="Review Trending Assets",
            description="Check out what's trending and assess if it fits your strategy.",
            xp_reward=50,
        ),
    ]
