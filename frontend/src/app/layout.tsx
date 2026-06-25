import type { Metadata } from "next";
import { Newsreader, Hanken_Grotesk, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { ThemeScript } from "@/components/chrome/theme-script";
import { DisclaimerBanner } from "@/components/chrome/disclaimer-banner";
import { Navigation } from "@/components/chrome/navigation";
import { Footer } from "@/components/chrome/footer";

const newsreader = Newsreader({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  display: "swap",
  variable: "--font-newsreader",
  // Newsreader has no Next.js fallback-metric entry; disable the auto override
  // to avoid a build warning. Our token fallback stack (Georgia, Times) applies.
  adjustFontFallback: false,
});

const hanken = Hanken_Grotesk({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
  variable: "--font-hanken",
});

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  display: "swap",
  variable: "--font-plex-mono",
});

export const metadata: Metadata = {
  title: {
    default: "CardioLens — a calibrated lens on a heart-disease model",
    template: "%s · CardioLens",
  },
  description:
    "An educational ML demo that presents a frozen heart-disease model as a readable case study — model scores on historical public research data. Not medical advice.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const fontVars = `${newsreader.variable} ${hanken.variable} ${plexMono.variable}`;
  return (
    <html lang="en" suppressHydrationWarning className={fontVars}>
      <body className="min-h-screen bg-bg text-ink antialiased">
        <ThemeScript />
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
        <header>
          <DisclaimerBanner />
          <Navigation />
        </header>
        <main id="main-content" tabIndex={-1} className="outline-none">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
