# Heart Disease Risk-Score ML — lightweight task runner.
# Usage: make <target>   (e.g. `make all`, `make app`)
PY ?= python

.PHONY: help data train evaluate phase1 explain subgroup app api test all

help:
	@echo "Targets: data train evaluate phase1 explain subgroup external app api test all"

data:        ## clean + build processed dataset
	$(PY) -m src.data

train:       ## compare models, select + calibrate best, save artifact
	$(PY) -m src.train

evaluate:    ## test metrics + figures
	$(PY) -m src.evaluate

phase1:      ## evaluation depth: thresholds, CIs, nested CV, calibration, DCA, errors, learning curve
	$(PY) -m src.thresholds
	$(PY) -m src.uncertainty
	$(PY) -m src.nested_cv
	$(PY) -m src.calibration_report
	$(PY) -m src.decision_curve
	$(PY) -m src.error_analysis
	$(PY) -m src.learning_curve

explain:     ## global + local explainability (permutation, SHAP, patient report)
	$(PY) -m src.explain
	$(PY) -m src.patient_report

subgroup:    ## exploratory subgroup performance screen
	$(PY) -m src.subgroup

external:    ## Phase 5 external validation on UCI Hungarian/VA/Switzerland cohorts
	$(PY) -m src.external_validation

app:         ## run the Streamlit educational dashboard
	streamlit run app/streamlit_app.py

api:         ## run the FastAPI service (docs at /docs)
	uvicorn api.main:app --reload

test:        ## run the test suite
	$(PY) -m pytest

all: data train evaluate phase1 explain subgroup external test  ## full pipeline + tests
