"""Central configuration: paths, column schema, and modelling constants.

Keeping every path and column list in one place is what makes the rest of the
pipeline reproducible — nothing downstream hard-codes a filename or a feature.
"""
from __future__ import annotations

from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths (resolved relative to the repo root so the project runs from anywhere) #
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = ROOT / "data" / "raw" / "heart_cleveland.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "heart_processed.csv"

MODELS_DIR = ROOT / "models"
MODEL_PATH = MODELS_DIR / "best_model.joblib"

REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_PATH = REPORTS_DIR / "metrics.json"

# --------------------------------------------------------------------------- #
# Column schema                                                               #
# --------------------------------------------------------------------------- #
# Raw column names as they appear in the UCI Cleveland CSV.
RAW_TARGET = "target"          # 1 = NO disease, 0 = disease in this CSV (see data/README.md)
TARGET = "heart_disease"       # our modelling target: 1 = disease present, 0 = absent

# Features split by how they must be pre-processed.
NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Human-readable labels (used in figures / the demo app).
FEATURE_LABELS = {
    "age": "Age (years)",
    "trestbps": "Resting blood pressure (mmHg)",
    "chol": "Serum cholesterol (mg/dl)",
    "thalach": "Max heart rate achieved",
    "oldpeak": "ST depression (oldpeak)",
    "sex": "Sex (1=male, 0=female)",
    "cp": "Chest pain type",
    "fbs": "Fasting blood sugar > 120 (1/0)",
    "restecg": "Resting ECG result",
    "exang": "Exercise-induced angina (1/0)",
    "slope": "Slope of ST segment",
    "ca": "Major vessels colored (0-4)",
    "thal": "Thalassemia result",
}

# --------------------------------------------------------------------------- #
# Modelling constants                                                         #
# --------------------------------------------------------------------------- #
RANDOM_STATE = 42
TEST_SIZE = 0.20      # held-out test fraction (stratified)
CV_FOLDS = 5          # stratified k-fold for model selection

# Runtime knobs. Defaults are conservative so the project never hangs on
# constrained environments (nested parallelism between CalibratedClassifierCV,
# the Pipeline, and the estimator can deadlock under n_jobs=-1). Advanced users
# on a strong machine can raise N_JOBS locally for speed.
N_JOBS = 1
PERMUTATION_N_REPEATS = 10

# HistGradientBoosting uses internal OpenMP threading that can hang on some
# constrained environments even with N_JOBS=1. It is therefore OPT-IN: the
# default `python -m src.train` runs Dummy + LogReg + SVM + MLP + RandomForest
# (all confirmed fast and reliable) and selects Random Forest. Set this to True
# to add HistGradientBoosting to the comparison on a capable machine. This does
# not change the selected model or the reported Cleveland metrics (Random Forest
# wins either way).
INCLUDE_HISTGB = False

# --------------------------------------------------------------------------- #
# Phase 1 — evaluation depth                                                  #
# --------------------------------------------------------------------------- #
CALIBRATION_METHOD = "isotonic"   # may be revised by the calibration comparison
DEFAULT_THRESHOLD = 0.50          # the *default* cut-off — NOT a clinical decision
THRESHOLD_GRID = [round(0.20 + 0.05 * i, 2) for i in range(9)]  # 0.20 .. 0.60
COST_FN = 5                       # a missed sick patient is treated as 5x worse...
COST_FP = 1                       # ...than a false alarm (Statlog-style cost ratio)
BOOTSTRAP_N = 2000                # bootstrap resamples for confidence intervals
