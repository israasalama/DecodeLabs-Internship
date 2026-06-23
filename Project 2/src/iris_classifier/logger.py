"""Logging service for experiment tracking and debugging."""

import logging
from pathlib import Path
from typing import Optional

from iris_classifier.config import get_config_manager


class LoggerService:
    """Centralized logging service for console and file output."""

    _instance: Optional["LoggerService"] = None

    def __new__(cls) -> "LoggerService":
        """Implement singleton pattern for logger."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize logger service once."""
        if self._initialized:
            return

        config = get_config_manager()
        log_config = config.get_logging_config()

        level = log_config.get("level", "INFO")
        log_file = log_config.get("log_file", "logs/experiment.log")
        fmt = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        self.logger = logging.getLogger("iris_classifier")
        self.logger.setLevel(getattr(logging, level))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))
        console_handler.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(console_handler)

        # File handler
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(file_handler)

        self._initialized = True

    def info(self, message: str) -> None:
        """Log info level message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning level message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error level message."""
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log debug level message."""
        self.logger.debug(message)


def get_logger() -> LoggerService:
    """Get or create global logger instance."""
    return LoggerService()
