"""Lightweight tests for the output layer (presenter + banner).

The design treats this layer as "manual smoke test only / lightweight
test if desired" since it has no business logic -- these tests simply
confirm the correct text reaches stdout.
"""

from pathlib import Path

import pytest

from src.output.banner import BannerRenderer
from src.output.presenter import TerminalPresenter


class TestTerminalPresenter:
    """Tests for TerminalPresenter output formatting."""

    def setup_method(self) -> None:
        self.presenter = TerminalPresenter(bot_prefix="Bot: ", user_prompt="You: ")

    def test_show_response_includes_bot_prefix(self, capsys: pytest.CaptureFixture) -> None:
        self.presenter.show_response("Hi there!")
        captured = capsys.readouterr()
        assert captured.out == "Bot: Hi there!\n"

    def test_show_goodbye_prints_farewell(self, capsys: pytest.CaptureFixture) -> None:
        self.presenter.show_goodbye()
        captured = capsys.readouterr()
        assert "Bot: " in captured.out
        assert "Session ended" in captured.out

    def test_show_prompt_prints_user_label(self, capsys: pytest.CaptureFixture) -> None:
        self.presenter.show_prompt()
        captured = capsys.readouterr()
        assert captured.out == "You: "

    def test_show_error_does_not_raise(self, capsys: pytest.CaptureFixture) -> None:
        self.presenter.show_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Something went wrong" in captured.out


class TestBannerRenderer:
    """Tests for BannerRenderer."""

    def test_renders_existing_banner_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        banner_file = tmp_path / "banner.txt"
        banner_file.write_text("WELCOME", encoding="utf-8")
        renderer = BannerRenderer(banner_file)
        renderer.render()
        captured = capsys.readouterr()
        assert "WELCOME" in captured.out

    def test_missing_banner_file_does_not_crash(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        missing_path = tmp_path / "does_not_exist.txt"
        renderer = BannerRenderer(missing_path)
        renderer.render()  # Should not raise.
        captured = capsys.readouterr()
        assert captured.out != ""
