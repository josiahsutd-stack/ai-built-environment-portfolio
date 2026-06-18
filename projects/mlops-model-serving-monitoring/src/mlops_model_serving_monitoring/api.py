from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .pipeline import generate_churn_data, predict_churn, train_churn_model

app = FastAPI(title="MLOps Model Serving and Monitoring")
MODEL, METRICS = train_churn_model(generate_churn_data())


class ChurnRequest(BaseModel):
    tenure_months: float
    monthly_spend: float
    support_tickets: float
    usage_score: float


@app.get("/metrics")
def metrics() -> dict[str, object]:
    return METRICS


@app.post("/predict")
def predict(payload: ChurnRequest) -> dict[str, float]:
    return predict_churn(MODEL, payload.model_dump())
