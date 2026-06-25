import * as React from "react";
import { cn } from "@/lib/utils";

/**
 * SectionHeader — encodes the page rhythm: eyebrow -> headline -> plain intro.
 * `as` sets the heading level so each page keeps a single <h1> and a logical
 * outline. Headlines use the display serif; intro is muted and measure-capped.
 */
export function SectionHeader({
  eyebrow,
  headline,
  intro,
  as = "h2",
  className,
  align = "start",
}: {
  eyebrow?: string;
  headline: React.ReactNode;
  intro?: React.ReactNode;
  as?: "h1" | "h2" | "h3";
  className?: string;
  align?: "start" | "center";
}) {
  const Heading = as;
  const sizeForLevel =
    as === "h1" ? "text-4xl md:text-5xl" : as === "h2" ? "text-3xl" : "text-2xl";
  return (
    <div
      className={cn(
        align === "center" && "mx-auto text-center",
        className
      )}
    >
      {eyebrow ? <p className="eyebrow mb-s3">{eyebrow}</p> : null}
      <Heading className={cn(sizeForLevel, "leading-snug text-balance")}>
        {headline}
      </Heading>
      {intro ? (
        <p
          className={cn(
            "mt-s4 max-w-measure text-lg leading-normal text-muted",
            align === "center" && "mx-auto"
          )}
        >
          {intro}
        </p>
      ) : null}
    </div>
  );
}
