"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_LINKS } from "@/lib/site";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "./theme-toggle";

function isActive(pathname: string, href: string) {
  return href === "/" ? pathname === "/" : pathname.startsWith(href);
}

/**
 * Navigation — wordmark + the 7 links (same order everywhere) + theme toggle.
 * Sticky, hairline-bottomed, blurred surface. Collapses to a disclosure menu
 * under `md`. The skip link lives first in <body> (see layout).
 */
export function Navigation() {
  const pathname = usePathname() ?? "/";
  const [open, setOpen] = React.useState(false);

  // Close the mobile menu on route change.
  React.useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <nav
      aria-label="Main"
      className="sticky top-0 z-sticky border-b border-border backdrop-blur bg-[color-mix(in_srgb,var(--bg-surface)_85%,transparent)]"
    >
      <div className="mx-auto flex h-[60px] max-w-container items-center justify-between px-s5">
        <Link
          href="/"
          className="font-mono text-base font-semibold tracking-wide text-ink no-underline"
        >
          Cardio<span className="text-accent-text">Lens</span>
        </Link>

        {/* Desktop links */}
        <ul className="hidden items-center gap-s2 md:flex">
          {NAV_LINKS.map((link) => {
            const active = isActive(pathname, link.href);
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={cn(
                    "inline-flex min-h-[40px] items-center rounded-sm px-s3 text-sm no-underline transition-colors duration-fast",
                    active
                      ? "text-accent-text"
                      : "text-muted hover:bg-subtle hover:text-ink"
                  )}
                >
                  {link.label}
                </Link>
              </li>
            );
          })}
        </ul>

        <div className="flex items-center gap-s2">
          <ThemeToggle />
          {/* Mobile menu button */}
          <button
            type="button"
            aria-expanded={open}
            aria-controls="mobile-nav"
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((v) => !v)}
            className="inline-flex min-h-[40px] min-w-[40px] items-center justify-center rounded-full border border-border bg-subtle text-ink transition-colors duration-fast hover:bg-border focus-visible:outline-focus md:hidden"
          >
            <span aria-hidden="true" className="text-base leading-none">
              {open ? "✕" : "☰"}
            </span>
          </button>
        </div>
      </div>

      {/* Mobile panel */}
      {open ? (
        <ul
          id="mobile-nav"
          className="border-t border-border bg-surface px-s5 py-s3 md:hidden"
        >
          {NAV_LINKS.map((link) => {
            const active = isActive(pathname, link.href);
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={cn(
                    "flex min-h-[44px] items-center rounded-sm px-s2 text-base no-underline",
                    active ? "text-accent-text" : "text-ink hover:bg-subtle"
                  )}
                >
                  {link.label}
                </Link>
              </li>
            );
          })}
        </ul>
      ) : null}
    </nav>
  );
}
