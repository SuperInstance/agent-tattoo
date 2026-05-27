"""TattooCollection — manages an agent's accumulated tattoos."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, List, Optional, Sequence

from .tattoo import Tattoo, TattooCategory, Visibility


@dataclass
class TattooCollection:
    """A collection of tattoos belonging to a single agent.

    Supports adding, removing, searching, and filtering tattoos by
    various criteria (category, visibility, keyword).
    """

    owner: str = ""
    _tattoos: List[Tattoo] = field(default_factory=list)

    # ── mutators ──────────────────────────────────────────────

    def add(self, tattoo: Tattoo) -> None:
        """Add a tattoo to the collection."""
        if any(t.id == tattoo.id for t in self._tattoos):
            raise ValueError(f"Tattoo with id {tattoo.id!r} already in collection")
        self._tattoos.append(tattoo)

    def remove(self, tattoo_id: str) -> Optional[Tattoo]:
        """Remove and return a tattoo by id, or None if not found."""
        for i, t in enumerate(self._tattoos):
            if t.id == tattoo_id:
                return self._tattoos.pop(i)
        return None

    def clear(self) -> None:
        """Remove all tattoos."""
        self._tattoos.clear()

    # ── queries ───────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._tattoos)

    def __iter__(self) -> Iterator[Tattoo]:  # type: ignore[override]
        return iter(self._tattoos)

    def __contains__(self, tattoo_id: str) -> bool:  # type: ignore[override]
        return any(t.id == tattoo_id for t in self._tattoos)

    def get(self, tattoo_id: str) -> Optional[Tattoo]:
        """Look up a tattoo by id."""
        for t in self._tattoos:
            if t.id == tattoo_id:
                return t
        return None

    @property
    def all(self) -> Sequence[Tattoo]:
        """Return all tattoos (read-only view)."""
        return list(self._tattoos)

    # ── filtering ─────────────────────────────────────────────

    def by_category(self, category: TattooCategory) -> List[Tattoo]:
        """Return tattoos matching a category."""
        return [t for t in self._tattoos if t.category == category]

    def by_visibility(self, visibility: Visibility) -> List[Tattoo]:
        """Return tattoos matching a visibility level."""
        return [t for t in self._tattoos if t.visibility == visibility]

    def visible_to(self, viewer: str = "public") -> List[Tattoo]:
        """Return tattoos visible to a given viewer role."""
        return [t for t in self._tattoos if t.is_visible_to(viewer)]

    def search(self, query: str) -> List[Tattoo]:
        """Search tattoos by name or description (case-insensitive)."""
        q = query.lower()
        return [
            t
            for t in self._tattoos
            if q in t.name.lower() or q in t.description.lower()
        ]

    def fresh(self, max_fade: float = 0.3) -> List[Tattoo]:
        """Return tattoos below a fade threshold."""
        return [t for t in self._tattoos if t.fade_level <= max_fade]

    def faded(self, min_fade: float = 0.7) -> List[Tattoo]:
        """Return tattoos above a fade threshold."""
        return [t for t in self._tattoos if t.fade_level >= min_fade]

    # ── stats ─────────────────────────────────────────────────

    @property
    def categories(self) -> dict[TattooCategory, int]:
        """Count tattoos per category."""
        counts: dict[TattooCategory, int] = {}
        for t in self._tattoos:
            counts[t.category] = counts.get(t.category, 0) + 1
        return counts

    @property
    def average_fade(self) -> float:
        """Average fade level across all tattoos."""
        if not self._tattoos:
            return 0.0
        return sum(t.fade_level for t in self._tattoos) / len(self._tattoos)

    # ── serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "tattoos": [t.to_dict() for t in self._tattoos],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TattooCollection":
        coll = cls(owner=data.get("owner", ""))
        for td in data.get("tattoos", []):
            coll.add(Tattoo.from_dict(td))
        return coll
