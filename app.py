from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

try:
    model = joblib.load('house_price_model.pkl')
    metadata = joblib.load('house_price_model_metadata.pkl')
except FileNotFoundError as e:
    print(f"Error loading model files: {e}")
    exit(1)

app = FastAPI(
    title="House Price Prediction API",
    description="Predict house prices based on area, bedrooms, bathrooms, location, and age",
    version="1.0.0"
)

# Define request/response models
class HouseFeatures(BaseModel):
    area: int = Field(..., gt=0, le=10000, description="House area in square feet")
    bedrooms: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=10, description="Number of bathrooms")
    location: str = Field(..., description="Location type: Luxury, Urban, Suburb, or Rural")
    age: int = Field(..., ge=0, le=200, description="House age in years")

    class Config:
        schema_extra = {
            "example": {
                "area": 1500,
                "bedrooms": 3,
                "bathrooms": 2,
                "location": "Urban",
                "age": 5
            }
        }

class PredictionResponse(BaseModel):
    predicted_price: float
    price_per_sqft: float
    confidence_score: float
    model_version: str
    timestamp: str

class BatchPredictionRequest(BaseModel):
    houses: List[HouseFeatures] = Field(..., max_items=100)

class BatchPredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]
    summary: Dict[str, float]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_type: str
    training_date: str
    performance_metrics: Dict[str, float]

@app.get("/")
def root():
    return {
        "message": "House Price Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Model health and metrics",
            "POST /predict": "Single house price prediction",
            "POST /predict/batch": "Batch house price predictions"
        },
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_type=metadata['model_type'],
        training_date=metadata['training_date'],
        performance_metrics=metadata['performance_metrics']
    )

@app.post("/predict", response_model=PredictionResponse)
def predict_house_price(house: HouseFeatures):
    try:
        valid_locations = ['Luxury', 'Urban', 'Suburb', 'Rural']
        if house.location not in valid_locations:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid location. Must be one of: {valid_locations}"
            )

        house_data = pd.DataFrame([{
            'area': house.area,
            'bedrooms': house.bedrooms,
            'bathrooms': house.bathrooms,
            'location': house.location,
            'age': house.age
        }])

        predicted_price = model.predict(house_data)[0]
        price_per_sqft = predicted_price / house.area
        confidence_score = 0.85

        return PredictionResponse(
            predicted_price=round(predicted_price, 2),
            price_per_sqft=round(price_per_sqft, 2),
            confidence_score=confidence_score,
            model_version="1.0.0",
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_house_prices_batch(request: BatchPredictionRequest):
    try:
        predictions = []

        for house in request.houses:
            valid_locations = ['Luxury', 'Urban', 'Suburb', 'Rural']
            if house.location not in valid_locations:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid location for house. Must be one of: {valid_locations}"
                )

            house_data = pd.DataFrame([{
                'area': house.area,
                'bedrooms': house.bedrooms,
                'bathrooms': house.bathrooms,
                'location': house.location,
                'age': house.age
            }])

            predicted_price = model.predict(house_data)[0]
            price_per_sqft = predicted_price / house.area

            predictions.append({
                "input": house.dict(),
                "predicted_price": round(predicted_price, 2),
                "price_per_sqft": round(price_per_sqft, 2),
                "confidence_score": 0.85
            })

        prices = [p['predicted_price'] for p in predictions]
        summary = {
            "count": len(predictions),
            "mean_price": round(np.mean(prices), 2),
            "median_price": round(np.median(prices), 2),
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2)
        }

        return BatchPredictionResponse(
            predictions=predictions,
            summary=summary
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)