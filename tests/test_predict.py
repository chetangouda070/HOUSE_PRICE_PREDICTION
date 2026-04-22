from pathlib import Path

import joblib
from fastapi.testclient import TestClient

from app.app import app

MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'model.pkl'
METADATA_PATH = Path(__file__).resolve().parents[1] / 'models' / 'model_metadata.pkl'


def test_model_artifact_exists():
    assert MODEL_PATH.exists()
    assert METADATA_PATH.exists()


def test_health_endpoint():
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'healthy'
    assert payload['model_loaded'] is True
    assert 'accuracy' in payload


def test_predict_single_message():
    client = TestClient(app)
    response = client.post('/predict', json={'message': 'Congratulations, you have won a free prize! Click now.'})
    assert response.status_code == 200
    payload = response.json()
    assert payload['prediction'] in {'HAM', 'SPAM'}
    assert isinstance(payload['confidence'], float)
    assert 'probabilities' in payload


def test_predict_batch_messages():
    client = TestClient(app)
    messages = [
        'Free coupon waiting for you.',
        'Hi, are we still on for the meeting tomorrow?'
    ]
    response = client.post('/predict/batch', json={'messages': messages})
    assert response.status_code == 200
    payload = response.json()
    assert payload['total_messages'] == 2
    assert len(payload['results']) == 2
    assert payload['summary']['spam_count'] + payload['summary']['ham_count'] == 2
