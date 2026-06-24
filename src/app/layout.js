import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Kanok MiahIT — #1 SEO Agency in Bangladesh | Local & International SEO",
  description:
    "Kanok MiahIT is Bangladesh's top SEO agency. We help local businesses rank higher on Google, generate qualified leads, and scale revenue with proven SEO strategies. Local SEO, Technical SEO, Link Building, GEO — Dhaka, Bangladesh.",
  keywords: [
    "SEO agency Bangladesh",
    "SEO services Dhaka",
    "local SEO Bangladesh",
    "Bangladesh SEO expert",
    "digital marketing agency Bangladesh",
    "on-page SEO",
    "technical SEO",
    "link building Bangladesh",
    "GEO optimization",
    "Kanok MiahIT",
  ],
  authors: [{ name: "Kanok MiahIT" }],
  creator: "Kanok MiahIT",
  publisher: "Kanok MiahIT",
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Kanok MiahIT",
    title: "Kanok MiahIT — #1 SEO Agency in Bangladesh",
    description:
      "Bangladesh's trusted SEO agency. Rank higher, grow faster, dominate search. Local & international SEO for Bangladeshi businesses.",
    url: "https://kanok-miahit.vercel.app",
  },
  twitter: {
    card: "summary_large_image",
    title: "Kanok MiahIT — #1 SEO Agency in Bangladesh",
    description:
      "Bangladesh's trusted SEO agency. Rank higher, grow faster, dominate search.",
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        {/* Canonical */}
        <link rel="canonical" href="https://kanok-miahit.vercel.app" />
        {/* Schema: Organization + LocalBusiness */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              name: "Kanok MiahIT",
              url: "https://kanok-miahit.vercel.app",
              logo: "https://kanok-miahit.vercel.app/favicon.ico",
              description:
                "Bangladesh-focused SEO agency. Local SEO, technical SEO, link building, and GEO optimization.",
              address: {
                "@type": "PostalAddress",
                addressLocality: "Dhaka",
                addressCountry: "BD",
              },
              contactPoint: {
                "@type": "ContactPoint",
                telephone: "+880-1313-019160",
                contactType: "customer service",
                availableLanguage: ["English", "Bengali"],
              },
              sameAs: [
                "https://kanokmiah.com",
              ],
            }),
          }}
        />
        {/* Schema: WebSite */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              name: "Kanok MiahIT",
              url: "https://kanok-miahit.vercel.app",
              potentialAction: {
                "@type": "SearchAction",
                target: "https://kanok-miahit.vercel.app/search?q={search_term_string}",
                "query-input": "required name=search_term_string",
              },
            }),
          }}
        />
        {/* Verification tags placeholder */}
        <meta name="google-site-verification" content="" />
        <meta name="msvalidate.01" content="" />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
