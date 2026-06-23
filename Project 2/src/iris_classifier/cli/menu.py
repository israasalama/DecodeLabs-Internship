"""Menu system for CLI interactions."""

from typing import Callable, Dict, Optional

from iris_classifier.logger import get_logger


class MenuOption:
    """Represents a single menu option."""

    def __init__(self, key: str, label: str, handler: Callable[[], None]) -> None:
        """Initialize menu option.

        Args:
            key: Single character key for selection.
            label: Display label.
            handler: Callback function when selected.
        """
        self.key = key
        self.label = label
        self.handler = handler


class Menu:
    """Interactive menu system."""

    def __init__(self, title: str) -> None:
        """Initialize menu.

        Args:
            title: Menu title.
        """
        self.title = title
        self.options: Dict[str, MenuOption] = {}
        self.logger = get_logger()

    def add_option(self, key: str, label: str, handler: Callable[[], None]) -> None:
        """Add menu option.

        Args:
            key: Single character key.
            label: Display label.
            handler: Callback function.
        """
        self.options[key.lower()] = MenuOption(key.lower(), label, handler)

    def display(self) -> None:
        """Display menu to user."""
        print(f"\n{'=' * 50}")
        print(f"  {self.title}")
        print(f"{'=' * 50}")

        for key in sorted(self.options.keys()):
            option = self.options[key]
            print(f"  [{key.upper()}] {option.label}")

        print(f"{'=' * 50}")

    def get_choice(self) -> str:
        """Get user's menu choice.

        Returns:
            Selected option key.
        """
        while True:
            choice = input("\nEnter your choice: ").lower().strip()

            if choice in self.options:
                return choice

            print("❌ Invalid choice. Please try again.")

    def execute_choice(self, choice: str) -> bool:
        """Execute selected option.

        Args:
            choice: Selected option key.

        Returns:
            True if executed, False if not found.
        """
        if choice in self.options:
            try:
                self.options[choice].handler()
                return True
            except Exception as e:
                print(f"❌ Error: {e}")
                self.logger.error(f"Menu option error: {e}")
                return False

        return False

    def run(self) -> None:
        """Run interactive menu loop."""
        while True:
            self.display()
            choice = self.get_choice()

            if not self.execute_choice(choice):
                print("Option not found")


class MenuBuilder:
    """Fluent API for building menus."""

    def __init__(self, title: str) -> None:
        """Initialize builder.

        Args:
            title: Menu title.
        """
        self.menu = Menu(title)

    def with_option(self, key: str, label: str, handler: Callable[[], None]) -> "MenuBuilder":
        """Add option to menu.

        Args:
            key: Single character key.
            label: Display label.
            handler: Callback function.

        Returns:
            Self for chaining.
        """
        self.menu.add_option(key, label, handler)
        return self

    def build(self) -> Menu:
        """Build and return menu.

        Returns:
            Constructed Menu object.
        """
        return self.menu
