"""Shared enumerations used across the chatbot's layers.

Enums are used instead of raw strings (like "exit" or "running") so
that typos are caught by the type checker / IDE instead of causing a
silent bug at runtime (e.g. comparing to "EXIT" instead of "exit").
"""

from enum import Enum, auto


class MatchType(Enum):
    """Classifies how a piece of sanitized input was handled.

    This is the heart of the chatbot's "white-box" explainability
    requirement (NFR-2): every response can be traced back to exactly
    one of these three categories, with no hidden logic in between.
    """

    EXIT = auto()
    INTENT = auto()
    FALLBACK = auto()


class SessionState(Enum):
    """Tracks whether the chat loop is active or has stopped."""

    RUNNING = auto()
    STOPPED = auto()
