/**
 * Md Kanok Miah — SEO Expert in Dhaka, Bangladesh
 * Built with Next.js 16
 * Last deployed: 2026-07-09 (SEO audit fixes)
 */
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Prevent Hostinger hCDN from caching pages for 1 year
export const dynamic = "force-dynamic";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Dynamic rendering removed — static generation enabled for full metadata support
export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "Best SEO Expert in Dhaka | Md Kanok Miah \u2014 #1 Specialist",
    template: "%s \u2014 Md Kanok Miah | SEO Expert Dhaka",
  },
  description:
    "Best SEO expert in Dhaka \u2014 Md Kanok Miah. 6+ years in Local SEO, Technical SEO, Link Building & GEO. Get higher rankings and qualified leads.",
  keywords: [
    "best SEO expert in Dhaka",
    "SEO expert Dhaka",
    "SEO specialist Bangladesh",
    "local SEO Bangladesh",
    "Bangladesh SEO expert",
    "SEO consultant Dhaka",
    "on-page SEO",
    "technical SEO",
    "link building Bangladesh",
    "semantic SEO",
    "GEO optimization",
    "Md Kanok Miah",
  ],
  authors: [{ name: "Md Kanok Miah" }],
  creator: "Md Kanok Miah",
  publisher: "Md Kanok Miah",
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "Best SEO Expert in Dhaka | Md Kanok Miah \u2014 #1 SEO Specialist",
    description:
      "Best SEO expert in Dhaka, Bangladesh \u2014 Md Kanok Miah. 6+ years experience in Local SEO, Technical SEO, Link Building, and GEO. Get higher rankings.",
    url: "https://kanokmiah.com.bd",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 Best SEO Expert in Dhaka, Bangladesh" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka | Md Kanok Miah",
    description:
      "Looking for the best SEO expert in Dhaka? Md Kanok Miah helps businesses rank higher, grow faster, and dominate search.",
    images: ["/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
  icons: {
    icon: [{ url: "/favicon.ico", sizes: "32x32", type: "image/png" }],
    apple: "/icon-192.png",
  },
};

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
  inLanguage: ["en", "bn"],
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
        {/* Hreflang for bilingual audience */}
        <link rel="alternate" hrefLang="en" href="https://kanokmiah.com.bd" />
        <link rel="alternate" hrefLang="bn" href="https://kanokmiah.com.bd" />
        <link rel="alternate" hrefLang="x-default" href="https://kanokmiah.com.bd" />
        {/* Apple Touch Icon for iOS bookmarks */}
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png" />
        <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png" />
        {/* Force og:image for all pages (critical for client-component pages like homepage) */}
        <meta property="og:image" content="https://kanokmiah.com.bd/kanok-miah-profile.webp" />
        <meta property="og:image:width" content="400" />
        <meta property="og:image:height" content="400" />
        <meta property="og:image:alt" content="Md Kanok Miah — Best SEO Expert in Dhaka, Bangladesh" />
        {/* Deploy version tag */}
        <meta name="deploy-version" content="2026-07-10-v18-canonical-fix" />
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
