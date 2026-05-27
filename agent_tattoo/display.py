"""TattooDisplay — render tattoo collections as text / markdown / ASCII art."""

from __future__ import annotations

from typing import List, Sequence

from .tattoo import Tattoo, TattooCategory, Visibility
from .collection import TattooCollection


CATEGORY_ICONS = {
    TattooCategory.MILESTONE: "★",
    TattooCategory.ACHIEVEMENT: "◆",
    TattooCategory.CAPABILITY: "●",
    TattooCategory.FAILURE: "✕",
    TattooCategory.EXPERIENCE: "◈",
    TattooCategory.IDENTITY: "◉",
}

VISIBILITY_ICONS = {
    Visibility.PUBLIC: "👁",
    Visibility.INTERNAL: "🔒",
    Visibility.PRIVATE: "🚫",
    Visibility.HIDDEN: "∅",
}

FADE_BAR_FULL = "█"
FADE_BAR_EMPTY = "░"


def _fade_bar(fade: float, width: int = 10) -> str:
    filled = round((1.0 - fade) * width)
    return FADE_BAR_FULL * filled + FADE_BAR_EMPTY * (width - filled)


class TattooDisplay:
    """Render tattoo collections in various text formats."""

    @staticmethod
    def tattoo_to_text(tattoo: Tattoo) -> str:
        """Single tattoo as a compact text line."""
        icon = CATEGORY_ICONS.get(tattoo.category, "?")
        vis = VISIBILITY_ICONS.get(tattoo.visibility, "?")
        bar = _fade_bar(tattoo.fade_level)
        return f"{icon} {tattoo.name} {vis} [{bar}] {tattoo.description}"

    @staticmethod
    def collection_as_text(collection: TattooCollection) -> str:
        """Render a full collection as plain text."""
        if not collection.all:
            return "(no tattoos)"
        lines: List[str] = []
        if collection.owner:
            lines.append(f"Tattoos for {collection.owner}")
            lines.append("=" * 40)
        for t in collection:
            lines.append(TattooDisplay.tattoo_to_text(t))
        lines.append(f"\nTotal: {len(collection)} | Avg fade: {collection.average_fade:.2f}")
        return "\n".join(lines)

    @staticmethod
    def collection_as_markdown(collection: TattooCollection) -> str:
        """Render a full collection as a markdown document."""
        lines: List[str] = []
        title = collection.owner or "Agent"
        lines.append(f"# 🖋️ Tattoos — {title}\n")
        if not collection.all:
            lines.append("_No tattoos yet._")
            return "\n".join(lines)

        # group by category
        by_cat: dict[TattooCategory, list] = {}
        for t in collection:
            by_cat.setdefault(t.category, []).append(t)

        for cat, tattoos in by_cat.items():
            lines.append(f"\n## {CATEGORY_ICONS.get(cat, '')} {cat.value.title()}\n")
            for t in tattoos:
                bar = _fade_bar(t.fade_level, 8)
                lines.append(f"- **{t.name}** — {t.description}")
                lines.append(f"  `[{bar}]` earned {t.earned_at.strftime('%Y-%m-%d')}")

        lines.append(f"\n---\n*{len(collection)} tattoos · average fade {collection.average_fade:.0%}*")
        return "\n".join(lines)

    @staticmethod
    def collection_as_ascii(collection: TattooCollection, width: int = 40) -> str:
        """Render a compact ASCII art sleeve of tattoos."""
        if not collection.all:
            return "(blank skin)"

        lines: List[str] = []
        border = "╱" + "─" * (width - 2) + "╲"
        lines.append(border)

        for t in collection:
            icon = CATEGORY_ICONS.get(t.category, "?")
            label = f" {icon} {t.name} "
            pad = width - 2 - len(label)
            if pad < 0:
                label = label[: width - 5] + "… "
                pad = width - 2 - len(label)
            lines.append("│" + label + " " * pad + "│")

            desc = f"   {t.description} "
            if len(desc) > width - 2:
                desc = desc[: width - 5] + "… "
            pad = width - 2 - len(desc)
            lines.append("│" + desc + " " * pad + "│")

            bar_label = f"   fade: {_fade_bar(t.fade_level, 6)} "
            pad = width - 2 - len(bar_label)
            lines.append("│" + bar_label + " " * pad + "│")
            lines.append("│" + " " * (width - 2) + "│")

        lines.append("╲" + "─" * (width - 2) + "╱")
        return "\n".join(lines)
