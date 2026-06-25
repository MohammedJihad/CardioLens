"""Decision Curve Analysis (net benefit).

Beyond discrimination/calibration, DCA asks the clinically meaningful question:
across a range of threshold probabilities, does *acting on the model* give more
net benefit than "treat everyone" or "treat no one"? Net benefit weighs true
positives against false positives by the odds implied by each threshold
(Vickers & Elkin, 2006).

Outputs: reports/figures/decision_curve.png, reports/decision_curve_report.md.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import config
from ._shared import load_test_predictions, write_report, EDU_DISCLAIMER


def net_benefit(y, proba, pt):
    """Net benefit of the model at threshold probability pt."""
    n = len(y)
    pred = (proba >= pt).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    if pt >= 1.0:
        return np.nan
    return tp / n - (fp / n) * (pt / (1 - pt))


def treat_all(y, pt):
    n = len(y); prev = float(np.mean(y))
    if pt >= 1.0:
        return np.nan
    return prev - (1 - prev) * (pt / (1 - pt))


def run(y_test, y_proba):
    pts = np.round(np.arange(0.05, 0.61, 0.05), 2)
    model = [net_benefit(np.asarray(y_test), np.asarray(y_proba), p) for p in pts]
    allnb = [treat_all(np.asarray(y_test), p) for p in pts]
    none = [0.0 for _ in pts]
    return pts, model, allnb, none


def plot(pts, model, allnb, none):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(pts, model, "o-", color="#d62728", label="Model")
    ax.plot(pts, allnb, "--", color="#1f77b4", label="Treat all")
    ax.plot(pts, none, "-", color="#7f7f7f", label="Treat none")
    ax.set_xlabel("Threshold probability"); ax.set_ylabel("Net benefit")
    ax.set_title("Decision curve analysis (test set)"); ax.legend()
    ax.set_ylim(min(-0.05, min(allnb)), max(model) + 0.05)
    fig.savefig(config.FIGURES_DIR / "decision_curve.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _, best, _, _, _, y_test, y_proba, _ = load_test_predictions()
    pts, model, allnb, none = run(y_test, y_proba)
    plot(pts, model, allnb, none)

    # Where does the model beat both reference strategies?
    beats = [p for p, m, a in zip(pts, model, allnb)
             if (m is not None and not np.isnan(m) and m >= a and m >= 0)]
    rng = (f"{min(beats):.2f}–{max(beats):.2f}" if beats else "none in the grid")
    rows = "\n".join(f"| {p:.2f} | {m:.3f} | {a:.3f} | 0.000 |"
                     for p, m, a in zip(pts, model, allnb))

    md = f"""# Decision Curve Analysis

{EDU_DISCLAIMER} _This is educational clinical-ML framing only — **not** clinical
validation._

Model: **{best}**, test set ({len(y_test)} patients). Net benefit compares acting
on the model against "treat all" and "treat none" across threshold probabilities.

| threshold prob. | model | treat-all | treat-none |
|---|---|---|---|
{rows}

**Reading it:** the model offers the highest net benefit over roughly
**{rng}** threshold probabilities. Where its curve sits above both reference
lines, using the model to decide is preferable to treating everyone or no one —
within this small test set and with all the usual caveats. This is a teaching
demonstration of net-benefit reasoning, not evidence of clinical usefulness.
"""
    write_report(config.REPORTS_DIR / "decision_curve_report.md", md)
    print(f"Decision curve: model beats reference strategies over {rng} threshold prob.")


if __name__ == "__main__":
    main()
