"""Unit tests for KnowledgeBase."""

import pytest

from src.config.settings import AppConfig
from src.knowledge.knowledge_base import KnowledgeBase


@pytest.fixture
def config() -> AppConfig:
    """A default AppConfig shared by all tests in this module."""
    return AppConfig()


@pytest.fixture
def knowledge_base(config: AppConfig) -> KnowledgeBase:
    """A KnowledgeBase built from the default config."""
    return KnowledgeBase(config)


class TestGetResponse:
    """Tests for KnowledgeBase.get_response()."""

    def test_known_intent_returns_mapped_response(
        self, knowledge_base: KnowledgeBase
    ) -> None:
        assert knowledge_base.get_response("hello") == (
            "Hi there! Welcome to the Logic Engine."
        )

    def test_unknown_intent_returns_fallback(
        self, knowledge_base: KnowledgeBase, config: AppConfig
    ) -> None:
        assert knowledge_base.get_response("asdfgh") == config.fallback_response

    def test_empty_string_returns_fallback(
        self, knowledge_base: KnowledgeBase, config: AppConfig
    ) -> None:
        assert knowledge_base.get_response("") == config.fallback_response


class TestHasIntent:
    """Tests for KnowledgeBase.has_intent()."""

    def test_known_key_returns_true(self, knowledge_base: KnowledgeBase) -> None:
        assert knowledge_base.has_intent("bye") is True

    def test_unknown_key_returns_false(self, knowledge_base: KnowledgeBase) -> None:
        assert knowledge_base.has_intent("nonexistent") is False

    def test_exit_is_not_a_knowledge_base_intent(
        self, knowledge_base: KnowledgeBase
    ) -> None:
        # Exit is handled by ExitDetector, not the knowledge base.
        assert knowledge_base.has_intent("exit") is False


class TestListIntents:
    """Tests for KnowledgeBase.list_intents()."""

    def test_returns_all_registered_keys(
        self, knowledge_base: KnowledgeBase
    ) -> None:
        intents = knowledge_base.list_intents()
        for expected_key in ("hello", "hi", "help", "bye", "how are you"):
            assert expected_key in intents

    def test_returns_a_list_not_a_view(self, knowledge_base: KnowledgeBase) -> None:
        assert isinstance(knowledge_base.list_intents(), list)


class TestValidate:
    """Tests for KnowledgeBase.validate()."""

    def test_seed_data_passes_validation(self, knowledge_base: KnowledgeBase) -> None:
        assert knowledge_base.validate() is True

    def test_fails_when_min_intents_exceeds_actual_count(
        self, config: AppConfig
    ) -> None:
        strict_config = AppConfig(min_intents=999)
        kb = KnowledgeBase(strict_config)
        assert kb.validate() is False

    def test_passes_when_min_intents_is_low(self) -> None:
        lenient_config = AppConfig(min_intents=1)
        kb = KnowledgeBase(lenient_config)
        assert kb.validate() is True


class TestPersonalityModes:
    """Tests for the portfolio-upgrade personality feature."""

    def test_default_personality_is_neutral(self, config: AppConfig) -> None:
        kb = KnowledgeBase(config)
        assert kb.personality == "neutral"

    def test_unknown_personality_falls_back_to_default(
        self, config: AppConfig
    ) -> None:
        kb = KnowledgeBase(config, personality="does-not-exist")
        assert kb.personality == "neutral"

    def test_friendly_personality_changes_response_text(
        self, config: AppConfig
    ) -> None:
        kb = KnowledgeBase(config, personality="friendly")
        assert kb.get_response("bye") != "Goodbye! Have a great day."
        assert "bye" in kb.list_intents()

    def test_set_personality_switches_responses(self, config: AppConfig) -> None:
        kb = KnowledgeBase(config)
        neutral_reply = kb.get_response("hello")
        switched = kb.set_personality("professional")
        assert switched is True
        assert kb.get_response("hello") != neutral_reply

    def test_set_personality_rejects_unknown_name(self, config: AppConfig) -> None:
        kb = KnowledgeBase(config)
        original = kb.personality
        switched = kb.set_personality("nonexistent")
        assert switched is False
        assert kb.personality == original

    def test_available_personalities_includes_all_three(self) -> None:
        names = KnowledgeBase.available_personalities()
        assert {"neutral", "friendly", "professional"}.issubset(set(names))

    def test_every_personality_meets_minimum_intent_count(
        self, config: AppConfig
    ) -> None:
        for name in KnowledgeBase.available_personalities():
            kb = KnowledgeBase(config, personality=name)
            assert kb.validate() is True
