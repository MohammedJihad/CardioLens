"""Bootstrap confidence intervals.

A 61-row test set makes any single point metric uncertain. We resample the test
predictions with replacement (BOOTSTRAP_N times) and report 95% percentile
intervals — turning "ROC-AUC 0.89" into "0.89 [0.80, 0.96]", which is the honest
way to present small-sample performance.

Outputs: reports/uncertainty_metrics.json, reports/uncertainty_report.md.
"""
from __future__ import annotations

import json

import numpy as np
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score,
    brier_score_loss, confusion_matrix, f1_score, log_loss, precision_score,
    recall_score, roc_auc_score,
)

from . import config
from ._shared import load_test_predictions, write_report, EDU_DISCLAIMER


def _specificity(y, p):
    tn, fp, fn, tp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    return tn / (tn + fp) if (tn + fp) else np.nan


def _metrics(y, proba, thr=config.DEFAULT_THRESHOLD) -> dict:
    pred = (proba >= thr).astype(int)
    out = {
        "accuracy": accuracy_score(y, pred),
        "balanced_accuracy": balanced_accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall_sensitivity": recall_score(y, pred, zero_division=0),
        "specificity": _specificity(y, pred),
        "f1": f1_score(y, pred, zero_division=0),
        "brier_score": brier_score_loss(y, proba),
        "log_loss": log_loss(y, proba, labels=[0, 1]),
    }
    # AUC-style metrics need both classes present in the resample.
    if len(np.unique(y)) == 2:
        out["roc_auc"] = roc_auc_score(y, proba)
        out["pr_auc"] = average_precision_score(y, proba)
    else:
        out["roc_auc"] = np.nan
        out["pr_auc"] = np.nan
    return out


def bootstrap(y_test, y_proba, n=config.BOOTSTRAP_N, seed=config.RANDOM_STATE):
    y_test = np.asarray(y_test); y_proba = np.asarray(y_proba)
    rng = np.random.default_rng(seed)
    point = _metrics(y_test, y_proba)
    samples = {k: [] for k in point}
    idx = np.arange(len(y_test))
    for _ in range(n):
        b = rng.choice(idx, size=len(idx), replace=True)
        m = _metrics(y_test[b], y_proba[b])
        for k, v in m.items():
            samples[k].append(v)
    result = {}
    for k, vals in samples.items():
        arr = np.array(vals, dtype=float)
        arr = arr[~np.isnan(arr)]
        result[k] = {
            "point": round(float(point[k]), 4) if not np.isnan(point[k]) else None,
            "ci_low": round(float(np.percentile(arr, 2.5)), 4) if arr.size else None,
            "ci_high": round(float(np.percentile(arr, 97.5)), 4) if arr.size else None,
            "n_valid": int(arr.size),
        }
    return result


def main() -> None:
    _, best, _, _, _, y_test, y_proba, _ = load_test_predictions()
    res = bootstrap(y_test, y_proba)
    payload = {"best_model": best, "n_test": int(len(y_test)),
               "n_bootstrap": config.BOOTSTRAP_N, "metrics": res}
    (config.REPORTS_DIR / "uncertainty_metrics.json").write_text(json.dumps(payload, indent=2))

    lines = ["| metric | point | 95% CI |", "|---|---|---|"]
    for k, v in res.items():
        if v["point"] is None:
            lines.append(f"| {k} | n/a | n/a |")
        else:
            lines.append(f"| {k} | {v['point']:.3f} | [{v['ci_low']:.3f}, {v['ci_high']:.3f}] |")
    table = "\n".join(lines)

    md = f"""# Bootstrap Confidence Intervals

{EDU_DISCLAIMER}

Model: **{best}**. Test set: **{len(y_test)} patients**.
Method: {config.BOOTSTRAP_N} bootstrap resamples (with replacement) of the test
predictions; 95% percentile intervals at the default {config.DEFAULT_THRESHOLD}
threshold.

{table}

**Reading these honestly:** the test set is small, so several intervals are wide
— the point estimates should not be over-trusted. ROC-AUC / PR-AUC intervals skip
the rare resamples that contain only one class. This is exactly why the project
also reports nested cross-validation (a less variance-prone generalisation
estimate) alongside this held-out evaluation.
"""
    write_report(config.REPORTS_DIR / "uncertainty_report.md", md)
    print(f"Bootstrap CIs ({config.BOOTSTRAP_N} resamples), model={best}:")
    for k, v in res.items():
        if v["point"] is not None:
            print(f"  {k:20s} {v['point']:.3f}  [{v['ci_low']:.3f}, {v['ci_high']:.3f}]")


if __name__ == "__main__":
    main()
