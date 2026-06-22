"""Detects whether sanitized input is the command to end the session.

This is deliberately its own class, separate from the knowledge base.
"Should the program stop running" is a different kind of decision
from "what answer should I give", so it gets its own single-purpose
component (FR-5, FR-7).
"""

from src.config.settings import AppConfig


class ExitDetector:
    """Compares sanitized input against the configured exit command."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the detector with the app's exit keyword.

        Args:
            config: Application configuration containing
                `exit_command`.
        """
        self._exit_command = config.exit_command

    def is_exit_command(self, clean_input: str) -> bool:
        """Check if sanitized input should terminate the session.

        Args:
            clean_input: Text that has already been sanitized
                (lowercased and stripped).

        Returns:
            True if `clean_input` exactly matches the configured exit
            command. Because both the input and the configured
            command are compared in their sanitized/lowercase form,
            `"EXIT"`, `"Exit"`, and `"  exit  "` will all be detected
            correctly once sanitized upstream.
        """
        return clean_input == self._exit_command
