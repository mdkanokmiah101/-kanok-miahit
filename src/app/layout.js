/**
 * Md Kanok Miah — SEO Expert in Dhaka, Bangladesh
 * Built with Next.js 16
 * Last deployed: 2026-07-09 (SEO audit fixes)
 */
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

// Fully static — all content is pre-built at deploy time.
// Cache-Control (s-maxage=60, must-revalidate) is set via next.config.mjs headers.
export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah \u2014 #1 SEO Specialist",
    template: "%s \u2014 Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
  },
  description:
    "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah is a top-rated SEO specialist with 6+ years of experience. Get higher rankings, more traffic, and qualified leads with proven SEO strategies. Local SEO, Technical SEO, Link Building, GEO \u2014 Dhaka, Bangladesh.",
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
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah \u2014 #1 SEO Specialist",
    description:
      "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah is a top-rated SEO specialist. Get higher rankings, more traffic, and qualified leads with proven SEO strategies. Local SEO, Technical SEO, Link Building, GEO \u2014 Dhaka, Bangladesh.",
    url: "https://kanokmiah.com.bd",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 Best SEO Expert in Dhaka, Bangladesh" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah \u2014 #1 SEO Specialist",
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
  address: { "@type": "PostalAddress", addressLocality: "Dhaka", addressCountry: "BD" },
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
  address: { "@type": "PostalAddress", addressLocality: "Dhaka", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "23.8103", longitude: "90.4125" },
  priceRange: "$$",
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
    "@type": "AggregateRating", ratingValue: "5.0", bestRating: "5", ratingCount: "108",
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
        {/* Search Console verification */}
        <meta name="google-site-verification" content="etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM" />
        {/* JSON-LD Structured Data — all 4 schemas render on every page */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(webSiteSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(personSchema) }} />
      </head>
      <body className="min-h-full flex flex-col">
        {children}
      </body>
    </html>
  );
}
