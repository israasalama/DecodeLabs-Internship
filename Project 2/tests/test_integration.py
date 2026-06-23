"""Integration tests for end-to-end workflows."""

import pytest

from iris_classifier.core.session import ExperimentSession
from iris_classifier.data.schema import IrisSample


class TestExperimentSession:
    """Integration tests for complete ML workflows."""

    def test_complete_workflow(self):
        """Test complete ML workflow: load -> preprocess -> train -> evaluate."""
        session = ExperimentSession()

        # Load data
        session.load_data()
        assert session.is_data_loaded
        assert session.dataset is not None

        # Preprocess
        session.preprocess()
        assert session.is_preprocessed
        assert session.preprocessed_data is not None

        # Train
        session.train(k=3)
        assert session.is_model_trained
        assert session.trained_model is not None

        # Evaluate
        session.evaluate()
        assert session.is_evaluated
        assert session.evaluation_result is not None
        assert session.evaluation_result.accuracy > 0

    def test_workflow_with_prediction(self):
        """Test workflow including new sample prediction."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()
        session.train(k=5)

        # Predict
        sample = IrisSample(5.1, 3.5, 1.4, 0.2)
        species = session.predict_new_sample(sample)

        assert species in session.dataset.target_names

    def test_different_algorithms(self):
        """Test workflow with different algorithms."""
        algorithms = ["knn", "logistic", "tree"]

        for algo in algorithms:
            session = ExperimentSession()
            session.load_data()
            session.preprocess()
            session.train(algorithm=algo)
            session.evaluate()

            assert session.is_model_trained
            assert session.evaluation_result is not None

    def test_k_tuning_workflow(self):
        """Test K-value tuning workflow."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()
        session.tune_k([1, 3, 5, 7])

        assert session.tuning_result is not None
        assert session.tuning_result.best_k in [1, 3, 5, 7]

    def test_session_reset(self):
        """Test session reset functionality."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()
        session.train()

        assert session.is_model_trained

        session.reset()

        assert not session.is_data_loaded
        assert not session.is_preprocessed
        assert not session.is_model_trained

    def test_error_without_preprocessing(self):
        """Test error when training without preprocessing."""
        session = ExperimentSession()
        session.load_data()

        with pytest.raises(RuntimeError):
            session.train()

    def test_error_without_training(self):
        """Test error when evaluating without training."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()

        with pytest.raises(RuntimeError):
            session.evaluate()

    def test_command_history(self):
        """Test command history tracking."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()
        session.train()

        history = session.get_history()
        assert "load_data" in history
        assert "preprocess" in history
        assert any(command.startswith("train") for command in history)

    def test_history_limit(self):
        """Test command history respects size limit."""
        session = ExperimentSession()
        # Add many commands
        for _ in range(100):
            session._add_to_history("test_command")

        history = session.get_history()
        # Should respect config limit (default 50)
        assert len(history) <= 60  # Allow some margin

    def test_log_command_adds_raw_command_history(self):
        """Test raw CLI commands are tracked in session history."""
        session = ExperimentSession()
        session.log_command("train knn 3")
        session.log_command("predict 5.1 3.5 1.4 0.2")

        history = session.get_history()
        assert history[-2:] == ["train knn 3", "predict 5.1 3.5 1.4 0.2"]

    def test_multiple_training_runs(self):
        """Test multiple training runs in same session."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()

        # First training
        session.train(k=3)
        acc1 = session.evaluation_result.accuracy if session.evaluation_result else None

        # Re-train with different k
        session.train(k=5)

        assert session.trained_model is not None

    def test_prediction_error_on_invalid_sample(self):
        """Test prediction error on invalid sample."""
        session = ExperimentSession()
        session.load_data()
        session.preprocess()
        session.train()

        invalid_sample = IrisSample(-1, 3.5, 1.4, 0.2)

        with pytest.raises(ValueError):
            session.predict_new_sample(invalid_sample)

    def test_workflow_reproducibility(self):
        """Test that same seed produces same results."""
        def run_workflow():
            session = ExperimentSession()
            session.load_data()
            session.preprocess()
            session.train(k=3)
            session.evaluate()
            return session.evaluation_result.accuracy

        acc1 = run_workflow()
        acc2 = run_workflow()

        assert acc1 == acc2  # Same seed should give same results
