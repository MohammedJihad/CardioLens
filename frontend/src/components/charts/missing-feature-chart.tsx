"use client";

import * as React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { reports } from "@/data/reports";
import { ChartCaveat } from "@/components/chart-caveat";
import { axisTick, gridStroke, labelText, tooltipContentStyle } from "./chart-style";

/**
 * MissingFeatureChart — the "why" behind the external drop. Per cohort, how
 * much of the model's two vessel/thalassemia features were missing. `ca` (major
 * vessels colored — the single strongest feature) is 96–99% missing across all
 * three cohorts. Amber = "gap / caution" (a non-text signal only); the two
 * series are told apart by shape (solid vs outlined) and a direct value label
 * on every bar, never by hue alone.
 */

const e = reports.external;

const DATA = [
  { name: "Hungarian", ca: e.hungarian.ca_missing_pct, thal: e.hungarian.thal_missing_pct },
  { name: "VA", ca: e.va.ca_missing_pct, thal: e.va.thal_missing_pct },
  { name: "Switzerland", ca: e.switzerland.ca_missing_pct, thal: e.switzerland.thal_missing_pct },
];

const pctLabel = (v: number) => `${v}%`;

function TipContent({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ dataKey: string; value: number }>;
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  const get = (k: string) => payload.find((p) => p.dataKey === k)?.value;
  return (
    <div style={tooltipContentStyle}>
      <div style={{ color: "var(--text-muted)" }}>{label}</div>
      <div>ca (major vessels) {pctLabel(get("ca") ?? 0)} missing</div>
      <div>thal (thalassemia) {pctLabel(get("thal") ?? 0)} missing</div>
    </div>
  );
}

export function MissingFeatureChart() {
  return (
    <figure
      className="m-0"
      role="group"
      aria-label="Percentage of the ca (major vessels) and thal (thalassemia) features missing in each external cohort."
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
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tick={axisTick}
              tickLine={false}
              axisLine={{ stroke: gridStroke }}
              width={38}
              tickFormatter={pctLabel}
            />
            <Tooltip
              content={<TipContent />}
              cursor={{ fill: "var(--bg-subtle)", opacity: 0.6 }}
            />
            <Bar
              dataKey="ca"
              name="ca — major vessels"
              fill="var(--gauge-mid)"
              radius={[4, 4, 0, 0]}
              maxBarSize={56}
              isAnimationActive={false}
            >
              <LabelList dataKey="ca" position="top" formatter={pctLabel} {...labelText} />
            </Bar>
            <Bar
              dataKey="thal"
              name="thal — thalassemia"
              fill="var(--gauge-mid)"
              fillOpacity={0.28}
              stroke="var(--gauge-mid)"
              strokeWidth={1.5}
              radius={[4, 4, 0, 0]}
              maxBarSize={56}
              isAnimationActive={false}
            >
              <LabelList dataKey="thal" position="top" formatter={pctLabel} {...labelText} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend — shape (solid vs outlined) + text, so hue is never the only cue. */}
      <ul className="mt-s4 flex flex-wrap gap-x-s5 gap-y-s2 text-2xs text-muted">
        <li className="flex items-center gap-s2">
          <span
            aria-hidden="true"
            className="inline-block h-[10px] w-[14px] rounded-[2px] align-middle"
            style={{ backgroundColor: "var(--gauge-mid)" }}
          />
          ca — major vessels colored (the #1 feature)
        </li>
        <li className="flex items-center gap-s2">
          <span
            aria-hidden="true"
            className="inline-block h-[10px] w-[14px] rounded-[2px] align-middle"
            style={{
              border: "1.5px solid var(--gauge-mid)",
              backgroundColor: "color-mix(in srgb, var(--gauge-mid) 28%, transparent)",
            }}
          />
          thal — thalassemia result
        </li>
      </ul>

      {/* Screen-reader data table. */}
      <table className="visually-hidden">
        <caption>Percentage missing of ca and thal by external cohort.</caption>
        <thead>
          <tr>
            <th scope="col">Cohort</th>
            <th scope="col">ca missing</th>
            <th scope="col">thal missing</th>
          </tr>
        </thead>
        <tbody>
          {DATA.map((d) => (
            <tr key={d.name}>
              <th scope="row">{d.name}</th>
              <td>{pctLabel(d.ca)}</td>
              <td>{pctLabel(d.thal)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <figcaption>
        <p className="mt-s4 max-w-measure text-sm leading-normal text-muted">
          The model leaned on two features the new cohorts barely recorded: ca
          (major vessels) is {e.switzerland.ca_missing_pct}–
          {e.hungarian.ca_missing_pct}% missing across all three, and thal is{" "}
          {e.switzerland.thal_missing_pct}–{e.hungarian.thal_missing_pct}% missing.
        </p>
        <ChartCaveat>
          Missingness is a property of these historical research cohorts, not of
          any person. It is the leading explanation for the external drop.
        </ChartCaveat>
      </figcaption>
    </figure>
  );
}
