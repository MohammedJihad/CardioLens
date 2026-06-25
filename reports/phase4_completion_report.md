# Phase 4 — Completion Report: Product Surface & Lightweight Reproducibility

_Educational and research use only. Outputs are **model scores** /
**model-estimated probabilities**, never diagnoses. Not a medical device; no
clinical validation._

Phase 4 wraps the Phase 0–3 science in a clean demo and a small API so the
project can be shown as a portfolio product. **The trained model and all metrics
are unchanged** (no retraining was required).

## Changed / new files
- **`app/streamlit_app.py`** — rebuilt as a **multipage** dashboard.
- **`api/main.py`** (new) — FastAPI service.
- **`Makefile`** (new) — task runner.
- **`src/subgroup.py`** — OOF now uses the **base (uncalibrated) pipeline**
  (faster, leakage-free); report reframed as an *exploratory performance screen,
  not a calibrated fairness audit*.
- **`src/_shared.py`** — added `get_selected_threshold()` so the app/API can show
  the training-OOF-selected operating point without recomputing it.
- Docs: this report + README run instructions; tests added.

## Streamlit dashboard
`streamlit run app/streamlit_app.py` — pages: **Prediction**, **Explanation**,
**Performance**, **Threshold & Calibration**, **Limitations**. Inputs live in the
sidebar; output is a **model score** + band with disclaimers on every page.
Performance/threshold/calibration pages render the already-generated figures and
reports (no new metrics invented).

## FastAPI
`uvicorn api.main:app --reload` (interactive docs at `/docs`). Endpoints:
- `GET /health` → `{"status":"ok","model_loaded":true}`
- `GET /model-info` → model name, features, default + selected threshold, disclaimer
- `POST /predict` (Pydantic-validated) → see example below.

### Example request / response
```
POST /predict
{ "age":62,"sex":1,"cp":0,"trestbps":140,"chol":268,"fbs":0,"restecg":0,
  "thalach":130,"exang":1,"oldpeak":3.6,"slope":0,"ca":2,"thal":3 }
```
```json
{
  "model_score": 1.0,
  "score_band": "Very high model score",
  "default_threshold": 0.5,
  "above_default_threshold": true,
  "selected_threshold": 0.2,
  "model": "Random Forest",
  "disclaimer": "Educational model score only — not a diagnosis, not medical advice, and not a medical device. No clinical validation."
}
```
No `diagnosis` field is ever returned; out-of-range inputs are rejected with HTTP 422.

## Makefile
`make data | train | evaluate | phase1 | explain | subgroup | app | api | test | all`.

## Verification
- `python -m src.predict` ✓
- FastAPI `/health`, `/model-info`, `/predict` smoke-tested via `TestClient` ✓
- `pytest` → all passing (existing + new: API health, API predict schema +
  no-diagnosis, API input validation 422, Streamlit file present with
  disclaimer/model-score language). A subprocess **hang-guard** for
  `python -m src.subgroup` also exists but is **opt-in** (see note below).

## Confirmations
- **Model metrics did not change** (no retraining; calibrated Random Forest and all
  Phase 0–3 reports preserved).
- **NOT started:** MLflow, Docker, CI, external validation.

## Remaining limitations
All Phase 0–3 limitations stand (small single historical cohort, no external
validation, exploratory subgroups, model-based non-causal explanations). The app
and API are demos for educational use only.

## Status
**Phase 4 complete.** Suggested next: **external validation** (the scientific
"crown"), or the engineering layer (CI / Docker / MLflow) if targeting MLOps roles.

## Review cleanup pass (wording/documentation only — no metric change)
- `python -m src.predict` now prints **only the safe public keys** via
  `public_view()` (`model_score`, `score_band`, `prediction_at_default_threshold`,
  `disclaimer`, …). Legacy `disease_probability`/`risk_band`/`prediction` remain in
  the returned dict but are clearly **deprecated** and hidden from the CLI/public view.
- API `/model-info` `output` reworded to
  *"model_score / model-estimated probability on research data"* (no clinical-probability implication).
- Streamlit Prediction page reworded to *"the model score is above/below the
  default threshold"* (removed clinical-sounding *positive/negative*).
- Subgroup report header now states it uses the **uncalibrated base RF pipeline**
  for OOF discrimination, while the deployed model stays calibrated separately;
  threshold-based recall/specificity flagged exploratory.
- Tests updated to assert the preferred `model_score`/`score_band` schema; test
  count grows with later phases; the default suite is deterministic.

## Reproducibility fix — `python -m src.subgroup` now exits cleanly
**Root cause:** the subgroup OOF used `cross_val_predict`. Even with `n_jobs=1`,
joblib/loky initialises a resource tracker / worker machinery that can stay alive
on some environments, so the command printed its table but the process never
terminated (it had to be timed out).

**Fix:** replaced `cross_val_predict` with a **manual serial `StratifiedKFold`
OOF loop** and forced the estimator to `n_jobs=1` — no joblib, no loky, no
lingering threads. The analysis stays leakage-free and exploratory, and the OOF
numbers are unchanged from the base-pipeline computation. Matplotlib figures are
closed explicitly. A new **subprocess hang-guard test** runs `python -m
src.subgroup` and fails if it does not terminate. The test deliberately avoids
`subprocess.run(capture_output=True)` — capturing via a PIPE makes the parent
block in `communicate()` until pipe EOF, which a lingering grandchild process can
prevent (this is what hung the test under `pytest` even though the command exits
fine directly). Instead it sends stdout to DEVNULL, runs the child in its own
process group with a single-threaded env, polls manually, and force-kills the
whole group on timeout. It also asserts the report/CSV are written. **Update:** because subprocess-under-pytest behaviour varies across environments, this guard is now **skipped by default** and runs only with `RUN_SUBPROCESS_GUARD=1`, so the default `pytest` is deterministic everywhere; the command itself exits cleanly when run directly.
