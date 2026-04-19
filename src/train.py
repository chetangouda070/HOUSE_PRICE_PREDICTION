from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("MLflow not available, skipping experiment tracking")

from src.preprocess import load_data

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = REPO_ROOT / 'data' / 'spam.csv'
DEFAULT_MODEL_PATH = REPO_ROOT / 'models' / 'model.pkl'
DEFAULT_METADATA_PATH = REPO_ROOT / 'models' / 'model_metadata.pkl'


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                'tfidf',
                TfidfVectorizer(
                    max_features=5000,
                    min_df=2,
                    max_df=0.8,
                    ngram_range=(1, 2),
                    lowercase=True,
                    strip_accents='unicode'
                )
            ),
            (
                'classifier',
                LogisticRegression(random_state=42, max_iter=2000, solver='liblinear')
            )
        ]
    )


def train_model(data_path: Path, model_path: Path, metadata_path: Path) -> None:
    df = load_data(str(data_path))
    X = df['cleaned']
    y = df['label_encoded']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metadata = {
        'model_name': 'Spam Classifier v1.0',
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'f1_score': float(f1_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'training_samples': int(len(df)),
        'classes': ['Ham', 'Spam']
    }

    joblib.dump(pipeline, model_path)
    joblib.dump(metadata, metadata_path)

    if MLFLOW_AVAILABLE:
        mlflow.set_experiment('spam_detection')
        with mlflow.start_run():
            mlflow.log_params({
                'max_features': 5000,
                'min_df': 2,
                'max_df': 0.8,
                'ngram_range': '(1,2)',
                'model_type': 'LogisticRegression',
                'solver': 'liblinear',
                'random_state': 42
            })
            mlflow.log_metrics({
                'accuracy': metadata['accuracy'],
                'f1_score': metadata['f1_score'],
                'precision': metadata['precision'],
                'recall': metadata['recall'],
                'training_samples': metadata['training_samples']
            })

            mlflow.sklearn.log_model(pipeline, artifact_path='pipeline')
            mlflow.log_artifact(str(model_path))
            mlflow.log_artifact(str(metadata_path))
        print("MLflow tracking completed")
    else:
        print("MLflow not available, skipping tracking")

    print('Model saved to:', model_path)
    print('Metadata saved to:', metadata_path)
    print('Accuracy:', metadata['accuracy'])
    print('F1 score:', metadata['f1_score'])


if __name__ == '__main__':
    parser = ArgumentParser(description='Train the spam detection model.')
    parser.add_argument('--data-path', type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument('--model-path', type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument('--metadata-path', type=Path, default=DEFAULT_METADATA_PATH)
    args = parser.parse_args()
    train_model(args.data_path, args.model_path, args.metadata_path)
