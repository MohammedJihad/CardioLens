import * as React from "react";

/**
 * ReportCard — a download/link tile for the model card, data card, raw metrics,
 * and repository (components.md `ReportCard`). The repository URL is still a
 * placeholder (see lib/site.ts), so every tile currently resolves there; the
 * page states that plainly rather than implying a live download.
 */
export function ReportCard({
  label,
  detail,
  href,
}: {
  label: string;
  detail: string;
  href: string;
}) {
  return (
    <a
      href={href}
      className="group flex min-h-[44px] flex-col rounded-md border border-border bg-surface p-s5 no-underline shadow-sm transition-colors duration-fast hover:bg-subtle focus-visible:outline-focus"
    >
      <span className="flex items-center gap-s2 text-base font-medium text-ink">
        <span aria-hidden="true" className="text-accent-text">
          ↗
        </span>
        {label}
      </span>
      <span className="mt-s2 text-sm text-muted">{detail}</span>
    </a>
  );
}
