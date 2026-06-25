import * as React from "react";

/**
 * HeroLattice — the static "lens" backdrop: nested gauge arcs in the gauge
 * palette at low opacity, faded out toward the bottom. Decorative only
 * (aria-hidden), no motion. Mirrors the lattice in styleguide.html.
 */
export function HeroLattice() {
  return (
    <div
      aria-hidden="true"
      className="hero-lattice pointer-events-none absolute inset-0 -z-10"
      style={{
        WebkitMaskImage: "linear-gradient(180deg, #000 0%, transparent 78%)",
        maskImage: "linear-gradient(180deg, #000 0%, transparent 78%)",
      }}
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1000 460"
        preserveAspectRatio="xMidYMid slice"
        role="presentation"
      >
        <g fill="none" strokeWidth={1.5}>
          <path d="M40 420 A380 380 0 0 1 800 420" stroke="var(--border-strong)" opacity={0.6} />
          <path d="M120 420 A300 300 0 0 1 720 420" stroke="var(--gauge-low)" opacity={0.5} />
          <path d="M200 420 A220 220 0 0 1 640 420" stroke="var(--gauge-mid)" opacity={0.45} />
          <path d="M280 420 A140 140 0 0 1 560 420" stroke="var(--gauge-high)" opacity={0.4} />
        </g>
      </svg>
    </div>
  );
}
