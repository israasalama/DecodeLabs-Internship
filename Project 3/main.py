"""
Entry point for the Tech Stack Recommender.

Usage:
    python main.py
"""

import logging
import sys

from src.config import LOG_DIR, LOG_FILE
from src.interface.cli import RecommenderCLI


def _configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )


def main() -> int:
    _configure_logging()
    cli = RecommenderCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
