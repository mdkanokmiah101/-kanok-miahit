/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=0, s-maxage=0, must-revalidate, no-cache, no-store' },
          { key: 'Vary', value: 'Accept-Encoding, Cookie' },
          { key: 'Surrogate-Control', value: 'no-store' },
          { key: 'CDN-Cache-Control', value: 'no-store' },
        ],
      },
      {
        source: '/(.*)',
        headers: [
          { key: 'Cache-Control', value: 'private, no-cache, no-store, must-revalidate, max-age=0, s-maxage=0' },
          { key: 'CDN-Cache-Control', value: 'no-store, max-age=0' },
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
