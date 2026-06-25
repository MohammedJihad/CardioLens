# Nested Cross-Validation

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Outer 5-fold (performance) × inner 5-fold (model + hyperparameter selection over
Logistic Regression, Random Forest, and SVM). Preprocessing is inside the
pipeline and re-fit per fold — no leakage.

## Per-fold results

|   outer_fold | selected_model         |   roc_auc |   recall |    f1 |   accuracy |   balanced_accuracy |
|-------------:|:-----------------------|----------:|---------:|------:|-----------:|--------------------:|
|            1 | LogisticRegression     |     0.971 |    0.964 | 0.931 |      0.934 |               0.937 |
|            2 | RandomForestClassifier |     0.911 |    0.857 | 0.842 |      0.852 |               0.853 |
|            3 | LogisticRegression     |     0.827 |    0.556 | 0.682 |      0.767 |               0.747 |
|            4 | LogisticRegression     |     0.927 |    0.852 | 0.852 |      0.867 |               0.865 |
|            5 | LogisticRegression     |     0.931 |    0.714 | 0.816 |      0.85  |               0.842 |

## Generalisation estimate (mean ± std across outer folds)

| metric | mean ± std |
|---|---|
| roc_auc | 0.913 ± 0.047 |
| recall | 0.789 ± 0.141 |
| f1 | 0.825 ± 0.081 |
| accuracy | 0.854 ± 0.053 |
| balanced_accuracy | 0.849 ± 0.061 |

**Model selected by the inner loop:** LogisticRegression×4, RandomForestClassifier×1.

This nested estimate is the project's most trustworthy single number for "how
well does this approach generalise on this data", and it is consistent with the
held-out test ROC-AUC. The selected family can vary across folds — expected when
several models are statistically tied on a small dataset.
