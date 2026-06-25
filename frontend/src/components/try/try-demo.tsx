"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { InputForm } from "./input-form";
import { PresetPicker } from "./preset-picker";
import { ResultCard } from "./result-card";
import {
  FIELDS,
  rangeLabel,
  type FieldDef,
  type PatientRecord,
  type Preset,
} from "./field-config";
import {
  predict,
  ERROR_COPY,
  type PredictErrorKind,
  type PredictionResponse,
} from "@/lib/api";

type Values = Record<string, string>;
type Errors = Record<string, string | undefined>;
type Status = "idle" | "loading" | "success" | "error";

function fieldError(field: FieldDef, raw: string): string | undefined {
  const v = raw.trim();
  const msg = `Enter a value in ${rangeLabel(field)} for ${field.label}.`;
  if (v === "") return msg;
  const num = Number(v);
  if (Number.isNaN(num)) return msg;
  if (num < field.min || num > field.max) return msg;
  if (field.integer && !Number.isInteger(num)) return msg;
  return undefined;
}

function validateAll(values: Values): Errors {
  const errors: Errors = {};
  for (const f of FIELDS) {
    const e = fieldError(f, values[f.name] ?? "");
    if (e) errors[f.name] = e;
  }
  return errors;
}

export function TryDemo() {
  const [values, setValues] = React.useState<Values>({});
  const [errors, setErrors] = React.useState<Errors>({});
  const [status, setStatus] = React.useState<Status>("idle");
  const [result, setResult] = React.useState<PredictionResponse | null>(null);
  const [errorKind, setErrorKind] = React.useState<PredictErrorKind | null>(null);
  const [showSummary, setShowSummary] = React.useState(false);

  function handleChange(name: string, value: string) {
    setValues((v) => ({ ...v, [name]: value }));
    // Live-clear a field's error once it becomes valid.
    setErrors((prev) => {
      if (!prev[name]) return prev;
      const f = FIELDS.find((x) => x.name === name)!;
      return { ...prev, [name]: fieldError(f, value) };
    });
  }

  function handleBlur(name: string) {
    const f = FIELDS.find((x) => x.name === name)!;
    const e = fieldError(f, values[name] ?? "");
    setErrors((prev) => ({ ...prev, [name]: e }));
  }

  async function score(record: PatientRecord) {
    setStatus("loading");
    setResult(null);
    setErrorKind(null);
    const res = await predict(record);
    if (res.ok) {
      setResult(res.data);
      setStatus("success");
    } else {
      setErrorKind(res.kind);
      setStatus("error");
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validateAll(values);
    setErrors(errs);
    const firstBad = FIELDS.find((f) => errs[f.name]);
    if (firstBad) {
      setShowSummary(true);
      // Move focus to the first invalid field for keyboard/SR users.
      requestAnimationFrame(() => document.getElementById(firstBad.name)?.focus());
      return;
    }
    setShowSummary(false);
    const record: PatientRecord = {};
    for (const f of FIELDS) record[f.name] = Number(values[f.name]);
    void score(record);
  }

  function handlePreset(preset: Preset) {
    const next: Values = {};
    for (const f of FIELDS) next[f.name] = String(preset.record[f.name]);
    setValues(next);
    setErrors({});
    setShowSummary(false);
    void score(preset.record);
  }

  function handleReset() {
    setValues({});
    setErrors({});
    setShowSummary(false);
    setStatus("idle");
    setResult(null);
    setErrorKind(null);
  }

  const loading = status === "loading";

  return (
    <div className="mt-s7 grid gap-s7">
      {/* Privacy line — always visible */}
      <p className="rounded-md border border-border bg-subtle px-s4 py-s3 text-sm text-muted">
        Inputs are sent to the model to compute a score and are not stored — no
        account, no database, no tracking of what you enter.
      </p>

      <Card className="p-s6">
        <form onSubmit={handleSubmit} noValidate>
          <InputForm
            values={values}
            errors={errors}
            onChange={handleChange}
            onBlur={handleBlur}
          />

          <div className="mt-s6 border-t border-border pt-s5">
            <PresetPicker onSelect={handlePreset} disabled={loading} />
          </div>

          {showSummary ? (
            <p
              role="alert"
              className="mt-s5 flex items-start gap-s2 rounded-sm border px-s4 py-s3 text-sm"
              style={{ color: "var(--danger-text)", borderColor: "var(--danger-text)" }}
            >
              <span aria-hidden="true">⚠</span>
              <span>
                Some fields need a valid value before the model can score this
                pattern.
              </span>
            </p>
          ) : null}

          <div className="mt-s6 flex flex-wrap items-center gap-s3">
            <Button type="submit" disabled={loading}>
              {loading ? "Scoring the pattern…" : "See the model score"}
            </Button>
            <Button type="button" variant="ghost" onClick={handleReset} disabled={loading}>
              Clear inputs
            </Button>
          </div>
        </form>
      </Card>

      {/* Result / status region */}
      <div aria-live="polite">
        {status === "idle" && !result ? (
          <p className="font-mono text-sm text-muted">
            Enter a pattern or pick a preset, then choose “See the model score.”
          </p>
        ) : null}

        {loading ? (
          <p className="font-mono text-sm text-muted">Scoring the pattern…</p>
        ) : null}

        {status === "error" && errorKind ? (
          <Card className="p-s5">
            <p className="flex items-start gap-s2 text-base text-ink">
              <span aria-hidden="true" style={{ color: "var(--danger-text)" }}>
                ⚠
              </span>
              <span>{ERROR_COPY[errorKind]}</span>
            </p>
          </Card>
        ) : null}

        {status === "success" && result ? <ResultCard data={result} /> : null}
      </div>
    </div>
  );
}
