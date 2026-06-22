# Project 2 Implementation Roadmap

Implementation plan for the **Iris KNN Classification System**, aligned with `docs/requirements.md` and `docs/architecture.md`. Milestones are ordered so each builds on the previous one.

---

## Milestone 1: Project Foundation & Infrastructure

**Objective**  
Establish a runnable Python project with externalized configuration, logging hooks, and the layered folder structure defined in the architecture.

**Deliverables**
- Repository layout (`src/iris_classifier/`, `tests/`, `logs/`, `main.py`)
- `requirements.txt` (Python 3.9+, scikit-learn, PyYAML, etc.)
- `config.yaml` with defaults (random seed, test split ratio, default K, log path)
- `config.py` — ConfigManager to load and validate configuration
- `logger.py` — LoggerService skeleton (console + file handlers)
- Minimal `main.py` entry point that loads config and starts the app shell

**Dependencies**  
None (starting point).

**Complexity**  
**Low** — Standard project scaffolding; no ML logic yet.

**Acceptance criteria**
- Project installs dependencies without errors
- `config.yaml` values load correctly; invalid/missing required keys produce clear errors
- Logger writes to console and a log file path from config
- Folder structure matches the architecture document
- Application starts and exits cleanly from `main.py`

---

## Milestone 2: Data Layer

**Objective**  
Load the Iris dataset and validate user-supplied flower measurements as structured domain objects.

**Deliverables**
- `data/schema.py` — `IrisSample` with `validate()` and `to_array()`
- `data/loader.py` — `DatasetLoader` returning a `Dataset` object (features, labels, feature_names, target_names)
- Dataset summary helper (shape, class distribution, feature names)

**Dependencies**  
Milestone 1 (project structure, config for any loader defaults).

**Complexity**  
**Low** — Small, well-defined dataset; sklearn provides the data.

**Acceptance criteria**
- Iris dataset loads with 150 samples, 4 features, 3 balanced classes (FR-1)
- Summary output includes shape, feature names, and class distribution
- `IrisSample` rejects non-numeric, negative, or empty inputs with clear messages
- Valid samples convert to a 4-element feature array
- Data layer has no CLI or training logic (NFR-2)

---

## Milestone 3: Preprocessing Pipeline

**Objective**  
Implement reproducible train/test splitting and feature scaling as isolated, testable services.

**Deliverables**
- `ml/preprocessing.py` — `PreprocessingService`
- Shuffled train/test split with configurable ratio and fixed random seed (FR-2, NFR-1)
- `StandardScaler` fit on training data only; transform applied to train and test sets (FR-3)
- Return typed split/scaled data structures for downstream use

**Dependencies**  
Milestone 2 (loaded dataset).

**Complexity**  
**Low–Medium** — Straightforward sklearn usage; scaler must not leak test data.

**Acceptance criteria**
- Split uses `shuffle=True` and respects configured random seed (reproducible runs)
- Invalid split ratios (≤0, ≥1, non-numeric) are rejected
- Scaler is fit on training features only; test features are transformed, not re-fit
- Same seed + ratio produces identical splits across runs
- Preprocessing is callable without a terminal or trained model

---

## Milestone 4: Core KNN Model — Train & Predict

**Objective**  
Deliver the mandatory KNN classification workflow: configurable K, training, and prediction on unseen data.

**Deliverables**
- `ml/models.py` — `ModelFactory` (KNN initially)
- `ml/trainer.py` — `TrainingService` to train on scaled training data
- Prediction on scaled test data and single new samples (FR-4, FR-5, FR-6, FR-7, FR-10)
- Validation for K (positive integer, K > training set size)

**Dependencies**  
Milestones 2 and 3 (data + preprocessed splits).

**Complexity**  
**Medium** — Core ML path; input validation and scaler application on new samples matter.

**Acceptance criteria**
- KNN trains successfully with user-configurable K
- Non-numeric K, K ≤ 0, and K larger than training set are rejected with clear errors
- Even K values are allowed with an advisory warning (per edge-case spec)
- Predictions run on held-out test data without retraining
- New sample prediction scales input with the fitted scaler and returns species name
- Attempting prediction before training returns a friendly message, not a crash
- Model/training modules remain independent of CLI (NFR-2, NFR-7)

---

## Milestone 5: Evaluation & Metrics

**Objective**  
Evaluate model performance using required metrics beyond accuracy alone.

**Deliverables**
- `ml/evaluator.py` — `EvaluationService`
- `EvaluationResult` dataclass (accuracy, macro F1, confusion matrix, classification report)
- Confusion matrix generation (FR-8)
- Macro/averaged F1-score and full precision/recall report (FR-9)
- Human-readable `summary()` for CLI display

**Dependencies**  
Milestone 4 (trained model + test predictions).

**Complexity**  
**Low–Medium** — sklearn metrics; emphasis on correct multi-class handling.

**Acceptance criteria**
- Confusion matrix is a 3×3 matrix for the three Iris species
- F1-score is reported (not accuracy alone)
- Classification report includes precision, recall, F1, and accuracy
- Evaluation runs only on test data (generalization demonstrated)
- `EvaluationResult.summary()` produces readable formatted output
- Evaluator is unit-testable with mock predictions

---

## Milestone 6: Experiment Session (Application Layer)

**Objective**  
Orchestrate the full ML workflow in a single session object that holds state and coordinates all domain services.

**Deliverables**
- `core/session.py` — `ExperimentSession`
- Methods: `load_data()`, `train()`, `evaluate()`, `predict_new_sample()`, `get_history()`
- Session state: dataset, scaler, model, last evaluation, command history list
- End-to-end train workflow: split → scale → train → predict → evaluate

**Dependencies**  
Milestones 2–5 (all ML and data components).

**Complexity**  
**Medium** — Integration milestone; state management and ordering of operations.

**Acceptance criteria**
- Session loads data once and reuses it across operations
- Full train pipeline executes in correct order without manual CLI steps
- Session tracks whether a model is trained before allowing prediction
- Each completed operation appends an entry to in-session history (FR-16 foundation)
- Session can be driven programmatically (no terminal required) for testing
- Invalid operations return structured errors, not unhandled exceptions

---

## Milestone 7: Interactive CLI

**Objective**  
Expose the application through a menu-driven terminal interface with robust input handling.

**Deliverables**
- `cli/menu.py` — `MenuRenderer` (menus, prompts, formatted reports)
- `cli/app.py` — `CLIApplication` main loop
- Main menu: Train Model, View Evaluation, Predict New Sample, Compare K Values, View History, Help, Exit
- Train workflow prompts: algorithm, K, test split ratio
- Graceful handling of invalid input, empty input, and keyboard interrupt (Ctrl+C)

**Dependencies**  
Milestone 6 (ExperimentSession).

**Complexity**  
**Medium** — UX and validation logic; many edge cases from requirements.

**Acceptance criteria**
- Menu-driven CLI runs continuously until Exit (FR-11)
- All menu options reachable and return to the main menu after completion
- Invalid menu choices, numeric inputs, and ratios are handled without crashing (NFR-5)
- Ctrl+C exits cleanly without stack traces
- Dataset summary and training reports display clearly (NFR-8)
- CLI contains no direct sklearn calls — only delegates to session/services (NFR-2)

---

## Milestone 8: Extended Features — Tuning, Multi-Algorithm, Logging & Config

**Objective**  
Complete Phase 7 enhancements: hyperparameter comparison, alternative classifiers, persistent logs, and full config externalization.

**Deliverables**
- `ml/tuner.py` — `HyperparameterTuner` for K-value comparison and elbow-style error report (FR-12)
- Extended `ModelFactory`: Logistic Regression and Decision Tree (FR-13)
- Experiment logging to file via `LoggerService` (FR-14)
- All hardcoded defaults moved to `config.yaml` (FR-15)
- Session history viewable from CLI (FR-16)
- Probability/confidence scores where the algorithm supports them

**Dependencies**  
Milestones 6 and 7 (session + CLI shell).

**Complexity**  
**Medium–High** — Multiple features; K comparison loop; log persistence edge cases.

**Acceptance criteria**
- User can compare multiple K values and see error rates in tabular/report form
- KNN, Logistic Regression, and Decision Tree are selectable and train successfully
- Each training run is appended to the experiment log file with timestamp, algorithm, K, and metrics
- Log file write failures are handled gracefully (app continues, user is warned)
- Config changes (seed, default K, split ratio, log path) take effect without code edits
- History menu shows prior session commands/results
- Algorithms that support `predict_proba` display confidence scores

---

## Milestone 9: Testing, Quality & Documentation

**Objective**  
Verify correctness, maintainability, and portability; deliver a complete, submittable project.

**Deliverables**
- Unit tests under `tests/` mirroring module structure (loader, preprocessing, trainer, evaluator, tuner, session)
- `README.md` with setup, usage, configuration, and example session walkthrough
- PEP 8 compliance, type hints, and docstrings on public APIs (NFR-3)
- Final integration smoke test of the full CLI workflow

**Dependencies**  
All prior milestones (especially 4–8 for meaningful test coverage).

**Complexity**  
**Medium** — Test design and documentation; not algorithmically hard.

**Acceptance criteria**
- Core functions (split/scale, train, evaluate, validate sample) have passing unit tests (NFR-7)
- Tests run without manual dataset download or CLI interaction
- README allows a new developer to install, configure, and run the app on Python 3.9+
- Public modules include type hints and docstrings
- Full mandatory requirement checklist (FR-1 through FR-10) verified end-to-end via CLI
- Extended requirements (FR-11 through FR-16) verified where implemented in Milestone 8
- No secrets or environment-specific paths committed

---

## Milestone Dependency Overview

```text
M1 Foundation
 └── M2 Data Layer
      └── M3 Preprocessing
           └── M4 KNN Train/Predict
                └── M5 Evaluation
                     └── M6 Experiment Session
                          └── M7 CLI
                               └── M8 Extended Features
                                    └── M9 Testing & Docs
```

---

## Complexity Summary

| Milestone | Complexity | Primary risk |
|-----------|------------|--------------|
| M1 Foundation | Low | Config validation gaps |
| M2 Data Layer | Low | Input validation completeness |
| M3 Preprocessing | Low–Medium | Data leakage via scaler |
| M4 KNN Train/Predict | Medium | New-sample scaling consistency |
| M5 Evaluation | Low–Medium | Multi-class metric correctness |
| M6 Session | Medium | State/lifecycle bugs |
| M7 CLI | Medium | Edge-case input handling |
| M8 Extended Features | Medium–High | Scope creep; log failure paths |
| M9 Testing & Docs | Medium | Test isolation from CLI |

---

## Suggested Delivery Phases

| Phase | Milestones | Covers |
|-------|------------|--------|
| **Core ML (minimum viable)** | M1 → M5 | FR-1 through FR-10 |
| **Usable application** | M6 → M7 | Runnable CLI + full workflow |
| **Production-ready submission** | M8 → M9 | Extended features + quality bar |

Milestones 1–5 satisfy the mandatory specification; 6–7 make it a complete interactive application; 8–9 meet extended requirements and engineering standards from the internship rubric.

---

*Roadmap derived from `docs/requirements.md` and `docs/architecture.md`.*
