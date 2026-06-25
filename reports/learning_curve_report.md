# Learning Curve

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._

Model: **Random Forest**, 5-fold CV ROC-AUC vs training-set size.

| train size | training AUC | validation AUC |
|---|---|---|
| 48 | 1.000 | 0.892 |
| 86 | 1.000 | 0.910 |
| 125 | 1.000 | 0.914 |
| 163 | 1.000 | 0.922 |
| 202 | 1.000 | 0.911 |
| 241 | 1.000 | 0.911 |

At the largest size the validation curve is **roughly flat**
(last-step change -0.000) with a train–validation gap of 0.089.

**Interpretation:** returns from more data look modest (validation score has largely plateaued); the train–validation gap points more to model variance. Either way, the dataset's small size (~300 rows) is
the binding constraint — the strongest realistic improvement is *more / external
data*, which is exactly why external validation is planned as a later phase.
