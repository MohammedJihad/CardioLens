import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TickDivider } from "@/components/tick-divider";
import { Card } from "@/components/ui/card";
import { MetricCard } from "@/components/metric-card";
import { ConfusionMatrix } from "@/components/results/confusion-matrix";
import { NotInSnapshot } from "@/components/not-in-snapshot";
import { ChartCaveat } from "@/components/chart-caveat";
import { reports, fmt3 } from "@/data/reports";

export const metadata: Metadata = { title: "Thresholds" };

const m = reports.metrics;
const t = reports.thresholds;

const fmtThreshold = (n: number) => n.toFixed(2);

export default function ThresholdsPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="Operating point"
        headline="Choosing where to draw the line."
        intro={`A model score is a number; a decision needs a threshold. We selected ${fmtThreshold(
          t.selected
        )} on out-of-fold data, then evaluated it once — tuned for a screening posture, not a clinical one.`}
      />

      {/* The selected operating point — every value from thresholds.* */}
      <div className="mt-s7 grid gap-s4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="Selected threshold"
          value={fmtThreshold(t.selected)}
          sub="tuned on out-of-fold data"
        />
        <MetricCard
          label="Sensitivity"
          value={fmt3(t.sens_selected)}
          sub={`true-positive rate at ${fmtThreshold(t.selected)}`}
        />
        <MetricCard
          label="Specificity"
          value={fmt3(t.spec_selected)}
          sub={`true-negative rate at ${fmtThreshold(t.selected)}`}
        />
        <MetricCard
          label="False negatives"
          value={String(t.fn_selected)}
          sub={`missed positive labels (n=${m.n_test})`}
        />
      </div>

      <Card className="mt-s5 p-s6">
        <p className="max-w-measure text-base leading-normal text-ink">
          A {fmtThreshold(t.selected)} threshold is a deliberately{" "}
          <strong className="font-semibold">screening-oriented</strong> choice:
          it catches every positive-labelled case in this test set (sensitivity{" "}
          {fmt3(t.sens_selected)}, {t.fn_selected} false negatives) at the cost of
          more false alarms (specificity {fmt3(t.spec_selected)}). It was tuned on
          out-of-fold data, then evaluated once on a small held-out set of{" "}
          {m.n_test} cases — so a sensitivity of {fmt3(t.sens_selected)} carries a
          wide confidence interval and should not be read as a guarantee.
        </p>
      </Card>

      <TickDivider className="my-s8" />

      {/* Trade-off — before/after confusion at 0.50 vs the selected 0.20 */}
      <SectionHeader
        eyebrow="Sensitivity vs specificity"
        headline="Catch more, or be more selective."
        intro={`At ${fmtThreshold(t.selected)}: sensitivity ${fmt3(
          t.sens_selected
        )}, specificity ${fmt3(t.spec_selected)}, false negatives ${
          t.fn_selected
        }. Moving the line down trades false alarms for missed cases.`}
      />
      <div className="mt-s6 grid gap-s6 lg:grid-cols-2">
        <div>
          <p className="eyebrow mb-s3">Default · 0.50</p>
          <ConfusionMatrix
            tp={m.confusion.tp}
            fp={m.confusion.fp}
            tn={m.confusion.tn}
            fn={m.confusion.fn}
            caption="Counts at the default 0.50 threshold (n=61)."
          />
        </div>
        <div>
          <p className="eyebrow mb-s3">Selected · {fmtThreshold(t.selected)}</p>
          <ConfusionMatrix
            tp={t.tp}
            fp={t.fp}
            tn={t.tn}
            fn={t.fn_selected}
            caption={`Counts at the selected ${fmtThreshold(
              t.selected
            )} screening threshold (n=61).`}
          />
        </div>
      </div>
      <ChartCaveat>
        Screening-oriented: it favors catching cases over avoiding false alarms.
        Lowering the line to {fmtThreshold(t.selected)} drives false negatives to{" "}
        {t.fn_selected} but raises false positives from {m.confusion.fp} to {t.fp}.
      </ChartCaveat>

      <div className="mt-s5">
        <NotInSnapshot detail={`The report snapshot holds only the single ${fmtThreshold(
          t.selected
        )} operating-point row, not a full sweep of sensitivity/specificity across every threshold. We show the before/after above rather than drawing a sweep curve we don't have the data for; a full curve would need the per-threshold series added to the report.`} />
      </div>

      <TickDivider className="my-s8" />

      {/* Calibration — Brier we have; per-bin curve we don't */}
      <SectionHeader
        eyebrow="Do the probabilities mean anything?"
        headline="When a score of 0.7 should mean 0.7."
        intro="Calibration asks whether the model's probabilities match observed frequencies on research data."
      />
      <div className="mt-s6 grid gap-s4 sm:grid-cols-2">
        <MetricCard
          label="Brier score"
          value={fmt3(m.brier)}
          sub="internal calibration error (lower is better)"
        />
      </div>
      <div className="mt-s5">
        <NotInSnapshot detail="The per-bin calibration curve (predicted vs observed by probability band) isn't in the report snapshot, so we don't plot it here. The headline Brier score above is the calibration summary we do have; the External test page shows how calibration weakened on unseen cohorts." />
        <ChartCaveat>
          Calibration held internally and weakened externally — see the External test.
        </ChartCaveat>
      </div>

      <TickDivider className="my-s8" />

      {/* Pull-quote */}
      <blockquote className="border-l-2 border-l-accent pl-s5">
        <p className="max-w-measure font-display text-2xl leading-snug text-ink">
          Screening-oriented, not clinical. A low score here is a below-threshold
          model result — never an all-clear.
        </p>
      </blockquote>
    </div>
  );
}
