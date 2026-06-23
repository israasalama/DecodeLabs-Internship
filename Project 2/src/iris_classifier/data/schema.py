"""Data schema definitions for the Iris classification system."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class IrisSample:
    """Represents a single iris flower sample with validation."""

    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: Optional[str] = None

    def validate(self) -> None:
        """Validate all measurements are numeric and positive.

        Raises:
            ValueError: If any measurement is invalid.
        """
        measurements = {
            "sepal_length": self.sepal_length,
            "sepal_width": self.sepal_width,
            "petal_length": self.petal_length,
            "petal_width": self.petal_width,
        }

        for name, value in measurements.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric, got {type(value).__name__}")
            if value < 0:
                raise ValueError(f"{name} must be positive, got {value}")

    def to_array(self) -> list[float]:
        """Convert sample to feature array.

        Returns:
            List of [sepal_length, sepal_width, petal_length, petal_width].
        """
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width,
        ]

    def __repr__(self) -> str:
        """String representation of sample."""
        base = f"IrisSample(sepal_length={self.sepal_length}, sepal_width={self.sepal_width}, petal_length={self.petal_length}, petal_width={self.petal_width}"
        if self.species:
            base += f", species={self.species}"
        return base + ")"


@dataclass
class Dataset:
    """Represents a loaded Iris dataset with metadata."""

    features: list[list[float]]
    labels: list[int]
    feature_names: list[str]
    target_names: list[str]
    sample_count: int = 0
    feature_count: int = 0

    def __post_init__(self) -> None:
        """Initialize metadata after dataclass initialization."""
        self.sample_count = len(self.labels)
        self.feature_count = len(self.feature_names)

    def summary(self) -> str:
        """Generate human-readable dataset summary.

        Returns:
            Formatted summary string.
        """
        class_counts = {target: sum(1 for label in self.labels if label == idx)
                       for idx, target in enumerate(self.target_names)}

        summary = f"Dataset Summary:\n"
        summary += f"  Samples: {self.sample_count}\n"
        summary += f"  Features: {self.feature_count}\n"
        summary += f"  Feature names: {', '.join(self.feature_names)}\n"
        summary += f"  Classes: {', '.join(self.target_names)}\n"
        summary += f"  Class distribution: {class_counts}\n"
        return summary
