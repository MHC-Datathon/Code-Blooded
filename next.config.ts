import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === "production";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "export",                  // <-- new static export flag
  basePath: isProd ? "/Code-Blooded" : "",
  assetPrefix: isProd ? "/Code-Blooded/" : "",
};

export default nextConfig;