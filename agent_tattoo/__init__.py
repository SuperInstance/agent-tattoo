"""Agent Tattoo — persistent behavioral markers for AI agents."""

from .tattoo import Tattoo, Visibility, TattooCategory
from .collection import TattooCollection
from .earner import TattooEarner, Condition
from .story import TattooStory
from .display import TattooDisplay

__all__ = [
    "Tattoo",
    "TattooCollection",
    "TattooEarner",
    "Condition",
    "TattooStory",
    "TattooDisplay",
    "Visibility",
    "TattooCategory",
]
__version__ = "0.1.0"
