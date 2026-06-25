"""FastAPI service — educational heart-disease *risk-score* API.

Endpoints:
  GET  /health      → liveness + whether a trained model is present
  GET  /model-info  → model name, features, default threshold, disclaimers
  POST /predict     → model score + band for one patient record (NOT a diagnosis)

Run locally:  uvicorn api.main:app --reload
Interactive docs:  http://127.0.0.1:8000/docs
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src import config                       # noqa: E402
from src.predict import load_model, predict_one  # noqa: E402
from src.patient_report import explain_prediction  # noqa: E402
from src._shared import get_selected_threshold   # noqa: E402

DISCLAIMER = (
    "Educational model score only — not a diagnosis, not medical advice, and not "
    "a medical device. No clinical validation."
)

app = FastAPI(
    title="Heart Disease Risk-Score API (educational)",
    description=("Returns a **model score** (estimated probability) for heart-disease "
                 "presence from clinical features. Educational/research use only — "
                 "**not** a diagnostic tool."),
    version="0.4.0",
)

# CORS — allow only the single front-end origin (no wildcard in committed code).
# Override in deployment with the FRONTEND_ORIGIN env var.
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class PatientFeatures(BaseModel):
    """One patient record. Values follow the Cleveland (recoded) encoding."""
    age: float = Field(..., ge=18, le=110, examples=[62])
    sex: int = Field(..., ge=0, le=1, description="1=male, 0=female", examples=[1])
    cp: int = Field(..., ge=0, le=3, description="chest pain type", examples=[0])
    trestbps: float = Field(..., ge=80, le=220, description="resting BP (mmHg)", examples=[140])
    chol: float = Field(..., ge=100, le=600, description="cholesterol (mg/dl)", examples=[268])
    fbs: int = Field(..., ge=0, le=1, description="fasting blood sugar > 120", examples=[0])
    restecg: int = Field(..., ge=0, le=2, examples=[0])
    thalach: float = Field(..., ge=60, le=220, description="max heart rate", examples=[130])
    exang: int = Field(..., ge=0, le=1, description="exercise-induced angina", examples=[1])
    oldpeak: float = Field(..., ge=0, le=7, description="ST depression", examples=[3.6])
    slope: int = Field(..., ge=0, le=2, examples=[0])
    ca: int = Field(..., ge=0, le=4, description="major vessels colored", examples=[2])
    thal: int = Field(..., ge=0, le=3, examples=[3])


class ExplanationFactor(BaseModel):
    """One within-model factor. `direction` is how this input moved the model
    score relative to a cohort baseline — 'up' or 'down'. Model-based and
    **not causal**: it never claims a feature caused heart disease."""
    feature: str
    direction: str
    magnitude: float


class PredictionResponse(BaseModel):
    model_score: float
    score_band: str
    default_threshold: float
    above_default_threshold: bool
    selected_threshold: float | None
    model: str
    disclaimer: str
    # Additive (v0.4.0): model-based explanation. Each factor "pushed the score
    # up/down" within this model; not causal, not medical advice.
    top_positive_factors: list[ExplanationFactor] = []
    top_negative_factors: list[ExplanationFactor] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": config.MODEL_PATH.exists()}


@app.get("/model-info")
def model_info() -> dict:
    if not config.MODEL_PATH.exists():
        return {"model_loaded": False, "message": "No trained model. Run `python -m src.train`."}
    bundle = load_model()
    return {
        "model_loaded": True,
        "model": bundle["best_name"],
        "features": config.FEATURES,
        "default_threshold": config.DEFAULT_THRESHOLD,
        "selected_threshold": get_selected_threshold(),
        "output": "model_score / model-estimated probability on research data",
        "disclaimer": DISCLAIMER,
    }


def _factors(items: list[dict], direction: str) -> list[ExplanationFactor]:
    """Map the existing explanation output to {feature, direction, magnitude}.
    Reuses src.patient_report.explain_prediction — no new explanation math."""
    return [
        ExplanationFactor(
            feature=x["label"],
            direction=direction,
            magnitude=round(abs(x["contribution"]), 4),
        )
        for x in items
    ]


@app.post("/predict", response_model=PredictionResponse)
def predict(features: PatientFeatures) -> PredictionResponse:
    record = features.model_dump()
    out = predict_one(record)
    # Additive: reuse the existing marginal local explanation for the same record.
    exp = explain_prediction(record)
    return PredictionResponse(
        model_score=out["model_score"],
        score_band=out["score_band"],
        default_threshold=config.DEFAULT_THRESHOLD,
        above_default_threshold=bool(out["model_score"] >= config.DEFAULT_THRESHOLD),
        selected_threshold=get_selected_threshold(),
        model=out["model"],
        disclaimer=DISCLAIMER,
        top_positive_factors=_factors(exp["top_positive_factors"], "up"),
        top_negative_factors=_factors(exp["top_negative_factors"], "down"),
    )
