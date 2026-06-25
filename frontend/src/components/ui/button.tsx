import * as React from "react";
import Link from "next/link";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

/**
 * Button — themed to CardioLens tokens. shadcn-style cva variants.
 * Primary = navy; secondary = surface + hairline; ghost = transparent.
 * Min target 44px (quality floor). Focus ring inherited from globals.
 */
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-s2 rounded-sm font-body text-sm font-semibold " +
    "min-h-[44px] px-s5 transition-colors duration-fast ease-standard " +
    "focus-visible:outline-focus disabled:pointer-events-none disabled:opacity-50 " +
    "active:translate-y-px select-none",
  {
    variants: {
      variant: {
        primary: "bg-primary text-onprimary hover:bg-primary-hover",
        secondary: "bg-surface text-ink border border-border hover:bg-subtle",
        ghost: "bg-transparent text-ink hover:bg-subtle",
      },
      size: {
        default: "h-11",
        sm: "min-h-[36px] h-9 px-s4 text-sm",
      },
    },
    defaultVariants: { variant: "primary", size: "default" },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Render as a Next.js link instead of a <button>. */
  href?: string;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, href, ...props }, ref) => {
    const classes = cn(buttonVariants({ variant, size }), className);
    if (href) {
      return (
        <Link href={href} className={classes} aria-label={props["aria-label"]}>
          {props.children}
        </Link>
      );
    }
    return <button ref={ref} className={classes} {...props} />;
  }
);
Button.displayName = "Button";

export { buttonVariants };
