import * as React from "react";
import { reports } from "@/data/reports";

/**
 * ConfusionMatrix — TP / FP / TN / FN counts at one operating threshold.
 *
 * Encoding rules (components.md): a SINGLE-HUE navy ramp where cell intensity
 * tracks the count — deliberately NOT a red/green pass-fail palette, so the
 * matrix reads as measurement, not judgement. Counts are mono; text flips to
 * the on-primary token on the darkest cells for contrast. It is a real <table>
 * with row/column headers and a caption, so screen readers get the full grid.
 *
 * Axis wording stays safe: rows are the research-data label (positive /
 * negative), columns are the model's above/below-threshold call — never
 * "patient is positive/negative" and never a clinical verdict.
 */

interface Cell {
  count: number;
  abbr: string;
  /** Plain, safe description of the cell. */
  desc: string;
}

function cellStyle(count: number, max: number): React.CSSProperties {
  const t = max > 0 ? count / max : 0;
  // 14% → 92% navy mixed into the surface: adapts to light/dark via the vars.
  const mix = Math.round(14 + t * 78);
  const onDark = t >= 0.6;
  return {
    backgroundColor: `color-mix(in srgb, var(--primary) ${mix}%, var(--bg-surface))`,
    color: onDark ? "var(--text-onprimary)" : "var(--text)",
  };
}

function CountCell({ cell, max }: { cell: Cell; max: number }) {
  return (
    <td
      className="rounded-sm border border-border p-s4 align-top"
      style={cellStyle(cell.count, max)}
    >
      <span className="block font-mono text-3xl leading-none tabular-nums">
        {cell.count}
      </span>
      <span className="mt-s2 block font-mono text-2xs uppercase tracking-eyebrow opacity-80">
        {cell.abbr}
      </span>
      <span className="mt-s1 block text-2xs leading-snug opacity-80">{cell.desc}</span>
    </td>
  );
}

export function ConfusionMatrix({
  tp = reports.metrics.confusion.tp,
  fp = reports.metrics.confusion.fp,
  tn = reports.metrics.confusion.tn,
  fn = reports.metrics.confusion.fn,
  caption,
}: {
  tp?: number;
  fp?: number;
  tn?: number;
  fn?: number;
  caption: string;
}) {
  const max = Math.max(tp, fp, tn, fn);
  return (
    <table className="w-full border-separate border-spacing-s2 text-left">
      <caption className="mb-s3 text-left text-sm text-muted">{caption}</caption>
      <thead>
        <tr>
          <td className="p-s2" />
          <th
            scope="col"
            className="p-s2 font-mono text-2xs uppercase tracking-eyebrow text-accent-text"
          >
            Model: above threshold
          </th>
          <th
            scope="col"
            className="p-s2 font-mono text-2xs uppercase tracking-eyebrow text-accent-text"
          >
            Model: below threshold
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th
            scope="row"
            className="p-s2 align-middle font-mono text-2xs uppercase tracking-eyebrow text-muted"
          >
            Research label: positive
          </th>
          <CountCell
            cell={{ count: tp, abbr: "TP", desc: "flagged, label positive" }}
            max={max}
          />
          <CountCell
            cell={{ count: fn, abbr: "FN", desc: "missed, label positive" }}
            max={max}
          />
        </tr>
        <tr>
          <th
            scope="row"
            className="p-s2 align-middle font-mono text-2xs uppercase tracking-eyebrow text-muted"
          >
            Research label: negative
          </th>
          <CountCell
            cell={{ count: fp, abbr: "FP", desc: "flagged, label negative" }}
            max={max}
          />
          <CountCell
            cell={{ count: tn, abbr: "TN", desc: "cleared, label negative" }}
            max={max}
          />
        </tr>
      </tbody>
    </table>
  );
}
