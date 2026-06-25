import * as React from "react";
import { Button } from "@/components/ui/button";

/** Closing CTA — copy verbatim from copy.md (/ — Home, closing block). */
export function ClosingCta() {
  return (
    <section className="mx-auto max-w-container px-s5 pb-s10 pt-s7">
      <div className="rounded-lg border border-border bg-subtle px-s6 py-s8 text-center">
        <h2 className="mx-auto max-w-[22ch] text-3xl leading-snug">
          Run one pattern through the lens.
        </h2>
        <p className="mx-auto mt-s4 max-w-[46ch] text-lg leading-normal text-muted">
          A single input pattern, scored live and explained. Nothing you enter is
          stored.
        </p>
        <div className="mt-s6 flex justify-center">
          <Button href="/try">Try the model</Button>
        </div>
      </div>
    </section>
  );
}
