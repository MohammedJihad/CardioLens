# Error Analysis

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Model: **Random Forest**, threshold 0.5. Test set:
**61 patients** — 8 false negatives (missed sick),
5 false positives (false alarms), 48 correct.

> **Caution:** with so few errors, these are *descriptive observations on a tiny
> sample*, not reliable patterns. They are not medical advice.

## False negatives (missed sick) vs cohort
Model scores of the missed patients: [0.23, 0.28, 0.29, 0.3, 0.3, 0.43, 0.43, 0.48].
**Some false negatives are borderline near 0.5 ([0.43, 0.43, 0.48]),
while others are lower-confidence misses ([0.23, 0.28, 0.29, 0.3, 0.3]).**
Lowering the threshold (see the threshold report) would recover the borderline
ones, but not necessarily the lower-confidence misses.

| feature | cohort mean | group mean |
|---|---|---|
| age | 54.0 | 57.5 |
| thalach | 148.2 | 149.1 |
| oldpeak | 1.0 | 1.1 |
| ca | 1.1 | 1.2 |
| cp | 1.1 | 1.1 |
| thal | 2.2 | 2.1 |
| exang | 0.3 | 0.0 |
| trestbps | 133.0 | 138.8 |
| chol | 237.1 | 223.5 |

## False positives (false alarms) vs cohort

| feature | cohort mean | group mean |
|---|---|---|
| age | 54.0 | 62.8 |
| thalach | 148.2 | 144.0 |
| oldpeak | 1.0 | 1.0 |
| ca | 1.1 | 1.6 |
| cp | 1.1 | 1.2 |
| thal | 2.2 | 2.4 |
| exang | 0.3 | 0.0 |
| trestbps | 133.0 | 142.0 |
| chol | 237.1 | 229.4 |

## Takeaways (tentative)
- The misses split between near-boundary cases and lower-confidence ones; a
  cost-sensitive lower threshold helps mainly with the former.
- Any feature direction noted above is a hypothesis to revisit with more data,
  not a finding. The sample is too small to conclude anything clinical.
