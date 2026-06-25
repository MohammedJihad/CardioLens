# External Validation (Phase 5)

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

The **deployed** calibrated model (Random Forest), trained only on Cleveland, is applied
unchanged to three independent UCI cohorts. Missing values are imputed by the
model's own pipeline using Cleveland statistics (i.e. true deployment behaviour).
Operating threshold = **0.2** (selected earlier on Cleveland training out-of-fold).

Internal Cleveland test ROC-AUC for reference: **0.892**.

| cohort        |   n |   disease_rate |   ca_missing_% |   thal_missing_% |   roc_auc | roc_auc_ci     |   pr_auc |   brier |   sensitivity@0.2 |   specificity@0.2 |
|:--------------|----:|---------------:|---------------:|-----------------:|----------:|:---------------|---------:|--------:|------------------:|------------------:|
| Hungarian     | 294 |          0.361 |             99 |               90 |     0.857 | [0.81, 0.902]  |    0.753 |   0.178 |             0.887 |             0.638 |
| VA Long Beach | 200 |          0.745 |             99 |               83 |     0.672 | [0.581, 0.754] |    0.83  |   0.339 |             0.866 |             0.314 |
| Switzerland   | 123 |          0.935 |             96 |               42 |     0.81  | [0.623, 0.962] |    0.981 |   0.337 |             0.974 |             0.375 |

## What this shows
- **Discrimination partially transfers, but calibration does not.** ROC-AUC falls
  from the internal 0.892 to **0.857 (Hungarian)**, **0.810 (Switzerland)**
  and **0.672 (VA)** — every cohort is lower, and VA drops the most. Yet Brier
  scores worsen sharply on all three (0.178–0.339 vs 0.137
  internally): probabilities calibrated on Cleveland do **not** match external base
  rates.
- The model keeps *some* ranking ability from the always-recorded features (age,
  cp, oldpeak, thalach, exang), so discrimination does not collapse to chance — but
  its two most important features, `ca` and `thal`, are **missing in 83–99%** of
  external rows and get imputed with Cleveland's mode, depriving the model of its
  top signal (see `figures/external_missingness.png`).
- **Base rates differ sharply** (Cleveland ~46% vs Hungarian ~36%, VA ~75%,
  Switzerland ~94%), which drives the miscalibration the Brier scores capture.
  Switzerland is an extreme, low-`n`, ~94%-disease cohort with cholesterol recorded
  as 0 (missing) — read it with great caution.

## Honest conclusion
External validation behaves exactly as good practice predicts: a single small,
historical, single-centre model **partly** preserves discrimination but loses
calibration on new populations and acquisition protocols. Deploying it elsewhere
would require, at minimum, **external recalibration or retraining** on
representative local data using features that are actually recorded there. This is
the expected and scientifically valuable outcome of external validation — a
limitation surfaced honestly, not a failure to hide.

→ `figures/external_auc_comparison.png`, `external_roc_curves.png`,
`external_missingness.png`.
