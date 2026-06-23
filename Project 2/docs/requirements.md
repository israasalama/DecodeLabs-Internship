# DecodeLabs AI Internship — Project 2 Requirements

**Source:** `Artificial intelligence P2.pdf` (Industrial Training Kit, Batch 2026)

---

## 1. Project Objective

Build a complete supervised machine learning classification system for the Iris dataset that predicts one of three species:

- Setosa
- Versicolor
- Virginica

The system must demonstrate a full ML workflow from data loading through model training, evaluation, and prediction on unseen examples.

### Primary goals

- Load and inspect the Iris dataset
- Preprocess and scale feature data
- Split data into reproducible training and test sets
- Train a K-Nearest Neighbors classifier
- Evaluate using confusion matrix and F1-score
- Predict new flower measurements accurately
- Provide a usable CLI interface for interaction

---

## 2. Functional Requirements

### Mandatory requirements

1. Dataset loading
   - Load Iris dataset from `scikit-learn`
   - Preserve feature and target label metadata
2. Train/test split
   - Split data into training and test sets
   - Use shuffling and a fixed random seed for reproducibility
3. Feature scaling
   - Apply `StandardScaler` before model training
4. Classification algorithm
   - Train and use a KNN classifier
5. Configurable hyperparameter
   - Allow user-specified `K` for KNN
6. Model training
   - Train using the training set only
7. Prediction
   - Predict labels for the hold-out test set
8. Evaluation metrics
   - Compute confusion matrix
   - Compute F1-score and accuracy
9. New sample prediction
   - Accept new flower measurements from the user and return a predicted species
10. External configuration
   - Store settings in `config.yaml` rather than hardcoding values

### Portfolio-enhancing requirements

1. Interactive CLI
   - Provide a menu-driven terminal interface
2. Conversational command mode
   - Accept natural command phrases in a second command mode
3. Multiple algorithm support
   - Include Logistic Regression and Decision Tree options alongside KNN
4. Tuning and comparison
   - Support K-value tuning and comparison across configured values
5. Session history
   - Track executed commands during a session
6. Logging
   - Persist experiment and application events to a file
7. Personality modes
   - Provide configurable response styles such as professional and friendly

---

## 3. Non-Functional Requirements

- Reproducibility
  - Fixed random seed for stable results
- Modularity
  - Separate components for data, preprocessing, modeling, evaluation, and CLI
- Maintainability
  - Use PEP8-compliant code, type hints, and docstrings
- Robustness
  - Validate user input and avoid crashes on invalid input
- Portability
  - Run on Python 3.9+ across Windows/macOS/Linux
- Testability
  - Ensure core services are unit-testable
- Usability
  - Provide clear prompts, feedback, and error messages
- Performance
  - Efficient handling of the small Iris dataset with no unnecessary overhead

---

## 4. Constraints

- Dataset: Iris dataset only
- ML framework: Use `scikit-learn` for data, preprocessing, and modeling
- Scaling: `StandardScaler` required before training
- Data splitting: Data must be shuffled before split
- Evaluation: Must include confusion matrix and F1-score, not accuracy alone
- Interface: Terminal-based CLI application
- Execution: Single-machine runtime, no server infrastructure

---

## 5. Inputs

- Iris dataset loaded from `sklearn.datasets`
- User menu selections and conversational commands
- K value for KNN
- Algorithm choice (`knn`, `logistic`, `tree`)
- Optional train/test split ratio via configuration
- Flower measurements: sepal length, sepal width, petal length, petal width
- Configuration settings from `config.yaml`

---

## 6. Outputs

- Dataset summary and metadata
- Training summary and chosen algorithm details
- Confusion matrix display
- Classification metrics: accuracy, precision, recall, F1-score
- Predicted species for new measurements
- K tuning results and best K selection
- CLI command history and session status
- Persisted logs for experiment activity
- Friendly validation and error messages

---

## 7. AI Concepts Covered

- Supervised learning
- Classification
- Feature scaling
- Train/test split
- Model evaluation
- Hyperparameter tuning
- Distance-based learning (KNN)
- Algorithm comparison
- Generalization to unseen data

---

## 8. Edge Cases

- Non-numeric K or measurement values
- K values ≤ 0 or larger than the training set
- Invalid command or menu input
- Prediction attempted before training
- Empty or malformed input
- Keyboard interrupts during CLI use
- Logging or configuration file access failures

---

## 9. Future Improvements

- Add cross-validation and learning curves
- Add external dataset upload support
- Persist models with export/import
- Add plots for confusion matrix and metrics
- Build a web or API frontend
- Add probability calibration and ROC analysis
- Use schema validation libraries for input data

---

## 10. Skills Assessed

- Machine learning pipeline design
- Data preprocessing and scaling
- Classifier training and evaluation
- CLI user experience design
- Configuration management
- Logging and session tracking
- Unit and integration testing
- Clean architecture and modular code

---

*This refined requirements document is aligned with the completed Project 2 implementation and the portfolio-grade Phase 7 enhancements.*
