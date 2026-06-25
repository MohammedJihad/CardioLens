import * as React from "react";
import { reports, fmt3 } from "@/data/reports";

/**
 * TrustStrip — three honest headline stats, all read from reports-summary.json.
 *
 * Per the Phase-C trust-strip decision: lead with ROC-AUC, and show the
 * operating point at the DEFAULT 0.50 threshold (sensitivity/specificity from
 * the internal test metrics), explicitly labelled. The 1.00@0.20 screening
 * story lives on the future /thresholds page. Every sens/spec figure states
 * its threshold.
 */
export function TrustStrip() {
  const m = reports.metrics;
  const stats = [
    {
      value: fmt3(m.roc_auc),
      label: "ROC-AUC",
      sub: `internal test set, n=${m.n_test}`,
    },
    {
      value: `${fmt3(m.sensitivity)} / ${fmt3(m.specificity)}`,
      label: "Sensitivity / Specificity",
      sub: "at the default 0.50 threshold",
    },
    {
      value: String(reports.external.n_cohorts),
      label: "External cohorts",
      sub: "it was never trained on",
    },
  ];

  return (
    <section aria-labelledby="trust-heading" className="mx-auto max-w-container px-s5 py-s8">
      <h2 id="trust-heading" className="visually-hidden">
        Headline results
      </h2>
      <dl className="grid gap-s5 sm:grid-cols-3">
        {stats.map((s) => (
          <div
            key={s.label}
            className="border-t border-border-strong pt-s4 sm:border-l sm:border-t-0 sm:pl-s5 sm:pt-0 sm:first:border-l-0 sm:first:pl-0"
          >
            <dd className="font-mono text-2xl leading-none tabular-nums text-ink">
              {s.value}
            </dd>
            <dt className="mt-s2 text-sm font-semibold text-ink">{s.label}</dt>
            <p className="mt-s1 text-sm text-muted">{s.sub}</p>
          </div>
        ))}
      </dl>
      <p className="mt-s5 max-w-measure font-mono text-xs leading-normal text-muted">
        These are model-score metrics on research data, measured once on held-out
        data. Small test set — read the Results page for the full picture.
      </p>
    </section>
  );
}
