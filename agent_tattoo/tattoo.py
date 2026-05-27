"""Core Tattoo data model."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class Visibility(Enum):
    """Who can see a tattoo."""

    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"
    HIDDEN = "hidden"


class TattooCategory(Enum):
    """Broad category of tattoo."""

    MILESTONE = "milestone"
    ACHIEVEMENT = "achievement"
    CAPABILITY = "capability"
    FAILURE = "failure"
    EXPERIENCE = "experience"
    IDENTITY = "identity"


@dataclass
class Tattoo:
    """A persistent behavioral marker earned by an agent.

    Tattoos are immutable records of something that happened — a skill
    demonstrated, a mistake made, a milestone reached. They accumulate
    over an agent's lifetime and form a kind of scar tissue / badge
    collection that tells the agent's story.

    ``fade_level`` goes from 0.0 (fresh, vivid) to 1.0 (ancient, faded).
    Older tattoos fade but never disappear.
    """

    name: str
    description: str
    category: TattooCategory = TattooCategory.EXPERIENCE
    visibility: Visibility = Visibility.PUBLIC
    earned_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fade_level: float = 0.0
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Tattoo name must not be empty")
        if not 0.0 <= self.fade_level <= 1.0:
            raise ValueError("fade_level must be between 0.0 and 1.0")

    @property
    def age_days(self) -> float:
        """Days since the tattoo was earned."""
        delta = datetime.now(timezone.utc) - self.earned_at
        return delta.total_seconds() / 86400

    def fade(self, amount: float = 0.01) -> "Tattoo":
        """Return a copy with increased fade level (capped at 1.0)."""
        new_fade = min(1.0, self.fade_level + amount)
        return Tattoo(
            name=self.name,
            description=self.description,
            category=self.category,
            visibility=self.visibility,
            earned_at=self.earned_at,
            fade_level=new_fade,
            id=self.id,
            metadata=self.metadata.copy(),
        )

    def is_visible_to(self, viewer: str = "public") -> bool:
        """Check whether this tattoo is visible to a given viewer role."""
        if viewer == "owner":
            return True
        visibility_map = {
            Visibility.PUBLIC: True,
            Visibility.INTERNAL: viewer in ("internal", "admin"),
            Visibility.PRIVATE: viewer == "admin",
            Visibility.HIDDEN: False,
        }
        return visibility_map.get(self.visibility, False)

    def to_dict(self) -> dict:
        """Serialize to a plain dict."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "visibility": self.visibility.value,
            "earned_at": self.earned_at.isoformat(),
            "fade_level": self.fade_level,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tattoo":
        """Deserialize from a plain dict."""
        data = dict(data)
        if "category" in data and isinstance(data["category"], str):
            data["category"] = TattooCategory(data["category"])
        if "visibility" in data and isinstance(data["visibility"], str):
            data["visibility"] = Visibility(data["visibility"])
        if "earned_at" in data and isinstance(data["earned_at"], str):
            data["earned_at"] = datetime.fromisoformat(data["earned_at"])
        return cls(**data)
