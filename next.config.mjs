/** @type {import('next').NextConfig} */
const nextConfig = {
  metadataBase: new URL('https://kanokmiah.com.bd'),
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          // Hostinger hCDN — aggressively prevent caching.
          // Hostinger hCDN was caching old responses for 1 year because Vercel's default
          // ISR cache-control (s-maxage=31536000) was served instead of these headers.
          // We use 'no-store' to prevent all caching and 'private' as override for CDNs
          // that ignore Surrogate-Control.
          { key: 'Cache-Control', value: 'no-store, no-cache, must-revalidate, proxy-revalidate, private, max-age=0, s-maxage=0' },
          { key: 'Pragma', value: 'no-cache' },
          { key: 'Expires', value: '-1' },
          { key: 'Vary', value: 'Accept-Encoding, Cookie, User-Agent' },
          { key: 'Surrogate-Control', value: 'no-store, no-cache, max-age=0, private' },
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
