"""TattooEarner — condition-based tattoo awards."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .tattoo import Tattoo, TattooCategory, Visibility
from .collection import TattooCollection


@dataclass
class Condition:
    """A condition that, when met, earns a tattoo.

    ``check`` receives arbitrary keyword arguments representing the
    agent's current state and returns True when the condition is
    satisfied.
    """

    name: str
    description: str
    tattoo_name: str
    tattoo_description: str
    category: TattooCategory = TattooCategory.ACHIEVEMENT
    visibility: Visibility = Visibility.PUBLIC
    check: Callable[..., bool] = field(default=lambda: False)
    one_shot: bool = True  # award only once?

    def evaluate(self, ctx: dict) -> bool:
        """Run the check against a context dict."""
        try:
            return self.check(**ctx)
        except TypeError:
            return False

    def make_tattoo(self) -> Tattoo:
        """Create the Tattoo object for this condition."""
        return Tattoo(
            name=self.tattoo_name,
            description=self.tattoo_description,
            category=self.category,
            visibility=self.visibility,
        )


# ── built-in condition factories ─────────────────────────────────

def milestone(name: str, desc: str, count_fn: Callable[..., int], threshold: int) -> Condition:
    """Award a tattoo when a counter reaches a threshold."""

    def check(**kw: object) -> bool:
        try:
            return count_fn(**kw) >= threshold  # type: ignore[arg-type]
        except TypeError:
            return False

    return Condition(
        name=f"milestone:{name}",
        description=f"Reach {threshold} {desc}",
        tattoo_name=name,
        tattoo_description=desc,
        category=TattooCategory.MILESTONE,
        check=check,
    )


def achievement(name: str, desc: str, predicate: Callable[..., bool]) -> Condition:
    """Award a tattoo when a predicate is satisfied."""
    return Condition(
        name=f"achievement:{name}",
        description=desc,
        tattoo_name=name,
        tattoo_description=desc,
        category=TattooCategory.ACHIEVEMENT,
        check=predicate,
    )


def failure(name: str, desc: str, predicate: Callable[..., bool]) -> Condition:
    """Award a tattoo when a failure condition is met."""
    return Condition(
        name=f"failure:{name}",
        description=desc,
        tattoo_name=name,
        tattoo_description=desc,
        category=TattooCategory.FAILURE,
        visibility=Visibility.INTERNAL,
        check=predicate,
    )


@dataclass
class TattooEarner:
    """Evaluates conditions and awards tattoos to a collection.

    Typical usage::

        earner = TattooEarner(collection)
        earner.register(milestone("First Blood", "First mission complete", ...))
        earner.check_all(missions_complete=1)
    """

    collection: TattooCollection
    _conditions: List[Condition] = field(default_factory=list)
    _awarded: set = field(default_factory=set)  # condition names already awarded

    def register(self, *conditions: Condition) -> None:
        """Register one or more conditions."""
        for c in conditions:
            self._conditions.append(c)

    def check_all(self, **ctx: object) -> List[Tattoo]:
        """Evaluate all conditions against *ctx*; award new tattoos.

        Returns the list of newly earned tattoos.
        """
        earned: List[Tattoo] = []
        for cond in self._conditions:
            if cond.one_shot and cond.name in self._awarded:
                continue
            if cond.evaluate(ctx):
                tattoo = cond.make_tattoo()
                self.collection.add(tattoo)
                self._awarded.add(cond.name)
                earned.append(tattoo)
        return earned

    def pending(self) -> List[Condition]:
        """Return conditions not yet awarded."""
        return [c for c in self._conditions if c.name not in self._awarded]
