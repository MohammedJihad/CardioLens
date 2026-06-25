"""Error analysis on the held-out test set.

Looks at *which* patients the model gets wrong — false negatives (missed sick)
and false positives (false alarms) — and compares their feature profiles to the
cohort. Strictly descriptive: no medical advice, and explicitly cautious because
the test set is tiny.

Outputs: reports/error_analysis.md.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config
from ._shared import load_test_predictions, write_report, EDU_DISCLAIMER

# Features worth profiling (clinically interpretable).
PROFILE = ["age", "thalach", "oldpeak", "ca", "cp", "thal", "exang", "trestbps", "chol"]


def main() -> None:
    _, best, _, X_test, _, y_test, y_proba, df = load_test_predictions()
    X = X_test.copy().reset_index(drop=True)
    y = np.asarray(y_test)
    proba = np.asarray(y_proba)
    pred = (proba >= config.DEFAULT_THRESHOLD).astype(int)

    fn_mask = (pred == 0) & (y == 1)
    fp_mask = (pred == 1) & (y == 0)
    correct = pred == y

    cohort_mean = X[PROFILE].mean()

    def profile(mask):
        if mask.sum() == 0:
            return None
        return X.loc[mask, PROFILE].mean()

    fn_prof, fp_prof = profile(fn_mask), profile(fp_mask)

    def cmp_table(prof):
        lines = ["| feature | cohort mean | group mean |", "|---|---|---|"]
        for f in PROFILE:
            lines.append(f"| {f} | {cohort_mean[f]:.1f} | {prof[f]:.1f} |")
        return "\n".join(lines)

    fn_block = (cmp_table(fn_prof) if fn_prof is not None else "_No false negatives._")
    fp_block = (cmp_table(fp_prof) if fp_prof is not None else "_No false positives._")

    # Probabilities of the FNs — were they borderline or confident misses?
    fn_probs = sorted(round(float(p), 2) for p in proba[fn_mask])
    thr = config.DEFAULT_THRESHOLD
    borderline = [p for p in fn_probs if p >= thr - 0.1]      # within 0.1 below 0.5
    lower_conf = [p for p in fn_probs if p < thr - 0.1]

    md = f"""# Error Analysis

{EDU_DISCLAIMER}

Model: **{best}**, threshold {config.DEFAULT_THRESHOLD}. Test set:
**{len(y)} patients** — {int(fn_mask.sum())} false negatives (missed sick),
{int(fp_mask.sum())} false positives (false alarms), {int(correct.sum())} correct.

> **Caution:** with so few errors, these are *descriptive observations on a tiny
> sample*, not reliable patterns. They are not medical advice.

## False negatives (missed sick) vs cohort
Model scores of the missed patients: {fn_probs if fn_probs else "—"}.
**Some false negatives are borderline near {thr} ({borderline if borderline else "none"}),
while others are lower-confidence misses ({lower_conf if lower_conf else "none"}).**
Lowering the threshold (see the threshold report) would recover the borderline
ones, but not necessarily the lower-confidence misses.

{fn_block}

## False positives (false alarms) vs cohort

{fp_block}

## Takeaways (tentative)
- The misses split between near-boundary cases and lower-confidence ones; a
  cost-sensitive lower threshold helps mainly with the former.
- Any feature direction noted above is a hypothesis to revisit with more data,
  not a finding. The sample is too small to conclude anything clinical.
"""
    write_report(config.REPORTS_DIR / "error_analysis.md", md)
    print(f"Error analysis: {int(fn_mask.sum())} FN, {int(fp_mask.sum())} FP "
          f"(test n={len(y)}). FN model scores: {fn_probs}")


if __name__ == "__main__":
    main()
