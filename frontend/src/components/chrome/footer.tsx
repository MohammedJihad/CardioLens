import * as React from "react";
import Link from "next/link";
import { NAV_LINKS, SITE } from "@/lib/site";
import { reports } from "@/data/reports";

/** Footer — tagline, the "inputs are not stored" honesty line, link columns. */
export function Footer() {
  return (
    <footer className="border-t border-border bg-subtle">
      <div className="mx-auto max-w-container px-s5 py-s8">
        <div className="grid gap-s7 md:grid-cols-[1.4fr_1fr]">
          <div className="max-w-measure">
            <p className="font-display text-xl text-ink">{SITE.tagline}</p>
            <p className="mt-s3 text-sm leading-normal text-muted">
              Every number on this site comes from the project&apos;s research
              reports. Inputs you try are sent to the model to compute a score and
              are not stored.
            </p>
          </div>

          <nav aria-label="Footer" className="grid grid-cols-2 gap-s5">
            <div>
              <h2 className="font-mono text-2xs uppercase tracking-eyebrow text-muted">
                Explore
              </h2>
              <ul className="mt-s3 space-y-s2">
                {NAV_LINKS.filter((l) => l.href !== "/").map((l) => (
                  <li key={l.href}>
                    <Link
                      href={l.href}
                      className="text-sm text-muted no-underline hover:text-ink"
                    >
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h2 className="font-mono text-2xs uppercase tracking-eyebrow text-muted">
                Responsible use
              </h2>
              <ul className="mt-s3 space-y-s2">
                <li>
                  <Link href="/about" className="text-sm text-muted no-underline hover:text-ink">
                    Limitations
                  </Link>
                </li>
                <li>
                  <Link href="/transparency" className="text-sm text-muted no-underline hover:text-ink">
                    Model &amp; data cards
                  </Link>
                </li>
                <li>
                  <a
                    href={SITE.repoUrl}
                    className="text-sm text-muted no-underline hover:text-ink"
                  >
                    View the code on GitHub
                  </a>
                </li>
              </ul>
            </div>
          </nav>
        </div>

        <p className="mt-s7 border-t border-border pt-s5 font-mono text-2xs text-muted">
          © {reports.year} {SITE.name} — an educational machine-learning case
          study. Not medical advice.
        </p>
      </div>
    </footer>
  );
}
