import * as React from "react";
import { SectionHeader } from "@/components/section-header";

/**
 * RouteStub — placeholder for routes that are not built yet (so the nav never
 * 404s). Renders only a SectionHeader; the real page arrives in a later phase.
 */
export function RouteStub({
  eyebrow,
  headline,
  intro,
}: {
  eyebrow: string;
  headline: string;
  intro: string;
}) {
  return (
    <div className="mx-auto max-w-container px-s5 py-s10">
      <SectionHeader as="h1" eyebrow={eyebrow} headline={headline} intro={intro} />
      <p className="mt-s6 font-mono text-xs text-muted">
        This page is coming in a later build phase.
      </p>
    </div>
  );
}
