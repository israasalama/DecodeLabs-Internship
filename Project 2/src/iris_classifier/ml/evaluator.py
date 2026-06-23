"""Model evaluation service for metrics computation."""

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    classification_report,
    accuracy_score,
)

from iris_classifier.logger import get_logger


@dataclass
class EvaluationResult:
    """Container for evaluation metrics."""

    accuracy: float
    f1_macro: float
    f1_weighted: float
    confusion_matrix_data: list[list[int]]
    classification_report_text: str
    target_names: list[str]

    def summary(self) -> str:
        """Generate human-readable evaluation summary."""
        summary = "=" * 50 + "\n"
        summary += "EVALUATION RESULTS\n"
        summary += "=" * 50 + "\n"
        summary += f"Accuracy: {self.accuracy:.4f}\n"
        summary += f"F1-Score (Macro): {self.f1_macro:.4f}\n"
        summary += f"F1-Score (Weighted): {self.f1_weighted:.4f}\n\n"
        summary += "Confusion Matrix:\n"
        summary += self._format_confusion_matrix() + "\n"
        summary += "\nClassification Report:\n"
        summary += self.classification_report_text
        summary += "=" * 50
        return summary

    def _format_confusion_matrix(self) -> str:
        """Format confusion matrix for display."""
        matrix_str = "     " + "   ".join(f"{name[:4]:>5}" for name in self.target_names) + "\n"

        for i, row in enumerate(self.confusion_matrix_data):
            target_name = self.target_names[i][:4]
            matrix_str += f"{target_name:>4} " + "   ".join(f"{val:>5}" for val in row) + "\n"

        return matrix_str


class EvaluationService:
    """Computes evaluation metrics for model predictions."""

    def __init__(self) -> None:
        """Initialize evaluation service."""
        self.logger = get_logger()

    def evaluate(
        self,
        y_true: list[int],
        y_pred: list[int],
        target_names: list[str],
    ) -> EvaluationResult:
        """Evaluate model predictions using multiple metrics.

        Args:
            y_true: True labels.
            y_pred: Predicted labels.
            target_names: Names of target classes.

        Returns:
            EvaluationResult with computed metrics.

        Raises:
            ValueError: If evaluation data is invalid.
        """
        if len(y_true) != len(y_pred):
            raise ValueError("y_true and y_pred must have same length")

        if len(y_true) == 0:
            raise ValueError("Cannot evaluate on empty data")

        try:
            accuracy = accuracy_score(y_true, y_pred)
            f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
            f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)
            conf_matrix = confusion_matrix(y_true, y_pred, labels=list(range(len(target_names))))
            class_report = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)

            result = EvaluationResult(
                accuracy=float(accuracy),
                f1_macro=float(f1_macro),
                f1_weighted=float(f1_weighted),
                confusion_matrix_data=conf_matrix.tolist(),
                classification_report_text=class_report,
                target_names=target_names,
            )

            self.logger.info(f"Model evaluated: Accuracy={accuracy:.4f}, F1-Macro={f1_macro:.4f}")
            return result
        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            raise RuntimeError(f"Model evaluation failed: {e}") from e
