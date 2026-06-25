import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TickDivider } from "@/components/tick-divider";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SITE } from "@/lib/site";

export const metadata: Metadata = { title: "About" };

/**
 * /about — limitations, privacy, and the project story. Copy is verbatim from
 * copy.md. The can/cannot columns use neutral keylines (accent for "can",
 * muted for "cannot") — deliberately NOT red/green, because limits are facts,
 * not errors.
 */

const CAN = [
  "Show how one frozen model scores research-style input patterns.",
  "Explain which inputs moved a given score, within the model.",
  "Demonstrate that performance drops on unseen cohorts.",
  "Make a real ML evaluation readable.",
];

const CANNOT = [
  "Make any claim about a real person's health or give a verdict about a body.",
  "Give medical advice or a clinical recommendation.",
  "Promise its probabilities hold outside this research data.",
  "Replace a conversation with a qualified clinician.",
];

function List({
  items,
  marker,
}: {
  items: string[];
  marker: { symbol: string; className: string };
}) {
  return (
    <ul className="space-y-s3">
      {items.map((it) => (
        <li key={it} className="flex gap-s3 text-base leading-normal text-ink">
          <span aria-hidden="true" className={marker.className}>
            {marker.symbol}
          </span>
          <span>{it}</span>
        </li>
      ))}
    </ul>
  );
}

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="Honest limits"
        headline="What CardioLens can and can't do."
        intro="A short, plain account of where this educational demo is useful and where it is not."
      />

      {/* Can / cannot — neutral keylines, never red/green */}
      <div className="mt-s7 grid gap-s5 md:grid-cols-2">
        <Card className="border-l-2 p-s6" style={{ borderLeftColor: "var(--accent)" }}>
          <h2 className="eyebrow mb-s4">Can</h2>
          <List items={CAN} marker={{ symbol: "✓", className: "text-accent-text" }} />
        </Card>
        <Card
          className="border-l-2 p-s6"
          style={{ borderLeftColor: "var(--text-muted)" }}
        >
          <h2 className="mb-s4 font-mono text-xs uppercase tracking-eyebrow text-muted">
            Cannot
          </h2>
          <List items={CANNOT} marker={{ symbol: "—", className: "text-muted" }} />
        </Card>
      </div>

      <TickDivider className="my-s8" />

      {/* When to seek real help — important, must be present */}
      <Card className="border-l-2 p-s6" style={{ borderLeftColor: "var(--accent)" }}>
        <SectionHeader
          headline="If you're worried about your heart."
          intro="This is an educational demo, not a source of medical advice. If you have symptoms or concerns, contact a qualified clinician or your local emergency number. CardioLens cannot help with an urgent situation."
        />
      </Card>

      <TickDivider className="my-s8" />

      {/* Privacy */}
      <SectionHeader
        headline="Your inputs are not stored."
        intro="The /try page sends your input pattern to the model to compute a score and a model-based explanation, then forgets it. No accounts, no database, no analytics of what you enter, no cookies tracking your medical inputs."
      />

      <TickDivider className="my-s8" />

      {/* Project story / stack */}
      <SectionHeader
        headline="Why this exists."
        intro="CardioLens turns a finished, frozen heart-disease ML study into a readable case study — built to show evaluation done honestly, limitations and all."
      />
      <p className="mt-s5 max-w-measure font-mono text-2xs leading-normal text-muted">
        Static Next.js front end · existing FastAPI model service · charts drawn
        from the project's real research reports.
      </p>
      <div className="mt-s6">
        <Button href={SITE.repoUrl}>View the code on GitHub</Button>
        <p className="mt-s3 font-mono text-2xs text-muted">
          The repository link is a placeholder until the project owner wires in the
          URL.
        </p>
      </div>
    </div>
  );
}
