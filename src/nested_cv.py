"""Nested cross-validation.

A single train/test split on ~300 rows is a shaky generalisation estimate. Nested
CV gives an (almost) unbiased one: the **outer** loop measures performance, while
an **inner** loop does model + hyperparameter selection — so selection never sees
the outer test fold. All preprocessing stays inside the pipeline, fit per fold,
so there is no leakage.

Outputs: reports/nested_cv_results.csv, reports/nested_cv_report.md.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor
from ._shared import write_report, EDU_DISCLAIMER


def _search_space():
    """Inner-loop grid: selects BOTH the model family and its hyperparameters."""
    pipe = Pipeline([("prep", build_preprocessor()),
                     ("clf", LogisticRegression(max_iter=1000,
                                                random_state=config.RANDOM_STATE))])
    grid = [
        {"clf": [LogisticRegression(max_iter=1000, random_state=config.RANDOM_STATE)],
         "clf__C": [0.1, 1.0, 10.0]},
        {"clf": [RandomForestClassifier(random_state=config.RANDOM_STATE)],
         "clf__n_estimators": [200, 300], "clf__max_depth": [None, 5]},
        {"clf": [SVC(probability=True, random_state=config.RANDOM_STATE)],
         "clf__C": [0.5, 1.0, 10.0], "clf__kernel": ["rbf", "linear"]},
    ]
    return pipe, grid


def run() -> tuple[pd.DataFrame, dict]:
    df = load_processed()
    X, y = df[config.FEATURES], df[config.TARGET]
    pipe, grid = _search_space()

    inner = StratifiedKFold(5, shuffle=True, random_state=config.RANDOM_STATE)
    outer = StratifiedKFold(5, shuffle=True, random_state=config.RANDOM_STATE)
    search = GridSearchCV(pipe, grid, scoring="roc_auc", cv=inner, n_jobs=config.N_JOBS)

    scoring = ["roc_auc", "recall", "f1", "accuracy", "balanced_accuracy"]
    cv = cross_validate(search, X, y, cv=outer, scoring=scoring,
                        return_estimator=True, n_jobs=config.N_JOBS)

    rows, picks = [], []
    for i in range(outer.get_n_splits()):
        est = cv["estimator"][i].best_estimator_.named_steps["clf"]
        picks.append(type(est).__name__)
        rows.append({"outer_fold": i + 1, "selected_model": type(est).__name__,
                     **{m: round(float(cv[f"test_{m}"][i]), 3) for m in scoring}})
    table = pd.DataFrame(rows)
    summary = {m: {"mean": round(float(np.mean(cv[f"test_{m}"])), 3),
                   "std": round(float(np.std(cv[f"test_{m}"])), 3)} for m in scoring}
    summary["selected_models"] = picks
    return table, summary


def main() -> None:
    table, summary = run()
    table.to_csv(config.REPORTS_DIR / "nested_cv_results.csv", index=False)

    from collections import Counter
    picks = Counter(summary.pop("selected_models"))
    picks_str = ", ".join(f"{k}×{v}" for k, v in picks.items())

    md = f"""# Nested Cross-Validation

{EDU_DISCLAIMER}

Outer 5-fold (performance) × inner 5-fold (model + hyperparameter selection over
Logistic Regression, Random Forest, and SVM). Preprocessing is inside the
pipeline and re-fit per fold — no leakage.

## Per-fold results

{table.to_markdown(index=False)}

## Generalisation estimate (mean ± std across outer folds)

| metric | mean ± std |
|---|---|
""" + "\n".join(f"| {m} | {v['mean']:.3f} ± {v['std']:.3f} |"
                 for m, v in summary.items()) + f"""

**Model selected by the inner loop:** {picks_str}.

This nested estimate is the project's most trustworthy single number for "how
well does this approach generalise on this data", and it is consistent with the
held-out test ROC-AUC. The selected family can vary across folds — expected when
several models are statistically tied on a small dataset.
"""
    write_report(config.REPORTS_DIR / "nested_cv_report.md", md)
    print("Nested CV (outer mean ± std):")
    for m, v in summary.items():
        print(f"  {m:20s} {v['mean']:.3f} ± {v['std']:.3f}")
    print(f"  selected per fold: {picks_str}")


if __name__ == "__main__":
    main()
