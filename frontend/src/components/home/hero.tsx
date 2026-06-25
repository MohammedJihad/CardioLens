import * as React from "react";
import { Button } from "@/components/ui/button";
import { HeroLattice } from "./hero-lattice";

/** Home hero — the thesis. Copy is verbatim from copy.md (/ — Home). */
export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <HeroLattice />
      <div className="mx-auto max-w-container px-s5 pb-s8 pt-s9">
        <p className="eyebrow mb-s3">Educational ML demo</p>
        <h1 className="max-w-[18ch] text-4xl leading-tight tracking-tight md:text-5xl">
          A calibrated lens on a heart-disease model.
        </h1>
        <p className="mt-s5 max-w-[54ch] text-lg leading-normal text-muted">
          See how one frozen machine-learning model reads historical public
          research data — what it gets right, what it doesn&apos;t, and where its
          confidence quietly breaks down.
        </p>
        <div className="mt-s6 flex flex-wrap gap-s3">
          <Button href="/try">Try the model</Button>
          <Button href="/results" variant="secondary">
            Read the results
          </Button>
        </div>
        <p className="mt-s5 font-mono text-xs text-muted">
          An educational demo. Not medical advice, not a medical verdict.
        </p>
      </div>
    </section>
  );
}
