import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TickDivider } from "@/components/tick-divider";
import { MetricCard } from "@/components/metric-card";
import { ConfusionMatrix } from "@/components/results/confusion-matrix";
import { NotInSnapshot } from "@/components/not-in-snapshot";
import { ChartCaveat } from "@/components/chart-caveat";
import { reports, fmt3 } from "@/data/reports";

export const metadata: Metadata = { title: "Results" };

const m = reports.metrics;

const METRICS = [
  { label: "ROC-AUC", value: fmt3(m.roc_auc), sub: "ranking ability" },
  { label: "PR-AUC", value: fmt3(m.pr_auc), sub: "precision–recall balance" },
  { label: "Sensitivity", value: fmt3(m.sensitivity), sub: "true-positive rate at 0.50" },
  { label: "Specificity", value: fmt3(m.specificity), sub: "true-negative rate at 0.50" },
  { label: "F1", value: fmt3(m.f1), sub: "harmonic mean" },
  { label: "Brier", value: fmt3(m.brier), sub: "calibration error (lower is better)" },
];

export default function ResultsPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="Internal evaluation"
        headline="How the model scored on its own test set."
        intro="Measured once on held-out historical research data the model never trained on. Honest version: the test set is small, so read these with their confidence intervals."
      />

      {/* Metric cards — every value from reports-summary.json metrics.* */}
      <div className="mt-s7 grid gap-s4 sm:grid-cols-2 lg:grid-cols-3">
        {METRICS.map((c) => (
          <MetricCard key={c.label} label={c.label} value={c.value} sub={c.sub} />
        ))}
      </div>
      <ChartCaveat>
        Model-score metrics on historical public research data, measured once on{" "}
        {m.n_test} held-out cases with this frozen model. Not clinical figures.
      </ChartCaveat>

      <TickDivider className="my-s8" />

      {/* Confusion matrix — at the default 0.50 threshold */}
      <SectionHeader
        eyebrow="Counts"
        headline="Where it was right and wrong."
        intro={`On ${m.n_test} held-out cases at the default 0.50 threshold.`}
      />
      <div className="mt-s6 max-w-[40rem]">
        <ConfusionMatrix caption="Counts at the default 0.50 threshold, across the 61-case held-out test set." />
        <ChartCaveat>
          Small sample — single counts move the percentages a lot. Navy intensity
          tracks the count only; it is not a pass/fail color.
        </ChartCaveat>
      </div>

      <TickDivider className="my-s8" />

      {/* ROC & PR — option (b): summary AUCs as stat blocks; no fabricated curve */}
      <SectionHeader
        eyebrow="Discrimination"
        headline="Ranking cases across every threshold."
        intro="The report snapshot carries the summary areas under the ROC and precision–recall curves, but not the point-by-point curve coordinates."
      />
      <div className="mt-s6 grid gap-s4 sm:grid-cols-2">
        <MetricCard label="ROC-AUC" value={fmt3(m.roc_auc)} sub="area under the ROC curve" />
        <MetricCard label="PR-AUC" value={fmt3(m.pr_auc)} sub="area under the precision–recall curve" />
      </div>
      <div className="mt-s5">
        <NotInSnapshot detail="We don't draw a ROC or PR curve here because the per-threshold coordinates aren't in reports-summary.json — only the summary areas above are. We won't invent or interpolate the curve." />
      </div>
      <ChartCaveat>Curves describe ranking, not calibrated probability.</ChartCaveat>

      <TickDivider className="my-s8" />

      {/* Learning curve — series not in snapshot */}
      <SectionHeader
        eyebrow="Data appetite"
        headline="Would more data help?"
        intro="A learning curve would need train/validation scores at several dataset sizes."
      />
      <div className="mt-s6">
        <NotInSnapshot detail="The learning-curve series (scores by training-set size) isn't part of the report snapshot, so this view is intentionally empty rather than estimated." />
        <ChartCaveat>Trend on this dataset only.</ChartCaveat>
      </div>

      <TickDivider className="my-s8" />

      {/* Confidence intervals — per-metric bootstrap series not in snapshot */}
      <SectionHeader
        eyebrow="Uncertainty"
        headline="How sure are these numbers?"
        intro="Bootstrapped intervals around each internal metric would belong here."
      />
      <div className="mt-s6">
        <NotInSnapshot detail="Per-metric bootstrap intervals for the internal test set aren't in the chart snapshot (reports-summary.json), so they aren't plotted here. The model card on the Transparency page lists them in full, and the external cohorts' ROC-AUC intervals are charted on the External test page." />
        <ChartCaveat>
          Wide intervals are the honest signal of a small test set.
        </ChartCaveat>
      </div>
    </div>
  );
}
