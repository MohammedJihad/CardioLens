"""Dataset registry — the safe, per-source target & encoding contract.

This fixes the core risk flagged in review: a single global `1 - target` rule is
**unsafe**. Different sources need different target derivations:

  * `kaggle_inverted_binary` — the current Cleveland CSV ships a binary label
    that is INVERTED vs its data dictionary (verified by exploratory consistency
    checks — see data/README.md). Use 1 - target.
  * `uci_num_severity` — original UCI files encode `num` as 0-4. Disease presence
    is `(num > 0)`. **Do NOT** apply the inversion to these.

Each entry also declares its encoding family (see schema.py) so external cohorts
can be harmonized before validation. Only the active training source is loaded by
the pipeline today; the UCI-original cohorts are registered (NOT loaded, NOT
trained) so Phase 1 external validation has an explicit, reviewed contract.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import config


@dataclass(frozen=True)
class DatasetSpec:
    key: str
    description: str
    target_rule: str          # 'kaggle_inverted_binary' | 'uci_num_severity'
    encoding: str             # 'canonical' | 'uci_original'  (see schema.py)
    raw_target_col: str       # column holding the raw label in that source
    status: str               # 'active' | 'registered_for_phase1'


REGISTRY: dict[str, DatasetSpec] = {
    # The dataset the pipeline trains on today.
    "cleveland_kaggle": DatasetSpec(
        key="cleveland_kaggle",
        description="Circulating Kaggle Cleveland CSV (302 rows; INVERTED binary label).",
        target_rule="kaggle_inverted_binary",
        encoding="canonical",
        raw_target_col="target",
        status="active",
    ),
    # Registered for Phase 1 external validation — NOT loaded or trained yet.
    "cleveland_uci": DatasetSpec(
        key="cleveland_uci",
        description="Original UCI Cleveland (processed.cleveland.data, num 0-4).",
        target_rule="uci_num_severity",
        encoding="uci_original",
        raw_target_col="num",
        status="registered_for_phase1",
    ),
    "hungarian_uci": DatasetSpec(
        key="hungarian_uci",
        description="UCI Hungarian cohort (~294 rows) — primary external validation.",
        target_rule="uci_num_severity",
        encoding="uci_original",
        raw_target_col="num",
        status="registered_for_phase1",
    ),
    "va_uci": DatasetSpec(
        key="va_uci",
        description="UCI VA Long Beach cohort (~200 rows) — secondary external validation.",
        target_rule="uci_num_severity",
        encoding="uci_original",
        raw_target_col="num",
        status="registered_for_phase1",
    ),
    "switzerland_uci": DatasetSpec(
        key="switzerland_uci",
        description="UCI Switzerland cohort (~123 rows) — severe chol missingness; use with caution.",
        target_rule="uci_num_severity",
        encoding="uci_original",
        raw_target_col="num",
        status="registered_for_phase1",
    ),
}

# The source the pipeline uses right now.
ACTIVE_KEY = "cleveland_kaggle"


def active_spec() -> DatasetSpec:
    return REGISTRY[ACTIVE_KEY]


def apply_target_rule(raw_values, rule: str):
    """Derive the binary `heart_disease` (1 = disease present) from a raw label.

    This is the single place target semantics live, so no source can be silently
    mislabelled again.
    """
    import pandas as pd

    s = pd.to_numeric(raw_values, errors="coerce")
    if rule == "kaggle_inverted_binary":
        if not set(s.dropna().unique()).issubset({0, 1}):
            raise ValueError(
                "kaggle_inverted_binary expects a 0/1 label; got non-binary values. "
                "Use 'uci_num_severity' for original 0-4 UCI files."
            )
        return (1 - s).astype("Int64")
    if rule == "uci_num_severity":
        return (s > 0).astype("Int64")
    raise ValueError(f"Unknown target_rule '{rule}'.")
