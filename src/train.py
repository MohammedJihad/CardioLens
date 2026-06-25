"""Model comparison, selection, and persistence.

Compares a baseline plus four real models by default (Logistic Regression, SVM,
MLP, Random Forest), with HistGradientBoosting available opt-in
(config.INCLUDE_HISTGB). Selects the best by mean ROC-AUC under stratified k-fold
CV (with recall reported alongside, since missing a sick patient is the costly
error here), refits it on the full training split, applies probability
calibration, and saves the fitted pipeline to models/.
"""
from __future__ import annotations

import json

import joblib
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from . import config
from .data import load_processed
from .preprocessing import build_preprocessor


def model_zoo() -> dict[str, object]:
    """The estimators we compare. Each is wrapped with the shared preprocessor.

    HistGradientBoosting is opt-in (config.INCLUDE_HISTGB) because its internal
    OpenMP threading can hang on constrained environments; when enabled it is
    configured for deterministic, fast runs on small data.
    """
    rs = config.RANDOM_STATE
    zoo = {
        "Dummy (most_frequent)": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=rs),
        "SVM (RBF)": SVC(probability=True, random_state=rs),
        "MLP": MLPClassifier(max_iter=1000, random_state=rs),
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=rs),
    }
    if config.INCLUDE_HISTGB:
        zoo["HistGradientBoosting"] = HistGradientBoostingClassifier(
            max_iter=100, early_stopping=False, random_state=rs
        )
    return zoo


def _pipe(estimator) -> Pipeline:
    return Pipeline([("prep", build_preprocessor()), ("clf", estimator)])


def split(df):
    X = df[config.FEATURES]
    y = df[config.TARGET]
    return train_test_split(
        X, y, test_size=config.TEST_SIZE,
        stratify=y, random_state=config.RANDOM_STATE,
    )


def cross_validate_models(X_train, y_train) -> dict[str, dict]:
    """Stratified k-fold CV for every model; returns mean/std of key metrics."""
    cv = StratifiedKFold(n_splits=config.CV_FOLDS, shuffle=True,
                         random_state=config.RANDOM_STATE)
    scoring = ["roc_auc", "recall", "f1", "accuracy", "balanced_accuracy"]
    results: dict[str, dict] = {}
    for name, est in model_zoo().items():
        scores = cross_validate(_pipe(est), X_train, y_train, cv=cv,
                                scoring=scoring, n_jobs=config.N_JOBS)
        results[name] = {
            m: {"mean": float(np.mean(scores[f"test_{m}"])),
                "std": float(np.std(scores[f"test_{m}"]))}
            for m in scoring
        }
    return results


def select_best(cv_results: dict[str, dict]) -> str:
    """Best model = highest mean CV ROC-AUC, ignoring the dummy baseline."""
    candidates = {k: v for k, v in cv_results.items() if not k.startswith("Dummy")}
    return max(candidates, key=lambda k: candidates[k]["roc_auc"]["mean"])


def fit_final(name: str, X_train, y_train) -> Pipeline:
    """Refit the chosen model on all training data, with probability calibration.

    Calibration matters in a medical context: we want the predicted probability
    to be readable as a probability estimate (model score), not just an ordering. It is applied to
    every model uniformly via an internal CV on the training split.
    """
    base = _pipe(model_zoo()[name])
    calibrated = CalibratedClassifierCV(base, method="isotonic", cv=config.CV_FOLDS)
    calibrated.fit(X_train, y_train)
    return calibrated


def main() -> None:
    df = load_processed()
    X_train, X_test, y_train, y_test = split(df)

    print(f"Train: {len(X_train)}  Test: {len(X_test)}  "
          f"(disease rate train={y_train.mean():.2%})")

    cv_results = cross_validate_models(X_train, y_train)
    print("\nCross-validated ROC-AUC (mean +/- std):")
    for name, r in cv_results.items():
        print(f"  {name:24s} AUC={r['roc_auc']['mean']:.3f}"
              f"+/-{r['roc_auc']['std']:.3f}  recall={r['recall']['mean']:.3f}")

    best = select_best(cv_results)
    print(f"\nSelected best model: {best}")

    final = fit_final(best, X_train, y_train)
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": final, "best_name": best, "features": config.FEATURES},
        config.MODEL_PATH,
    )
    print(f"Saved calibrated model -> {config.MODEL_PATH}")

    # Stash CV table + the split for the evaluation step.
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (config.REPORTS_DIR / "cv_results.json").write_text(json.dumps(cv_results, indent=2))


if __name__ == "__main__":
    main()
