"""Configuration management for the Iris Classification System."""

from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigManager:
    """Handles loading and validation of application configuration from YAML."""

    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"

    def __init__(self, config_path: str | Path | None = None) -> None:
        """Initialize ConfigManager and load configuration.

        Args:
            config_path: Path to YAML configuration file.
                        Defaults to config.yaml in project root.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValueError: If config is invalid.
        """
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_PATH)
        self.config: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load and validate configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config: {e}") from e

        self._validate()

    def _validate(self) -> None:
        """Validate required configuration keys exist."""
        required_sections = ["application", "ml", "logging", "cli"]
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve config value using dot notation.

        Args:
            key: Config key in format 'section.key' or 'section.subsection.key'.
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        parts = key.split(".")
        value = self.config

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_ml_config(self) -> Dict[str, Any]:
        """Get ML-specific configuration."""
        return self.config.get("ml", {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging-specific configuration."""
        return self.config.get("logging", {})


# Global instance
_config_manager: ConfigManager | None = None


def get_config_manager(config_path: str | Path | None = None) -> ConfigManager:
    """Get or create global ConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager
