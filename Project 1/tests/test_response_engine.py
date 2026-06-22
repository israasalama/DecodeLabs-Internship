"""Unit tests for ResponseEngine.

Test cases mirror the turn-level decision table in design.md Section 7.
"""

from src.config.settings import AppConfig
from src.core.enums import MatchType
from src.knowledge.knowledge_base import KnowledgeBase
from src.process.exit_detector import ExitDetector
from src.process.intent_matcher import IntentMatcher
from src.process.response_engine import ResponseEngine


class TestProcess:
    """Tests for ResponseEngine.process()."""

    def setup_method(self) -> None:
        config = AppConfig()
        knowledge_base = KnowledgeBase(config)
        self.engine = ResponseEngine(
            exit_detector=ExitDetector(config),
            intent_matcher=IntentMatcher(knowledge_base),
        )

    def test_exit_input_stops_session(self) -> None:
        result = self.engine.process(raw_input="exit", clean_input="exit")
        assert result.match.match_type == MatchType.EXIT
        assert result.match.is_exit is True
        assert result.should_continue is False

    def test_greeting_input_continues_session(self) -> None:
        result = self.engine.process(raw_input="hello", clean_input="hello")
        assert result.match.match_type == MatchType.INTENT
        assert result.should_continue is True

    def test_unknown_input_falls_back_and_continues(self) -> None:
        result = self.engine.process(raw_input="asdfgh", clean_input="asdfgh")
        assert result.match.match_type == MatchType.FALLBACK
        assert result.should_continue is True

    def test_empty_input_falls_back_and_continues(self) -> None:
        result = self.engine.process(raw_input="", clean_input="")
        assert result.match.match_type == MatchType.FALLBACK
        assert result.should_continue is True

    def test_uppercase_exit_after_sanitization_stops_session(self) -> None:
        # clean_input is what sanitizer would have produced from "EXIT".
        result = self.engine.process(raw_input="EXIT", clean_input="exit")
        assert result.match.match_type == MatchType.EXIT
        assert result.should_continue is False

    def test_process_result_preserves_raw_and_clean_input(self) -> None:
        result = self.engine.process(raw_input="  HeLLo  ", clean_input="hello")
        assert result.raw_input == "  HeLLo  "
        assert result.clean_input == "hello"

    def test_exit_is_checked_before_intent_matching(self) -> None:
        # Even though "exit" is technically not in the knowledge base,
        # the engine must short-circuit to EXIT rather than FALLBACK.
        result = self.engine.process(raw_input="exit", clean_input="exit")
        assert result.match.match_type != MatchType.FALLBACK
