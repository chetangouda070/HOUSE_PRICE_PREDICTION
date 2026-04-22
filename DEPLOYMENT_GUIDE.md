# House Price Prediction - Deployment Guide

## Table of Contents

1. Local Development Setup
2. Docker Deployment
3. Testing
4. Production Deployment
5. API Documentation
6. Troubleshooting

---

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or conda
- Docker & Docker Compose (optional)
- Git

### Step 1: Clone and Setup

```bash
git clone <repository-url>
cd ml2_housing

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Step 2: Verify Model Files

Ensure these files exist:
- house_price_model.pkl
- house_price_model_metadata.pkl
- housing.csv (optional)

If missing, run:
```bash
python house_price_prediction.py
```

### Step 3: Start API Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Access the API:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Step 4: Test the API

```bash
python test_api.py

# Or comprehensive tests
pytest test_house_price_api.py -v
```

---

## Docker Deployment

### Step 1: Build Docker Image

```bash
docker build -t house-price-api .
docker images | grep house-price-api
```

### Step 2: Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

### Step 3: Verify Container

```bash
docker ps
curl http://localhost:8000/health
```

---

## Testing

### Unit Tests

```bash
pytest test_house_price_api.py -v

# With coverage
pytest test_house_price_api.py --cov=app
```

### Manual API Testing

```bash
# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "location": "Urban",
    "age": 5
  }'

# Health check
curl http://localhost:8000/health
```

---

## Production Deployment

### AWS EC2

```bash
ssh -i your-key.pem ubuntu@your-instance-ip

sudo apt-get update
sudo apt-get install docker.io docker-compose

git clone <repository-url>
cd ml2_housing
sudo docker compose up -d
```

### Heroku

```bash
heroku login
heroku create house-price-prediction
git push heroku main
heroku logs --tail
```

### Google Cloud Run

```bash
gcloud auth login
gcloud run deploy house-price-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## API Documentation

### Single Prediction

POST /predict

Request:
```json
{
  "area": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "Urban",
  "age": 5
}
```

Response:
```json
{
  "predicted_price": 275700.50,
  "price_per_sqft": 184.47
}
```

### Batch Prediction

POST /predict/batch

Request:
```json
{
  "houses": [
    {"area": 1200, "bedrooms": 3, "bathrooms": 2, "location": "Suburb", "age": 10},
    {"area": 2000, "bedrooms": 4, "bathrooms": 3, "location": "Luxury", "age": 2}
  ]
}
```

Response:
```json
{
  "predictions": [...],
  "summary": {
    "count": 2,
    "mean_price": 314600.00,
    "min_price": 219300.00,
    "max_price": 409900.00
  }
}
```

### Health Check

GET /health

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "Random Forest Regressor"
}
```

### Input Validation

- area: 1-10000
- bedrooms: 1-10
- bathrooms: 1-10
- location: Urban, Suburb, Luxury, Rural
- age: 0-200

---

## Troubleshooting

### Model files not found

```bash
ls -la house_price_model.pkl
python house_price_prediction.py
```

### Port 8000 already in use

```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --port 8001
```

### Docker build fails

```bash
docker system prune -a
docker build --progress=plain -t house-price-api .
```

### API timeout

```bash
# In docker-compose.yml
healthcheck:
  timeout: 30s

# Or with gunicorn
gunicorn app:app --workers 4 --timeout 120
```

---

## Monitoring

### View Docker Logs

```bash
docker compose logs -f house-price-api
docker compose logs --tail 100
```

### Set Log Level

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

