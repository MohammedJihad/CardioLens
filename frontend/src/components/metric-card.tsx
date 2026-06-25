import * as React from "react";
import { Card } from "@/components/ui/card";

/**
 * MetricCard — one headline figure + label + sub. The value is mono with
 * tabular figures (instrument readout). Numbers always come from
 * reports-summary.json; this component never owns a metric.
 */
export function MetricCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <Card className="p-s5">
      <div className="eyebrow">{label}</div>
      <div className="mt-s2 font-mono text-3xl leading-none tabular-nums text-ink">
        {value}
      </div>
      {sub ? <div className="mt-s2 text-sm text-muted">{sub}</div> : null}
    </Card>
  );
}
