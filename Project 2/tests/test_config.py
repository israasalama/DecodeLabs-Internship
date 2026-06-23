"""Tests for configuration management."""

import pytest
import tempfile
from pathlib import Path

from iris_classifier.config import ConfigManager


@pytest.fixture
def valid_config_file():
    """Create a valid test config file."""
    content = """
application:
  name: "Test App"
  version: "1.0.0"

ml:
  random_seed: 42
  test_split_ratio: 0.2
  default_k: 3

logging:
  level: "INFO"
  log_file: "logs/test.log"

cli:
  show_warnings: true
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(content)
        f.flush()
        yield Path(f.name)
    Path(f.name).unlink()


@pytest.fixture
def invalid_yaml_file():
    """Create an invalid YAML file."""
    content = """
this is not: valid: yaml: syntax:
  - broken structure
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(content)
        f.flush()
        yield Path(f.name)
    Path(f.name).unlink()


class TestConfigManager:
    """Tests for ConfigManager."""

    def test_load_valid_config(self, valid_config_file):
        """Test loading valid configuration."""
        config = ConfigManager(valid_config_file)
        assert config.get("application.name") == "Test App"
        assert config.get("ml.random_seed") == 42

    def test_missing_required_section(self):
        """Test error handling for missing sections."""
        content = "application:\n  name: Test"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="Missing required config section"):
                ConfigManager(path)
        finally:
            path.unlink()

    def test_invalid_yaml_syntax(self, invalid_yaml_file):
        """Test error handling for invalid YAML."""
        with pytest.raises(ValueError, match="Invalid YAML"):
            ConfigManager(invalid_yaml_file)

    def test_missing_config_file(self):
        """Test error handling for missing config file."""
        with pytest.raises(FileNotFoundError):
            ConfigManager("/nonexistent/path/config.yaml")

    def test_get_nested_value(self, valid_config_file):
        """Test retrieving nested values with dot notation."""
        config = ConfigManager(valid_config_file)
        assert config.get("ml.default_k") == 3
        assert config.get("logging.level") == "INFO"

    def test_get_with_default(self, valid_config_file):
        """Test get with default value for missing key."""
        config = ConfigManager(valid_config_file)
        assert config.get("nonexistent.key", "default") == "default"
        assert config.get("nonexistent.key") is None

    def test_get_ml_config(self, valid_config_file):
        """Test getting ML config section."""
        config = ConfigManager(valid_config_file)
        ml_config = config.get_ml_config()
        assert ml_config["random_seed"] == 42
        assert ml_config["default_k"] == 3

    def test_get_logging_config(self, valid_config_file):
        """Test getting logging config section."""
        config = ConfigManager(valid_config_file)
        log_config = config.get_logging_config()
        assert log_config["level"] == "INFO"
