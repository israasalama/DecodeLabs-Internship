"""Tests for data schema and validation."""

import pytest

from iris_classifier.data.schema import IrisSample, Dataset


class TestIrisSample:
    """Tests for IrisSample."""

    def test_valid_sample(self):
        """Test creating valid sample."""
        sample = IrisSample(5.1, 3.5, 1.4, 0.2)
        assert sample.sepal_length == 5.1
        assert sample.sepal_width == 3.5

    def test_sample_validation_passes(self):
        """Test validation passes for valid measurements."""
        sample = IrisSample(5.1, 3.5, 1.4, 0.2)
        sample.validate()  # Should not raise

    def test_negative_measurement_fails_validation(self):
        """Test validation fails for negative measurements."""
        sample = IrisSample(-5.1, 3.5, 1.4, 0.2)
        with pytest.raises(ValueError, match="must be positive"):
            sample.validate()

    def test_non_numeric_measurement_fails_validation(self):
        """Test validation fails for non-numeric measurements."""
        sample = IrisSample("invalid", 3.5, 1.4, 0.2)
        with pytest.raises(ValueError, match="must be numeric"):
            sample.validate()

    def test_to_array(self):
        """Test converting sample to array."""
        sample = IrisSample(5.1, 3.5, 1.4, 0.2)
        array = sample.to_array()
        assert array == [5.1, 3.5, 1.4, 0.2]
        assert len(array) == 4

    def test_sample_with_species(self):
        """Test sample with species label."""
        sample = IrisSample(5.1, 3.5, 1.4, 0.2, species="setosa")
        assert sample.species == "setosa"

    def test_zero_measurement(self):
        """Test zero measurements are allowed."""
        sample = IrisSample(0, 0, 0, 0)
        sample.validate()  # Should pass

    def test_very_large_measurements(self):
        """Test large numeric measurements."""
        sample = IrisSample(999.9, 888.8, 777.7, 666.6)
        sample.validate()  # Should pass

    def test_float_precision(self):
        """Test handling of float precision."""
        sample = IrisSample(5.123456789, 3.987654321, 1.4, 0.2)
        array = sample.to_array()
        assert array[0] == pytest.approx(5.123456789)
        assert array[1] == pytest.approx(3.987654321)

    def test_repr(self):
        """Test string representation."""
        sample = IrisSample(5.1, 3.5, 1.4, 0.2, species="setosa")
        repr_str = repr(sample)
        assert "5.1" in repr_str
        assert "setosa" in repr_str


class TestDataset:
    """Tests for Dataset."""

    @pytest.fixture
    def sample_dataset(self):
        """Create a sample dataset."""
        return Dataset(
            features=[[5.1, 3.5, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4]],
            labels=[0, 1],
            feature_names=["sepal length", "sepal width", "petal length", "petal width"],
            target_names=["setosa", "versicolor", "virginica"],
        )

    def test_dataset_creation(self, sample_dataset):
        """Test creating dataset."""
        assert sample_dataset.sample_count == 2
        assert sample_dataset.feature_count == 4

    def test_dataset_summary(self, sample_dataset):
        """Test dataset summary generation."""
        summary = sample_dataset.summary()
        assert "Samples: 2" in summary
        assert "Features: 4" in summary
        assert "setosa" in summary

    def test_empty_dataset(self):
        """Test empty dataset handling."""
        dataset = Dataset(
            features=[],
            labels=[],
            feature_names=["f1", "f2"],
            target_names=["a", "b"],
        )
        assert dataset.sample_count == 0
        assert dataset.feature_count == 2

    def test_class_distribution(self, sample_dataset):
        """Test class distribution in dataset."""
        summary = sample_dataset.summary()
        # Summary should show class distribution
        assert "Class distribution" in summary
