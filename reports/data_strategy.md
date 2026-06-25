# Data Strategy — Heart Disease Risk Screening ML System

**Phase 0 deliverable.** Defines how datasets are used across the project. Built
on `data_source_research.md`. **Phase 0 added no new training or model
experiments; existing artifacts were preserved.** Outputs are always **model
scores for educational use only**, never diagnoses.

## Guiding principle
Keep distinct *problems* as distinct *experiments*. A clinical-exam tabular model
(UCI) and a population survey risk-factor model (BRFSS/NHANES) answer different
questions on different data — they are **never merged**. Each track is honest
about its own scope and limits.

---

## Track A — Clinical tabular model  ✅ *active*

**Data:** UCI Cleveland (train/test, already integrated) + other UCI cohorts
(Hungarian, VA Long Beach, Switzerland) for **external validation**.

**Goal:** strengthen the existing clinical-tabular model — better evaluation,
calibration, explainability, and a genuine external-validation signal — while
keeping the schema aligned across cohorts.

**Plan:**
1. Keep Cleveland as the primary development cohort (302 rows after cleaning).
2. Align the **same 14-column schema** across UCI cohorts; harmonise encodings.
3. Train on Cleveland; **externally validate on Hungarian** (primary), then VA
   Long Beach (secondary); treat Switzerland cautiously (severe `chol` missingness).
4. Report external metrics + calibration separately; **expect and document
   performance drop**, especially where `ca`/`thal` are unrecorded.
5. **Do not claim clinical validity.** This remains educational.

**Per-dataset target & encoding contract (already scaffolded in Phase 0 cleanup):**
- Target derivation is **per source**, never a global flip. The active Kaggle
  Cleveland CSV uses `heart_disease = 1 - target` (inverted binary); original UCI
  cohorts use `heart_disease = (num > 0)`. Enforced in `src/dataset_registry.py`.
- Categorical **encodings differ**: training data is recoded (cp 0-3, slope 0-2,
  thal 0-3) while original UCI uses cp 1-4, slope 1-3, thal {3,6,7}. Translation
  maps live in `src/schema.py` and must be applied before validation. The `thal`
  value `0` in the Kaggle CSV is ambiguous and will be resolved/documented at the
  start of Phase 1.

**Why it's strong:** external validation on a different cohort with the same
schema is the single most credible thing a small-data clinical project can show —
and the honest "our top features aren't recorded elsewhere" finding demonstrates
real understanding of generalisation.

---

## Track B — Public-health risk-factor model  🔭 *separate experiment*

**Data:** CDC **BRFSS 2015** Heart Disease Health Indicators (primary), or
**NHANES** (alternative, measured variables). Used **only as a standalone model**
— never combined with UCI.

**Goal:** broader, population-level **risk-factor** modelling on survey data,
explicitly framed as a different problem from the clinical-tabular track.

**Plan:**
1. Build as an isolated sub-project (e.g. `experiments/track_b_brfss/`).
2. Define the target precisely (BRFSS `HeartDiseaseorAttack` from `_MICHD`).
3. Handle the heavy **class imbalance** (~9.4% positive) with appropriate
   metrics (PR-AUC, recall) and resampling/weighting — not raw accuracy.
4. Keep its own README, data card, and limitations (self-report, recall bias,
   cross-sectional).
5. **Label clearly** as a separate experiment; never report Track A and Track B
   numbers as if comparable.

**Why kept separate:** different features, different target definition, different
population and collection method. Merging would be a silent leakage/validity
error. Demonstrating that you *chose not to merge* is itself a maturity signal.

**NHANES note:** richer *measured* labs/exams but requires multi-component
assembly (merge by `SEQN`) and correct **survey-weight** handling — higher
effort, deferred unless measured variables are specifically wanted.

---

## Track C — Advanced EHR (stretch)  💤 *gated, future only*

**Data:** **MIMIC-IV** (PhysioNet) — restricted, credentialed access.

**Goal:** a future extension into real longitudinal ICU/EHR data.

**Hard preconditions (all required before any implementation):**
- Credentialed PhysioNet account, **and**
- Completed CITI "Data or Specimens Only Research" training, **and**
- Signed PhysioNet Credentialed Health Data Use Agreement (License 1.5.0).

**Rules:** do **not** implement, download, or simulate results until access is
genuinely in place. **Never fake access or fabricate MIMIC results.** Until then,
this track exists only as a documented aspiration with no code dependency.

---

## Cross-track decisions (summary)

| Question | Decision |
|---|---|
| Best dataset to use **now** | UCI Cleveland (already integrated) |
| Best **external-validation** dataset | UCI **Hungarian** (same schema, different cohort) |
| Secondary external validation | UCI VA Long Beach |
| Use with caution | UCI Switzerland (severe `chol` missingness) |
| Optional sanity check | Statlog (Heart) — overlaps Cleveland, not independent |
| **Separate** public-health experiment | BRFSS 2015 (Track B); NHANES alternative |
| **Special-access / gated** | MIMIC-IV (Track C) — credentials + DUA required |
| **Avoid entirely** | scraped/identifiable data; unprovenanced CSVs as source of record |
| **Never do** | merge UCI with BRFSS/NHANES; claim clinical validity; invent results |

---

## What this strategy proves to a reviewer
- Understanding of **dataset provenance** and quirks (the inverted Cleveland label).
- Understanding of **target definitions** differing across sources.
- Awareness of **privacy/ethics and access tiers** (open vs CC BY vs credentialed).
- Knowing **why not to merge** heterogeneous datasets.
- A correct notion of **external validation** (different cohort, same schema).
- Honesty about the **limits of small clinical datasets** and survey self-report.
