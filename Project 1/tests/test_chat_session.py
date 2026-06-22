"""Unit tests for ChatSession.

These tests mock `TerminalInputReader` so the loop can be verified
without a human typing anything, per the design's testing guidance.
"""

from unittest.mock import MagicMock

import pytest

from src.config.settings import AppConfig
from src.core.enums import SessionState
from src.input.reader import TerminalInputReader
from src.input.sanitizer import InputSanitizer
from src.knowledge.knowledge_base import KnowledgeBase
from src.output.presenter import TerminalPresenter
from src.process.command_router import CommandRouter
from src.process.exit_detector import ExitDetector
from src.process.intent_matcher import IntentMatcher
from src.process.response_engine import ResponseEngine
from src.session.chat_session import ChatSession
from src.session.interaction_logger import InteractionLogger


def build_session(
    scripted_inputs: list[str], with_logger: bool = True
) -> tuple[ChatSession, InteractionLogger | None]:
    """Helper to build a ChatSession with a mocked reader.

    Args:
        scripted_inputs: A sequence of raw inputs the mocked reader
            will return, one per call to `read()`.
        with_logger: Whether to attach a real InteractionLogger.

    Returns:
        A tuple of (session, logger) where logger is None if
        `with_logger` is False.
    """
    config = AppConfig()
    knowledge_base = KnowledgeBase(config)

    reader = MagicMock(spec=TerminalInputReader)
    reader.read.side_effect = scripted_inputs

    sanitizer = InputSanitizer()
    engine = ResponseEngine(
        exit_detector=ExitDetector(config),
        intent_matcher=IntentMatcher(knowledge_base),
    )
    presenter = TerminalPresenter(bot_prefix=config.bot_prefix, user_prompt=config.user_prompt)
    logger = InteractionLogger() if with_logger else None
    command_router = CommandRouter(knowledge_base=knowledge_base, logger=logger)

    session = ChatSession(
        reader=reader,
        sanitizer=sanitizer,
        engine=engine,
        presenter=presenter,
        logger=logger,
        command_router=command_router,
    )
    return session, logger


class TestChatSessionLoop:
    """Tests for ChatSession.start() loop behavior."""

    def test_loop_runs_until_exit_command(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        session, _ = build_session(["hello", "exit"])
        session.start()
        assert session.state == SessionState.STOPPED

    def test_loop_processes_multiple_turns_before_exit(self) -> None:
        session, logger = build_session(["hello", "bye", "asdfgh", "exit"])
        session.start()
        assert logger is not None
        trace = logger.get_trace()
        assert len(trace) == 4
        assert trace[-1].clean_input == "exit"

    def test_empty_input_does_not_crash_the_loop(self) -> None:
        session, logger = build_session(["", "   ", "exit"])
        session.start()  # Should complete without raising.
        assert logger is not None
        assert len(logger.get_trace()) == 3

    def test_session_shows_goodbye_on_exit(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        session, _ = build_session(["exit"])
        session.start()
        captured = capsys.readouterr()
        assert "Session ended" in captured.out

    def test_session_works_without_a_logger(self) -> None:
        session, logger = build_session(["hello", "exit"], with_logger=False)
        assert logger is None
        session.start()  # Should not raise even with logger=None.
        assert session.state == SessionState.STOPPED

    def test_uppercase_exit_terminates_loop(self) -> None:
        session, logger = build_session(["HELLO", "EXIT"])
        session.start()
        assert logger is not None
        assert logger.get_trace()[-1].clean_input == "exit"

    def test_mode_command_does_not_appear_in_intent_log(self) -> None:
        # "mode friendly" is intercepted by the CommandRouter before
        # reaching the ResponseEngine, so it should NOT be logged as
        # a regular interaction.
        session, logger = build_session(["mode friendly", "exit"])
        session.start()
        assert logger is not None
        trace = logger.get_trace()
        assert len(trace) == 1  # only "exit" was logged
        assert trace[0].clean_input == "exit"

    def test_history_command_keeps_session_running(self) -> None:
        session, _ = build_session(["hello", "history", "exit"])
        session.start()
        assert session.state == SessionState.STOPPED  # ended via "exit", not crash
