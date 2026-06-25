"use client";

import * as React from "react";
import { THEME_STORAGE_KEY } from "@/lib/site";

type Mode = "light" | "dark";

function systemMode(): Mode {
  return typeof window !== "undefined" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function currentMode(): Mode {
  if (typeof document === "undefined") return "light";
  const attr = document.documentElement.getAttribute("data-theme");
  if (attr === "dark" || attr === "light") return attr;
  return systemMode();
}

/**
 * ThemeToggle — flips between light and dark. System preference is the default;
 * an explicit choice persists in localStorage (a UI preference only) and wins
 * over the OS, matching the [data-theme] mechanism in tokens.css.
 */
export function ThemeToggle() {
  const [mounted, setMounted] = React.useState(false);
  const [mode, setMode] = React.useState<Mode>("light");

  React.useEffect(() => {
    setMounted(true);
    setMode(currentMode());
  }, []);

  function toggle() {
    const next: Mode = currentMode() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try {
      localStorage.setItem(THEME_STORAGE_KEY, next);
    } catch {
      /* ignore: storage may be unavailable */
    }
    setMode(next);
  }

  // Before mount, render a stable, non-flashing placeholder label.
  const label = !mounted
    ? "Toggle theme"
    : mode === "dark"
      ? "Switch to light theme"
      : "Switch to dark theme";

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={label}
      title={label}
      className="inline-flex min-h-[40px] min-w-[40px] items-center justify-center gap-s2 rounded-full border border-border bg-subtle px-s3 font-mono text-xs text-ink transition-colors duration-fast hover:bg-border focus-visible:outline-focus"
    >
      <span aria-hidden="true" className="text-base leading-none">
        {mounted && mode === "dark" ? "☀" : "☾"}
      </span>
      <span className="hidden sm:inline">{mounted && mode === "dark" ? "Light" : "Dark"}</span>
    </button>
  );
}
