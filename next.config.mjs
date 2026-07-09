/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          // Hostinger hCDN — the 'private' directive is meant to prevent shared caching,
          // but Hostinger hCDN overrides it. Use public + short s-maxage so the CDN
          // checks with the origin every 60s instead of caching the first response for 1 year.
          { key: 'Cache-Control', value: 'public, max-age=0, s-maxage=60, must-revalidate' },
          { key: 'Pragma', value: 'no-cache' },
          { key: 'Expires', value: '0' },
          { key: 'Vary', value: 'Accept-Encoding, Cookie, User-Agent' },
          { key: 'Surrogate-Control', value: 'no-store, no-cache, max-age=0' },
          { key: 'CDN-Cache-Control', value: 'no-store, max-age=0, private' },
          { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
          { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        ],
      },
    ];
  },
};

export default nextConfig;
