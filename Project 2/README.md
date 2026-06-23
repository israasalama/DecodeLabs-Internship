# Iris Flower Classification System

A clean, modular Python project that trains and evaluates a supervised machine learning classifier for the Iris dataset using K-Nearest Neighbors (KNN).

## Overview

This project demonstrates a production-style ML pipeline with:
- Dataset loading
- Train/test splitting with shuffling and a fixed random seed
- Feature scaling using `StandardScaler`
- Configurable KNN training
- Prediction on unseen data
- Confusion matrix and F1-score evaluation
- Interactive CLI with session state, tuning, and history tracking

## Project Structure

- `config.yaml` — external configuration for ML settings, logging, and CLI
- `main.py` — entry point for the CLI application
- `src/iris_classifier/` — modular implementation:
  - `config.py` — configuration loader and validator
  - `logger.py` — centralized logging service
  - `data/` — dataset loader and input schema
  - `ml/` — preprocessing, modeling, training, evaluation, and tuning
  - `core/` — experiment session orchestration
  - `cli/` — interactive menu and application shell
- `tests/` — unit and integration tests
- `requirements.txt` — required Python packages

## Installation

### Prerequisites

- Python 3.9+ installed
- Optional: virtual environment recommended

### Setup

1. Open a terminal in the project root:
   ```bash
   cd "c:/Users/israa/Projects/DecodeLabs-Internship/Project 2"
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the application

```bash
python main.py
```

The CLI provides the following options:
- Load dataset
- Preprocess data (train/test split + scaling)
- Train model with KNN, Logistic Regression, or Decision Tree
- Evaluate model using confusion matrix and F1-score
- Predict a new iris sample from user input
- Tune K values automatically using configurable search values
- View session info and command history
- Reset the session
- Run an automated demo workflow
- Enter conversational command mode with natural-style commands
- Switch personality mode between `professional` and `friendly`

### Example interaction

Once the CLI starts, choose options in order:
1. Load Dataset
2. Preprocess Data
3. Train Model
4. Evaluate Model
5. Predict New Sample

Example sample values for prediction:
- Sepal length: `5.1`
- Sepal width: `3.5`
- Petal length: `1.4`
- Petal width: `0.2`

### Quick demo mode

Select **Quick Demo (Auto)** to execute a full pipeline automatically:
- load dataset
- preprocess
- train KNN with default configuration
- evaluate
- predict a known sample

## Testing

Run the full test suite with:

```bash
python -m pytest tests/ -q
```

All tests verify functionality across configuration, preprocessing, training, evaluation, and end-to-end workflows.

## Configuration

Important settings are stored in `config.yaml`:
- `ml.random_seed` — reproducible split and training behavior
- `ml.test_split_ratio` — test dataset proportion
- `ml.default_k` — default K value for KNN
- `ml.k_range` — K values evaluated during tuning
- `logging.log_file` — path to save experiment logs
- `cli.history_size` — number of commands kept in session history
- `cli.default_personality` — starting response personality mode for the CLI

## Future Enhancements

Potential upgrades to improve portfolio quality:
- Persist experiment metadata to JSON or SQLite
- Add support for dataset augmentation and cross-validation
- Add model comparison reports for KNN, Logistic Regression, and Decision Tree
- Add model export/import and saved experiment replay
- Add a web interface or REST API for prediction requests

## Why this project matters

This system illustrates how AI systems move beyond hardcoded rules into data-driven classification. It uses real machine learning components to learn from examples, preprocess inputs, evaluate predictions, and generalize to new data.

## License

This project is intended for educational use and portfolio demonstration.
