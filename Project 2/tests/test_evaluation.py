"""Tests for model evaluation."""

import pytest

from iris_classifier.ml.evaluator import EvaluationService, EvaluationResult


@pytest.fixture
def evaluation_service():
    """Create evaluation service."""
    return EvaluationService()


class TestEvaluationService:
    """Tests for EvaluationService."""

    def test_basic_evaluation(self, evaluation_service):
        """Test basic evaluation."""
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 1, 2, 0, 1, 2]
        targets = ["setosa", "versicolor", "virginica"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert result.accuracy == pytest.approx(1.0)
        assert result.f1_macro == pytest.approx(1.0)

    def test_evaluation_with_errors(self, evaluation_service):
        """Test evaluation with some misclassifications."""
        y_true = [0, 0, 1, 1, 2, 2]
        y_pred = [0, 1, 1, 2, 2, 0]  # 3 errors out of 6
        targets = ["setosa", "versicolor", "virginica"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert result.accuracy == pytest.approx(0.5, abs=0.01)
        assert 0 < result.f1_macro < 1

    def test_confusion_matrix_structure(self, evaluation_service):
        """Test confusion matrix has correct shape."""
        y_true = [0, 0, 1, 1, 2, 2]
        y_pred = [0, 0, 1, 1, 2, 2]
        targets = ["a", "b", "c"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert len(result.confusion_matrix_data) == 3
        assert all(len(row) == 3 for row in result.confusion_matrix_data)

    def test_evaluation_result_summary(self, evaluation_service):
        """Test evaluation result summary generation."""
        y_true = [0, 0, 1, 1]
        y_pred = [0, 0, 1, 1]
        targets = ["a", "b"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)
        summary = result.summary()

        assert "EVALUATION RESULTS" in summary
        assert "Accuracy:" in summary
        assert "F1-Score" in summary
        assert "Confusion Matrix" in summary

    def test_mismatched_lengths(self, evaluation_service):
        """Test error when y_true and y_pred have different lengths."""
        y_true = [0, 1, 2]
        y_pred = [0, 1]
        targets = ["a", "b", "c"]

        with pytest.raises(ValueError, match="same length"):
            evaluation_service.evaluate(y_true, y_pred, targets)

    def test_empty_predictions(self, evaluation_service):
        """Test error on empty data."""
        y_true = []
        y_pred = []
        targets = ["a", "b"]

        with pytest.raises(ValueError, match="empty"):
            evaluation_service.evaluate(y_true, y_pred, targets)

    def test_binary_classification(self, evaluation_service):
        """Test evaluation on binary classification."""
        y_true = [0, 0, 1, 1, 0, 1]
        y_pred = [0, 0, 1, 0, 0, 1]
        targets = ["negative", "positive"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert len(result.confusion_matrix_data) == 2
        assert result.accuracy == pytest.approx(5/6, abs=0.01)

    def test_perfect_predictions(self, evaluation_service):
        """Test with perfect predictions."""
        y_true = [0, 0, 1, 1, 2, 2]
        y_pred = [0, 0, 1, 1, 2, 2]
        targets = ["a", "b", "c"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert result.accuracy == 1.0
        assert result.f1_macro == 1.0

    def test_all_wrong_predictions(self, evaluation_service):
        """Test with all wrong predictions."""
        y_true = [0, 0, 0, 1, 1, 1]
        y_pred = [1, 1, 1, 0, 0, 0]
        targets = ["a", "b"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert result.accuracy == 0.0

    def test_classification_report_present(self, evaluation_service):
        """Test that classification report is included."""
        y_true = [0, 0, 1, 1, 2, 2]
        y_pred = [0, 0, 1, 1, 2, 2]
        targets = ["setosa", "versicolor", "virginica"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert len(result.classification_report_text) > 0
        assert "precision" in result.classification_report_text.lower()
        assert "recall" in result.classification_report_text.lower()

    def test_imbalanced_classes(self, evaluation_service):
        """Test evaluation with imbalanced classes."""
        y_true = [0, 0, 0, 0, 1, 1, 2]
        y_pred = [0, 0, 0, 0, 1, 0, 2]
        targets = ["majority", "minority", "rare"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)

        assert 0 <= result.accuracy <= 1
        assert 0 <= result.f1_macro <= 1

    def test_confusion_matrix_formatting(self, evaluation_service):
        """Test confusion matrix formatting."""
        y_true = [0, 0, 1, 1]
        y_pred = [0, 0, 1, 1]
        targets = ["cat", "dog"]

        result = evaluation_service.evaluate(y_true, y_pred, targets)
        formatted = result._format_confusion_matrix()

        assert "cat" in formatted or "dog" in formatted
