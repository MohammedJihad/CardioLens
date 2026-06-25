"""Single-record inference for the saved model.

Loads the calibrated pipeline and returns a disease probability + risk band for
one patient dictionary. Used by the tests and the Streamlit demo.
"""
from __future__ import annotations

import joblib
import pandas as pd

from . import config


def load_model():
    if not config.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model at {config.MODEL_PATH}. Run `python -m src.train` first."
        )
    return joblib.load(config.MODEL_PATH)


def risk_band(p: float) -> str:
    if p < 0.20:
        return "Low"
    if p < 0.50:
        return "Moderate"
    if p < 0.80:
        return "High"
    return "Very high"


def score_band(p: float) -> str:
    """Model-score band wording (never a diagnosis)."""
    return f"{risk_band(p)} model score"


def predict_one(record: dict) -> dict:
    """record: {feature: value} for all config.FEATURES. Returns model score + band.

    Output uses 'model score' wording. `disease_probability`/`prediction`/
    `risk_band` are kept for backward compatibility with existing tests.
    """
    bundle = load_model()
    model = bundle["model"]
    X = pd.DataFrame([{f: record.get(f) for f in config.FEATURES}])
    proba = round(float(model.predict_proba(X)[:, 1][0]), 4)
    thr = config.DEFAULT_THRESHOLD
    return {
        # model-score wording (preferred)
        "model_score": proba,
        "score_band": score_band(proba),
        "threshold": thr,
        "prediction_at_default_threshold": int(proba >= thr),
        "disclaimer": "Educational model score only — not a diagnosis or medical advice.",
        "model": bundle["best_name"],
        # --- deprecated backward-compatible keys (do not use in new code) ---
        "disease_probability": proba,   # deprecated alias of model_score
        "prediction": int(proba >= thr),          # deprecated
        "risk_band": risk_band(proba),            # deprecated alias of score_band
    }


# Preferred public output keys (safe, model-score wording).
PUBLIC_KEYS = ("model_score", "score_band", "threshold",
               "prediction_at_default_threshold", "disclaimer", "model")


def public_view(out: dict) -> dict:
    """Preferred output without the deprecated legacy keys."""
    return {k: out[k] for k in PUBLIC_KEYS if k in out}


# A realistic example record (a higher-risk profile) for quick manual testing.
EXAMPLE = {
    "age": 62, "sex": 1, "cp": 0, "trestbps": 140, "chol": 268, "fbs": 0,
    "restecg": 0, "thalach": 130, "exang": 1, "oldpeak": 3.6, "slope": 0,
    "ca": 2, "thal": 3,
}

if __name__ == "__main__":
    import json
    # show only the preferred, safe public keys (legacy keys stay in the dict for
    # backward compatibility but are intentionally not surfaced here).
    try:
        print(json.dumps(public_view(predict_one(EXAMPLE)), indent=2))
    except BrokenPipeError:  # output piped into head/less, etc.
        pass
