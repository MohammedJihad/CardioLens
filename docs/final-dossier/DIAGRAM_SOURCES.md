# Diagram Sources — CardioLens Dossier

All figures were generated **programmatically for this dossier** from the project's frozen
reports and design tokens. No external image assets, no Mermaid/Graphviz binaries, and no
copyrighted material were used. Two techniques were used:

1. **Hand-authored inline SVG** (CardioLens design tokens) — for structural / flow diagrams.
   Exported as standalone files in `assets/diagram_*.svg`.
2. **matplotlib** — for the data-driven charts, reading values verbatim from the frozen
   reports. Exported as `assets/chart_*.png`.

## Flow / structure diagrams (inline SVG → `assets/diagram_*.svg`)
| File | Figure | Description |
|---|---|---|
| `diagram_pipeline.svg` | Fig 1 | ML pipeline: data → preprocess → train+CV → internal → external → limits → web app |
| `diagram_architecture.svg` | Fig 8 | Next.js → FastAPI → frozen model + reports-summary.json snapshot |
| `diagram_calibration_vs_discrimination.svg` | Fig 5 | Conceptual ranking vs reliability, annotated with real Brier values |
| `diagram_sitemap.svg` | Fig 9 | Home + six pages |
| `diagram_explanation_flow.svg` | Fig 10 | Record → model score → marginal contributions → up/down factors |
| `diagram_guardrails.svg` | Fig 11 | Five safety layers (frozen science → human in the loop) |
| `diagram_privacy_flow.svg` | Fig 12 | /try input → /predict → score → rendered once → no storage |
| `diagram_timeline.svg` | Fig 13 | Phases 0–5 (science) + A–F (web) |

## Data-driven charts (matplotlib → `assets/chart_*.png`)
| File | Figure | Source data |
|---|---|---|
| `chart_cv_models.png` | Fig 2 | `reports/cv_results.json` |
| `chart_external_auc.png` | Fig 3 | `reports/external_validation_metrics.csv` |
| `chart_missingness.png` | Fig 4 | `reports/external_validation_metrics.csv` |
| `chart_brier.png` | Fig 6 | internal Brier (`metrics.json`) + external (`external_validation_metrics.csv`) |
| `chart_threshold.png` | Fig 7 | `reports/threshold_test_evaluation.csv` + internal confusion |

## Native (rendered directly in the PDF from tokens/copy)
- Score gauge (teal→amber→coral arc), colour palette swatches, typography specimen, and the
  page layout previews — all rendered from `docs/design/tokens.css` and `docs/design/copy.md`.

## Reproduce
The builder script lives outside the frozen tree and reads only `web-data/reports-summary.json`
and `reports/*` (read-only). It writes solely under `docs/final-dossier/`. Tooling: WeasyPrint
(HTML/CSS → PDF), matplotlib (charts), and the project's brand fonts (Newsreader, Hanken
Grotesk, IBM Plex Mono).

*Generated June 2026. Not medical advice — every number traces to the frozen research reports.*
