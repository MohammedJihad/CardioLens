# External Feature Availability (Phase 5)

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

How much of each key feature is actually **recorded** in the external UCI cohorts,
before any imputation. Percentages are share **missing** (`?`, or `chol`/`trestbps`
recorded as 0). This is the structural reason external validation degrades.

| cohort        |   n |   disease_rate |   ca_missing_% |   thal_missing_% |   slope_missing_% |   chol_missing_% |   fbs_missing_% |   restecg_missing_% |
|:--------------|----:|---------------:|---------------:|-----------------:|------------------:|-----------------:|----------------:|--------------------:|
| Hungarian     | 294 |          0.361 |             99 |               90 |                65 |                8 |               3 |                   0 |
| VA Long Beach | 200 |          0.745 |             99 |               83 |                51 |               28 |               4 |                   0 |
| Switzerland   | 123 |          0.935 |             96 |               42 |                14 |              100 |              61 |                   1 |

## Why this matters
- **`ca` and `thal` are the model's two most important features** (see
  `reports/explainability_report.md`), yet they are missing in **83–99%** of
  external rows. When the deployed pipeline imputes them with Cleveland's mode, the
  model is effectively stripped of its strongest signal on these cohorts.
- `slope` is also largely missing (51–65% in Hungarian/VA), and Switzerland records
  `chol` as 0 throughout (treated as missing).
- Because the missing values are filled with **Cleveland** statistics, the external
  inputs are pulled toward Cleveland's distribution regardless of the patient — a
  direct driver of the miscalibration seen in `external_validation_report.md`.

## What it limits
This is why the model **cannot be deployed directly** on these populations: the
information it relies on is not collected there. Honest use elsewhere would require
retraining/recalibrating on features that the target site actually records.

**This is a retrospective, educational analysis — not a clinical validation.**
