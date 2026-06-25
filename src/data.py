"""Data loading and cleaning.

Responsibilities
----------------
1. Load the raw UCI Cleveland CSV, failing with a helpful message if it is
   missing (so a fresh clone tells the user exactly what to do).
2. Normalise column names (strip whitespace — the original course notebook had
   a leading-space `" Oldpeak"` column).
3. Fix the target: in this widely-circulated CSV the label is INVERTED relative
   to its own data dictionary. We verified empirically (lower max-HR, higher
   oldpeak, more exercise angina all track `target == 0`) that **target == 0 is
   the diseased group**. We therefore model `heart_disease = 1 - target` so that
   the positive class means "disease present" — which is what recall/sensitivity
   should reward in a screening context. See data/README.md for the full check.
4. Drop exact duplicate rows and persist a clean processed file.
"""
from __future__ import annotations

import pandas as pd

from . import config
from . import dataset_registry as registry


class DatasetNotFoundError(FileNotFoundError):
    """Raised when the raw dataset is absent, with guidance on how to fix it."""


def _require_raw() -> None:
    if not config.RAW_DATA.exists():
        raise DatasetNotFoundError(
            f"\nRaw dataset not found at: {config.RAW_DATA}\n"
            "This project uses the UCI Cleveland Heart Disease dataset (303 rows).\n"
            "Place a CSV with the standard columns "
            "[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, "
            "oldpeak, slope, ca, thal, target] at the path above.\n"
            "See data/README.md for the source and download instructions."
        )


def load_raw() -> pd.DataFrame:
    """Load the raw CSV and standardise column names."""
    _require_raw()
    df = pd.read_csv(config.RAW_DATA)
    # Strip BOM and stray whitespace from headers (fixes the legacy " Oldpeak").
    df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw frame and build the corrected modelling target."""
    df = df.copy()

    # Original UCI files use '?' for missing ca/thal. Coerce to NaN; the
    # preprocessing pipeline imputes them. (The cleaned CSV has none, but a
    # production pipeline should never assume that.)
    for col in ("ca", "thal"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derive the target via the ACTIVE source's documented rule (see
    # dataset_registry.py). The current Cleveland CSV uses the inverted-binary
    # rule; original UCI files (num 0-4) would use (num > 0) instead — so adding
    # external cohorts later cannot silently mislabel them.
    spec = registry.active_spec()
    df[config.TARGET] = registry.apply_target_rule(
        df[spec.raw_target_col], spec.target_rule
    ).astype(int)
    df = df.drop(columns=[spec.raw_target_col])

    # Remove exact duplicate rows (the Cleveland CSV contains one).
    df = df.drop_duplicates().reset_index(drop=True)

    keep = config.FEATURES + [config.TARGET]
    missing = [c for c in keep if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")
    return df[keep]


def load_processed(save: bool = True) -> pd.DataFrame:
    """End-to-end: raw -> cleaned frame, optionally persisted to data/processed."""
    df = clean(load_raw())
    if save:
        config.PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(config.PROCESSED_DATA, index=False)
    return df


if __name__ == "__main__":
    out = load_processed()
    print(f"Processed dataset: {out.shape[0]} rows x {out.shape[1]} cols")
    print(out[config.TARGET].value_counts().rename("count"))
