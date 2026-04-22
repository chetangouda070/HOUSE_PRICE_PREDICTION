import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_single_prediction():
    house_data = {
        "area": 1500,
        "bedrooms": 3,
        "bathrooms": 2,
        "location": "Urban",
        "age": 5
    }
    response = client.post("/predict", json=house_data)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0

def test_batch_prediction():
    batch_data = {
        "houses": [
            {
                "area": 1200,
                "bedrooms": 3,
                "bathrooms": 2,
                "location": "Suburb",
                "age": 10
            },
            {
                "area": 2000,
                "bedrooms": 4,
                "bathrooms": 3,
                "location": "Luxury",
                "age": 2
            }
        ]
    }
    response = client.post("/predict/batch", json=batch_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 2

def test_invalid_area():
    house_data = {
        "area": 0,
        "bedrooms": 3,
        "bathrooms": 2,
        "location": "Urban",
        "age": 5
    }
    response = client.post("/predict", json=house_data)
    assert response.status_code == 422

def test_invalid_bedrooms():
    house_data = {
        "area": 1500,
        "bedrooms": 0,
        "bathrooms": 2,
        "location": "Urban",
        "age": 5
    }
    response = client.post("/predict", json=house_data)
    assert response.status_code == 422

def test_missing_field():
    house_data = {
        "area": 1500,
        "bedrooms": 3,
        "location": "Urban",
        "age": 5
    }
    response = client.post("/predict", json=house_data)
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

