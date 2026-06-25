# Phase 3 — Completion Report: Responsible AI & Documentation

_Educational and research use only. Outputs are **model scores** and **model
explanations**, not diagnoses; not a medical device; no clinical validation._

Phase 3 added company-grade documentation and an honest, exploratory fairness
view. Phases 0–2 reports and metrics are preserved. No model pipeline change was
needed; the calibrated Random Forest and all prior metrics are unchanged.

> Adopted the reviewer-refined Phase 2 base, which honestly softened the SHAP
> wording (SHAP on the uncalibrated RF is a *proxy* for feature usage, not an
> exact explanation of the calibrated ensemble) and the patient-report score
> label. Phase 3 builds on that.

## What was added
1. **`src/subgroup.py` + `reports/subgroup_report.md` / `subgroup_metrics.csv` /
   `figures/subgroup_metrics.png`** — exploratory subgroup performance by sex and
   age band, computed on **out-of-fold predictions across all 302 patients**
   (leakage-free; the 61-row test split is far too small to slice), each metric
   with a bootstrap 95% CI and labelled exploratory.
2. **`reports/data_card.md`** — focused data card: identity, size, features,
   target (incl. the inversion fix), missingness, known bias, provenance caveats,
   and why the dataset is not deployment-ready.
3. **`reports/clinical_reporting_checklist.md`** — TRIPOD+AI-inspired checklist of
   what was / was not done (no external or prospective validation; no deployment
   readiness), stated honestly.
4. **`reports/model_card.md` expanded** — subgroup summary, explicit
   *not-intended uses*, and a version history.

## Subgroup summary (exploratory — not a fairness verdict)
| subgroup | n | disease rate | OOF ROC-AUC | recall | specificity |
|---|---|---|---|---|---|
| Overall | 302 | 0.46 | 0.903 | 0.783 | 0.866 |
| Female | 96 | 0.25 | 0.922 | 0.750 | 0.972 |
| Male | 206 | 0.55 | 0.875 | 0.789 | 0.783 |
| Age < 55 | 143 | 0.31 | 0.934 | 0.727 | 0.939 |
| Age ≥ 55 | 159 | 0.59 | 0.856 | 0.809 | 0.754 |

Performance looks slightly higher for females and younger patients, but their
disease rates are much lower (base-rate effect) and subgroup CIs are wide — these
gaps are mostly within noise. A real fairness audit needs far more data per group.

## Tests
`pytest` — all passing (existing + new: subgroup schema, data card present,
clinical checklist present).

## Remaining limitations
- Subgroups remain small even pooled over all 302 rows → wide CIs; exploratory only.
- No external/prospective validation; no deployment or regulatory readiness.
- All small-dataset caveats from earlier phases still apply.

## Status
**Phase 3 complete. Later phases (Streamlit multipage app, FastAPI, MLflow,
Docker, CI, external validation) were NOT started.**
