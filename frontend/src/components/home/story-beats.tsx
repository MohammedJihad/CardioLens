import * as React from "react";
import { Card } from "@/components/ui/card";

/**
 * StoryBeats — the three-beat narrative (BUILD / EXPLAIN / STRESS-TEST).
 * Copy is verbatim from copy.md. The numbered eyebrows are a true sequence,
 * so the 01/02/03 markers are meaningful here.
 */
const BEATS = [
  {
    eyebrow: "Beat 01 — Build",
    headline: "A leakage-free model, built carefully.",
    intro:
      "Cross-validation without target leakage, a corrected target inversion, and harmonized encodings — so the score reflects the data, not a shortcut.",
    caveat: "Built on historical public research data only.",
  },
  {
    eyebrow: "Beat 02 — Explain",
    headline: "Every score comes with its reasons.",
    intro:
      "For any input pattern, the model shows which values pushed its score up and which pushed it down — a model-based explanation, not a cause.",
    caveat: "Within this model — not a claim about the body.",
  },
  {
    eyebrow: "Beat 03 — Stress-test",
    headline: "Then we tried to break it.",
    intro:
      "We ran the same frozen model on cohorts it had never seen. Its ability to rank cases partly survived; its calibrated probabilities did not.",
    caveat: "Discrimination partially transfers; calibration does not.",
  },
];

export function StoryBeats() {
  return (
    <section aria-labelledby="story-heading" className="mx-auto max-w-container px-s5 py-s9">
      <h2 id="story-heading" className="visually-hidden">
        How CardioLens works, in three beats
      </h2>
      <ol className="grid gap-s5 md:grid-cols-3">
        {BEATS.map((beat) => (
          <li key={beat.eyebrow}>
            <Card className="flex h-full flex-col p-s6">
              <p className="eyebrow">{beat.eyebrow}</p>
              <h3 className="mt-s3 text-2xl leading-snug">{beat.headline}</h3>
              <p className="mt-s3 flex-1 text-base leading-normal text-muted">
                {beat.intro}
              </p>
              <p className="mt-s5 border-t border-border pt-s3 font-mono text-xs leading-normal text-muted">
                {beat.caveat}
              </p>
            </Card>
          </li>
        ))}
      </ol>
    </section>
  );
}
