# CardioLens — Copy Deck (Phase A, final)

> The safe, final wording for every page in `docs/WEBSITE_PLAN.md`.
>
> **Numbers are never hand-typed.** Anywhere a metric appears it is written as a
> `{{placeholder}}` that is filled at build time from
> `frontend/data/reports-summary.json` (snapshotted from the real files in
> `reports/`). The placeholder names below map to those report fields. If a
> number isn't in the reports, it doesn't go on the site.
>
> All copy obeys the banned-wording rules. The recurring pattern per section is:
> **eyebrow → headline → 1–2 sentence plain intro → visual → one-line honest caveat.**

---

## Global

### Disclaimer banner (persistent, every page)
> **Educational ML demo — not medical advice.** CardioLens shows a model score on
> historical public research data. It is not a medical verdict and not a clinical tool.

- Collapsed label (sticky, compact): `Educational ML demo — not medical advice`
- Dismiss control label: `Got it` (re-openable; never permanently hidden)

### Navigation (labels)
`Home` · `Try the model` · `Results` · `External test` · `Thresholds` ·
`Transparency` · `About`
- Brand wordmark: `CardioLens`
- Skip link: `Skip to main content`
- Theme toggle a11y labels: `Switch to dark theme` / `Switch to light theme`

### Footer
- Tagline line: `A calibrated lens on heart-disease research data.`
- Honest line: `Every number on this site comes from the project's research
  reports. Inputs you try are sent to the model to compute a score and are not
  stored.`
- Column heads: `Explore` · `The science` · `Responsible use`
- Links: `View the code on GitHub` · `Model card` · `Data card` · `Limitations`
- Legal/■ line: `© {{year}} CardioLens · An educational machine-learning case
  study. Not medical advice.`

### Universal caveat snippets (reused under visuals)
- `Model score on research data — not a statement about any person.`
- `Numbers reflect this dataset and this frozen model only.`
- `Not causal — these are associations the model learned.`

---

## `/` — Home

- **Eyebrow:** `EDUCATIONAL ML DEMO`
- **Headline:** `A calibrated lens on a heart-disease model.`
- **Subhead:** `See how one frozen machine-learning model reads historical public
  research data — what it gets right, what it doesn't, and where its confidence
  quietly breaks down.`
- **Primary CTA:** `Try the model`
- **Secondary CTA:** `Read the results`
- **Hero caveat:** `An educational demo. Not medical advice, not a medical verdict.`

### Trust strip (three honest stats, all from reports)
- `ROC-AUC {{metrics.roc_auc}}` — `internal test set, n={{metrics.n_test}}`
- `Sensitivity {{thresholds.sens_selected}} / Specificity
  {{thresholds.spec_selected}}` — `at the {{thresholds.selected}} screening-style threshold`
- `Tested on {{external.n_cohorts}} external cohorts` — `it was never trained on`

> Caveat under strip: `These are model-score metrics on research data, measured
> once on held-out data. Small test set — read the Results page for the full
> picture.`

### Story in three beats
1. **Eyebrow** `BEAT 01 — BUILD`
   **Headline** `A leakage-free model, built carefully.`
   **Intro** `Cross-validation without target leakage, a corrected target
   inversion, and harmonized encodings — so the score reflects the data, not a
   shortcut.`
   **Caveat** `Built on historical public research data only.`
2. **Eyebrow** `BEAT 02 — EXPLAIN`
   **Headline** `Every score comes with its reasons.`
   **Intro** `For any input pattern, the model shows which values pushed its score
   up and which pushed it down — a model-based explanation, not a cause.`
   **Caveat** `Within this model — not a claim about the body.`
3. **Eyebrow** `BEAT 03 — STRESS-TEST`
   **Headline** `Then we tried to break it.`
   **Intro** `We ran the same frozen model on cohorts it had never seen. Its
   ability to rank cases partly survived; its calibrated probabilities did not.`
   **Caveat** `Discrimination partially transfers; calibration does not.`

- **Closing CTA block headline:** `Run one pattern through the lens.`
- **Closing CTA sub:** `A single input pattern, scored live and explained. Nothing
  you enter is stored.`
- **Closing CTA button:** `Try the model`

---

## `/try` — Live demo

- **Eyebrow:** `LIVE · EDUCATIONAL DEMO`
- **Headline:** `Run an input pattern through the model.`
- **Subhead:** `Enter a research-style input pattern, or load a preset, to see the
  model score and a model-based explanation. This is the one page that talks to
  the live model.`
- **Privacy line (always visible near the form):** `Inputs are sent to the model
  to compute a score and are not stored — no account, no database, no tracking of
  what you enter.`

### Form
- Section legends: `Demographics` · `Vitals & labs` · `ECG & exercise`
- Preset picker label: `Or start from a preset pattern`
- Preset names: `Low model score` · `Borderline pattern` · `High model score`
- Preset helper: `Presets are illustrative research-style patterns, not real
  people.`
- Field hint format (mono): `{{field.range}} · {{field.unit}}`
- Submit button: `See the model score`
- Reset button: `Clear inputs`
- While loading: `Scoring the pattern…`

### Result card
- Gauge label (above readout): `MODEL SCORE`
- Gauge readout sub: `model-estimated probability on research data`
- Band line (template): `{{band}} the {{thresholds.selected}} threshold`
  - bands render only as: `Above` / `Below`
- Magnitude caption (under gauge, fixed): `The gauge shows the size of the model
  score only — teal to coral is low to high magnitude, not a health verdict.`
- Explanation heading: `What moved this score`
- Explanation lead: `Within this model, these inputs pushed the score up or down.
  This is a model-based explanation — it is not causal and not medical advice.`
- Factor row (template, positive): `{{feature}} — pushed the score up`
- Factor row (template, negative): `{{feature}} — pushed the score down`
- Plain-language box heading: `What this means`
- Plain-language body: `A higher model score means this input pattern looks more
  like the historical research patterns the model associates with heart disease in
  its training data. It is not a medical verdict, and it does not describe you. To
  understand your own health, talk to a qualified clinician.`

### `/try` states
- **Empty (before first run):** `Enter a pattern or pick a preset, then choose
  “See the model score.”`
- **Validation error (field):** `Enter a value in {{field.range}} for
  {{field.label}}.` (icon + text, `aria-invalid`, red reserved for this only)
- **Validation error (summary):** `Some fields need a valid value before the model
  can score this pattern.`
- **Backend asleep / unreachable:** `The model service is waking up or
  unavailable. The rest of the site still works — try again in a moment, or read
  the Results page meanwhile.`
- **Backend error (5xx):** `The model couldn't score that pattern just now. Nothing
  was stored. Please try again.`
- **Timeout:** `That took too long to score. Try again, or load a preset pattern.`

---

## `/results` — Internal performance

- **Eyebrow:** `INTERNAL EVALUATION`
- **Headline:** `How the model scored on its own test set.`
- **Subhead:** `Measured once on held-out historical research data the model never
  trained on. Honest version: the test set is small, so read these with their
  confidence intervals.`

### Metric cards (labels; values from reports)
- `ROC-AUC` → `{{metrics.roc_auc}}` · sub `ranking ability`
- `PR-AUC` → `{{metrics.pr_auc}}` · sub `precision–recall balance`
- `Sensitivity` → `{{metrics.sensitivity}}` · sub `true-positive rate`
- `Specificity` → `{{metrics.specificity}}` · sub `true-negative rate`
- `F1` → `{{metrics.f1}}` · sub `harmonic mean`
- `Brier` → `{{metrics.brier}}` · sub `calibration error (lower is better)`

### Sections
- **Confusion matrix** — eyebrow `COUNTS` · head `Where it was right and wrong.`
  intro `On {{metrics.n_test}} held-out cases at the operating threshold.`
  caveat `Small sample — single counts move the percentages a lot.`
- **ROC & PR curves** — eyebrow `DISCRIMINATION` · head `Ranking cases across every
  threshold.` caveat `Curves describe ranking, not calibrated probability.`
- **Learning curve** — eyebrow `DATA APPETITE` · head `Would more data help?` caveat
  `Trend on this dataset only.`
- **Confidence intervals** — eyebrow `UNCERTAINTY` · head `How sure are these
  numbers?` intro `Bootstrapped intervals around each metric.` caveat `Wide
  intervals are the honest signal of a small test set.`

---

## `/external` — External validation (scroll story)

- **Eyebrow:** `THE STRESS TEST`
- **Headline:** `What happened on cohorts it had never seen.`
- **Subhead:** `We froze the model and ran it on external research cohorts. This is
  where a model usually tells the truth about itself.`

### Scroll beats
1. **Eyebrow** `STARTING POINT` · **Line** `On its own test set, the model reached
   ROC-AUC {{metrics.roc_auc}}.` · caveat `Internal, held-out research data.`
2. **Eyebrow** `NEW COHORT — HUNGARIAN` · **Line** `Ranking ability held up
   reasonably: ROC-AUC {{external.hungarian.auc}}.` · caveat `Discrimination partly
   transfers.`
3. **Eyebrow** `NEW COHORT — VA` · **Line** `Here it dropped to
   {{external.va.auc}}.` · caveat `Different population, different result.`
4. **Eyebrow** `NEW COHORT — SWITZERLAND` · **Line** `ROC-AUC
   {{external.switzerland.auc}}, but the probabilities drifted.` · caveat
   `Calibration is the first thing to break.`
5. **Eyebrow** `THE CATCH — CALIBRATION` · **Line** `Brier score worsened across
   cohorts ({{external.hungarian.brier}} → {{external.va.brier}}).` · caveat `Good
   ranking can hide bad calibration.`
6. **Eyebrow** `WHY — MISSING FEATURES` · **Line** `Two of the model's strongest
   inputs were {{external.missing_range}} missing in these cohorts.` · caveat
   `The model leaned on signals the new data barely had.`
- **Story conclusion (pinned end card):** `Discrimination partially transfers.
  Calibration does not. That gap is the most important thing on this whole site.`
- Caveat: `Retrospective educational validation on historical public research data.`

---

## `/thresholds` — Threshold trade-off

- **Eyebrow:** `OPERATING POINT`
- **Headline:** `Choosing where to draw the line.`
- **Subhead:** `A model score is a number; a decision needs a threshold. We selected
  {{thresholds.selected}} on out-of-fold data, then evaluated it once — tuned for a
  screening posture, not a clinical one.`

### Sections
- **Trade-off** — eyebrow `SENSITIVITY vs SPECIFICITY` · head `Catch more, or be
  more selective.` intro `At {{thresholds.selected}}: sensitivity
  {{thresholds.sens_selected}}, specificity {{thresholds.spec_selected}}, false
  negatives {{thresholds.fn_selected}}.` caveat `Screening-oriented: it favors
  catching cases over avoiding false alarms.`
- **Calibration** — eyebrow `DO THE PROBABILITIES MEAN ANYTHING?` · head `When a
  score of 0.7 should mean 0.7.` intro `Calibration asks whether the model's
  probabilities match observed frequencies on research data.` caveat `Calibration
  held internally and weakened externally — see the External test.`
- **Pull-quote:** `Screening-oriented, not clinical. A low score here is a
  below-threshold model result — never an all-clear.`

---

## `/transparency` — Model & data cards

- **Eyebrow:** `OPEN BY DEFAULT`
- **Headline:** `The model card and data card, in full.`
- **Subhead:** `What the model is, what it was built on, and the choices that shaped
  it — rendered as readable web pages, straight from the project's reports.`

### Sections
- **Model card** — head `What the model is.` intro `Architecture, training data,
  intended use, and known limitations.`
- **Data card** — head `What it learned from.` intro `Historical public research
  data, its features, and its gaps.`
- **Methodology highlights** — head `The choices that matter.` items:
  - `Leakage-free cross-validation` — `the score isn't borrowed from the answer.`
  - `Target-inversion fix` — `a labeling bug found and corrected.`
  - `Harmonized encodings` — `cohorts made comparable before testing.`
- **Downloads** — head `Take the receipts.` labels: `Download model card` ·
  `Download data card` · `View raw metrics` · `Open the repository`
- Caveat: `Everything here is descriptive of a research model on historical public
  research data.`

---

## `/about` — Limitations, privacy, story

- **Eyebrow:** `HONEST LIMITS`
- **Headline:** `What CardioLens can and can't do.`
- **Subhead:** `A short, plain account of where this educational demo is useful and
  where it is not.`

### Can / cannot cards
- **Can:** `Show how one frozen model scores research-style input patterns.` ·
  `Explain which inputs moved a given score, within the model.` · `Demonstrate that
  performance drops on unseen cohorts.` · `Make a real ML evaluation readable.`
- **Cannot:** `Make any claim about a real person's health or give a verdict about a
  body.` · `Give medical advice or a clinical recommendation.` · `Promise its
  probabilities hold outside this research data.` · `Replace a conversation with a
  qualified clinician.`

### When to seek real help
- **Head:** `If you're worried about your heart.`
- **Body:** `This is an educational demo, not a source of medical advice. If you
  have symptoms or concerns, contact a qualified clinician or your local emergency
  number. CardioLens cannot help with an urgent situation.`

### Privacy
- **Head:** `Your inputs are not stored.`
- **Body:** `The `/try` page sends your input pattern to the model to compute a
  score and a model-based explanation, then forgets it. No accounts, no database,
  no analytics of what you enter, no cookies tracking your medical inputs.`

### Project story / stack
- **Head:** `Why this exists.`
- **Body:** `CardioLens turns a finished, frozen heart-disease ML study into a
  readable case study — built to show evaluation done honestly, limitations and
  all.`
- **Stack line:** `Static Next.js front end · existing FastAPI model service ·
  charts drawn from the project's real research reports.`
- **GitHub CTA:** `View the code on GitHub`

---

## Microcopy & reusable states

- **Generic empty state:** `Nothing to show here yet.`
- **Generic load state:** `Loading…`
- **Chart no-data:** `This chart's data isn't available in the report snapshot.`
- **Offline/asleep (global):** `Some live features are resting. Static pages and
  results are fully available.`
- **Tooltip on every metric:** `Measured on historical public research data with
  this frozen model. Not a clinical figure.`
- **404 head / body:** `That page isn't here.` / `Try the navigation above to get
  back to the case study.`
- **Cookie/consent (if ever needed):** Not used — CardioLens stores no personal
  inputs and sets no tracking cookies.
