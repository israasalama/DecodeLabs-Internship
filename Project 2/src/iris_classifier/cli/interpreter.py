"""Command interpreter for conversational CLI input."""

from typing import Any

from iris_classifier.logger import get_logger


class CommandInterpreter:
    """Parses natural command strings into application actions."""

    def __init__(self) -> None:
        self.logger = get_logger()

    def parse(self, raw_command: str) -> tuple[str, dict[str, Any]]:
        """Parse raw command text into action and arguments."""
        normalized = raw_command.lower().strip()
        tokens = normalized.split()

        if not tokens:
            return "none", {}

        first = tokens[0]
        self.logger.debug(f"Parsing command: {normalized}")

        if first in {"exit", "quit", "bye"}:
            return "exit", {}

        if first in {"back", "menu"}:
            return "back", {}

        if first in {"help", "h", "?"}:
            return "help", {"topic": tokens[1] if len(tokens) > 1 else None}

        if first in {"load", "dataset", "load_data", "load dataset"}:
            return "load_data", {}

        if first in {"preprocess", "prepare", "split"}:
            return "preprocess", {}

        if first in {"train", "fit"}:
            algorithm = "knn"
            k = None
            if len(tokens) > 1 and tokens[1] in {"knn", "logistic", "tree"}:
                algorithm = tokens[1]
            if len(tokens) > 2:
                try:
                    k = int(tokens[2])
                except ValueError:
                    pass
            return "train", {"algorithm": algorithm, "k": k}

        if first in {"evaluate", "eval", "score", "test"}:
            return "evaluate", {}

        if first in {"predict", "infer"}:
            values = []
            for token in tokens[1:]:
                try:
                    values.append(float(token))
                except ValueError:
                    continue
            return "predict", {"values": values}

        if first in {"tune", "grid", "search"}:
            return "tune_k", {}

        if first in {"session", "status", "info"}:
            return "session_info", {}

        if first in {"history", "log", "commands"}:
            return "history", {}

        if first in {"reset", "clear"}:
            return "reset", {}

        if first == "mode":
            mode = tokens[1] if len(tokens) > 1 else None
            return "set_mode", {"mode": mode}

        return "unknown", {"raw": raw_command}

    def help_text(self, topic: str | None = None) -> str:
        """Return help text for general or specific topics."""
        if topic in {"train", "knn", "logistic", "tree"}:
            return (
                "Use 'train knn 3' to train a KNN model, 'train logistic' for Logistic Regression, "
                "or 'train tree' for a Decision Tree."
            )

        if topic in {"predict", "infer"}:
            return "Use 'predict 5.1 3.5 1.4 0.2' to classify a new iris sample."

        if topic == "mode":
            return "Use 'mode friendly' or 'mode professional' to change CLI personality."

        return (
            "Available commands: load, preprocess, train, evaluate, predict, tune, history, "
            "session, reset, mode, help, exit. Example: 'train knn 5'."
        )
