"""
The Tech Stack Recommender pipeline.

Orchestrates the exact 4-step pipeline specified on Page 17:

    1. Ingestion  -- capture and validate the user's skill input
    2. Scoring    -- compute cosine similarity against every job role
    3. Sorting    -- order roles by descending similarity
    4. Filtering  -- truncate to the Top-N list

Also implements the Cold Start fallback (Pages 20-21): if the user's
profile has zero meaningful overlap with the dataset, we don't show an
error -- we fall back to a "Trending Roles" list instead.
"""

import logging

from src.config import (
    COLD_START_THRESHOLD,
    MIN_SKILLS_REQUIRED,
    TOP_N_RESULTS,
    TRENDING_FALLBACK_COUNT,
)
from src.core.normalizer import SkillNormalizer
from src.core.similarity import CosineSimilarity
from src.core.vectorizer import TfidfVectorizer
from src.data_layer.models import JobRole, RecommendationResult
from src.data_layer.repository import SkillsRepository
from src.exceptions import InsufficientSkillsError

logger = logging.getLogger(__name__)


class TechStackRecommender:
    """
    High-level facade that ties together normalization, vectorization,
    and similarity scoring into a single `recommend()` call.
    """

    def __init__(
        self,
        repository: SkillsRepository,
        normalizer: SkillNormalizer | None = None,
        vectorizer: TfidfVectorizer | None = None,
    ) -> None:
        self._repository = repository
        self._normalizer = normalizer or SkillNormalizer()
        self._vectorizer = vectorizer or TfidfVectorizer()
        self._job_roles: list[JobRole] = []

    def load_data(self) -> None:
        """Load and cache job-role data from the repository."""
        self._job_roles = self._repository.load()
        logger.info("Loaded %d job roles from dataset.", len(self._job_roles))

    @property
    def job_roles(self) -> list[JobRole]:
        """Read-only access to the currently loaded job roles."""
        return list(self._job_roles)

    def recommend(
        self, user_skills: list[str], top_n: int = TOP_N_RESULTS
    ) -> list[RecommendationResult]:
        """
        Run the full 4-step pipeline and return ranked recommendations.

        Args:
            user_skills: Raw skill strings provided by the user.
            top_n: How many top results to return.

        Returns:
            A list of RecommendationResult, best match first. If the
            user's profile has no meaningful overlap with any job role
            (Cold Start), falls back to a "trending" (alphabetical, as
            a simple stand-in for popularity) list instead of an
            empty/error response.

        Raises:
            InsufficientSkillsError: If fewer than MIN_SKILLS_REQUIRED
                skills are provided.
        """
        # --- Step 1: Ingestion ---------------------------------------
        if len(user_skills) < MIN_SKILLS_REQUIRED:
            raise InsufficientSkillsError(
                f"At least {MIN_SKILLS_REQUIRED} skills are required, "
                f"but only {len(user_skills)} were provided."
            )

        normalized_user_skills = self._normalizer.normalize_all(user_skills)
        logger.info("Normalized user skills: %s", normalized_user_skills)

        if not self._job_roles:
            self.load_data()

        # Build the shared vocabulary from job-role documents only.
        # (The user profile is transformed into this space, not fitted
        # into it -- this mirrors how a real system treats new query
        # data against an existing, stable item catalog.)
        documents = [role.skills for role in self._job_roles]
        self._vectorizer.fit(documents)

        # --- Step 2: Scoring -------------------------------------------
        user_vector = self._vectorizer.transform(normalized_user_skills)
        results = self._score_all_roles(user_vector)

        total_score = sum(result.score for result in results)
        if total_score < COLD_START_THRESHOLD:
            logger.warning(
                "Cold Start detected: user skills have no overlap with "
                "dataset vocabulary. Falling back to trending roles."
            )
            return self._trending_fallback(top_n)

        # --- Step 3: Sorting --------------------------------------------
        results.sort(key=lambda r: (-r.score, r.role_name))

        # --- Step 4: Filtering --------------------------------------------
        return results[:top_n]

    def _score_all_roles(self, user_vector: list[float]) -> list[RecommendationResult]:
        """Compute cosine similarity between the user vector and every role."""
        results: list[RecommendationResult] = []
        for role in self._job_roles:
            role_vector = self._vectorizer.transform(role.skills)
            score = CosineSimilarity.compute(user_vector, role_vector)
            results.append(RecommendationResult(role_name=role.name, score=score))
        return results

    def _trending_fallback(self, top_n: int) -> list[RecommendationResult]:
        """
        Cold Start bypass strategy (Page 21): "Trending Fallbacks."

        In the absence of real popularity/interaction data, we use
        alphabetical order as a deterministic, explainable stand-in so
        the user always receives *something* useful rather than an
        empty result.
        """
        sorted_roles = sorted(self._job_roles, key=lambda r: r.name)
        fallback_count = min(top_n, TRENDING_FALLBACK_COUNT, len(sorted_roles))
        return [
            RecommendationResult(role_name=role.name, score=0.0)
            for role in sorted_roles[:fallback_count]
        ]
