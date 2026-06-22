"""Routes session-level meta-commands that aren't ordinary intents.

PORTFOLIO UPGRADE. Commands like `history`, `clear`, and `mode <name>`
need access to things a plain `IntentMatcher` shouldn't know about
(the interaction logger, the knowledge base's personality switch).
Rather than bloating `ResponseEngine` or `KnowledgeBase` with that
knowledge, this dedicated router owns it -- keeping each existing
class's original single responsibility intact.

`ChatSession` checks this router BEFORE the normal exit/intent/
fallback pipeline, so these commands work regardless of personality
or knowledge-base content.
"""

from src.knowledge.knowledge_base import KnowledgeBase
from src.session.interaction_logger import InteractionLogger


class CommandRouter:
    """Handles `history`, `clear`, and `mode` meta-commands."""

    def __init__(
        self, knowledge_base: KnowledgeBase, logger: InteractionLogger | None
    ) -> None:
        """Initialize the router with the components it needs to control.

        Args:
            knowledge_base: Used to switch personalities via `mode`.
            logger: Used to display past turns via `history`. May be
                None if logging is disabled for this session.
        """
        self._knowledge_base = knowledge_base
        self._logger = logger

    def is_meta_command(self, clean_input: str) -> bool:
        """Check whether sanitized input is a meta-command this router handles.

        Args:
            clean_input: Sanitized text from the input layer.

        Returns:
            True if `clean_input` is exactly `"history"`, `"clear"`,
            or starts with `"mode "`.
        """
        return (
            clean_input == "history"
            or clean_input == "clear"
            or clean_input.startswith("mode ")
        )

    def handle(self, clean_input: str) -> str:
        """Execute a meta-command and return its response text.

        Args:
            clean_input: Sanitized text already confirmed to be a
                meta-command via `is_meta_command()`.

        Returns:
            A response string describing the result of the command.
        """
        if clean_input == "history":
            return self._show_history()
        if clean_input == "clear":
            return self._clear_screen()
        if clean_input.startswith("mode "):
            requested = clean_input.removeprefix("mode ").strip()
            return self._switch_mode(requested)
        # Defensive fallback: should be unreachable if is_meta_command()
        # was checked first, but never crash on an unexpected case.
        return "I do not understand that command."

    def _show_history(self) -> str:
        """Format the last few logged turns as a readable summary."""
        if self._logger is None:
            return "History is not available in this session."
        trace = self._logger.get_trace()
        if not trace:
            return "No interactions yet."
        recent = trace[-5:]
        lines = [f'  "{record.raw_input}" -> {record.response_text}' for record in recent]
        return "Recent history:\n" + "\n".join(lines)

    def _clear_screen(self) -> str:
        """Print enough blank lines to visually clear the terminal."""
        print("\n" * 50)
        return "Screen cleared."

    def _switch_mode(self, requested: str) -> str:
        """Attempt to switch the knowledge base's active personality.

        Args:
            requested: The personality name the user typed after
                `"mode "`.

        Returns:
            A confirmation message on success, or a helpful error
            listing valid options on failure.
        """
        if self._knowledge_base.set_personality(requested):
            return f"Mode switched to '{requested}'."
        available = ", ".join(KnowledgeBase.available_personalities())
        return f"Unknown mode '{requested}'. Available modes: {available}."
