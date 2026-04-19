# Spam Detection MLOps

A spam classification project that includes data preparation, model training, API deployment, and CI validation.

## Problem statement

Build a machine learning system that can classify SMS messages as ham or spam using NLP, and expose the model via a REST API.

## Model approach and results

- Approach: clean and preprocess raw SMS text, convert to TF-IDF features, and train a Logistic Regression classifier.
- Metrics logged: accuracy, F1 score, precision, recall.
- The pipeline is built in `src/train.py` and now includes MLflow tracking for parameters, metrics, and model artifacts.

## Repository structure

- `data/` - dataset files
- `notebooks/` - exploratory notebooks
- `src/` - preprocessing and training code
- `app/` - FastAPI application
- `tests/` - unit tests
- `models/` - trained model artifacts
- `.github/workflows/` - CI workflow

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

## Run with Docker

```bash
docker build -t spam-detection-api .
docker run -p 8000:8000 spam-detection-api
```

## API usage example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message":"Congratulations! You have won a free prize. Click here to claim."}'
```

## Test

```bash
pytest
```
