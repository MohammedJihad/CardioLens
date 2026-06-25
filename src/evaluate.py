"""Evaluation: the metric suite a medical screening project actually needs.

Accuracy alone is misleading on an imbalanced clinical problem, so we report
sensitivity/specificity, ROC-AUC, PR-AUC, a proper probability-based log loss,
Brier score, and a calibration curve — plus the confusion matrix that shows how
many sick patients were missed.
"""
from __future__ import annotations

import json

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score,
    brier_score_loss, confusion_matrix, f1_score, log_loss, precision_score,
    precision_recall_curve, recall_score, roc_auc_score, roc_curve,
)
from sklearn.calibration import calibration_curve

from . import config
from .data import load_processed
from .train import split


def specificity_score(y_true, y_pred) -> float:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn / (tn + fp) if (tn + fp) else 0.0


def compute_metrics(y_true, y_pred, y_proba) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall_sensitivity": recall_score(y_true, y_pred),
        "specificity": specificity_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_proba),
        "pr_auc": average_precision_score(y_true, y_proba),
        "log_loss": log_loss(y_true, y_proba),
        "brier_score": brier_score_loss(y_true, y_proba),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


# --------------------------------------------------------------------------- #
# Figures                                                                     #
# --------------------------------------------------------------------------- #
def _save(fig, name):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(config.FIGURES_DIR / name, dpi=130, bbox_inches="tight")
    plt.close(fig)


def plot_confusion(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    ax.imshow(cm, cmap="Blues")
    for (i, j), v in np.ndenumerate(cm):
        ax.text(j, i, str(v), ha="center", va="center",
                color="white" if v > cm.max() / 2 else "black", fontsize=13)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["No disease", "Disease"])
    ax.set_yticklabels(["No disease", "Disease"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title("Confusion matrix (test set)")
    _save(fig, "confusion_matrix.png")


def plot_roc_pr(y_true, y_proba):
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    prec, rec, _ = precision_recall_curve(y_true, y_proba)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].plot(fpr, tpr, color="#1f77b4")
    axes[0].plot([0, 1], [0, 1], "--", color="grey", lw=1)
    axes[0].set_title(f"ROC (AUC={roc_auc_score(y_true, y_proba):.3f})")
    axes[0].set_xlabel("1 - specificity"); axes[0].set_ylabel("Sensitivity")
    axes[1].plot(rec, prec, color="#d62728")
    axes[1].set_title(f"Precision-Recall (AP={average_precision_score(y_true, y_proba):.3f})")
    axes[1].set_xlabel("Recall"); axes[1].set_ylabel("Precision")
    _save(fig, "roc_pr_curves.png")


def plot_calibration(y_true, y_proba):
    frac_pos, mean_pred = calibration_curve(y_true, y_proba, n_bins=8, strategy="quantile")
    fig, ax = plt.subplots(figsize=(4.4, 4.0))
    ax.plot([0, 1], [0, 1], "--", color="grey", lw=1, label="Perfect")
    ax.plot(mean_pred, frac_pos, "o-", color="#2ca02c", label="Model")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed fraction positive")
    ax.set_title("Calibration curve")
    ax.legend()
    _save(fig, "calibration_curve.png")


def plot_model_comparison():
    path = config.REPORTS_DIR / "cv_results.json"
    if not path.exists():
        return
    cv = json.loads(path.read_text())
    names = list(cv.keys())
    auc = [cv[n]["roc_auc"]["mean"] for n in names]
    err = [cv[n]["roc_auc"]["std"] for n in names]
    order = np.argsort(auc)
    names = [names[i] for i in order]; auc = [auc[i] for i in order]; err = [err[i] for i in order]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.barh(names, auc, xerr=err, color="#4c72b0")
    ax.set_xlim(0.5, 1.0)
    ax.set_xlabel("CV ROC-AUC (mean +/- std)")
    ax.set_title("Model comparison")
    _save(fig, "model_comparison.png")


def main() -> None:
    bundle = joblib.load(config.MODEL_PATH)
    model, best = bundle["model"], bundle["best_name"]
    df = load_processed()
    _, X_test, _, y_test = split(df)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    metrics = compute_metrics(y_test, y_pred, y_proba)
    payload = {
        "best_model": best,
        "dataset": {"rows": int(df.shape[0]), "test_rows": int(len(y_test)),
                    "disease_rate": float(df[config.TARGET].mean())},
        "test_metrics": metrics,
    }
    config.METRICS_PATH.write_text(json.dumps(payload, indent=2))

    plot_confusion(y_test, y_pred)
    plot_roc_pr(y_test, y_proba)
    plot_calibration(y_test, y_proba)
    plot_model_comparison()

    print(f"Best model: {best}")
    for k, v in metrics.items():
        if k != "confusion_matrix":
            print(f"  {k:20s} {v:.3f}")
    cm = metrics["confusion_matrix"]
    print(f"  confusion: TP={cm['tp']} FN={cm['fn']} (missed sick) "
          f"TN={cm['tn']} FP={cm['fp']}")
    print(f"Saved metrics -> {config.METRICS_PATH}  | figures -> {config.FIGURES_DIR}")


if __name__ == "__main__":
    main()
