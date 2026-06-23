# Iris Flower Classification System Documentation

This documentation mirrors the main README and provides project usage details, implementation notes, and enhancement ideas.

## Installation

1. Open a terminal in the repository root.
2. Optionally create a Python virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python main.py
```

The CLI supports the following operations:
- Load dataset
- Preprocess data
- Train model
- Evaluate model
- Predict new sample
- Tune K values
- View session state
- Reset session
- Run demo workflow

## Configuration

Change behavior via `config.yaml`:
- `ml.random_seed`
- `ml.test_split_ratio`
- `ml.default_k`
- `ml.k_range`
- `logging.level`
- `logging.log_file`
- `cli.history_size`

## Testing

```bash
python -m pytest tests/ -q
```

## Future improvements

- Add persistence for experiments
- Extend support for extra datasets
- Add a web or API front end
- Add chat-style personality modes
