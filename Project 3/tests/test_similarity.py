"""Unit tests for CosineSimilarity. Pure math, no domain data needed."""

import math

import pytest

from src.core.similarity import CosineSimilarity


class TestCosineSimilarity:
    def test_identical_vectors_have_similarity_one(self) -> None:
        vector = [1.0, 2.0, 3.0]
        score = CosineSimilarity.compute(vector, vector)
        assert math.isclose(score, 1.0, rel_tol=1e-9)

    def test_orthogonal_vectors_have_similarity_zero(self) -> None:
        vector_a = [1.0, 0.0]
        vector_b = [0.0, 1.0]
        score = CosineSimilarity.compute(vector_a, vector_b)
        assert math.isclose(score, 0.0, abs_tol=1e-9)

    def test_opposite_vectors_have_similarity_negative_one(self) -> None:
        vector_a = [1.0, 0.0]
        vector_b = [-1.0, 0.0]
        score = CosineSimilarity.compute(vector_a, vector_b)
        assert math.isclose(score, -1.0, rel_tol=1e-9)

    def test_magnitude_invariance(self) -> None:
        """
        Page 14's core lesson: cosine similarity should NOT change just
        because one vector is scaled up, since only orientation matters.
        """
        vector_a = [1.0, 2.0]
        vector_b = [2.0, 4.0]  # Same direction, double magnitude.
        score = CosineSimilarity.compute(vector_a, vector_b)
        assert math.isclose(score, 1.0, rel_tol=1e-9)

    def test_zero_vector_returns_zero_not_error(self) -> None:
        """Cold Start scenario: a zero-magnitude vector has no orientation."""
        zero_vector = [0.0, 0.0, 0.0]
        normal_vector = [1.0, 2.0, 3.0]
        score = CosineSimilarity.compute(zero_vector, normal_vector)
        assert score == 0.0

    def test_both_zero_vectors_returns_zero(self) -> None:
        zero_vector = [0.0, 0.0]
        score = CosineSimilarity.compute(zero_vector, zero_vector)
        assert score == 0.0

    def test_mismatched_vector_lengths_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            CosineSimilarity.compute([1.0, 2.0], [1.0, 2.0, 3.0])

    def test_score_range_for_non_negative_inputs_is_zero_to_one(self) -> None:
        """Page 16: with non-negative TF-IDF inputs, score in [0, 1]."""
        vector_a = [0.5, 0.3, 0.0]
        vector_b = [0.1, 0.4, 0.2]
        score = CosineSimilarity.compute(vector_a, vector_b)
        assert 0.0 <= score <= 1.0
