"""Tests for CLI command interpreter and response personalities."""

import pytest

from iris_classifier.cli.interpreter import CommandInterpreter
from iris_classifier.cli.responses import ResponseManager


class TestCommandInterpreter:
    """Tests for conversational command parsing."""

    def setup_method(self) -> None:
        self.interpreter = CommandInterpreter()

    def test_parse_exit_command(self):
        action, params = self.interpreter.parse("exit")
        assert action == "exit"
        assert params == {}

    def test_parse_train_knn_with_k(self):
        action, params = self.interpreter.parse("train knn 5")
        assert action == "train"
        assert params["algorithm"] == "knn"
        assert params["k"] == 5

    def test_parse_predict_values(self):
        action, params = self.interpreter.parse("predict 5.1 3.5 1.4 0.2")
        assert action == "predict"
        assert params["values"] == [5.1, 3.5, 1.4, 0.2]

    def test_parse_mode_command(self):
        action, params = self.interpreter.parse("mode friendly")
        assert action == "set_mode"
        assert params["mode"] == "friendly"

    def test_parse_unknown_command(self):
        action, params = self.interpreter.parse("fly away")
        assert action == "unknown"
        assert params["raw"] == "fly away"

    def test_parse_back_command(self):
        action, params = self.interpreter.parse("back")
        assert action == "back"
        assert params == {}

    def test_help_text_default(self):
        help_message = self.interpreter.help_text()
        assert "Available commands" in help_message

    def test_help_text_specific(self):
        help_message = self.interpreter.help_text("predict")
        assert "predict 5.1 3.5 1.4 0.2" in help_message


class TestResponseManager:
    """Tests for personality-based response handling."""

    def setup_method(self) -> None:
        self.manager = ResponseManager()

    def test_default_mode_is_configured(self):
        assert self.manager.get_mode() in {"professional", "friendly"}

    def test_format_welcome_message(self):
        welcome = self.manager.format("welcome")
        assert isinstance(welcome, str)
        assert welcome

    def test_set_mode_changes_personality(self):
        self.manager.set_mode("friendly")
        assert self.manager.get_mode() == "friendly"
        assert "flower classifier" in self.manager.format("welcome").lower()

    def test_set_mode_invalid_raises(self):
        with pytest.raises(ValueError):
            self.manager.set_mode("robotic")
