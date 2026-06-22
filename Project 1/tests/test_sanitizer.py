"""Unit tests for InputSanitizer."""

from src.input.sanitizer import InputSanitizer


class TestSanitize:
    """Tests for InputSanitizer.sanitize()."""

    def setup_method(self) -> None:
        self.sanitizer = InputSanitizer()

    def test_lowercases_mixed_case_input(self) -> None:
        assert self.sanitizer.sanitize("HeLLo") == "hello"

    def test_strips_leading_and_trailing_whitespace(self) -> None:
        assert self.sanitizer.sanitize("  HeLLo  ") == "hello"

    def test_strips_only_internal_spacing_is_preserved(self) -> None:
        # Internal spacing between words must NOT be collapsed.
        assert self.sanitizer.sanitize("  how ARE you  ") == "how are you"

    def test_uppercase_exit_command_normalizes(self) -> None:
        assert self.sanitizer.sanitize("EXIT") == "exit"
        assert self.sanitizer.sanitize("  Exit  ") == "exit"

    def test_empty_string_stays_empty(self) -> None:
        assert self.sanitizer.sanitize("") == ""

    def test_whitespace_only_becomes_empty(self) -> None:
        assert self.sanitizer.sanitize("   ") == ""

    def test_does_not_crash_on_special_characters(self) -> None:
        result = self.sanitizer.sanitize("héllo!@#$%^&*()")
        assert result == "héllo!@#$%^&*()"

    def test_does_not_crash_on_very_long_input(self) -> None:
        long_input = "a" * 10_000
        result = self.sanitizer.sanitize(f"  {long_input}  ")
        assert result == long_input


class TestIsEmpty:
    """Tests for InputSanitizer.is_empty()."""

    def setup_method(self) -> None:
        self.sanitizer = InputSanitizer()

    def test_empty_string_is_empty(self) -> None:
        assert self.sanitizer.is_empty("") is True

    def test_non_empty_string_is_not_empty(self) -> None:
        assert self.sanitizer.is_empty("hello") is False

    def test_already_sanitized_whitespace_only_input(self) -> None:
        # is_empty expects already-sanitized text, so a pre-stripped
        # whitespace-only string becomes "".
        clean = self.sanitizer.sanitize("    ")
        assert self.sanitizer.is_empty(clean) is True
