"""Unit tests for CommandRouter (portfolio upgrade)."""

from src.config.settings import AppConfig
from src.core.enums import MatchType
from src.knowledge.knowledge_base import KnowledgeBase
from src.process.command_router import CommandRouter
from src.session.interaction_logger import InteractionLogger


class TestIsMetaCommand:
    """Tests for CommandRouter.is_meta_command()."""

    def setup_method(self) -> None:
        config = AppConfig()
        self.kb = KnowledgeBase(config)
        self.logger = InteractionLogger()
        self.router = CommandRouter(knowledge_base=self.kb, logger=self.logger)

    def test_history_is_a_meta_command(self) -> None:
        assert self.router.is_meta_command("history") is True

    def test_clear_is_a_meta_command(self) -> None:
        assert self.router.is_meta_command("clear") is True

    def test_mode_with_argument_is_a_meta_command(self) -> None:
        assert self.router.is_meta_command("mode friendly") is True

    def test_ordinary_greeting_is_not_a_meta_command(self) -> None:
        assert self.router.is_meta_command("hello") is False

    def test_bare_mode_without_argument_is_not_a_meta_command(self) -> None:
        # "mode" alone (no trailing space + name) is not handled here.
        assert self.router.is_meta_command("mode") is False


class TestHandleHistory:
    """Tests for CommandRouter.handle('history')."""

    def test_empty_history_returns_friendly_message(self) -> None:
        kb = KnowledgeBase(AppConfig())
        logger = InteractionLogger()
        router = CommandRouter(knowledge_base=kb, logger=logger)
        assert router.handle("history") == "No interactions yet."

    def test_history_includes_logged_turns(self) -> None:
        kb = KnowledgeBase(AppConfig())
        logger = InteractionLogger()
        logger.log(
            raw_input="hello",
            clean_input="hello",
            match_type=MatchType.INTENT,
            response_text="Hi there!",
        )
        router = CommandRouter(knowledge_base=kb, logger=logger)
        result = router.handle("history")
        assert "hello" in result
        assert "Hi there!" in result

    def test_history_without_a_logger_does_not_crash(self) -> None:
        kb = KnowledgeBase(AppConfig())
        router = CommandRouter(knowledge_base=kb, logger=None)
        result = router.handle("history")
        assert isinstance(result, str)


class TestHandleMode:
    """Tests for CommandRouter.handle('mode <name>')."""

    def setup_method(self) -> None:
        self.kb = KnowledgeBase(AppConfig())
        self.router = CommandRouter(knowledge_base=self.kb, logger=None)

    def test_switching_to_valid_mode_succeeds(self) -> None:
        result = self.router.handle("mode friendly")
        assert "friendly" in result.lower()
        assert self.kb.personality == "friendly"

    def test_switching_to_invalid_mode_lists_options(self) -> None:
        result = self.router.handle("mode nonexistent")
        assert "Unknown mode" in result
        assert "neutral" in result

    def test_invalid_mode_does_not_change_active_personality(self) -> None:
        original = self.kb.personality
        self.router.handle("mode nonexistent")
        assert self.kb.personality == original


class TestHandleClear:
    """Tests for CommandRouter.handle('clear')."""

    def test_clear_returns_confirmation_message(
        self, capsys: object
    ) -> None:
        kb = KnowledgeBase(AppConfig())
        router = CommandRouter(knowledge_base=kb, logger=None)
        result = router.handle("clear")
        assert result == "Screen cleared."
