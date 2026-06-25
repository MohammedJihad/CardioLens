# Website Build Plan

A premium, mostly-static Next.js case-study site that re-presents the frozen heart-disease
ML science and adds one live interactive demo on `/try` (calls the existing FastAPI).

## Pages (Next.js App Router)
- `/` Home — hero, story in three beats (build → explain → stress-test), trust strip, CTA.
- `/try` — input form (grouped), presets, result card (gauge, band, above/below threshold),
  inline explanation, "what this means" (plain language), disclaimer.
- `/results` — internal performance: metric cards, confusion matrix, ROC/PR, learning curve,
  CIs. Honest "small test set" framing.
- `/external` — external-validation scroll-story: AUC drop (0.892 → 0.857 / 0.672 / 0.810),
  Brier worsening, missing-feature chart, "discrimination partially transfers, calibration
  does not." (GSAP pinned sequence.)
- `/thresholds` — threshold trade-off (0.20 OOF-selected, evaluated once → sens 1.00 /
  spec 0.606 / FN 0) + calibration explainer. "Screening-oriented, not clinical."
- `/transparency` — model card + data card rendered as readable web content; downloads;
  methodology highlights (leakage-free CV, target-inversion fix, harmonized encodings).
- `/about` — limitations (can/cannot cards), "when to seek real help" (no medical advice),
  privacy ("inputs are not stored"), project story, stack, GitHub.

Every page: persistent `DisclaimerBanner`; section rhythm = eyebrow → headline →
1–2 sentence plain intro → visual → one-line honest caveat.

## Components
HeroSection, DisclaimerBanner, Navigation, Footer, MetricCard, ModelScoreGauge,
FeatureImpactChart, ExternalValidationChart, ThresholdTradeoffChart, MissingFeatureChart,
CalibrationMeter, ConfusionMatrix, LearningCurveChart, LimitationsGrid, InputForm,
PresetPicker, ResultCard, PlainLanguageBox, ReportCard, CanCannotCards.

## Real data sources (snapshot to frontend/data/reports-summary.json — never hand-typed)
- `reports/metrics.json` → internal ROC-AUC 0.892, PR-AUC 0.853, sensitivity 0.714,
  specificity 0.848, F1 0.755, Brier 0.137, confusion TP20/FN8/TN28/FP5 (n=61).
- `reports/external_validation_metrics.csv` → Hungarian 0.857/Brier0.178,
  VA 0.672/0.339, Switzerland 0.810/0.337; ca/thal 83–99% missing.
- `reports/threshold_test_evaluation.csv` → threshold 0.20: TP28/FP13/TN20/FN0,
  sens 1.00, spec 0.606, precision 0.683, f1 0.812.
- `reports/feature_importance.csv` → permutation importances (ca, cp, thal, oldpeak…).
- `reports/external_feature_availability.md` / figures → missingness per cohort.

## Backend (additive only — no model/metric change)
- Extend `POST /predict` (or add `POST /explain`) to include `top_positive_factors` /
  `top_negative_factors` from the existing `explain_prediction()`.
- `GET /reports-summary` → serve the real numbers above as JSON (single source of truth).
- `GET /example-inputs` → the 3 presets (low / borderline / high model score).
- CORS: dev `http://localhost:3000`; prod origin via `FRONTEND_ORIGIN` env var; no wildcard
  in prod (or document as demo-only). Keep `/predict` free of any `diagnosis` field.

## Phases (one at a time, stop for approval after each)
**A — Design system & content.** Tailwind tokens, type scale, color, components inventory,
final safe copy, brand (name/tagline/tone). Output: styled kit + copy doc. Test:
banned-wording unit test. Checkpoint: approve look + copy before building pages.

**B — Backend polish.** Add factors to `/predict` (or `/explain`), `/reports-summary`,
`/example-inputs`, CORS env var. Test: response schema; no-diagnosis; `/reports-summary`
values equal the real files (golden test). Risk: none to model (additive only).

**C — Frontend foundation.** Next.js scaffold in `frontend/`, layout, Navigation,
DisclaimerBanner, Footer, Home. Test: pages render; a11y smoke. 

**D — Try-demo flow.** InputForm (grouped), PresetPicker, ResultCard, ModelScoreGauge,
explanation. Test: API integration for the 3 presets; no-diagnosis wording; validation errors.

**E — Charts & reports.** `/results`, `/external`, `/thresholds`, `/transparency` from the
static JSON. Test: chart data === source files; caveat line present on every chart.

**F — Responsible-AI safety review.** Can/cannot cards, privacy, when-to-seek-help, full
wording audit across the build. Test: global banned-wording scan on built output. Gate
before deploy.

**G — Deployment docs.** Vercel (frontend) + Render or HF Space Docker (FastAPI) guide,
env vars, CORS, `Dockerfile` for the API. (I run the actual deploy + secrets.)

**H — Final polish.** Motion tuning, reduced-motion, Lighthouse + axe pass, OG/meta
(seo-geo), README / case-study writeup.

## Deployment (recommendation)
Frontend on **Vercel**, FastAPI on **Render** (or HF Space Docker as all-in-one fallback),
CORS via `FRONTEND_ORIGIN`. Because most pages read static JSON, the site stays fast and
functional even if the backend is cold; only `/try` needs the live API.

## Testing & verification
Backend: schema; no-diagnosis; reports-summary == real files. Frontend: routes exist;
banned-wording grep on build output; component render; gauge score→band mapping; mocked +
live `/predict` for presets. Privacy: no localStorage/DB/analytics of inputs; "inputs not
stored" copy present. Deployment: Lighthouse perf/a11y targets; reduced-motion honored.
