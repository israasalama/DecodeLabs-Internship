"""Personality-based response management for the CLI."""

from typing import Any

from iris_classifier.config import get_config_manager
from iris_classifier.logger import get_logger


class ResponseManager:
    """Manages configurable response templates across personality modes."""

    DEFAULT_TEMPLATES = {
        "professional": {
            "welcome": "Welcome to the Iris Flower Classification System.",
            "goodbye": "Thank you for using the Iris classifier. Goodbye!",
            "load_start": "Loading Iris dataset...",
            "load_success": "Dataset loaded successfully.",
            "preprocess_start": "Preprocessing dataset (split + scale)...",
            "preprocess_success": "Preprocessing complete.",
            "train_start": "Training model...",
            "train_success": "Model trained successfully.",
            "evaluate_start": "Evaluating model on test set...",
            "evaluate_success": "Evaluation complete.",
            "predict_prompt": "Please provide sample measurements.",
            "predict_success": "Prediction complete.",
            "tune_start": "Tuning K values...",
            "tune_success": "K tuning finished.",
            "unknown_command": "I did not understand that command. Type 'help' for options.",
            "invalid_input": "Invalid input detected. Please try again.",
            "mode_changed": "Personality changed to {mode}.",
            "current_mode": "Current personality mode: {mode}.",
            "command_mode_header": "Conversational command mode enabled. Type 'help' for instructions.",
            "exit_command_mode": "Exiting command mode.",
            "help_text": "Available commands: load, preprocess, train, evaluate, predict, tune, history, session, reset, mode, help, exit.",
        },
        "friendly": {
            "welcome": "Hey there! Ready to explore the Iris flower classifier?",
            "goodbye": "Thanks for stopping by! Have a great day.",
            "load_start": "Let's load the Iris data.",
            "load_success": "Sweet! The dataset is ready.",
            "preprocess_start": "Now we're preprocessing the data.",
            "preprocess_success": "Nice! Preprocessing is done.",
            "train_start": "Time to train your model.",
            "train_success": "Awesome! The model is trained.",
            "evaluate_start": "Evaluating performance now.",
            "evaluate_success": "Done! Here's how it performed.",
            "predict_prompt": "Tell me the flower measurements.",
            "predict_success": "Prediction is ready!",
            "tune_start": "Let's find the best K value.",
            "tune_success": "Tuning complete — best K selected.",
            "unknown_command": "Hmm, I couldn't understand that. Try 'help' for tips.",
            "invalid_input": "Oops! That input didn't work. Please try again.",
            "mode_changed": "Great! Personality is now {mode}.",
            "current_mode": "You're in {mode} mode.",
            "command_mode_header": "Command mode is on! Type 'help' if you need it.",
            "exit_command_mode": "You're back to the normal menu.",
            "help_text": "Try commands like 'train knn 3', 'predict 5.1 3.5 1.4 0.2', or 'mode friendly'.",
        },
    }

    def __init__(self) -> None:
        self.logger = get_logger()
        config = get_config_manager()
        self.personality_mode = config.get("cli.default_personality", "professional")
        self.templates = self.DEFAULT_TEMPLATES

        if self.personality_mode not in self.templates:
            self.logger.warning(f"Unknown personality mode: {self.personality_mode}. Falling back to professional.")
            self.personality_mode = "professional"

    def format(self, key: str, **kwargs: Any) -> str:
        """Format a response using the current personality.

        Args:
            key: Template key.
            kwargs: Variables for substitution.

        Returns:
            Formatted response string.
        """
        templates = self.templates.get(self.personality_mode, {})
        text = templates.get(key) or self.DEFAULT_TEMPLATES["professional"].get(key, "")
        return text.format(**kwargs)

    def set_mode(self, mode: str) -> None:
        """Change the personality mode."""
        normalized = mode.lower().strip()
        if normalized in self.templates:
            self.personality_mode = normalized
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def get_mode(self) -> str:
        """Get the current personality mode."""
        return self.personality_mode
