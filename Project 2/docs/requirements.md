# DecodeLabs AI Internship — Project 2 Specification Analysis

**Source:** `Artificial intelligence P2.pdf` (Industrial Training Kit, Batch 2026)

---

## 1. Project Objective

Build a **Supervised Machine Learning Classification System** that classifies Iris flowers into one of three species:

- Setosa
- Versicolor
- Virginica

using four physical flower measurements and the **K-Nearest Neighbors (KNN)** algorithm.

The project serves as the transition from deterministic rule-based systems to data-driven learning systems. Instead of manually writing rules, historical labeled examples are provided and the machine learns patterns from data.

The complete machine learning pipeline must be demonstrated:

- Data loading
- Data preprocessing
- Train/test splitting
- Feature scaling
- Model training
- Prediction
- Evaluation
- Generalization to unseen data

This project validates understanding of how machine learning systems are built, evaluated, and improved rather than simply calling a library function.

---

## 2. Functional Requirements

### Core goal (explicit)

Create a machine learning application that predicts Iris flower species using supervised classification.

### Mandatory requirements (Project 2 specification)

| # | Requirement | Description |
|---|-------------|-------------|
| FR-1 | **Dataset loading** | Load and understand the Iris dataset (150 samples, 4 features, 3 balanced classes). |
| FR-2 | **Train/test split** | Split data into training and testing sets with shuffling enabled. |
| FR-3 | **Feature scaling** | Apply StandardScaler before model training. |
| FR-4 | **Classification algorithm** | Implement K-Nearest Neighbors (KNN). |
| FR-5 | **Configurable K** | Allow changing the number of neighbors (K). |
| FR-6 | **Model training** | Train the classifier using the training dataset. |
| FR-7 | **Prediction** | Generate predictions on unseen testing data. |
| FR-8 | **Confusion Matrix** | Evaluate predictions using a confusion matrix. |
| FR-9 | **F1 Score** | Evaluate using F1-score rather than relying solely on accuracy. |
| FR-10 | **New sample prediction** | Predict the class of unseen flower measurements. |

### Extended requirements (Phase 7 enhancements)

| # | Requirement |
|---|-------------|
| FR-11 | Provide an interactive menu-driven CLI. |
| FR-12 | Allow comparing multiple K values and generate an elbow-style error comparison. |
| FR-13 | Support multiple algorithms (KNN plus Logistic Regression and/or Decision Tree). |
| FR-14 | Persist experiment results in a log file. |
| FR-15 | Externalize configuration values instead of hardcoding them. |
| FR-16 | Maintain in-session command history. |

---

## 3. Non-Functional Requirements

| # | Category | Requirement |
|---|----------|-------------|
| NFR-1 | **Reproducibility** | Fixed random seed ensures consistent train/test splits and repeatable results. |
| NFR-2 | **Modularity** | Data loading, preprocessing, training, evaluation, and UI should be separate components. |
| NFR-3 | **Maintainability** | Follow PEP8, type hints, docstrings, and clean architecture principles. |
| NFR-4 | **Performance** | Efficient enough for the small Iris dataset without unnecessary overhead. |
| NFR-5 | **Robustness** | Invalid user input must be handled gracefully without crashing. |
| NFR-6 | **Portability** | Must run on any platform supporting Python 3.9+ and required dependencies. |
| NFR-7 | **Testability** | Core functions should be independently unit testable. |
| NFR-8 | **Usability** | CLI interactions should be clear, informative, and user-friendly. |

---

## 4. Constraints

| Constraint | Detail |
|------------|--------|
| **Dataset** | Must use the Iris dataset. |
| **ML framework** | Must use scikit-learn for dataset handling, preprocessing, training, and evaluation. |
| **Scaling requirement** | StandardScaler must be applied before training. |
| **Data splitting** | Dataset must be shuffled before train/test split. |
| **Evaluation requirement** | Accuracy alone is insufficient; confusion matrix and F1-score are mandatory. |
| **Application type** | Terminal-based application only. |
| **Execution model** | Single-machine execution; no server infrastructure required. |

---

## 5. Inputs

| Input | Description |
|-------|-------------|
| **Iris dataset** | Loaded automatically from sklearn datasets. |
| **Menu choice** | User selects available operations. |
| **K value** | Positive integer representing number of neighbors. |
| **Algorithm choice** | KNN, Logistic Regression, or Decision Tree. |
| **Train/test ratio** | Optional user-defined split ratio. |
| **Flower measurements** | Sepal length, sepal width, petal length, petal width. |
| **Random seed** | Optional value controlling reproducibility. |

---

## 6. Outputs

| Output | Description |
|--------|-------------|
| **Dataset summary** | Shape, class distribution, and feature information. |
| **Training report** | Model type, configuration, and training details. |
| **Confusion Matrix** | Multi-class evaluation matrix. |
| **Classification metrics** | Precision, recall, F1-score, and accuracy. |
| **Predicted species** | Classification result for new flower samples. |
| **Probability scores** | Prediction confidence where supported. |
| **K comparison report** | Error rates across multiple K values. |
| **Experiment logs** | Persisted records of previous runs. |
| **Validation messages** | Friendly error and warning messages. |

---

## 7. AI Concepts Involved

| Concept | Where it appears |
|----------|------------------|
| **Supervised Learning** | Learning from labeled examples. |
| **Classification** | Predicting discrete flower species. |
| **Feature Space** | Representing flowers using four numerical features. |
| **Distance Metrics** | KNN uses distance between feature vectors. |
| **Feature Scaling** | Standardization prevents feature dominance. |
| **Generalization** | Evaluating performance on unseen test data. |
| **Train/Test Split** | Separating learning and evaluation data. |
| **Hyperparameter Tuning** | Selecting the best value of K. |
| **Lazy Learning** | KNN stores examples and computes at prediction time. |
| **Model Evaluation** | Confusion Matrix, Precision, Recall, F1-score, Accuracy. |
| **Precision/Recall Tradeoff** | Understanding metric selection based on context. |
| **Algorithm Comparison** | Comparing KNN against alternative classifiers. |

---

## 8. Edge Cases

| Edge case | Expected behavior |
|-----------|------------------|
| Non-numeric K value | Reject input and request correction. |
| K ≤ 0 | Display validation error. |
| K larger than training set | Explain error without crashing. |
| Even K value | Allow but provide advisory warning. |
| Negative measurements | Warn user about unrealistic values. |
| Extreme outlier measurements | Predict normally and show confidence. |
| Invalid train/test ratio | Reject and request valid value. |
| Empty input | Prompt user again. |
| Prediction before training | Inform user that a model must be trained first. |
| Log file unavailable | Handle failure gracefully. |
| Keyboard interrupt | Exit cleanly without stack traces. |

---

## 9. Possible Future Improvements

- K-fold cross-validation.
- Automated hyperparameter tuning with GridSearchCV.
- Support for external CSV datasets.
- Visualization dashboards and plots.
- Model persistence using joblib or pickle.
- REST API or web interface.
- Probability calibration and ROC/AUC analysis.
- Schema-based data validation using tools such as Pydantic.

---

## 10. Skills Being Tested

| Skill area | What the project assesses |
|------------|---------------------------|
| **Machine Learning Fundamentals** | Understanding supervised learning workflows. |
| **Data Preprocessing** | Scaling, cleaning, and preparing data. |
| **Model Training** | Building and configuring classifiers. |
| **Evaluation Metrics** | Using confusion matrices and F1-scores correctly. |
| **Hyperparameter Tuning** | Selecting suitable K values. |
| **Python Development** | Building maintainable and modular applications. |
| **Software Architecture** | Separation of concerns and reusable design. |
| **Error Handling** | Robust handling of invalid input and failures. |
| **Experimentation** | Comparing algorithms and configurations. |
| **Professional Engineering Practices** | Logging, configuration management, and testing. |

---

## Summary

Project 2 introduces machine learning through the Iris classification problem. Students must build a complete supervised learning pipeline that loads data, scales features, trains classifiers, evaluates performance using meaningful metrics, and predicts unseen samples. Success demonstrates mastery of the transition from deterministic logic systems to data-driven AI systems while maintaining software engineering best practices.

---

*Analysis based on the Project 2 specification and requirements provided.*
