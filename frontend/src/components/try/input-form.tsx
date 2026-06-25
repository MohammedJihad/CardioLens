import * as React from "react";
import { FIELDS, FIELD_GROUPS, rangeLabel, type FieldDef } from "./field-config";

/**
 * InputForm — research-style inputs grouped Demographics / Vitals & labs /
 * ECG & exercise. Native <label> for every field; mono range·unit hints;
 * aria-invalid + aria-describedby on errors; targets ≥44px. Error styling
 * (--danger-text) is the only place that color appears, always with icon + text.
 */
const inputBase =
  "min-h-[44px] w-full rounded-sm border bg-surface px-s3 text-base text-ink " +
  "transition-colors duration-fast focus-visible:outline-focus";

function FieldRow({
  field,
  value,
  error,
  onChange,
  onBlur,
}: {
  field: FieldDef;
  value: string;
  error?: string;
  onChange: (name: string, value: string) => void;
  onBlur: (name: string) => void;
}) {
  const hintId = `${field.name}-hint`;
  const errId = `${field.name}-err`;
  // Coded selects (sex/cp/restecg/exang/slope/ca/thal, fbs) read clearly from
  // their labelled options, so we skip the numeric range hint there; numeric
  // inputs always show range · unit.
  const showHint = !field.options;
  const hint = field.unit
    ? `${rangeLabel(field)} · ${field.unit}`
    : rangeLabel(field);
  const describedBy = [showHint ? hintId : null, error ? errId : null]
    .filter(Boolean)
    .join(" ");

  return (
    <div>
      <label htmlFor={field.name} className="block text-sm font-medium text-ink">
        {field.label}
      </label>

      {field.options ? (
        <select
          id={field.name}
          name={field.name}
          value={value}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy || undefined}
          onChange={(e) => onChange(field.name, e.target.value)}
          onBlur={() => onBlur(field.name)}
          className={`${inputBase} ${error ? "border-danger" : "border-border"}`}
          style={error ? { borderColor: "var(--danger-text)" } : undefined}
        >
          <option value="">Select…</option>
          {field.options.map((o) => (
            <option key={o.value} value={String(o.value)}>
              {o.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          id={field.name}
          name={field.name}
          type="number"
          inputMode="decimal"
          min={field.min}
          max={field.max}
          step={field.step}
          value={value}
          placeholder={rangeLabel(field)}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy || undefined}
          onChange={(e) => onChange(field.name, e.target.value)}
          onBlur={() => onBlur(field.name)}
          className={inputBase}
          style={error ? { borderColor: "var(--danger-text)" } : { borderColor: "var(--border)" }}
        />
      )}

      {showHint ? (
        <p id={hintId} className="mt-s1 font-mono text-2xs text-muted">
          {hint}
        </p>
      ) : null}

      {error ? (
        <p
          id={errId}
          className="mt-s1 flex items-start gap-s1 text-2xs"
          style={{ color: "var(--danger-text)" }}
        >
          <span aria-hidden="true">⚠</span>
          <span>{error}</span>
        </p>
      ) : null}
    </div>
  );
}

export function InputForm({
  values,
  errors,
  onChange,
  onBlur,
}: {
  values: Record<string, string>;
  errors: Record<string, string | undefined>;
  onChange: (name: string, value: string) => void;
  onBlur: (name: string) => void;
}) {
  return (
    <div className="space-y-s6">
      {FIELD_GROUPS.map((group) => (
        <fieldset key={group} className="border-0 p-0">
          <legend className="mb-s3 font-mono text-2xs uppercase tracking-eyebrow text-accent-text">
            {group}
          </legend>
          <div className="grid gap-s5 sm:grid-cols-2">
            {FIELDS.filter((f) => f.group === group).map((field) => (
              <FieldRow
                key={field.name}
                field={field}
                value={values[field.name] ?? ""}
                error={errors[field.name]}
                onChange={onChange}
                onBlur={onBlur}
              />
            ))}
          </div>
        </fieldset>
      ))}
    </div>
  );
}
