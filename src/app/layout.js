/**
 * Md Kanok Miah — SEO Expert in Dhaka, Bangladesh
 * Built with Next.js 16
 * Last deployed: 2026-07-09 (SEO audit fixes — schemas via next/script for SSR)
 */
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Script from "next/script";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const dynamic = 'force-dynamic';

export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    template: "%s \u2014 Md Kanok Miah",
  },
  description:
    "Md Kanok Miah \u2014 top SEO expert in Dhaka, Bangladesh. 6+ years experience. Higher rankings, more traffic, qualified leads. Local SEO, Technical SEO, Link Building, GEO.",
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
    title: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    description:
      "Md Kanok Miah \u2014 top SEO expert in Dhaka, Bangladesh. Higher rankings, more traffic, qualified leads.",
    url: "https://kanokmiah.com.bd",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
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
  other: {
    "google-site-verification": "etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM",
    "msvalidate.01": "",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {/* JSON-LD Structured Data — next/script with beforeInteractive renders during SSR */}
        <Script id="schema-organization" type="application/ld+json" strategy="beforeInteractive">
          {`{"@context":"https://schema.org","@type":"Organization","name":"Md Kanok Miah","url":"https://kanokmiah.com.bd","logo":"https://kanokmiah.com.bd/favicon.ico","description":"Bangladesh-focused SEO expert. Local SEO, technical SEO, link building, semantic SEO, and GEO optimization.","address":{"@type":"PostalAddress","addressLocality":"Dhaka","addressCountry":"BD"},"contactPoint":{"@type":"ContactPoint","telephone":"+880-1712-883101","contactType":"customer service","availableLanguage":["English","Bengali"]},"sameAs":["https://kanokmiah.com","https://www.facebook.com/mdkanokmiahweb","https://bd.linkedin.com/in/kanok-miah","https://www.youtube.com/@kanokmiah","https://www.pinterest.com/mdkanokmiah","https://www.instagram.com/kanokmiahbd","https://www.tiktok.com/@kanokmiahbd","https://wa.me/8801712883101"],"foundingDate":"2020","knowsAbout":["Search Engine Optimization","Local SEO","Technical SEO","Link Building","Semantic SEO","GEO / AI Search Optimization","E-commerce SEO","Content Marketing","Google Business Profile Optimization","Generative Engine Optimization"]}`}
        </Script>
        <Script id="schema-localbusiness" type="application/ld+json" strategy="beforeInteractive">
          {`{"@context":"https://schema.org","@type":"LocalBusiness","name":"Md Kanok Miah \u2014 SEO Expert","url":"https://kanokmiah.com.bd","telephone":"+880-1712-883101","email":"mdkanokmiah232@gmail.com","description":"Best SEO expert in Dhaka, Bangladesh. Specializing in Local SEO, Technical SEO, Link Building, and GEO optimization.","image":"https://kanokmiah.com.bd/kanok-miah-profile.webp","address":{"@type":"PostalAddress","addressLocality":"Dhaka","addressCountry":"BD"},"geo":{"@type":"GeoCoordinates","latitude":"23.8103","longitude":"90.4125"},"priceRange":"$$","areaServed":["Dhaka","Mirpur","Gulshan","Banani","Uttara","Dhanmondi","Chittagong","Sylhet","Bangladesh"],"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","bestRating":"5","ratingCount":"50"}}`}
        </Script>
        <Script id="schema-website" type="application/ld+json" strategy="beforeInteractive">
          {`{"@context":"https://schema.org","@type":"WebSite","name":"Md Kanok Miah","url":"https://kanokmiah.com.bd","description":"Best SEO expert in Dhaka, Bangladesh. Get higher rankings, more traffic, and qualified leads with proven SEO strategies.","inLanguage":["en","bn"],"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https://kanokmiah.com.bd/blog?q={search_term_string}"},"query-input":"required name=search_term_string"}}`}
        </Script>
        <Script id="schema-person" type="application/ld+json" strategy="beforeInteractive">
          {`{"@context":"https://schema.org","@type":"Person","name":"Md Kanok Miah","alternateName":"Kanok Miah","givenName":"Kanok","familyName":"Miah","url":"https://kanokmiah.com.bd","sameAs":["https://kanokmiah.com","https://www.facebook.com/mdkanokmiahweb","https://bd.linkedin.com/in/kanok-miah","https://www.youtube.com/@kanokmiah","https://www.pinterest.com/mdkanokmiah","https://www.instagram.com/kanokmiahbd","https://www.tiktok.com/@kanokmiahbd"],"jobTitle":"SEO Expert & Digital Marketing Specialist","worksFor":{"@type":"Organization","name":"Md Kanok Miah"},"description":"Best SEO expert in Dhaka, Bangladesh with 6+ years of experience. Specializing in local SEO, technical SEO, link building, and GEO optimization."`}
        </Script>
        {children}
      </body>
    </html>
  );
}
