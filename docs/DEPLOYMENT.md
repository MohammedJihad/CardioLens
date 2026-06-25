# Deploying CardioLens

This guide takes the repository from your machine to a **live, public demo** that
anyone can try — without changing any of the frozen science.

CardioLens has two deployable pieces:

| Piece | What it is | Where it goes | Cost |
|---|---|---|---|
| **Frontend** | Next.js site (6 static pages + the live `/try`) | **Vercel** | Free (Hobby) |
| **Backend** | FastAPI service that loads the frozen model | **Render** (or Hugging Face Spaces) | Free tier |

> The free backend **sleeps after ~15 min idle** and takes ~30–50 s to wake on the
> next request. That is fine — the `/try` page already shows a calm *"waking the
> model up"* state for exactly this case.

You (the owner) perform every deploy step and enter every secret. No credentials
live in the repo.

---

## 0 · One-time pre-flight (keep the repo clean)

The updated `.gitignore` already excludes the big/private stuff
(`node_modules/`, `frontend/.next/`, `.venv/`, `.env*`). If you had already
committed any of them in a previous attempt, untrack them once:

```bash
git rm -r --cached frontend/.next frontend/node_modules .venv 2>/dev/null
```

**What actually gets uploaded** (everything needed to run + reproduce):

```
✓ src/  models/best_model.joblib (8.8 MB)  data/raw/  reports/  api/
✓ frontend/src/  frontend/package.json  frontend/public/  (NOT .next or node_modules)
✓ docs/  (incl. docs/final-dossier/ PDF + MD)  web-data/
✓ Dockerfile  render.yaml  requirements.txt  api/requirements.txt  README.md  LICENSE
✗ node_modules, .next, .venv, __pycache__, .env*  (ignored — never pushed)
```

`data/processed/*.csv` is **intentionally not committed** — the build regenerates
it from `data/raw/heart_cleveland.csv` via `python -m src.data`. The `/try`
explanation step needs it, so the Render build command and the Dockerfile both
run that step automatically.

---

## 1 · Push to GitHub

```bash
cd heart-disease-ml
git init
git add .
git commit -m "CardioLens — heart-disease ML study + premium website"
git branch -M main
git remote add origin https://github.com/<you>/cardiolens.git
git push -u origin main
```

(Create the empty `cardiolens` repo on GitHub first, without a README so the push
isn't rejected.)

---

## 2 · Deploy the backend (Render)

1. Go to **render.com → New + → Blueprint**, and select your GitHub repo.
   Render reads `render.yaml` and creates the `cardiolens-api` web service.
2. First build runs `pip install -r api/requirements.txt && python -m src.data`,
   then starts `uvicorn api.main:app`.
3. When it's live you'll get a URL like **`https://cardiolens-api.onrender.com`**.
4. Verify: open `https://cardiolens-api.onrender.com/health` → `{"status":"ok","model_loaded":true}`.
   The interactive API docs are at `…/docs`.

> Leave `FRONTEND_ORIGIN` unset for now — you'll fill it in step 4 once the site URL exists.

---

## 3 · Deploy the frontend (Vercel)

1. Go to **vercel.com → Add New → Project**, import the same GitHub repo.
2. **Root Directory: `frontend`** (important — the Next app lives there).
   Vercel auto-detects Next.js; keep the default build/output settings.
3. Add an environment variable:
   `NEXT_PUBLIC_API_BASE_URL = https://cardiolens-api.onrender.com` (your step-2 URL, **no trailing slash**).
4. Deploy → you get a site URL like **`https://cardiolens.vercel.app`**.

---

## 4 · Wire CORS (connect the two)

The API only accepts requests from the one origin in `FRONTEND_ORIGIN`
(no wildcard in committed code — that's deliberate).

1. In **Render → cardiolens-api → Environment**, set
   `FRONTEND_ORIGIN = https://cardiolens.vercel.app` (your step-3 URL).
2. Save → Render redeploys. Done.

Now open the site, go to **/try**, submit the example pattern, and you should get
a model score plus the up/down factors.

---

## 5 · Replace the placeholder links

`frontend/src/lib/site.ts` ships with a placeholder repo URL:

```ts
repoUrl: "https://github.com/",   // ← change to https://github.com/<you>/cardiolens
```

Set it to your repo (and add your live URL if you keep a `siteUrl` field), commit,
and push — Vercel redeploys automatically. The footer "View the code" link and the
/transparency "Open the repository" button will then resolve correctly.

---

## 6 · Final verification checklist

- [ ] `…/health` returns `model_loaded: true`
- [ ] `/try` returns a score **and** factors (factors confirm `data/processed` was regenerated)
- [ ] All 7 pages load; light/dark toggle works
- [ ] No CORS error in the browser console on `/try`
- [ ] Footer + /transparency repo links point at your GitHub

---

## Alternative backend hosts

**Hugging Face Spaces (Docker)** — ML-native, shows on your HF profile, sleeps less aggressively:
1. Create a **Docker** Space. Push this repo to it (it uses the root `Dockerfile`).
2. In the Space settings, set **app_port = 7860** and add `PORT=7860` + `FRONTEND_ORIGIN=<vercel url>` as secrets/vars.
3. Use the Space URL as `NEXT_PUBLIC_API_BASE_URL` on Vercel.

**Railway / Fly.io** — both consume the root `Dockerfile`; set `FRONTEND_ORIGIN`
and expose `$PORT` the same way.

---

## Troubleshooting

| Symptom | Cause → Fix |
|---|---|
| `/try` first call is slow / times out, then works | Free backend was asleep. Expected; the page shows a waking state. Upgrade the host tier to remove cold starts. |
| Browser console: **CORS** blocked | `FRONTEND_ORIGIN` on the backend ≠ your exact site URL (scheme + host, no trailing slash). Fix and redeploy. |
| Score works but **no factors** appear | `data/processed/heart_processed.csv` missing. Ensure the build ran `python -m src.data` (it's in `render.yaml`/`Dockerfile`). |
| `InconsistentVersionWarning` or model fails to load | Deployed scikit-learn ≠ training version. Pin the exact version in `api/requirements.txt` (find it with `python -c "import sklearn; print(sklearn.__version__)"` in your training env). |
| Build error on `python -m src.data` | `data/raw/heart_cleveland.csv` not pushed. Confirm it's committed (it is not gitignored). |
| Vercel build can't find the app | Root Directory isn't set to `frontend`. |

---

## Security & scope

- Secrets (host tokens, env vars) are entered **only** in the Vercel/Render dashboards — never in git.
- The API has **no auth, no database, no analytics of inputs**; `/predict` scores and forgets. Nothing to leak.
- Deploying changes **none** of the frozen science (`src/ models/ reports/ data/ notebooks/ tests/`); the model artifact is unchanged.

*CardioLens is an educational ML demo on historical public research data — not medical advice.*
