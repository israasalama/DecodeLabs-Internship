"""Owns the chatbot's continuous interaction loop.

This is the single place in the entire codebase where a `while` loop
runs (FR-1, FR-9). `ChatSession` does not know HOW to sanitize input
or WHICH response matches an intent -- it only knows the *order* of
operations for one turn, and delegates everything else to its
injected dependencies. This keeps the orchestration logic completely
separate from the business rules (single-responsibility, NFR-6).
"""

from src.core.enums import SessionState
from src.input.reader import TerminalInputReader
from src.input.sanitizer import InputSanitizer
from src.output.presenter import TerminalPresenter
from src.process.command_router import CommandRouter
from src.process.response_engine import ResponseEngine
from src.session.interaction_logger import InteractionLogger


class ChatSession:
    """Runs the chatbot's main loop until an exit command is received."""

    def __init__(
        self,
        reader: TerminalInputReader,
        sanitizer: InputSanitizer,
        engine: ResponseEngine,
        presenter: TerminalPresenter,
        logger: InteractionLogger | None = None,
        command_router: CommandRouter | None = None,
    ) -> None:
        """Initialize the session with all its collaborators.

        Args:
            reader: Acquires raw text from the terminal.
            sanitizer: Normalizes raw text for matching.
            engine: Classifies input and produces a ProcessResult.
            presenter: Displays prompts and responses.
            logger: Optional interaction history recorder. If None,
                logging is skipped entirely (it is not required for
                the chatbot to function).
            command_router: Optional handler for meta-commands like
                `history`, `clear`, and `mode <name>`. If None, those
                words are treated as ordinary chat input instead
                (falling back to the knowledge base / fallback text).
        """
        self._reader = reader
        self._sanitizer = sanitizer
        self._engine = engine
        self._presenter = presenter
        self._logger = logger
        self._command_router = command_router
        self._state = SessionState.STOPPED

    @property
    def state(self) -> SessionState:
        """Return the current lifecycle state of the session."""
        return self._state

    def start(self) -> None:
        """Run the chat loop until the user issues an exit command.

        Each iteration performs exactly one IPO turn: read input,
        sanitize it, process it into a response, display the
        response, optionally log it, then either continue or break.
        """
        self._state = SessionState.RUNNING

        while self._state == SessionState.RUNNING:
            should_continue = self._handle_turn()
            if not should_continue:
                self._state = SessionState.STOPPED

        self._presenter.show_goodbye()

    def _handle_turn(self) -> bool:
        """Run a single Input -> Process -> Output cycle.

        Returns:
            True if the session should keep looping, False if this
            turn signaled that the session should stop.
        """
        self._presenter.show_prompt()
        raw_input = self._reader.read()
        clean_input = self._sanitizer.sanitize(raw_input)

        # Meta-commands (history/clear/mode) are checked first, before
        # the deterministic exit -> intent -> fallback pipeline, since
        # they operate on session state rather than being a chat reply.
        if self._command_router is not None and self._command_router.is_meta_command(
            clean_input
        ):
            response_text = self._command_router.handle(clean_input)
            self._presenter.show_response(response_text)
            return True

        result = self._engine.process(raw_input, clean_input)
        self._presenter.show_response(result.match.response_text)

        if self._logger is not None:
            self._logger.log(
                raw_input=result.raw_input,
                clean_input=result.clean_input,
                match_type=result.match.match_type,
                response_text=result.match.response_text,
            )

        return result.should_continue
