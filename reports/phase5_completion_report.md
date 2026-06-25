# Phase 5 — Completion Report: External Validation

_Educational and research use only. Outputs are **model scores**, not diagnoses;
not a medical device; no clinical validation._

Phase 5 adds the scientific "crown": the **deployed** Cleveland model is applied,
**unchanged**, to three independent UCI cohorts. No retraining; Phase 0–4 model and
metrics are untouched.

## What was added
- **`src/external_validation.py`** — loads the original UCI processed files for
  Hungarian / VA Long Beach / Switzerland (`uci_original` encoding), harmonises
  them to the training schema via `src/schema.py`, derives the binary target via
  `dataset_registry` (`num > 0`), treats physiologically-impossible `chol`/`trestbps`
  zeros as missing, and scores them with the deployed calibrated model (missing
  values imputed by the pipeline using **Cleveland** statistics — true deployment
  behaviour). Per-cohort ROC-AUC (with bootstrap CI), PR-AUC, Brier, and
  sensitivity/specificity at the screening threshold.
- **`data/external/`** — the three cohorts cached for reproducibility, with a
  README documenting source, license (CC BY 4.0), and caveats.
- **Reports/figures** — `external_validation_report.md`,
  `external_validation_metrics.csv`, and `figures/external_auc_comparison.png`,
  `external_roc_curves.png`, `external_missingness.png`.
- Docs updated: model card (external-validation section + v0.4), clinical-reporting
  checklist (item 20 now ✅ educational), README, Makefile (`make external`).
- Tests added (cohorts load with both classes; report is honest; CSV schema).

## Result (real numbers)
| cohort | n | disease rate | ca miss | thal miss | ROC-AUC | Brier |
|---|---|---|---|---|---|---|
| Cleveland (internal test) | 61 | 0.46 | 0% | 0% | **0.892** | 0.137 |
| Hungarian | 294 | 0.36 | 99% | 90% | 0.857 | 0.178 |
| VA Long Beach | 200 | 0.75 | 99% | 83% | **0.672** | 0.339 |
| Switzerland | 123 | 0.94 | 96% | 42% | 0.810 | 0.337 |

**Discrimination partially transfers, calibration does not.** ROC-AUC drops on
every cohort (VA worst); Brier worsens sharply everywhere. Cause is structural: the
model's top features `ca`/`thal` are missing in 83–99% of external rows (imputed
with Cleveland's mode), and base rates differ widely (46% vs 36/75/94%). Switzerland
is extreme (low n, ~94% disease, cholesterol = 0) — read with caution.

## Honest conclusion
External validation behaves exactly as good practice predicts. A single small,
historical, single-centre model does not transfer cleanly; it would need **external
recalibration or retraining** on representative local data with features that are
actually recorded there. This limitation is surfaced honestly — it is the value of
external validation, not a failure.

## Verification
- `python -m src.external_validation` → runs, exits cleanly, writes report/CSV/figures.
- `pytest` → **28 passed, 1 skipped** by default (the subprocess hang-guard is
  opt-in; enable with `RUN_SUBPROCESS_GUARD=1`). The count is reported as-is rather
  than as a fixed universal number.
- Model and all Phase 0–4 metrics unchanged (no retraining).

## Documentation/structure cleanup (post-review, no metric change)
- **Loader split:** data loading/parsing/harmonisation moved to **`src/external_data.py`**
  (sources, columns, cache read, target mapping, schema harmonisation, missing-value
  handling, feature-availability table); `src/external_validation.py` now imports it
  and only does scoring/metrics/figures/report. External metrics are byte-for-byte
  unchanged.
- **New report `reports/external_feature_availability.md`** — per-cohort % missing
  for ca/thal/slope/chol/fbs/restecg, why missing ca/thal matters, why it limits
  direct deployment, and an explicit note that this is not a clinical validation.
- **Doc contradictions fixed:** README and model card no longer say "no external
  validation"; they now state that retrospective educational external-cohort
  validation was performed but no prospective/contemporary/clinical validation was.
- **Test guard made opt-in:** the subgroup subprocess hang-guard is skipped by
  default so `pytest` is deterministic across environments.

## Confirmations
- The deployed model was **not** changed or retrained.
- **NOT started:** MLflow, Docker, CI (engineering layer remains optional/future).

## Status
**Phase 5 complete.** The project now spans a reproducible pipeline, deep
evaluation, explainability, responsible-AI documentation, a product surface, and
honest external validation.
