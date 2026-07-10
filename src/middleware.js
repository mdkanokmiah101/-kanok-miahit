/**
 * Middleware — override CDN-friendly cache headers on every response.
 * Next.js ISR sets s-maxage=31536000 (1 year) which tells external CDNs
 * (like Hostinger hCDN) to cache for a full year without re-validation.
 * This middleware forces a short CDN TTL so new deploys propagate quickly.
 *
 * Matches: all routes (/, /services/*, /blog/*, /industries/*, etc.)
 */
import { NextResponse } from 'next/server';

export function middleware(request) {
  const response = NextResponse.next();

  // Override Cache-Control for the outer (CDN) layer.
  // - s-maxage=60  →  external CDNs cache for 60 seconds only
  // - stale-while-revalidate=600  →  serve stale up to 10 min while revalidating
  // - Vercel's own edge cache still honours the ISR revalidate value internally
  response.headers.set(
    'Cache-Control',
    'public, s-maxage=60, stale-while-revalidate=600',
  );

  // Tell Vercel's edge to also respect a short CDN TTL
  response.headers.set('CDN-Cache-Control', 's-maxage=60, stale-while-revalidate=600');

  return response;
}

export const config = {
  matcher: [
    // Match all page routes, excluding static assets, _next, and API
    '/((?!_next/static|_next/image|favicon.ico|apple-touch-icon|android-chrome|favicon-|site\\.webmanifest).*)',
  ],
};
