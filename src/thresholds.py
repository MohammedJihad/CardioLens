"""Threshold analysis with LEAKAGE-FREE selection.

Two clearly separated things:

1. **Selection (training only).** The operating threshold is chosen on
   out-of-fold (OOF) probabilities of the *training* split — the test labels are
   never used to pick it. We minimise a cost that weights a false negative
   COST_FN x a false positive (screening priority).

2. **Held-out test sensitivity analysis.** We still sweep thresholds on the test
   set for transparency, but this is a *post-hoc sensitivity table*, NOT the
   basis for the recommendation. The selected threshold is evaluated on the test
   set exactly once.

Outputs:
  reports/threshold_selection_train_oof.csv   (OOF sweep used for selection)
  reports/threshold_metrics.csv               (held-out test sensitivity sweep)
  reports/threshold_test_evaluation.csv       (selected threshold, test metrics)
  reports/figures/threshold_plot.png
  reports/threshold_report.md
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score,
    precision_score, recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

from . import config
from .preprocessing import build_preprocessor
from .train import model_zoo
from ._shared import load_test_predictions, write_report, EDU_DISCLAIMER


def threshold_table(y, proba, grid=None) -> pd.DataFrame:
    """Confusion-based metrics at each threshold in `grid` (default config grid)."""
    grid = config.THRESHOLD_GRID if grid is None else grid
    y = pd.Series(list(y))
    rows = []
    for t in grid:
        y_pred = (pd.Series(list(proba)) >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y, y_pred, labels=[0, 1]).ravel()
        sens = recall_score(y, y_pred, zero_division=0)
        spec = tn / (tn + fp) if (tn + fp) else 0.0
        rows.append({
            "threshold": t, "TP": int(tp), "FP": int(fp), "TN": int(tn), "FN": int(fn),
            "sensitivity_recall": round(sens, 3),
            "specificity": round(spec, 3),
            "precision": round(precision_score(y, y_pred, zero_division=0), 3),
            "f1": round(f1_score(y, y_pred, zero_division=0), 3),
            "accuracy": round(accuracy_score(y, y_pred), 3),
            "balanced_accuracy": round(balanced_accuracy_score(y, y_pred), 3),
            "cost": int(config.COST_FN * fn + config.COST_FP * fp),
        })
    return pd.DataFrame(rows)


def _fresh_estimator(best_name):
    """Unfitted copy of the deployed calibrated estimator (for OOF prediction)."""
    base = Pipeline([("prep", build_preprocessor()), ("clf", model_zoo()[best_name])])
    return CalibratedClassifierCV(base, method=config.CALIBRATION_METHOD, cv=config.CV_FOLDS)


def select_threshold_oof(X_train, y_train, best_name):
    """Cost-minimising threshold chosen on TRAINING out-of-fold probabilities."""
    cv = StratifiedKFold(config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE)
    oof = cross_val_predict(_fresh_estimator(best_name), X_train, y_train,
                            cv=cv, method="predict_proba", n_jobs=config.N_JOBS)[:, 1]
    table = threshold_table(y_train, oof)
    selected = float(table.loc[table["cost"].idxmin(), "threshold"])
    return selected, table


def plot(test_df: pd.DataFrame, selected: float) -> None:
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(6.6, 4.2))
    ax1.plot(test_df["threshold"], test_df["sensitivity_recall"], "o-", color="#d62728", label="Sensitivity")
    ax1.plot(test_df["threshold"], test_df["specificity"], "o-", color="#1f77b4", label="Specificity")
    ax1.plot(test_df["threshold"], test_df["f1"], "o--", color="#2ca02c", label="F1")
    ax1.axvline(selected, color="black", ls=":", lw=1.5, label=f"Selected (train-OOF) = {selected:.2f}")
    ax1.set_xlabel("Decision threshold"); ax1.set_ylabel("Metric value (held-out test)")
    ax1.set_ylim(0, 1.02); ax1.legend(loc="lower left", fontsize=8)
    ax1.set_title("Held-out test sensitivity vs threshold\n(threshold selected on training OOF, marked)")
    fig.savefig(config.FIGURES_DIR / "threshold_plot.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _, best, X_train, _, y_train, y_test, y_proba, _ = load_test_predictions()

    # 1) Select on training OOF only (no test labels used).
    selected, oof_table = select_threshold_oof(X_train, y_train, best)
    oof_table.to_csv(config.REPORTS_DIR / "threshold_selection_train_oof.csv", index=False)

    # 2) Held-out test sensitivity sweep (post-hoc, transparency only).
    test_table = threshold_table(y_test, y_proba)
    test_table.to_csv(config.REPORTS_DIR / "threshold_metrics.csv", index=False)
    plot(test_table, selected)

    # 3) Evaluate the SELECTED threshold once on the test set.
    test_eval = threshold_table(y_test, y_proba, grid=[selected])
    test_eval.to_csv(config.REPORTS_DIR / "threshold_test_evaluation.csv", index=False)
    row = test_eval.iloc[0]
    default_row = threshold_table(y_test, y_proba, grid=[config.DEFAULT_THRESHOLD]).iloc[0]

    md = f"""# Threshold Analysis

{EDU_DISCLAIMER}

Model: **{best}** (calibrated). The 0.5 cut-off is only a default — not a clinical
decision threshold.

## Operating threshold — selected WITHOUT test labels
The threshold is chosen on **training out-of-fold predictions** (5-fold), by
minimising `cost = {config.COST_FN}·FN + {config.COST_FP}·FP` (a false negative
weighted {config.COST_FN}× a false positive). The test set is **not** used for
selection, which avoids the optimistic bias of tuning a policy on test labels.

- **Selected threshold (from training OOF): {selected:.2f}**
- Selection sweep: `reports/threshold_selection_train_oof.csv`

### Held-out test performance AT the selected threshold (evaluated once)

| threshold | sensitivity | specificity | precision | F1 | FN | FP |
|---|---|---|---|---|---|---|
| {selected:.2f} (selected) | {row['sensitivity_recall']} | {row['specificity']} | {row['precision']} | {row['f1']} | {int(row['FN'])} | {int(row['FP'])} |
| {config.DEFAULT_THRESHOLD:.2f} (default) | {default_row['sensitivity_recall']} | {default_row['specificity']} | {default_row['precision']} | {default_row['f1']} | {int(default_row['FN'])} | {int(default_row['FP'])} |

## Held-out test sensitivity analysis (post-hoc, NOT used to choose the threshold)
The table below shows how metrics move with the threshold on the test set. It is
provided for transparency; the operating threshold above was **not** picked from
it.

{test_table.to_markdown(index=False)}

Lowering the threshold raises sensitivity (catches more sick patients) at the
cost of specificity. The cost weights ({config.COST_FN}:{config.COST_FP}) are
illustrative, not clinically derived; a real deployment would set them with
clinicians.
"""
    write_report(config.REPORTS_DIR / "threshold_report.md", md)
    print(f"Selected threshold (training OOF only): {selected:.2f}")
    print(f"  -> held-out test: sensitivity={row['sensitivity_recall']} "
          f"specificity={row['specificity']} FN={int(row['FN'])} FP={int(row['FP'])}")


if __name__ == "__main__":
    main()
