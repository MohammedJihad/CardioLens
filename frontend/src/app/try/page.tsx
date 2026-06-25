import type { Metadata } from "next";
import { SectionHeader } from "@/components/section-header";
import { TryDemo } from "@/components/try/try-demo";

export const metadata: Metadata = { title: "Try the model" };

export default function TryPage() {
  return (
    <div className="mx-auto max-w-container px-s5 py-s9">
      <SectionHeader
        as="h1"
        eyebrow="Live · Educational demo"
        headline="Run an input pattern through the model."
        intro="Enter a research-style input pattern, or load a preset, to see the model score and a model-based explanation. This is the one page that talks to the live model."
      />
      <TryDemo />
    </div>
  );
}
