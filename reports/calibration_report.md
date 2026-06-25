# Calibration Comparison

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Model: **Random Forest**. Lower Brier / log-loss is better.

## Primary: training out-of-fold (241 patients, no test labels used)

| method | Brier | log-loss |
|---|---|---|
| none | 0.1222 | 0.3915 |
| sigmoid | 0.1210 | 0.3945 |
| isotonic | 0.1186 | 0.6488 |

**Lowest-Brier method on training OOF: `isotonic`.** The currently deployed
method is `isotonic`. Note the **Brier and log-loss disagree**: where isotonic
has the lowest Brier it can have a much worse log-loss, a classic sign of
isotonic over-fitting the small calibration set and producing over-confident
(near-0/1) probabilities. So no method is a clear winner here.

## Secondary: held-out test (61 patients) — for transparency only

| method | Brier | log-loss |
|---|---|---|
| none | 0.1427 | 0.4341 |
| sigmoid | 0.1401 | 0.4362 |
| isotonic | 0.1371 | 0.4247 |

## How to read this (honestly)
On a dataset this small the calibration methods are **close and unstable** — and
the Brier-vs-log-loss disagreement above shows isotonic's apparent Brier edge is
fragile. We therefore base any reading on the training-OOF comparison rather than
the test set, and do **not** claim a method is decisively best. The deployed
choice (`isotonic`) is defensible, but `sigmoid` (more stable on small data) or
even `none` would be equally reasonable; a different split could reorder these
closely-spaced numbers. Reliability curves:
`reports/figures/calibration_comparison.png`.
