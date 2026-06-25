# Kickoff — driving this build in **Google Antigravity**

Antigravity reads **`AGENTS.md`** (and **`CLAUDE.md`** when the agent runs on a Claude
model) from the project root automatically — both are included, so your guardrails load
every session. Recommended setup for this sensitive project:

1. Open Antigravity → sign in (personal Gmail, preview).
2. **File → Open Folder** → the repo (the one containing `src/`, `api/`, `reports/`).
3. Pick the model: **Claude Sonnet 4.6** (or Opus) — better for multi-file reasoning and it
   honours `CLAUDE.md`.
4. Set the autonomy profile to **Review-driven development** (checkpoints), and the Terminal
   Execution Policy to **Request review** (so it asks before running commands). This keeps
   the red lines safe.
5. Open **Manager View → Start Conversation** → select this workspace → choose **Planning
   Mode** (it produces a Plan Artifact you approve before any code).
6. Paste the **First message** below. Review the Plan Artifact, comment if needed, approve,
   then let it build **Phase A only**. Use the integrated terminal for `npm run dev` and the
   built-in browser to preview.
7. After each phase, paste the self-check prompt, then drive the next phase.

(If you ever prefer the Claude Code CLI instead: Antigravity is a VS Code fork, so you can
run `claude` in its integrated terminal and the same `CLAUDE.md` applies.)

---

# First message (paste into the agent)

## First message (paste this after launching `claude` in the repo)

> Read `CLAUDE.md` and `docs/WEBSITE_PLAN.md` in full before doing anything.
>
> This repo is a finished heart-disease ML project. We are adding a premium public
> website in a new `frontend/` folder and making only additive changes to `api/main.py`.
> The model, metrics, reports, data, and notebooks are FROZEN — do not modify anything
> under `src/`, `models/`, `reports/`, `data/`, `notebooks/`, `tests/`, or the build
> files. Never hand-type metrics; numbers come from the real files in `reports/`.
>
> Enforce the safe-wording rules in CLAUDE.md everywhere (no "diagnosis", "sick",
> "healthy", "clinically validated", etc.). This is an educational ML demo that shows a
> "model score" on historical research data — never a medical tool.
>
> Use Plan Mode. Start with **Phase A only** (design system, color/type tokens, component
> inventory, final safe copy, and brand name/tagline/tone) from `docs/WEBSITE_PLAN.md`.
> Show me the plan and a small visual preview, then STOP and wait for my approval before
> writing the rest. Do not start Phase B until I say so. Do not deploy or enter any
> secrets — prepare configs and hand those steps to me.

Tip: turn on **Plan Mode** first (press `Shift+Tab` to cycle to "plan mode", or type
`/plan` if available). Review the plan before letting it edit files.

## Driving each later phase (one at a time)
After you approve a phase, paste:

> Phase A is approved. Proceed with **Phase B only** (backend: add `top_positive_factors`/
> `top_negative_factors` to the prediction response, add `GET /reports-summary` and
> `GET /example-inputs`, CORS via `FRONTEND_ORIGIN`). Reuse existing `predict_one` and
> `explain_prediction`. Do NOT change the model or any metric — if a number would change,
> stop and ask. Add the schema / no-diagnosis / reports-match-files tests. Then run
> `pytest`, confirm metrics unchanged, and STOP for my review.

…and similarly "Phase C only", "Phase D only", … each time reminding it to stop and to keep
the red lines and safe wording.

## Useful controls in Antigravity
- **Planning Mode** (per agent) — produces a Plan Artifact; review/comment/approve before code.
- **Manager View** — spawn one agent per phase; watch its artifacts (plan, diffs, screenshots).
- **Comment on artifacts** — leave inline feedback; the agent revises without restarting.
- **Editor View (Ctrl+E)** — open files, read diffs, run the integrated terminal/preview.
- Keep **Review-driven** autonomy + **Request review** terminal policy so nothing runs or
  edits without your OK. Start one phase per conversation to keep context clean.

## After each phase, ask it to self-check
> Before we continue: confirm you did not edit anything under `src/`, `models/`, `reports/`,
> `data/`, `notebooks/`, or `tests/`; confirm `pytest` still passes and metrics are
> unchanged; and run the banned-wording check on what you built. Report the results.
