import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === "production";

const nextConfig = {
  reactStrictMode: true,
  output: "export",
  basePath: isProd ? "/Code-Blooded" : "",
  assetPrefix: isProd ? "/Code-Blooded/" : "",
};

export default nextConfig;