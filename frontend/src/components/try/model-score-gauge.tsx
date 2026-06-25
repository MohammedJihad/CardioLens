"use client";

import * as React from "react";

/**
 * ModelScoreGauge — the signature element.
 *
 * A 180° calibrated arc (geometry from styleguide.html: cx/cy 200,200, r=160,
 * arc length = π·r). The teal→amber→coral gradient encodes MODEL-SCORE
 * MAGNITUDE ONLY — never a health verdict. A hairline tick scale frames it and
 * a mono readout shows the value. Each <linearGradient> gets a unique id via
 * useId so multiple gauges never collide. The sweep is plain rAF and jumps
 * straight to value under prefers-reduced-motion.
 */
const CX = 200;
const CY = 200;
const R = 160;
const ARC_LEN = Math.PI * R; // ≈ 502.65
const ARC_PATH = `M${CX - R} ${CY} A${R} ${R} 0 0 1 ${CX + R} ${CY}`;

const TICKS = [
  { x1: 32, y1: 200, x2: 20, y2: 200 },
  { x1: 81, y1: 81, x2: 73, y2: 73 },
  { x1: 200, y1: 32, x2: 200, y2: 20 },
  { x1: 319, y1: 81, x2: 327, y2: 73 },
  { x1: 368, y1: 200, x2: 380, y2: 200 },
];

function knobPoint(score: number) {
  const theta = (180 - score * 180) * (Math.PI / 180);
  return { x: CX + R * Math.cos(theta), y: CY - R * Math.sin(theta) };
}

function knobColor(score: number): string {
  if (score < 1 / 3) return "var(--gauge-low)";
  if (score < 2 / 3) return "var(--gauge-mid)";
  return "var(--gauge-high)";
}

function easeOutCubic(t: number) {
  return 1 - Math.pow(1 - t, 3);
}

export function ModelScoreGauge({ score }: { score: number }) {
  const clamped = Math.min(1, Math.max(0, score));
  const gradientId = React.useId();
  const [v, setV] = React.useState(0);

  React.useEffect(() => {
    const prefersReduced =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReduced) {
      setV(clamped);
      return;
    }
    let raf = 0;
    const start = performance.now();
    const duration = 600;
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      setV(clamped * easeOutCubic(t));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [clamped]);

  const knob = knobPoint(v);

  return (
    <figure className="m-0 text-center">
      <svg
        viewBox="0 0 400 230"
        className="mx-auto h-auto w-full max-w-[320px]"
        role="img"
        aria-label={`Model score ${clamped.toFixed(2)} out of 1 — a model score on research data; the gauge shows magnitude only.`}
      >
        <defs>
          <linearGradient
            id={gradientId}
            x1="40"
            y1="0"
            x2="360"
            y2="0"
            gradientUnits="userSpaceOnUse"
          >
            <stop offset="0" stopColor="var(--gauge-low)" />
            <stop offset="0.5" stopColor="var(--gauge-mid)" />
            <stop offset="1" stopColor="var(--gauge-high)" />
          </linearGradient>
        </defs>

        {/* Track */}
        <path d={ARC_PATH} fill="none" stroke="var(--gauge-track)" strokeWidth={16} strokeLinecap="round" />
        {/* Value arc */}
        <path
          d={ARC_PATH}
          fill="none"
          stroke={`url(#${gradientId})`}
          strokeWidth={16}
          strokeLinecap="round"
          strokeDasharray={`${ARC_LEN * v} ${ARC_LEN}`}
        />
        {/* Tick scale */}
        <g stroke="var(--border-strong)" strokeWidth={2}>
          {TICKS.map((t, i) => (
            <line key={i} x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2} />
          ))}
        </g>
        {/* Knob */}
        <circle cx={knob.x} cy={knob.y} r={9} fill="var(--bg-surface)" stroke={knobColor(clamped)} strokeWidth={3.5} />
      </svg>

      <figcaption>
        <div className="font-mono text-2xs uppercase tracking-eyebrow text-muted">
          Model score
        </div>
        <div className="mt-s1 font-mono text-4xl leading-none tabular-nums text-ink">
          {v.toFixed(2)}
        </div>
        <div className="mt-s1 text-xs text-muted">
          model-estimated probability on research data
        </div>
        <p className="mx-auto mt-s4 max-w-[34ch] text-xs leading-normal text-muted">
          The gauge shows the size of the model score only — teal to coral is low
          to high magnitude, not a health verdict.
        </p>
      </figcaption>
    </figure>
  );
}
