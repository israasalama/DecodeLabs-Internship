"""Unit tests for IntentMatcher."""

from src.config.settings import AppConfig
from src.core.enums import MatchType
from src.knowledge.knowledge_base import KnowledgeBase
from src.process.intent_matcher import IntentMatcher


class TestMatch:
    """Tests for IntentMatcher.match()."""

    def setup_method(self) -> None:
        self.config = AppConfig()
        self.knowledge_base = KnowledgeBase(self.config)
        self.matcher = IntentMatcher(self.knowledge_base)

    def test_known_intent_returns_match_type_intent(self) -> None:
        result = self.matcher.match("hello")
        assert result.match_type == MatchType.INTENT
        assert result.intent_key == "hello"
        assert result.response_text == "Hi there! Welcome to the Logic Engine."
        assert result.is_exit is False

    def test_unknown_input_returns_match_type_fallback(self) -> None:
        result = self.matcher.match("asdfgh")
        assert result.match_type == MatchType.FALLBACK
        assert result.intent_key is None
        assert result.response_text == self.config.fallback_response
        assert result.is_exit is False

    def test_empty_input_returns_fallback(self) -> None:
        result = self.matcher.match("")
        assert result.match_type == MatchType.FALLBACK

    def test_multi_word_intent_matches_exactly(self) -> None:
        result = self.matcher.match("how are you")
        assert result.match_type == MatchType.INTENT
        assert result.intent_key == "how are you"

    def test_partial_match_does_not_match_full_intent(self) -> None:
        # "hello there" should NOT match "hello" -- exact key lookup only.
        result = self.matcher.match("hello there")
        assert result.match_type == MatchType.FALLBACK

    def test_matcher_never_sets_is_exit_true(self) -> None:
        # Exit handling is ExitDetector's job, not IntentMatcher's.
        result = self.matcher.match("exit")
        assert result.is_exit is False
