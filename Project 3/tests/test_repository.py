"""Unit tests for SkillsRepository."""

from pathlib import Path

import pytest

from src.data_layer.repository import SkillsRepository
from src.exceptions import EmptyDatasetError


def _write_csv(tmp_path: Path, content: str) -> Path:
    filepath = tmp_path / "test_skills.csv"
    filepath.write_text(content, encoding="utf-8")
    return filepath


class TestSkillsRepository:
    def test_loads_valid_csv_correctly(self, tmp_path: Path) -> None:
        csv_content = (
            "role_name,skills\n"
            '"Data Scientist","python,sql,statistics"\n'
            '"Backend Developer","java,sql,apis"\n'
        )
        filepath = _write_csv(tmp_path, csv_content)
        repo = SkillsRepository(filepath)

        roles = repo.load()

        assert len(roles) == 2
        assert roles[0].name == "Data Scientist"
        assert roles[0].skills == ["python", "sql", "statistics"]

    def test_missing_file_raises_empty_dataset_error(self, tmp_path: Path) -> None:
        missing_path = tmp_path / "does_not_exist.csv"
        repo = SkillsRepository(missing_path)

        with pytest.raises(EmptyDatasetError):
            repo.load()

    def test_empty_csv_raises_empty_dataset_error(self, tmp_path: Path) -> None:
        filepath = _write_csv(tmp_path, "role_name,skills\n")
        repo = SkillsRepository(filepath)

        with pytest.raises(EmptyDatasetError):
            repo.load()

    def test_malformed_rows_are_skipped_not_fatal(self, tmp_path: Path) -> None:
        csv_content = (
            "role_name,skills\n"
            '"Data Scientist","python,sql"\n'
            ',\n'  # malformed: both fields blank
            '"Backend Developer","java,sql"\n'
        )
        filepath = _write_csv(tmp_path, csv_content)
        repo = SkillsRepository(filepath)

        roles = repo.load()

        assert len(roles) == 2  # malformed row silently skipped

    def test_skills_are_normalized_to_lowercase_on_load(self, tmp_path: Path) -> None:
        csv_content = 'role_name,skills\n"DevOps Engineer","AWS,Docker,Kubernetes"\n'
        filepath = _write_csv(tmp_path, csv_content)
        repo = SkillsRepository(filepath)

        roles = repo.load()

        assert roles[0].skills == ["aws", "docker", "kubernetes"]

    def test_extra_whitespace_in_skills_is_stripped(self, tmp_path: Path) -> None:
        csv_content = 'role_name,skills\n"Role","  python , sql  ,  java "\n'
        filepath = _write_csv(tmp_path, csv_content)
        repo = SkillsRepository(filepath)

        roles = repo.load()

        assert roles[0].skills == ["python", "sql", "java"]
