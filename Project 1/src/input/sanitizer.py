"""Normalizes raw user text before it is matched against intents.

Users type inconsistently -- "Hello", " hello ", "HELLO" should all
mean the same thing to the bot. This module is the single place where
that normalization happens (FR-2), so the rest of the system can
always assume input has already been cleaned.
"""


class InputSanitizer:
    """Applies a small, predictable normalization pipeline to raw text."""

    def sanitize(self, raw: str) -> str:
        """Normalize raw input for intent matching.

        Args:
            raw: The exact string the user typed.

        Returns:
            The input with leading/trailing whitespace removed and all
            characters lowercased. `strip()` runs before `lower()`,
            though for ASCII text the order does not change the
            result -- this order is simply the more conventional one.
        """
        return raw.strip().lower()

    def is_empty(self, clean: str) -> bool:
        """Check whether sanitized input is empty or whitespace-only.

        Args:
            clean: Text that has already been passed through
                `sanitize()`.

        Returns:
            True if there is no meaningful content left to match.
        """
        return clean == ""
