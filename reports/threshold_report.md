# Threshold Analysis

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Model: **Random Forest** (calibrated). The 0.5 cut-off is only a default — not a clinical
decision threshold.

## Operating threshold — selected WITHOUT test labels
The threshold is chosen on **training out-of-fold predictions** (5-fold), by
minimising `cost = 5·FN + 1·FP` (a false negative
weighted 5× a false positive). The test set is **not** used for
selection, which avoids the optimistic bias of tuning a policy on test labels.

- **Selected threshold (from training OOF): 0.20**
- Selection sweep: `reports/threshold_selection_train_oof.csv`

### Held-out test performance AT the selected threshold (evaluated once)

| threshold | sensitivity | specificity | precision | F1 | FN | FP |
|---|---|---|---|---|---|---|
| 0.20 (selected) | 1.0 | 0.606 | 0.683 | 0.812 | 0 | 13 |
| 0.50 (default) | 0.714 | 0.848 | 0.8 | 0.755 | 8 | 5 |

## Held-out test sensitivity analysis (post-hoc, NOT used to choose the threshold)
The table below shows how metrics move with the threshold on the test set. It is
provided for transparency; the operating threshold above was **not** picked from
it.

|   threshold |   TP |   FP |   TN |   FN |   sensitivity_recall |   specificity |   precision |    f1 |   accuracy |   balanced_accuracy |   cost |
|------------:|-----:|-----:|-----:|-----:|---------------------:|--------------:|------------:|------:|-----------:|--------------------:|-------:|
|        0.2  |   28 |   13 |   20 |    0 |                1     |         0.606 |       0.683 | 0.812 |      0.787 |               0.803 |     13 |
|        0.25 |   27 |   11 |   22 |    1 |                0.964 |         0.667 |       0.711 | 0.818 |      0.803 |               0.815 |     16 |
|        0.3  |   25 |   10 |   23 |    3 |                0.893 |         0.697 |       0.714 | 0.794 |      0.787 |               0.795 |     25 |
|        0.35 |   23 |    8 |   25 |    5 |                0.821 |         0.758 |       0.742 | 0.78  |      0.787 |               0.79  |     33 |
|        0.4  |   23 |    7 |   26 |    5 |                0.821 |         0.788 |       0.767 | 0.793 |      0.803 |               0.805 |     32 |
|        0.45 |   21 |    7 |   26 |    7 |                0.75  |         0.788 |       0.75  | 0.75  |      0.77  |               0.769 |     42 |
|        0.5  |   20 |    5 |   28 |    8 |                0.714 |         0.848 |       0.8   | 0.755 |      0.787 |               0.781 |     45 |
|        0.55 |   18 |    5 |   28 |   10 |                0.643 |         0.848 |       0.783 | 0.706 |      0.754 |               0.746 |     55 |
|        0.6  |   18 |    2 |   31 |   10 |                0.643 |         0.939 |       0.9   | 0.75  |      0.803 |               0.791 |     52 |

Lowering the threshold raises sensitivity (catches more sick patients) at the
cost of specificity. The cost weights (5:1) are
illustrative, not clinically derived; a real deployment would set them with
clinicians.
