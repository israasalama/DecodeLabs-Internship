"""Tests for CLI menu system."""

import pytest

from iris_classifier.cli.menu import Menu, MenuOption, MenuBuilder


class TestMenuOption:
    """Tests for MenuOption."""

    def test_menu_option_creation(self):
        """Test creating menu option."""
        def handler():
            pass

        option = MenuOption("a", "Test Option", handler)

        assert option.key == "a"
        assert option.label == "Test Option"
        assert option.handler == handler


class TestMenu:
    """Tests for Menu."""

    def test_menu_creation(self):
        """Test creating menu."""
        menu = Menu("Test Menu")
        assert menu.title == "Test Menu"
        assert len(menu.options) == 0

    def test_add_single_option(self):
        """Test adding single menu option."""
        menu = Menu("Test")

        def handler():
            pass

        menu.add_option("a", "Option A", handler)
        assert "a" in menu.options

    def test_add_multiple_options(self):
        """Test adding multiple options."""
        menu = Menu("Test")

        def handler1():
            pass

        def handler2():
            pass

        menu.add_option("a", "Option A", handler1)
        menu.add_option("b", "Option B", handler2)

        assert len(menu.options) == 2
        assert "a" in menu.options
        assert "b" in menu.options

    def test_option_case_insensitive(self):
        """Test that options are case-insensitive."""
        menu = Menu("Test")

        def handler():
            pass

        menu.add_option("A", "Option", handler)
        assert "a" in menu.options

    def test_execute_valid_choice(self):
        """Test executing valid menu choice."""
        called = False

        def handler():
            nonlocal called
            called = True

        menu = Menu("Test")
        menu.add_option("a", "Test", handler)

        result = menu.execute_choice("a")
        assert result is True
        assert called is True

    def test_execute_invalid_choice(self):
        """Test executing invalid choice."""
        menu = Menu("Test")

        result = menu.execute_choice("z")
        assert result is False

    def test_display_output(self, capsys):
        """Test menu display output."""
        menu = Menu("Test Menu")
        menu.add_option("a", "Option A", lambda: None)
        menu.add_option("b", "Option B", lambda: None)

        menu.display()

        captured = capsys.readouterr()
        assert "Test Menu" in captured.out
        assert "Option A" in captured.out
        assert "Option B" in captured.out

    def test_handler_exception_handling(self):
        """Test exception handling in handler execution."""
        def failing_handler():
            raise ValueError("Test error")

        menu = Menu("Test")
        menu.add_option("a", "Failing Option", failing_handler)

        result = menu.execute_choice("a")
        # Should not raise, but return False due to exception
        assert result is False


class TestMenuBuilder:
    """Tests for MenuBuilder."""

    def test_builder_creation(self):
        """Test creating builder."""
        builder = MenuBuilder("Test")
        assert builder.menu.title == "Test"

    def test_builder_chaining(self):
        """Test method chaining."""
        builder = (
            MenuBuilder("Test")
            .with_option("a", "Option A", lambda: None)
            .with_option("b", "Option B", lambda: None)
        )

        menu = builder.build()
        assert len(menu.options) == 2

    def test_builder_build_returns_menu(self):
        """Test that build returns Menu object."""
        builder = MenuBuilder("Test")
        menu = builder.build()

        assert isinstance(menu, Menu)
        assert menu.title == "Test"
