"""
Central configuration for the Tech Stack Recommender.

Keeping constants in one place means tuning behavior (e.g. how many
results to show) never requires touching business logic elsewhere.
"""

from pathlib import Path

# --- Project paths -----------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_SKILLS_CSV: Path = DATA_DIR / "raw_skills.csv"
LOG_DIR: Path = PROJECT_ROOT / "logs"
LOG_FILE: Path = LOG_DIR / "recommender.log"

# --- Pipeline rules -----------------------------------------------------
# The spec (Page 18) mandates a minimum of 3 user inputs for sufficient
# data density. This is a hard business rule, not a UI suggestion.
MIN_SKILLS_REQUIRED: int = 3

# The spec (Page 19) demonstrates truncating output to the Top-3 matches
# to prevent "choice overload."
TOP_N_RESULTS: int = 3

# A cosine similarity score below this is treated as "no meaningful
# match" when deciding whether to trigger the Cold Start fallback.
COLD_START_THRESHOLD: float = 0.0001

# Number of "trending" roles to show when Cold Start fallback triggers.
TRENDING_FALLBACK_COUNT: int = 3
