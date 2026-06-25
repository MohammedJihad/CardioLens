# CardioLens ًں«€ â€” Educational Heart-Disease ML Demo

**A calibrated lens on heart-disease research data.** A reproducible machine-learning
study on the public UCI Cleveland dataset, wrapped in a premium public website that
shows the evaluation *honestly* â€” what the model gets right, where it transfers, and
where its confidence quietly breaks down.

> âڑ ï¸ڈ **Not medical advice.** Every figure is a *model score on historical public
> research data* â€” not a medical verdict and not a clinical tool. Trained on a small,
> decades-old, single-centre dataset with **no clinical validation**.

<!-- After deploying (see docs/DEPLOYMENT.md), fill these in: -->
**ًں”— Live demo:** `https://cardiolens-psi.vercel.app` آ· **API:** `https://cardiolens-api-uhpi.onrender.com/docs`
**ًں“„ Project dossier (36-page PDF):** [`docs/final-dossier/CardioLens_Project_Dossier.pdf`](docs/final-dossier/CardioLens_Project_Dossier.pdf)

---

## What this is

Two halves of one project:

1. **The science** â€” a leakage-free pipeline that cleans the data, fixes a known
   target-label inversion, compares models under stratified cross-validation,
   calibrates the best one, and evaluates it for discrimination, calibration,
   uncertainty, explainability, subgroups, and **generalisation to three external
   cohorts it never trained on.** This is **frozen** â€” the website never recomputes it.
2. **The website (CardioLens)** â€” a Next.js + FastAPI experience that presents those
   frozen numbers as honest, well-designed pages, plus one live page that scores a
   single research-style input pattern and explains it.

## Headline results (generated, not hand-written)

**Model selection â€” stratified 5-fold CV (training split):**

| model | CV ROC-AUC | CV recall |
|---|---|---|
| Logistic Regression | 0.906 آ± 0.040 | 0.800 |
| SVM (RBF) | 0.907 آ± 0.042 | 0.818 |
| **Random Forest** âœ… | **0.910 آ± 0.038** | 0.809 |
| MLP | 0.859 آ± 0.063 | 0.773 |
| Dummy (baseline) | 0.500 | 0.000 |

The top three are a statistical tie â€” on data this small, a simple interpretable
model is as defensible as the ensemble.

**Held-out test (61 cases, threshold 0.50):** ROC-AUC **0.892**, PR-AUC 0.853,
sensitivity 0.714, specificity 0.848, F1 0.755, Brier 0.137. Confusion: TP 20 آ·
FN 8 (missed positive-label cases) آ· TN 28 آ· FP 5. Intervals are wide (e.g. ROC-AUC
**0.892 [0.805, 0.961]**) because the test set is small.

**The central lesson â€” external validation:** the model (trained only on Cleveland)
applied unchanged to three independent cohorts shows that **discrimination partially
transfers, but calibration does not.**

| cohort | n | ROC-AUC | Brier | ca / thal missing |
|---|---:|---:|---:|---:|
| Cleveland (internal) | 61 | 0.892 | 0.137 | â€” |
| Hungarian | 294 | 0.857 | 0.178 | 99% / 90% |
| VA Long Beach | 200 | 0.672 | 0.339 | 99% / 83% |
| Switzerland | 123 | 0.810 | 0.337 | 96% / 42% |

The model's strongest features (`ca`, `thal`) are 42â€“99% missing externally, so its
probabilities stop meaning what they say off the training cohort.

## The website

Seven pages: **/** (thesis + honest stats) آ· **/try** (live model score + explanation)
آ· **/results** (internal metrics) آ· **/external** (the stress test) آ· **/thresholds**
(operating-point trade-off) آ· **/transparency** (full model + data cards) آ· **/about**
(limits, privacy, when to see a clinician).

- **/try** sends one input pattern to the API, returns a **model score** + a gauge +
  the top inputs that pushed the score up/down. It is **stateless**: no account, no
  database, no analytics of inputs â€” scored and forgotten.
- **Architecture:** six static pages render from a committed `reports-summary.json`
  snapshot; only `/try` calls the FastAPI `/predict` endpoint, which loads the frozen
  model. Additive-only backend; no metric ever changes.

## Project structure

```
heart-disease-ml/
â”œâ”€â”€ src/               data آ· preprocess آ· train آ· evaluate آ· explain آ· predict   (FROZEN)
â”œâ”€â”€ models/            best_model.joblib â€” calibrated Random Forest               (FROZEN)
â”œâ”€â”€ reports/           metrics.json آ· model_card.md آ· external validation آ· â€¦     (FROZEN)
â”œâ”€â”€ data/              raw/ (committed) + processed/ (regenerated)                 (FROZEN)
â”œâ”€â”€ notebooks/ tests/  original course notebook آ· pytest suite                    (FROZEN)
â”œâ”€â”€ api/               main.py â€” FastAPI service (+ requirements.txt)
â”œâ”€â”€ frontend/          Next.js 14 site (App Router, TS, Tailwind)
â”œâ”€â”€ web-data/          reports-summary.json (snapshot of the frozen reports)
â”œâ”€â”€ docs/              design/ آ· WEBSITE_PLAN.md آ· DEPLOYMENT.md آ· final-dossier/
â”œâ”€â”€ Dockerfile آ· render.yaml   deploy configs for the API
â””â”€â”€ README.md آ· LICENSE
```

## Run locally

**Science / backend** (Python 3.12):
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.data          # build processed dataset
uvicorn api.main:app --reload    # API at http://127.0.0.1:8000  (docs at /docs)
```

**Frontend** (Node 18+):
```bash
cd frontend
npm install
cp .env.local.example .env.local      # points at http://127.0.0.1:8000 by default
npm run dev                            # site at http://localhost:3000
```

Reproduce the full study with `python -m src.train | evaluate | explain` and `pytest -q`
(a `Makefile` wraps these).

## Deploy it (so people can try it)

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for the full step-by-step: push to
GitHub â†’ backend on **Render** (or Hugging Face Spaces) â†’ frontend on **Vercel** â†’
wire the two with environment variables. Free tiers throughout; you enter every secret.

## Responsible use

CardioLens shows how a frozen model behaves, where it transfers, and where it fails.
It is **not medical advice, not a medical verdict, and not a clinical tool.** Wording
across the site avoids "diagnosis / healthy / sick / you are safe"; results are framed
as *model scores on research data*. For any concern about your own health, talk to a
qualified clinician.

## License & data

Code released under the repository `LICENSE`. Dataset: UCI Heart Disease (Cleveland),
DOI 10.24432/C52P4X, CC BY 4.0 â€” Janosi, Steinbrunn, Pfisterer, Detrano (1988).

*An educational machine-learning case study. Not medical advice.*

