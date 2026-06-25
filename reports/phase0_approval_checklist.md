# Phase 0 — Approval Checklist

A go/no-go gate before Phase 1. Status reflects the Phase 0 cleanup pass.

## Research & strategy
- [x] **Data sources researched** — UCI (Cleveland/Hungarian/VA/Switzerland),
      Statlog, CDC BRFSS, NHANES, MIMIC-IV → `reports/data_source_research.md`.
- [x] **Safe datasets identified** — UCI cohorts + Statlog (CC BY 4.0,
      de-identified); BRFSS (CDC public-use); NHANES (CDC public, de-identified).
- [x] **Rejected datasets documented** — any scraped/identifiable data;
      unprovenanced CSVs as a source of record.
- [x] **First dataset selected** — UCI Cleveland (already integrated, 302 rows).
- [x] **External-validation dataset selected** — UCI Hungarian (primary),
      VA Long Beach (secondary), Switzerland (cautious).
- [x] **Separate public-health track defined** — BRFSS (Track B), not merged
      with UCI; NHANES as alternative; MIMIC-IV gated (Track C).

## Correctness cleanup (this pass)
- [x] **Target mapping made safe** — per-source rules in `src/dataset_registry.py`
      (`kaggle_inverted_binary` vs `uci_num_severity`); no global `1 - target`.
- [x] **Schema harmonization scaffolded** — `src/schema.py` documents the
      UCI-original → canonical encoding maps (cp/slope/thal). External cohorts are
      **registered, not loaded/trained**.
- [x] **README wording fixed** — "medical-grade" → "clinically aware".
- [x] **Explainability runtime made safe** — `N_JOBS=1`,
      `PERMUTATION_N_REPEATS=10` in `config.py`, used by `train.py` / `explain.py`.
- [x] **pytest runs without `PYTHONPATH=.`** — `pyproject.toml` (pythonpath) +
      `tests/conftest.py`.
- [x] **Phase 0 wording clarified** — "no *new* training; existing artifacts
      preserved" across both reports.
- [x] **BRFSS source-of-record corrected** — CDC official; Kaggle = mirror.

## Reproducibility cleanup #2 (training hang)
- [x] **`python -m src.train` hang fixed.** Root cause: HistGradientBoosting's
      internal **OpenMP** threading (independent of `n_jobs`) can deadlock on
      constrained/containerised environments. Two-layer fix:
      (1) native thread pools capped to 1 in `src/__init__.py` **before** sklearn
      imports; (2) HistGradientBoosting made **opt-in** via `config.INCLUDE_HISTGB`
      (default `False`), so the default run uses Dummy + LogReg + SVM + MLP + RF.
      HGB was **not removed** — enabling the flag restores it (CV ROC-AUC ≈ 0.869)
      and completes; it does not change the selected model or metrics.
- [x] **"verified clinically" wording removed** → "verified by exploratory
      consistency checks" in `src/dataset_registry.py`.

## Reproducibility check (current data unchanged)
- [x] `python -m src.data` → 302 rows, 45.7% disease.
- [x] `python -m src.train` → **finishes in ~9s** (HGB opt-in off); best model +
      metrics **unchanged** vs pre-cleanup.
- [x] `python -m src.evaluate` → ROC-AUC 0.892, recall 0.714, FN 8 (identical).
- [x] `python -m src.explain` → completes (~18s), no hang.
- [x] `python -m src.predict` → works.
- [x] `pytest` → 7 passed directly (no `PYTHONPATH`).

## Unresolved risks (carry into Phase 1)
- [ ] `thal` value `0` ambiguity in the Kaggle CSV vs UCI `{3,6,7}` — resolve and
      document before any thal-dependent external comparison.
- [ ] Heavy missingness in `ca`/`thal`/`chol` in external UCI cohorts — expect
      performance drop; quantify and report honestly.
- [ ] Small data throughout — point metrics carry wide uncertainty (addressed by
      planned bootstrap CIs / nested CV in Phase 1).

## Training statement
**No new training or model experiments were performed in Phase 0 (including this
cleanup). Previously generated artifacts were preserved; re-running the pipeline
reproduces identical metrics.**

## Decision
**Status: READY for Phase 1** once the above unresolved risks are accepted as
Phase 1 work items. Phase 1 (evaluation depth: thresholds, bootstrap CIs,
nested CV, calibration comparison, decision curve, error analysis, learning
curve) has **not** been started.
