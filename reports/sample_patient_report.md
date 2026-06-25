# Sample Patient Model-Score Report

_Educational model explanation only — this is a **model score and model explanation**, not a diagnosis or medical advice. Explanations are model-based, one-at-a-time approximations and are **not causal**._

## Model score
- **Model score / model-estimated probability:** 50%
- **Band:** High model score
- **Threshold used:** 0.5 → prediction at threshold:
  positive (above threshold)

## Inputs vs cohort baseline
| feature | this patient | cohort baseline |
|---|---|---|
| Age (years) | 58.0 | 55.5 |
| Resting blood pressure (mmHg) | 132.0 | 130.0 |
| Serum cholesterol (mg/dl) | 224.0 | 240.5 |
| Max heart rate achieved | 173.0 | 152.5 |
| ST depression (oldpeak) | 3.2 | 0.8 |
| Sex (1=male, 0=female) | 1 | 1 |
| Chest pain type | 2 | 0 |
| Fasting blood sugar > 120 (1/0) | 0 | 0 |
| Resting ECG result | 0 | 1 |
| Exercise-induced angina (1/0) | 0 | 0 |
| Slope of ST segment | 2 | 2 |
| Major vessels colored (0-4) | 2 | 0 |
| Thalassemia result | 3 | 2 |

## Top factors increasing the model score
| factor | value | baseline | contribution |
|---|---|---|---|
| Thalassemia result | 3 | 2 | +0.191 |
| Major vessels colored (0-4) | 2 | 0 | +0.145 |
| ST depression (oldpeak) | 3.2 | 0.8 | +0.065 |
| Age (years) | 58.0 | 55.5 | +0.019 |

## Top factors decreasing the model score
| factor | value | baseline | contribution |
|---|---|---|---|
| Chest pain type | 2 | 0 | -0.423 |
| Serum cholesterol (mg/dl) | 224.0 | 240.5 | -0.004 |
| Resting blood pressure (mmHg) | 132.0 | 130.0 | -0.002 |

## Notes
Contributions are one-at-a-time marginal effects on the **deployed model's**
score relative to a cohort baseline; they are model-based, approximate, and
**not causal**. This report is an educational explanation of a model score, not a
clinical assessment.
