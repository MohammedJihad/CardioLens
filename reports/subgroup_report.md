# Subgroup Analysis (exploratory)

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

> **Exploratory performance screen — not a calibrated fairness audit.** Metrics
> use **out-of-fold predictions across all
> 302 patients** (each row scored by a model
> that never trained on it) from the **base (uncalibrated) pipeline** — fast,
> leakage-free, and focused on discrimination. Subgroups are small and the 95% CIs
> are wide, so apparent differences are usually within noise and must **not** be
> read as fairness or clinical conclusions.

Subgroup screen uses the **uncalibrated base Random Forest pipeline** for out-of-fold
discrimination analysis; the deployed model remains calibrated separately.
Threshold-based recall/specificity (at threshold 0.5) are
**exploratory**, not a calibrated fairness audit.

| subgroup       |   n |   disease_rate |   roc_auc | roc_auc_ci     |   recall | recall_ci      |   specificity | specificity_ci   |
|:---------------|----:|---------------:|----------:|:---------------|---------:|:---------------|--------------:|:-----------------|
| Overall        | 302 |          0.457 |     0.903 | [0.869, 0.937] |    0.783 | [0.712, 0.851] |         0.866 | [0.809, 0.919]   |
| Female (sex=0) |  96 |          0.25  |     0.922 | [0.823, 0.988] |    0.75  | [0.538, 0.923] |         0.972 | [0.925, 1.0]     |
| Male (sex=1)   | 206 |          0.553 |     0.875 | [0.826, 0.915] |    0.789 | [0.719, 0.857] |         0.783 | [0.692, 0.862]   |
| Age < 55       | 143 |          0.308 |     0.934 | [0.879, 0.973] |    0.727 | [0.587, 0.842] |         0.939 | [0.89, 0.98]     |
| Age >= 55      | 159 |          0.591 |     0.856 | [0.792, 0.908] |    0.809 | [0.727, 0.888] |         0.754 | [0.646, 0.855]   |

## How to read this
- Compare each subgroup's CI to the overall CI; heavy overlap means no reliable
  difference. With ~100–200 patients per subgroup, most gaps here are not
  distinguishable from noise.
- A real fairness audit needs far more data per subgroup and pre-registered
  metrics. This section demonstrates the *method and the honesty*, not a verdict.
- → `reports/figures/subgroup_metrics.png`.
