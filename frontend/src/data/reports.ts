/**
 * Typed loader for the frozen research numbers.
 *
 * EVERY metric shown on the site reads from here — components must never
 * hard-code a number. The JSON is a committed snapshot of web-data/
 * reports-summary.json (regenerate with `make -f Makefile.web reports-summary`
 * when the reports change). Values are verbatim from reports/, never recomputed.
 */
import summary from "./reports-summary.json";

export interface Confusion {
  tp: number;
  fp: number;
  tn: number;
  fn: number;
}

export interface InternalMetrics {
  roc_auc: number;
  pr_auc: number;
  sensitivity: number;
  specificity: number;
  f1: number;
  brier: number;
  n_test: number;
  confusion: Confusion;
}

export interface ThresholdPoint {
  selected: number;
  sens_selected: number;
  spec_selected: number;
  fn_selected: number;
  tp: number;
  fp: number;
  tn: number;
}

export interface ExternalCohort {
  label: string;
  n: number;
  disease_rate: number;
  roc_auc: number;
  roc_auc_ci: [number, number];
  pr_auc: number;
  brier: number;
  "sens_at_0.2": number;
  "spec_at_0.2": number;
  ca_missing_pct: number;
  thal_missing_pct: number;
}

export interface ExternalValidation {
  n_cohorts: number;
  missing_range: string;
  missing_range_ca: string;
  missing_range_thal: string;
  hungarian: ExternalCohort;
  va: ExternalCohort;
  switzerland: ExternalCohort;
}

export interface ReportsSummary {
  generated_from: string[];
  year: number;
  note: string;
  metrics: InternalMetrics;
  thresholds: ThresholdPoint;
  external: ExternalValidation;
}

export const reports = summary as unknown as ReportsSummary;

/** Format a 0..1 model figure as a 3-decimal string (e.g. 0.892). */
export function fmt3(n: number): string {
  return n.toFixed(3);
}

/** Format a 0..1 figure as a whole-number percent (e.g. 71%). */
export function pct(n: number): string {
  return `${Math.round(n * 100)}%`;
}

export default reports;
