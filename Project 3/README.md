# Tech Stack Recommender — Project 3 (DecodeLabs AI Track)

A **content-based recommendation engine** that maps a user's technical
skills to the most relevant career/job roles, built entirely from
first-principles similarity mathematics — no machine learning model
training, no external libraries, no collaborative filtering.

> This is the "Digital Matchmaker" milestone: before building neural
> collaborative-filtering models, this project proves mastery of the
> fundamental logic that powers real recommender systems like
> Netflix's and Amazon's — **TF-IDF feature weighting + Cosine
> Similarity matching.**

---

## How It Works

```
Input (your skills) → Process (TF-IDF + Cosine Similarity) → Output (Top-3 career matches)
```

1. **Ingestion** — You provide at least 3 skills.
2. **Scoring** — Each skill set (yours and every job role's) is converted
   into a TF-IDF weighted vector, and Cosine Similarity measures how
   closely your "direction" of interests aligns with each role.
3. **Sorting** — Roles are ranked by similarity score, highest first.
4. **Filtering** — Only the Top 3 matches are shown, to avoid choice overload.

If your skills don't match anything in the dataset (a "Cold Start"),
the system gracefully falls back to a list of popular roles instead of
returning an error.

---

## Installation

**Requirements:** Python 3.10+ (uses modern type-hint syntax like `list[str]`)

```bash
# 1. Clone or download the project
cd tech_stack_recommender

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install dev/test dependencies
pip install -r requirements.txt
```

> **Note:** The recommendation engine itself has **zero third-party
> dependencies** — only the Python standard library (`math`, `csv`,
> `dataclasses`, `collections`) is used. `pytest` is only needed if you
> want to run the test suite.

---

## Usage

Run the interactive CLI:

```bash
python main.py
```

You'll see a menu:

```
============================================================
   DECODELABS  |  AI TECH STACK RECOMMENDER  (Project 3)
============================================================

What would you like to do?
  1) Get career recommendations
  2) View available skills in the dataset
  3) Help
  4) Exit
```

### Example Interaction

```
Enter your choice (1-4): 1

Enter at least 3 skills, separated by commas
(e.g. Python, Cloud Computing, Automation):
> Python, Cloud Computing, Automation

Based on your skills (Python, Cloud Computing, Automation), here are your top 3 matches:

  1. Cloud Architect              match: 43.5%
  2. Data Engineer                match: 31.0%
  3. QA Automation Engineer       match: 19.0%
```

### Cold Start Example

```
Enter your choice (1-4): 1
> made up skill, another fake one, totally unknown

Based on your skills (made up skill, another fake one, totally unknown), here are your top 3 matches:

(No strong matches found — showing popular roles instead.)

  1. AI Research Engineer         match: 0.0%
  2. Backend Developer            match: 0.0%
  3. Cloud Architect              match: 0.0%
```

---

## Project Structure

```
tech_stack_recommender/
├── data/raw_skills.csv          # Job roles → required skills dataset
├── src/
│   ├── config.py                # Tunable constants
│   ├── exceptions.py            # Custom exception types
│   ├── data_layer/               # CSV loading & data models
│   ├── core/                     # Normalizer, TF-IDF, Cosine Similarity
│   ├── pipeline/                 # The 4-step recommendation pipeline
│   └── interface/                # CLI front-end
├── tests/                         # 40 unit + integration tests
├── logs/recommender.log          # Runtime logs
└── main.py                        # Entry point
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

40 tests covering normalization, TF-IDF math, cosine similarity edge
cases, CSV loading/validation, and full pipeline integration
(including Cold Start fallback).

---

## Future Enhancements

- Let users **rate** recommendations to build a feedback loop toward
  hybrid (content + collaborative) filtering
- Support **weighted skill proficiency** (e.g., "Python: expert" vs.
  "Python: beginner") instead of binary presence/absence
- Expand the synonym map to catch more naming-convention mismatches
  (e.g., "Web Design" ↔ "Frontend Development")
- Replace the alphabetical Cold Start fallback with real popularity
  data once usage telemetry exists
- Swap the CSV repository for a database-backed one without touching
  any other layer (the architecture already supports this)

---

## Credits

Built as part of the **DecodeLabs Industrial Training Kit — AI Track,
Batch 2026, Project 3: AI Recommendation Logic.**
