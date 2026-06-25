import * as React from "react";
import type { ApiFactor } from "@/lib/api";

/**
 * FactorBars — the model-based explanation. Up factors are coral, down factors
 * are teal, but color is never the only signal: each row carries an arrow and
 * an explicit "pushed the score up/down" label, plus the mono magnitude.
 */
function Row({ factor, max }: { factor: ApiFactor; max: number }) {
  const up = factor.direction === "up";
  const width = max > 0 ? Math.max(4, (factor.magnitude / max) * 100) : 0;
  const phrase = up ? "pushed the score up" : "pushed the score down";
  return (
    <li className="grid grid-cols-[1fr_auto] items-center gap-x-s4 gap-y-s1 py-s2">
      <span className="text-sm text-ink">
        {factor.feature} — {phrase}
      </span>
      <span className="font-mono text-2xs tabular-nums text-muted">
        <span aria-hidden="true" className="mr-s1">
          {up ? "▲" : "▼"}
        </span>
        {factor.magnitude.toFixed(3)}
      </span>
      <span
        className="col-span-2 h-[8px] overflow-hidden rounded-full bg-subtle"
        aria-hidden="true"
      >
        <span
          className="block h-full rounded-full"
          style={{
            width: `${width}%`,
            backgroundColor: up ? "var(--gauge-high)" : "var(--gauge-low)",
          }}
        />
      </span>
    </li>
  );
}

export function FactorBars({
  positive,
  negative,
}: {
  positive: ApiFactor[];
  negative: ApiFactor[];
}) {
  const all = [...positive, ...negative];
  const max = all.reduce((m, f) => Math.max(m, f.magnitude), 0);

  if (all.length === 0) {
    return (
      <p className="text-sm text-muted">
        For this pattern the model showed no clear directional factors.
      </p>
    );
  }

  return (
    <ul className="space-y-s2">
      {positive.map((f, i) => (
        <Row key={`p-${i}`} factor={f} max={max} />
      ))}
      {negative.map((f, i) => (
        <Row key={`n-${i}`} factor={f} max={max} />
      ))}
    </ul>
  );
}
