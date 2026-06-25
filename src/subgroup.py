"""Exploratory subgroup analysis (fairness-aware, honest about small n).

Reports model performance separately for sex and age bands. Two deliberate
methodological choices:

* Metrics are computed on **out-of-fold predictions across the whole dataset**
  (each row scored by a model that never saw it) rather than the 61-row test
  split — subgroups of a 61-row set would be far too small to read at all.
* Every subgroup metric carries a bootstrap 95% CI, and the whole analysis is
  labelled **exploratory**: even pooled, the subgroups are small, so apparent
  gaps are usually within noise and must not be read as fairness conclusions.

Outputs: reports/subgroup_metrics.csv, reports/figures/subgroup_metrics.png,
reports/subgroup_report.md.
"""
from __future__ import annotations

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import confusion_matrix, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor
from .train import model_zoo
from ._shared import write_report, EDU_DISCLAIMER

AGE_CUT = 55  # interpretable clinical split: < 55 vs >= 55


def oof_probabilities(X, y, best_name):
    """Leakage-free out-of-fold probabilities via a **manual serial
    StratifiedKFold loop**.

    Deliberately avoids ``cross_val_predict``/joblib: even at ``n_jobs=1`` the
    joblib/loky machinery can leave a resource tracker or worker pool alive on
    some environments, so ``python -m src.subgroup`` would print results but not
    exit. A plain serial loop with a single-threaded estimator removes every
    parallel resource and guarantees a clean exit.

    Uses the base (uncalibrated) pipeline — this is an exploratory *discrimination*
    screen (ROC-AUC unaffected by calibration), not a calibrated fairness audit.
    """
    X = X.reset_index(drop=True)
    y = np.asarray(y)
    pipe = Pipeline([("prep", build_preprocessor()), ("clf", model_zoo()[best_name])])
    clf = pipe.named_steps["clf"]
    if "n_jobs" in clf.get_params():          # force single-threaded fit
        clf.set_params(n_jobs=1)
    cv = StratifiedKFold(config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE)
    oof = np.zeros(len(y), dtype=float)
    for train_idx, val_idx in cv.split(X, y):
        est = clone(pipe)
        est.fit(X.iloc[train_idx], y[train_idx])
        oof[val_idx] = est.predict_proba(X.iloc[val_idx])[:, 1]
    return oof


def _spec(y, pred):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return tn / (tn + fp) if (tn + fp) else np.nan


def _ci(values):
    arr = np.array([v for v in values if not np.isnan(v)], dtype=float)
    if arr.size == 0:
        return (np.nan, np.nan)
    return float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))


def subgroup_row(name, y, proba, thr=config.DEFAULT_THRESHOLD, n_boot=1000):
    y = np.asarray(y); proba = np.asarray(proba)
    pred = (proba >= thr).astype(int)
    two_class = len(np.unique(y)) == 2
    auc = roc_auc_score(y, proba) if two_class else np.nan
    rec = recall_score(y, pred, zero_division=0)
    spec = _spec(y, pred)

    rng = np.random.default_rng(config.RANDOM_STATE)
    idx = np.arange(len(y))
    aucs, recs, specs = [], [], []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        yb, pb = y[b], proba[b]
        predb = (pb >= thr).astype(int)
        aucs.append(roc_auc_score(yb, pb) if len(np.unique(yb)) == 2 else np.nan)
        recs.append(recall_score(yb, predb, zero_division=0))
        specs.append(_spec(yb, predb))
    auc_ci, rec_ci, spec_ci = _ci(aucs), _ci(recs), _ci(specs)

    def s(v):
        return None if v is None or (isinstance(v, float) and np.isnan(v)) else round(float(v), 3)

    return {
        "subgroup": name, "n": int(len(y)), "disease_rate": round(float(y.mean()), 3),
        "roc_auc": s(auc), "roc_auc_ci": f"[{s(auc_ci[0])}, {s(auc_ci[1])}]",
        "recall": s(rec), "recall_ci": f"[{s(rec_ci[0])}, {s(rec_ci[1])}]",
        "specificity": s(spec), "specificity_ci": f"[{s(spec_ci[0])}, {s(spec_ci[1])}]",
    }


def run():
    df = load_processed()
    X, y = df[config.FEATURES], df[config.TARGET]
    best = joblib.load(config.MODEL_PATH)["best_name"]
    proba = oof_probabilities(X, y, best)

    masks = {
        "Overall": np.ones(len(df), dtype=bool),
        "Female (sex=0)": (df["sex"] == 0).to_numpy(),
        "Male (sex=1)": (df["sex"] == 1).to_numpy(),
        f"Age < {AGE_CUT}": (df["age"] < AGE_CUT).to_numpy(),
        f"Age >= {AGE_CUT}": (df["age"] >= AGE_CUT).to_numpy(),
    }
    rows = [subgroup_row(name, y[m], proba[m]) for name, m in masks.items()]
    return pd.DataFrame(rows), best


def plot(table: pd.DataFrame):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sub = table[table["subgroup"] != "Overall"]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(sub))
    ax.bar(x, sub["roc_auc"].astype(float), color="#4c72b0")
    ax.axhline(float(table.loc[table["subgroup"] == "Overall", "roc_auc"].iloc[0]),
               color="grey", ls="--", lw=1, label="Overall OOF ROC-AUC")
    ax.set_xticks(x); ax.set_xticklabels(sub["subgroup"], rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("OOF ROC-AUC"); ax.set_ylim(0.5, 1.0)
    ax.set_title("Subgroup ROC-AUC (out-of-fold) — exploratory"); ax.legend(fontsize=8)
    fig.savefig(config.FIGURES_DIR / "subgroup_metrics.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    table, best = run()
    table.to_csv(config.REPORTS_DIR / "subgroup_metrics.csv", index=False)
    plot(table)

    cols = ["subgroup", "n", "disease_rate", "roc_auc", "roc_auc_ci",
            "recall", "recall_ci", "specificity", "specificity_ci"]
    md = f"""# Subgroup Analysis (exploratory)

{EDU_DISCLAIMER}

> **Exploratory performance screen — not a calibrated fairness audit.** Metrics
> use **out-of-fold predictions across all
> {int(table.loc[table.subgroup=='Overall','n'].iloc[0])} patients** (each row scored by a model
> that never trained on it) from the **base (uncalibrated) pipeline** — fast,
> leakage-free, and focused on discrimination. Subgroups are small and the 95% CIs
> are wide, so apparent differences are usually within noise and must **not** be
> read as fairness or clinical conclusions.

Subgroup screen uses the **uncalibrated base {best} pipeline** for out-of-fold
discrimination analysis; the deployed model remains calibrated separately.
Threshold-based recall/specificity (at threshold {config.DEFAULT_THRESHOLD}) are
**exploratory**, not a calibrated fairness audit.

{table[cols].to_markdown(index=False)}

## How to read this
- Compare each subgroup's CI to the overall CI; heavy overlap means no reliable
  difference. With ~100–200 patients per subgroup, most gaps here are not
  distinguishable from noise.
- A real fairness audit needs far more data per subgroup and pre-registered
  metrics. This section demonstrates the *method and the honesty*, not a verdict.
- → `reports/figures/subgroup_metrics.png`.
"""
    write_report(config.REPORTS_DIR / "subgroup_report.md", md)
    print("Subgroup OOF metrics:")
    print(table[["subgroup", "n", "disease_rate", "roc_auc", "recall", "specificity"]].to_string(index=False))


if __name__ == "__main__":
    main()
