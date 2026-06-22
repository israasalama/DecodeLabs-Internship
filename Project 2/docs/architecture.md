# DecodeLabs AI Internship — Project 2 Solution Design

**Source:** Derived from `requirements.md` (Project 2 Specification Analysis)

---

# PHASE 2 — SYSTEM DESIGN

## 1. Architectural Style

The system follows a **Layered / Clean Architecture** approach that separates responsibilities into independent layers.

```text
┌─────────────────────────────────────────┐
│              CLI / UI LAYER             │
│      Menus, prompts, reports, output    │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│          APPLICATION LAYER              │
│     Experiment and session control      │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│            DOMAIN / ML LAYER            │
│ Data loading, preprocessing, training,  │
│ prediction, evaluation, tuning          │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│         INFRASTRUCTURE LAYER            │
│      Configuration, logging, I/O        │
└─────────────────────────────────────────┘
```

### Design Benefits

- ML logic remains independent from user interaction.
- Every ML component can be unit tested without a terminal.
- The CLI can later be replaced by a web API or SaaS interface.
- Closely follows the Input → Process → Output framework from the project specification.
- Encourages maintainability, scalability, and clean separation of concerns.

---

## 2. Folder Structure

```text
iris-classifier/
│
├── src/
│   └── iris_classifier/
│       ├── config.py
│       ├── logger.py
│       │
│       ├── data/
│       │   ├── loader.py
│       │   └── schema.py
│       │
│       ├── ml/
│       │   ├── preprocessing.py
│       │   ├── models.py
│       │   ├── trainer.py
│       │   ├── evaluator.py
│       │   └── tuner.py
│       │
│       ├── core/
│       │   └── session.py
│       │
│       └── cli/
│           ├── menu.py
│           └── app.py
│
├── tests/
├── logs/
├── config.yaml
├── requirements.txt
├── README.md
└── main.py
```

### Design Rationale

- Data handling is isolated from machine learning logic.
- Models are created through a factory pattern.
- Session management acts as the single source of truth.
- Configuration is externalized rather than hardcoded.
- Test structure mirrors application structure.

---

## 3. Components

| Component | Purpose |
|------------|---------|
| ConfigManager | Loads and validates configuration values |
| LoggerService | Handles experiment logging |
| DatasetLoader | Loads the Iris dataset |
| IrisSample | Represents a flower sample and validates input |
| PreprocessingService | Splits and scales data |
| ModelFactory | Creates machine learning models |
| TrainingService | Trains selected models |
| EvaluationService | Calculates metrics and confusion matrices |
| HyperparameterTuner | Compares multiple K values |
| ExperimentSession | Coordinates application workflow |
| MenuRenderer | Displays CLI menus |
| CLIApplication | Main user interface controller |

---

## 4. Module Breakdown

| Module | Responsibility |
|----------|----------------|
| config.py | Load configuration and defaults |
| logger.py | Configure file and console logging |
| data/schema.py | Input validation models |
| data/loader.py | Load Iris dataset |
| ml/preprocessing.py | Split and scale data |
| ml/models.py | Create ML models |
| ml/trainer.py | Train classifiers |
| ml/evaluator.py | Generate evaluation metrics |
| ml/tuner.py | Perform K-value analysis |
| core/session.py | Coordinate complete workflows |
| cli/menu.py | Menu rendering and validation |
| cli/app.py | Main application loop |
| main.py | Entry point |

---

## 5. Classes

### Dataset

| Attribute | Type |
|------------|------|
| features | ndarray |
| labels | ndarray |
| feature_names | list |
| target_names | list |

---

### IrisSample

| Attribute | Type |
|------------|------|
| sepal_length | float |
| sepal_width | float |
| petal_length | float |
| petal_width | float |

#### Methods

- validate()
- to_array()

---

### EvaluationResult

| Attribute | Type |
|------------|------|
| accuracy | float |
| macro_f1 | float |
| confusion_matrix | ndarray |
| report | str |

#### Methods

- summary()

---

### ExperimentSession

| Attribute | Description |
|------------|-------------|
| dataset | Loaded dataset |
| scaler | StandardScaler instance |
| model | Current trained model |
| last_evaluation | Latest evaluation result |
| history | Session command history |

#### Methods

- load_data()
- train()
- evaluate()
- predict_new_sample()
- compare_k_values()
- get_history()

---

## 6. Responsibilities Mapping

| Requirement | Responsible Component |
|-------------|----------------------|
| Dataset loading | DatasetLoader |
| Train/Test Split | PreprocessingService |
| Feature Scaling | PreprocessingService |
| KNN Training | TrainingService |
| Alternative Models | ModelFactory |
| Prediction | ExperimentSession |
| Confusion Matrix | EvaluationService |
| F1 Score | EvaluationService |
| K Comparison | HyperparameterTuner |
| Logging | LoggerService |
| Session History | ExperimentSession |
| CLI Interaction | CLIApplication |

---

## 7. Data Flow

```text
User
 │
 ▼
CLI Layer
 │
 ▼
Experiment Session
 │
 ├── Dataset Loader
 ├── Preprocessing Service
 ├── Model Factory
 ├── Training Service
 ├── Evaluation Service
 └── Hyperparameter Tuner
 │
 ▼
Results
 │
 ▼
CLI Output
```

### IPO Mapping

| Stage | Modules |
|---------|----------|
| Input | DatasetLoader, MenuRenderer |
| Process | PreprocessingService, ModelFactory, TrainingService |
| Output | EvaluationService, CLIApplication |

---

## 8. Execution Flow

```text
START
  │
  ├─ Load configuration
  ├─ Initialize logger
  ├─ Create ExperimentSession
  ├─ Load Iris dataset
  │
  ▼
Display Main Menu
  │
  ├─ Train Model
  ├─ View Evaluation
  ├─ Predict New Sample
  ├─ Compare K Values
  ├─ View History
  ├─ Help
  └─ Exit
  │
  ▼
Execute Selected Operation
  │
  ▼
Return to Menu
  │
  ▼
EXIT
```

---

## 9. Train Model Workflow

```text
User selects Train Model
          │
          ▼
Choose Algorithm
          │
          ▼
Enter K Value (if KNN)
          │
          ▼
Enter Test Split Ratio
          │
          ▼
Split Dataset
          │
          ▼
Scale Features
          │
          ▼
Create Model
          │
          ▼
Train Model
          │
          ▼
Predict Test Data
          │
          ▼
Evaluate Performance
          │
          ▼
Store Results + Log Run
          │
          ▼
Display Metrics
```

---

## 10. Future Scalability

### Machine Learning Enhancements

- Cross-validation support
- GridSearchCV integration
- Additional classifiers
- Probability calibration
- ROC and AUC analysis

### Data Enhancements

- CSV dataset support
- Data validation schemas
- Dataset profiling

### User Experience Enhancements

- Graphical visualizations
- Web interface
- REST API
- Dashboard reporting

### Engineering Enhancements

- Model persistence
- Dependency injection
- Plugin architecture
- Automated testing pipelines

---

## Design Summary

| Concern | Design Choice |
|----------|--------------|
| Architecture | Layered Clean Architecture |
| Dataset | Built-in Iris Dataset |
| Models | KNN + extensible model factory |
| State Management | ExperimentSession |
| Configuration | External YAML file |
| Logging | File-based experiment logs |
| Evaluation | Confusion Matrix + F1 Score |
| Extensibility | Modular and testable components |

This design satisfies all Project 2 functional and non-functional requirements while remaining scalable, maintainable, and suitable for future expansion into larger machine learning applications.

---

*Solution design based on Project 2 requirements and Phase 2 architecture planning.*
