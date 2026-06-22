"""Orchestrates the deterministic decision pipeline for one turn.

This is the component that enforces FR-8: a single, fixed order of
conditional checks (exit, then intent, then fallback) rather than an
unpredictable or overlapping set of rules. Every input takes exactly
one of these three paths, every time.
"""

from src.core.enums import MatchType
from src.core.models import IntentMatch, ProcessResult
from src.process.exit_detector import ExitDetector
from src.process.intent_matcher import IntentMatcher


class ResponseEngine:
    """Combines exit detection and intent matching into one decision."""

    def __init__(
        self, exit_detector: ExitDetector, intent_matcher: IntentMatcher
    ) -> None:
        """Initialize the engine with its two process-stage collaborators.

        Args:
            exit_detector: Checked first, before any intent matching.
            intent_matcher: Checked only if the input is not an exit
                command.
        """
        self._exit_detector = exit_detector
        self._intent_matcher = intent_matcher

    def process(self, raw_input: str, clean_input: str) -> ProcessResult:
        """Run one full turn through the fixed exit -> intent -> fallback order.

        Args:
            raw_input: The exact text the user typed.
            clean_input: The sanitized version of `raw_input`.

        Returns:
            A `ProcessResult` describing the classification, the
            response text to show, and whether the session should
            continue afterward.
        """
        if self._exit_detector.is_exit_command(clean_input):
            exit_match = IntentMatch(
                match_type=MatchType.EXIT,
                intent_key=None,
                response_text="Goodbye! Have a great day.",
                is_exit=True,
            )
            return ProcessResult(
                raw_input=raw_input,
                clean_input=clean_input,
                match=exit_match,
                should_continue=False,
            )

        match = self._intent_matcher.match(clean_input)
        return ProcessResult(
            raw_input=raw_input,
            clean_input=clean_input,
            match=match,
            should_continue=True,
        )
