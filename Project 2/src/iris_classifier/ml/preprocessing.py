"""Data preprocessing service for train/test splitting and feature scaling."""

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from iris_classifier.config import get_config_manager
from iris_classifier.data.schema import Dataset
from iris_classifier.logger import get_logger


@dataclass
class PreprocessedData:
    """Container for preprocessed train/test splits."""

    X_train: list[list[float]]
    X_test: list[list[float]]
    y_train: list[int]
    y_test: list[int]
    scaler: StandardScaler
    feature_count: int

    def summary(self) -> str:
        """Generate preprocessing summary."""
        return (f"Preprocessing Summary:\n"
                f"  Training samples: {len(self.X_train)}\n"
                f"  Testing samples: {len(self.X_test)}\n"
                f"  Features: {self.feature_count}\n"
                f"  Scaling: StandardScaler")


class PreprocessingService:
    """Handles train/test splitting and feature scaling."""

    def __init__(self) -> None:
        """Initialize preprocessing service."""
        self.logger = get_logger()
        config = get_config_manager()
        self.random_seed = config.get("ml.random_seed", 42)
        self.test_split_ratio = config.get("ml.test_split_ratio", 0.2)

    def preprocess(self, dataset: Dataset) -> PreprocessedData:
        """Apply full preprocessing pipeline: split and scale.

        Args:
            dataset: Raw dataset to preprocess.

        Returns:
            PreprocessedData with train/test splits and fitted scaler.

        Raises:
            ValueError: If split ratio is invalid.
        """
        if not 0 < self.test_split_ratio < 1:
            raise ValueError(f"Test split ratio must be between 0 and 1, got {self.test_split_ratio}")

        # Train/test split with reproducibility
        X_train, X_test, y_train, y_test = train_test_split(
            dataset.features,
            dataset.labels,
            test_size=self.test_split_ratio,
            random_state=self.random_seed,
            shuffle=True,
        )

        # Fit scaler on training data only
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train).tolist()
        X_test_scaled = scaler.transform(X_test).tolist()

        result = PreprocessedData(
            X_train=X_train_scaled,
            X_test=X_test_scaled,
            y_train=y_train,
            y_test=y_test,
            scaler=scaler,
            feature_count=dataset.feature_count,
        )

        self.logger.info(f"Data preprocessed: {len(X_train)} train, {len(X_test)} test samples")

        return result

    def scale_sample(self, sample: list[float], scaler: StandardScaler) -> list[float]:
        """Scale a single sample using fitted scaler.

        Args:
            sample: Single sample features.
            scaler: Fitted StandardScaler instance.

        Returns:
            Scaled sample as list.
        """
        scaled = scaler.transform([sample])
        return scaled[0].tolist()
