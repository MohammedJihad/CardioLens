import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TickDivider } from "@/components/tick-divider";
import { Card } from "@/components/ui/card";
import { CardTable } from "@/components/transparency/card-table";
import { ReportCard } from "@/components/transparency/report-card";
import Link from "next/link";
import { SITE } from "@/lib/site";
import { reports } from "@/data/reports";

export const metadata: Metadata = { title: "Transparency" };

/**
 * /transparency renders the FROZEN report docs — reports/model_card.md and
 * reports/data_card.md — faithfully as web sections. Every claim, number, and
 * limitation is preserved exactly; only banned surface tokens (e.g. the words
 * "diagnosis"/"sick"/"diagnostic"/"clinically validated") are reworded into the
 * site's allowed vocabulary per the CLAUDE.md red line. No claim is added or
 * changed; nothing appears here that isn't in those two documents (plus the
 * methodology/downloads copy from copy.md).
 */

function H3({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="mt-s7 font-display text-xl leading-snug text-ink">{children}</h3>
  );
}

function Lead({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-s3 max-w-measure text-base leading-normal text-muted">{children}</p>
  );
}

function Bullets({ items }: { items: React.ReactNode[] }) {
  return (
    <ul className="mt-s3 max-w-measure list-disc space-y-s2 pl-s5 text-base leading-normal text-muted">
      {items.map((it, i) => (
        <li key={i}>{it}</li>
      ))}
    </ul>
  );
}

const METHODOLOGY = [
  {
    title: "Leakage-free cross-validation",
    detail: "the score isn’t borrowed from the answer.",
  },
  { title: "Target-inversion fix", detail: "a labeling bug found and corrected." },
  {
    title: "Harmonized encodings",
    detail: "cohorts made comparable before testing.",
  },
];

const DOWNLOADS = [
  { label: "Download model card", detail: "reports/model_card.md" },
  { label: "Download data card", detail: "reports/data_card.md" },
  { label: "View raw metrics", detail: "reports/metrics.json" },
  { label: "Open the repository", detail: "the full reproducible project" },
];

export default function TransparencyPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="Open by default"
        headline="The model card and data card, in full."
        intro="What the model is, what it was built on, and the choices that shaped it — rendered as readable web pages, straight from the project's reports."
      />

      {/* ============================ MODEL CARD ============================ */}
      <TickDivider className="my-s8" />
      <SectionHeader
        eyebrow="Model card"
        headline="What the model is."
        intro="Architecture, training data, intended use, and known limitations."
      />

      <H3>Overview</H3>
      <Lead>
        A calibrated <strong className="text-ink">Random Forest</strong> classifier
        (selected from the default candidate set by stratified cross-validation)
        that estimates a model probability for the heart-disease research label
        from 13 routine clinical features. Built as a reproducible, educational
        data-science project.
      </Lead>

      <H3>Intended use</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Intended:</strong> learning, portfolio
            demonstration, exploring clinical-ML evaluation and explainability on a
            public dataset.
          </>,
          <>
            <strong className="text-ink">Out of scope:</strong> clinical use,
            screening, triage, or any real clinical or individual health decision.
            This is <strong className="text-ink">not</strong> a medical device.
          </>,
        ]}
      />

      <H3>Data</H3>
      <Lead>
        UCI Cleveland Heart Disease — 302 records after de-duplication, 45.7%
        positive (disease). Target corrected for a known label inversion (see{" "}
        <code>data/README.md</code>). The dataset is small, single-centre, decades
        old, and not representative of any current population.
      </Lead>

      <H3>Model selection</H3>
      <div className="mt-s5">
        <CardTable
          caption="Stratified 5-fold cross-validation on the training split."
          headers={["Model", "CV ROC-AUC", "CV recall"]}
          rows={[
            ["Dummy (baseline)", "0.500", "0.000"],
            ["Logistic Regression", "0.906 ± 0.040", "0.800"],
            ["SVM (RBF)", "0.907 ± 0.042", "0.818"],
            ["MLP", "0.859 ± 0.063", "0.773"],
            [
              { text: "Random Forest", strong: true },
              { text: "0.910 ± 0.038", strong: true },
              "0.809",
            ],
            ["HistGradientBoosting (opt-in)", "0.869 ± 0.040", "0.782"],
          ]}
        />
      </div>
      <Lead>
        The default candidate set is Dummy, Logistic Regression, SVM, MLP, and
        Random Forest; HistGradientBoosting is an optional opt-in model
        (<code>config.INCLUDE_HISTGB</code>, off by default for reliable training).
        Logistic Regression, SVM, and Random Forest are statistically tied (their
        intervals overlap). Random Forest was chosen on the top mean AUC, but a
        simple, interpretable Logistic Regression would be an equally defensible
        production choice on data this size.
      </Lead>

      <H3>Held-out test performance</H3>
      <div className="mt-s5 max-w-[32rem]">
        <CardTable
          caption="Held-out test performance — 61 patients, threshold = 0.5."
          headers={["Metric", "Value"]}
          rows={[
            ["ROC-AUC", "0.892"],
            ["PR-AUC", "0.853"],
            ["Accuracy", "0.787"],
            ["Balanced accuracy", "0.781"],
            ["Precision", "0.800"],
            [
              { text: "Recall / sensitivity", strong: true },
              { text: "0.714", strong: true },
            ],
            ["Specificity", "0.848"],
            ["F1", "0.755"],
            ["Log loss (probabilities)", "0.425"],
            ["Brier score", "0.137"],
          ]}
        />
      </div>
      <Lead>
        Confusion matrix: TP = 20, <strong className="text-ink">FN = 8</strong>{" "}
        (missed positive-label cases), TN = 28, FP = 5.
      </Lead>

      <H3>Key limitations</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Tiny test set (61 rows):</strong> point
            metrics carry wide uncertainty; treat the CV ranges as more reliable
            than any single test number.
          </>,
          <>
            <strong className="text-ink">8 false negatives</strong> at the default
            threshold — in a real screening setting you would lower the decision
            threshold to raise sensitivity, trading away specificity. The threshold
            here is not clinically tuned.
          </>,
          <>
            <strong className="text-ink">Dataset shift:</strong> trained on one
            historical cohort. Retrospective external-cohort validation was
            performed on UCI Hungarian, VA Long Beach, and Switzerland; the model
            still has no prospective, contemporary, or clinical validation.
          </>,
          <>
            Not assessed for fairness across subgroups beyond what the small sample
            allows.
          </>,
        ]}
      />

      <H3>Explainability</H3>
      <Lead>
        <strong className="text-ink">Global:</strong> permutation importance
        (model-agnostic, deployed model) and SHAP (TreeExplainer on the
        uncalibrated RF — TreeExplainer cannot run on the{" "}
        <code>CalibratedClassifierCV</code> wrapper directly). Both rank number of
        major vessels (<code>ca</code>), chest pain type (<code>cp</code>), and{" "}
        <code>thal</code> as the strongest drivers — consistent with the dataset’s
        predictive patterns and with the project’s earlier model reports.{" "}
        <strong className="text-ink">Local:</strong> per-patient explanations via
        marginal contributions on the deployed model (
        <code>src/patient_report.py</code>). All explanations are model-based,
        approximate, and <strong className="text-ink">not causal</strong>; they are
        not medical advice.
      </Lead>

      <H3>Evaluation depth (statistical honesty)</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Confidence intervals (bootstrap, 2000):</strong>{" "}
            ROC-AUC 0.892 [0.805, 0.961]; sensitivity 0.714 [0.542, 0.879];
            specificity 0.849 [0.710, 0.964]. Intervals are wide because the test
            set is small.
          </>,
          <>
            <strong className="text-ink">Nested CV:</strong> ROC-AUC 0.913 ± 0.047
            (unbiased); Logistic Regression selected in 4/5 outer folds — the
            interpretable model is competitive on this data.
          </>,
          <>
            <strong className="text-ink">Threshold:</strong> default 0.5 is not
            clinical. A cost-sensitive threshold (FN weighted 5× FP) is selected on
            training out-of-fold data only (no test leakage) → 0.20; on the held-out
            test it gives sensitivity 1.00, specificity 0.61.
          </>,
          <>
            <strong className="text-ink">Calibration:</strong> compared on training
            OOF (primary). Isotonic had the lowest Brier (0.119) but a much worse
            log-loss (0.65 vs ~0.39), suggesting over-fit; methods are close and
            unstable, so no method is decisively best (deployed isotonic is
            defensible, sigmoid/none equally reasonable).
          </>,
          <>
            <strong className="text-ink">Decision curve:</strong> positive net
            benefit vs treat-all / treat-none across ~0.05–0.60 (educational framing
            only).
          </>,
          <>
            <strong className="text-ink">Error analysis:</strong> 8 false negatives —
            some borderline near 0.5 (0.43–0.48), others lower-confidence
            (0.23–0.30); descriptive only, too few for conclusions.
          </>,
          <>
            <strong className="text-ink">Learning curve:</strong> validation AUC
            plateaus → more data helps only modestly; ~300 rows is the binding limit.
          </>,
        ]}
      />

      <H3>Subgroup performance (exploratory, out-of-fold)</H3>
      <Lead>
        Computed on out-of-fold predictions across all 302 patients (not the tiny
        test split), with wide CIs — exploratory only, not a fairness verdict.
      </Lead>
      <div className="mt-s5">
        <CardTable
          caption="Exploratory subgroup performance (out-of-fold)."
          headers={["Subgroup", "n", "Disease rate", "OOF ROC-AUC", "Recall", "Specificity"]}
          rows={[
            ["Overall", "302", "0.46", "0.903", "0.783", "0.866"],
            ["Female", "96", "0.25", "0.922", "0.750", "0.972"],
            ["Male", "206", "0.55", "0.875", "0.789", "0.783"],
            ["Age < 55", "143", "0.31", "0.934", "0.727", "0.939"],
            ["Age ≥ 55", "159", "0.59", "0.856", "0.809", "0.754"],
          ]}
        />
      </div>
      <Lead>
        Differences are mostly within noise given subgroup sizes and base-rate gaps.
      </Lead>

      <H3>External validation (Phase 5)</H3>
      <Lead>
        The deployed model, trained only on Cleveland, was applied unchanged to
        three independent UCI cohorts (encodings harmonised). Result —{" "}
        <strong className="text-ink">
          discrimination partially transfers, calibration does not
        </strong>
        .
      </Lead>
      <div className="mt-s5">
        <CardTable
          caption="External validation across three independent UCI cohorts."
          headers={["Cohort", "n", "Disease rate", "ROC-AUC", "Brier"]}
          rows={[
            ["Cleveland (internal test)", "61", "0.46", "0.892", "0.137"],
            ["Hungarian", "294", "0.36", "0.857", "0.178"],
            ["VA Long Beach", "200", "0.75", "0.672", "0.339"],
            ["Switzerland", "123", "0.94", "0.810", "0.337"],
          ]}
        />
      </div>
      <Lead>
        ROC-AUC drops on every cohort (VA worst) and Brier worsens sharply
        everywhere, because the model’s top features <code>ca</code>/<code>thal</code>{" "}
        are missing in 83–99% of external rows (imputed with Cleveland’s mode) and
        the base rates differ widely. Honest conclusion: the model would need
        external recalibration/retraining before any use elsewhere.
      </Lead>
      <p className="mt-s3 max-w-measure text-sm leading-normal text-muted">
        See the{" "}
        <Link href="/external" className="text-accent-text">
          External test
        </Link>{" "}
        page for per-feature missingness by cohort (ca{" "}
        {reports.external.missing_range_ca}, thal{" "}
        {reports.external.missing_range_thal}).
      </p>

      <H3>Not intended uses</H3>
      <Lead>
        Not for clinical use, screening of real patients, triage, clinical
        decisions, or any individual health use. Not a medical device. Not
        prospectively validated and with no clinical validation. The external
        validation here is retrospective and educational only.
      </Lead>

      <H3>Version history</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">v0.4 (Phase 5):</strong> external validation
            on UCI Hungarian/VA/Switzerland cohorts — discrimination partially
            transfers, calibration does not; documented honestly.
          </>,
          <>
            <strong className="text-ink">v0.3 (Phase 3):</strong> data card,
            exploratory subgroup analysis, clinical-reporting checklist; model card
            expanded with version history and not-intended uses.
          </>,
          <>
            <strong className="text-ink">v0.2 (Phase 1–2):</strong> leakage-free
            threshold selection, bootstrap CIs, nested CV, calibration comparison,
            decision curve, error analysis, learning curve; global + local
            explainability (permutation, SHAP, marginal local).
          </>,
          <>
            <strong className="text-ink">v0.1 (Phase 0):</strong> reproducible
            pipeline, target-inversion fix, multi-model CV, calibrated Random Forest,
            core evaluation, data-source research &amp; strategy.
          </>,
        ]}
      />

      <H3>Ethical statement</H3>
      <Lead>
        This project is for <strong className="text-ink">educational and research
        purposes only</strong>. It is not a clinical tool and must not replace
        professional medical advice. Reporting follows the spirit of
        clinical-prediction guidance (e.g. TRIPOD+AI) by being explicit about data
        provenance, evaluation, calibration, and limitations.
      </Lead>

      {/* ============================ DATA CARD ============================ */}
      <TickDivider className="my-s8" />
      <SectionHeader
        eyebrow="Data card"
        headline="What it learned from."
        intro="Historical public research data, its features, and its gaps."
      />

      <H3>Identity</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Name:</strong> UCI Heart Disease — Cleveland
            cohort (circulating processed CSV).
          </>,
          <>
            <strong className="text-ink">Source of record:</strong> UCI Machine
            Learning Repository, “Heart Disease” (id 45), DOI 10.24432/C52P4X.
            Original contributors: Janosi, Steinbrunn, Pfisterer, Detrano (1988).
            License <strong className="text-ink">CC BY 4.0</strong>.
          </>,
          <>
            <strong className="text-ink">File in repo:</strong>{" "}
            <code>data/raw/heart_cleveland.csv</code> → cleaned to{" "}
            <code>data/processed/heart_processed.csv</code> by{" "}
            <code>python -m src.data</code>.
          </>,
        ]}
      />

      <H3>Size &amp; composition</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Rows:</strong> 303 raw → 302 after removing
            1 exact duplicate.
          </>,
          <>
            <strong className="text-ink">Columns:</strong> 13 clinical features + 1
            target.
          </>,
          <>
            <strong className="text-ink">Class balance:</strong> 45.7% disease (138
            disease / 164 no-disease) — roughly balanced.
          </>,
        ]}
      />

      <H3>Features</H3>
      <Lead>
        Numeric: <code>age</code>, <code>trestbps</code> (resting BP),{" "}
        <code>chol</code> (cholesterol), <code>thalach</code> (max HR),{" "}
        <code>oldpeak</code> (ST depression). Categorical: <code>sex</code>,{" "}
        <code>cp</code> (chest pain type), <code>fbs</code> (fasting blood sugar &gt;
        120), <code>restecg</code>, <code>exang</code> (exercise angina),{" "}
        <code>slope</code>, <code>ca</code> (major vessels 0–4), <code>thal</code>.
        Full definitions in <code>dataset_description.md</code>.
      </Lead>

      <H3>Target</H3>
      <Lead>
        <code>heart_disease</code> — <strong className="text-ink">1 = disease
        present, 0 = absent</strong>. Derived per-source: the circulating Cleveland
        CSV ships an inverted binary label, corrected with{" "}
        <code>heart_disease = 1 − target</code> (verified by exploratory consistency
        checks — lower max-HR, higher oldpeak, more exercise angina all track the
        diseased group; see <code>data/README.md</code>). Original UCI files
        (<code>num</code> 0–4) instead use <code>(num &gt; 0)</code>.
      </Lead>

      <H3>Missing values</H3>
      <Lead>
        The circulating CSV has no explicit missing cells, but the pipeline still
        imputes (median / mode) because the original UCI files use <code>?</code> for
        missing <code>ca</code>/<code>thal</code>, and external cohorts
        (Hungarian/VA/Switzerland) have substantial missingness in exactly those
        high-importance fields.
      </Lead>

      <H3>Known bias &amp; representativeness</H3>
      <Bullets
        items={[
          <>
            <strong className="text-ink">Single centre, 1988, ~300 patients</strong> —
            not representative of any current or general population.
          </>,
          <>
            <strong className="text-ink">Subgroup imbalance:</strong> females are
            under-represented (~32%) and have a much lower disease rate here (~25%)
            than males (~55%); age skews older.
          </>,
          <>Referral/selection bias typical of a cardiology-clinic cohort.</>,
        ]}
      />

      <H3>Provenance caveats</H3>
      <Lead>
        Many re-encoded/relabelled copies of “Cleveland” circulate (different{" "}
        <code>cp</code>, <code>slope</code>, <code>thal</code> codings; sometimes
        inverted targets). This project traces to UCI, documents the inversion, and
        harmonises encodings via <code>src/schema.py</code> before any cross-cohort
        use.
      </Lead>

      <H3>Why this dataset is not enough for clinical deployment</H3>
      <Lead>
        Too small for stable estimates (wide CIs), decades old, single-cohort, no
        external validation here, and the most predictive features (<code>ca</code>,{" "}
        <code>thal</code>) are often unrecorded elsewhere. Suitable for{" "}
        <strong className="text-ink">education and method demonstration only</strong>{" "}
        — never for clinical use or individual clinical decisions.
      </Lead>

      {/* ====================== METHODOLOGY HIGHLIGHTS ====================== */}
      <TickDivider className="my-s8" />
      <SectionHeader
        eyebrow="Methodology highlights"
        headline="The choices that matter."
      />
      <div className="mt-s6 grid gap-s4 md:grid-cols-3">
        {METHODOLOGY.map((m) => (
          <Card key={m.title} className="p-s5">
            <h3 className="font-display text-lg text-ink">{m.title}</h3>
            <p className="mt-s2 text-sm leading-normal text-muted">{m.detail}</p>
          </Card>
        ))}
      </div>

      {/* ============================ DOWNLOADS ============================ */}
      <TickDivider className="my-s8" />
      <SectionHeader eyebrow="Downloads" headline="Take the receipts." />
      <div className="mt-s6 grid gap-s4 sm:grid-cols-2">
        {DOWNLOADS.map((d) => (
          <ReportCard
            key={d.label}
            label={d.label}
            detail={d.detail}
            href={SITE.repoUrl}
          />
        ))}
      </div>
      <p className="mt-s4 font-mono text-2xs text-muted">
        Repository links currently resolve to a placeholder — the repository URL is
        wired in by the project owner (see <code>lib/site.ts</code>).
      </p>

      <p className="mt-s8 border-t border-border pt-s5 font-mono text-2xs leading-normal text-muted">
        Everything here is descriptive of a research model on historical public
        research data.
      </p>
    </div>
  );
}
