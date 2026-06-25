import * as React from "react";

/**
 * DisclaimerBanner — the single most important piece of chrome. Calm (no alarm
 * color), persistent, and announced as a note. Copy is verbatim from copy.md.
 */
export function DisclaimerBanner() {
  return (
    <div role="note" className="border-b border-border bg-subtle">
      <div className="mx-auto flex max-w-container flex-wrap items-baseline gap-x-s3 gap-y-s1 px-s5 py-s2">
        <span className="font-mono text-2xs uppercase tracking-eyebrow text-accent-text">
          Educational ML demo
        </span>
        <span className="text-sm text-muted">
          Not medical advice — a model score on historical public research data,
          not a medical verdict and not a clinical tool.
        </span>
      </div>
    </div>
  );
}
