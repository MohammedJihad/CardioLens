"""Learning curve.

Plots cross-validated ROC-AUC as a function of training-set size to show whether
the model is data-limited (validation score still rising → more data would help)
or capacity-limited. On ~300 rows this directly visualises the project's central
limitation.

Outputs: reports/figures/learning_curve.png, reports/learning_curve_report.md.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedKFold, learning_curve
from sklearn.pipeline import Pipeline

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor
from .train import model_zoo
from ._shared import write_report, EDU_DISCLAIMER

BASE_MODEL = "Random Forest"


def run():
    df = load_processed()
    X, y = df[config.FEATURES], df[config.TARGET]
    pipe = Pipeline([("prep", build_preprocessor()), ("clf", model_zoo()[BASE_MODEL])])
    cv = StratifiedKFold(5, shuffle=True, random_state=config.RANDOM_STATE)
    sizes, train_scores, val_scores = learning_curve(
        pipe, X, y, cv=cv, scoring="roc_auc",
        train_sizes=np.linspace(0.2, 1.0, 6), n_jobs=config.N_JOBS,
        random_state=config.RANDOM_STATE, shuffle=True,
    )
    return sizes, train_scores.mean(1), train_scores.std(1), val_scores.mean(1), val_scores.std(1)


def plot(sizes, tr_m, tr_s, va_m, va_s):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(sizes, tr_m, "o-", color="#1f77b4", label="Training")
    ax.fill_between(sizes, tr_m - tr_s, tr_m + tr_s, alpha=0.15, color="#1f77b4")
    ax.plot(sizes, va_m, "o-", color="#d62728", label="Validation (CV)")
    ax.fill_between(sizes, va_m - va_s, va_m + va_s, alpha=0.15, color="#d62728")
    ax.set_xlabel("Training set size"); ax.set_ylabel("ROC-AUC")
    ax.set_title("Learning curve"); ax.legend(loc="lower right")
    fig.savefig(config.FIGURES_DIR / "learning_curve.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    sizes, tr_m, tr_s, va_m, va_s = run()
    plot(sizes, tr_m, tr_s, va_m, va_s)

    last_slope = va_m[-1] - va_m[-2]
    gap = tr_m[-1] - va_m[-1]
    rising = "still rising" if last_slope > 0.005 else "roughly flat"
    verdict = ("more training data would likely help (validation score is "
               "still climbing at the largest size)"
               if last_slope > 0.005 else
               "returns from more data look modest (validation score has largely "
               "plateaued); the train–validation gap points more to model variance")

    rows = "\n".join(f"| {int(s)} | {tm:.3f} | {vm:.3f} |"
                     for s, tm, vm in zip(sizes, tr_m, va_m))
    md = f"""# Learning Curve

{EDU_DISCLAIMER}

Model: **{BASE_MODEL}**, 5-fold CV ROC-AUC vs training-set size.

| train size | training AUC | validation AUC |
|---|---|---|
{rows}

At the largest size the validation curve is **{rising}**
(last-step change {last_slope:+.3f}) with a train–validation gap of {gap:.3f}.

**Interpretation:** {verdict}. Either way, the dataset's small size (~300 rows) is
the binding constraint — the strongest realistic improvement is *more / external
data*, which is exactly why external validation is planned as a later phase.
"""
    write_report(config.REPORTS_DIR / "learning_curve_report.md", md)
    print(f"Learning curve: val AUC {va_m[0]:.3f} -> {va_m[-1]:.3f}, "
          f"last-step {last_slope:+.3f}, gap {gap:.3f}")


if __name__ == "__main__":
    main()
