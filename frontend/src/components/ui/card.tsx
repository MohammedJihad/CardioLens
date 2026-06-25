import * as React from "react";
import { cn } from "@/lib/utils";

/** Card — surface panel with hairline framing and soft elevation. */
export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-md border border-border bg-surface shadow-sm",
        className
      )}
      {...props}
    />
  );
}
