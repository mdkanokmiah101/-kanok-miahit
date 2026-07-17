/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/locations/chittagong',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/sylhet',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/khulna',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/rajshahi',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/barisal',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/rangpur',
        destination: '/locations/dhaka',
        permanent: true,
      },
      {
        source: '/locations/mymensingh',
        destination: '/locations/dhaka',
        permanent: true,
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          // Hostinger hCDN — aggressively prevent caching.
          // Hostinger hCDN was caching old responses for 1 year because Vercel's default
          // ISR cache-control (s-maxage=31536000) was served in addition to these headers.
          // The CDN-Cache-Control header is the authoritative one for hCDN; if ignored,
          // Surrogate-Control (Akamai-origin) and Cache-Control both say max-age=0.
          { key: 'Cache-Control', value: 'public, no-cache, must-revalidate, proxy-revalidate, max-age=0, s-maxage=0, stale-while-revalidate=30' },
          { key: 'CDN-Cache-Control', value: 'no-cache, max-age=0, stale-while-revalidate=30' },
          { key: 'Surrogate-Control', value: 'max-age=0, stale-while-revalidate=30' },
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
