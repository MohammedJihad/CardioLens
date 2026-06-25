/* =====================================================================
 * CardioLens — Design Tokens (typed TypeScript export)
 * ---------------------------------------------------------------------
 * Mirrors tokens.css 1:1. This is the source of truth for code that needs
 * token values in JS/TS (Recharts colors, the score gauge, Framer Motion
 * transitions, the Tailwind config in a later phase). If you change a value
 * in tokens.css, change it here too.
 *
 * Colors are split into `light` and `dark` so charts/gauges can read the
 * active palette explicitly. Everything is `as const` for literal types.
 * ===================================================================== */

export const color = {
  light: {
    base: "#FAFAF7",
    surface: "#FFFFFF",
    subtle: "#F2F1EC",
    hairline: "#E4E2DA",
    borderStrong: "#D5D3C9",
    ink: "#16181D",
    muted: "#5B6068",
    primary: "#1E2A44",
    primaryHover: "#2A3A5C",
    teal: "#2F8F83",
    /** AA-safe teal for TEXT/links on white */
    tealText: "#277A6F",
    amber: "#C98A3B",
    coral: "#C2614E",
    error: "#B4452F",
    focusRing: "#3E63B8",
    onPrimary: "#FAFAF7",
  },
  dark: {
    base: "#0E1117",
    surface: "#161B22",
    raised: "#1C232E",
    hairline: "#283040",
    borderStrong: "#3A465A",
    ink: "#E8EAED",
    muted: "#9AA2AD",
    /** Lifted navy so it reads on dark and carries dark text */
    primary: "#4C6190",
    primaryHover: "#5C73A8",
    teal: "#46A89B",
    /** Brighter teal is already AA on the dark base, text-safe */
    tealText: "#46A89B",
    amber: "#D69A4E",
    coral: "#D2725E",
    error: "#E08B76",
    focusRing: "#7CA0F0",
    onPrimary: "#0E1117",
  },
} as const;

/** Score-gauge scale — encodes MODEL-SCORE MAGNITUDE ONLY, never a verdict.
 *  teal (low) -> amber (mid) -> coral (high). Coral is calm, not alarm red. */
export const gauge = {
  light: {
    low: color.light.teal,
    mid: color.light.amber,
    high: color.light.coral,
    track: color.light.hairline,
  },
  dark: {
    low: color.dark.teal,
    mid: color.dark.amber,
    high: color.dark.coral,
    track: color.dark.hairline,
  },
  /** Gradient stops as offsets for SVG <linearGradient> (0..1 along the arc). */
  stops: [
    { offset: 0, key: "low" as const },
    { offset: 0.5, key: "mid" as const },
    { offset: 1, key: "high" as const },
  ],
} as const;

export const font = {
  display: '"Newsreader", Georgia, "Times New Roman", serif',
  body: '"Hanken Grotesk", system-ui, -apple-system, "Segoe UI", sans-serif',
  mono: '"IBM Plex Mono", ui-monospace, "SF Mono", "Cascadia Code", monospace',
  /** Google Fonts loader hints for next/font or <link>. */
  google: {
    Newsreader: { weights: [400, 500, 600], italics: true, optical: true },
    "Hanken Grotesk": { weights: [400, 500, 600, 700], italics: false },
    "IBM Plex Mono": { weights: [400, 500, 600], italics: false },
  },
} as const;

export const fontSize = {
  "2xs": "0.6875rem",
  xs: "0.75rem",
  sm: "0.875rem",
  base: "1rem",
  lg: "1.1875rem",
  xl: "1.5rem",
  "2xl": "1.9375rem",
  "3xl": "2.5rem",
  "4xl": "3.25rem",
  "5xl": "4.25rem",
} as const;

export const lineHeight = {
  tight: 1.08,
  snug: 1.22,
  normal: 1.55,
  relaxed: 1.7,
} as const;

export const fontWeight = {
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const;

export const letterSpacing = {
  tight: "-0.02em",
  normal: "0",
  wide: "0.02em",
  eyebrow: "0.14em",
} as const;

export const space = {
  0: "0",
  1: "0.25rem",
  2: "0.5rem",
  3: "0.75rem",
  4: "1rem",
  5: "1.5rem",
  6: "2rem",
  7: "3rem",
  8: "4rem",
  9: "6rem",
  10: "8rem",
} as const;

export const layout = {
  measure: "68ch",
  container: "72rem",
} as const;

export const radius = {
  xs: "4px",
  sm: "8px",
  md: "12px",
  lg: "16px",
  full: "999px",
} as const;

export const borderWidth = {
  hairline: "1px",
  strong: "1.5px",
  focus: "2px",
} as const;

export const shadow = {
  light: {
    xs: "0 1px 2px rgba(22, 24, 29, 0.04)",
    sm: "0 1px 3px rgba(22, 24, 29, 0.06), 0 1px 2px rgba(22, 24, 29, 0.04)",
    md: "0 4px 12px rgba(22, 24, 29, 0.07), 0 2px 4px rgba(22, 24, 29, 0.04)",
    lg: "0 12px 32px rgba(22, 24, 29, 0.10), 0 4px 8px rgba(22, 24, 29, 0.05)",
  },
  dark: {
    xs: "0 1px 2px rgba(0, 0, 0, 0.40)",
    sm: "0 1px 3px rgba(0, 0, 0, 0.45)",
    md: "0 4px 14px rgba(0, 0, 0, 0.50)",
    lg: "0 16px 40px rgba(0, 0, 0, 0.55)",
  },
} as const;

export const duration = {
  instant: 90,
  fast: 160,
  base: 240,
  slow: 420,
  story: 640,
} as const;

export const easing = {
  standard: [0.2, 0, 0, 1],
  entrance: [0.16, 1, 0.3, 1],
  exit: [0.4, 0, 1, 1],
  gauge: [0.34, 1.2, 0.64, 1],
} as const;

export const zIndex = {
  base: 0,
  raised: 10,
  sticky: 100,
  overlay: 1000,
} as const;

export const tokens = {
  color,
  gauge,
  font,
  fontSize,
  lineHeight,
  fontWeight,
  letterSpacing,
  space,
  layout,
  radius,
  borderWidth,
  shadow,
  duration,
  easing,
  zIndex,
} as const;

export type Tokens = typeof tokens;
export type ThemeMode = "light" | "dark";
export type ColorTokens = (typeof color)["light"];
export type GaugeKey = (typeof gauge.stops)[number]["key"];

export default tokens;
