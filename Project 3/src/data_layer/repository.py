"""
Repository layer: the only module allowed to know that job-role data
lives in a CSV file. If this project later migrates to a database or
an API, only this file needs to change.
"""

import csv
from pathlib import Path

from src.data_layer.models import JobRole
from src.exceptions import EmptyDatasetError


class SkillsRepository:
    """Loads and validates job-role data from a CSV file."""

    def __init__(self, filepath: Path) -> None:
        self._filepath = filepath

    def load(self) -> list[JobRole]:
        """
        Load all job roles from the CSV dataset.

        Expected CSV schema:
            role_name,skills
            "Data Scientist","python,sql,machine learning"

        Returns:
            A list of JobRole objects.

        Raises:
            EmptyDatasetError: If the file is missing, unreadable, or
                contains no valid rows.
        """
        if not self._filepath.exists():
            raise EmptyDatasetError(
                f"Dataset file not found at: {self._filepath}"
            )

        roles: list[JobRole] = []

        try:
            with self._filepath.open(mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row_number, row in enumerate(reader, start=2):
                    role = self._parse_row(row, row_number)
                    if role is not None:
                        roles.append(role)
        except (OSError, csv.Error) as exc:
            raise EmptyDatasetError(
                f"Failed to read dataset at {self._filepath}: {exc}"
            ) from exc

        if not roles:
            raise EmptyDatasetError(
                f"Dataset at {self._filepath} contains no valid job roles."
            )

        return roles

    @staticmethod
    def _parse_row(row: dict, row_number: int) -> JobRole | None:
        """
        Parse a single CSV row into a JobRole, skipping malformed rows
        rather than crashing the whole load (data resilience).
        """
        name = (row.get("role_name") or "").strip()
        raw_skills = (row.get("skills") or "").strip()

        if not name or not raw_skills:
            return None  # Skip silently malformed/blank rows.

        skills = [s.strip().lower() for s in raw_skills.split(",") if s.strip()]
        if not skills:
            return None

        return JobRole(name=name, skills=skills)
