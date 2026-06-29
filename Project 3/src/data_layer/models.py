"""
Data models for the recommender's data layer.

These are plain, immutable dataclasses -- they hold data and have no
business logic. This keeps the data layer "dumb" on purpose: all
intelligence lives in the core/ and pipeline/ layers.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobRole:
    """
    Represents a single job role "item" in the recommendation engine.

    Attributes:
        name: Human-readable role name, e.g. "DevOps Engineer".
        skills: The list of normalized skill tags that define this role.
    """

    name: str
    skills: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("JobRole name must not be empty.")
        if not self.skills:
            raise ValueError(f"JobRole '{self.name}' must have at least one skill.")


@dataclass(frozen=True)
class RecommendationResult:
    """
    Represents a single scored recommendation returned to the user.

    Attributes:
        role_name: The recommended job role's name.
        score: Cosine similarity score in the range [0.0, 1.0].
    """

    role_name: str
    score: float

    def as_percentage(self) -> str:
        """Render the score as a human-friendly percentage string."""
        return f"{self.score * 100:.1f}%"
