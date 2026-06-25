import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

/**
 * Badge — small neutral/informational marker (mono, tracked). Never used to
 * signal a good/bad health outcome — purely status/labelling.
 */
const badgeVariants = cva(
  "inline-flex items-center rounded-full border font-mono text-2xs tracking-wide " +
    "px-s3 py-s1 leading-none",
  {
    variants: {
      variant: {
        neutral: "bg-subtle text-ink border-border",
        accent: "bg-subtle text-accent-text border-border",
      },
    },
    defaultVariants: { variant: "neutral" },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
