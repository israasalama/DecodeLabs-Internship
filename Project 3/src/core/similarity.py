"""
Cosine Similarity engine.

Implements the formula specified (Page 15):

    cos(theta) = (A . B) / (||A|| * ||B||)

Chosen over Euclidean distance because the spec explicitly demonstrates
(Page 14) that Euclidean distance is sensitive to vector magnitude,
which produces inaccurate results when comparing items of very
different "sizes" (e.g. a user with 3 skills vs. a job role with 10).
Cosine similarity is magnitude-invariant -- it measures orientation
(angle), not length -- which is exactly the property we need.

This module is intentionally domain-agnostic: it knows nothing about
skills or job roles, only about vectors of floats. That makes it
trivially unit-testable and reusable elsewhere.
"""

import math


class CosineSimilarity:
    """Stateless cosine similarity calculator for equal-length vectors."""

    @staticmethod
    def compute(vector_a: list[float], vector_b: list[float]) -> float:
        """
        Compute the cosine similarity between two vectors.

        Args:
            vector_a: First vector.
            vector_b: Second vector. Must be the same length as vector_a.

        Returns:
            A similarity score. With non-negative TF-IDF inputs, this
            naturally falls in [0.0, 1.0] (Page 16). Returns 0.0 if
            either vector has zero magnitude (no signal to compare).

        Raises:
            ValueError: If the vectors have mismatched lengths.
        """
        if len(vector_a) != len(vector_b):
            raise ValueError(
                f"Vector length mismatch: {len(vector_a)} vs {len(vector_b)}. "
                "Both vectors must be aligned to the same vocabulary space."
            )

        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))

        if magnitude_a == 0.0 or magnitude_b == 0.0:
            # One vector has no weighted terms at all -- e.g. a Cold
            # Start user profile (Page 20). No orientation to compare.
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)
