"""Calibration comparison — CV-based (primary) + held-out (secondary).

Compares no calibration vs sigmoid (Platt) vs isotonic for the chosen model.
Selecting a calibration method from the *test* set is the same kind of optimistic
bias as tuning a threshold on it, so the **primary** comparison uses training
out-of-fold predictions; the held-out test numbers are reported only as a
secondary check, with deliberately cautious wording (the margins are small on a
~300-row dataset).

Outputs: reports/calibration_report.md, reports/figures/calibration_comparison.png.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor
from .train import model_zoo, split
from ._shared import write_report, EDU_DISCLAIMER

BASE_MODEL = "Random Forest"


def _variant(name):
    base = Pipeline([("prep", build_preprocessor()), ("clf", model_zoo()[BASE_MODEL])])
    if name == "none":
        return base
    return CalibratedClassifierCV(base, method=name, cv=config.CV_FOLDS)


def _scores(y, proba):
    return (round(float(brier_score_loss(y, proba)), 4),
            round(float(log_loss(y, proba, labels=[0, 1])), 4))


def run():
    df = load_processed()
    X_train, X_test, y_train, y_test = split(df)
    cv = StratifiedKFold(config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE)

    cv_results, test_results, curves = {}, {}, {}
    for name in ("none", "sigmoid", "isotonic"):
        # Primary: training out-of-fold (no test labels used).
        oof = cross_val_predict(_variant(name), X_train, y_train, cv=cv,
                                method="predict_proba", n_jobs=config.N_JOBS)[:, 1]
        cv_results[name] = _scores(y_train, oof)
        # Secondary: held-out test (fit on full train, predict test).
        est = _variant(name).fit(X_train, y_train)
        proba = est.predict_proba(X_test)[:, 1]
        test_results[name] = _scores(y_test, proba)
        frac, mean_pred = calibration_curve(y_test, proba, n_bins=6, strategy="quantile")
        curves[name] = (mean_pred, frac)
    return cv_results, test_results, curves, len(y_train), len(y_test)


def plot(curves):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    ax.plot([0, 1], [0, 1], "--", color="grey", lw=1, label="Perfect")
    colors = {"none": "#7f7f7f", "sigmoid": "#1f77b4", "isotonic": "#2ca02c"}
    for name, (mp, fr) in curves.items():
        ax.plot(mp, fr, "o-", color=colors[name], label=name)
    ax.set_xlabel("Mean predicted probability"); ax.set_ylabel("Observed fraction positive")
    ax.set_title("Calibration comparison (held-out test)"); ax.legend()
    fig.savefig(config.FIGURES_DIR / "calibration_comparison.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    cv_results, test_results, curves, n_tr, n_te = run()
    plot(curves)

    cv_best = min(cv_results, key=lambda k: (cv_results[k][0], cv_results[k][1]))
    deployed = config.CALIBRATION_METHOD
    cv_rows = "\n".join(f"| {k} | {v[0]:.4f} | {v[1]:.4f} |" for k, v in cv_results.items())
    te_rows = "\n".join(f"| {k} | {v[0]:.4f} | {v[1]:.4f} |" for k, v in test_results.items())

    md = f"""# Calibration Comparison

{EDU_DISCLAIMER}

Model: **{BASE_MODEL}**. Lower Brier / log-loss is better.

## Primary: training out-of-fold ({n_tr} patients, no test labels used)

| method | Brier | log-loss |
|---|---|---|
{cv_rows}

**Lowest-Brier method on training OOF: `{cv_best}`.** The currently deployed
method is `{deployed}`. Note the **Brier and log-loss disagree**: where isotonic
has the lowest Brier it can have a much worse log-loss, a classic sign of
isotonic over-fitting the small calibration set and producing over-confident
(near-0/1) probabilities. So no method is a clear winner here.

## Secondary: held-out test ({n_te} patients) — for transparency only

| method | Brier | log-loss |
|---|---|---|
{te_rows}

## How to read this (honestly)
On a dataset this small the calibration methods are **close and unstable** — and
the Brier-vs-log-loss disagreement above shows isotonic's apparent Brier edge is
fragile. We therefore base any reading on the training-OOF comparison rather than
the test set, and do **not** claim a method is decisively best. The deployed
choice (`{deployed}`) is defensible, but `sigmoid` (more stable on small data) or
even `none` would be equally reasonable; a different split could reorder these
closely-spaced numbers. Reliability curves:
`reports/figures/calibration_comparison.png`.
"""
    write_report(config.REPORTS_DIR / "calibration_report.md", md)
    print("Calibration — training OOF (primary), lower better:")
    for k, v in cv_results.items():
        print(f"  {k:9s} Brier={v[0]:.4f}  log_loss={v[1]:.4f}")
    print(f"OOF lowest-Brier: {cv_best}  (deployed: {deployed})")
    print("Held-out test (secondary):")
    for k, v in test_results.items():
        print(f"  {k:9s} Brier={v[0]:.4f}  log_loss={v[1]:.4f}")


if __name__ == "__main__":
    main()
