# Model Card — Heart Disease Risk Classifier

## Overview
A calibrated **Random Forest** classifier (selected from the default candidate set by
stratified cross-validation) that estimates the probability of heart-disease
presence from 13 routine clinical features. Built as a reproducible,
educational data-science project.

## Intended use
- **Intended:** learning, portfolio demonstration, exploring clinical-ML
  evaluation and explainability on a public dataset.
- **Out of scope:** diagnosis, screening, triage, or any real clinical or
  individual health decision. This is **not** a medical device.

## Data
UCI Cleveland Heart Disease — 302 records after de-duplication, 45.7% positive
(disease). Target corrected for a known label inversion (see `data/README.md`).
The dataset is small, single-centre, decades old, and not representative of any
current population.

## Model selection (stratified 5-fold CV on the training split)
| model | CV ROC-AUC | CV recall |
|---|---|---|
| Dummy (baseline) | 0.500 | 0.000 |
| Logistic Regression | 0.906 ± 0.040 | 0.800 |
| SVM (RBF) | 0.907 ± 0.042 | 0.818 |
| MLP | 0.859 ± 0.063 | 0.773 |
| **Random Forest** | **0.910 ± 0.038** | 0.809 |
| HistGradientBoosting _(opt-in)_ | 0.869 ± 0.040 | 0.782 |

The default candidate set is Dummy, Logistic Regression, SVM, MLP, and Random
Forest; **HistGradientBoosting is available as an optional opt-in model**
(`config.INCLUDE_HISTGB`, off by default for reliable training). Logistic Regression, SVM, and Random Forest are **statistically tied** (their
intervals overlap). Random Forest was chosen on the top mean AUC, but a simple,
interpretable Logistic Regression would be an equally defensible production
choice on data this size.

## Held-out test performance (61 patients, threshold = 0.5)
| metric | value |
|---|---|
| ROC-AUC | 0.892 |
| PR-AUC | 0.853 |
| Accuracy | 0.787 |
| Balanced accuracy | 0.781 |
| Precision | 0.800 |
| **Recall / sensitivity** | **0.714** |
| Specificity | 0.848 |
| F1 | 0.755 |
| Log loss (probabilities) | 0.425 |
| Brier score | 0.137 |

Confusion matrix: TP = 20, **FN = 8 (missed sick patients)**, TN = 28, FP = 5.

## Key limitations
- **Tiny test set (61 rows):** point metrics carry wide uncertainty; treat the
  CV ranges as more reliable than any single test number.
- **8 false negatives** at the default threshold — in a real screening setting
  you would lower the decision threshold to raise sensitivity, trading away
  specificity. The threshold here is not clinically tuned.
- **Dataset shift:** trained on one historical cohort. Retrospective external-cohort
  validation was performed on UCI Hungarian, VA Long Beach, and Switzerland; the
  model still has no prospective, contemporary, or clinical validation.
- Not assessed for fairness across subgroups beyond what the small sample allows.

## Explainability
**Global:** permutation importance (model-agnostic, deployed model) and SHAP
(TreeExplainer on the uncalibrated RF — TreeExplainer cannot run on the
`CalibratedClassifierCV` wrapper directly). Both rank number of major vessels
(`ca`), chest pain type (`cp`), and `thal` as the strongest drivers — consistent
with the dataset's predictive patterns and with the project's earlier model reports. **Local:** per-patient explanations via marginal
contributions on the deployed model (`src/patient_report.py`). All explanations
are model-based, approximate, and **not causal**; they are not medical advice.
See `reports/explainability_report.md` and `reports/figures/`
(`permutation_importance.png`, `shap_summary.png`).

## Phase 1 — evaluation depth (statistical honesty)

- **Confidence intervals (bootstrap, 2000):** ROC-AUC 0.892 [0.805, 0.961];
  sensitivity 0.714 [0.542, 0.879]; specificity 0.849 [0.710, 0.964]. Intervals
  are wide because the test set is small.
- **Nested CV:** ROC-AUC 0.913 ± 0.047 (unbiased); Logistic Regression selected
  in 4/5 outer folds — the interpretable model is competitive on this data.
- **Threshold:** default 0.5 is not clinical. A cost-sensitive threshold (FN
  weighted 5× FP) is selected on **training out-of-fold** data only (no test
  leakage) → **0.20**; on the held-out test it gives sensitivity 1.00,
  specificity 0.61.
- **Calibration:** compared on training OOF (primary). Isotonic had the lowest
  Brier (0.119) but a much worse log-loss (0.65 vs ~0.39), suggesting over-fit;
  methods are close and unstable, so no method is decisively best (deployed
  isotonic is defensible, sigmoid/none equally reasonable).
- **Decision curve:** positive net benefit vs treat-all / treat-none across
  ~0.05–0.60 (educational framing only).
- **Error analysis:** 8 false negatives — some borderline near 0.5 (0.43–0.48),
  others lower-confidence (0.23–0.30); descriptive only, too few for conclusions.
- **Learning curve:** validation AUC plateaus → more data helps only modestly;
  ~300 rows is the binding limit.

## Subgroup performance (exploratory, out-of-fold)
Computed on out-of-fold predictions across all 302 patients (not the tiny test
split), with wide CIs — **exploratory only, not a fairness verdict**:

| subgroup | n | disease rate | OOF ROC-AUC | recall | specificity |
|---|---|---|---|---|---|
| Overall | 302 | 0.46 | 0.903 | 0.783 | 0.866 |
| Female | 96 | 0.25 | 0.922 | 0.750 | 0.972 |
| Male | 206 | 0.55 | 0.875 | 0.789 | 0.783 |
| Age < 55 | 143 | 0.31 | 0.934 | 0.727 | 0.939 |
| Age ≥ 55 | 159 | 0.59 | 0.856 | 0.809 | 0.754 |

Differences are mostly within noise given subgroup sizes and base-rate gaps. See
`reports/subgroup_report.md`.

## External validation (Phase 5)
The deployed model, trained only on Cleveland, was applied unchanged to three
independent UCI cohorts (loaded from the original processed files, encodings
harmonised). Result — **discrimination partially transfers, calibration does not**:

| cohort | n | disease rate | ROC-AUC | Brier |
|---|---|---|---|---|
| Cleveland (internal test) | 61 | 0.46 | 0.892 | 0.137 |
| Hungarian | 294 | 0.36 | 0.857 | 0.178 |
| VA Long Beach | 200 | 0.75 | 0.672 | 0.339 |
| Switzerland | 123 | 0.94 | 0.810 | 0.337 |

ROC-AUC drops on every cohort (VA worst) and Brier worsens sharply everywhere,
because the model's top features `ca`/`thal` are missing in 83–99% of external
rows (imputed with Cleveland's mode) and the base rates differ widely. **Honest
conclusion: the model would need external recalibration/retraining before any use
elsewhere.** See `reports/external_validation_report.md`.

## Not intended uses
Not for diagnosis, screening of real patients, triage, clinical decisions, or any
individual health use. Not a medical device. Not prospectively or clinically
validated. The external validation here is retrospective and educational only.

## Version history
- **v0.4 (Phase 5):** external validation on UCI Hungarian/VA/Switzerland cohorts —
  discrimination partially transfers, calibration does not; documented honestly.
- **v0.3 (Phase 3):** data card, exploratory subgroup analysis, clinical-reporting
  checklist; model card expanded with version history and not-intended uses.
- **v0.2 (Phase 1–2):** leakage-free threshold selection, bootstrap CIs, nested CV,
  calibration comparison, decision curve, error analysis, learning curve;
  global + local explainability (permutation, SHAP, marginal local).
- **v0.1 (Phase 0):** reproducible pipeline, target-inversion fix, multi-model CV,
  calibrated Random Forest, core evaluation, data-source research & strategy.

## Ethical statement
This project is for **educational and research purposes only**. It is not a
diagnostic tool and must not replace professional medical advice. Reporting
follows the spirit of clinical-prediction guidance (e.g. TRIPOD+AI) by being
explicit about data provenance, evaluation, calibration, and limitations.
