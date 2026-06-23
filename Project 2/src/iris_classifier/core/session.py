"""Experiment session management - coordinates all ML services."""

from typing import Optional
from dataclasses import dataclass, field

from iris_classifier.config import get_config_manager
from iris_classifier.data.loader import DatasetLoader
from iris_classifier.data.schema import Dataset, IrisSample
from iris_classifier.ml.preprocessing import PreprocessingService, PreprocessedData
from iris_classifier.ml.models import ModelFactory
from iris_classifier.ml.trainer import TrainingService, TrainedModel
from iris_classifier.ml.evaluator import EvaluationService, EvaluationResult
from iris_classifier.ml.tuner import TuningService, TuningResult
from iris_classifier.logger import get_logger


@dataclass
class ExperimentSession:
    """Manages complete ML experiment lifecycle."""

    dataset: Optional[Dataset] = None
    preprocessed_data: Optional[PreprocessedData] = None
    trained_model: Optional[TrainedModel] = None
    evaluation_result: Optional[EvaluationResult] = None
    tuning_result: Optional[TuningResult] = None
    command_history: list[str] = field(default_factory=list)
    is_data_loaded: bool = False
    is_preprocessed: bool = False
    is_model_trained: bool = False
    is_evaluated: bool = False

    def __post_init__(self) -> None:
        """Initialize session services."""
        self.config = get_config_manager()
        self.logger = get_logger()
        self.data_loader = DatasetLoader()
        self.preprocessing = PreprocessingService()
        self.training = TrainingService()
        self.evaluation = EvaluationService()
        self.tuning = TuningService()

    def load_data(self) -> None:
        """Load the Iris dataset."""
        self.dataset = self.data_loader.load_iris_dataset()
        self.is_data_loaded = True
        self._add_to_history("load_data")
        self.logger.info("Data loading complete")

    def preprocess(self) -> None:
        """Preprocess loaded data (split and scale)."""
        if not self.is_data_loaded:
            raise RuntimeError("Must load data first with load_data()")

        self.preprocessed_data = self.preprocessing.preprocess(self.dataset)
        self.is_preprocessed = True
        self._add_to_history("preprocess")
        self.logger.info("Preprocessing complete")

    def train(self, k: Optional[int] = None, algorithm: str = "knn") -> None:
        """Train classifier model.

        Args:
            k: Number of neighbors for KNN. Uses config default if None.
            algorithm: Algorithm to use ('knn', 'logistic', 'tree').

        Raises:
            RuntimeError: If data not preprocessed first.
            ValueError: If algorithm is invalid.
        """
        if not self.is_preprocessed:
            raise RuntimeError("Must preprocess data first with preprocess()")

        if algorithm.lower() == "knn":
            k = k or self.config.get("ml.default_k", 3)
            ModelFactory.validate_k(k, len(self.preprocessed_data.X_train))
            model = ModelFactory.create_knn(k)
            algo_name = f"KNN(k={k})"
        elif algorithm.lower() == "logistic":
            model = ModelFactory.create_logistic_regression()
            algo_name = "Logistic Regression"
        elif algorithm.lower() == "tree":
            model = ModelFactory.create_decision_tree()
            algo_name = "Decision Tree"
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        self.trained_model = self.training.train(
            model,
            self.preprocessed_data.X_train,
            self.preprocessed_data.y_train,
            algo_name,
        )
        self.is_model_trained = True
        self._add_to_history(f"train({algorithm})")
        self.logger.info("Model training complete")

    def evaluate(self) -> None:
        """Evaluate trained model on test set.

        Raises:
            RuntimeError: If model not trained first.
        """
        if not self.is_model_trained:
            raise RuntimeError("Must train model first with train()")

        y_pred = self.training.predict(self.trained_model, self.preprocessed_data.X_test)
        self.evaluation_result = self.evaluation.evaluate(
            self.preprocessed_data.y_test,
            y_pred,
            self.dataset.target_names,
        )
        self.is_evaluated = True
        self._add_to_history("evaluate")
        self.logger.info("Model evaluation complete")

    def predict_new_sample(self, sample: IrisSample) -> str:
        """Predict species for a new sample.

        Args:
            sample: IrisSample with flower measurements.

        Returns:
            Predicted species name.

        Raises:
            RuntimeError: If model not trained.
            ValueError: If sample is invalid.
        """
        if not self.is_model_trained:
            raise RuntimeError("Must train model first with train()")

        sample.validate()

        # Scale sample using fitted scaler
        scaled_sample = self.preprocessing.scale_sample(
            sample.to_array(),
            self.preprocessed_data.scaler,
        )

        # Predict
        predictions = self.training.predict(self.trained_model, [scaled_sample])
        predicted_label = predictions[0]
        predicted_species = self.dataset.target_names[predicted_label]

        self._add_to_history(f"predict({sample.sepal_length}, {sample.sepal_width}, {sample.petal_length}, {sample.petal_width})")
        self.logger.info(f"Predicted species: {predicted_species}")

        return predicted_species

    def tune_k(self, k_values: Optional[list[int]] = None) -> None:
        """Perform K-value tuning on test set.

        Args:
            k_values: List of K values to evaluate. Uses config default if None.

        Raises:
            RuntimeError: If data not preprocessed.
        """
        if not self.is_preprocessed:
            raise RuntimeError("Must preprocess data first")

        self.tuning_result = self.tuning.tune_k(
            self.preprocessed_data.X_train,
            self.preprocessed_data.y_train,
            self.preprocessed_data.X_test,
            self.preprocessed_data.y_test,
            k_values,
        )
        self._add_to_history("tune_k")
        self.logger.info("K-tuning complete")

    def get_history(self, limit: Optional[int] = None) -> list[str]:
        """Get command history.

        Args:
            limit: Maximum number of commands to return.

        Returns:
            List of executed commands.
        """
        if limit:
            return self.command_history[-limit:]
        return self.command_history

    def log_command(self, command: str) -> None:
        """Log a raw CLI command for session history."""
        self._add_to_history(command)
        self.logger.debug(f"Command logged: {command}")

    def reset(self) -> None:
        """Reset session state."""
        self.dataset = None
        self.preprocessed_data = None
        self.trained_model = None
        self.evaluation_result = None
        self.tuning_result = None
        self.is_data_loaded = False
        self.is_preprocessed = False
        self.is_model_trained = False
        self.is_evaluated = False
        self._add_to_history("reset")
        self.logger.info("Session reset")

    def _add_to_history(self, command: str) -> None:
        """Add command to history with size limit."""
        max_history = self.config.get("cli.history_size", 50)
        self.command_history.append(command)
        if len(self.command_history) > max_history:
            self.command_history.pop(0)
