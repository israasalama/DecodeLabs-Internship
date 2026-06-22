"""Unit tests for ExitDetector."""

from src.config.settings import AppConfig
from src.input.sanitizer import InputSanitizer
from src.process.exit_detector import ExitDetector


class TestIsExitCommand:
    """Tests for ExitDetector.is_exit_command()."""

    def setup_method(self) -> None:
        self.config = AppConfig()
        self.detector = ExitDetector(self.config)
        self.sanitizer = InputSanitizer()

    def test_exact_exit_keyword_returns_true(self) -> None:
        assert self.detector.is_exit_command("exit") is True

    def test_uppercase_exit_after_sanitization_returns_true(self) -> None:
        sanitized = self.sanitizer.sanitize("EXIT")
        assert self.detector.is_exit_command(sanitized) is True

    def test_mixed_case_with_spacing_after_sanitization_returns_true(self) -> None:
        sanitized = self.sanitizer.sanitize("  Exit  ")
        assert self.detector.is_exit_command(sanitized) is True

    def test_non_exit_word_returns_false(self) -> None:
        assert self.detector.is_exit_command("hello") is False

    def test_exit_synonym_bye_is_not_treated_as_exit(self) -> None:
        # "bye" is a knowledge-base intent, not the exit command,
        # unless explicitly configured otherwise.
        assert self.detector.is_exit_command("bye") is False

    def test_empty_string_returns_false(self) -> None:
        assert self.detector.is_exit_command("") is False

    def test_custom_exit_command_is_respected(self) -> None:
        custom_config = AppConfig(exit_command="quit")
        custom_detector = ExitDetector(custom_config)
        assert custom_detector.is_exit_command("quit") is True
        assert custom_detector.is_exit_command("exit") is False
