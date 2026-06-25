#!/usr/bin/env python
"""Export a single web-data/reports-summary.json from the frozen report files.

This script is **pure file-reading**. It does NOT import the model, does NOT load
sklearn, and does NOT recompute anything. Every value is copied verbatim from the
research reports under ``reports/`` (only re-rounded for display consistency) and
written to ``web-data/reports-summary.json`` so the website has one honest source
of truth. Nothing under ``reports/`` is ever written.

Sources:
  * reports/metrics.json                     -> internal test metrics + confusion
  * reports/threshold_test_evaluation.csv    -> the evaluated 0.2 operating point
  * reports/external_validation_metrics.csv  -> 3 external cohorts

Run:  python scripts/export_reports_summary.py        (prints JSON to stdout)
"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT_DIR = ROOT / "web-data"
OUT_FILE = OUT_DIR / "reports-summary.json"

SOURCES = [
    "reports/metrics.json",
    "reports/threshold_test_evaluation.csv",
    "reports/external_validation_metrics.csv",
]

# Map the cohort label as written in the CSV to a stable JSON key.
COHORT_KEY = {
    "hungarian": "hungarian",
    "va long beach": "va",
    "switzerland": "switzerland",
}


def r3(x) -> float:
    """Round AUC / Brier / sensitivity / specificity to 3 decimals (display only)."""
    return round(float(x), 3)


def _ci(raw: str) -> list[float]:
    """Parse a '[0.81, 0.902]' CI string verbatim into two rounded floats."""
    nums = raw.strip().strip("[]").split(",")
    return [r3(n) for n in nums]


def build_metrics() -> dict:
    data = json.loads((REPORTS / "metrics.json").read_text())
    tm = data["test_metrics"]
    cm = tm["confusion_matrix"]
    confusion = {"tp": cm["tp"], "fp": cm["fp"], "tn": cm["tn"], "fn": cm["fn"]}
    return {
        "roc_auc": r3(tm["roc_auc"]),
        "pr_auc": r3(tm["pr_auc"]),
        "sensitivity": r3(tm["recall_sensitivity"]),   # source key: recall_sensitivity
        "specificity": r3(tm["specificity"]),
        "f1": r3(tm["f1"]),
        "brier": r3(tm["brier_score"]),                # source key: brier_score
        "n_test": confusion["tp"] + confusion["fp"] + confusion["tn"] + confusion["fn"],
        "confusion": confusion,
    }


def build_thresholds() -> dict:
    with (REPORTS / "threshold_test_evaluation.csv").open(newline="") as fh:
        row = next(csv.DictReader(fh))   # the single 0.2 row
    return {
        "selected": float(row["threshold"]),
        "sens_selected": r3(row["sensitivity_recall"]),
        "spec_selected": r3(row["specificity"]),
        "fn_selected": int(row["FN"]),
        "tp": int(row["TP"]),
        "fp": int(row["FP"]),
        "tn": int(row["TN"]),
    }


def build_external() -> dict:
    cohorts: dict[str, dict] = {}
    ca_missing: list[float] = []
    thal_missing: list[float] = []
    with (REPORTS / "external_validation_metrics.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            key = COHORT_KEY[row["cohort"].strip().lower()]
            ca = float(row["ca_missing_%"])
            thal = float(row["thal_missing_%"])
            ca_missing.append(ca)
            thal_missing.append(thal)
            cohorts[key] = {
                "label": row["cohort"].strip(),
                "n": int(row["n"]),
                "disease_rate": r3(row["disease_rate"]),
                "roc_auc": r3(row["roc_auc"]),
                "roc_auc_ci": _ci(row["roc_auc_ci"]),
                "pr_auc": r3(row["pr_auc"]),
                "brier": r3(row["brier"]),
                "sens_at_0.2": r3(row["sensitivity@0.2"]),
                "spec_at_0.2": r3(row["specificity@0.2"]),
                "ca_missing_pct": ca,
                "thal_missing_pct": thal,
            }

    def rng(vals: list[float]) -> str:
        return f"{int(min(vals))}-{int(max(vals))}%"

    return {
        "n_cohorts": len(cohorts),
        # ca = number of major vessels = the model's most important feature.
        "missing_range": rng(ca_missing),          # ca missingness span (96-99%)
        "missing_range_ca": rng(ca_missing),
        "missing_range_thal": rng(thal_missing),
        **cohorts,                                  # hungarian / va / switzerland
    }


def build_summary() -> dict:
    return {
        "generated_from": SOURCES,
        "year": datetime.now().year,
        "note": ("Values copied verbatim from the frozen research reports and re-rounded "
                 "for display only — nothing here is recomputed. Educational ML demo; "
                 "model scores on historical public research data, not medical advice."),
        "metrics": build_metrics(),
        "thresholds": build_thresholds(),
        "external": build_external(),
    }


def main() -> None:
    summary = build_summary()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(summary, indent=2, ensure_ascii=False)
    OUT_FILE.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
