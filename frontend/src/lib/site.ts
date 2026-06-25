/** Site-wide constants: the canonical navigation order (used by Nav + Footer,
 *  kept consistent across every page per the a11y "consistent navigation" rule). */

export const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/try", label: "Try the model" },
  { href: "/results", label: "Results" },
  { href: "/external", label: "External test" },
  { href: "/thresholds", label: "Thresholds" },
  { href: "/transparency", label: "Transparency" },
  { href: "/about", label: "About" },
] as const;

export const SITE = {
  name: "CardioLens",
  tagline: "A calibrated lens on heart-disease research data.",
  // Educational repo link placeholder â€” wired in a later phase / by the owner.
  repoUrl: "https://github.com/MohammedJihad/CardioLens",
} as const;

export const THEME_STORAGE_KEY = "cardiolens-theme";

