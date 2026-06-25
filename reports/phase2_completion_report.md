# Phase 2 — Completion Report: Explainability Done Right

_Educational and research use only. Outputs are **model scores** and **model
explanations**, not diagnoses. Explanations are model-based and **not causal**;
not medical advice; no clinical validation._

Phase 2 added honest global and local explainability. Phase 1 reports and metrics
are preserved unchanged.

## SHAP: implemented (not skipped)
SHAP **was implemented**. `shap.TreeExplainer` cannot run directly on the deployed
`CalibratedClassifierCV` (it wraps several cross-fitted RF pipelines plus a
preprocessing step and exposes no single tree model). We therefore run SHAP on the
**uncalibrated Random Forest** pipeline. SHAP on the uncalibrated Random
Forest is a useful proxy for feature-usage patterns, but it is not an exact
explanation of the calibrated ensemble's final probability. SHAP installs and runs cleanly (`shap 0.52`).

## Global explanation summary
Two independent global views agree:

| rank | permutation importance (deployed model) | SHAP mean\|value\| (uncalibrated RF) |
|---|---|---|
| 1 | `ca` (major vessels) | `thal` |
| 2 | `cp` (chest pain type) | `ca` |
| 3 | `thal` | `cp` |
| 4 | `oldpeak` | `oldpeak` |

`ca`, `cp`, `thal`, and `oldpeak` dominate in both — consistent with the clinical
literature. → `reports/feature_importance.csv`,
`reports/figures/permutation_importance.png`, `reports/figures/shap_summary.png`,
`reports/explainability_report.md`.

## Local explanation (per-patient)
`explain_prediction(record)` (in `src/patient_report.py`) returns, for one
patient: `model_score`, `threshold`, `score_band` (model-score language),
`top_positive_factors`, `top_negative_factors`, `disclaimer`. Local contributions
use a transparent **marginal** method on the **deployed** model: each feature is
set to a cohort baseline and the change in model score is measured (so the
explanation matches the actual score). These are one-at-a-time approximations
(they do not sum exactly to the score, unlike additive SHAP).

### Sample (a real borderline test patient, model score ≈ 0.50)
- **Band:** High model score; **threshold** 0.50.
- **Top factors increasing the score:** `thal`, `ca`, `oldpeak`, `age`.
- **Top factors decreasing the score:** `cp`, `chol`, `trestbps`.
→ `reports/sample_patient_report.md`.

## Tests
`pytest` — all passing (existing + new: local-explanation schema, patient-report
safety/language, explainability-report present and disclaims causality).

## What these explanations are and are not
- **Permutation importance** is global and reflects predictive usefulness, not
  causation.
- **SHAP** attributes the RF model's output to features (model-based, not causal).
- **Local marginal contributions** explain *this model's score* for *this patient*,
  approximately — not a clinical assessment.
- None of it is medical advice; the dataset is small, historical, and single-cohort.

## Remaining limitations
- SHAP is computed on the uncalibrated RF, not the exact calibrated estimator
  (documented; ordering is preserved by monotonic calibration).
- Local contributions are marginal (one-at-a-time), not additive Shapley values.
- Explanations inherit all the dataset's small-sample limitations.

## Status
**Phase 2 complete. Phase 3 (Streamlit upgrades, FastAPI, MLflow, Docker, CI,
external validation) was NOT started.**
