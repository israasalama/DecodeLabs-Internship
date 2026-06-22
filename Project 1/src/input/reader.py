"""Acquires raw text from the terminal.

This is the only place in the codebase that calls Python's built-in
`input()`. Isolating it here means the rest of the system never talks
to the terminal directly, which makes it possible to test everything
else (sanitizing, matching, etc.) without a human typing anything.

Note: this reader does NOT print the prompt label itself. That is
`TerminalPresenter.show_prompt()`'s job (output layer). `read()` is
called immediately after, so the label appears once, not twice.
"""


class TerminalInputReader:
    """Reads one line of raw text from standard input."""

    def read(self) -> str:
        """Block until the user types a line and presses Enter.

        Returns:
            The raw string typed by the user, exactly as entered
            (no trimming or case changes -- that is the sanitizer's
            job, not this class's).
        """
        return input()
