"""Matches sanitized input against the knowledge base.

This module bridges the raw `dict.get()` lookup in `KnowledgeBase`
with the typed `IntentMatch` object that the rest of the system
expects, recording not just *what* the response was but *how* it was
classified (matched intent vs. fallback).
"""

from src.core.enums import MatchType
from src.core.models import IntentMatch
from src.knowledge.knowledge_base import KnowledgeBase


class IntentMatcher:
    """Performs intent lookup and classifies the result."""

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        """Initialize the matcher with a knowledge base to query.

        Args:
            knowledge_base: The dictionary-backed source of intents.
        """
        self._knowledge_base = knowledge_base

    def match(self, clean_input: str) -> IntentMatch:
        """Classify sanitized input as a known intent or a fallback.

        Args:
            clean_input: Sanitized text (assumed NOT to be the exit
                command -- that check happens earlier in
                `ResponseEngine`).

        Returns:
            An `IntentMatch` with `MatchType.INTENT` and the matched
            key/response if `clean_input` exists in the knowledge
            base; otherwise `MatchType.FALLBACK` with the fallback
            text. In both cases `is_exit` is False, since exit
            handling does not belong to this class.
        """
        if self._knowledge_base.has_intent(clean_input):
            response_text = self._knowledge_base.get_response(clean_input)
            return IntentMatch(
                match_type=MatchType.INTENT,
                intent_key=clean_input,
                response_text=response_text,
                is_exit=False,
            )

        fallback_text = self._knowledge_base.get_response(clean_input)
        return IntentMatch(
            match_type=MatchType.FALLBACK,
            intent_key=None,
            response_text=fallback_text,
            is_exit=False,
        )
