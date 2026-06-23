"""Entry point for the Iris Flower Classification System."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from iris_classifier.cli.app import IrisClassifierApp
from iris_classifier.logger import get_logger


def main() -> None:
    """Main entry point."""
    try:
        logger = get_logger()
        logger.info("Application started")

        app = IrisClassifierApp()
        app.run()

        logger.info("Application ended normally")
    except KeyboardInterrupt:
        print("\n\nApplication interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
