/**
 * Md Kanok Miah — Middleware
 * Purpose: Override cache-control headers for CDN freshness.
 * Next.js 16 prerendered pages emit s-maxage=31536000 (1 year) by default,
 * which long-caches at the Hostinger CDN edge.  This middleware shortens
 * that window so ISR revalidate (60s) is actually honoured by the CDN.
 *
 * Pattern: match HTML page requests, set s-maxage to match the ISR window
 * with a stale-while-revalidate grace period.
 */

import { NextResponse } from "next/server";

const PAGE_RE = /\.html$|^\/[^.]*$/;          // bare paths + .html

export function middleware(request) {
  const { pathname } = request.nextUrl;

  // Only act on HTML page requests
  if (!PAGE_RE.test(pathname)) {
    return NextResponse.next();
  }

  const response = NextResponse.next();

  response.headers.set(
    "Cache-Control",
    "public, s-maxage=300, stale-while-revalidate=600",
  );

  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - api (API routes)
     * - images / fonts / media
     */
    "/((?!_next/static|_next/image|favicon\\.ico|api/|[^/]*\\.(?:png|jpg|jpeg|gif|webp|svg|ico|woff2?|css|js)).*)",
  ],
};
