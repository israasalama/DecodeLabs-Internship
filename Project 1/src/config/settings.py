"""Application configuration.

Every "magic string" the chatbot depends on (the exit keyword, the
fallback message, terminal labels, etc.) lives here instead of being
scattered through the codebase. Centralizing config means a change
like renaming the exit command happens in exactly one place.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Immutable container for chatbot runtime settings.

    Using a frozen dataclass means once an AppConfig is created, its
    values cannot be accidentally changed later in the program -- this
    protects against bugs where one part of the app mutates settings
    that another part depends on.

    Attributes:
        exit_command: The sanitized keyword that ends the session.
        fallback_response: Reply shown when no intent matches.
        user_prompt: Label shown before the user types input.
        bot_prefix: Label shown before the bot's reply.
        min_intents: Minimum number of knowledge-base entries required
            for the bot to be considered valid (per FR-3).
    """

    exit_command: str = "exit"
    fallback_response: str = "I do not understand."
    user_prompt: str = "You: "
    bot_prefix: str = "Bot: "
    min_intents: int = 5
