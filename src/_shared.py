"""Shared loaders for Phase 1 evaluation modules (keeps each script DRY).

Everything here reads the *already trained* artifact and the same held-out test
split used in `evaluate.py`, so every Phase 1 number is consistent with the
reported model and reproducible from a clean clone.
"""
from __future__ import annotations

import joblib

from . import config
from .data import load_processed
from .train import split


def load_test_predictions():
    """Return (model, best_name, X_test, y_test, y_proba, df) for the saved model."""
    if not config.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model at {config.MODEL_PATH}. Run `python -m src.train` first."
        )
    bundle = joblib.load(config.MODEL_PATH)
    model, best = bundle["model"], bundle["best_name"]
    df = load_processed()
    X_train, X_test, y_train, y_test = split(df)
    y_proba = model.predict_proba(X_test)[:, 1]
    return model, best, X_train, X_test, y_train, y_test, y_proba, df


def write_report(path, text: str) -> None:
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


EDU_DISCLAIMER = (
    "_Educational and research use only. Outputs are **model scores**, not "
    "diagnoses; this is not a medical device and has had no clinical validation._"
)


def get_selected_threshold():
    """Return the training-OOF-selected operating threshold if available, else None.

    Read from the threshold report's saved evaluation; never recomputed here.
    """
    import csv
    path = config.REPORTS_DIR / "threshold_test_evaluation.csv"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            row = next(csv.DictReader(f))
        return float(row["threshold"])
    except Exception:
        return None
