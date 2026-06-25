"""Per-patient (local) explanation and a structured patient report.

`explain_prediction(record)` returns a model score, the band ("model score"
language, never a diagnosis), and the features that most push the score up/down
for *this* patient. Local contributions use a transparent **marginal** method on
the DEPLOYED calibrated model: for each feature, we set it to a cohort baseline
(median for numeric, mode for categorical) and measure how the model score
changes. A feature whose real value raises the score above the baseline is a
"factor increasing the score".

This is model-based and **not causal**, and the contributions are a one-at-a-time
approximation (they do not sum exactly to the score, unlike additive SHAP).
Outputs: reports/sample_patient_report.md.
"""
from __future__ import annotations

import pandas as pd

from . import config
from .data import load_processed
from .predict import EXAMPLE, load_model, risk_band

DISCLAIMER = (
    "Educational model explanation only — this is a **model score and model "
    "explanation**, not a diagnosis or medical advice. Explanations are "
    "model-based, one-at-a-time approximations and are **not causal**."
)


def _cohort_baseline(df: pd.DataFrame) -> dict:
    base = {c: float(df[c].median()) for c in config.NUMERIC_FEATURES}
    base.update({c: df[c].mode().iloc[0] for c in config.CATEGORICAL_FEATURES})
    return base


def _score(model, record: dict) -> float:
    X = pd.DataFrame([{f: record.get(f) for f in config.FEATURES}])
    return float(model.predict_proba(X)[:, 1][0])


def score_band(p: float) -> str:
    return f"{risk_band(p)} model score"


def explain_prediction(input_record: dict, top_k: int = 4) -> dict:
    """Local explanation for one patient record (see module docstring)."""
    bundle = load_model()
    model = bundle["model"]
    df = load_processed()
    base = _cohort_baseline(df)

    score = _score(model, input_record)
    contribs = {}
    for f in config.FEATURES:
        perturbed = dict(input_record)
        perturbed[f] = base[f]
        # score(actual) - score(feature -> baseline): + => feature pushes score up
        contribs[f] = score - _score(model, perturbed)

    def fmt(items):
        return [{"feature": f,
                 "label": config.FEATURE_LABELS.get(f, f),
                 "value": input_record.get(f),
                 "cohort_baseline": round(base[f], 2),
                 "contribution": round(c, 4)} for f, c in items]

    pos = sorted(((f, c) for f, c in contribs.items() if c > 0), key=lambda x: -x[1])[:top_k]
    neg = sorted(((f, c) for f, c in contribs.items() if c < 0), key=lambda x: x[1])[:top_k]
    thr = config.DEFAULT_THRESHOLD
    return {
        "model_score": round(score, 4),
        "threshold": thr,
        "prediction_at_threshold": int(score >= thr),
        "score_band": score_band(score),
        "top_positive_factors": fmt(pos),
        "top_negative_factors": fmt(neg),
        "disclaimer": DISCLAIMER,
    }


def _factor_rows(factors):
    if not factors:
        return "_none_"
    return "\n".join(
        f"| {x['label']} | {x['value']} | {x['cohort_baseline']} | {x['contribution']:+.3f} |"
        for x in factors)


def build_report(record: dict) -> str:
    exp = explain_prediction(record)
    df = load_processed()
    base = _cohort_baseline(df)

    inputs = "\n".join(
        f"| {config.FEATURE_LABELS.get(f, f)} | {record.get(f)} | {round(base[f], 2)} |"
        for f in config.FEATURES)

    return f"""# Sample Patient Model-Score Report

_{DISCLAIMER}_

## Model score
- **Model score / model-estimated probability:** {exp['model_score']:.0%}
- **Band:** {exp['score_band']}
- **Threshold used:** {exp['threshold']} → prediction at threshold:
  {"positive (above threshold)" if exp['prediction_at_threshold'] else "negative (below threshold)"}

## Inputs vs cohort baseline
| feature | this patient | cohort baseline |
|---|---|---|
{inputs}

## Top factors increasing the model score
| factor | value | baseline | contribution |
|---|---|---|---|
{_factor_rows(exp['top_positive_factors'])}

## Top factors decreasing the model score
| factor | value | baseline | contribution |
|---|---|---|---|
{_factor_rows(exp['top_negative_factors'])}

## Notes
Contributions are one-at-a-time marginal effects on the **deployed model's**
score relative to a cohort baseline; they are model-based, approximate, and
**not causal**. This report is an educational explanation of a model score, not a
clinical assessment.
"""


def _borderline_record() -> dict:
    """Pick a real patient whose model score is near 0.5 — the most informative
    case for a local explanation (saturated 0/1 scores yield flat contributions)."""
    from .train import split
    bundle = load_model()
    model = bundle["model"]
    df = load_processed()
    _, X_test, _, _ = split(df)
    proba = model.predict_proba(X_test)[:, 1]
    idx = int(abs(proba - 0.5).argmin())
    row = X_test.iloc[idx]
    return {f: (float(row[f]) if f in config.NUMERIC_FEATURES else int(row[f]))
            for f in config.FEATURES}


def main() -> None:
    record = _borderline_record()
    md = build_report(record)
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (config.REPORTS_DIR / "sample_patient_report.md").write_text(md)
    exp = explain_prediction(record)
    print(f"Model score: {exp['model_score']:.3f}  band: {exp['score_band']}")
    print("Top +:", [x["feature"] for x in exp["top_positive_factors"]])
    print("Top -:", [x["feature"] for x in exp["top_negative_factors"]])
    print(f"Saved -> {config.REPORTS_DIR / 'sample_patient_report.md'}")


if __name__ == "__main__":
    main()
