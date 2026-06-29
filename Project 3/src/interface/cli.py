"""
Command-line interface for the Tech Stack Recommender.

Responsible only for I/O (reading input, printing output) and basic
flow control. All business logic lives in the pipeline/core layers --
this keeps the CLI thin and easy to swap out (e.g. for a web UI later)
without touching the recommendation logic itself.
"""

import logging

from src.config import RAW_SKILLS_CSV, TOP_N_RESULTS
from src.data_layer.models import RecommendationResult
from src.data_layer.repository import SkillsRepository
from src.exceptions import EmptyDatasetError, InsufficientSkillsError
from src.pipeline.recommender import TechStackRecommender

logger = logging.getLogger(__name__)

_BANNER = """
============================================================
   DECODELABS  |  AI TECH STACK RECOMMENDER  (Project 3)
============================================================
"""

_MENU = """
What would you like to do?
  1) Get career recommendations
  2) View available skills in the dataset
  3) Help
  4) Exit
"""


class RecommenderCLI:
    """Interactive command-line front-end for the recommender."""

    def __init__(self) -> None:
        self._repository = SkillsRepository(RAW_SKILLS_CSV)
        self._recommender = TechStackRecommender(self._repository)

    def run(self) -> None:
        """Main entry point: load data, then loop on the menu until exit."""
        print(_BANNER)
        try:
            self._recommender.load_data()
        except EmptyDatasetError as exc:
            print(f"[FATAL] Could not start the recommender: {exc}")
            return

        while True:
            print(_MENU)
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                self._handle_recommendation_flow()
            elif choice == "2":
                self._show_available_skills()
            elif choice == "3":
                self._show_help()
            elif choice == "4":
                print("Goodbye! Keep building. 🚀")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

    def _handle_recommendation_flow(self) -> None:
        """Collect skills from the user and display recommendations."""
        print(
            "\nEnter at least 3 skills, separated by commas "
            "(e.g. Python, Cloud Computing, Automation):"
        )
        raw_input_line = input("> ").strip()
        user_skills = [s.strip() for s in raw_input_line.split(",") if s.strip()]

        try:
            results = self._recommender.recommend(user_skills, top_n=TOP_N_RESULTS)
        except InsufficientSkillsError as exc:
            print(f"\n[INPUT ERROR] {exc}\n")
            return

        self._display_results(results, user_skills)

    @staticmethod
    def _display_results(
        results: list[RecommendationResult], user_skills: list[str]
    ) -> None:
        print(f"\nBased on your skills ({', '.join(user_skills)}), here are your "
              f"top {len(results)} matches:\n")

        if all(r.score == 0.0 for r in results):
            print("(No strong matches found — showing popular roles instead.)\n")

        for rank, result in enumerate(results, start=1):
            print(f"  {rank}. {result.role_name:<28} match: {result.as_percentage()}")
        print()

    def _show_available_skills(self) -> None:
        """Display the full set of unique skills present in the dataset."""
        all_skills: set[str] = set()
        for role in self._recommender.job_roles:
            all_skills.update(role.skills)

        print(f"\nThere are {len(all_skills)} unique skills in the dataset:\n")
        for skill in sorted(all_skills):
            print(f"  - {skill}")
        print()

    @staticmethod
    def _show_help() -> None:
        print(
            """
HELP
----
This tool recommends career paths based on your technical skills,
using content-based filtering (TF-IDF + Cosine Similarity).

Tips:
  - Provide at least 3 skills for best results.
  - Use specific terms (e.g. "Kubernetes" instead of "containers")
    for more accurate matching.
  - If your skills don't match anything in the dataset, you'll see
    a fallback list of popular roles instead of an error.
"""
        )
