/**
 * Minimal client for the FastAPI model service.
 *
 * - Base URL from NEXT_PUBLIC_API_BASE_URL (default http://127.0.0.1:8000).
 * - Stateless: inputs are sent to compute a score and are never stored,
 *   logged, or sent anywhere else. No localStorage, no analytics.
 * - Returns a discriminated result so the UI can show the exact copy for each
 *   state (success / validation / unreachable / server / timeout).
 */
import type { PatientRecord } from "@/components/try/field-config";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

export interface ApiFactor {
  feature: string;
  direction: "up" | "down";
  magnitude: number;
}

export interface PredictionResponse {
  model_score: number;
  score_band: string;
  default_threshold: number;
  above_default_threshold: boolean;
  selected_threshold: number | null;
  model: string;
  disclaimer: string;
  top_positive_factors: ApiFactor[];
  top_negative_factors: ApiFactor[];
}

export type PredictErrorKind =
  | "validation"
  | "unreachable"
  | "server"
  | "timeout";

export type PredictResult =
  | { ok: true; data: PredictionResponse }
  | { ok: false; kind: PredictErrorKind };

const TIMEOUT_MS = 60000;

export async function predict(record: PatientRecord): Promise<PredictResult> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(record),
      signal: controller.signal,
      // Never cache a prediction; never persist anything.
      cache: "no-store",
    });

    if (res.ok) {
      const data = (await res.json()) as PredictionResponse;
      return { ok: true, data };
    }
    if (res.status === 422) return { ok: false, kind: "validation" };
    return { ok: false, kind: "server" };
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") {
      return { ok: false, kind: "timeout" };
    }
    // fetch throws a TypeError when the host is unreachable / asleep / CORS-blocked.
    return { ok: false, kind: "unreachable" };
  } finally {
    clearTimeout(timer);
  }
}

/** Verbatim copy from copy.md (/try states). */
export const ERROR_COPY: Record<PredictErrorKind, string> = {
  validation:
    "Some fields need a valid value before the model can score this pattern.",
  unreachable:
    "The model service is waking up or unavailable. The rest of the site still works â€” try again in a moment, or read the Results page meanwhile.",
  server:
    "The model couldn't score that pattern just now. Nothing was stored. Please try again.",
  timeout:
    "That took too long to score. Try again, or load a preset pattern.",
};

