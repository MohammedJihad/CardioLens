import * as React from "react";

/**
 * NotInSnapshot — the honest empty-state for a visual whose numeric series is
 * NOT in `reports-summary.json` (ROC/PR curve coordinates, a full threshold
 * sweep, learning-curve points, calibration bins). We never invent or
 * interpolate those — we say so plainly and, where we have them, show the
 * summary figures we DO have instead.
 *
 * The headline reuses the exact `Chart no-data` microcopy from copy.md.
 */
export function NotInSnapshot({
  detail,
  children,
}: {
  detail: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="rounded-md border border-dashed border-border bg-subtle p-s5">
      <p className="font-mono text-2xs uppercase tracking-eyebrow text-muted">
        Not in the report snapshot
      </p>
      <p className="mt-s2 text-base text-ink">
        This chart&apos;s data isn&apos;t available in the report snapshot.
      </p>
      <p className="mt-s2 max-w-measure text-sm leading-normal text-muted">{detail}</p>
      {children ? <div className="mt-s4">{children}</div> : null}
    </div>
  );
}
