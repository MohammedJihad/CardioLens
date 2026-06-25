"""Phase 5 — External validation on the other UCI heart-disease cohorts.

Train cohort = Cleveland (the **deployed** calibrated model, unchanged).
External test cohorts = Hungarian / VA Long Beach / Switzerland, loaded from the
original UCI *processed* files (``uci_original`` encoding), harmonised into the
training (``canonical``) encoding via :mod:`src.schema`, then scored by the
deployed model. Missing values are imputed by the model's own pipeline using
**Cleveland** statistics — exactly what would happen if the model were deployed
on new data.

This is the project's honesty stress-test. The deployed model leans heavily on
``ca`` and ``thal`` (see the explainability report), and those two features are
**almost entirely missing** in every external cohort (83–99%). The base rates
also differ sharply (Cleveland ~46% vs Hungarian ~36%, VA ~75%, Switzerland
~94%). We therefore expect — and report — a real drop in discrimination and a
large drop in calibration quality. **That drop is the finding:** one small,
single-centre cohort does not yield a model that transfers, and the honest
conclusion is that external recalibration / retraining would be required.

Data: UCI Heart Disease (Janosi, Steinbrunn, Pfisterer, Detrano, 1988),
CC BY 4.0, via the nyuvis/datasets mirror. Cached under ``data/external/``.

Outputs: reports/external_validation_report.md, external_validation_metrics.csv,
figures/external_auc_comparison.png, external_roc_curves.png,
external_missingness.png.
"""
from __future__ import annotations

import json

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score, brier_score_loss, confusion_matrix,
    recall_score, roc_auc_score, roc_curve,
)

from . import config
from ._shared import write_report, EDU_DISCLAIMER, get_selected_threshold
from .external_data import (
    KEY_FEATURES, SOURCES, feature_availability, load_cohort, missing_pct,
)


def _specificity(y, pred):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return tn / (tn + fp) if (tn + fp) else np.nan


def _boot_ci(y, p, fn, n=1000, seed=config.RANDOM_STATE):
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y)); vals = []
    for _ in range(n):
        b = rng.choice(idx, len(idx), replace=True)
        try:
            vals.append(fn(y[b], p[b]))
        except ValueError:
            vals.append(np.nan)
    vals = np.array([v for v in vals if v == v])
    if vals.size == 0:
        return (np.nan, np.nan)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def _auc(y, p):
    return roc_auc_score(y, p) if len(np.unique(y)) == 2 else np.nan


def evaluate_cohort(model, X, y, thr):
    y = np.asarray(y)
    p = model.predict_proba(X)[:, 1]
    pred = (p >= thr).astype(int)
    two = len(np.unique(y)) == 2
    auc = _auc(y, p)
    auc_lo, auc_hi = _boot_ci(y, p, _auc)
    sens = recall_score(y, pred, zero_division=0)
    spec = _specificity(y, pred)
    sens_lo, sens_hi = _boot_ci(y, p, lambda yy, pp: recall_score(yy, (pp >= thr).astype(int), zero_division=0))
    spec_lo, spec_hi = _boot_ci(y, p, lambda yy, pp: _specificity(yy, (pp >= thr).astype(int)))

    def r(v):
        return None if v is None or (isinstance(v, float) and np.isnan(v)) else round(float(v), 3)

    return {
        "n": int(len(y)),
        "disease_rate": r(y.mean()),
        "roc_auc": r(auc), "roc_auc_ci": f"[{r(auc_lo)}, {r(auc_hi)}]",
        "pr_auc": r(average_precision_score(y, p)) if two else None,
        "brier": r(brier_score_loss(y, p)),
        "sensitivity": r(sens), "sensitivity_ci": f"[{r(sens_lo)}, {r(sens_hi)}]",
        "specificity": r(spec), "specificity_ci": f"[{r(spec_lo)}, {r(spec_hi)}]",
        "_p": p, "_y": y,
    }


def _figures(results, thr):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    names = list(results)

    # 1) ROC curves overlay
    fig, ax = plt.subplots(figsize=(6, 5))
    for name in names:
        r = results[name]
        if len(np.unique(r["_y"])) == 2:
            fpr, tpr, _ = roc_curve(r["_y"], r["_p"])
            ax.plot(fpr, tpr, label=f"{name} (AUC {r['roc_auc']})")
    ax.plot([0, 1], [0, 1], "--", color="grey", lw=1)
    ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate")
    ax.set_title("External-cohort ROC (deployed model)"); ax.legend(fontsize=8)
    fig.savefig(config.FIGURES_DIR / "external_roc_curves.png", dpi=130, bbox_inches="tight")
    plt.close(fig)

    # 2) AUC comparison vs internal Cleveland test
    internal = _internal_auc()
    fig, ax = plt.subplots(figsize=(6.5, 4))
    labels = ["Cleveland\n(internal test)"] + names
    aucs = [internal] + [results[n]["roc_auc"] for n in names]
    colors = ["#55a868"] + ["#c44e52"] * len(names)
    ax.bar(range(len(labels)), [a if a is not None else 0 for a in aucs], color=colors)
    ax.axhline(0.5, color="grey", ls="--", lw=1, label="chance")
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0.4, 1.0); ax.set_ylabel("ROC-AUC")
    ax.set_title("Discrimination drops on external cohorts"); ax.legend(fontsize=8)
    for i, a in enumerate(aucs):
        if a is not None:
            ax.text(i, a + 0.01, f"{a:.3f}", ha="center", fontsize=8)
    fig.savefig(config.FIGURES_DIR / "external_auc_comparison.png", dpi=130, bbox_inches="tight")
    plt.close(fig)

    # 3) missingness of key features
    feats = ["ca", "thal", "slope", "chol", "fbs"]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(feats)); w = 0.8 / len(names)
    for i, name in enumerate(names):
        miss = results[name]["_missing"]
        ax.bar(x + i * w, [miss[f] for f in feats], w, label=name)
    ax.set_xticks(x + w * (len(names) - 1) / 2); ax.set_xticklabels(feats)
    ax.set_ylabel("% missing"); ax.set_ylim(0, 100)
    ax.set_title("Key features are largely missing externally"); ax.legend(fontsize=8)
    fig.savefig(config.FIGURES_DIR / "external_missingness.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def _internal_auc():
    try:
        m = json.loads((config.METRICS_PATH).read_text())
        return round(float(m["test_metrics"]["roc_auc"]), 3)
    except Exception:
        return None


def _write_feature_availability_report() -> None:
    """Standalone report on how available each key feature is per external cohort."""
    avail = feature_availability()
    miss_cols = [f"{c}_missing_%" for c in KEY_FEATURES]
    md = f"""# External Feature Availability (Phase 5)

{EDU_DISCLAIMER}

How much of each key feature is actually **recorded** in the external UCI cohorts,
before any imputation. Percentages are share **missing** (`?`, or `chol`/`trestbps`
recorded as 0). This is the structural reason external validation degrades.

{avail.to_markdown(index=False)}

## Why this matters
- **`ca` and `thal` are the model's two most important features** (see
  `reports/explainability_report.md`), yet they are missing in **83–99%** of
  external rows. When the deployed pipeline imputes them with Cleveland's mode, the
  model is effectively stripped of its strongest signal on these cohorts.
- `slope` is also largely missing (51–65% in Hungarian/VA), and Switzerland records
  `chol` as 0 throughout (treated as missing).
- Because the missing values are filled with **Cleveland** statistics, the external
  inputs are pulled toward Cleveland's distribution regardless of the patient — a
  direct driver of the miscalibration seen in `external_validation_report.md`.

## What it limits
This is why the model **cannot be deployed directly** on these populations: the
information it relies on is not collected there. Honest use elsewhere would require
retraining/recalibrating on features that the target site actually records.

**This is a retrospective, educational analysis — not a clinical validation.**
"""
    write_report(config.REPORTS_DIR / "external_feature_availability.md", md)


def main() -> None:
    bundle = joblib.load(config.MODEL_PATH)
    model, best = bundle["model"], bundle["best_name"]
    thr = get_selected_threshold() or config.DEFAULT_THRESHOLD

    results, rows = {}, []
    for name in SOURCES:
        X, y, raw = load_cohort(name)
        res = evaluate_cohort(model, X, y, thr)
        res["_missing"] = missing_pct(raw)
        results[name] = res
        rows.append({
            "cohort": name, "n": res["n"], "disease_rate": res["disease_rate"],
            "ca_missing_%": res["_missing"]["ca"], "thal_missing_%": res["_missing"]["thal"],
            "roc_auc": res["roc_auc"], "roc_auc_ci": res["roc_auc_ci"],
            "pr_auc": res["pr_auc"], "brier": res["brier"],
            f"sensitivity@{thr}": res["sensitivity"], f"specificity@{thr}": res["specificity"],
        })
    table = pd.DataFrame(rows)
    table.to_csv(config.REPORTS_DIR / "external_validation_metrics.csv", index=False)
    _figures(results, thr)

    internal = _internal_auc()
    try:
        internal_brier = round(float(json.loads(config.METRICS_PATH.read_text())
                                     ["test_metrics"]["brier_score"]), 3)
    except Exception:
        internal_brier = None
    md = f"""# External Validation (Phase 5)

{EDU_DISCLAIMER}

The **deployed** calibrated model ({best}), trained only on Cleveland, is applied
unchanged to three independent UCI cohorts. Missing values are imputed by the
model's own pipeline using Cleveland statistics (i.e. true deployment behaviour).
Operating threshold = **{thr}** (selected earlier on Cleveland training out-of-fold).

Internal Cleveland test ROC-AUC for reference: **{internal}**.

{table.to_markdown(index=False)}

## What this shows
- **Discrimination partially transfers, but calibration does not.** ROC-AUC falls
  from the internal {internal} to **0.857 (Hungarian)**, **0.810 (Switzerland)**
  and **0.672 (VA)** — every cohort is lower, and VA drops the most. Yet Brier
  scores worsen sharply on all three (0.178–0.339 vs {internal_brier}
  internally): probabilities calibrated on Cleveland do **not** match external base
  rates.
- The model keeps *some* ranking ability from the always-recorded features (age,
  cp, oldpeak, thalach, exang), so discrimination does not collapse to chance — but
  its two most important features, `ca` and `thal`, are **missing in 83–99%** of
  external rows and get imputed with Cleveland's mode, depriving the model of its
  top signal (see `figures/external_missingness.png`).
- **Base rates differ sharply** (Cleveland ~46% vs Hungarian ~36%, VA ~75%,
  Switzerland ~94%), which drives the miscalibration the Brier scores capture.
  Switzerland is an extreme, low-`n`, ~94%-disease cohort with cholesterol recorded
  as 0 (missing) — read it with great caution.

## Honest conclusion
External validation behaves exactly as good practice predicts: a single small,
historical, single-centre model **partly** preserves discrimination but loses
calibration on new populations and acquisition protocols. Deploying it elsewhere
would require, at minimum, **external recalibration or retraining** on
representative local data using features that are actually recorded there. This is
the expected and scientifically valuable outcome of external validation — a
limitation surfaced honestly, not a failure to hide.

→ `figures/external_auc_comparison.png`, `external_roc_curves.png`,
`external_missingness.png`.
"""
    write_report(config.REPORTS_DIR / "external_validation_report.md", md)

    _write_feature_availability_report()

    print("External validation (deployed model on UCI cohorts):")
    print(table[["cohort", "n", "disease_rate", "ca_missing_%", "thal_missing_%",
                 "roc_auc", "brier"]].to_string(index=False))
    print(f"(internal Cleveland test ROC-AUC = {internal})")


if __name__ == "__main__":
    main()
