"""Hyperparameter tuning service for model optimization."""

from dataclasses import dataclass
from typing import Dict, List

from sklearn.metrics import accuracy_score, f1_score

from iris_classifier.config import get_config_manager
from iris_classifier.ml.models import ModelFactory
from iris_classifier.logger import get_logger


@dataclass
class TuningResult:
    """Container for tuning results."""

    k_values: List[int]
    accuracies: List[float]
    f1_scores: List[float]
    best_k: int
    best_accuracy: float
    best_f1: float

    def summary(self) -> str:
        """Generate tuning summary."""
        summary = "K-Value Tuning Results:\n"
        summary += "K\tAccuracy\tF1-Score\n"
        summary += "-" * 30 + "\n"

        for k, acc, f1 in zip(self.k_values, self.accuracies, self.f1_scores):
            marker = " ← Best" if k == self.best_k else ""
            summary += f"{k}\t{acc:.4f}\t\t{f1:.4f}{marker}\n"

        summary += f"\nBest K: {self.best_k} (Accuracy: {self.best_accuracy:.4f}, F1: {self.best_f1:.4f})"
        return summary


class TuningService:
    """Tunes hyperparameters for KNN model."""

    def __init__(self) -> None:
        """Initialize tuning service."""
        self.logger = get_logger()
        config = get_config_manager()
        self.default_k_range = config.get("ml.k_range", [1, 3, 5, 7, 9, 11, 13, 15])

    def tune_k(
        self,
        X_train: list[list[float]],
        y_train: list[int],
        X_test: list[list[float]],
        y_test: list[int],
        k_values: List[int] | None = None,
    ) -> TuningResult:
        """Tune K value for KNN using grid search.

        Args:
            X_train: Training features.
            y_train: Training labels.
            X_test: Test features.
            y_test: Test labels.
            k_values: List of K values to try. Uses config default if None.

        Returns:
            TuningResult with metrics for each K.

        Raises:
            ValueError: If K values are invalid.
        """
        k_values = k_values or self.default_k_range

        if not k_values:
            raise ValueError("k_values cannot be empty")

        accuracies = []
        f1_scores_list = []

        for k in k_values:
            try:
                ModelFactory.validate_k(k, len(X_train))
                model = ModelFactory.create_knn(k)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                acc = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

                accuracies.append(float(acc))
                f1_scores_list.append(float(f1))
            except (ValueError, Exception) as e:
                self.logger.warning(f"Tuning failed for k={k}: {e}")
                accuracies.append(0.0)
                f1_scores_list.append(0.0)

        # Find best K
        best_idx = max(range(len(accuracies)), key=lambda i: (accuracies[i], f1_scores_list[i]))
        best_k = k_values[best_idx]

        result = TuningResult(
            k_values=k_values,
            accuracies=accuracies,
            f1_scores=f1_scores_list,
            best_k=best_k,
            best_accuracy=accuracies[best_idx],
            best_f1=f1_scores_list[best_idx],
        )

        self.logger.info(f"K-tuning complete: Best K={best_k} with accuracy={accuracies[best_idx]:.4f}")
        return result
