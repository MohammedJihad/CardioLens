# Bootstrap Confidence Intervals

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Model: **Random Forest**. Test set: **61 patients**.
Method: 2000 bootstrap resamples (with replacement) of the test
predictions; 95% percentile intervals at the default 0.5
threshold.

| metric | point | 95% CI |
|---|---|---|
| accuracy | 0.787 | [0.672, 0.885] |
| balanced_accuracy | 0.781 | [0.673, 0.880] |
| precision | 0.800 | [0.631, 0.952] |
| recall_sensitivity | 0.714 | [0.542, 0.879] |
| specificity | 0.849 | [0.710, 0.964] |
| f1 | 0.755 | [0.609, 0.870] |
| brier_score | 0.137 | [0.088, 0.192] |
| log_loss | 0.425 | [0.289, 0.594] |
| roc_auc | 0.892 | [0.805, 0.961] |
| pr_auc | 0.853 | [0.711, 0.961] |

**Reading these honestly:** the test set is small, so several intervals are wide
— the point estimates should not be over-trusted. ROC-AUC / PR-AUC intervals skip
the rare resamples that contain only one class. This is exactly why the project
also reports nested cross-validation (a less variance-prone generalisation
estimate) alongside this held-out evaluation.
