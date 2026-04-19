from pathlib import Path
import logging
from typing import Any, Dict

import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.pkl"

app = FastAPI(
    title="Spam Detection API",
    description="A machine learning API for detecting spam messages using NLP",
    version="1.0.0"
)

try:
    model = joblib.load(MODEL_PATH)
    metadata = joblib.load(METADATA_PATH)
    logger.info("Model and metadata loaded successfully")
except Exception as exc:
    logger.error(f"Failed to load model or metadata: {exc}")
    raise

class MessageRequest(BaseModel):
    message: str

class BatchRequest(BaseModel):
    messages: list[str]

class PredictionResponse(BaseModel):
    message: str
    prediction: str
    label: int
    confidence: float
    probabilities: Dict[str, float]
    model_info: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    accuracy: float
    f1_score: float

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Spam Detection API is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /predict": "Predict if message is spam",
            "POST /predict/batch": "Batch prediction for multiple messages"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_name=metadata.get("model_name", "spam-classifier"),
        accuracy=round(metadata.get("accuracy", 0.0), 4),
        f1_score=round(metadata.get("f1_score", 0.0), 4)
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_spam(request: MessageRequest):
    try:
        prediction = model.predict([request.message])[0]
        probabilities = model.predict_proba([request.message])[0]
        label_text = "SPAM" if prediction == 1 else "HAM"
        confidence = float(probabilities[prediction])

        return PredictionResponse(
            message=request.message,
            prediction=label_text,
            label=int(prediction),
            confidence=round(confidence, 4),
            probabilities={
                "ham": round(float(probabilities[0]), 4),
                "spam": round(float(probabilities[1]), 4)
            },
            model_info={
                "name": metadata.get("model_name", "spam-classifier"),
                "accuracy": round(metadata.get("accuracy", 0.0), 4),
                "f1_score": round(metadata.get("f1_score", 0.0), 4)
            }
        )
    except Exception as exc:
        logger.error(f"Prediction error: {exc}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")

@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(request: BatchRequest):
    try:
        messages = request.messages
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        if len(messages) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 messages per batch")

        predictions = model.predict(messages)
        probabilities = model.predict_proba(messages)

        results = []
        for idx, (message, prediction, probs) in enumerate(zip(messages, predictions, probabilities), start=1):
            results.append({
                "id": idx,
                "message": message,
                "prediction": "SPAM" if prediction == 1 else "HAM",
                "label": int(prediction),
                "confidence": round(float(probs[prediction]), 4),
                "probabilities": {
                    "ham": round(float(probs[0]), 4),
                    "spam": round(float(probs[1]), 4)
                }
            })

        return {
            "total_messages": len(results),
            "results": results,
            "summary": {
                "spam_count": sum(1 for item in results if item["prediction"] == "SPAM"),
                "ham_count": sum(1 for item in results if item["prediction"] == "HAM")
            }
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Batch prediction error: {exc}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(exc)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
