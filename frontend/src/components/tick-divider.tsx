import * as React from "react";
import { cn } from "@/lib/utils";

/**
 * TickDivider — the measurement-scale rule (the signature "lens" motif): a
 * hairline with evenly spaced ticks, echoing the score-gauge scale. Purely
 * decorative, so it is hidden from assistive tech.
 */
export function TickDivider({ className }: { className?: string }) {
  return (
    <div
      aria-hidden="true"
      className={cn("h-[14px] w-full border-b border-border opacity-70", className)}
      style={{
        backgroundImage:
          "repeating-linear-gradient(90deg, var(--border-strong) 0 1px, transparent 1px 28px)",
      }}
    />
  );
}
