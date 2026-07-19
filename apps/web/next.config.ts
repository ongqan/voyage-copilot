import type { NextConfig } from "next";

const staticExport = process.env.STATIC_EXPORT === "true";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: staticExport ? "export" : undefined,
  trailingSlash: staticExport,
  basePath: staticExport ? "/voyage-copilot" : "",
};

export default nextConfig;
