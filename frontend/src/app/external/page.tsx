import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TickDivider } from "@/components/tick-divider";
import { Card } from "@/components/ui/card";
import { ExternalValidationChart } from "@/components/charts/external-validation-chart";
import { MissingFeatureChart } from "@/components/charts/missing-feature-chart";
import { reports, fmt3 } from "@/data/reports";

export const metadata: Metadata = { title: "External test" };

const m = reports.metrics;
const e = reports.external;

/**
 * The six narrative beats from copy.md, rendered as ordered STATIC sections.
 * The pinned-scroll treatment is Phase H — here the story is correct and
 * readable without any motion. Every number is read from reports-summary.json.
 */
const BEATS: { eyebrow: string; line: React.ReactNode; caveat: string }[] = [
  {
    eyebrow: "Starting point",
    line: <>On its own test set, the model reached ROC-AUC {fmt3(m.roc_auc)}.</>,
    caveat: "Internal, held-out research data.",
  },
  {
    eyebrow: "New cohort — Hungarian",
    line: (
      <>Ranking ability held up reasonably: ROC-AUC {fmt3(e.hungarian.roc_auc)}.</>
    ),
    caveat: "Discrimination partly transfers.",
  },
  {
    eyebrow: "New cohort — VA",
    line: <>Here it dropped to {fmt3(e.va.roc_auc)}.</>,
    caveat: "Different population, different result.",
  },
  {
    eyebrow: "New cohort — Switzerland",
    line: (
      <>ROC-AUC {fmt3(e.switzerland.roc_auc)}, but the probabilities drifted.</>
    ),
    caveat: "Calibration is the first thing to break.",
  },
  {
    eyebrow: "The catch — calibration",
    line: (
      <>
        Brier score worsened across cohorts ({fmt3(e.hungarian.brier)} →{" "}
        {fmt3(e.va.brier)}).
      </>
    ),
    caveat: "Good ranking can hide bad calibration.",
  },
  {
    eyebrow: "Why — missing features",
    line: (
      <>
        Two of the model&apos;s strongest inputs were {e.missing_range} missing in
        these cohorts.
      </>
    ),
    caveat: "The model leaned on signals the new data barely had.",
  },
];

export default function ExternalPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="The stress test"
        headline="What happened on cohorts it had never seen."
        intro="We froze the model and ran it on external research cohorts. This is where a model usually tells the truth about itself."
      />

      {/* The headline visual — ranking ability across cohorts (the drop). */}
      <Card className="mt-s7 p-s6">
        <ExternalValidationChart />
      </Card>

      <TickDivider className="my-s8" />

      {/* Six ordered story beats (static; Phase H adds the pinned scroll). */}
      <ol className="space-y-s7">
        {BEATS.map((b, i) => (
          <li key={b.eyebrow} className="grid gap-s3 sm:grid-cols-[auto_1fr] sm:gap-s5">
            <span
              aria-hidden="true"
              className="font-mono text-2xl tabular-nums text-border-strong"
            >
              {String(i + 1).padStart(2, "0")}
            </span>
            <div>
              <p className="eyebrow mb-s2">{b.eyebrow}</p>
              <p className="max-w-measure font-display text-2xl leading-snug text-ink">
                {b.line}
              </p>
              <p className="mt-s3 font-mono text-2xs text-muted">{b.caveat}</p>
            </div>
          </li>
        ))}
      </ol>

      {/* The "why" chart, paired with the final missing-features beat. */}
      <Card className="mt-s7 p-s6">
        <MissingFeatureChart />
      </Card>

      <TickDivider className="my-s8" />

      {/* The pinned conclusion → static callout. */}
      <Card className="border-l-2 border-l-accent p-s6">
        <p className="eyebrow mb-s3">The gap that matters</p>
        <p className="max-w-measure font-display text-3xl leading-snug text-ink">
          Discrimination partially transfers. Calibration does not. That gap is the
          most important thing on this whole site.
        </p>
        <p className="mt-s5 font-mono text-2xs text-muted">
          Retrospective educational validation on historical public research data.
        </p>
      </Card>
    </div>
  );
}
