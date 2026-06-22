"""Renders the chatbot's startup banner.

Splitting this out from `TerminalPresenter` keeps "branding/welcome
screen" separate from "ongoing conversation display" -- two different
responsibilities that happen to both print text.
"""

from pathlib import Path


class BannerRenderer:
    """Loads and prints an ASCII banner from a text file."""

    def __init__(self, banner_path: str | Path) -> None:
        """Initialize the renderer with a path to the banner file.

        Args:
            banner_path: Filesystem path to a plain-text banner file.
        """
        self._banner_path = Path(banner_path)

    def render(self) -> None:
        """Print the banner file's contents, if it exists.

        Missing or unreadable banner files are treated as non-fatal:
        the chatbot's core purpose is conversation, not branding, so a
        missing banner should never stop the program from starting
        (NFR-4: unknown/edge conditions must not crash the program).
        """
        try:
            banner_text = self._banner_path.read_text(encoding="utf-8")
            print(banner_text)
        except (FileNotFoundError, OSError):
            # No banner available -- fall back to a minimal text header
            # rather than crashing or printing nothing at all.
            print("=== Rule-Based AI Chatbot ===")
