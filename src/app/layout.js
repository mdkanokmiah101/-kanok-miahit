import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SchemaOrg from "@/components/Schema";
import WhatsAppWidget from "@/components/WhatsAppWidget";
import Link from "next/link";

export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
    template: "%s — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
  },
  description:
    "Md Kanok Miah — SEO Expert in Dhaka, Bangladesh since 2019. 210+ SEO projects, 108 verified reviews. White-hat SEO, Local SEO, Technical SEO, GEO services.",
  keywords: [
    "SEO Expert Dhaka",
    "SEO Expert Bangladesh",
    "Md Kanok Miah",
    "Local SEO Dhaka",
    "Technical SEO",
    "GEO Optimization",
    "Digital Marketing Bangladesh",
  ],
  alternates: {
    canonical: "https://kanokmiah.com.bd",
  },
  openGraph: {
    title: "Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
    description:
      "Best SEO expert in Dhaka since 2019. 210+ SEO projects, 108 verified reviews. White-hat SEO, Local SEO, Technical SEO, GEO services.",
    url: "https://kanokmiah.com.bd",
    siteName: "Md Kanok Miah — SEO Expert Dhaka",
    images: [
      {
        url: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
        width: 400,
        height: 400,
        alt: "Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
    description:
      "Best SEO expert in Dhaka since 2019. 210+ SEO projects, 108 verified reviews.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  other: {
    "google-site-verification": "YOUR_VERIFICATION_CODE_HERE",
  },
};

const localBusinessSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah",
  description:
    "SEO Expert in Dhaka, Bangladesh. White-hat SEO, Local SEO, Technical SEO, GEO services since 2019.",
  url: "https://kanokmiah.com.bd",
  telephone: "+8801604809110",
  email: "mdkanokmiah101@gmail.com",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  priceRange: "BDT 15,000–50,000",
  address: {
    "@type": "PostalAddress",
    addressLocality: "Dhaka",
    addressCountry: "BD",
  },
  areaServed: [
    {
      "@type": "City",
      name: "Dhaka",
      sameAs: "https://en.wikipedia.org/wiki/Dhaka",
    },
  ],
  knowsAbout: [
    "Search Engine Optimization",
    "Local SEO",
    "Technical SEO",
    "E-commerce SEO",
    "Semantic SEO",
    "Generative Engine Optimization",
    "Google Business Profile Optimization",
    "Link Building",
    "Content Marketing",
    "Keyword Research",
    "SEO Audit",
    "Core Web Vitals",
    "Structured Data",
    "AI Search Optimization",
  ],
  hasOfferCatalog: {
    "@type": "OfferCatalog",
    name: "SEO Services",
    itemListElement: [
      {
        "@type": "Offer",
        itemOffered: {
          "@type": "Service",
          name: "Local SEO",
          url: "https://kanokmiah.com.bd/services/local-seo",
        },
      },
      {
        "@type": "Offer",
        itemOffered: {
          "@type": "Service",
          name: "Technical SEO",
          url: "https://kanokmiah.com.bd/services/technical-seo",
        },
      },
    ],
  },
  aggregateRating: {
    "@type": "AggregateRating", ratingValue: "4.9", bestRating: "5", ratingCount: "108",
  },
};

const webSiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Md Kanok Miah — SEO Expert Dhaka",
  url: "https://kanokmiah.com.bd",
  potentialAction: {
    "@type": "SearchAction",
    target: {
      "@type": "EntryPoint",
      urlTemplate: "https://kanokmiah.com.bd/?s={search_term_string}",
    },
    "query-input": "required name=search_term_string",
  },
};

const personSchema = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "Md Kanok Miah",
  jobTitle: "SEO Project Manager",
  worksFor: [
    { "@type": "Organization", name: "Khan IT" },
    { "@type": "Organization", name: "CloudMatrix Tech" },
  ],
  url: "https://kanokmiah.com.bd",
  sameAs: [
    "https://linkedin.com/in/md-kanok-miah",
    "https://maps.google.com/?cid=YOUR_GBP_ID",
  ],
  knowsAbout: ["SEO", "Digital Marketing", "Local SEO", "Technical SEO", "GEO"],
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <SchemaOrg schema={localBusinessSchema} />
        <SchemaOrg schema={webSiteSchema} />
        <SchemaOrg schema={personSchema} />
        <meta
          name="google-site-verification"
          content="YOUR_VERIFICATION_CODE_HERE"
        />
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link
          rel="apple-touch-icon"
          href="/apple-touch-icon.png"
          type="image/png"
          sizes="180x180"
        />
      </head>
      <body className="min-h-screen bg-white text-gray-900 antialiased flex flex-col">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
        <WhatsAppWidget />
      </body>
    </html>
  );
}
