"""Typed data carriers that flow between the chatbot's IPO layers.

Instead of passing loose tuples or dicts between functions (which are
easy to misuse -- e.g. forgetting which index holds what), each stage
of the pipeline returns one of these well-named, type-checked objects.
This is what makes the system's logic traceable: every value has a
name and a type.
"""

from dataclasses import dataclass, field
from datetime import datetime

from src.core.enums import MatchType


@dataclass(frozen=True)
class IntentMatch:
    """Result of classifying a single sanitized input string.

    Attributes:
        match_type: Whether this was an exit, a known intent, or a
            fallback case.
        intent_key: The knowledge-base key that was matched, or None
            if no intent matched (exit / fallback cases).
        response_text: The text the bot should display to the user.
        is_exit: True if the session should terminate after this turn.
    """

    match_type: MatchType
    intent_key: str | None
    response_text: str
    is_exit: bool


@dataclass(frozen=True)
class ProcessResult:
    """Outcome of running one full turn through the process layer.

    Attributes:
        raw_input: The exact text the user typed, before any cleanup.
        clean_input: The sanitized (lowercased/stripped) version used
            for matching.
        match: The IntentMatch describing how the input was classified.
        should_continue: False when the session loop should break.
    """

    raw_input: str
    clean_input: str
    match: IntentMatch
    should_continue: bool


@dataclass(frozen=True)
class InteractionRecord:
    """A single logged turn, used for explainability and debugging.

    Attributes:
        timestamp: When the interaction was processed.
        raw_input: Original user text for this turn.
        clean_input: Sanitized text used for matching.
        match_type: How the turn was classified.
        response_text: What the bot replied with.
    """

    raw_input: str
    clean_input: str
    match_type: MatchType
    response_text: str
    timestamp: datetime = field(default_factory=datetime.now)
