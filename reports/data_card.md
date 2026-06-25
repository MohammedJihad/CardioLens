# Data Card — UCI Cleveland Heart Disease (as used in this project)

_Educational and research use only. This card documents the dataset actually used
for modelling; the broader source survey is in `data_source_research.md`._

## Identity
- **Name:** UCI Heart Disease — Cleveland cohort (circulating processed CSV).
- **Source of record:** UCI Machine Learning Repository, "Heart Disease" (id 45),
  DOI 10.24432/C52P4X. Original contributors: Janosi, Steinbrunn, Pfisterer,
  Detrano (1988). License **CC BY 4.0**.
- **File in repo:** `data/raw/heart_cleveland.csv` → cleaned to
  `data/processed/heart_processed.csv` by `python -m src.data`.

## Size & composition
- **Rows:** 303 raw → **302 after removing 1 exact duplicate.**
- **Columns:** 13 clinical features + 1 target.
- **Class balance:** 45.7% disease (138 disease / 164 no-disease) — roughly
  balanced.

## Features
Numeric: `age`, `trestbps` (resting BP), `chol` (cholesterol), `thalach` (max HR),
`oldpeak` (ST depression). Categorical: `sex`, `cp` (chest pain type), `fbs`
(fasting blood sugar > 120), `restecg`, `exang` (exercise angina), `slope`,
`ca` (major vessels 0–4), `thal`. Full definitions in `dataset_description.md`.

## Target
`heart_disease` — **1 = disease present, 0 = absent.** Derived per-source (see
`dataset_registry.py`): the circulating Cleveland CSV ships an **inverted** binary
label, corrected with `heart_disease = 1 - target` (verified by exploratory
consistency checks — lower max-HR, higher oldpeak, more exercise angina all track
the diseased group; see `data/README.md`). Original UCI files (`num` 0–4) instead
use `(num > 0)`.

## Missing values
The circulating CSV has no explicit missing cells, but the pipeline still imputes
(median / mode) because the original UCI files use `?` for missing `ca`/`thal`,
and external cohorts (Hungarian/VA/Switzerland) have substantial missingness in
exactly those high-importance fields.

## Known bias & representativeness
- **Single centre, 1988, ~300 patients** — not representative of any current or
  general population.
- **Subgroup imbalance:** females are under-represented (~32%) and have a much
  lower disease rate here (~25%) than males (~55%); age skews older. See
  `reports/subgroup_report.md` (exploratory).
- Referral/selection bias typical of a cardiology-clinic cohort.

## Provenance caveats
Many re-encoded/relabelled copies of "Cleveland" circulate (different `cp`,
`slope`, `thal` codings; sometimes inverted targets). This project traces to UCI,
documents the inversion, and harmonises encodings via `src/schema.py` before any
cross-cohort use.

## Why this dataset is NOT enough for clinical deployment
Too small for stable estimates (wide CIs), decades old, single-cohort, no external
validation here, and the most predictive features (`ca`, `thal`) are often
unrecorded elsewhere. Suitable for **education and method demonstration only** —
never for diagnosis or clinical decisions.
