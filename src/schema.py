"""Schema definition and encoding harmonization.

The training data (current Cleveland CSV) uses **recoded** categorical encodings
(the "Kaggle" style): cp in 0-3, slope in 0-2, thal in 0-3. The *original* UCI
files (Hungarian / VA / Switzerland / raw Cleveland) use the historical
encodings: cp in 1-4, slope in 1-3, thal in {3, 6, 7}.

Before any external-cohort validation (Phase 1), every source must be mapped
into the **canonical** (training) encoding. This module declares that canonical
schema and the documented translation maps. It is **not** wired into the active
pipeline yet — the current dataset is already canonical — it exists so the
harmonization is explicit and reviewable before Phase 1.
"""
from __future__ import annotations

import pandas as pd

# Canonical encoding == the encoding of the current training CSV.
CANONICAL_NUMERIC = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CANONICAL_CATEGORICAL = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]

# Translation: ORIGINAL UCI value -> CANONICAL (training) value.
# cp and slope are a clean "-1" shift.
UCI_TO_CANONICAL = {
    "cp": {1: 0, 2: 1, 3: 2, 4: 3},        # typical/atypical/non-anginal/asymptomatic
    "slope": {1: 0, 2: 1, 3: 2},           # up / flat / down
    # thal: 3=normal, 6=fixed defect, 7=reversible defect.
    # NOTE: the current Kaggle CSV uses thal in {0,1,2,3} where the meaning of 0
    # is ambiguous (often treated as missing/unknown). We map the three real UCI
    # categories onto {1,2,3} and leave 0 reserved for unknown. This ambiguity
    # is intentionally surfaced here and must be resolved (with documentation)
    # at the start of Phase 1 before trusting any thal-dependent comparison.
    "thal": {3: 1, 6: 2, 7: 3},
}

ENCODINGS = {
    "canonical": "training encoding (cp 0-3, slope 0-2, thal 0-3)",
    "uci_original": "historical UCI encoding (cp 1-4, slope 1-3, thal 3/6/7)",
}


def harmonize(df: pd.DataFrame, encoding: str) -> pd.DataFrame:
    """Translate a source dataframe into the canonical encoding.

    encoding == 'canonical' -> returned unchanged.
    encoding == 'uci_original' -> cp/slope/thal remapped per UCI_TO_CANONICAL.
    Unknown encodings raise, so a new source can never be silently mis-aligned.
    """
    if encoding == "canonical":
        return df
    if encoding != "uci_original":
        raise ValueError(f"Unknown encoding '{encoding}'. Known: {list(ENCODINGS)}")

    out = df.copy()
    for col, mapping in UCI_TO_CANONICAL.items():
        if col in out.columns:
            out[col] = out[col].map(mapping).astype("Int64")
    return out
