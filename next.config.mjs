/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          // Hostinger hCDN aggressively overrides Cache-Control. Setting private
          // + no-store is the strongest signal we can send from the application.
          // The 'private' directive SHOULD prevent shared/CDN caching per HTTP spec.
          { key: 'Cache-Control', value: 'private, no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate' },
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
