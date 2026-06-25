/**
 * Shared Recharts styling — the one place chart chrome reads design tokens.
 *
 * From components.md: gridlines `--border`, axes mono `--text-2xs` `--text-muted`,
 * tooltip `--bg-surface` + `--shadow-md` + `--border`. Series colors are passed
 * per-chart from the token palette (primary / accent / gauge-mid). Keeping these
 * here means every chart axis looks identical and theme-switches with the vars.
 */
import type { CSSProperties } from "react";

/** Axis tick text — mono, ~text-2xs (11px), muted. */
export const axisTick = {
  fontFamily: "var(--font-mono)",
  fontSize: 11,
  fill: "var(--text-muted)",
} as const;

/** Hairline used for gridlines and axis lines. */
export const gridStroke = "var(--border)";

/** Tooltip surface — matches the Card/Tooltip primitive. */
export const tooltipContentStyle: CSSProperties = {
  background: "var(--bg-surface)",
  border: "1px solid var(--border)",
  borderRadius: 8,
  boxShadow: "var(--shadow-md)",
  fontFamily: "var(--font-mono)",
  fontSize: 12,
  color: "var(--text)",
  padding: "0.5rem 0.625rem",
};

/** Data-label text drawn above bars — mono, small, muted. */
export const labelText = {
  fontFamily: "var(--font-mono)",
  fontSize: 11,
  fill: "var(--text-muted)",
} as const;
