"""Tests for model factory and validation."""

import pytest

from iris_classifier.ml.models import ModelFactory


class TestModelFactory:
    """Tests for ModelFactory."""

    def test_create_knn_default(self):
        """Test creating KNN with default k."""
        model = ModelFactory.create_knn()
        assert model is not None
        assert model.n_neighbors == 3

    def test_create_knn_custom_k(self):
        """Test creating KNN with custom k."""
        model = ModelFactory.create_knn(k=5)
        assert model.n_neighbors == 5

    def test_create_knn_invalid_k_zero(self):
        """Test error for k=0."""
        with pytest.raises(ValueError, match="positive integer"):
            ModelFactory.create_knn(k=0)

    def test_create_knn_invalid_k_negative(self):
        """Test error for negative k."""
        with pytest.raises(ValueError, match="positive integer"):
            ModelFactory.create_knn(k=-1)

    def test_create_knn_invalid_k_non_integer(self):
        """Test error for non-integer k."""
        with pytest.raises(ValueError, match="positive integer"):
            ModelFactory.create_knn(k=3.5)

    def test_create_knn_even_k_warning(self, capsys):
        """Test warning for even k value."""
        model = ModelFactory.create_knn(k=4)
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "warning" in captured.out.lower()
        assert model.n_neighbors == 4

    def test_create_logistic_regression(self):
        """Test creating logistic regression model."""
        model = ModelFactory.create_logistic_regression()
        assert model is not None

    def test_create_decision_tree(self):
        """Test creating decision tree model."""
        model = ModelFactory.create_decision_tree()
        assert model is not None
        assert model.max_depth == 5

    def test_create_decision_tree_custom_depth(self):
        """Test creating decision tree with custom depth."""
        model = ModelFactory.create_decision_tree(max_depth=10)
        assert model.max_depth == 10

    def test_validate_k_valid(self):
        """Test k validation passes for valid values."""
        # Should not raise
        ModelFactory.validate_k(3, 100)

    def test_validate_k_exceeds_training_size(self):
        """Test error when k exceeds training set size."""
        with pytest.raises(ValueError, match="cannot exceed training set size"):
            ModelFactory.validate_k(50, 30)

    def test_validate_k_equal_to_training_size(self):
        """Test k equal to training set size."""
        ModelFactory.validate_k(30, 30)

    def test_validate_k_just_below_training_size(self):
        """Test k just below training set size."""
        ModelFactory.validate_k(29, 30)

    def test_k_value_one(self):
        """Test k=1 (minimum valid value)."""
        model = ModelFactory.create_knn(k=1)
        assert model.n_neighbors == 1

    def test_k_value_large(self):
        """Test large k value."""
        model = ModelFactory.create_knn(k=100)
        assert model.n_neighbors == 100
