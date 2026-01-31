import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  /*
    async rewrites() {
      return [
        {
          source: '/api/python/:path*',
          destination: 'process.env.NEXT_PUBLIC_API_URL/:path*', // Needs real Env var in Prod
        },
      ]
    },
  */
};

export default nextConfig;
