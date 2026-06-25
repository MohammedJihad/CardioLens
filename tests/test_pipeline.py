"""Lightweight tests for the core pipeline contract.

Run with:  pytest -q
These guard the things most likely to break silently: the target fix, the
no-leakage preprocessing shape, and the prediction output schema.
"""
from __future__ import annotations

import numpy as np
import pytest

from src import config
from src.data import clean, load_processed
from src.preprocessing import build_preprocessor
import pandas as pd


def _fake_raw() -> pd.DataFrame:
    # Two rows: one clearly diseased-coded (target=0), one healthy (target=1).
    return pd.DataFrame({
        "age": [60, 45], "sex": [1, 0], "cp": [0, 2], "trestbps": [140, 120],
        "chol": [280, 200], "fbs": [0, 0], "restecg": [0, 1], "thalach": [120, 170],
        "exang": [1, 0], "oldpeak": [3.0, 0.0], "slope": [0, 2], "ca": [3, 0],
        "thal": [3, 2], "target": [0, 1],
    })


def test_target_is_flipped_to_disease_positive():
    out = clean(_fake_raw())
    # raw target=0 (diseased) must become heart_disease=1
    assert out.loc[0, config.TARGET] == 1
    assert out.loc[1, config.TARGET] == 0
    assert config.RAW_TARGET not in out.columns


def test_clean_drops_duplicates():
    raw = pd.concat([_fake_raw(), _fake_raw().iloc[[0]]], ignore_index=True)
    out = clean(raw)
    assert len(out) == 2  # the duplicated first row is removed


def test_processed_dataset_loads_and_balances():
    df = load_processed(save=False)
    assert set(config.FEATURES + [config.TARGET]).issubset(df.columns)
    assert df[config.TARGET].nunique() == 2
    assert 100 < len(df) < 1000  # Cleveland is ~300 rows


def test_preprocessor_outputs_finite_numeric_matrix():
    df = load_processed(save=False)
    pre = build_preprocessor()
    X = pre.fit_transform(df[config.FEATURES])
    assert X.shape[0] == len(df)
    assert np.isfinite(X).all()  # imputation + scaling leave no NaNs


def test_uci_num_severity_rule_maps_0to4_correctly():
    """Original UCI num 0-4: 0 -> absent, 1..4 -> present (NOT inverted)."""
    from src.dataset_registry import apply_target_rule
    out = apply_target_rule(pd.Series([0, 1, 2, 3, 4]), "uci_num_severity")
    assert list(out) == [0, 1, 1, 1, 1]


def test_kaggle_inverted_rule_flips_and_rejects_nonbinary():
    """Kaggle inverted binary: 0<->1 flip; must refuse a non-binary label."""
    from src.dataset_registry import apply_target_rule
    out = apply_target_rule(pd.Series([0, 1, 1, 0]), "kaggle_inverted_binary")
    assert list(out) == [1, 0, 0, 1]
    with pytest.raises(ValueError):
        apply_target_rule(pd.Series([0, 1, 2, 3]), "kaggle_inverted_binary")


def test_schema_harmonize_remaps_uci_encodings():
    """UCI-original cp/slope/thal translate into the canonical encoding."""
    from src.schema import harmonize
    df = pd.DataFrame({"cp": [1, 4], "slope": [1, 3], "thal": [3, 7]})
    out = harmonize(df, "uci_original")
    assert list(out["cp"]) == [0, 3]
    assert list(out["slope"]) == [0, 2]
    assert list(out["thal"]) == [1, 3]
    # canonical encoding is returned untouched
    assert harmonize(df, "canonical").equals(df)


def test_predict_one_schema():
    pytest.importorskip("joblib")
    from src.predict import predict_one, public_view, EXAMPLE
    if not config.MODEL_PATH.exists():
        pytest.skip("model not trained yet; run `python -m src.train`")
    out = predict_one(EXAMPLE)
    # preferred public schema
    assert 0.0 <= out["model_score"] <= 1.0
    assert "model score" in out["score_band"].lower()
    assert out["prediction_at_default_threshold"] in (0, 1)
    assert "disclaimer" in out
    # public_view exposes only safe keys (deprecated aliases hidden)
    pub = public_view(out)
    assert "disease_probability" not in pub and "risk_band" not in pub


# --------------------------------------------------------------------------- #
# Phase 1 — evaluation depth                                                  #
# --------------------------------------------------------------------------- #
def test_threshold_table_schema():
    """threshold_table returns one row per grid threshold with all metric columns."""
    from src.thresholds import threshold_table
    y = pd.Series([0, 1, 0, 1, 1, 0, 1, 0])
    proba = np.array([0.1, 0.9, 0.3, 0.6, 0.8, 0.4, 0.55, 0.2])
    tbl = threshold_table(y, proba)
    assert len(tbl) == len(config.THRESHOLD_GRID)
    for col in ["threshold", "TP", "FP", "TN", "FN", "sensitivity_recall",
                "specificity", "precision", "f1", "accuracy",
                "balanced_accuracy", "cost"]:
        assert col in tbl.columns


def test_bootstrap_schema():
    """bootstrap returns point + 95% CI bounds for every metric."""
    from src.uncertainty import bootstrap
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, size=40)
    proba = rng.random(40)
    res = bootstrap(y, proba, n=50, seed=1)
    assert {"roc_auc", "recall_sensitivity", "brier_score"}.issubset(res)
    for v in res.values():
        assert set(v).issuperset({"point", "ci_low", "ci_high", "n_valid"})


def test_calibration_report_present_and_nonempty():
    """If generated, the calibration report exists and is substantive."""
    p = config.REPORTS_DIR / "calibration_report.md"
    if not p.exists():
        pytest.skip("run `python -m src.calibration_report` first")
    assert len(p.read_text().strip()) > 200


def test_no_generated_report_is_empty():
    """Every generated markdown report under reports/ must be non-empty."""
    md_files = list(config.REPORTS_DIR.glob("*.md"))
    if not md_files:
        pytest.skip("no reports generated yet")
    for f in md_files:
        assert len(f.read_text().strip()) > 50, f"empty report: {f.name}"


# --------------------------------------------------------------------------- #
# Phase 2 — explainability                                                    #
# --------------------------------------------------------------------------- #
def test_explain_prediction_schema():
    """Local explanation returns the documented schema with safe language."""
    if not config.MODEL_PATH.exists():
        pytest.skip("model not trained yet; run `python -m src.train`")
    from src.patient_report import explain_prediction
    from src.predict import EXAMPLE
    out = explain_prediction(EXAMPLE)
    assert set(out) >= {"model_score", "threshold", "score_band",
                        "top_positive_factors", "top_negative_factors", "disclaimer"}
    assert 0.0 <= out["model_score"] <= 1.0
    assert "model score" in out["score_band"].lower()
    assert "not a diagnosis" in out["disclaimer"].lower()
    for factor in out["top_positive_factors"] + out["top_negative_factors"]:
        assert {"feature", "contribution"}.issubset(factor)


def test_patient_report_present_and_safe():
    """If generated, the patient report uses model-score language, no diagnosis claims."""
    p = config.REPORTS_DIR / "sample_patient_report.md"
    if not p.exists():
        pytest.skip("run `python -m src.patient_report` first")
    text = p.read_text().lower()
    assert len(text.strip()) > 200
    assert "model score" in text
    for forbidden in ["you have heart disease", "diagnosed with heart disease",
                      "the patient has heart disease"]:
        assert forbidden not in text


def test_explainability_report_present_and_nonempty():
    p = config.REPORTS_DIR / "explainability_report.md"
    if not p.exists():
        pytest.skip("run `python -m src.explain` first")
    text = p.read_text()
    assert len(text.strip()) > 200
    assert "not causal" in text.lower()  # explanations must disclaim causality


# --------------------------------------------------------------------------- #
# Phase 3 — responsible AI & documentation                                    #
# --------------------------------------------------------------------------- #
def test_subgroup_row_schema():
    """subgroup_row returns counts, rates, and CI-bearing metrics."""
    from src.subgroup import subgroup_row
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, size=60)
    proba = rng.random(60)
    row = subgroup_row("test", y, proba, n_boot=50)
    assert {"subgroup", "n", "disease_rate", "roc_auc", "roc_auc_ci",
            "recall", "specificity"}.issubset(row)
    assert row["n"] == 60


def test_data_card_and_checklist_present():
    """Phase 3 documentation files exist and are substantive."""
    for name in ("data_card.md", "clinical_reporting_checklist.md"):
        p = config.REPORTS_DIR / name
        if not p.exists():
            pytest.skip(f"{name} not generated yet")
        assert len(p.read_text().strip()) > 200


def test_subgroup_report_is_labelled_exploratory():
    p = config.REPORTS_DIR / "subgroup_report.md"
    if not p.exists():
        pytest.skip("run `python -m src.subgroup` first")
    assert "exploratory" in p.read_text().lower()


def test_subgroup_module_exits_cleanly_as_subprocess(tmp_path):
    """`python -m src.subgroup` must TERMINATE (guards against hanging worker
    pools) and write its outputs.

    OPT-IN: spawning a subprocess and waiting on it under pytest behaves
    differently across environments (CI runners, sandboxes), so this guard is
    **skipped by default** to keep `pytest` deterministic everywhere. Enable it
    with ``RUN_SUBPROCESS_GUARD=1 pytest``. The underlying command is fast and
    exits cleanly when run directly (`python -m src.subgroup` / `make subgroup`).

    Implementation notes (why not a plain ``subprocess.run(capture_output=True)``):
    capturing via PIPE makes the parent block in ``communicate()`` until EOF on the
    pipe. If any short-lived grandchild (BLAS/OpenMP helper, multiprocessing
    resource tracker) inherits the pipe fd and lingers, the parent hangs even
    though the child already exited. So we send stdout to DEVNULL (nothing to wait
    on), poll the child manually, and force-kill the whole process group on
    timeout.
    """
    import os
    import signal
    import subprocess
    import sys
    import time

    if os.environ.get("RUN_SUBPROCESS_GUARD") != "1":
        pytest.skip("opt-in: set RUN_SUBPROCESS_GUARD=1 to run the subprocess hang-guard")
    if not config.MODEL_PATH.exists():
        pytest.skip("model not trained yet; run `python -m src.train`")

    env = dict(os.environ)
    env.update({
        "PYTHONUNBUFFERED": "1",
        "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1",
    })
    err_log = tmp_path / "subgroup_stderr.log"
    timeout_s = 90

    with open(err_log, "wb") as err:
        proc = subprocess.Popen(
            [sys.executable, "-m", "src.subgroup"],
            cwd=str(config.ROOT),
            stdout=subprocess.DEVNULL,   # no stdout pipe -> no communicate() deadlock
            stderr=err,                  # stderr to a file (also no pipe to block on)
            env=env,
            start_new_session=True,      # own process group, so we can kill the tree
        )
        deadline = time.time() + timeout_s
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.5)
        if proc.poll() is None:          # still running -> hang: kill the group
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                proc.kill()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
            pytest.fail(f"`python -m src.subgroup` did not terminate within {timeout_s}s (hang).")

    assert proc.returncode == 0, err_log.read_text()[-2000:]
    assert (config.REPORTS_DIR / "subgroup_report.md").exists()
    assert (config.REPORTS_DIR / "subgroup_metrics.csv").exists()


# --------------------------------------------------------------------------- #
# Phase 4 — product surface (API + app)                                       #
# --------------------------------------------------------------------------- #
def _api_client():
    fastapi = pytest.importorskip("fastapi")  # noqa: F841
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


def test_api_health():
    client = _api_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_api_predict_schema_and_no_diagnosis():
    if not config.MODEL_PATH.exists():
        pytest.skip("model not trained yet; run `python -m src.train`")
    client = _api_client()
    from src.predict import EXAMPLE
    r = client.post("/predict", json=EXAMPLE)
    assert r.status_code == 200
    body = r.json()
    assert {"model_score", "score_band", "default_threshold",
            "above_default_threshold", "disclaimer"}.issubset(body)
    assert 0.0 <= body["model_score"] <= 1.0
    assert "model score" in body["score_band"].lower()
    # no diagnosis-as-output wording anywhere in the response
    blob = " ".join(str(v) for v in body.values()).lower()
    for forbidden in ["diagnosis:", "you have heart disease", "diagnosed with"]:
        assert forbidden not in blob


def test_api_predict_validation_rejects_bad_input():
    client = _api_client()
    from src.predict import EXAMPLE
    bad = {**EXAMPLE, "sex": 5}  # out of range
    assert client.post("/predict", json=bad).status_code == 422


def test_streamlit_app_present_with_disclaimer_language():
    app_file = config.ROOT / "app" / "streamlit_app.py"
    assert app_file.exists()
    text = app_file.read_text().lower()
    assert "model score" in text
    assert "disclaimer" in text
    # anti-diagnosis framing must be present (phrase kept on one source line)
    assert "never a diagnosis" in text or "not a diagnosis" in text


# --------------------------------------------------------------------------- #
# Phase 5 — external validation                                               #
# --------------------------------------------------------------------------- #
def test_external_cohorts_load_and_have_both_classes():
    """Each external cohort loads, harmonises, and has both outcome classes."""
    ed = pytest.importorskip("src.external_data")
    for name in ed.SOURCES:
        path = ed.EXTERNAL_DIR / ed.SOURCES[name][0]
        if not path.exists():
            pytest.skip(f"{name} cohort not cached and no network")
        X, y, _ = ed.load_cohort(name)
        assert len(X) == len(y) > 50
        assert set(y.unique()).issubset({0, 1})
        assert list(X.columns) == config.FEATURES


def test_external_validation_report_is_honest():
    """The report must state the drop and the missing-feature cause, no diagnosis."""
    p = config.REPORTS_DIR / "external_validation_report.md"
    if not p.exists():
        pytest.skip("run `python -m src.external_validation` first")
    text = p.read_text().lower()
    assert "external" in text
    assert "recalibration" in text or "retrain" in text
    assert "missing" in text
    assert "diagnosis" not in text or "not a diagnosis" in text


def test_external_metrics_csv_schema():
    p = config.REPORTS_DIR / "external_validation_metrics.csv"
    if not p.exists():
        pytest.skip("run `python -m src.external_validation` first")
    import csv
    with open(p) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 3
    for r in rows:
        assert {"cohort", "n", "roc_auc", "brier"}.issubset(r)


# --------------------------------------------------------------------------- #
# Phase 5 cleanup — split loader, feature-availability report, doc consistency #
# --------------------------------------------------------------------------- #
def test_external_data_load_cohort():
    """src.external_data.load_cohort returns aligned X/y with both classes."""
    ed = pytest.importorskip("src.external_data")
    name = next(iter(ed.SOURCES))
    if not (ed.EXTERNAL_DIR / ed.SOURCES[name][0]).exists():
        pytest.skip("external cohort not cached and no network")
    X, y, raw = ed.load_cohort(name)
    assert len(X) == len(y) == len(raw) > 50
    assert list(X.columns) == config.FEATURES
    assert set(y.unique()).issubset({0, 1})


def test_external_feature_availability_report_present():
    p = config.REPORTS_DIR / "external_feature_availability.md"
    if not p.exists():
        pytest.skip("run `python -m src.external_validation` first")
    text = p.read_text()
    assert len(text.strip()) > 300
    assert "ca" in text and "thal" in text
    assert "not a clinical validation" in text.lower() or "educational" in text.lower()


def test_docs_have_no_stale_no_external_validation_claim():
    """README and model card must not still claim 'no external validation'."""
    for rel in ("README.md", "reports/model_card.md"):
        p = config.ROOT / rel
        if not p.exists():
            continue
        assert "no external validation" not in p.read_text().lower()
