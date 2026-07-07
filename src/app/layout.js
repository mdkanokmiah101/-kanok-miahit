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
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: "Best SEO Agency in Dhaka | Md Kanok Miah — #1 SEO in Bangladesh",
  description:
    "Looking for the best SEO agency in Dhaka? Md Kanok Miah is Bangladesh's top-rated SEO company. Get higher rankings, more traffic, and qualified leads with proven SEO strategies. Local SEO, Technical SEO, Link Building, GEO — Dhaka, Bangladesh.",
  keywords: [
    "best SEO agency in Dhaka",
    "SEO agency Dhaka",
    "SEO company in Bangladesh",
    "local SEO Bangladesh",
    "Bangladesh SEO expert",
    "digital marketing agency Bangladesh",
    "on-page SEO",
    "technical SEO",
    "link building Bangladesh",
    "GEO optimization",
    "Md Kanok Miah",
  ],
  authors: [{ name: "Md Kanok Miah" }],
  creator: "Md Kanok Miah",
  publisher: "Md Kanok Miah",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "Best SEO Agency in Dhaka | Md Kanok Miah — #1 SEO in Bangladesh",
    description:
      "Looking for the best SEO agency in Dhaka? Md Kanok Miah is Bangladesh's top-rated SEO company. Get higher rankings and more traffic with proven SEO strategies.",
    url: "https://kanokmiah.com.bd",
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Agency in Dhaka | Md Kanok Miah — #1 SEO in Bangladesh",
    description:
      "Looking for the best SEO agency in Dhaka? Md Kanok Miah helps businesses rank higher, grow faster, dominate search.",
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
        {/* Canonical is managed via 'alternates.canonical' in metadata export */}
        {/* Schema: Organization */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              name: "Md Kanok Miah",
              url: "https://kanokmiah.com.bd",
              logo: "https://kanokmiah.com.bd/favicon.ico",
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
              sameAs: ["https://kanokmiah.com"],
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
              name: "Md Kanok Miah",
              url: "https://kanokmiah.com.bd",
              potentialAction: {
                "@type": "SearchAction",
                target:
                  "https://kanokmiah.com.bd/search?q={search_term_string}",
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
