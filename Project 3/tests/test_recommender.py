"""
Integration tests for TechStackRecommender.

These tests exercise the full 4-step pipeline (Ingestion -> Scoring ->
Sorting -> Filtering) end-to-end against a small, controlled dataset,
rather than mocking individual stages.
"""

from pathlib import Path

import pytest

from src.data_layer.repository import SkillsRepository
from src.exceptions import InsufficientSkillsError
from src.pipeline.recommender import TechStackRecommender


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    content = (
        "role_name,skills\n"
        '"Data Scientist","python,sql,machine learning,statistics"\n'
        '"DevOps Engineer","aws,docker,kubernetes,automation"\n'
        '"Backend Developer","java,python,sql,apis"\n'
    )
    filepath = tmp_path / "skills.csv"
    filepath.write_text(content, encoding="utf-8")
    return filepath


@pytest.fixture()
def recommender(sample_csv: Path) -> TechStackRecommender:
    repo = SkillsRepository(sample_csv)
    rec = TechStackRecommender(repo)
    rec.load_data()
    return rec


class TestTechStackRecommender:
    # --- Validation ------------------------------------------------------

    def test_raises_when_fewer_than_minimum_skills_given(
        self, recommender: TechStackRecommender
    ) -> None:
        with pytest.raises(InsufficientSkillsError):
            recommender.recommend(["python", "sql"])  # only 2 skills

    def test_accepts_exactly_minimum_required_skills(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(["python", "sql", "apis"])
        assert len(results) > 0

    # --- Core recommendation behavior -------------------------------------

    def test_returns_top_n_results_sorted_descending_by_score(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(
            ["python", "machine learning", "statistics"], top_n=2
        )
        assert len(results) == 2
        assert results[0].score >= results[1].score

    def test_best_match_is_most_relevant_role(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(
            ["aws", "docker", "kubernetes"], top_n=1
        )
        assert results[0].role_name == "DevOps Engineer"

    def test_skill_order_does_not_affect_result(
        self, recommender: TechStackRecommender
    ) -> None:
        results_a = recommender.recommend(["aws", "docker", "kubernetes"], top_n=1)
        results_b = recommender.recommend(["kubernetes", "aws", "docker"], top_n=1)
        assert results_a[0].role_name == results_b[0].role_name

    def test_duplicate_skills_do_not_break_pipeline(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(
            ["python", "python", "sql", "sql"], top_n=1
        )
        assert len(results) == 1

    def test_case_insensitive_input(
        self, recommender: TechStackRecommender
    ) -> None:
        results_lower = recommender.recommend(["aws", "docker", "kubernetes"], top_n=1)
        results_upper = recommender.recommend(["AWS", "DOCKER", "KUBERNETES"], top_n=1)
        assert results_lower[0].role_name == results_upper[0].role_name

    # --- Cold Start ---------------------------------------------------------

    def test_cold_start_falls_back_to_trending_instead_of_crashing(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(
            ["nonexistent_skill_a", "nonexistent_skill_b", "nonexistent_skill_c"]
        )
        assert len(results) > 0
        assert all(r.score == 0.0 for r in results)

    def test_top_n_larger_than_dataset_returns_all_available(
        self, recommender: TechStackRecommender
    ) -> None:
        results = recommender.recommend(["python", "sql", "java"], top_n=100)
        assert len(results) == 3  # only 3 roles exist in the sample dataset
