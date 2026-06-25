import type { Config } from "tailwindcss";

/**
 * CardioLens Tailwind theme.
 *
 * Colors/shadows/radii reference the CSS variables defined in globals.css,
 * which are copied VERBATIM from docs/design/tokens.css (the single source of
 * truth). No hex values are invented or redefined here — every color is a
 * `var(--token)` so light/dark switching happens in one place.
 */
const config: Config = {
  // Dark mode is driven by CSS variables (prefers-color-scheme + [data-theme]).
  // This selector only exists so any incidental `dark:` utility tracks the
  // manual override; the palette itself switches via the variables.
  darkMode: ["selector", '[data-theme="dark"]'],
  content: ["./src/**/*.{ts,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--bg-surface)",
        subtle: "var(--bg-subtle)",
        border: "var(--border)",
        "border-strong": "var(--border-strong)",
        ink: "var(--text)",
        muted: "var(--text-muted)",
        onprimary: "var(--text-onprimary)",
        accent: "var(--accent)",
        "accent-text": "var(--accent-text)",
        primary: {
          DEFAULT: "var(--primary)",
          hover: "var(--primary-hover)",
        },
        focus: "var(--focus-ring)",
        danger: "var(--danger-text)",
        gauge: {
          low: "var(--gauge-low)",
          mid: "var(--gauge-mid)",
          high: "var(--gauge-high)",
          track: "var(--gauge-track)",
        },
      },
      fontFamily: {
        display: "var(--font-display)",
        body: "var(--font-body)",
        mono: "var(--font-mono)",
      },
      fontSize: {
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
      },
      lineHeight: {
        tight: "1.08",
        snug: "1.22",
        normal: "1.55",
        relaxed: "1.7",
      },
      letterSpacing: {
        tight: "-0.02em",
        normal: "0",
        wide: "0.02em",
        eyebrow: "0.14em",
      },
      spacing: {
        // 4px base / 8px rhythm (named to mirror tokens.css --space-*)
        "s1": "0.25rem",
        "s2": "0.5rem",
        "s3": "0.75rem",
        "s4": "1rem",
        "s5": "1.5rem",
        "s6": "2rem",
        "s7": "3rem",
        "s8": "4rem",
        "s9": "6rem",
        "s10": "8rem",
      },
      maxWidth: {
        container: "72rem",
        measure: "68ch",
      },
      borderRadius: {
        xs: "4px",
        sm: "8px",
        md: "12px",
        lg: "16px",
        full: "999px",
      },
      boxShadow: {
        xs: "var(--shadow-xs)",
        sm: "var(--shadow-sm)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
      },
      transitionDuration: {
        instant: "90ms",
        fast: "160ms",
        base: "240ms",
        slow: "420ms",
        story: "640ms",
      },
      transitionTimingFunction: {
        standard: "cubic-bezier(0.2, 0, 0, 1)",
        entrance: "cubic-bezier(0.16, 1, 0.3, 1)",
        exit: "cubic-bezier(0.4, 0, 1, 1)",
        gauge: "cubic-bezier(0.34, 1.2, 0.64, 1)",
      },
      zIndex: {
        sticky: "100",
        overlay: "1000",
      },
    },
  },
  plugins: [],
};

export default config;
