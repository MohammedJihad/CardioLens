# CardioLens - Educational Heart-Disease ML Demo

A calibrated lens on heart-disease research data.

CardioLens is a responsible machine-learning portfolio project built on the public UCI Cleveland heart-disease dataset. It combines a reproducible ML study with a premium public website that explains the evaluation honestly: what the model gets right, where it transfers, and where its confidence breaks down.

Important: CardioLens is not medical advice. Every number is a model score on historical public research data. It is not a medical verdict, not a diagnostic tool, and not a clinical tool. The model was trained on a small, decades-old, single-centre dataset with no clinical validation.

Live demo: https://cardiolens-psi.vercel.app

API docs: https://cardiolens-api-uhpi.onrender.com/docs

Project dossier: docs/final-dossier/CardioLens_Project_Dossier.pdf

---

## What this is

CardioLens has two parts.

1. The science: a leakage-free machine-learning pipeline that cleans the data, fixes a known target-label inversion, compares models with stratified cross-validation, calibrates the selected model, and evaluates discrimination, calibration, uncertainty, explainability, subgroup performance, and external validation.

2. The website: a Next.js and FastAPI public demo that presents the frozen research outputs clearly, plus one live page where users can score a research-style input pattern and see a model-based explanation.

The scientific results are frozen. The website reads and presents those results; it does not recompute or change them.

---

## Headline results

### Model selection - stratified 5-fold cross-validation

| Model | CV ROC-AUC | CV Recall |
|---|---:|---:|
| Logistic Regression | 0.906 +/- 0.040 | 0.800 |
| SVM RBF | 0.907 +/- 0.042 | 0.818 |
| Random Forest | 0.910 +/- 0.038 | 0.809 |
| MLP | 0.859 +/- 0.063 | 0.773 |
| Dummy baseline | 0.500 | 0.000 |

Random Forest was selected, but the top three models are statistically close. On a dataset this small, a simpler interpretable model is also defensible.

### Held-out test performance

Held-out test set: 61 cases. Default threshold: 0.50.

| Metric | Value |
|---|---:|
| ROC-AUC | 0.892 |
| PR-AUC | 0.853 |
| Sensitivity | 0.714 |
| Specificity | 0.848 |
| F1 | 0.755 |
| Brier score | 0.137 |

Confusion matrix at threshold 0.50:

| | Model above threshold | Model below threshold |
|---|---:|---:|
| Label positive | 20 TP | 8 FN |
| Label negative | 5 FP | 28 TN |

Because the test set is small, intervals are wide. For example, ROC-AUC is 0.892 with interval [0.805, 0.961].

---

## External validation

The central lesson of CardioLens is that discrimination partially transfers, but calibration does not.

The model was trained only on Cleveland and applied unchanged to three independent UCI cohorts.

| Cohort | n | ROC-AUC | Brier | ca / thal missing |
|---|---:|---:|---:|---:|
| Cleveland internal | 61 | 0.892 | 0.137 | not applicable |
| Hungarian | 294 | 0.857 | 0.178 | 99% / 90% |
| VA Long Beach | 200 | 0.672 | 0.339 | 99% / 83% |
| Switzerland | 123 | 0.810 | 0.337 | 96% / 42% |

The model's strongest features, ca and thal, are often missing externally. This is one reason the model's probability calibration degrades outside the original training cohort.

---

## Website pages

The website includes:

- Home
- Try the model
- Results
- External test
- Thresholds
- Transparency
- About

The Try page is stateless. Inputs are sent to the API to compute a score and are not stored. There is no account system, no database, and no analytics tracking user inputs.

---

## Architecture

CardioLens uses:

- Next.js frontend
- FastAPI backend
- Frozen model artifact
- Static reports-summary JSON for public results pages
- Render for the API deployment
- Vercel for the frontend deployment

Six pages are static and read from committed report snapshots. Only the Try page calls the FastAPI predict endpoint.

---

## Project structure

- src: data, preprocessing, training, evaluation, explanation
- models: frozen calibrated model artifact
- reports: metrics, model card, validation reports, figures
- data: raw, external, and processed datasets
- notebooks: original notebook
- tests: test suite
- api: FastAPI service
- frontend: Next.js public website
- web-data: reports-summary JSON snapshot
- docs: design docs, deployment guide, final dossier
- Dockerfile: API deployment container
- render.yaml: Render deployment config

---

## Run locally

Backend:

1. Create a Python virtual environment.
2. Install requirements.
3. Run python -m src.data.
4. Run uvicorn api.main:app --reload.
5. Open http://127.0.0.1:8000/docs.

Frontend:

1. cd frontend
2. npm install
3. copy .env.local.example to .env.local
4. npm run dev
5. Open http://localhost:3000.

---

## Deployment

API on Render:

https://cardiolens-api-uhpi.onrender.com/docs

Frontend on Vercel:

https://cardiolens-psi.vercel.app

For full deployment instructions, see docs/DEPLOYMENT.md.

---

## Responsible use

CardioLens shows how a frozen machine-learning model behaves on historical public research data. It is not medical advice, not a medical verdict, and not a clinical tool.

Results are framed as model scores on research data. For any real health concern, talk to a qualified clinician.

---

## License and data

Code is released under the repository license.

Dataset: UCI Heart Disease Cleveland dataset, DOI 10.24432/C52P4X, CC BY 4.0.

CardioLens is an educational machine-learning case study. It is not medical advice.