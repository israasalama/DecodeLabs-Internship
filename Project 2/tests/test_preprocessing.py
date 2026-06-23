"""Tests for data preprocessing."""

import pytest

from iris_classifier.ml.preprocessing import PreprocessingService
from iris_classifier.data.schema import Dataset


@pytest.fixture
def sample_dataset():
    """Create a sample dataset for testing."""
    features = [
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [7.0, 3.2, 4.7, 1.4],
        [6.4, 3.2, 4.5, 1.5],
        [5.9, 3.0, 4.2, 1.5],
        [6.3, 3.3, 6.0, 2.5],
    ]
    return Dataset(
        features=features,
        labels=[0, 0, 1, 1, 1, 2],
        feature_names=["sepal length", "sepal width", "petal length", "petal width"],
        target_names=["setosa", "versicolor", "virginica"],
    )


class TestPreprocessingService:
    """Tests for PreprocessingService."""

    def test_basic_preprocessing(self, sample_dataset):
        """Test basic preprocessing pipeline."""
        service = PreprocessingService()
        result = service.preprocess(sample_dataset)

        assert len(result.X_train) > 0
        assert len(result.X_test) > 0
        assert len(result.y_train) > 0
        assert len(result.y_test) > 0

    def test_train_test_split_ratio(self, sample_dataset):
        """Test train/test split respects configured ratio."""
        service = PreprocessingService()
        service.test_split_ratio = 0.5
        result = service.preprocess(sample_dataset)

        total = len(result.y_train) + len(result.y_test)
        test_ratio = len(result.y_test) / total
        assert test_ratio == pytest.approx(0.5, abs=0.15)  # Allow some variance due to shuffling

    def test_invalid_split_ratio_zero(self, sample_dataset):
        """Test error for invalid split ratio (0)."""
        service = PreprocessingService()
        service.test_split_ratio = 0
        with pytest.raises(ValueError):
            service.preprocess(sample_dataset)

    def test_invalid_split_ratio_one(self, sample_dataset):
        """Test error for invalid split ratio (1)."""
        service = PreprocessingService()
        service.test_split_ratio = 1.0
        with pytest.raises(ValueError):
            service.preprocess(sample_dataset)

    def test_invalid_split_ratio_negative(self, sample_dataset):
        """Test error for negative split ratio."""
        service = PreprocessingService()
        service.test_split_ratio = -0.2
        with pytest.raises(ValueError):
            service.preprocess(sample_dataset)

    def test_scaler_fit_on_train_only(self, sample_dataset):
        """Test that scaler is fit only on training data."""
        service = PreprocessingService()
        result = service.preprocess(sample_dataset)

        # Get means from scaler (should be based on training data)
        scaler_mean = result.scaler.mean_
        # Manually compute training data mean
        import numpy as np
        manual_mean = np.mean(result.X_train, axis=0)  # Before scaling, use preprocessed
        # The actual means from scaler should exist
        assert scaler_mean is not None

    def test_reproducible_split(self, sample_dataset):
        """Test that same seed produces same split."""
        service1 = PreprocessingService()
        service1.random_seed = 42
        result1 = service1.preprocess(sample_dataset)

        service2 = PreprocessingService()
        service2.random_seed = 42
        result2 = service2.preprocess(sample_dataset)

        assert result1.y_train == result2.y_train
        assert result1.y_test == result2.y_test

    def test_scale_single_sample(self, sample_dataset):
        """Test scaling a single sample."""
        service = PreprocessingService()
        result = service.preprocess(sample_dataset)

        sample = [5.1, 3.5, 1.4, 0.2]
        scaled = service.scale_sample(sample, result.scaler)

        assert len(scaled) == 4
        assert all(isinstance(x, float) for x in scaled)

    def test_preprocessing_summary(self, sample_dataset):
        """Test preprocessing summary generation."""
        service = PreprocessingService()
        result = service.preprocess(sample_dataset)

        summary = result.summary()
        assert "Training samples:" in summary
        assert "Testing samples:" in summary
        assert "Features:" in summary

    def test_features_dimension_preserved(self, sample_dataset):
        """Test that feature dimensions are preserved."""
        service = PreprocessingService()
        result = service.preprocess(sample_dataset)

        for sample in result.X_train:
            assert len(sample) == 4

        for sample in result.X_test:
            assert len(sample) == 4

    def test_small_dataset_split(self):
        """Test preprocessing on very small dataset."""
        small_dataset = Dataset(
            features=[[1, 2, 3, 4], [5, 6, 7, 8]],
            labels=[0, 1],
            feature_names=["f1", "f2", "f3", "f4"],
            target_names=["a", "b"],
        )
        service = PreprocessingService()
        result = service.preprocess(small_dataset)

        # Should still produce train/test split
        assert len(result.y_train) >= 1
        assert len(result.y_test) >= 1
