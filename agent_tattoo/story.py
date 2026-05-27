"""TattooStory — connect tattoos into narratives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .tattoo import Tattoo
from .collection import TattooCollection


@dataclass
class StoryEntry:
    """A single narrative beat tied to one or more tattoos."""

    timestamp: datetime
    narrative: str
    tattoo_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "narrative": self.narrative,
            "tattoo_ids": self.tattoo_ids,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StoryEntry":
        d = dict(data)
        if "timestamp" in d and isinstance(d["timestamp"], str):
            d["timestamp"] = datetime.fromisoformat(d["timestamp"])
        return cls(**d)


@dataclass
class TattooStory:
    """Weaves tattoos into chronological narratives.

    A story is a sequence of entries, each tying a narrative blurb
    to the tattoos that were earned (or were prominent) at that
    moment. Think of it as an agent's autobiography told through
    its scars.
    """

    collection: TattooCollection
    _entries: List[StoryEntry] = field(default_factory=list)

    def add_entry(
        self,
        narrative: str,
        tattoos: Optional[List[Tattoo]] = None,
        tags: Optional[List[str]] = None,
    ) -> StoryEntry:
        """Append a narrative entry linked to specific tattoos."""
        tids = [t.id for t in (tattoos or [])]
        entry = StoryEntry(
            timestamp=datetime.now(),
            narrative=narrative,
            tattoo_ids=tids,
            tags=tags or [],
        )
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> List[StoryEntry]:
        return list(self._entries)

    def timeline(self) -> List[dict]:
        """Return entries enriched with the actual tattoo objects."""
        result: List[dict] = []
        for entry in self._entries:
            tattoos = [
                t for tid in entry.tattoo_ids if (t := self.collection.get(tid))
            ]
            result.append(
                {
                    "timestamp": entry.timestamp.isoformat(),
                    "narrative": entry.narrative,
                    "tattoos": [t.to_dict() for t in tattoos],
                    "tags": entry.tags,
                }
            )
        return result

    def search(self, query: str) -> List[StoryEntry]:
        """Search entries by narrative text (case-insensitive)."""
        q = query.lower()
        return [e for e in self._entries if q in e.narrative.lower()]

    def by_tag(self, tag: str) -> List[StoryEntry]:
        """Return entries with a given tag."""
        return [e for e in self._entries if tag in e.tags]

    def summary(self) -> str:
        """Generate a short text summary of the story so far."""
        n = len(self._entries)
        nt = len({tid for e in self._entries for tid in e.tattoo_ids})
        return f"{n} entries, {nt} tattoos referenced"

    def to_dict(self) -> dict:
        return {
            "entries": [e.to_dict() for e in self._entries],
        }

    @classmethod
    def from_dict(cls, data: dict, collection: TattooCollection) -> "TattooStory":
        story = cls(collection=collection)
        for ed in data.get("entries", []):
            story._entries.append(StoryEntry.from_dict(ed))
        return story
