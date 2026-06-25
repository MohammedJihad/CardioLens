/**
 * Field configuration for the /try form.
 *
 * Ranges, types, and field set match api/main.py `PatientFeatures` EXACTLY
 * (age 18–110, sex 0–1, cp 0–3, trestbps 80–220, chol 100–600, fbs 0–1,
 * restecg 0–2, thalach 60–220, exang 0–1, oldpeak 0–7, slope 0–2, ca 0–4,
 * thal 0–3). If the schema changes, change it here too.
 *
 * Coded categorical features (cp/restecg/slope/ca/thal) render as labelled
 * <select>s. Each option pairs the integer value the API expects with the
 * DOCUMENTED UCI label from this project's own schema/config — no invented
 * clinical names (see src/schema.py ENCODINGS / UCI_TO_CANONICAL and
 * src/config.py FEATURE_LABELS). `ca` stays a plain numeric select (0–4).
 * Binary features use neutral Yes/No (and Female/Male) selects. The value the
 * API receives is identical to the old integer inputs — only the visible label
 * changes.
 */

export type FieldGroup = "Demographics" | "Vitals & labs" | "ECG & exercise";

export interface SelectOption {
  value: number;
  label: string;
}

export interface FieldDef {
  name: string;
  label: string;
  group: FieldGroup;
  min: number;
  max: number;
  step: number;
  integer: boolean;
  unit?: string;
  /** Present => render as a <select> of these coded options. */
  options?: SelectOption[];
}

export const FIELD_GROUPS: FieldGroup[] = [
  "Demographics",
  "Vitals & labs",
  "ECG & exercise",
];

export const FIELDS: FieldDef[] = [
  // Demographics
  { name: "age", label: "Age", group: "Demographics", min: 18, max: 110, step: 1, integer: false, unit: "years" },
  {
    name: "sex", label: "Sex", group: "Demographics", min: 0, max: 1, step: 1, integer: true,
    options: [
      { value: 0, label: "Female" },
      { value: 1, label: "Male" },
    ],
  },
  // Vitals & labs
  {
    name: "cp", label: "Chest pain type", group: "Vitals & labs", min: 0, max: 3, step: 1, integer: true,
    options: [
      { value: 0, label: "0 — typical angina" },
      { value: 1, label: "1 — atypical angina" },
      { value: 2, label: "2 — non-anginal pain" },
      { value: 3, label: "3 — asymptomatic" },
    ],
  },
  { name: "trestbps", label: "Resting blood pressure", group: "Vitals & labs", min: 80, max: 220, step: 1, integer: false, unit: "mmHg" },
  { name: "chol", label: "Serum cholesterol", group: "Vitals & labs", min: 100, max: 600, step: 1, integer: false, unit: "mg/dl" },
  {
    name: "fbs", label: "Fasting blood sugar > 120 mg/dl", group: "Vitals & labs", min: 0, max: 1, step: 1, integer: true,
    options: [
      { value: 0, label: "No" },
      { value: 1, label: "Yes" },
    ],
  },
  // ECG & exercise
  {
    name: "restecg", label: "Resting ECG result", group: "ECG & exercise", min: 0, max: 2, step: 1, integer: true,
    options: [
      { value: 0, label: "0 — normal" },
      { value: 1, label: "1 — ST-T wave abnormality" },
      { value: 2, label: "2 — left ventricular hypertrophy" },
    ],
  },
  { name: "thalach", label: "Maximum heart rate", group: "ECG & exercise", min: 60, max: 220, step: 1, integer: false, unit: "bpm" },
  {
    name: "exang", label: "Exercise-induced angina", group: "ECG & exercise", min: 0, max: 1, step: 1, integer: true,
    options: [
      { value: 0, label: "No" },
      { value: 1, label: "Yes" },
    ],
  },
  { name: "oldpeak", label: "ST depression (oldpeak)", group: "ECG & exercise", min: 0, max: 7, step: 0.1, integer: false, unit: "ST depression" },
  {
    name: "slope", label: "ST slope", group: "ECG & exercise", min: 0, max: 2, step: 1, integer: true,
    options: [
      { value: 0, label: "0 — upsloping" },
      { value: 1, label: "1 — flat" },
      { value: 2, label: "2 — downsloping" },
    ],
  },
  {
    name: "ca", label: "Major vessels colored", group: "ECG & exercise", min: 0, max: 4, step: 1, integer: true,
    options: [
      { value: 0, label: "0" },
      { value: 1, label: "1" },
      { value: 2, label: "2" },
      { value: 3, label: "3" },
      { value: 4, label: "4" },
    ],
  },
  {
    name: "thal", label: "Thalassemia result", group: "ECG & exercise", min: 0, max: 3, step: 1, integer: true,
    options: [
      { value: 0, label: "0 — unknown" },
      { value: 1, label: "1 — normal" },
      { value: 2, label: "2 — fixed defect" },
      { value: 3, label: "3 — reversible defect" },
    ],
  },
];

export const FEATURE_NAMES = FIELDS.map((f) => f.name);

/** en-dash range label, e.g. "18–110". */
export function rangeLabel(f: FieldDef): string {
  return `${f.min}–${f.max}`;
}

export type PatientRecord = Record<string, number>;

/**
 * Three illustrative research-style patterns — NOT real people. Each posts
 * through the same /predict path. Values are within the schema ranges and
 * chosen to land low / mid / high model scores.
 */
export interface Preset {
  id: "low" | "borderline" | "high";
  label: string;
  record: PatientRecord;
}

export const PRESETS: Preset[] = [
  {
    id: "low",
    label: "Low model score",
    record: { age: 40, sex: 0, cp: 0, trestbps: 118, chol: 198, fbs: 0, restecg: 0, thalach: 172, exang: 0, oldpeak: 0, slope: 2, ca: 0, thal: 2 },
  },
  {
    id: "borderline",
    label: "Borderline pattern",
    record: { age: 58, sex: 1, cp: 2, trestbps: 132, chol: 224, fbs: 0, restecg: 0, thalach: 173, exang: 0, oldpeak: 3.2, slope: 2, ca: 2, thal: 3 },
  },
  {
    id: "high",
    label: "High model score",
    record: { age: 55, sex: 1, cp: 3, trestbps: 150, chol: 250, fbs: 1, restecg: 0, thalach: 140, exang: 0, oldpeak: 1.4, slope: 1, ca: 2, thal: 3 },
  },
];
