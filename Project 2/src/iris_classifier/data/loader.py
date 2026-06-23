"""Dataset loading service for the Iris dataset."""

from iris_classifier.data.schema import Dataset
from iris_classifier.logger import get_logger

try:
    from sklearn.datasets import load_iris
except ImportError:
    raise ImportError("scikit-learn is required. Install with: pip install -r requirements.txt")


class DatasetLoader:
    """Loads and manages the Iris dataset."""

    @staticmethod
    def load_iris_dataset() -> Dataset:
        """Load the Iris dataset from scikit-learn.

        Returns:
            Dataset object containing features, labels, and metadata.

        Raises:
            RuntimeError: If dataset fails to load.
        """
        try:
            iris = load_iris()
            dataset = Dataset(
                features=iris.data.tolist(),
                labels=iris.target.tolist(),
                feature_names=iris.feature_names,
                target_names=iris.target_names,
            )

            logger = get_logger()
            logger.info(f"Loaded Iris dataset: {dataset.sample_count} samples, {dataset.feature_count} features")

            return dataset
        except Exception as e:
            raise RuntimeError(f"Failed to load Iris dataset: {e}") from e

    @staticmethod
    def get_dataset_info() -> str:
        """Get dataset information without loading full data.

        Returns:
            Formatted information string.
        """
        try:
            iris = load_iris()
            return f"Iris Dataset: {iris.data.shape[0]} samples, {iris.data.shape[1]} features, {len(iris.target_names)} classes"
        except Exception as e:
            return f"Error getting dataset info: {e}"
