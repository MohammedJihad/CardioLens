# External validation cohorts (UCI Heart Disease)

These three cohorts are used **only for external validation** (Phase 5); the model
is never trained on them.

| file | cohort | rows | notes |
|---|---|---|---|
| `hungarian.data` | Hungarian Institute of Cardiology, Budapest | 294 | `ca`/`thal` almost all missing |
| `va.data` | V.A. Medical Center, Long Beach | 200 | high disease rate (~75%) |
| `switzerland.data` | University Hospitals, Zurich/Basel | 123 | cholesterol recorded as 0 (missing); ~94% disease |

**Source:** UCI Machine Learning Repository — Heart Disease (Janosi, Steinbrunn,
Pfisterer, Detrano, 1988), DOI 10.24432/C52P4X, license **CC BY 4.0**. Files are
the original *processed* 14-column versions (`num` target 0–4; `?` = missing),
retrieved from the `nyuvis/datasets` GitHub mirror and cached here for
reproducibility. Encodings are harmonised to the training schema by
`src/schema.py` before scoring; see `reports/external_validation_report.md`.
