"""Tests for model training."""

import pytest

from iris_classifier.ml.trainer import TrainingService, TrainedModel
from iris_classifier.ml.models import ModelFactory


@pytest.fixture
def training_service():
    """Create training service instance."""
    return TrainingService()


@pytest.fixture
def sample_training_data():
    """Create sample training data."""
    X_train = [
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [7.0, 3.2, 4.7, 1.4],
        [6.4, 3.2, 4.5, 1.5],
    ]
    y_train = [0, 0, 1, 1]

    X_test = [[5.5, 3.6, 1.3, 0.2], [6.5, 3.1, 4.6, 1.5]]
    y_test = [0, 1]

    return X_train, y_train, X_test, y_test


class TestTrainingService:
    """Tests for TrainingService."""

    def test_train_knn(self, training_service, sample_training_data):
        """Test training KNN model."""
        X_train, y_train, _, _ = sample_training_data
        model = ModelFactory.create_knn(k=3)

        trained = training_service.train(model, X_train, y_train, "KNN")

        assert isinstance(trained, TrainedModel)
        assert trained.algorithm == "KNN"
        assert trained.training_samples == 4
        assert trained.feature_count == 4

    def test_train_summary(self, training_service, sample_training_data):
        """Test training summary generation."""
        X_train, y_train, _, _ = sample_training_data
        model = ModelFactory.create_knn()
        trained = training_service.train(model, X_train, y_train)

        summary = trained.summary()
        assert "Algorithm: KNN" in summary
        assert "Training samples: 4" in summary
        assert "Features: 4" in summary

    def test_predict_after_training(self, training_service, sample_training_data):
        """Test making predictions after training."""
        X_train, y_train, X_test, _ = sample_training_data
        model = ModelFactory.create_knn()
        trained = training_service.train(model, X_train, y_train)

        predictions = training_service.predict(trained, X_test)

        assert len(predictions) == 2
        assert all(pred in [0, 1] for pred in predictions)

    def test_predict_single_sample(self, training_service, sample_training_data):
        """Test predicting single sample."""
        X_train, y_train, _, _ = sample_training_data
        model = ModelFactory.create_knn()
        trained = training_service.train(model, X_train, y_train)

        single_sample = [[5.1, 3.5, 1.4, 0.2]]
        predictions = training_service.predict(trained, single_sample)

        assert len(predictions) == 1
        assert predictions[0] in [0, 1]

    def test_train_with_different_algorithms(self, training_service, sample_training_data):
        """Test training different algorithms."""
        X_train, y_train, _, _ = sample_training_data

        algorithms = [
            (ModelFactory.create_knn(), "KNN"),
            (ModelFactory.create_logistic_regression(), "LogReg"),
            (ModelFactory.create_decision_tree(), "Tree"),
        ]

        for model, name in algorithms:
            trained = training_service.train(model, X_train, y_train, name)
            assert trained.algorithm == name

    def test_train_empty_data_fails(self, training_service):
        """Test training with empty data fails."""
        model = ModelFactory.create_knn()

        with pytest.raises(Exception):
            training_service.train(model, [], [], "KNN")

    def test_predict_unequal_features(self, training_service, sample_training_data):
        """Test prediction with wrong feature count."""
        X_train, y_train, _, _ = sample_training_data
        model = ModelFactory.create_knn()
        trained = training_service.train(model, X_train, y_train)

        # Try to predict with 3 features instead of 4
        wrong_features = [[5.1, 3.5, 1.4]]

        with pytest.raises(Exception):
            training_service.predict(trained, wrong_features)

    def test_training_summary_different_algorithms(self, training_service, sample_training_data):
        """Test summaries for different algorithms."""
        X_train, y_train, _, _ = sample_training_data

        models = [
            (ModelFactory.create_knn(k=5), "KNN(k=5)"),
            (ModelFactory.create_logistic_regression(), "LogisticRegression"),
            (ModelFactory.create_decision_tree(max_depth=3), "DecisionTree"),
        ]

        for model, name in models:
            trained = training_service.train(model, X_train, y_train, name)
            summary = trained.summary()
            assert "Training samples: 4" in summary
            assert "Features: 4" in summary
