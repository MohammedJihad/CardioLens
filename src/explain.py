"""Explainability — global, model-based, and explicitly non-causal.

Two complementary global views (neither is a causal or medical claim):

* **Permutation importance** (model-agnostic) on the *deployed calibrated model*:
  how much test ROC-AUC drops when each raw feature is shuffled.
* **SHAP** (TreeExplainer) on the *uncalibrated* Random Forest pipeline. SHAP's
  TreeExplainer cannot run directly on `CalibratedClassifierCV` (it wraps several
  cross-fitted estimators plus a preprocessing step and exposes no single tree
  model), so SHAP on the uncalibrated Random Forest is a useful proxy for
  feature-usage patterns, but it is not an exact explanation of the calibrated
  ensemble's final probability. If SHAP is unavailable it is skipped and documented.

Outputs: reports/feature_importance.csv, reports/figures/permutation_importance.png,
reports/figures/shap_summary.png (if SHAP works), reports/explainability_report.md.
"""
from __future__ import annotations

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor
from .train import model_zoo, split
from ._shared import write_report, EDU_DISCLAIMER


def _save(fig, name):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(config.FIGURES_DIR / name, dpi=130, bbox_inches="tight")
    plt.close(fig)


def permutation_view(model, X_test, y_test) -> pd.DataFrame:
    r = permutation_importance(
        model, X_test, y_test, scoring="roc_auc",
        n_repeats=config.PERMUTATION_N_REPEATS,
        random_state=config.RANDOM_STATE, n_jobs=config.N_JOBS,
    )
    imp = (pd.DataFrame({"feature": config.FEATURES,
                         "importance": r.importances_mean,
                         "std": r.importances_std})
           .sort_values("importance", ascending=False).reset_index(drop=True))
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    top = imp.iloc[::-1]
    ax.barh([config.FEATURE_LABELS.get(f, f) for f in top["feature"]],
            top["importance"], xerr=top["std"], color="#8172b3")
    ax.set_xlabel("Drop in ROC-AUC when shuffled")
    ax.set_title("Permutation importance (global, deployed model)")
    _save(fig, "permutation_importance.png")
    return imp


def shap_global(df) -> tuple[bool, str]:
    """SHAP summary on the uncalibrated RF pipeline. Returns (ok, note)."""
    try:
        import shap
    except Exception as e:  # pragma: no cover
        return False, f"SHAP not installed ({e}); skipped. Permutation importance still provided."
    try:
        X_train, X_test, y_train, _ = split(df)
        pre = build_preprocessor()
        Xtr = pre.fit_transform(X_train)
        Xte = pre.transform(X_test)
        names = list(pre.get_feature_names_out())
        rf = model_zoo()["Random Forest"]
        rf.fit(Xtr, y_train)

        sv = shap.TreeExplainer(rf).shap_values(Xte)
        if isinstance(sv, list):                 # [class0, class1]
            sv_pos = sv[1]
        elif getattr(sv, "ndim", 2) == 3:        # (n, features, classes)
            sv_pos = sv[:, :, 1]
        else:
            sv_pos = sv

        fig = plt.figure()
        shap.summary_plot(sv_pos, Xte, feature_names=names, show=False, max_display=12)
        _save(plt.gcf(), "shap_summary.png")

        mean_abs = np.abs(sv_pos).mean(axis=0)
        order = np.argsort(mean_abs)[::-1][:6]
        top = ", ".join(f"{names[i]} ({mean_abs[i]:.3f})" for i in order)
        return True, f"SHAP TreeExplainer on the uncalibrated RF. Top mean|SHAP|: {top}."
    except Exception as e:  # pragma: no cover
        return False, f"SHAP attempted but failed ({type(e).__name__}: {e}); skipped. Permutation importance still provided."


def main() -> None:
    bundle = joblib.load(config.MODEL_PATH)
    model, best = bundle["model"], bundle["best_name"]
    df = load_processed()
    _, X_test, _, y_test = split(df)

    imp = permutation_view(model, X_test, y_test)
    imp.to_csv(config.REPORTS_DIR / "feature_importance.csv", index=False)
    shap_ok, shap_note = shap_global(df)

    perm_top = "\n".join(
        f"| {config.FEATURE_LABELS.get(r.feature, r.feature)} | {r.importance:.3f} | {r['std']:.3f} |"
        for _, r in imp.head(8).iterrows())

    md = f"""# Explainability Report

{EDU_DISCLAIMER} _Explanations describe **how the model uses features**; they are
**not causal** and **not medical advice**._

Model: **{best}** (calibrated).

## Global — permutation importance (model-agnostic, deployed model)
How much held-out ROC-AUC drops when each raw feature is randomly shuffled.

| feature | importance | std |
|---|---|---|
{perm_top}

→ `reports/figures/permutation_importance.png`, `reports/feature_importance.csv`.

## Global — SHAP
{shap_note}

{"→ `reports/figures/shap_summary.png`." if shap_ok else ""}

**Why SHAP runs on the uncalibrated RF:** `shap.TreeExplainer` needs a single
tree model. The deployed estimator is a `CalibratedClassifierCV` wrapping several
cross-fitted RF pipelines, which TreeExplainer cannot read directly. SHAP on the uncalibrated Random Forest is a useful proxy for
feature-usage patterns, but it is not an exact explanation of the calibrated
ensemble's final probability.

## Local explanations
Per-patient explanations are produced by `src/patient_report.py` using a
marginal-contribution method on the **deployed** model (so they match the score a
user sees). See that module and `reports/sample_patient_report.md`.

## What these are and are not
- Global permutation importance reflects predictive usefulness, **not causation**.
- SHAP attributes the model's output to features for the RF model only.
- None of this is clinical evidence or advice; the dataset is small and historical.
"""
    write_report(config.REPORTS_DIR / "explainability_report.md", md)
    print("Top permutation features:")
    print(imp.head(8).to_string(index=False))
    print(f"SHAP: {'OK -> shap_summary.png' if shap_ok else 'skipped'} | {shap_note}")


if __name__ == "__main__":
    main()
