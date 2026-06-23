"""Machine learning models factory and implementations."""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


class ModelFactory:
    """Factory for creating different classification models."""

    @staticmethod
    def create_knn(k: int = 3) -> KNeighborsClassifier:
        """Create K-Nearest Neighbors classifier.

        Args:
            k: Number of neighbors.

        Returns:
            Configured KNeighborsClassifier.

        Raises:
            ValueError: If k is invalid.
        """
        if not isinstance(k, int) or k <= 0:
            raise ValueError(f"k must be a positive integer, got {k}")

        # Warning for even k (but still allowed)
        if k % 2 == 0:
            print(f"⚠ Warning: Even k value ({k}) may be less effective for tie-breaking")

        return KNeighborsClassifier(n_neighbors=k)

    @staticmethod
    def create_logistic_regression() -> LogisticRegression:
        """Create Logistic Regression classifier.

        Returns:
            Configured LogisticRegression model.
        """
        return LogisticRegression(max_iter=200, random_state=42)

    @staticmethod
    def create_decision_tree(max_depth: int = 5) -> DecisionTreeClassifier:
        """Create Decision Tree classifier.

        Args:
            max_depth: Maximum tree depth.

        Returns:
            Configured DecisionTreeClassifier.
        """
        return DecisionTreeClassifier(max_depth=max_depth, random_state=42)

    @staticmethod
    def validate_k(k: int, training_size: int) -> None:
        """Validate k value for KNN.

        Args:
            k: Number of neighbors.
            training_size: Size of training set.

        Raises:
            ValueError: If k is invalid for training set.
        """
        if k > training_size:
            raise ValueError(f"k ({k}) cannot exceed training set size ({training_size})")
