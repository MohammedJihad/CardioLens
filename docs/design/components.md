# CardioLens — Component Inventory (Phase A)

> Purpose + token usage for every component in `docs/WEBSITE_PLAN.md`. **No code
> yet** — this is the contract the later phases build against. Token names refer to
> the semantic aliases in `tokens.css` / `tokens.ts`.
>
> **The signature is the *lens / instrument* language**: the score gauge is the
> aperture, and a recurring **hairline tick scale** (the measurement motif) appears
> in the gauge, section dividers, and chart axes. Boldness lives only in the gauge;
> everything else stays quiet and disciplined.

---

## Layout & chrome

### `Navigation`
- **Purpose:** Persistent top bar — wordmark, the 7 page links, theme toggle. Same
  order on every page (a11y: consistent navigation).
- **Tokens:** `--bg-surface` (subtle blur over `--bg`), `--border` bottom hairline,
  `--text` links, `--accent-text` for `aria-current`, `--font-mono` for the
  wordmark, `--z-sticky`, `--shadow-xs` on scroll. Focus: `--focus-ring`.
- **Notes:** Skip link first in DOM. Targets ≥ 24px. Collapses to a menu under `md`.

### `DisclaimerBanner`
- **Purpose:** Always-present "educational ML demo — not medical advice" line. The
  single most important piece of chrome on the site.
- **Tokens:** `--bg-subtle` fill, `--text` / `--text-muted`, `--border` bottom,
  `--font-mono` `--text-2xs` `--tracking-eyebrow` for the label. **No alarm color** —
  this is calm, not a warning.
- **Notes:** Sticky directly under the nav. Dismiss collapses to a compact pill but
  is never permanently removable. `role="note"`.

### `Footer`
- **Purpose:** Tagline, the "inputs are not stored" honesty line, link columns,
  repository link.
- **Tokens:** `--bg-subtle`, `--border` top hairline, `--text-muted` body,
  `--accent-text` links, `--font-display` for the tagline line.

### `SectionHeader` (rhythm primitive)
- **Purpose:** Encodes the page rhythm: eyebrow → headline → plain intro. Used at
  the top of every section.
- **Tokens:** eyebrow = `--font-mono` `--text-xs` `--tracking-eyebrow`
  `--accent-text`; headline = `--font-display` `--text-3xl`/`--text-2xl`
  `--leading-snug` `--text`; intro = `--font-body` `--text-lg` `--text-muted`
  `--measure` max-width.

### `TickDivider` (signature motif)
- **Purpose:** The measurement-scale rule between sections — a hairline with short
  ticks, echoing the gauge scale. Ties the whole system to the lens identity.
- **Tokens:** `--border` line, `--border-strong` ticks, `--space-8` vertical
  rhythm. Decorative → `aria-hidden`.

---

## Hero & narrative

### `HeroSection`
- **Purpose:** The thesis. Headline + subhead + dual CTA, with a quiet static SVG
  **gauge-arc lattice** as ambient backdrop (the lens, abstracted — default to
  static; subtle parallax only if motion is allowed).
- **Tokens:** `--font-display` `--text-5xl`/`--text-4xl` `--tracking-tight`
  `--leading-tight`; subhead `--text-lg` `--text-muted`; backdrop strokes use
  `--gauge-low`/`--gauge-mid`/`--gauge-high` at low opacity over `--bg`.
- **Notes:** Backdrop is decorative SVG, never a matplotlib PNG. Respects
  `prefers-reduced-motion`.

### `TrustStrip`
- **Purpose:** Three honest headline stats (from reports) with one caveat line.
- **Tokens:** numbers `--font-mono` `--text-2xl` (tabular figures) `--text`; labels
  `--text-sm` `--text-muted`; dividers `--border`.

### `StoryBeat`
- **Purpose:** The build → explain → stress-test trio on Home.
- **Tokens:** numbered eyebrow `--font-mono` `--accent-text`; uses `SectionHeader`;
  `--shadow-sm` on the optional inset figure.

---

## The score gauge (signature) & demo

### `ModelScoreGauge`  ★ signature element
- **Purpose:** Render a single model score as a magnitude on a calibrated arc.
  Teal → amber → coral encodes **score magnitude only — never a health verdict.**
- **Tokens:** arc gradient = `--gauge-low` → `--gauge-mid` → `--gauge-high`; track =
  `--gauge-track`; readout = `--font-mono` `--text-4xl` (tabular); label =
  `--font-mono` `--tracking-eyebrow` `--text-muted`; tick scale = `--border-strong`;
  sweep animation = `--dur-slow` `--ease-gauge` (0 → score), disabled under reduced
  motion (jumps straight to value).
- **Notes:** Always paired with the fixed magnitude caption from `copy.md`.
  Accessible: `role="img"` + `aria-label` stating the numeric score and that it is a
  model score on research data. Never renders a banned word.

### `InputForm`
- **Purpose:** Grouped research-style inputs (Demographics / Vitals & labs / ECG &
  exercise). The only component that talks to the live API.
- **Tokens:** fields `--bg-surface` + `--border`, focus `--focus-ring`
  `--border-focus`; legends `--font-mono` `--tracking-eyebrow`; hints `--font-mono`
  `--text-2xs` `--text-muted`; error `--danger-text` + icon (never color-only).
- **Notes:** Native labels for every field; `aria-invalid` + `aria-describedby` on
  errors; targets ≥ 44px. Privacy line always visible.

### `PresetPicker`
- **Purpose:** Load low / borderline / high model-score patterns.
- **Tokens:** segmented control on `--bg-subtle`, selected = `--primary` +
  `--text-onprimary`; `--radius-sm`. Helper text clarifies presets are illustrative,
  not real people.

### `ResultCard`
- **Purpose:** Houses the gauge, the above/below-threshold band, the explanation,
  and the plain-language box.
- **Tokens:** `--bg-surface`, `--ring-inset`, `--shadow-md`, `--radius-lg`,
  `--space-6` padding. Band chip uses `--bg-subtle` + `--text` (no red/green pass-fail
  coloring — neutral by design).

### `FactorBars` / `FeatureImpactChart`
- **Purpose:** Show which inputs pushed a score up vs down (model-based explanation).
- **Tokens:** up bars `--gauge-high` (muted), down bars `--gauge-low`; baseline
  `--border-strong`; labels `--font-body` `--text-sm`; values `--font-mono`.
- **Notes:** Caption always present: "within this model… not causal." Color is
  backed by a directional label + sign, never color alone.

### `PlainLanguageBox`
- **Purpose:** "What this means" in plain language — the human translation of the
  score.
- **Tokens:** `--bg-subtle`, left keyline `--accent` `--border-strong-w`,
  `--text` body, `--radius-md`.

---

## Reports & charts (Recharts, from static JSON)

> All charts read `reports-summary.json`. Shared chart tokens: gridlines `--border`,
> axes `--font-mono` `--text-2xs` `--text-muted`, series from the palette below,
> tooltip `--bg-surface` + `--shadow-md` + `--border`. Every chart ships a one-line
> honest caveat beneath it.

### `MetricCard`
- **Purpose:** One headline number + label + sub + tooltip; grid on `/results`.
- **Tokens:** value `--font-mono` `--text-3xl` (tabular) `--text`; label
  `--font-mono` `--tracking-eyebrow` `--accent-text`; `--bg-surface` `--ring-inset`
  `--radius-md` `--shadow-sm`.

### `ConfusionMatrix`
- **Purpose:** TP/FP/TN/FN counts at the operating threshold.
- **Tokens:** cells `--bg-subtle`→`--primary` sequential (single-hue, intensity =
  count); text auto-contrast `--text` / `--text-onprimary`; `--font-mono` counts.
  **No red/green** — neutral navy ramp avoids pass/fail framing.

### `RocPrChart` / `LearningCurveChart`
- **Purpose:** ROC & PR curves; learning curve.
- **Tokens:** primary series `--primary`, secondary `--accent`, reference diagonal
  `--border-strong` dashed; CI band fill = `--accent` at low opacity.

### `ExternalValidationChart`
- **Purpose:** AUC across internal + external cohorts (the drop).
- **Tokens:** bars `--primary`, the internal baseline highlighted with `--accent`;
  cohort labels `--font-mono`. Drives the `/external` GSAP story states.

### `MissingFeatureChart`
- **Purpose:** Per-cohort missingness of the model's strong features.
- **Tokens:** bars `--gauge-mid` (amber = "caution / gap", non-text use only);
  `--border` axis.

### `ThresholdTradeoffChart`
- **Purpose:** Sensitivity vs specificity across thresholds; marks the selected
  operating point.
- **Tokens:** sensitivity `--accent`, specificity `--primary`, selected-threshold
  marker `--gauge-high` dot + `--font-mono` callout.

### `CalibrationMeter`
- **Purpose:** Calibration curve / Brier readout — predicted vs observed.
- **Tokens:** ideal line `--border-strong` dashed; observed `--primary`; deviation
  shading `--gauge-mid` low-opacity.

### `ReportCard`
- **Purpose:** Link/download tile for model card, data card, raw metrics, repo.
- **Tokens:** `--bg-surface` `--ring-inset` `--radius-md`, icon `--accent`, hover
  `--bg-subtle`, `--shadow-sm`→`--shadow-md` on hover.

---

## Responsible-AI & utility

### `LimitationsGrid` / `CanCannotCards`
- **Purpose:** Two-column "can / cannot" honesty cards on `/about`.
- **Tokens:** can-column keyline `--accent`; cannot-column keyline `--text-muted`
  (deliberately *not* red — limits are neutral facts, not errors); `--bg-surface`
  `--ring-inset` `--radius-md`.

### `Badge`
- **Purpose:** Small status/marker chips ("Above threshold", "External cohort",
  "Internal"). Neutral, informational.
- **Tokens:** `--bg-subtle` fill, `--text` or `--accent-text`, `--font-mono`
  `--text-2xs` `--tracking-wide`, `--radius-full`. Never used to signal good/bad
  health outcomes.

### `Button` (shadcn primitive, themed)
- **Variants:** primary = `--primary`/`--primary-hover` + `--text-onprimary`;
  secondary = `--bg-surface` + `--border` + `--text`; ghost = transparent + `--text`.
- **Tokens:** `--radius-sm`, `--dur-fast` `--ease-standard` transitions, focus
  `--focus-ring` `--border-focus`. Min target 44px. Label = the literal action.

### `Tooltip` & `Dialog` (shadcn primitives, themed)
- **Tokens:** `--bg-surface`, `--border`, `--shadow-md`/`--shadow-lg`, `--text`,
  `--z-overlay`. Dialog uses native focus-trap semantics; reduced-motion shortens
  enter/exit.

### `ThemeToggle`
- **Purpose:** Light/dark switch; defaults to system, override persists in
  `localStorage` (a UI preference only — never any medical input).
- **Tokens:** `--text`, `--accent` active, `--focus-ring`. Sets `data-theme` to
  flip the token sets in `tokens.css`.
