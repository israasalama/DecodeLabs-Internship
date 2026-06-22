"""Renders all chatbot output to the terminal.

This module's only job is printing. It contains zero decision-making
logic -- it never decides *what* the bot should say, only *how* that
text is displayed (NFR-8). Keeping output this "dumb" makes the
chatbot easy to port to a different interface later (a website, an
API, etc.) without touching this file at all.
"""


class TerminalPresenter:
    """Displays prompts and bot replies using configured labels."""

    def __init__(self, bot_prefix: str, user_prompt: str = "") -> None:
        """Initialize the presenter with labels for replies and prompts.

        Args:
            bot_prefix: Text shown before every bot response
                (e.g. "Bot: ").
            user_prompt: Text shown before the user types
                (e.g. "You: "). Optional because `TerminalInputReader`
                also prints this label itself via `input(prompt)`;
                `show_prompt()` exists for callers that need to render
                the label separately from blocking on input.
        """
        self._bot_prefix = bot_prefix
        self._user_prompt = user_prompt

    def show_prompt(self) -> None:
        """Print the user input label without blocking for input.

        Useful for UIs that separate "display the prompt" from
        "wait for text", unlike the standard blocking `input()` call.
        """
        print(self._user_prompt, end="")

    def show_response(self, text: str) -> None:
        """Print a bot reply with its configured prefix.

        Args:
            text: The response text to display.
        """
        print(f"{self._bot_prefix}{text}")

    def show_goodbye(self) -> None:
        """Print a final farewell message when the session ends."""
        print(f"{self._bot_prefix}Session ended. See you next time!")

    def show_error(self, message: str) -> None:
        """Print a non-fatal error message without crashing the session.

        Args:
            message: A human-readable description of what went wrong.
        """
        print(f"[Error] {message}")
