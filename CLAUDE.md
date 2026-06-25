# CLAUDE.md — Heart-Disease ML → Public Web Experience

You are building a **premium public website** for an existing, finished heart-disease
ML project. Your job is to *present* the frozen science beautifully and add one live
interactive demo. You are **not** doing data science here.

Read `docs/WEBSITE_PLAN.md` before starting. Work **phase by phase** and **stop for
my approval** after each phase (use Plan Mode first).

---

## 🚫 Red lines (never cross)
- **Do NOT modify, regenerate, retrain, or "improve"** anything in: `src/`, `models/`,
  `reports/`, `data/`, `notebooks/`, `tests/`, `Makefile`, `requirements.txt`,
  `pyproject.toml`. The model, metrics, and scientific results are **frozen**.
- The website lives in a **new `frontend/`** folder. The only backend edits allowed are
  **additive** changes to `api/main.py` (new endpoints / extra response fields) that
  **reuse existing functions** (`predict_one`, `explain_prediction`, report files) and
  **must not change the model or any metric**. If a change would alter a number, stop
  and ask.
- **Never hand-type metrics.** Every number on the site comes from the real files in
  `reports/` (e.g. `metrics.json`, `external_validation_metrics.csv`,
  `threshold_test_evaluation.csv`, `feature_importance.csv`). Snapshot them to
  `frontend/data/reports-summary.json` at build time.
- **Do not** add a database, auth, accounts, analytics of medical inputs, or any storage
  of user inputs. Inputs are sent to the model to compute a score and are **not stored**.
- **Do not deploy, create accounts, or enter any secret/token/API key yourself.** Prepare
  configs + docs and hand those steps to me.

## ✅ Safe wording (enforce everywhere — copy, code, tests)
ALLOWED: "model score", "model-estimated probability on research data", "educational ML
demo", "research-style input pattern", "similar historical research patterns",
"above/below threshold", "model-based explanation", "not causal", "not medical advice",
"retrospective educational validation", "historical public research data".

BANNED (never render, even dynamically): "diagnosis", "disease probability" (as clinical
truth), "sick", "healthy", "you have heart disease", "you are safe", "medical decision",
"patient is positive/negative", "clinically validated", "medical-grade", "real-world
clinical tool". Explanations say *"within this model, these inputs pushed the score
up/down"* — never *"this caused heart disease."*

A test must grep the built output for the banned list and fail if any appears.

## 🧱 Stack (do not substitute without asking)
- Frontend: **Next.js (App Router) + TypeScript + Tailwind + Recharts + Framer Motion**,
  **shadcn/ui** for primitives only (button, tooltip, dialog), one **GSAP ScrollTrigger**
  story on the external-validation page. Charts use Recharts from real data — **not**
  embedded matplotlib PNGs.
- Backend: existing **FastAPI** (`api/main.py`), Python. Keep it stateless.
- Most pages are **static** (read `reports-summary.json` at build); only `/try` calls the
  live API. The site must still render if the backend is asleep.

## 🎨 Design intent (keep ONE coherent language)
Calm, trustworthy, editorial — a research-lab case study, not a hospital tool and not a
toy. Off-white/ink base, deep navy-indigo primary, a single muted-teal accent, amber only
for the gauge mid-range. Generous whitespace, big type scale, soft shadows, subtle motion,
full dark mode. Respect `prefers-reduced-motion`. No red alarm UI, no literal beating
heart, no heavy 3D.

## 🧠 Skills to use (consult as principles — don't blindly apply all)
**Primary craft:** high-end-visual-design, impeccable, emil-design-eng,
make-interfaces-feel-better, web-design-guidelines, modern-web-design, frontend-design,
ui-ux-pro-max, design-taste-frontend, brand-guidelines, shadcn-ui, writing-guidelines.
**Next.js / Vercel / perf:** vercel-react-best-practices, vercel-composition-patterns,
vercel-optimize, vercel-react-view-transitions, next-cache-components, web-perf, api-design,
architecture-decision-records, seo-geo.
**Motion (light):** motion-framer, gsap-scrolltrigger.
**Honest data viz / framing:** scientific-visualization, statistical-analysis,
scientific-critical-thinking, scientific-writing.
**Quality / process / safety:** accessibility, webapp-testing, ai-regression-testing,
test-driven-development, verification-loop, systematic-debugging, requesting-code-review,
receiving-code-review, full-output-enforcement, planning-with-files, writing-plans,
ai-first-engineering, git-commit, frontend-design-review (run at the design-review gate).
**Optional:** lightweight-3d-effects (subtle hero only; default to a static SVG/gradient
lattice), deploy-to-vercel + vercel-cli-with-tokens (frontend deploy, docs only — I run it).

**Do NOT use** (redundant or irrelevant): brandkit, canvas-design, ckm-* (all),
ckmdesign*, ckmui-styling, gpt-taste, stitch-design-taste, theme-factory, minimalist-ui,
design-taste-frontend-v1, redesign-existing-projects, web-artifacts-builder, vite-patterns,
spark-app-template, turborepo, threejs-webgl, react-three-fiber, spline-interactive,
blender-web-pipeline, substance-3d-texturing, pixijs-2d, web3d-integration-patterns,
algorithmic-art, animejs, barba-js, locomotive-scroll, lottie-animations, rive-interactive,
scroll-reveal-libraries, animated-component-libraries, remotion, matplotlib, polars, dask,
statsmodels, peer-review, scholar-evaluation, literature-review, pubmed-database,
clinicaltrials-database, fda-database, supabase, stripe-*, cloudflare*, workers-*, wrangler,
durable-objects, sandbox-sdk, expo-*, gws-*, docx, pdf, pptx, agents-sdk, ai-sdk,
agent-browser, anysearch, defuddle, firecrawl-parse, api-connector-builder, skill-creator,
writing-skills, find-skills, cloud-solution-architect, nodejs-backend-patterns.

## ⚙️ Commands
- Backend (existing): `python -m src.predict`, `uvicorn api.main:app --reload`, `pytest`.
- Frontend (new, in `frontend/`): `npm install`, `npm run dev`, `npm run build`,
  `npm run test`, `npm run lint`.

## 🔁 Workflow rules
1. Start in **Plan Mode**; show the plan for the current phase only.
2. Build **one phase** (see `docs/WEBSITE_PLAN.md`), run its tests, then **stop and ask**
   for approval before the next phase.
3. After each phase: confirm no red line was crossed (no edits under `src/`, `models/`,
   `reports/`, `data/`; metrics unchanged), and run the banned-wording test.
4. Commit per phase with clear messages (git-commit skill). Never commit secrets.
5. If anything is ambiguous or would alter the science, **ask me** instead of guessing.
