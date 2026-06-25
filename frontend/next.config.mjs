/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Node-only production build — no Python at build time. Data is read from the
  // committed src/data/reports-summary.json snapshot.
};

export default nextConfig;
