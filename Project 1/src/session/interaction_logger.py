"""Optional traceability log for chatbot interactions.

This satisfies the "white-box" explainability requirement (NFR-2):
every turn the bot processes can be looked back on to see exactly
what was typed, how it was sanitized, how it was classified, and what
was said in response -- with nothing hidden.

PORTFOLIO UPGRADE: in addition to the original in-memory trace, this
logger can optionally append each turn to a log file on disk, so a
session's history survives after the program exits.
"""

from pathlib import Path

from src.core.enums import MatchType
from src.core.models import InteractionRecord


class InteractionLogger:
    """Stores a history of InteractionRecords for the current session."""

    def __init__(self, log_file_path: str | Path | None = None) -> None:
        """Initialize the logger with an empty in-memory history.

        Args:
            log_file_path: Optional path to a text file. If provided,
                every logged turn is also appended there as one line,
                in addition to being kept in memory. If the file can't
                be written (e.g. permissions), logging falls back to
                in-memory only rather than crashing the session
                (NFR-4).
        """
        self._records: list[InteractionRecord] = []
        self._log_file_path = Path(log_file_path) if log_file_path else None

    def log(
        self, raw_input: str, clean_input: str, match_type: MatchType, response_text: str
    ) -> None:
        """Record one completed turn.

        Args:
            raw_input: The exact text the user typed.
            clean_input: The sanitized version used for matching.
            match_type: How the turn was classified.
            response_text: What the bot replied with.
        """
        record = InteractionRecord(
            raw_input=raw_input,
            clean_input=clean_input,
            match_type=match_type,
            response_text=response_text,
        )
        self._records.append(record)
        self._write_to_file(record)

    def _write_to_file(self, record: InteractionRecord) -> None:
        """Append one record to the log file, if one was configured.

        Failures here are swallowed on purpose: file logging is a
        nice-to-have, not core chatbot functionality, so a disk error
        must never interrupt the conversation.
        """
        if self._log_file_path is None:
            return
        try:
            line = (
                f"{record.timestamp.isoformat()} | "
                f"raw={record.raw_input!r} | "
                f"clean={record.clean_input!r} | "
                f"type={record.match_type.name} | "
                f"response={record.response_text!r}\n"
            )
            with self._log_file_path.open("a", encoding="utf-8") as log_file:
                log_file.write(line)
        except OSError:
            pass

    def get_trace(self) -> list[InteractionRecord]:
        """Return the full interaction history for this session.

        Returns:
            A list of every `InteractionRecord` logged so far, in the
            order they occurred. Useful for debugging or testing
            without needing to parse printed terminal output.
        """
        return list(self._records)
