# CardioLens — Brand

> Phase A artifact. This defines the name, voice, and positioning that every
> page's copy and visual design must hold to. All wording obeys the safe-wording
> rules in `AGENTS.md` / `CLAUDE.md`.

---

## Name — confirmed: **CardioLens**

The working name holds up, and it earns its keep. A **lens** is an instrument you
look *through* to see something more clearly — it does not change the thing it
observes, and it has a focus, a limit, and an edge beyond which it blurs. That is
exactly the honest framing this project needs: we are presenting a *frozen* model
as a calibrated instrument for **reading research data**, not a device that judges
a person. "Cardio" anchors the domain without claiming the clinic.

The lens metaphor is also the visual signature (see `components.md`): the score
gauge is the aperture, hairline tick marks are the measurement scale, and "focus"
language runs through the copy ("what the model brought into focus").

**Two alternative names** (if you'd rather not ship CardioLens):

1. **Cardiograph Lab** — leans fully into "research-lab case study." Warm,
   academic, clearly retrospective. Slightly longer; less of a product feel.
2. **Beat & Margin** — editorial and memorable; "margin" nods to uncertainty,
   error bars, and the honest limits of the model. More literary, less literal —
   a small risk if first-time visitors want instant clarity on the subject.

Recommendation: **keep CardioLens.** It is the clearest fit for the instrument
identity and reads well as a portfolio case-study title.

---

## Tagline

**Primary:** *A calibrated lens on heart-disease research data.*

**Alternates (same register, pick per surface):**
- *Read the model, not the verdict.*
- *An educational ML demo — honest about what it sees, and what it can't.*

Avoid anything that implies a personal health outcome. The tagline sells the
*instrument and the honesty*, never a result.

---

## Positioning (one paragraph)

CardioLens is an **educational ML demo** that re-presents a finished, frozen
heart-disease machine-learning study as a premium, readable case study. It shows
how a model trained on **historical public research data** behaves — the internal
performance, what happens when the same model meets new cohorts it never saw, and
where its calibration holds or breaks — and lets you run one **live, non-storing**
input pattern through it to see a **model score** and a **model-based explanation**.
It is built for curious readers, students, and engineers who want to understand a
real model's strengths *and* its limits. It is **not medical advice** and **not a
clinical tool**; every number on the site comes straight from the project's
research reports, and every result is framed as a model score on research data —
never a statement about any real person.

---

## Tone of voice

The voice is a **precise, generous research narrator**: the person who can explain
a hard result plainly without dumbing it down, and who points at the weak spots
before you have to ask.

**Five rules:**

1. **Calm and exact.** State what is true and stop. No hype, no alarm, no
   exclamation points. The drama lives in the honesty, not the adjectives.
2. **Lead with the caveat, not as an afterthought.** Every claim earns a one-line
   honest qualifier in the same breath ("discrimination partially transfers;
   calibration does not"). Limits are a feature of the voice, not fine print.
3. **Say "model," not "medicine."** We describe what *the model* did to a *score*
   on *research data*. We never describe what is true of a person's body. When
   tempted to write a verdict, write a measurement instead.
4. **Plain verbs, sentence case, active voice.** "See the score," not "Initiate
   assessment." A button names exactly what happens; the result uses the same
   word back to the reader.
5. **Specific beats clever.** Real numbers, real cohort names, real limitations.
   Cleverness is allowed only when it also clarifies.

**Register:** editorial and warm-neutral — closer to a well-written science
feature than to either a corporate dashboard or a hospital pamphlet.

---

## Words we use / words we never use

**Use:** model score · model-estimated probability on research data · educational
ML demo · historical public research data · research-style input pattern ·
model-based explanation · above/below threshold · not causal · not medical advice ·
retrospective educational validation · similar historical research patterns.

**Never render (even dynamically):** diagnosis · disease probability (as clinical
truth) · sick · healthy · "you have heart disease" · "you are safe" · medical
decision · "patient is positive/negative" · clinically validated · medical-grade ·
real-world clinical tool. Explanations always say *"within this model, these inputs
pushed the score up/down"* — never *"this caused heart disease."*

A build-time test greps the rendered output for the banned list and fails on any
match. The brand voice and the test are the same rule, enforced twice.
