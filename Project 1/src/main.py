"""Application entry point.

Wires every layer together in one place: this is the only module that
knows about ALL the other modules. Everything below it only knows
about its direct collaborators (dependency injection), which is what
makes each piece independently testable.
"""

import sys
from pathlib import Path

from src.config.settings import AppConfig
from src.input.reader import TerminalInputReader
from src.input.sanitizer import InputSanitizer
from src.knowledge.knowledge_base import KnowledgeBase
from src.output.banner import BannerRenderer
from src.output.presenter import TerminalPresenter
from src.process.command_router import CommandRouter
from src.process.exit_detector import ExitDetector
from src.process.intent_matcher import IntentMatcher
from src.process.response_engine import ResponseEngine
from src.session.chat_session import ChatSession
from src.session.interaction_logger import InteractionLogger

BANNER_PATH = Path(__file__).resolve().parent.parent / "assets" / "banner.txt"
LOG_FILE_PATH = Path(__file__).resolve().parent.parent / "chatbot_session.log"


class ChatBotApp:
    """Bootstraps dependencies and runs the chatbot session."""

    def __init__(self, config: AppConfig | None = None) -> None:
        """Build every layer of the application.

        Args:
            config: Optional custom configuration. Defaults to
                `AppConfig()` if not provided, so the app can be run
                with zero setup.
        """
        self._config = config or AppConfig()
        self._knowledge_base = KnowledgeBase(self._config)
        self._banner = BannerRenderer(BANNER_PATH)
        self._session = self._build_session()

    def _build_session(self) -> ChatSession:
        """Wire up the input/process/output layers into one ChatSession.

        Returns:
            A fully constructed ChatSession ready to call `.start()`.
        """
        reader = TerminalInputReader()
        sanitizer = InputSanitizer()
        engine = ResponseEngine(
            exit_detector=ExitDetector(self._config),
            intent_matcher=IntentMatcher(self._knowledge_base),
        )
        presenter = TerminalPresenter(
            bot_prefix=self._config.bot_prefix, user_prompt=self._config.user_prompt
        )
        logger = InteractionLogger(log_file_path=LOG_FILE_PATH)
        command_router = CommandRouter(knowledge_base=self._knowledge_base, logger=logger)
        return ChatSession(
            reader=reader,
            sanitizer=sanitizer,
            engine=engine,
            presenter=presenter,
            logger=logger,
            command_router=command_router,
        )

    def run(self) -> None:
        """Validate the knowledge base, show the banner, and start chatting.

        Raises:
            SystemExit: If the knowledge base fails validation (fewer
                than the minimum required intents), the app fails fast
                with a clear message rather than starting a broken
                session.
        """
        if not self._knowledge_base.validate():
            print(
                f"[Startup Error] Knowledge base has fewer than "
                f"{self._config.min_intents} intents. Cannot start."
            )
            raise SystemExit(1)

        self._banner.render()
        self._session.start()


def main() -> None:
    """CLI entry point: build and run the chatbot application."""
    app = ChatBotApp()
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        # Graceful shutdown on Ctrl+C or end-of-input (e.g. piped
        # input running out) instead of an ugly traceback.
        print("\nBot: Session interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
