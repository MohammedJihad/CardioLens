"use client";

import * as React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ErrorBar,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { reports, fmt3 } from "@/data/reports";
import { ChartCaveat } from "@/components/chart-caveat";
import { axisTick, gridStroke, labelText, tooltipContentStyle } from "./chart-style";

/**
 * ExternalValidationChart — ROC-AUC for the internal test set next to the three
 * external cohorts (the drop). The internal bar is highlighted with --accent;
 * external bars use --primary. 95% bootstrap CIs (present in the snapshot for
 * the three external cohorts) render as vertical error bars; the internal bar
 * has no CI in the snapshot, so it is drawn without one — never invented.
 *
 * The Y axis runs the full 0–1 (no truncated/misleading scale). Color is never
 * the only signal: every bar is labelled with its value, the cohort name sits
 * on the axis, and a visually-hidden table carries the full data for SRs.
 */

const m = reports.metrics;
const e = reports.external;

interface Row {
  name: string;
  auc: number;
  highlight: boolean;
  ciLow?: number;
  ciHigh?: number;
  /** Recharts ErrorBar reads [minusError, plusError] magnitudes. */
  error?: [number, number];
}

function extRow(name: string, c: typeof e.hungarian): Row {
  return {
    name,
    auc: c.roc_auc,
    highlight: false,
    ciLow: c.roc_auc_ci[0],
    ciHigh: c.roc_auc_ci[1],
    error: [c.roc_auc - c.roc_auc_ci[0], c.roc_auc_ci[1] - c.roc_auc],
  };
}

const DATA: Row[] = [
  { name: "Internal", auc: m.roc_auc, highlight: true },
  extRow("Hungarian", e.hungarian),
  extRow("VA", e.va),
  extRow("Switzerland", e.switzerland),
];

function TipContent({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{ payload: Row }>;
}) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={tooltipContentStyle}>
      <div style={{ color: "var(--text-muted)" }}>
        {d.highlight ? "Internal (held-out)" : "External cohort"}
      </div>
      <div>
        {d.name} · ROC-AUC {fmt3(d.auc)}
      </div>
      <div style={{ color: "var(--text-muted)" }}>
        {d.ciLow != null
          ? `95% CI ${fmt3(d.ciLow)}–${fmt3(d.ciHigh as number)}`
          : "no CI in snapshot"}
      </div>
    </div>
  );
}

function Swatch({ color, outline }: { color: string; outline?: boolean }) {
  return (
    <span
      aria-hidden="true"
      className="inline-block h-[10px] w-[14px] rounded-[2px] align-middle"
      style={
        outline
          ? { border: `1.5px solid ${color}` }
          : { backgroundColor: color }
      }
    />
  );
}

export function ExternalValidationChart() {
  return (
    <figure
      className="m-0"
      role="group"
      aria-label="ROC-AUC by cohort: internal test set versus three external cohorts, with 95% confidence intervals where available."
    >
      <div aria-hidden="true" className="h-[320px] w-full">
        <ResponsiveContainer>
          <BarChart data={DATA} margin={{ top: 24, right: 12, left: 0, bottom: 4 }}>
            <CartesianGrid stroke={gridStroke} vertical={false} />
            <XAxis
              dataKey="name"
              tick={axisTick}
              tickLine={false}
              axisLine={{ stroke: gridStroke }}
            />
            <YAxis
              domain={[0, 1]}
              ticks={[0, 0.2, 0.4, 0.6, 0.8, 1]}
              tick={axisTick}
              tickLine={false}
              axisLine={{ stroke: gridStroke }}
              width={34}
              tickFormatter={(v: number) => v.toFixed(1)}
            />
            <Tooltip
              content={<TipContent />}
              cursor={{ fill: "var(--bg-subtle)", opacity: 0.6 }}
            />
            <Bar
              dataKey="auc"
              radius={[4, 4, 0, 0]}
              maxBarSize={84}
              isAnimationActive={false}
            >
              {DATA.map((d) => (
                <Cell
                  key={d.name}
                  fill={d.highlight ? "var(--accent)" : "var(--primary)"}
                />
              ))}
              <ErrorBar
                dataKey="error"
                direction="y"
                width={6}
                strokeWidth={1.5}
                stroke="var(--border-strong)"
              />
              <LabelList
                dataKey="auc"
                position="top"
                formatter={(v: number) => fmt3(v)}
                {...labelText}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Visible legend — color is reinforced with text + shape, never alone. */}
      <ul className="mt-s4 flex flex-wrap gap-x-s5 gap-y-s2 text-2xs text-muted">
        <li className="flex items-center gap-s2">
          <Swatch color="var(--accent)" />
          Internal — held-out test set
        </li>
        <li className="flex items-center gap-s2">
          <Swatch color="var(--primary)" />
          External cohort — never trained on
        </li>
        <li className="flex items-center gap-s2">
          <span
            aria-hidden="true"
            className="inline-block h-[12px] w-0 align-middle"
            style={{ borderLeft: "1.5px solid var(--border-strong)" }}
          />
          95% bootstrap CI
        </li>
      </ul>

      {/* Screen-reader data table. */}
      <table className="visually-hidden">
        <caption>ROC-AUC by cohort with 95% confidence intervals.</caption>
        <thead>
          <tr>
            <th scope="col">Cohort</th>
            <th scope="col">ROC-AUC</th>
            <th scope="col">95% CI</th>
          </tr>
        </thead>
        <tbody>
          {DATA.map((d) => (
            <tr key={d.name}>
              <th scope="row">{d.name}</th>
              <td>{fmt3(d.auc)}</td>
              <td>
                {d.ciLow != null
                  ? `${fmt3(d.ciLow)} to ${fmt3(d.ciHigh as number)}`
                  : "not in snapshot"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <figcaption>
        <p className="mt-s4 max-w-measure text-sm leading-normal text-muted">
          Ranking ability is highest on the internal test set (ROC-AUC{" "}
          {fmt3(m.roc_auc)}), holds reasonably on Hungarian (
          {fmt3(e.hungarian.roc_auc)}), and is lowest on VA Long Beach (
          {fmt3(e.va.roc_auc)}). The wide external intervals reflect smaller,
          different cohorts.
        </p>
        <ChartCaveat>
          Retrospective educational validation on historical public research
          data. Bars show ranking ability (ROC-AUC), not calibrated probability.
        </ChartCaveat>
      </figcaption>
    </figure>
  );
}
