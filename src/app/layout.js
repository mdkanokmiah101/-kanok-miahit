/**
 * Md Kanok Miah — SEO Expert in Dhaka, Bangladesh
 * Built with Next.js 16
 * Last deployed: 2026-07-09 (SEO audit fixes)
 */
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// ISR: revalidate every 60s for CDN freshness (middleware further limits s-maxage)
export const revalidate = 60;

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// NO metadata export in root layout — it prevents page-level metadata
// from appearing in this Next.js version. Each page defines its own
// metadata via server-component page.js exports.
// metadataBase and icons are set via hardcoded <link> tags in <head> below.

// JSON-LD schemas defined as objects for reliable SSR rendering
const organizationSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Md Kanok Miah",
  url: "https://kanokmiah.com.bd",
  logo: "https://kanokmiah.com.bd/favicon.ico",
  description: "Bangladesh-focused SEO expert. Local SEO, technical SEO, link building, semantic SEO, and GEO optimization.",
  address: { "@type": "PostalAddress", streetAddress: "Mirpur, Dhaka", addressLocality: "Dhaka", addressCountry: "BD" },
  contactPoint: {
    "@type": "ContactPoint", telephone: "+880-1712-883101", contactType: "customer service",
    availableLanguage: ["English", "Bengali"],
  },
  sameAs: [
    "https://kanokmiah.com", "https://www.facebook.com/mdkanokmiahweb",
    "https://bd.linkedin.com/in/kanok-miah", "https://www.youtube.com/@kanokmiah",
    "https://www.pinterest.com/mdkanokmiah", "https://www.instagram.com/kanokmiahbd",
    "https://www.tiktok.com/@kanokmiahbd", "https://wa.me/8801712883101",
  ],
  foundingDate: "2020",
  founder: {
    "@type": "Person",
    name: "Md Kanok Miah",
    url: "https://kanokmiah.com.bd/about",
  },
  knowsAbout: [
    "Search Engine Optimization", "Local SEO", "Technical SEO", "Link Building",
    "Semantic SEO", "GEO / AI Search Optimization", "E-commerce SEO",
    "Content Marketing", "Google Business Profile Optimization", "Generative Engine Optimization",
  ],
};

const localBusinessSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert",
  url: "https://kanokmiah.com.bd",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Best SEO expert in Dhaka, Bangladesh. Specializing in Local SEO, Technical SEO, Link Building, and GEO optimization.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Mirpur, Dhaka", addressLocality: "Dhaka", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "23.8103", longitude: "90.4125" },
  priceRange: "$$",
  openingHours: "Mo-Fr 09:00-18:00",
  areaServed: ["Dhaka", "Mirpur", "Gulshan", "Banani", "Uttara", "Dhanmondi", "Chittagong", "Sylhet", "Bangladesh"],
  hasOfferCatalog: {
    "@type": "OfferCatalog",
    name: "SEO Services",
    itemListElement: [
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "Local SEO" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "On-Page SEO" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "Technical SEO" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "Link Building" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "Semantic SEO" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "GEO / AI Search" } },
      { "@type": "Offer", itemOffered: { "@type": "Service", name: "E-commerce SEO" } },
    ],
  },
  aggregateRating: {
    "@type": "AggregateRating", ratingValue: "4.9", bestRating: "5", ratingCount: "50",
  },
};

const webSiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Md Kanok Miah",
  url: "https://kanokmiah.com.bd",
  description: "Best SEO expert in Dhaka, Bangladesh. Get higher rankings, more traffic, and qualified leads with proven SEO strategies.",
  inLanguage: ["en"],
  potentialAction: {
    "@type": "SearchAction",
    target: { "@type": "EntryPoint", urlTemplate: "https://kanokmiah.com.bd/blog?q={search_term_string}" },
    "query-input": "required name=search_term_string",
  },
};

const personSchema = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "Md Kanok Miah",
  alternateName: "Kanok Miah",
  givenName: "Kanok",
  familyName: "Miah",
  url: "https://kanokmiah.com.bd",
  sameAs: [
    "https://kanokmiah.com", "https://www.facebook.com/mdkanokmiahweb",
    "https://bd.linkedin.com/in/kanok-miah", "https://www.youtube.com/@kanokmiah",
    "https://www.pinterest.com/mdkanokmiah", "https://www.instagram.com/kanokmiahbd",
    "https://www.tiktok.com/@kanokmiahbd", "https://wa.me/8801712883101",
  ],
  jobTitle: "SEO Expert & Digital Marketing Specialist",
  worksFor: { "@type": "Organization", name: "Md Kanok Miah" },
  knowsAbout: [
    "Search Engine Optimization", "Local SEO", "Technical SEO", "Link Building",
    "Semantic SEO", "GEO / AI Search Optimization", "E-commerce SEO",
    "Content Marketing", "Google Business Profile Optimization", "Generative Engine Optimization",
  ],
  description: "Best SEO expert in Dhaka, Bangladesh with 6+ years of experience. Specializing in local SEO, technical SEO, link building, and GEO optimization.",
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        {/* Search Console & Bing verification */}
        <meta name="google-site-verification" content="etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM" />
        <meta name="msvalidate.01" content="A10B9573E2B9D84E27B9BCE37CCB8B28" />
        {/* Hreflang - only English content currently exists */}
        <link rel="alternate" hrefLang="en" href="https://kanokmiah.com.bd" />
        <link rel="alternate" hrefLang="x-default" href="https://kanokmiah.com.bd" />
        {/* Apple Touch Icon for iOS bookmarks */}
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png" />
        <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png" />
        {/* Fallback favicon for all pages (since root layout has no metadata export) */}
        <link rel="icon" href="/favicon.ico" sizes="32x32" type="image/png" />
        <link rel="icon" href="/favicon.ico" />
        {/* Force og:image for all pages (critical for client-component pages like homepage) */}
        <meta property="og:image" content="https://kanokmiah.com.bd/kanok-miah-profile.webp" />
        <meta property="og:image:width" content="400" />
        <meta property="og:image:height" content="400" />
        <meta property="og:image:alt" content="Md Kanok Miah — Best SEO Expert in Dhaka, Bangladesh" />
        {/* Force twitter:image for all pages (critical for client-component pages) */}
        <meta name="twitter:image" content="https://kanokmiah.com.bd/kanok-miah-profile.webp" />
        <meta name="twitter:card" content="summary_large_image" />
        {/* Robots fallback for pages without their own robots meta */}
        <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
        {/* Deploy version tag */}
        <meta name="deploy-version" content="2026-07-10-v36-cdn-fix" />
      </head>
      <body className="min-h-full flex flex-col">
        {/* JSON-LD Structured Data — in <body> for Next.js SSR compatibility */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(webSiteSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(personSchema) }} />
        {children}
      </body>
    </html>
  );
}
