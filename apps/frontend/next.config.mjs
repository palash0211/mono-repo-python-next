/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable SSR for SPA mode
  reactStrictMode: true,
  swcMinify: true,
  // Force all pages to be client-side rendered
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;

