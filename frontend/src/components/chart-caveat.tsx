import * as React from "react";
import { cn } from "@/lib/utils";

/**
 * ChartCaveat — the one-line honest caveat that ships beneath every visual
 * (the recurring rhythm from copy.md / components.md). Mono, muted, small so it
 * reads as a measurement footnote, never as alarm copy.
 */
export function ChartCaveat({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <p className={cn("mt-s3 font-mono text-2xs leading-normal text-muted", className)}>
      {children}
    </p>
  );
}
