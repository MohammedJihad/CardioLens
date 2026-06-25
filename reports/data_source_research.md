# Data Source Research — Heart Disease Risk Screening ML System

**Phase 0 deliverable.** This document surveys reputable, public, de-identified
cardiovascular datasets to inform the project's data strategy. **Phase 0 added no
new training and no new model experiments; previously generated training
artifacts were preserved unchanged.** Research and documentation only.

**Scope rules honoured:** only public, reputable, legally usable, de-identified
sources; no scraping of identifiable individuals; every candidate carries a
source URL, license/access note, target definition, feature notes, and
limitations. Datasets are *not* merged blindly — differing schemas/targets are
kept as separate experiments.

> All outputs of this project are **model scores for educational use only** —
> never diagnoses. None of the datasets below are used here to make medical
> claims.

---

## Summary table

| Dataset | Source quality | Rows | Schema vs current UCI | Target clarity | Privacy safety | Legal use | Difficulty | Ext-validation value | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| UCI Cleveland | Reference (UCI) | 303 | identical (in use) | high (0–4 → binary) | high (de-identified) | CC BY 4.0 | low | n/a (train set) | **Use now (already in repo)** |
| UCI Hungarian | Reference (UCI) | 294 | same schema, more missing | high | high | CC BY 4.0 | medium | **high** | **Use later — primary external validation** |
| UCI VA Long Beach | Reference (UCI) | 200 | same schema, heavy missing | high | high | CC BY 4.0 | medium–high | medium | Use later — secondary external validation |
| UCI Switzerland | Reference (UCI) | 123 | same schema, severe missing (chol≈0) | high | high | CC BY 4.0 | high | low–medium | Use with caution — document missingness |
| Statlog (Heart) | Reference (UCI) | 270 | overlapping but re-encoded | high (2-class) | high | CC BY 4.0 | medium | low (overlaps Cleveland) | Optional sanity check only |
| CDC BRFSS 2015 (Health Indicators) | Official survey (CDC) | 253,680 | **different** (risk-factor survey) | high (HeartDiseaseorAttack) | high (de-identified) | CDC public-use (Kaggle copy = mirror) | medium | none (different problem) | **Separate experiment — Track B** |
| NHANES | Official survey (CDC/NCHS) | varies by cycle | **different** (multi-component) | medium (must derive) | high (de-identified, consented) | public | high (assembly + weights) | none (different problem) | Track B alternative — later |
| MIMIC-IV | Reference EHR (MIT/PhysioNet) | ICU-scale | **different** (EHR) | n/a (must define cohort) | restricted (credentialed) | DUA + CITI required | very high | none for this schema | **Track C stretch — only with access** |

---

## 1. UCI Cleveland Heart Disease  ✅ *in use*

- **Source:** UCI ML Repository, "Heart Disease" (id 45). DOI 10.24432/C52P4X.
  https://archive.ics.uci.edu/dataset/45/heart+disease
- **Rows / features:** 303 patients; 13 clinical features + target (14 columns
  used out of 76 raw attributes).
- **Features:** age, sex, cp (chest pain type), trestbps (resting BP), chol
  (serum cholesterol), fbs (fasting blood sugar >120), restecg, thalach (max HR),
  exang (exercise angina), oldpeak (ST depression), slope, ca (major vessels),
  thal (thalassemia).
- **Target:** original `num` 0–4 (0 = no disease, 1–4 = disease severity);
  standard task binarises to presence vs absence. **Note (project-specific):** the
  circulating CSV we use has an inverted binary label; corrected in
  `data/README.md` (`heart_disease = 1 - target`).
- **Schema vs current repo:** identical — this *is* the training set.
- **License / access:** CC BY 4.0 — free reuse with attribution.
- **Privacy:** names and SSNs were removed and replaced with dummy values; safe.
- **Limitations:** ~300 rows (small), single-centre, collected 1988 — not
  representative of any current population.
- **Recommendation:** **Use now (already integrated).**

## 2. UCI Hungarian (Budapest)  🔜 *primary external validation*

- **Source:** same UCI "Heart Disease" bundle (Hungarian Institute of Cardiology,
  A. Janosi). Mirrored e.g. on Kaggle "redwankarimsony/heart-disease-data".
- **Rows:** 294. **Schema:** the same 14-column schema as Cleveland.
- **Target:** same disease presence definition.
- **Why valuable:** a **different cohort, same schema** → the cleanest path to
  genuine *external validation* (train on Cleveland, test on Hungary).
- **License / privacy:** CC BY 4.0; de-identified.
- **Limitations:** substantially more **missing values**, especially in `ca`,
  `thal`, and `slope` — which are among our most important features. This is
  itself an informative finding about external validity (top predictors may be
  unrecorded elsewhere).
- **Recommendation:** **Use later — Track A external validation (primary).**

## 3. UCI VA Long Beach  ⏳ *secondary external validation*

- **Source:** same UCI bundle (V.A. Medical Center, Long Beach; R. Detrano).
- **Rows:** 200. **Schema:** same 14-column schema.
- **Limitations:** heavy missingness and higher disease prevalence than Cleveland
  (sicker population) → distribution shift.
- **Recommendation:** **Use later — secondary external-validation cohort**, with
  explicit shift/missingness reporting.

## 4. UCI Switzerland  ⚠️ *use with caution*

- **Source:** same UCI bundle (University Hospitals Zurich/Basel).
- **Rows:** 123. **Schema:** same 14-column schema.
- **Limitations:** **severe missingness** — notably `chol` is recorded as 0
  (effectively missing) for most patients, and very high disease prevalence.
- **Recommendation:** **Optional / cautious** external check; document the
  missingness honestly; do not over-interpret.

## 5. Statlog (Heart)  ◻️ *optional sanity check*

- **Source:** UCI "Statlog (Heart)" (id 145).
  https://archive.ics.uci.edu/ml/datasets/statlog+(heart)
- **Rows / features:** 270 instances; 13 features; 2 classes (presence/absence).
- **Schema vs UCI:** overlapping variables but **re-encoded** (e.g. `thal` coded
  3/6/7; `slope` 1/2/3) and largely derived from the same Cleveland population —
  so it is **not an independent cohort**.
- **Notable extra:** ships an explicit **cost matrix** where a false negative
  (predicting absence when disease is present) costs 5× a false positive — useful
  inspiration for our cost-sensitive threshold work.
- **License:** CC BY 4.0.
- **Recommendation:** **Optional** — use only as an encoding/sanity cross-check,
  not as external validation (overlaps Cleveland).

## 6. CDC BRFSS 2015 — Heart Disease Health Indicators  🔭 *Track B*

- **Source of record:** CDC Behavioral Risk Factor Surveillance System — the
  **official** public-use survey data
  (https://www.cdc.gov/brfss/annual_data/annual_2015.html). The widely used ML
  version is a cleaned **convenience mirror** on Kaggle ("Heart Disease Health
  Indicators Dataset", Alex Teboul). Treat CDC as authoritative; the Kaggle
  derivative may carry its own platform terms and should not be cited as the
  licensing source of record.
- **Rows / features:** cleaned to 253,680 responses, 21 features + 1 target
  (raw 2015 BRFSS had 441,456 records, 330 features).
- **Features:** risk-factor and behavioural variables (high BP, high cholesterol,
  BMI, smoking, diabetes, physical activity, general health, age band, etc.) —
  **survey-derived, not clinical-exam measurements**.
- **Target:** `HeartDiseaseorAttack`, derived from the BRFSS calculated variable
  `_MICHD` (ever told they had coronary heart disease or a myocardial infarction).
- **Class balance:** strongly imbalanced — ~23,893 positives (~9.4%).
- **Schema vs UCI:** **fundamentally different** — different features, different
  target definition, different population (self-reported national survey vs
  clinical exam). **Must not be merged with UCI.**
- **License / privacy:** CDC public-use survey data, de-identified (the source of
  record). Cleaned Kaggle copies are convenience mirrors that may carry separate
  platform terms — cite CDC, not Kaggle, for licensing.
- **Limitations:** self-reported (recall/reporting bias); cross-sectional (not
  incident-risk); telephone-survey sampling biases.
- **Recommendation:** **Separate experiment (Track B)** — a population-level
  risk-factor model, clearly labelled as distinct from the clinical-tabular model.

## 7. NHANES (CDC / NCHS)  🔭 *Track B alternative*

- **Source:** CDC National Center for Health Statistics, continuous NHANES.
  https://wwwn.cdc.gov/nchs/nhanes/
- **Structure:** 2-year cycles (~5K participants/year) with a complex probability
  sampling design and **survey weights**; data split across Demographics,
  Examination, Laboratory, and Questionnaire components, merged by `SEQN`.
- **Cardiovascular content:** CDQ questionnaire (Rose angina, age 40+),
  measured blood pressure, lab cholesterol, and self-reported prior diagnoses.
- **Target:** **must be derived** by the analyst (e.g. self-reported CHD/MI or a
  composite) — no single ready-made label.
- **Schema vs UCI:** different; richer measured labs/exams but needs assembly.
- **License / privacy:** public, free, de-identified; participants consented;
  some sensitive variables are restricted via the NCHS Research Data Center.
- **Limitations:** **high implementation effort** (multi-file assembly, correct
  survey-weight handling); easy to misuse weights and bias estimates.
- **Recommendation:** **Track B alternative**, later — only if we want measured
  (not self-reported) clinical variables and are ready to handle survey design.

## 8. MIMIC-IV (MIT / PhysioNet)  💤 *Track C stretch*

- **Source:** PhysioNet, MIMIC-IV (current v3.1, DOI 10.13026/kpb9-mt58).
  https://physionet.org/content/mimiciv/3.1/
- **Content:** large de-identified ICU + hospital EHR (vitals, labs, diagnoses,
  procedures) — a fundamentally different, longitudinal EHR modality.
- **Access (hard gate):** **restricted**. Requires (1) becoming a credentialed
  PhysioNet user, (2) completing CITI "Data or Specimens Only Research" training,
  and (3) signing the PhysioNet Credentialed Health Data Use Agreement
  (License 1.5.0). It is **not** an anonymous download.
- **Schema vs UCI:** entirely different; no direct alignment.
- **Recommendation:** **Track C — future stretch only**. Do **not** implement
  unless credentialed access and DUA are genuinely in place. Never fake access or
  results. Until then, document it as an aspiration, not a dependency.

---

## Datasets reviewed and **rejected / avoided**

- **Any scraped patient stories, forum posts, hospital pages, or social-media
  health data** — rejected outright: identifiable individuals, no consent, legal
  and ethical violations.
- **Unattributed "heart.csv" copies with no provenance** — avoid as a *source of
  record*; only use mirrors that trace back to UCI, and always document the
  origin and any label quirks (as we did for the inverted Cleveland target).
- **MIMIC-IV without credentials** — not rejected on quality, but **off-limits
  until access requirements are satisfied**.

---

## Key judgements (the interview-relevant takeaways)

- **Provenance matters:** the same "Cleveland" data circulates in several
  re-encoded/relabelled forms; we trace to UCI and document every quirk.
- **Don't merge across problems:** UCI (clinical exam) and BRFSS/NHANES (survey)
  measure different things with different targets — combining them would be a
  silent methodological error. They become **separate tracks**.
- **External validation ≠ a bigger test split:** the right move is a *different
  cohort, same schema* (UCI Hungarian/VA), accepting that performance may drop —
  and that the drop is itself a finding.
- **Access ethics are part of engineering:** MIMIC-IV's credentialing is a
  feature, not an obstacle; we treat it as a gated future track.
