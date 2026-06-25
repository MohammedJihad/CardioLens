# Explainability Report

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._ _Explanations describe **how the model uses features**; they are
**not causal** and **not medical advice**._

Model: **Random Forest** (calibrated).

## Global — permutation importance (model-agnostic, deployed model)
How much held-out ROC-AUC drops when each raw feature is randomly shuffled.

| feature | importance | std |
|---|---|---|
| Major vessels colored (0-4) | 0.076 | 0.021 |
| Chest pain type | 0.041 | 0.022 |
| Thalassemia result | 0.014 | 0.023 |
| ST depression (oldpeak) | 0.013 | 0.011 |
| Exercise-induced angina (1/0) | 0.013 | 0.010 |
| Sex (1=male, 0=female) | 0.012 | 0.010 |
| Max heart rate achieved | 0.008 | 0.010 |
| Age (years) | 0.004 | 0.008 |

→ `reports/figures/permutation_importance.png`, `reports/feature_importance.csv`.

## Global — SHAP
SHAP TreeExplainer on the uncalibrated RF. Top mean|SHAP|: cat__thal_2 (0.082), cat__ca_0 (0.071), cat__cp_0 (0.063), cat__thal_3 (0.057), num__oldpeak (0.052), num__thalach (0.042).

→ `reports/figures/shap_summary.png`.

**Why SHAP runs on the uncalibrated RF:** `shap.TreeExplainer` needs a single
tree model. The deployed estimator is a `CalibratedClassifierCV` wrapping several
cross-fitted RF pipelines, which TreeExplainer cannot read directly. SHAP on the uncalibrated Random Forest is a useful proxy for
feature-usage patterns, but it is not an exact explanation of the calibrated
ensemble's final probability.

## Local explanations
Per-patient explanations are produced by `src/patient_report.py` using a
marginal-contribution method on the **deployed** model (so they match the score a
user sees). See that module and `reports/sample_patient_report.md`.

## What these are and are not
- Global permutation importance reflects predictive usefulness, **not causation**.
- SHAP attributes the model's output to features for the RF model only.
- None of this is clinical evidence or advice; the dataset is small and historical.
