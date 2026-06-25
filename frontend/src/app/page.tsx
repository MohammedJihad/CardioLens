import { Hero } from "@/components/home/hero";
import { TrustStrip } from "@/components/home/trust-strip";
import { StoryBeats } from "@/components/home/story-beats";
import { ClosingCta } from "@/components/home/closing-cta";
import { TickDivider } from "@/components/tick-divider";

export default function HomePage() {
  return (
    <>
      <Hero />
      <TickDivider />
      <TrustStrip />
      <TickDivider />
      <StoryBeats />
      <ClosingCta />
    </>
  );
}
