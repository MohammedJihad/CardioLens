"""External-cohort data loading for Phase 5 validation.

Single home for: dataset sources, column names, local/cache reading (with a
network fallback), target mapping, schema harmonisation, and missing-value
handling. :mod:`src.external_validation` imports from here and only does the
scoring/metrics, keeping data and evaluation concerns separate.

Data: UCI Heart Disease (Janosi, Steinbrunn, Pfisterer, Detrano, 1988), CC BY 4.0,
via the nyuvis/datasets mirror; cached under ``data/external/``.
"""
from __future__ import annotations

from io import StringIO
from urllib.request import urlopen

import numpy as np
import pandas as pd

from . import config
from .dataset_registry import apply_target_rule
from .schema import harmonize

COLS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
        "exang", "oldpeak", "slope", "ca", "thal", "num"]
EXTERNAL_DIR = config.ROOT / "data" / "external"
MIRROR = "https://raw.githubusercontent.com/nyuvis/datasets/master/heart"
SOURCES = {
    "Hungarian": ("hungarian.data", "processed.hungarian.data"),
    "VA Long Beach": ("va.data", "processed.va.data"),
    "Switzerland": ("switzerland.data", "processed.switzerland.data"),
}
# physiologically-impossible zeros that are really "missing" in these files
ZERO_AS_MISSING = ["chol", "trestbps"]
# key features whose external availability we care about
KEY_FEATURES = ["ca", "thal", "slope", "chol", "fbs", "restecg"]


def _read_local_or_download(local_name: str, remote_name: str) -> str:
    path = EXTERNAL_DIR / local_name
    if path.exists():
        return path.read_text()
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    text = urlopen(f"{MIRROR}/{remote_name}", timeout=30).read().decode()  # noqa: S310
    path.write_text(text)
    return text


def load_cohort(name: str):
    """Return ``(X[FEATURES], y, raw_df)`` for one external cohort, harmonised.

    * optional header row is dropped (the Hungarian file ships one),
    * ``?`` and impossible ``chol``/``trestbps`` zeros become missing,
    * target is ``num > 0`` (via the dataset registry),
    * categorical encodings are mapped into the training schema.
    """
    local_name, remote_name = SOURCES[name]
    raw = _read_local_or_download(local_name, remote_name).splitlines()
    first_cell = raw[0].split(",")[0].replace(".", "", 1).lstrip("-")
    body = raw[1:] if not first_cell.isdigit() else raw          # drop header row if present
    df = pd.read_csv(StringIO("\n".join(body)), header=None, names=COLS, na_values=["?"])
    for c in COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ZERO_AS_MISSING:                                    # 0 is a missing sentinel here
        df[c] = df[c].replace(0, np.nan)
    y = apply_target_rule(df["num"], "uci_num_severity").astype("Int64")
    X = harmonize(df[config.FEATURES].copy(), "uci_original")
    keep = y.notna()
    return (X[keep.values].reset_index(drop=True),
            y[keep.values].astype(int).reset_index(drop=True),
            df[keep.values].reset_index(drop=True))


def missing_pct(raw_df: pd.DataFrame) -> dict:
    """Percent missing per key feature (chol/trestbps zeros already NaN)."""
    return {c: round(float(raw_df[c].isna().mean()) * 100, 0) for c in KEY_FEATURES}


def feature_availability() -> pd.DataFrame:
    """Per-cohort n, disease rate, and % missing for each key feature."""
    rows = []
    for name in SOURCES:
        _, y, raw = load_cohort(name)
        row = {"cohort": name, "n": int(len(y)), "disease_rate": round(float(y.mean()), 3)}
        row.update({f"{c}_missing_%": missing_pct(raw)[c] for c in KEY_FEATURES})
        rows.append(row)
    return pd.DataFrame(rows)
