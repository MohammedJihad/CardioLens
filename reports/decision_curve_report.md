# Decision Curve Analysis

_Educational and research use only. Outputs are **model scores**, not diagnoses; this is not a medical device and has had no clinical validation._ _This is educational clinical-ML framing only — **not** clinical
validation._

Model: **Random Forest**, test set (61 patients). Net benefit compares acting
on the model against "treat all" and "treat none" across threshold probabilities.

| threshold prob. | model | treat-all | treat-none |
|---|---|---|---|
| 0.05 | 0.439 | 0.431 | 0.000 |
| 0.10 | 0.421 | 0.399 | 0.000 |
| 0.15 | 0.407 | 0.364 | 0.000 |
| 0.20 | 0.406 | 0.324 | 0.000 |
| 0.25 | 0.383 | 0.279 | 0.000 |
| 0.30 | 0.340 | 0.227 | 0.000 |
| 0.35 | 0.306 | 0.168 | 0.000 |
| 0.40 | 0.301 | 0.098 | 0.000 |
| 0.45 | 0.250 | 0.016 | 0.000 |
| 0.50 | 0.246 | -0.082 | 0.000 |
| 0.55 | 0.195 | -0.202 | 0.000 |
| 0.60 | 0.246 | -0.352 | 0.000 |

**Reading it:** the model offers the highest net benefit over roughly
**0.05–0.60** threshold probabilities. Where its curve sits above both reference
lines, using the model to decide is preferable to treating everyone or no one —
within this small test set and with all the usual caveats. This is a teaching
demonstration of net-benefit reasoning, not evidence of clinical usefulness.
