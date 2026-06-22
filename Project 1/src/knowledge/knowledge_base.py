"""The chatbot's knowledge base: a dictionary of known intents.

This is the "brain" of the rule-based system, but deliberately a very
simple one -- a Python dict. Looking a key up in a dict is an O(1)
operation (constant time, regardless of how many intents exist),
which is why the spec prefers `dict.get()` over a long chain of
if/elif statements (which would be O(n): slower as it grows, and
harder to read).

PORTFOLIO UPGRADE: this version supports multiple "personality modes"
(neutral / friendly / professional) and intent aliases (multiple
phrasings mapping to one canonical intent), while keeping the exact
same public interface the rest of the system already depends on.
"""

from src.config.settings import AppConfig

# Each personality is a complete, self-contained set of intents.
# Adding a new personality means adding one new dict here -- no other
# file needs to change.
_PERSONALITIES: dict[str, dict[str, str]] = {
    "neutral": {
        "hello": "Hi there! Welcome to the Logic Engine.",
        "hi": "Hello! How can I help you today?",
        "hey": "Hello! How can I help you today?",
        "good morning": "Good morning! Ready when you are.",
        "good evening": "Good evening! How can I help?",
        "help": (
            "Supported commands: hello, hi, help, bye, how are you, "
            "what can you do, your name, who made you, thanks, joke, "
            "history, clear, mode, exit."
        ),
        "what can you do": (
            "I match your message against a fixed set of rules and "
            "reply with a pre-written response. No guessing, no AI "
            "model -- just deterministic logic."
        ),
        "your name": "I'm the Logic Engine, a rule-based chatbot.",
        "who made you": "I was built as Project 1 of the DecodeLabs AI track.",
        "bye": "Goodbye! Have a great day.",
        "how are you": "I'm running on deterministic logic - always consistent!",
        "thanks": "You're welcome!",
        "thank you": "You're welcome!",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs.",
    },
    "friendly": {
        "hello": "Heyyy! So glad you're here :) What's up?",
        "hi": "Hii! What can I do for you today?",
        "hey": "Heyy! What's going on?",
        "good morning": "Good morniiing! Hope today treats you well!",
        "good evening": "Good evening! Cozy chat time, huh?",
        "help": (
            "Sure thing! You can try: hello, hi, help, bye, how are you, "
            "what can you do, your name, who made you, thanks, joke, "
            "history, clear, mode, exit."
        ),
        "what can you do": (
            "Honestly? I just follow a script of rules -- but I follow "
            "it really enthusiastically!"
        ),
        "your name": "People call me the Logic Engine! Nice to meet you.",
        "who made you": "An intern built me for the DecodeLabs AI program!",
        "bye": "Aww, bye! Come back soon, okay?",
        "how are you": "Doing great -- consistently great, every single time!",
        "thanks": "Anytime, friend!",
        "thank you": "Anytime, friend!",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    },
    "professional": {
        "hello": "Good day. How may I assist you?",
        "hi": "Hello. Please let me know how I can help.",
        "hey": "Hello. How can I assist you?",
        "good morning": "Good morning. I am ready to assist.",
        "good evening": "Good evening. How may I help?",
        "help": (
            "Available commands: hello, hi, help, bye, how are you, "
            "what can you do, your name, who made you, thanks, joke, "
            "history, clear, mode, exit."
        ),
        "what can you do": (
            "I respond to a predefined set of inputs using deterministic "
            "rule-matching. I do not use machine learning."
        ),
        "your name": "I am referred to as the Logic Engine.",
        "who made you": "I was developed as Project 1 of the DecodeLabs AI program.",
        "bye": "Goodbye. Have a productive day.",
        "how are you": "Operating normally. My behavior is fully deterministic.",
        "thanks": "You are welcome.",
        "thank you": "You are welcome.",
        "joke": "Programmers prefer dark mode because light attracts bugs.",
    },
}

DEFAULT_PERSONALITY = "neutral"


class KnowledgeBase:
    """Stores intent -> response mappings and serves lookups.

    The `exit` command is intentionally NOT stored here. It is
    handled by `ExitDetector` instead, keeping "end the program" logic
    separate from "answer a question" logic (single-responsibility).
    """

    def __init__(self, config: AppConfig, personality: str = DEFAULT_PERSONALITY) -> None:
        """Initialize the knowledge base with a seed set of intents.

        Args:
            config: Application configuration, used for the fallback
                response and the minimum-intents threshold.
            personality: Which response set to load. Falls back to
                `DEFAULT_PERSONALITY` if the name is not recognized,
                rather than raising -- an unknown personality should
                never crash the app (NFR-4).
        """
        self._config = config
        self._personality = personality if personality in _PERSONALITIES else DEFAULT_PERSONALITY
        self._intents: dict[str, str] = dict(_PERSONALITIES[self._personality])

    @property
    def personality(self) -> str:
        """Return the name of the currently active personality."""
        return self._personality

    def set_personality(self, personality: str) -> bool:
        """Switch to a different personality's response set.

        Args:
            personality: One of the keys in `available_personalities()`.

        Returns:
            True if the switch succeeded, False if the name was not
            recognized (in which case the current personality is left
            unchanged -- a typo should not crash the session).
        """
        if personality not in _PERSONALITIES:
            return False
        self._personality = personality
        self._intents = dict(_PERSONALITIES[personality])
        return True

    @staticmethod
    def available_personalities() -> list[str]:
        """Return the names of all personalities that can be selected."""
        return list(_PERSONALITIES.keys())

    def get_response(self, key: str) -> str:
        """Look up a response for a sanitized key, or return the fallback.

        Args:
            key: A sanitized (lowercase, stripped) input string.

        Returns:
            The mapped response if `key` is a known intent, otherwise
            the configured fallback response. Using `.get()` combines
            the lookup and the fallback into a single atomic operation
            (FR-11), rather than checking `if key in dict` and then
            indexing separately.
        """
        return self._intents.get(key, self._config.fallback_response)

    def has_intent(self, key: str) -> bool:
        """Check whether a sanitized key is a registered intent.

        Args:
            key: A sanitized input string.

        Returns:
            True if `key` exists in the knowledge base.
        """
        return key in self._intents

    def list_intents(self) -> list[str]:
        """Return all registered intent keys.

        Returns:
            A list of every key currently in the knowledge base.
        """
        return list(self._intents.keys())

    def validate(self) -> bool:
        """Check that the knowledge base meets the minimum size requirement.

        Returns:
            True if the number of intents is at least
            `config.min_intents` (FR-3), otherwise False.
        """
        return len(self._intents) >= self._config.min_intents
