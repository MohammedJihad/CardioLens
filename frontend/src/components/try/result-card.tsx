import * as React from "react";
import { Card } from "@/components/ui/card";
import { ModelScoreGauge } from "./model-score-gauge";
import { FactorBars } from "./factor-bars";
import { PlainLanguageBox } from "./plain-language-box";
import { reports } from "@/data/reports";
import type { PredictionResponse } from "@/lib/api";

/**
 * ResultCard — gauge + above/below band + "What moved this score" explanation
 * + plain-language box. The band uses the 0.20 selected threshold (from the
 * reports snapshot) and is a neutral chip (no pass/fail color).
 */
export function ResultCard({ data }: { data: PredictionResponse }) {
  const selected = reports.thresholds.selected; // 0.2, from the frozen reports
  const thresholdLabel = selected.toFixed(2); // "0.20"
  const above = data.model_score >= selected;
  const band = above ? "Above" : "Below";

  return (
    <Card className="p-s6">
      <div className="grid gap-s7 md:grid-cols-[minmax(0,320px)_1fr]">
        {/* Gauge + band */}
        <div>
          <ModelScoreGauge score={data.model_score} />
          <div className="mt-s5 flex justify-center">
            <span className="inline-flex items-center rounded-full border border-border bg-subtle px-s4 py-s2 font-mono text-sm text-ink">
              {band} the {thresholdLabel} threshold
            </span>
          </div>
        </div>

        {/* Explanation */}
        <div>
          <h2 className="text-2xl leading-snug">What moved this score</h2>
          <p className="mt-s2 max-w-measure text-base leading-normal text-muted">
            Within this model, these inputs pushed the score up or down. This is a
            model-based explanation — it is not causal and not medical advice.
          </p>
          <div className="mt-s5">
            <FactorBars
              positive={data.top_positive_factors}
              negative={data.top_negative_factors}
            />
          </div>
        </div>
      </div>

      <div className="mt-s7">
        <PlainLanguageBox />
      </div>
    </Card>
  );
}
