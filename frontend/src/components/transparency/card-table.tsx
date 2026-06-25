import * as React from "react";

/**
 * CardTable — a small, readable data table for the model/data-card figures.
 * Real <table> semantics (caption + column headers) so the numbers are legible
 * to assistive tech as well as sighted readers. Numbers are transcribed
 * verbatim from the frozen report docs (reports/model_card.md, data_card.md).
 */
export function CardTable({
  caption,
  headers,
  rows,
  highlightFirstCol = true,
}: {
  caption: string;
  headers: string[];
  rows: (string | { text: string; strong?: boolean })[][];
  highlightFirstCol?: boolean;
}) {
  const cell = (c: string | { text: string; strong?: boolean }) =>
    typeof c === "string" ? { text: c, strong: false } : c;
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-left text-sm">
        <caption className="mb-s3 text-left text-sm text-muted">{caption}</caption>
        <thead>
          <tr className="border-b border-border-strong">
            {headers.map((h, i) => (
              <th
                key={h}
                scope="col"
                className={`py-s2 pr-s4 font-mono text-2xs uppercase tracking-eyebrow text-muted ${
                  i === 0 ? "" : "text-right"
                }`}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri} className="border-b border-border">
              {row.map((c, ci) => {
                const { text, strong } = cell(c);
                const isHead = ci === 0 && highlightFirstCol;
                const Tag = isHead ? "th" : "td";
                return (
                  <Tag
                    key={ci}
                    scope={isHead ? "row" : undefined}
                    className={[
                      "py-s2 pr-s4 align-top",
                      ci === 0 ? "text-ink" : "text-right font-mono tabular-nums text-muted",
                      strong ? "font-semibold text-ink" : "",
                    ].join(" ")}
                  >
                    {text}
                  </Tag>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
