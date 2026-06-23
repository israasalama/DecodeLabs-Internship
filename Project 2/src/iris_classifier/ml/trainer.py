"""Model training service."""

from dataclasses import dataclass
from typing import Any

from iris_classifier.logger import get_logger


@dataclass
class TrainedModel:
    """Container for trained model and metadata."""

    model: Any
    algorithm: str
    training_samples: int
    feature_count: int

    def summary(self) -> str:
        """Generate training summary."""
        return (f"Training Summary:\n"
                f"  Algorithm: {self.algorithm}\n"
                f"  Training samples: {self.training_samples}\n"
                f"  Features: {self.feature_count}")


class TrainingService:
    """Handles model training."""

    def __init__(self) -> None:
        """Initialize training service."""
        self.logger = get_logger()

    def train(
        self,
        model: Any,
        X_train: list[list[float]],
        y_train: list[int],
        algorithm_name: str = "KNN",
    ) -> TrainedModel:
        """Train a classifier model.

        Args:
            model: Unfitted sklearn classifier.
            X_train: Training features.
            y_train: Training labels.
            algorithm_name: Name of algorithm for logging.

        Returns:
            TrainedModel with trained classifier.

        Raises:
            RuntimeError: If training fails.
        """
        try:
            model.fit(X_train, y_train)
            trained = TrainedModel(
                model=model,
                algorithm=algorithm_name,
                training_samples=len(X_train),
                feature_count=len(X_train[0]) if X_train else 0,
            )
            self.logger.info(f"Model trained: {algorithm_name} with {len(X_train)} samples")
            return trained
        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            raise RuntimeError(f"Model training failed: {e}") from e

    def predict(self, trained_model: TrainedModel, X: list[list[float]]) -> list[int]:
        """Make predictions with trained model.

        Args:
            trained_model: Trained model object.
            X: Features to predict.

        Returns:
            List of predicted class labels.

        Raises:
            RuntimeError: If prediction fails.
        """
        try:
            predictions = trained_model.model.predict(X)
            return predictions.tolist() if hasattr(predictions, 'tolist') else list(predictions)
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise RuntimeError(f"Model prediction failed: {e}") from e
