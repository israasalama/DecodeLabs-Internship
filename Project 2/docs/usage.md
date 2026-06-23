# Usage Guide

This guide explains how to run and interact with the Iris Flower Classification System.

## Running the Application

From the project root directory:

```bash
python main.py
```

The application opens a menu-driven CLI.

## CLI Workflow

1. **Load Dataset**
   - Loads the Iris dataset from scikit-learn.
   - Shows dataset summary information.

2. **Preprocess Data**
   - Splits the dataset into training and test sets.
   - Applies `StandardScaler` to training data and transforms test data.

3. **Train Model**
   - Select the algorithm: `knn`, `logistic`, or `tree`.
   - If `knn` is selected, enter the desired `K` value.

4. **Evaluate Model**
   - Computes accuracy, F1 macro score, confusion matrix, and classification report.

5. **Predict New Sample**
   - Enter sepal and petal measurements.
   - The CLI returns the predicted species.

6. **Tune K Value**
   - Runs KNN tuning over configured `k_range` values.
   - Displays the best `k` based on accuracy and F1.

7. **View Session Info**
   - Displays completed steps and recent command history.

8. **Quick Demo (Auto)**
   - Runs a full automated pipeline: load, preprocess, train, evaluate, predict.

9. **Reset Session**
   - Clears session state and history.

10. **Exit**
    - Closes the application.

## Conversational Command Mode

The CLI also supports a chat-style command mode. Choose option `2` from the startup prompt and enter commands such as:

- `load`
- `preprocess`
- `train knn 3`
- `evaluate`
- `predict 5.1 3.5 1.4 0.2`
- `mode friendly`
- `mode professional`
- `history`
- `session`
- `reset`
- `help`
- `exit`

This mode offers flexible navigation and configurable personality responses.

## Example Interaction

After starting the app, follow this sample sequence:

1. Choose `1` to load the dataset.
2. Choose `2` to preprocess the data.
3. Choose `3` to train the model.
   - Enter `knn` and `3` for K.
4. Choose `4` to evaluate the trained model.
5. Choose `5` to predict a new sample.
   - Enter `5.1`, `3.5`, `1.4`, `0.2` for the four measurements.

Expected prediction output:

- Predicted species: `SETOSA`

## Error Handling

The CLI validates user inputs and prints helpful errors when:
- non-numeric values are entered for measurements
- invalid K values are provided
- operations are attempted in the wrong order

## Configuration Overrides

Change settings in `config.yaml`:
- `ml.random_seed`
- `ml.test_split_ratio`
- `ml.default_k`
- `ml.k_range`
- `logging.log_file`
- `cli.history_size`
- `cli.default_personality`
