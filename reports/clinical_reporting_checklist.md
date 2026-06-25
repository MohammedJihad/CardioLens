# Clinical-ML Reporting Checklist (TRIPOD+AI-inspired)

_Educational and research use only — not a clinical study. This checklist adapts
the spirit of clinical-prediction reporting guidance (e.g. TRIPOD+AI) to keep the
project honest about what was and was not done. It is **not** a claim of
compliance with any standard._

| # | Item | Status | Where |
|---|---|---|---|
| 1 | Problem & intended use stated (educational risk *screening*, not diagnosis) | ✅ | README, model_card |
| 2 | Data source, license, and provenance documented | ✅ | data_card, data_source_research |
| 3 | Target definition explicit (incl. label-inversion fix) | ✅ | data/README, data_card |
| 4 | Features defined | ✅ | dataset_description, data_card |
| 5 | Missing-data handling described | ✅ | preprocessing, data_card |
| 6 | Preprocessing inside CV (no leakage) | ✅ | preprocessing, train |
| 7 | Model selection method (stratified + nested CV) | ✅ | train, nested_cv |
| 8 | Discrimination reported (ROC-AUC, PR-AUC) | ✅ | evaluate, metrics.json |
| 9 | Sensitivity/specificity & confusion matrix reported | ✅ | evaluate, model_card |
| 10 | Calibration assessed (Brier, log-loss, reliability) | ✅ | calibration_report |
| 11 | Uncertainty quantified (bootstrap 95% CIs) | ✅ | uncertainty |
| 12 | Decision threshold selected WITHOUT test leakage | ✅ | thresholds (train-OOF) |
| 13 | Clinical utility framing (decision curve / net benefit) | ✅ (educational) | decision_curve |
| 14 | Explainability (global + local, non-causal) | ✅ | explain, patient_report |
| 15 | Error analysis | ✅ | error_analysis |
| 16 | Subgroup performance (exploratory) | ✅ | subgroup |
| 17 | Sample-size / data-sufficiency discussed | ✅ | learning_curve, limitations |
| 18 | Limitations & not-intended-uses stated | ✅ | model_card, data_card |
| 19 | Reproducible from a clean clone | ✅ | README, scripts, tests |
| 20 | **External validation** | ✅ (educational) | external_validation (Hungarian/VA/Switzerland) |
| 21 | **Prospective / clinical validation** | ❌ not done | out of scope |
| 22 | **Regulatory / deployment readiness** | ❌ no | explicitly disclaimed |

## Summary
The project meets the *reporting and rigour* items appropriate for an educational
clinical-ML demonstration: documented data, leakage-free evaluation, calibration,
uncertainty, threshold selection without test leakage, explainability, and honest
limitations. It now also includes an **educational external validation** (Phase 5)
on three independent UCI cohorts, which honestly shows the model does not transfer
without recalibration. It still does **not** claim prospective
validation, or any deployment/regulatory readiness.
